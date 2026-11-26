"""
Celery task: Send daily reminders to users.
"""
from flask import current_app
from ..models.user import User
from ..app import db
from backend.celery_app import celery_app
import smtplib
from ..utils.email_service import send_email
import requests
import os
def send_google_chat_reminder(user_name, user_email):
    webhook_url = os.environ.get('GOOGLE_CHAT_WEBHOOK_URL')
    if webhook_url:
        message = {
            "text": f"Hello *{user_name}*,\n\nThis is a friendly reminder to book your parking spot for today if you haven't already. Don't miss out on the best spots!\n\n- The ParkSmart Team"
        }
        try:
            response = requests.post(webhook_url, json=message)
            response.raise_for_status()
            print(f"Sent Google Chat reminder to {user_name}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send Google Chat reminder to {user_name}: {e}")
@celery_app.task
def send_daily_reminders():
    """
    Send daily reminders to users who have not booked a spot today.
    """
    with current_app.app_context():
        from ..models.reservation import Reservation
        from datetime import datetime, timedelta
        users = User.query.filter_by(is_admin=False).all()
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        for user in users:
            has_booking = Reservation.query.filter(
                Reservation.user_id == user.id,
                Reservation.parking_timestamp >= today,
                Reservation.parking_timestamp < tomorrow
            ).count() > 0
            if not has_booking:
                try:
                    subject = "Don't Forget to Book Your Parking Spot!"
                    html_body = f"""
                    <p>Hi {user.fullname},</p>
                    <p>Just a friendly reminder to book your parking spot for today if you haven't already. The best spots get filled up quickly!</p>
                    <p>Best,<br>The ParkSmart Team</p>
                    """
                    send_email(user.email, subject, html_body)
                    print(f"Sending email reminder to {user.email}")
                except Exception as e:
                    print(f"Failed to send email reminder to {user.email}: {e}")
                send_google_chat_reminder(user.fullname, user.email)