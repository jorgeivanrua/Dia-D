"""
Script para crear un usuario testigo de prueba
Ejecutar: python scripts/crear_testigo_prueba.py
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

def get_database_url():
    database_url = os.getenv('DATABASE_URL', 'sqlite:///instance/electoral.db')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    return database_url

print("=" * 80)
print("CREAR USUARIO TESTIGO DE PRUEBA")
print("=" * 80)
print()

database_url = get_database_url()
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Buscar un puesto para asignar
    puesto = session.execute(
        text("SELECT id, puesto_nombre, puesto_codigo FROM locations WHERE tipo = 'puesto' LIMIT 1")
    ).fetchone()
    
    if not puesto:
        print("❌ No hay puestos en la base de datos")
        print("   Ejecuta primero: python scripts/cargar_divipola_v2.py")
        sys.exit(1)
    
    puesto_id, puesto_nombre, puesto_codigo = puesto
    print(f"✅ Puesto encontrado: {puesto_nombre} (ID: {puesto_id})")
    print()
    
    # Crear nombre de usuario basado en el puesto
    nombre_usuario = f"TESTIGO_{puesto_codigo}"
    
    # Verificar si ya existe
    existe = session.execute(
        text("SELECT id FROM users WHERE nombre = :nombre"),
        {"nombre": nombre_usuario}
    ).fetchone()
    
    if existe:
        print(f"⚠️ El usuario {nombre_usuario} ya existe")
        print()
        print("Credenciales:")
        print(f"  Usuario: {nombre_usuario}")
        print(f"  Contraseña: test123")
        sys.exit(0)
    
    # Crear usuario
    password_hash = generate_password_hash('test123')
    
    session.execute(
        text("""
            INSERT INTO users (nombre, password_hash, rol, ubicacion_id, activo)
            VALUES (:nombre, :password, 'testigo_electoral', :ubicacion_id, 1)
        """),
        {
            "nombre": nombre_usuario,
            "password": password_hash,
            "ubicacion_id": puesto_id
        }
    )
    
    session.commit()
    
    print("✅ Usuario testigo creado exitosamente")
    print()
    print("=" * 80)
    print("CREDENCIALES DE ACCESO")
    print("=" * 80)
    print(f"Usuario: {nombre_usuario}")
    print(f"Contraseña: test123")
    print(f"Puesto: {puesto_nombre}")
    print("=" * 80)
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    session.close()
