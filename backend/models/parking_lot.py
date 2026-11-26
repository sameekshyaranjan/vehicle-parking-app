from ..app import db
class ParkingLot(db.Model):
    __tablename__ = 'parking_lot'
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(128))
    price = db.Column(db.Float)
    address = db.Column(db.String(256))
    pin_code = db.Column(db.String(10))
    number_of_spots = db.Column(db.Integer)
    spots = db.relationship('ParkingSpot', backref='parking_lot', lazy=True, cascade="all, delete-orphan")
    def get_available_spots(self):
        from .parking_spot import ParkingSpot
        return ParkingSpot.query.filter_by(lot_id=self.id, status='A').all()
    def to_dict(self):
        return {
            'lot_id': self.id,
            'prime_location_name': self.prime_location_name,
            'price': self.price,
            'address': self.address,
            'pin_code': self.pin_code,
            'number_of_spots': self.number_of_spots,
            'available_spots':len(self.get_available_spots()),
            'occupied_spots': self.number_of_spots - len(self.get_available_spots())
        }