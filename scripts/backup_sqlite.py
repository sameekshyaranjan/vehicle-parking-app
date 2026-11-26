"""Create an integrity-checked backup of a ParkSmart SQLite database."""

import argparse
from contextlib import closing
from pathlib import Path
import sqlite3


def backup_sqlite(source, destination):
    source_uri = Path(source).resolve(strict=True).as_uri() + '?mode=ro'
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.touch(exist_ok=False)
    try:
        with closing(sqlite3.connect(source_uri, uri=True)) as original:
            with closing(sqlite3.connect(destination)) as backup:
                original.backup(backup)
                if backup.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                    raise ValueError('The SQLite backup failed its integrity check.')
    except Exception:
        destination.unlink(missing_ok=True)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    try:
        backup_sqlite(args.source, args.destination)
    except (OSError, sqlite3.Error, ValueError) as error:
        parser.exit(1, f'Backup failed: {error}\n')
    print(f'Verified SQLite backup: {args.destination}')


if __name__ == '__main__':
    main()
