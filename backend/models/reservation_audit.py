from sqlalchemy.dialects.mysql import DATETIME, DOUBLE

from ..app import db


class ReservationAudit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, nullable=False)
    event_type = db.Column(db.Text, nullable=False)
    recorded_at = db.Column(
        db.DateTime(timezone=True).with_variant(DATETIME(fsp=6), 'mysql'),
        server_default=db.func.now(), nullable=False,
    )
    final_cost = db.Column(db.Float().with_variant(DOUBLE(asdecimal=False), 'mysql'))
