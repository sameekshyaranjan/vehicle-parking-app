# #!/usr/bin/env python3

# import os
# import sys
# from pathlib import Path

# # Add the backend directory to Python path
# backend_dir = Path(__file__).parent / 'backend'
# sys.path.insert(0, str(backend_dir))

# from app import create_app, db
# from models.user import User
# from models.parking_lot import ParkingLot
# from models.parking_spot import ParkingSpot
# from models.reservation import Reservation

# def create_admin_user(app):
#     with app.app_context():
#         admin = User.query.filter_by(is_admin=True).first()
#         if not admin:
#             from werkzeug.security import generate_password_hash
#             admin_user = User(
#                 username='admin',
#                 password=generate_password_hash('admin123'),
#                 fullname='System Administrator',
#                 email='admin@parkingapp.com',
#                 address='System Address',
#                 pin_code='000000',
#                 is_admin=True
#             )
#             db.session.add(admin_user)
#             db.session.commit()
#             print(" Default admin user created successfully!")
#             print("Username: admin, Password: admin123")
#         else:
#             print(" Admin user already exists")

# def initialize_database(app):
#     with app.app_context():
#         # Create all database tables
#         db.create_all()
#         print(" Database tables created successfully!")
        
#         # Create admin user
#         create_admin_user(app)

# if __name__ == '__main__':
#     # Create Flask app
#     app = create_app()
    
#     # Initialize database
#     initialize_database(app)
    
#     # Get configuration from environment
#     host = os.environ.get('FLASK_HOST', '127.0.0.1')
#     port = int(os.environ.get('FLASK_PORT', 5000))
#     debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
#     print("\n" + "="*50)
#     print("🚗 Vehicle Parking App V2 Starting...")
#     print("="*50)
#     print(f"🌐 Server running on: http://{host}:{port}")
#     print(f"🔧 Debug mode: {debug}")
#     print(f"💾 Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
#     # print(f"🔴 Redis: {app.config['REDIS_HOST']}:{app.config['REDIS_PORT']}")
#     print("="*50)
    
#     # Run the application
#     try:
#         app.run(
#             host=host,
#             port=port,
#             debug=True,
#             threaded=True
#         )
#     except KeyboardInterrupt:
#         print("\n👋 Application stopped by user")
#     except Exception as e:
#         print(f"❌ Error starting application: {e}")

# run.py
import os

from backend.app import create_app

# Create the Flask app instance using the factory function
app = create_app()

if __name__ == '__main__':
    app.run(
        host=os.environ.get('FLASK_RUN_HOST', '0.0.0.0'),
        port=int(os.environ.get('FLASK_RUN_PORT', '5000')),
        debug=os.environ.get('FLASK_DEBUG', '1').lower() in {'1', 'true', 'yes'},
    )
