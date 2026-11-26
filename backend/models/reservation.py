from ..app import db
from datetime import datetime, timedelta
from sqlalchemy.dialects.mysql import DATETIME, DOUBLE
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
