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
- SQLite is included with Python. MySQL and PostgreSQL are supported when configured. Redis and a Celery worker are optional for the core web app.

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
from a root `.env` file. It reads `DATABASE_URL`, `SQLALCHEMY_DATABASE_URI`, `SECRET_KEY`,
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
the configured database. Demo sign-in is available on the local development
app at port 8080 when enabled.

Redis provides caching and backs the optional Celery worker. Account registration,
parking reservations, and direct CSV download work without a Redis server.
Automated email and scheduled reporting require further integration in this checkout.

## MySQL migration on Windows

Install MySQL Community Server 8.4 LTS with the [official Windows MSI](https://dev.mysql.com/downloads/mysql/8.4.html?os=3). Configure a local-only Windows service on `127.0.0.1:3306`, with UTF-8 data using `utf8mb4` and `utf8mb4_0900_bin`. The local rehearsal service provisioned for this workspace is named `ParkSmartMySQL`. Check it with `Get-Service ParkSmartMySQL`; an administrator can run `Start-Service ParkSmartMySQL` if it is stopped.

Use a dedicated MySQL database. Use a migration account with schema and trigger permissions and a separate application account with data access. On the local rehearsal service, binary logging is disabled so the migration account can install the trigger. The runtime account uses the trigger through the definer that installed it.

From the project root in PowerShell, install dependencies and load the rehearsal credentials into **this terminal only**. The workspace setup saved them encrypted for your Windows user. On another computer, set `DATABASE_URL` to the migration account's `mysql://` URL instead. URL-encode passwords that contain special characters.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
npm.cmd ci
$vault = Join-Path $env:LOCALAPPDATA 'ParkSmartMySQL\connections.dpapi'
$secureConnections = (Get-Content -LiteralPath $vault -Raw).Trim() | ConvertTo-SecureString
$connections = [System.Net.NetworkCredential]::new('', $secureConnections).Password | ConvertFrom-Json
$env:DATABASE_URL = $connections.rehearsalMigration
npm.cmd run db:mysql:validate
npm.cmd run db:mysql:deploy
npm.cmd run db:mysql:status
```

The MySQL schema and migrations live in `prisma/mysql`. PostgreSQL has a separate schema and migration history. The MySQL release trigger and the two functional unique indexes are part of the versioned SQL migration. These indexes enforce one active reservation per user and per spot. An active reservation has no leaving timestamp.

### Import and rehearse

Use the source path configured by the running SQLite app. The default is shown below. Keep the target app disconnected while importing. The importer verifies every original row, including timestamps and hashes, and checks that MySQL's auto-increment counters are past the imported IDs. It protects the import from concurrent import commands and refuses to overwrite different data.

```powershell
$snapshot = 'backend/instance/backups/parksmart-mysql-rehearsal.sqlite3'
.\.venv\Scripts\python.exe -m scripts.backup_sqlite backend/instance/parking.db $snapshot
.\.venv\Scripts\python.exe -m scripts.import_sqlite --source $snapshot
.\.venv\Scripts\python.exe -m scripts.import_sqlite --source $snapshot --verify-only
```

For the integration suite, migrate a **separate empty database** and pass the migration and runtime credentials separately. The test writes its own fixture data and exercises both the database guards and the application's workflows.

```powershell
$env:DATABASE_URL = $connections.integrationMigration
npm.cmd run db:mysql:deploy
$env:PARKSMART_TEST_DATABASE_URL = $env:DATABASE_URL
$env:PARKSMART_TEST_APP_DATABASE_URL = $connections.integrationApp
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### Cut over or roll back

After approval, stop Flask and its workers, take a fresh SQLite backup, apply the MySQL migrations to the designated database, and import and verify the backup. Configure Flask and the worker with the **runtime** URL in `SQLALCHEMY_DATABASE_URI`. Keep JWT and Flask secrets. Clear or isolate cached parking data before restarting. To demo the trigger, sign in as a user, book and release a spot, then open **Reservation Activity** on the admin dashboard.

To roll back before MySQL receives writes, stop Flask and its workers, restore the previous SQLite connection settings, clear the parking cache, and restart. If MySQL has accepted writes, stop writes and dump the database with `mysqldump --single-transaction --triggers` before reconciling those records with SQLite. Keep the original SQLite database and its backups.

## PostgreSQL migration on Windows

Use a PostgreSQL server and a dedicated database for ParkSmart. The role applying
migrations and running the import needs to own the target tables and sequences.
Use Node.js 22.12+ on the 22 line or Node.js 24 for the root Prisma tools. The Vue
dependencies still install separately in `frontend`.

Prisma reads `DATABASE_URL` from the shell or the root `.env`. Flask and its
Celery worker use `SQLALCHEMY_DATABASE_URI` first, then `DATABASE_URL`, and
default to `backend/instance/parking.db` if both are unset. Use a plain
`postgresql://` URL targeting the `public` schema. URL-encode any special
characters in the password. Flask uses Psycopg for that URL. Keep credentials
in the environment or the ignored `.env` file. Prisma owns PostgreSQL schema
changes. Flask's `init-db` command is for SQLite.

### Rehearse the migration

From the project root, create a PostgreSQL rehearsal database and use its URL in
a separate PowerShell terminal. Here `parking.db` is the default SQLite file.
If the running app points elsewhere, use that SQLite path for the backup.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
npm.cmd ci
$env:DATABASE_URL = 'postgresql://USER:URL_ENCODED_PASSWORD@localhost:5432/parksmart_rehearsal'
$snapshot = 'backend/instance/backups/parksmart-rehearsal.sqlite3'
.\.venv\Scripts\python.exe -m scripts.backup_sqlite backend/instance/parking.db $snapshot
npm.cmd run db:validate
npm.cmd run db:deploy
npm.cmd run db:status
.\.venv\Scripts\python.exe -m scripts.import_sqlite --source $snapshot
.\.venv\Scripts\python.exe -m scripts.import_sqlite --source $snapshot --verify-only
```

The import copies the four SQLite application tables by ID in one transaction, checks every field
against the snapshot, and advances the PostgreSQL sequences. It can be rerun on
an identical destination and refuses to overwrite different data. Foreign-key
violations and duplicate active reservations must be resolved before import.
Existing timestamps remain local wall-clock values with microsecond precision.
If an admin later removes a spot while resizing a lot, PostgreSQL retains its
completed reservations and clears their reference to that spot.

To run the integration test suite, apply the Prisma migration to a **separate
empty database** and pass its URL with `PARKSMART_TEST_DATABASE_URL`. The test
creates and exercises its own data, including concurrent booking requests.

```powershell
$env:DATABASE_URL = 'postgresql://USER:URL_ENCODED_PASSWORD@localhost:5432/parksmart_integration'
npm.cmd run db:deploy
$env:PARKSMART_TEST_DATABASE_URL = $env:DATABASE_URL
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### Cutover and rollback

After approving the cutover, stop Flask and any workers so the old database
stops receiving writes. Take a fresh SQLite backup under a new filename. Apply
the migrations to an empty PostgreSQL target, import the fresh backup, and run
`--verify-only`. Set the approved `DATABASE_URL` for Flask and the worker,
remove any SQLite `SQLALCHEMY_DATABASE_URI` override, and keep the existing JWT
and secret keys. Restart the services and smoke-test both login modes, demo
accounts, and bookings. Clear or isolate any shared Redis parking data cache at
cutover so it reflects the new database.

To roll back before PostgreSQL has accepted new app writes, stop the services,
restore the previous SQLite connection settings, clear the parking cache, and
restart. If PostgreSQL has accepted writes, stop writes and export that database
first. Reconcile those changes before returning traffic to SQLite. The original
SQLite database and its backup should be retained until cutover is accepted.

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

On MySQL and PostgreSQL the app has five tables. In addition to users, parking lots,
parking spots, and reservations, `reservation_audit` stores release events.
Its reservation ID is a snapshot that is retained if an admin later deletes
the original reservation. The `reservation_release_audit` database trigger
records a `RELEASED` event when a reservation's leaving timestamp first changes
from empty to set. Imported completed reservations do not create events.

### Demonstrate the PostgreSQL trigger

1. Apply the Prisma migrations with `npm.cmd run db:deploy` on the demo database.
2. As admin, create a parking lot with an available spot.
3. As a regular user, book a spot and release it.
4. Sign in as admin and open **Reservation Activity** on the dashboard. The
   new `RELEASED` row shows the reservation ID, recorded time, and final cost.

### User Model
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    fullname = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)
    address = db.Column(db.Text)
    pin_code = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
```

### Parking Lot Model
```python
class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.Text)
    price = db.Column(db.Float)
    address = db.Column(db.Text)
    pin_code = db.Column(db.Text)
    number_of_spots = db.Column(db.Integer)
```

### Parking Spot Model
```python
class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'))
    status = db.Column(db.Text, default='A')  # 'A' for available, 'O' for occupied
    spot_number = db.Column(db.Integer)
```

### Reservation Model
```python
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id', ondelete='SET NULL'))
    vehicle_number = db.Column(db.Text)
    parking_timestamp = db.Column(db.DateTime, default=get_ist_time)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, nullable=True)
    remarks = db.Column(db.Text, nullable=True)
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
