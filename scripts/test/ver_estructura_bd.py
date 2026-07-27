"""
Script para ver la estructura real de la BD
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
    # Ver todos los puestos con sus códigos
    print("PUESTOS (primeros 10):")
    result = session.execute(
        text("""
            SELECT 
                id,
                departamento_codigo,
                municipio_codigo,
                zona_codigo,
                puesto_codigo,
                puesto_nombre
            FROM locations
            WHERE tipo = 'puesto'
            ORDER BY departamento_codigo, municipio_codigo, zona_codigo, puesto_codigo
            LIMIT 10
        """)
    ).fetchall()
    
    for row in result:
        print(f"  ID: {row[0]} | Depto: {row[1]} | Muni: {row[2]} | Zona: {row[3]} | Puesto: {row[4]} | Nombre: {row[5]}")
    print()
    
    # Ver testigos con sus ubicaciones
    print("TESTIGOS CON UBICACIONES (primeros 10):")
    result = session.execute(
        text("""
            SELECT 
                u.id,
                u.nombre,
                l.departamento_codigo,
                l.municipio_codigo,
                l.zona_codigo,
                l.puesto_codigo,
                l.puesto_nombre
            FROM users u
            JOIN locations l ON u.ubicacion_id = l.id
            WHERE u.rol = 'testigo_electoral'
            ORDER BY u.nombre
            LIMIT 10
        """)
    ).fetchall()
    
    for row in result:
        print(f"  Usuario: {row[1]}")
        print(f"    Depto: {row[2]} | Muni: {row[3]} | Zona: {row[4]} | Puesto: {row[5]}")
        print(f"    Puesto nombre: {row[6]}")
        print()
    
    session.close()
    
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
