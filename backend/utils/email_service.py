"""
Email sending utility for Vehicle Parking App V2.
Replace with your actual email backend (Flask-Mail, SMTP, etc.).
"""
import smtplib
from email.mime.text import MIMEText
from flask import current_app
def send_email(to_email, subject, html_body, plain_body=None, attachment=None, attachment_filename=None):
    """
    Send an email.
    For production, use Flask-Mail or a transactional email service.
    """
    mail_server = current_app.config.get('MAIL_SERVER')
    mail_port = current_app.config.get('MAIL_PORT')
    mail_username = current_app.config.get('MAIL_USERNAME')
    mail_password = current_app.config.get('MAIL_PASSWORD')
    mail_from = mail_username
    msg = MIMEText(html_body, 'html')
    msg['Subject'] = subject
    msg['From'] = mail_from
    msg['To'] = to_email
    try:
        with smtplib.SMTP(mail_server, mail_port) as server:
            server.starttls()
            server.login(mail_username, mail_password)
            server.sendmail(mail_from, [to_email], msg.as_string())
        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Email sending failed to {to_email}: {e}")
        return False