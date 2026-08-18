"""
Migrate the full SQLite database (instance/electoral.db) into PostgreSQL.

Creates the destination schema using the application models (db.create_all()),
then copies every table's data via SQLAlchemy reflection from SQLite.
Finally resets all user passwords to the default `test123`.

Usage (from repo root, DATABASE_URL points to the target PostgreSQL):
  $env:DATABASE_URL='postgresql://postgres:postgres@localhost:5432/electoral_db'
  py -3.14 scripts/migrate_sqlite_to_postgres.py
"""
import os
import sys
from datetime import datetime
from sqlalchemy import create_engine, MetaData, text, select, Table
from sqlalchemy.dialects import postgresql

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

SQLITE_URL = 'sqlite:///instance/electoral.db'
POSTGRES_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/electoral_db')


def _normalize(value, coltype):
    """Convert a SQLite value to something psycopg2 accepts for the column type."""
    if value is None:
        return None
    ct = str(coltype).upper()
    if 'BOOL' in ct:
        return bool(value)
    if 'TIMESTAMP' in ct or 'DATETIME' in ct:
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return None
    return value


def main():
    src = create_engine(SQLITE_URL)
    dst = create_engine(POSTGRES_URL)

    # 1) Create the destination schema from the app models (Postgres-compatible types)
    os.environ['DATABASE_URL'] = POSTGRES_URL
    from backend.app import create_app
    app = create_app('production')
    app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URL
    from backend.database import db
    with app.app_context():
        db.drop_all()
        db.create_all()
    print('Destination schema created from app models (30 tables).\n')

    # 2) Reflect source tables for data copy
    meta = MetaData()
    meta.reflect(bind=src)
    src_tables = [t for t in sorted(meta.tables) if not t.startswith('alembic_')]

    with dst.connect() as conn:
        try:
            conn.execute(text('SET session_replication_role = replica'))
            conn.commit()
        except Exception as exc:
            print(f'[warn] could not set replica role: {exc}')

    try:
        for name in src_tables:
            src_table = meta.tables[name]
            try:
                dst_table = Table(name, MetaData(), autoload_with=dst)
            except Exception:
                print(f'  - {name:40} SKIPPED (not in app schema)')
                continue

            with src.connect() as sconn:
                rows = list(sconn.execute(select(src_table)))
            if not rows:
                print(f'  - {name:40} (empty)')
                continue

            src_cols = {c.name for c in src_table.columns}
            dst_cols = {c.name for c in dst_table.columns}
            common = src_cols & dst_cols
            insert_cols = [c for c in dst_table.columns if c.name in common]

            with dst.begin() as conn:
                for row in rows:
                    values = {
                        c.name: _normalize(row._mapping.get(c.name), c.type)
                        for c in insert_cols
                    }
                    conn.execute(dst_table.insert().values(**values))
            print(f'  - {name:40} {len(rows)} rows')
    finally:
        with dst.connect() as conn:
            try:
                conn.execute(text('SET session_replication_role = DEFAULT'))
                conn.commit()
            except Exception:
                pass

    # 3) Reset all user passwords to test123 (migration convention)
    print('\nResetting all user passwords to test123...')
    with app.app_context():
        from werkzeug.security import generate_password_hash
        from backend.models.user import User
        hashed = generate_password_hash('test123')
        count = 0
        for user in User.query.all():
            user.password_hash = hashed
            count += 1
        db.session.commit()
        print(f'  - {count} users updated (all roles -> test123)')
    print('\nMigration complete.')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'\nERROR: {exc}')
        sys.exit(1)