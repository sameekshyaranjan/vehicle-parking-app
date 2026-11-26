# Vehicle Parking App

A comprehensive web-based parking management system built with Flask and Vue.js for the Modern Application Development II (MAD II) project at IITM BS Degree.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Models](#database-models)
- [Celery Tasks](#celery-tasks)
- [Contributing](#contributing)
- [License](#license)

## 🚗 Overview

The Vehicle Parking App is a full-stack web application that manages parking lots, spots, and vehicle reservations. It provides separate interfaces for administrators and regular users, enabling efficient parking management with real-time updates and automated reporting.

### Key Functionalities:
- **Admin Panel**: Manage parking lots, spots, and user accounts
- **User Interface**: Reserve parking spots, view booking history, and generate reports
- **Real-time Updates**: Live parking spot availability
- **Automated Tasks**: Daily reminders and monthly reports
- **Export Features**: CSV export of parking history

## ✨ Features

### Admin Features
- Create and manage parking lots
- Monitor parking spot availability
- View user statistics and activity
- Generate comprehensive reports
- Manage user accounts

### User Features
- Browse available parking lots
- Reserve parking spots in real-time
- View booking history
- Receive automated reminders
- Export parking history to CSV
- Access monthly activity reports

### System Features
- JWT-based authentication
- Redis caching for improved performance
- Celery-based background tasks
- Email notifications
- PDF and CSV report generation

## 🛠 Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite
- **Caching**: Redis
- **Task Queue**: Celery
- **Authentication**: JWT

### Frontend
- **Framework**: Vue.js 3
- **State Management**: Vuex
- **Routing**: Vue Router
- **HTTP Client**: Axios

### Additional Tools
- **Email Service**: Flask-Mail
- **PDF Generation**: Custom PDF utilities
- **Background Processing**: Celery with Redis broker

## 📁 Project Structure

```
vehicle_parking_app/
├── frontend/                    # Vue.js frontend application
│   ├── public/                  # Static assets
│   ├── src/
│   │   ├── components/          # Reusable Vue components
│   │   ├── views/              # Page-level components
│   │   ├── router/             # Vue Router configuration
│   │   ├── store/              # Vuex store modules
│   │   └── services/           # API communication services
│   └── package.json
│
├── backend/                     # Flask backend application
│   ├── models/                  # Database models
│   ├── routes/                  # API route handlers
│   ├── services/               # Business logic services
│   ├── tasks/                  # Celery background tasks
│   ├── utils/                  # Utility functions
│   ├── templates/              # Jinja2 templates
│   └── auth/                   # Authentication module
│
├── migrations/                  # Database migrations
├── scripts/                     # Utility scripts
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── celery_worker.py            # Celery worker entry point
└── README.md                   # Project documentation
```

## Prerequisites

- Python and pip. This setup was verified with Python 3.14.
- Node.js and npm. Node.js 22 is within the engine range declared by the Vue CLI dependency tree.
- SQLite is included with Python. Redis and a Celery worker are optional for the core web app.

## Installation

From the project root in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app run init-db
.\.venv\Scripts\python.exe -m flask --app run create-admin
```

The CLI creates `backend/instance/parking.db` by default. It creates a local admin
account with username `admin` and password `admin123` if no admin exists. Use
the registration page to create a regular user.

Install the frontend dependencies from the lockfile:

```powershell
cd frontend
npm.cmd ci
```

## Configuration

The default settings are sufficient for a local run. Flask loads optional values
from a root `.env` file. It reads `SQLALCHEMY_DATABASE_URI`, `SECRET_KEY`,
`JWT_SECRET_KEY`, `REDIS_URL`, `CELERY_BROKER_URL`, and `CELERY_RESULT_BACKEND`.
The default Redis endpoint is `localhost:6379`. The Flask API uses port 5000
and the Vue development server uses port 8080.

## Usage

Start Flask from the project root:

```powershell
.\.venv\Scripts\python.exe -m flask --app run run --host 127.0.0.1 --port 5000
```

Start Vue from the project root in a second PowerShell terminal:

```powershell
cd frontend
npm.cmd run serve -- --host 127.0.0.1 --port 8080
```

Open [the web app](http://localhost:8080). Select **Admin Login** to use the
local admin account. Create a parking lot in the admin panel before testing a
reservation as a regular user.

### One-click demo login

Create the demo accounts from the project root:

```powershell
.\.venv\Scripts\python.exe -m flask --app run create-demo-accounts
```

Add `PARKSMART_DEMO_LOGIN=1` to the root `.env` file and restart Flask. Open
[the login page](http://localhost:8080/login) and select **Sign in as Demo User**
or **Sign in as Demo Admin**. Each button signs in to a dedicated account in
the local SQLite database. Demo sign-in is available on the local development
app at port 8080 when enabled.

Redis provides caching and backs the optional Celery worker. Account registration,
parking reservations, and direct CSV download work without a Redis server.
Automated email and scheduled reporting require further integration in this checkout.

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout

### Admin Endpoints
- `GET /api/admin/parking-lots` - Get all parking lots
- `POST /api/admin/parking-lots` - Create new parking lot
- `PUT /api/admin/parking-lots/{id}` - Update parking lot
- `DELETE /api/admin/parking-lots/{id}` - Delete parking lot
- `GET /api/admin/users` - Get all users
- `GET /api/admin/statistics` - Get system statistics

### User Endpoints
- `GET /api/user/parking-lots` - Get available parking lots
- `POST /api/user/reservations` - Create reservation
- `GET /api/user/reservations` - Get user reservations
- `PUT /api/user/reservations/{id}` - Update reservation
- `DELETE /api/user/reservations/{id}` - Cancel reservation
- `GET /api/user/export-history` - Export parking history

## 📊 Database Models

### User Model
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    fullname = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    address = db.Column(db.String(256))
    pin_code = db.Column(db.String(10))
    is_admin = db.Column(db.Boolean, default=False)
```

### Parking Lot Model
```python
class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(128))
    price = db.Column(db.Float)
    address = db.Column(db.String(256))
    pin_code = db.Column(db.String(10))
    number_of_spots = db.Column(db.Integer)
```

### Parking Spot Model
```python
class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'))
    status = db.Column(db.String(1), default='A')  # 'A' for available, 'O' for occupied
    spot_number = db.Column(db.Integer)
```

### Reservation Model
```python
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'))
    vehicle_number = db.Column(db.String(20))
    parking_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, nullable=True)
```

## 🔄 Celery Tasks

### Daily Reminder Task
```python
@celery.task
def send_daily_reminders():
    """Send daily reminders to users who haven't visited or booked parking recently"""
```

### Monthly Report Task
```python
@celery.task
def generate_monthly_reports():
    """Generate and send monthly activity reports to all users"""
```

### CSV Export Task
```python
@celery.task
def export_user_parking_history(user_id):
    """Export user's parking history to CSV"""
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript/Vue.js
- Write unit tests for new features
- Update documentation for API changes
- Ensure all tests pass before submitting PR

## 📝 License

This project is created for educational purposes as part of the MAD II project at IITM BS Degree program.

## 📞 Contact

- **Author**: Student ID 22f3003124
- **Institution**: Indian Institute of Technology Madras (IITM)
- **Course**: Modern Application Development II (MAD II)

## 🎓 Academic Context

This project is developed as part of the Modern Application Development II course curriculum, demonstrating:

- Full-stack web development skills
- RESTful API design
- Modern frontend frameworks
- Database design and management
- Background task processing
- Caching strategies
- Authentication and authorization
- Automated testing and deployment

---

**Note**: This application is developed for academic purposes and may require additional security enhancements for production use.
