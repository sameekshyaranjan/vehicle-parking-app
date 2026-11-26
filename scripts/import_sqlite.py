"""Import a ParkSmart SQLite snapshot into a migrated PostgreSQL database."""

import argparse
from contextlib import closing
from datetime import datetime
import os
from pathlib import Path
import sqlite3

from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import DBAPIError

from backend.database import sqlalchemy_database_url
from backend.models import ParkingLot, ParkingSpot, Reservation, User


TABLES = tuple(model.__table__ for model in (User, ParkingLot, ParkingSpot, Reservation))


def load_snapshot(path):
    uri = Path(path).resolve(strict=True).as_uri() + '?mode=ro'
    with closing(sqlite3.connect(uri, uri=True)) as source:
        source.row_factory = sqlite3.Row
        source.execute('BEGIN')
        if source.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
            raise ValueError('The SQLite snapshot failed its integrity check.')
        violation = source.execute('PRAGMA foreign_key_check').fetchone()
        if violation:
            raise ValueError(f'SQLite table {violation[0]} has an invalid foreign key at row {violation[1]}.')
        snapshot = {}
        for table in TABLES:
            columns = ', '.join(f'"{column.name}"' for column in table.columns)
            rows = [dict(row) for row in source.execute(f'SELECT {columns} FROM "{table.name}" ORDER BY id')]
            snapshot[table] = rows

    for row in snapshot[User.__table__]:
        if row['is_admin'] not in (None, 0, 1):
            raise ValueError(f'Invalid is_admin value on SQLite user ID {row["id"]}.')
        if row['is_admin'] is not None:
            row['is_admin'] = bool(row['is_admin'])

    for row in snapshot[Reservation.__table__]:
        for field in ('parking_timestamp', 'leaving_timestamp'):
            if row[field] is None:
                continue
            try:
                timestamp = datetime.fromisoformat(row[field])
                if timestamp.tzinfo is not None:
                    raise ValueError('Unexpected timezone offset')
            except (TypeError, ValueError) as error:
                raise ValueError(f'Invalid {field} on SQLite reservation ID {row["id"]}.') from error
            row[field] = timestamp
    return snapshot


def read_target(connection):
    return {
        table: [dict(row) for row in connection.execute(select(table).order_by(table.c.id)).mappings()]
        for table in TABLES
    }


def import_snapshot(path, target_url, verify_only=False):
    url = sqlalchemy_database_url(target_url)
    if url.drivername != 'postgresql+psycopg':
        raise ValueError('DATABASE_URL must be a PostgreSQL connection URL.')
    snapshot = load_snapshot(path)
    engine = create_engine(url)
    try:
        with engine.begin() as connection:
            quote_table = connection.dialect.identifier_preparer.format_table
            names = ', '.join(quote_table(table) for table in TABLES)
            lock = 'SHARE' if verify_only else 'SHARE ROW EXCLUSIVE'
            connection.exec_driver_sql(f'LOCK TABLE {names} IN {lock} MODE')
            current = read_target(connection)
            if current != snapshot and not verify_only:
                if any(current.values()):
                    raise ValueError('The destination contains different data. Use an empty migrated database.')
                for table, rows in snapshot.items():
                    if rows:
                        connection.execute(table.insert(), rows)
                current = read_target(connection)
                for table, rows in snapshot.items():
                    sequence = connection.scalar(
                        text("SELECT pg_get_serial_sequence(:table_name, 'id')"),
                        {'table_name': quote_table(table)},
                    )
                    if not sequence:
                        raise ValueError(f'Missing ID sequence for PostgreSQL table {table.name}.')
                    next_id = max(1, max((row['id'] for row in rows), default=0) + 1)
                    # The catalog supplies a quoted, schema-qualified name for the owned sequence.
                    connection.exec_driver_sql(f'ALTER SEQUENCE {sequence} RESTART WITH {next_id}')
            mismatches = [table.name for table in TABLES if current[table] != snapshot[table]]
            if mismatches:
                raise ValueError(f'SQLite and PostgreSQL differ in: {", ".join(mismatches)}.')
    finally:
        engine.dispose()
    return {table.name: len(snapshot[table]) for table in TABLES}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path, help='Path to the SQLite snapshot')
    parser.add_argument('--verify-only', action='store_true', help='Compare records without writing to PostgreSQL')
    args = parser.parse_args()
    target_url = os.environ.get('DATABASE_URL')
    if not target_url:
        parser.exit(1, 'Set DATABASE_URL to the migrated PostgreSQL destination.\n')
    try:
        counts = import_snapshot(args.source, target_url, args.verify_only)
    except (OSError, sqlite3.Error, ValueError) as error:
        parser.exit(1, f'Import failed: {error}\n')
    except DBAPIError as error:
        state = getattr(error.orig, 'sqlstate', None) or 'connection error'
        constraint = getattr(getattr(error.orig, 'diag', None), 'constraint_name', None)
        detail = f', constraint {constraint}' if constraint else ''
        parser.exit(1, f'PostgreSQL import failed ({state}{detail}). Check the connection, schema, and source data.\n')
    print('Verified matching rows: ' + ', '.join(f'{table}={count}' for table, count in counts.items()))


if __name__ == '__main__':
    main()
