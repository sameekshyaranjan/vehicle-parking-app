import os
import dotenv
from click import ClickException, echo
from datetime import timedelta
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import redis
from .celery_app import celery_app
from .database import sqlalchemy_database_url
from .tasks.celery_config import configure_celery
dotenv.load_dotenv()
db = SQLAlchemy()
jwt = JWTManager()
def register_commands(app):
    pass
def create_app(config_name='development'):
    instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
    app = Flask(__name__, instance_path=instance_path)
    database_url = os.environ.get('SQLALCHEMY_DATABASE_URI') or os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_url(database_url or 'sqlite:///parking.db')
    if app.config['SQLALCHEMY_DATABASE_URI'].get_backend_name() == 'mysql':
        # Read availability after acquiring the booking locks, including when JWT lookup ran earlier.
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'isolation_level': 'READ COMMITTED', 'pool_pre_ping': True}
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-string-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['DEMO_LOGIN_ENABLED'] = os.environ.get('PARKSMART_DEMO_LOGIN') == '1'
    app.config['MAX_PARKING_SPOTS_PER_LOT'] = 1000
    app.extensions['celery'] = celery_app
    app.config['REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    app.config['CELERY_BROKER_URL'] = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    app.config['CELERY_RESULT_BACKEND'] = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')
    app.redis = None
    if app.config['REDIS_URL']:
        try:
            client = redis.from_url(app.config['REDIS_URL'])
            if client.ping():
                app.redis = client
                print("✅ Successfully connected to Redis!")
        except redis.exceptions.ConnectionError as e:
            print(f"❌ Could not connect to Redis: {e}")
        except Exception as e:
            print(f"An error occurred during Redis initialization: {e}")
    initialize_extensions(app)
    CORS(app)
    register_blueprints(app)
    register_commands(app)
    configure_celery(app, celery_app)
    return app
def initialize_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    with app.app_context():
        from .models.user import User
        @jwt.user_identity_loader
        def user_identity_lookup(user):
            if hasattr(user, 'id'):
                return str(user.id)
            return str(user)
        @jwt.user_lookup_loader
        def user_lookup_callback(_jwt_header, jwt_data):
            identity = jwt_data["sub"]
            try:
                return User.query.filter_by(id=int(identity)).one_or_none()
            except (ValueError, TypeError):
                return None
        @jwt.expired_token_loader
        def expired_token_callback(jwt_header, jwt_payload):
            return jsonify({
                'error': True,
                'message': 'Token has expired'
            }), 401
        @jwt.invalid_token_loader
        def invalid_token_callback(error):
            return jsonify({
                'error': True,
                'message': 'Invalid token'
            }), 401
        @jwt.unauthorized_loader
        def missing_token_callback(error):
            return jsonify({
                'error': True,
                'message': 'Authorization token is required'
            }), 401
    print("✅ Flask extensions initialized")
def register_blueprints(app):
    try:
        from .auth.routes import auth_bp
        from .routes.admin_routes import admin_bp
        from .routes.user_routes import user_bp
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(admin_bp, url_prefix='/api/admin')
        app.register_blueprint(user_bp, url_prefix='/api/user')
        print("✅ Blueprints registered successfully:")
        print("   - Auth routes: /api/auth/*")
        print("   - Admin routes: /api/admin/*")
        print("   - User routes: /api/user/*")
    except ImportError as e:
        print(f"❌ Blueprint import error: {e}")
        raise
def register_commands(app):
    @app.cli.command("init-db")
    def init_db_command():
        with app.app_context():
            dialect = db.engine.dialect.name
            if dialect != 'sqlite':
                command = 'db:mysql:deploy' if dialect == 'mysql' else 'db:deploy'
                raise ClickException(f'Apply the database schema with npm run {command}.')
            db.create_all()
        print("✅ Database tables created successfully!")
    @app.cli.command("create-admin")
    def create_admin_command():
        from .models.user import User
        from werkzeug.security import generate_password_hash
        with app.app_context():
            if User.query.filter_by(is_admin=True).first():
                print("🔶 Admin user already exists.")
                return
            admin_user = User(
                username='admin',
                password=generate_password_hash('admin123'),
                fullname='System Administrator',
                email='admin@parkingapp.com',
                address='System Address',
                pin_code='000000',
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Default admin user created successfully!")
            print("   - Username: admin")
            print("   - Password: admin123")
    @app.cli.command('create-demo-accounts')
    def create_demo_accounts_command():
        from .auth.demo import DEMO_ACCOUNTS, DEMO_PASSWORD, find_demo_account
        from .models.user import User

        for role, (username, fullname, is_admin) in DEMO_ACCOUNTS.items():
            if find_demo_account(role):
                continue
            email = f'{username}@demo.invalid'
            if User.query.filter((User.username == username) | (User.email == email)).first():
                raise ClickException(f'An existing account conflicts with {username}.')
            db.session.add(User(
                username=username,
                password=DEMO_PASSWORD,
                fullname=fullname,
                email=email,
                address='Demo Address',
                pin_code='000000',
                is_admin=is_admin,
            ))
        db.session.commit()
        print('Demo user and demo admin accounts are ready.')
    @app.cli.command('seed-demo-data')
    def seed_demo_data_command():
        from .demo_data import seed_demo_data

        lots, completed, active = seed_demo_data()
        if app.redis and (lots or completed or active):
            try:
                app.redis.delete('admin_dashboard_stats', 'available_parking_lots')
            except redis.exceptions.RedisError:
                app.logger.warning('Demo data saved. The dashboard cache could not be cleared.')
        echo(f'Demo data added: {lots} lots, {completed} completed bookings, {active} active bookings.')
if __name__ == '__main__':
    app = create_app()
    print("🚗 Flask app created successfully!")
    print("💡 Use 'python run.py' to start the application")
