from ..app import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text().with_variant(db.String(512), 'mysql'), unique=True)
    password = db.Column(db.Text)
    fullname = db.Column(db.Text)
    email = db.Column(db.Text().with_variant(db.String(512), 'mysql'), unique=True)
    address = db.Column(db.Text)
    pin_code = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
    reservations = db.relationship('Reservation', backref='user', lazy=True)
