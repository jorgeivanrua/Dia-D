"""
Script para crear usuarios de prueba
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location


def create_test_users():
    """Crear usuarios de prueba para el sistema"""
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("\n>> Creando usuarios de prueba...")
        
        # Obtener ubicaciones necesarias
        caqueta = Location.query.filter_by(
            tipo='departamento',
            departamento_codigo='44'
        ).first()
        
        florencia = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo='44',
            municipio_codigo='01'
        ).first()
        
        zona_01 = Location.query.filter_by(
            tipo='zona',
            departamento_codigo='44',
            municipio_codigo='01',
            zona_codigo='01'
        ).first()
        
        puesto_01 = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo='44',
            municipio_codigo='01',
            zona_codigo='01',
            puesto_codigo='01'
        ).first()
        
        if not caqueta or not florencia:
            print("❌ Error: No se encontraron las ubicaciones necesarias")
            print("   Ejecuta primero: python scripts/load_divipola.py")
            return
        
        # Limpiar usuarios existentes
        print(">> Limpiando usuarios existentes...")
        User.query.delete()
        db.session.commit()
        
        # Lista de usuarios a crear
        users_to_create = [
            {
                'nombre': 'Super Admin',
                'rol': 'super_admin',
                'ubicacion_id': None,
                'password': 'SuperAdmin123!'
            },
            {
                'nombre': 'Admin Departamental Caquetá',
                'rol': 'admin_departamental',
                'ubicacion_id': caqueta.id if caqueta else None,
                'password': 'AdminDept123!'
            },
            {
                'nombre': 'Admin Municipal Florencia',
                'rol': 'admin_municipal',
                'ubicacion_id': florencia.id if florencia else None,
                'password': 'AdminMuni123!'
            },
            {
                'nombre': 'Coordinador Departamental Caquetá',
                'rol': 'coordinador_departamental',
                'ubicacion_id': caqueta.id if caqueta else None,
                'password': 'CoordDept123!'
            },
            {
                'nombre': 'Coordinador Municipal Florencia',
                'rol': 'coordinador_municipal',
                'ubicacion_id': florencia.id if florencia else None,
                'password': 'CoordMuni123!'
            },
            {
                'nombre': 'Auditor Electoral Caquetá',
                'rol': 'auditor_electoral',
                'ubicacion_id': caqueta.id if caqueta else None,
                'password': 'Auditor123!'
            }
        ]
        
        # Agregar coordinadores de puesto y testigos si hay puestos disponibles
        if puesto_01:
            users_to_create.extend([
                {
                    'nombre': 'Coordinador Puesto 01',
                    'rol': 'coordinador_puesto',
                    'ubicacion_id': puesto_01.id,
                    'password': 'CoordPuesto123!'
                },
                {
                    'nombre': 'Testigo Electoral Puesto 01',
                    'rol': 'testigo_electoral',
                    'ubicacion_id': puesto_01.id,
                    'password': 'Testigo123!'
                }
            ])
        
        # Crear usuarios
        created_count = 0
        for user_data in users_to_create:
            if user_data['ubicacion_id'] is None and user_data['rol'] != 'super_admin':
                print(f"⚠️  Saltando {user_data['nombre']} - ubicación no encontrada")
                continue
            
            try:
                user = User(
                    nombre=user_data['nombre'],
                    rol=user_data['rol'],
                    ubicacion_id=user_data['ubicacion_id']
                )
                user.set_password(user_data['password'])
                
                db.session.add(user)
                db.session.commit()
                
                ubicacion_info = "Sin ubicación" if user_data['ubicacion_id'] is None else f"Ubicación ID: {user_data['ubicacion_id']}"
                print(f"✅ Creado: {user_data['nombre']} ({user_data['rol']}) - {ubicacion_info}")
                print(f"   Password: {user_data['password']}")
                created_count += 1
                
            except Exception as e:
                print(f"❌ Error creando {user_data['nombre']}: {e}")
                db.session.rollback()
        
        print(f"\n>> Total de usuarios creados: {created_count}")
        
        # Mostrar resumen de ubicaciones
        print("\n>> Resumen de ubicaciones disponibles:")
        print(f"   Departamento Caquetá: ID {caqueta.id if caqueta else 'N/A'}")
        print(f"   Municipio Florencia: ID {florencia.id if florencia else 'N/A'}")
        if zona_01:
            print(f"   Zona 01: ID {zona_01.id}")
        if puesto_01:
            print(f"   Puesto 01: ID {puesto_01.id}")
        
        print("\n✅ Usuarios de prueba creados exitosamente!")


if __name__ == '__main__':
    create_test_users()
