from datetime import timedelta

from click import ClickException

from .app import db
from .auth.demo import find_demo_account
from .models import ParkingLot, ParkingSpot, Reservation, User
from .models.reservation import get_ist_time
from .models.reservation_audit import ReservationAudit


LOTS = {
    'cedar': ('Cedar Square Garage (Demo)', '18 Cedar Square Road, Bengaluru', '560001', 12, 45),
    'maple': ('Maple Junction Parking (Demo)', '42 Maple Arcade Lane, Bengaluru', '560038', 10, 55),
    'lake': ('Lakeview Arcade Parking (Demo)', '7 Lakeview Arcade Road, Bengaluru', '560102', 8, 40),
    'orchid': ('Orchid Business Centre (Demo)', '26 Orchid Crescent, Bengaluru', '560066', 14, 70),
}
# The reserved fictional plates identify each booking for Demo User across retries and releases.
HISTORY = (
    ('KA00PS8101', 'cedar', timedelta(minutes=10), timedelta(minutes=48), 5),
    ('KA00PS8102', 'maple', timedelta(days=1, hours=5), timedelta(hours=1, minutes=24), 4),
    ('KA00PS8103', 'orchid', timedelta(days=3, hours=3), timedelta(hours=2, minutes=10), 5),
    ('KA00PS8104', 'lake', timedelta(days=6), timedelta(minutes=55), 4),
    ('KA00PS8105', 'cedar', timedelta(days=12, hours=7), timedelta(hours=1, minutes=35), 5),
    ('KA00PS8106', 'maple', timedelta(days=19, hours=4), timedelta(hours=3, minutes=5), 4),
)
ACTIVE_PLATE = 'KA00PS8107'


def demo_lot(details):
    name, address, pin_code, capacity, hourly_rate = details
    matches = db.session.scalars(
        db.select(ParkingLot).where(ParkingLot.prime_location_name == name).limit(2).with_for_update()
    ).all()
    if matches:
        lot = matches[0]
        if len(matches) != 1 or (lot.address, lot.pin_code) != (address, pin_code):
            raise ClickException(f'An existing lot conflicts with {name}.')
        return lot, False

    lot = ParkingLot(
        prime_location_name=name, address=address, pin_code=pin_code,
        price=hourly_rate, number_of_spots=capacity,
        spots=[ParkingSpot(spot_number=number) for number in range(1, capacity + 1)],
    )
    db.session.add(lot)
    db.session.flush()
    return lot, True


def park(lot, plate, parked_at, user_id=None):
    spot = db.session.scalar(
        db.select(ParkingSpot).filter_by(lot_id=lot.id, status='A')
        .order_by(ParkingSpot.spot_number, ParkingSpot.id).limit(1).with_for_update()
    )
    if spot is None:
        raise ClickException(f'No free spot in {lot.prime_location_name}.')
    reservation = Reservation(
        user_id=user_id, spot=spot, vehicle_number=plate,
        parking_timestamp=parked_at, parking_cost=lot.price,
    )
    spot.status = 'O'
    db.session.add(reservation)
    db.session.flush()
    return reservation


def seed_demo_data():
    if db.engine.dialect.name != 'mysql':
        raise ClickException('Point ParkSmart at the migrated MySQL database before seeding demo data.')

    with db.session.begin():
        user = find_demo_account('user')
        if user is None or find_demo_account('admin') is None:
            raise ClickException('Run create-demo-accounts before seeding demo data.')
        # The normal booking flow takes the same lock before checking for an active reservation.
        db.session.execute(db.select(User.id).where(User.id == user.id).with_for_update()).scalar_one()
        bookings = db.session.execute(
            db.select(Reservation.vehicle_number, Reservation.leaving_timestamp).filter_by(user_id=user.id)
        ).all()
        plates = {plate for plate, _ in bookings}
        already_active = any(leaving is None for _, leaving in bookings)

        lots = {}
        lots_created = 0
        for key, details in LOTS.items():
            lots[key], created = demo_lot(details)
            lots_created += created

        now = get_ist_time().replace(microsecond=0)
        released_ids = []
        for plate, lot_key, release_age, duration, rating in HISTORY:
            if plate in plates:
                continue
            leaving_time = now - release_age
            # Stage the historical booking in this transaction without competing with the user's active one.
            reservation = park(lots[lot_key], plate, leaving_time - duration)
            reservation.release(leaving_time, rating)
            reservation.user_id = user.id
            db.session.flush()
            released_ids.append(reservation.id)

        if released_ids:
            recorded_ids = db.session.scalars(
                db.select(ReservationAudit.reservation_id).where(
                    ReservationAudit.reservation_id.in_(released_ids), ReservationAudit.event_type == 'RELEASED'
                )
            ).all()
            if sorted(recorded_ids) != sorted(released_ids):
                raise ClickException('Expected one MySQL release audit per booking. Check the audit migration.')

        active_created = not already_active and ACTIVE_PLATE not in plates
        if active_created:
            park(lots['orchid'], ACTIVE_PLATE, now - timedelta(minutes=32), user_id=user.id)

    return lots_created, len(released_ids), int(active_created)
