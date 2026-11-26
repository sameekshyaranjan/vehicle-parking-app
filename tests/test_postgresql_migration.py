import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Barrier
import unittest
from unittest.mock import patch

from redis.exceptions import ConnectionError as RedisConnectionError
from sqlalchemy import create_engine, inspect, select, update
from werkzeug.security import generate_password_hash

from backend.app import create_app, db
from backend.auth.demo import DEMO_PASSWORD
from backend.models import ParkingLot, ParkingSpot, Reservation, User
from backend.models.reservation_audit import ReservationAudit
from scripts.backup_sqlite import backup_sqlite
from scripts.import_sqlite import TABLES, import_snapshot


TEST_DATABASE_URL = os.environ.get('PARKSMART_TEST_DATABASE_URL')
POSTGRESQL_TABLES = (*TABLES, ReservationAudit.__table__)


@unittest.skipUnless(TEST_DATABASE_URL, 'Set PARKSMART_TEST_DATABASE_URL to an empty migrated PostgreSQL database')
class PostgreSQLMigrationTest(unittest.TestCase):
    def setUp(self):
        settings = {
            'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URL,
            'PARKSMART_DEMO_LOGIN': '1',
            'JWT_SECRET_KEY': 'isolated-postgresql-integration-tests',
        }
        with patch.dict(os.environ, settings), patch('backend.app.redis.from_url', side_effect=RedisConnectionError()):
            self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        with self.app.app_context():
            self.addCleanup(db.engine.dispose)
            self.assertEqual(db.engine.dialect.name, 'postgresql')
            for table in POSTGRESQL_TABLES:
                self.assertIsNone(db.session.execute(select(table.c.id).limit(1)).first(), 'Use an empty test database')

    def check_schema(self):
        with self.app.app_context():
            inspector = inspect(db.engine)
            for table in POSTGRESQL_TABLES:
                columns = {column['name']: column for column in inspector.get_columns(table.name)}
                self.assertEqual(set(columns), set(table.c.keys()))
                for column in table.c:
                    actual = columns[column.name]
                    self.assertIsInstance(actual['type'], type(column.type))
                    self.assertEqual(actual['nullable'], column.nullable)
                expected_keys = {(fk.parent.name, fk.column.table.name, fk.ondelete) for fk in table.foreign_keys}
                actual_keys = {
                    (fk['constrained_columns'][0], fk['referred_table'], fk['options'].get('ondelete'))
                    for fk in inspector.get_foreign_keys(table.name)
                }
                self.assertEqual(actual_keys, expected_keys)
            indexes = {index['name']: index for index in inspector.get_indexes('reservation')}
            for index in Reservation.__table__.indexes:
                self.assertTrue(indexes[index.name]['unique'])
                self.assertIn('leaving_timestamp IS NULL', indexes[index.name]['dialect_options']['postgresql_where'])

    def test_migration_and_parking_workflow(self):
        self.check_schema()
        with TemporaryDirectory() as directory:
            source = Path(directory) / 'parking.db'
            snapshot = Path(directory) / 'backup.sqlite3'
            self.create_source(source)
            backup_sqlite(source, snapshot)
            expected = {'user': 4, 'parking_lot': 1, 'parking_spot': 2, 'reservation': 1}
            self.assertEqual(import_snapshot(snapshot, TEST_DATABASE_URL), expected)
            self.assertEqual(import_snapshot(snapshot, TEST_DATABASE_URL), expected)
            self.assertEqual(import_snapshot(snapshot, TEST_DATABASE_URL, verify_only=True), expected)
            self.exercise_app()
            with self.assertRaisesRegex(ValueError, 'destination contains different data'):
                import_snapshot(snapshot, TEST_DATABASE_URL)

    def create_source(self, path):
        engine = create_engine(f'sqlite:///{path.as_posix()}')
        try:
            with engine.begin() as connection:
                db.metadata.create_all(connection)
                for user_id, username, password, is_admin in (
                    (100, 'admin', generate_password_hash('integration-password'), True),
                    (101, 'demo_user', DEMO_PASSWORD, False),
                    (102, 'demo_admin', DEMO_PASSWORD, True),
                    (109, 'returning_user', generate_password_hash('integration-password'), False),
                ):
                    connection.execute(User.__table__.insert().values(
                        id=user_id, username=username, password=password, fullname=username,
                        email=f'{username}@demo.invalid', address='A' * 300, pin_code='000001', is_admin=is_admin,
                    ))
                connection.execute(ParkingLot.__table__.insert().values(
                    id=200, prime_location_name='Imported lot', price=17.5, address='123 Test Street',
                    pin_code='123456', number_of_spots=2,
                ))
                connection.execute(ParkingSpot.__table__.insert(), [
                    {'id': 300, 'lot_id': 200, 'spot_number': 1},
                    {'id': 301, 'lot_id': 200, 'spot_number': 2},
                ])
                connection.execute(Reservation.__table__.insert().values(
                    id=400, user_id=109, spot_id=301, vehicle_number='KA01AA0001',
                    parking_timestamp=datetime(2025, 8, 28, 12, 18, 5, 123456),
                    leaving_timestamp=datetime(2025, 8, 28, 13, 18, 5, 654321),
                    parking_cost=17.5, remarks='Historical booking',
                ))
        finally:
            engine.dispose()

    def request(self, method, path, status=200, *, body=None, token=None, origin=None):
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        if origin:
            headers['Origin'] = origin
        response = self.client.open('/api/' + path, method=method, json=body, headers=headers)
        self.assertEqual(response.status_code, status, (path, response.get_json(silent=True)))
        return response.get_json() if response.is_json else response

    def race_bookings(self, first, second):
        barrier = Barrier(2)

        def book(attempt):
            token, lot, vehicle = attempt
            barrier.wait(timeout=5)
            return self.app.test_client().post('/api/user/book-parking',
                json={'lot_id': lot, 'vehicle_number': vehicle}, headers={'Authorization': f'Bearer {token}'})

        with ThreadPoolExecutor(max_workers=2) as executor:
            responses = list(executor.map(book, (first, second)))
        self.assertEqual(sorted(response.status_code for response in responses), [201, 400])
        for attempt, response in zip((first, second), responses):
            if response.status_code == 201:
                return attempt[0], response.json['data']['reservation_id']

    def exercise_app(self):
        credentials = {'username': 'admin', 'password': 'integration-password'}
        admin = self.request('POST', 'auth/admin-login', body=credentials)['data']['tokens']['access_token']
        credentials['username'] = 'returning_user'
        returning = self.request('POST', 'auth/login', body=credentials)['data']['tokens']['access_token']
        origin = 'http://localhost:8080'
        self.assertTrue(self.request('GET', 'auth/demo', origin=origin)['enabled'])
        demo_user = self.request('POST', 'auth/demo/user', origin=origin)['data']
        demo_admin = self.request('POST', 'auth/demo/admin', origin=origin)['data']
        self.assertEqual(demo_user['user']['id'], 101)
        self.assertEqual(demo_admin['user']['id'], 102)
        demo_token = demo_user['tokens']['access_token']
        self.request('GET', 'admin/dashboard', 403, token=demo_token)
        self.request('GET', 'admin/reservation-audit', 403, token=demo_token)
        self.assertEqual(self.request('GET', 'admin/reservation-audit', token=admin)['data'], [])
        self.request('GET', 'admin/dashboard', token=demo_admin['tokens']['access_token'])
        self.request('GET', 'user/dashboard', token=demo_token)
        self.request('POST', 'auth/refresh', token=demo_user['tokens']['refresh_token'])

        regular = self.request('POST', 'auth/register', 201, body={
            'username': 'new_user', 'password': 'integration-password', 'email': 'new_user@example.test',
            'fullname': 'New User', 'address': 'A' * 300, 'pin_code': '123456',
        })['data']
        self.assertEqual(regular['user']['id'], 110)
        lot = self.request('POST', 'admin/parking-lots', 201, token=admin, body={
            'prime_location_name': 'Race lot', 'price': 25, 'address': '123 Test Street',
            'pin_code': '123456', 'number_of_spots': 1,
        })['data']['id']
        self.assertEqual(lot, 201)
        self.assertEqual(self.request('GET', f'admin/parking-spots/{lot}', token=admin)['data']['spots'][0]['id'], 302)

        token, reservation = self.race_bookings(
            (demo_token, lot, 'KA01BB0001'), (regular['tokens']['access_token'], lot, 'KA01BB0002'),
        )
        self.assertEqual(reservation, 401)
        self.request('POST', f'user/extend-booking/{reservation}', token=token, body={'additional_hours': 1})
        self.assertEqual(self.request('GET', 'admin/reservation-audit', token=admin)['data'], [])
        release = self.request('POST', f'user/release-parking/{reservation}', token=token, body={'rating': 5})['data']
        with self.app.app_context():
            db.session.execute(update(Reservation).where(Reservation.id == reservation).values(
                leaving_timestamp=Reservation.leaving_timestamp,
            ))
            db.session.commit()
        entries = self.request('GET', 'admin/reservation-audit', token=admin)['data']
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['reservation_id'], reservation)
        self.assertEqual(entries[0]['event_type'], 'RELEASED')
        self.assertEqual(entries[0]['final_cost'], release['final_cost'])
        self.assertIsNotNone(datetime.fromisoformat(entries[0]['recorded_at']).tzinfo)
        token, reservation = self.race_bookings(
            (demo_token, 200, 'KA01CC0001'), (demo_token, lot, 'KA01CC0002'),
        )
        self.request('POST', f'user/release-parking/{reservation}', token=token, body={'rating': 5})

        self.request('PUT', 'admin/parking-lots/200', token=admin, body={'number_of_spots': 1})
        history = self.request('GET', 'user/my-bookings', token=returning)['data']['bookings']
        self.assertEqual(history[0]['parking_timestamp'], '2025-08-28T12:18:05.123456')
        self.assertEqual(history[0]['remarks'], 'Historical booking')
        self.assertIsNone(history[0]['spot_number'])
        csv = self.request('POST', 'user/export-history', token=returning)
        self.assertIn(b'KA01AA0001', csv.data)
        for path in ('dashboard', 'statistics', 'statistics/detailed', 'parking-lots'):
            self.request('GET', 'user/' + path, token=returning)
        for path in ('dashboard', 'statistics', 'statistics/comprehensive', 'statistics/revenue-trends', 'statistics/performance-metrics'):
            self.request('GET', 'admin/' + path, token=admin)
        self.request('DELETE', f'admin/parking-lots/{lot}', token=admin)
