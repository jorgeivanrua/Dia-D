"""
Script para ver qué tablas existen en la base de datos
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker

def get_database_url():
    database_url = os.getenv('DATABASE_URL', 'sqlite:///instance/electoral.db')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    return database_url

database_url = get_database_url()
print(f"Base de datos: {database_url}")
print()

engine = create_engine(database_url)
inspector = inspect(engine)

print("Tablas en la base de datos:")
for table_name in inspector.get_table_names():
    print(f"  - {table_name}")
