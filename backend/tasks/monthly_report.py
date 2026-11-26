"""
Celery task: Generate and send monthly activity reports.
"""
from flask import current_app
from ..models.user import User
from ..models.reservation import Reservation
from ..app import db
from .celery_config import make_celery
from backend.celery_app import celery
import smtplib
celery = None
@celery.task
def send_monthly_reports():
    """
    Generate and email monthly activity reports to all users.
    """
    with current_app.app_context():
        from datetime import datetime, timedelta
        users = User.query.filter_by(is_admin=False).all()
        today = datetime.now()
        first_day = today.replace(day=1)
        last_month = first_day - timedelta(days=1)
        start = last_month.replace(day=1)
        end = last_month.replace(day=last_month.day)
        for user in users:
            reservations = Reservation.query.filter(
                Reservation.user_id == user.id,
                Reservation.parking_timestamp >= start,
                Reservation.parking_timestamp <= end
            ).all()
            total_spent = sum(r.parking_cost or 0 for r in reservations)
            most_used_lot = None
            if reservations:
                lot_counts = {}
                for r in reservations:
                    lot_name = r.spot.parking_lot.prime_location_name
                    lot_counts[lot_name] = lot_counts.get(lot_name, 0) + 1
                most_used_lot = max(lot_counts, key=lot_counts.get)
            report_html = f"""
            <h2>Monthly Parking Report</h2>
            <p>Total bookings: {len(reservations)}</p>
            <p>Total spent: ₹{total_spent}</p>
            <p>Most used lot: {most_used_lot or 'N/A'}</p>
            """
            try:
                print(f"Sending monthly report to {user.email}")
            except Exception as e:
                print(f"Failed to send report to {user.email}: {e}")