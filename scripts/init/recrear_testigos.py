"""
Script para recrear todos los usuarios testigos
- Elimina todos los testigos existentes
- Crea un testigo por cada mesa en cada puesto
- Nombre: DEPTO_MUNI_ZONA_PUESTO_MESA
- Contraseña: test123
"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

def get_database_url():
    return 'sqlite:///C:/Users/Ivan/OneDrive - Fundación ProMITIERRA/Documentos/MVP/mvp/instance/electoral.db'

print("=" * 80)
print("RECREAR USUARIOS TESTIGOS")
print("=" * 80)
print()

database_url = get_database_url()
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()

try:
    # 1. ELIMINAR TODOS LOS TESTIGOS EXISTENTES
    print("🗑️  Eliminando testigos existentes...")
    result = session.execute(
        text("DELETE FROM users WHERE rol = 'testigo_electoral'")
    )
    eliminados = result.rowcount
    session.commit()
    print(f"✅ {eliminados} testigo(s) eliminado(s)")
    print()
    
    # 2. OBTENER TODOS LOS PUESTOS CON SUS MESAS
    print("📋 Obteniendo puestos y mesas...")
    puestos = session.execute(
        text("""
            SELECT 
                p.id as puesto_id,
                p.departamento_codigo,
                p.municipio_codigo, 
                p.zona_codigo,
                p.puesto_codigo,
                p.puesto_nombre,
                COUNT(m.id) as num_mesas
            FROM locations p
            LEFT JOIN locations m ON m.puesto_codigo = p.puesto_codigo AND m.tipo = 'mesa'
            WHERE p.tipo = 'puesto'
            GROUP BY p.id
            HAVING num_mesas > 0
            ORDER BY p.departamento_codigo, p.municipio_codigo, p.zona_codigo, p.puesto_codigo
        """)
    ).fetchall()
    
    print(f"✅ {len(puestos)} puesto(s) encontrado(s)")
    print()
    
    # 3. CREAR TESTIGOS
    print("👥 Creando testigos...")
    password_hash = generate_password_hash('test123')
    testigos_creados = 0
    
    for puesto in puestos:
        puesto_id, dd, mm, zz, pp, puesto_nombre, num_mesas = puesto
        
        # Obtener mesas del puesto
        mesas = session.execute(
            text("""
                SELECT id, mesa_codigo
                FROM locations
                WHERE puesto_codigo = :puesto_codigo AND tipo = 'mesa'
                ORDER BY mesa_codigo
            """),
            {"puesto_codigo": pp}
        ).fetchall()
        
        # Obtener nombre del municipio (normalizado para nombre de usuario)
        municipio_nombre = session.execute(
            text("""
                SELECT municipio_nombre
                FROM locations
                WHERE tipo = 'municipio' AND municipio_codigo = :municipio_codigo
                LIMIT 1
            """),
            {"municipio_codigo": mm}
        ).fetchone()
        
        if not municipio_nombre:
            print(f"  ⚠️ Municipio no encontrado para código {mm}, saltando puesto {pp}")
            continue
        
        # Normalizar nombre del municipio para nombre de usuario
        # Remover espacios, acentos, caracteres especiales
        muni_nombre = municipio_nombre[0].upper()
        muni_nombre = muni_nombre.replace(' ', '_')
        muni_nombre = muni_nombre.replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U')
        muni_nombre = muni_nombre.replace('Ñ', 'N')
        
        # Crear un testigo por cada mesa
        for mesa_id, mesa_codigo in mesas:
            # Extraer solo el número de mesa del código completo
            # Formato: DDMMZZPPMM -> extraer últimos 2 dígitos
            mesa_num = mesa_codigo[-2:]
            
            # Nombre del testigo: MUNICIPIO_PXX_MXX
            # Ejemplo: FLORENCIA_P01_M01
            nombre_testigo = f"{muni_nombre}_P{pp}_M{mesa_num}"
            
            # Crear testigo asignado al PUESTO (no a la mesa)
            now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            session.execute(
                text("""
                    INSERT INTO users (nombre, password_hash, rol, ubicacion_id, activo, intentos_fallidos, presencia_verificada, es_usuario_basico, created_at, updated_at)
                    VALUES (:nombre, :password, 'testigo_electoral', :ubicacion_id, 1, 0, 0, 0, :created_at, :updated_at)
                """),
                {
                    "nombre": nombre_testigo,
                    "password": password_hash,
                    "ubicacion_id": puesto_id,  # Asignado al puesto, no a la mesa
                    "created_at": now,
                    "updated_at": now
                }
            )
            testigos_creados += 1
        
        if testigos_creados % 50 == 0:
            print(f"  ✅ {testigos_creados} testigos creados...")
            session.commit()
    
    session.commit()
    
    print()
    print("=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print(f"✅ Testigos eliminados: {eliminados}")
    print(f"✅ Testigos creados: {testigos_creados}")
    print(f"✅ Puestos procesados: {len(puestos)}")
    print()
    print("CREDENCIALES:")
    print("  Formato: [MUNICIPIO]_P[PUESTO]_M[MESA]")
    print("  Ejemplo: FLORENCIA_P01_M01")
    print("  Contraseña: test123")
    print()
    print("COMO HACER LOGIN:")
    print("  1. Seleccionar rol: Testigo Electoral")
    print("  2. Seleccionar ubicación: Departamento > Municipio > Zona > Puesto")
    print("  3. Ingresar contraseña: test123")
    print("  4. El sistema encontrará automáticamente al testigo del puesto")
    print()
    print("NOTA: Los testigos están asignados al PUESTO, pero pueden")
    print("      seleccionar y verificar cualquier mesa del puesto en su dashboard")
    print("=" * 80)
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    session.rollback()
finally:
    session.close()
