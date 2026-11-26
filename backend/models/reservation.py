from ..app import db
from datetime import datetime, timedelta
def get_ist_time():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'))
    vehicle_number = db.Column(db.String(20))
    parking_timestamp = db.Column(db.DateTime, default=get_ist_time)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, nullable=True)
    remarks = db.Column(db.String(256), nullable=True)