from ..app import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    fullname = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    address = db.Column(db.String(256))
    pin_code = db.Column(db.String(10))
    is_admin = db.Column(db.Boolean, default=False)
    reservations = db.relationship('Reservation', backref='user', lazy=True)