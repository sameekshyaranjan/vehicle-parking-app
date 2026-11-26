from ..app import db
class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'))
    status = db.Column(db.String(1), default='A')
    spot_number = db.Column(db.Integer)
    reservations = db.relationship('Reservation', backref='spot', lazy=True)