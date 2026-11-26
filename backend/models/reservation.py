from datetime import datetime, timedelta
from math import ceil

from sqlalchemy.dialects.mysql import DATETIME, DOUBLE

from ..app import db
def get_ist_time():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)
class Reservation(db.Model):
    __table_args__ = (
        db.Index(
            'reservation_one_active_per_spot', 'spot_id', unique=True,
            postgresql_where=db.text('leaving_timestamp IS NULL'),
            sqlite_where=db.text('leaving_timestamp IS NULL'),
        ).ddl_if(dialect=('postgresql', 'sqlite')),
        db.Index(
            'reservation_one_active_per_user', 'user_id', unique=True,
            postgresql_where=db.text('leaving_timestamp IS NULL'),
            sqlite_where=db.text('leaving_timestamp IS NULL'),
        ).ddl_if(dialect=('postgresql', 'sqlite')),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id', ondelete='SET NULL'))
    vehicle_number = db.Column(db.Text)
    parking_timestamp = db.Column(db.DateTime().with_variant(DATETIME(fsp=6), 'mysql'), default=get_ist_time)
    leaving_timestamp = db.Column(db.DateTime().with_variant(DATETIME(fsp=6), 'mysql'), nullable=True)
    parking_cost = db.Column(db.Float().with_variant(DOUBLE(asdecimal=False), 'mysql'), nullable=True)
    remarks = db.Column(db.Text, nullable=True)

    def release(self, leaving_time, rating):
        duration = leaving_time - self.parking_timestamp
        hours_parked = max(1, ceil(duration.total_seconds() / 3600))
        spot = self.spot
        final_cost = spot.parking_lot.price * hours_parked
        self.leaving_timestamp = leaving_time
        self.parking_cost = final_cost
        self.remarks = f'User Rating: {rating}/5'
        spot.status = 'A'
        return hours_parked
