"""
Script simple para verificar testigos creados
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
    # Contar testigos
    result = session.execute(
        text("SELECT COUNT(*) as total FROM users WHERE rol = 'testigo_electoral'")
    ).fetchone()
    
    print(f"Total testigos: {result[0]}")
    print()
    
    # Mostrar primeros 10
    result = session.execute(
        text("""
            SELECT 
                u.id,
                u.nombre,
                l.puesto_nombre,
                l.municipio_nombre
            FROM users u
            LEFT JOIN locations l ON u.ubicacion_id = l.id
            WHERE u.rol = 'testigo_electoral'
            ORDER BY u.nombre
            LIMIT 10
        """)
    ).fetchall()
    
    print("Primeros 10 testigos:")
    print("-" * 80)
    for row in result:
        user_id, nombre, puesto, municipio = row
        print(f"ID: {user_id} | Usuario: {nombre} | Puesto: {puesto} | Municipio: {municipio}")
    
    print("-" * 80)
    print()
    
    # Verificar formato de nombres
    result = session.execute(
        text("""
            SELECT DISTINCT nombre
            FROM users
            WHERE rol = 'testigo_electoral'
            ORDER BY nombre
            LIMIT 20
        """)
    ).fetchall()
    
    print("Ejemplos de nombres de usuario:")
    for row in result:
        print(f"  - {row[0]}")
    
    session.close()
    
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
