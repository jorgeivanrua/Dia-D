"""
Script para verificar códigos de ubicaciones
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
    # Verificar departamento Caquetá
    print("DEPARTAMENTOS:")
    result = session.execute(
        text("""
            SELECT departamento_codigo, departamento_nombre
            FROM locations
            WHERE tipo = 'departamento'
            LIMIT 5
        """)
    ).fetchall()
    
    for row in result:
        print(f"  {row[0]} - {row[1]}")
    print()
    
    # Verificar municipio Florencia
    print("MUNICIPIOS DE CAQUETA:")
    result = session.execute(
        text("""
            SELECT municipio_codigo, municipio_nombre, departamento_codigo
            FROM locations
            WHERE tipo = 'municipio' AND departamento_codigo = '44'
            LIMIT 5
        """)
    ).fetchall()
    
    for row in result:
        print(f"  {row[0]} - {row[1]} (Depto: {row[2]})")
    print()
    
    # Verificar zonas de Florencia
    print("ZONAS DE FLORENCIA:")
    result = session.execute(
        text("""
            SELECT zona_codigo, municipio_codigo
            FROM locations
            WHERE tipo = 'zona' AND municipio_codigo = '001' AND departamento_codigo = '44'
            LIMIT 5
        """)
    ).fetchall()
    
    for row in result:
        print(f"  Zona: {row[0]} (Municipio: {row[1]})")
    print()
    
    # Verificar puestos de Florencia
    print("PUESTOS DE FLORENCIA (primeros 5):")
    result = session.execute(
        text("""
            SELECT puesto_codigo, puesto_nombre, zona_codigo, municipio_codigo
            FROM locations
            WHERE tipo = 'puesto' AND municipio_codigo = '001' AND departamento_codigo = '44'
            LIMIT 5
        """)
    ).fetchall()
    
    for row in result:
        print(f"  {row[0]} - {row[1]} (Zona: {row[2]}, Municipio: {row[3]})")
    print()
    
    # Verificar un testigo específico
    print("TESTIGOS DE FLORENCIA (primeros 5):")
    result = session.execute(
        text("""
            SELECT u.id, u.nombre, l.puesto_codigo, l.zona_codigo, l.municipio_codigo, l.departamento_codigo
            FROM users u
            JOIN locations l ON u.ubicacion_id = l.id
            WHERE u.rol = 'testigo_electoral' AND l.municipio_codigo = '001' AND l.departamento_codigo = '44'
            LIMIT 5
        """)
    ).fetchall()
    
    for row in result:
        print(f"  ID: {row[0]} | Usuario: {row[1]} | Puesto: {row[2]} | Zona: {row[3]} | Municipio: {row[4]} | Depto: {row[5]}")
    
    session.close()
    
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
