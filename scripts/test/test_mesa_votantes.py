"""
Script para probar que una mesa específica tiene votantes
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
    print("MESAS DEL PUESTO 01 DE FLORENCIA:")
    print("-" * 80)
    result = session.execute(
        text("""
            SELECT 
                id,
                mesa_codigo,
                puesto_nombre,
                total_votantes_registrados,
                mujeres,
                hombres
            FROM locations
            WHERE tipo = 'mesa'
            AND departamento_codigo = '44'
            AND municipio_codigo = '01'
            AND zona_codigo = '01'
            AND puesto_codigo = '01'
            ORDER BY mesa_codigo
        """)
    ).fetchall()
    
    for row in result:
        print(f"ID: {row[0]} | Mesa: {row[1]} | Puesto: {row[2]}")
        print(f"  Votantes: {row[3]} | Mujeres: {row[4]} | Hombres: {row[5]}")
        print()
    
    session.close()
    
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
