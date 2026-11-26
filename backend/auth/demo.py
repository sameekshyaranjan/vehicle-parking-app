from urllib.parse import urlsplit

from flask import current_app, request

from ..models.user import User


DEMO_ACCOUNTS = {
    'user': ('demo_user', 'Demo User', False),
    'admin': ('demo_admin', 'Demo Admin', True),
}
DEMO_PASSWORD = '!demo-only'
DEMO_ORIGINS = {'http://localhost:8080', 'http://127.0.0.1:8080'}
LOOPBACK_HOSTS = {'localhost', '127.0.0.1', '::1'}


def demo_login_available():
    origin = request.headers.get('Origin')
    return (
        current_app.config['DEMO_LOGIN_ENABLED']
        and request.remote_addr in LOOPBACK_HOSTS
        and urlsplit(request.host_url).hostname in LOOPBACK_HOSTS
        and (origin is None or origin in DEMO_ORIGINS)
    )


def find_demo_account(role):
    username, _, is_admin = DEMO_ACCOUNTS[role]
    return User.query.filter_by(
        username=username,
        email=f'{username}@demo.invalid',
        password=DEMO_PASSWORD,
        is_admin=is_admin,
    ).one_or_none()
