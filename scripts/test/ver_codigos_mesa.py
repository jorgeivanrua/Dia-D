"""
Script para ver códigos de mesa en la BD
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def get_database_url():
    return 'sqlite:///C:/Users/Ivan/OneDrive - Fundación ProMITIERRA/Documentos/MVP/mvp/instance/electoral.db'

database_url = get_database_url()
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()

try:
    print("CÓDIGOS DE MESA EN LA BD (primeros 10):")
    result = session.execute(
        text("""
            SELECT mesa_codigo, puesto_nombre
            FROM locations
            WHERE tipo = 'mesa'
            ORDER BY mesa_codigo
            LIMIT 10
        """)
    ).fetchall()
    
    for row in result:
        print(f"  {row[0]} - {row[1]}")
    
    session.close()
    
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
