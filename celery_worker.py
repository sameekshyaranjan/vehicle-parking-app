# ~/parking/celery_worker.py

import os
from backend.app import create_app

# Create the Flask app instance to load the configuration
flask_app = create_app(os.getenv('FLASK_CONFIG') or 'development')

# Get the configured Celery app instance from the Flask app
celery_app = flask_app.extensions['celery']