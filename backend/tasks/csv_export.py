from flask import current_app
from ..models.user import User
from ..models.reservation import Reservation
from ..app import db
import csv
import io
from flask_mail import Message
from backend.celery_app import celery_app
celery = None
@celery_app.task(bind=True)
def export_user_parking_history_impl(user_id):
    with current_app.app_context():
        user = User.query.get(user_id)
        if not user:
            print(f"User {user_id} not found")
            return
        reservations = Reservation.query.filter_by(user_id=user_id).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Slot ID', 'Spot ID', 'Vehicle Number', 'Parking In', 'Parking Out', 'Cost', 'Remarks'])
        for r in reservations:
            writer.writerow([
                r.id,
                r.spot_id,
                r.vehicle_number,
                r.parking_timestamp,
                r.leaving_timestamp,
                r.parking_cost,
                r.remarks
            ])
        csv_content = output.getvalue()
        output.close()
        try:
            mail = current_app.extensions['mail']
            msg = Message(
                subject="Your Parking History Export",
                recipients=[user.email],
                body="See the attached CSV file for your parking history."
            )
            msg.attach("parking_history.csv", "text/csv", csv_content)
            mail.send(msg)
            print(f"CSV export sent to {user.email}")
        except Exception as e:
            print(f"Failed to send CSV to {user.email}: {e}")
export_user_parking_history = None
def get_task():
    return export_user_parking_history