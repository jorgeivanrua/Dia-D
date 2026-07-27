"""
Script para verificar votantes registrados en mesas
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
    print("VOTANTES REGISTRADOS EN MESAS (primeros 10):")
    print("-" * 80)
    result = session.execute(
        text("""
            SELECT 
                mesa_codigo,
                puesto_nombre,
                total_votantes_registrados,
                mujeres,
                hombres
            FROM locations
            WHERE tipo = 'mesa' AND total_votantes_registrados IS NOT NULL
            ORDER BY puesto_nombre, mesa_codigo
            LIMIT 10
        """)
    ).fetchall()
    
    for row in result:
        print(f"Mesa: {row[0]} | Puesto: {row[1]}")
        print(f"  Total: {row[2]} | Mujeres: {row[3]} | Hombres: {row[4]}")
        print()
    
    # Contar mesas con y sin votantes
    result = session.execute(
        text("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN total_votantes_registrados IS NOT NULL THEN 1 ELSE 0 END) as con_votantes,
                SUM(CASE WHEN total_votantes_registrados IS NULL THEN 1 ELSE 0 END) as sin_votantes
            FROM locations
            WHERE tipo = 'mesa'
        """)
    ).fetchone()
    
    print("-" * 80)
    print(f"Total mesas: {result[0]}")
    print(f"Con votantes registrados: {result[1]}")
    print(f"Sin votantes registrados: {result[2]}")
    
    session.close()
    
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
