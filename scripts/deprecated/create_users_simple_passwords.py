"""
Script para crear usuarios con contraseñas simples
admin123 para super_admin
test123 para todos los demás
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location


def create_users_simple():
    """Crear usuarios con contraseñas simples"""
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("\n>> Creando usuarios con contraseñas simples...")
        
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
                'nombre': 'admin',
                'rol': 'super_admin',
                'ubicacion_id': None,
                'password': 'admin123'
            },
            {
                'nombre': 'Admin Departamental Caquetá',
                'rol': 'admin_departamental',
                'ubicacion_id': caqueta.id if caqueta else None,
                'password': 'test123'
            },
            {
                'nombre': 'Admin Municipal Florencia',
                'rol': 'admin_municipal',
                'ubicacion_id': florencia.id if florencia else None,
                'password': 'test123'
            },
            {
                'nombre': 'Coordinador Departamental Caquetá',
                'rol': 'coordinador_departamental',
                'ubicacion_id': caqueta.id if caqueta else None,
                'password': 'test123'
            },
            {
                'nombre': 'Coordinador Municipal Florencia',
                'rol': 'coordinador_municipal',
                'ubicacion_id': florencia.id if florencia else None,
                'password': 'test123'
            },
            {
                'nombre': 'Auditor Electoral Caquetá',
                'rol': 'auditor_electoral',
                'ubicacion_id': caqueta.id if caqueta else None,
                'password': 'test123'
            }
        ]
        
        # Agregar coordinadores de puesto para cada puesto disponible
        puestos = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo='44',
            municipio_codigo='01'
        ).all()
        
        print(f"\n>> Encontrados {len(puestos)} puestos de votación")
        
        for puesto in puestos:
            # Crear coordinador de puesto
            users_to_create.append({
                'nombre': f'Coordinador {puesto.nombre_completo}',
                'rol': 'coordinador_puesto',
                'ubicacion_id': puesto.id,
                'password': 'test123'
            })
            
            # Obtener todas las mesas de este puesto
            mesas = Location.query.filter_by(
                tipo='mesa',
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                zona_codigo=puesto.zona_codigo,
                puesto_codigo=puesto.puesto_codigo
            ).all()
            
            print(f"   Puesto {puesto.puesto_codigo}: {len(mesas)} mesas")
            
            # Crear un testigo por cada mesa, pero asignado al PUESTO
            # Se individualizarán cuando verifiquen presencia en una mesa específica
            for i, mesa in enumerate(mesas, 1):
                users_to_create.append({
                    'nombre': f'Testigo {i} - {puesto.nombre_completo}',
                    'rol': 'testigo_electoral',
                    'ubicacion_id': puesto.id,  # Asignar al puesto, no a la mesa
                    'password': 'test123'
                })
        
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
                print(f"   Contraseña: {user_data['password']}")
                created_count += 1
                
            except Exception as e:
                print(f"❌ Error creando {user_data['nombre']}: {e}")
                db.session.rollback()
        
        print(f"\n>> Total de usuarios creados: {created_count}")
        
        # Mostrar resumen
        print("\n" + "="*60)
        print("CREDENCIALES DEL SISTEMA")
        print("="*60)
        print("\n🔑 Super Admin:")
        print("   Usuario: admin")
        print("   Contraseña: admin123")
        print("\n🔑 Todos los demás usuarios:")
        print("   Contraseña: test123")
        print("\n" + "="*60)
        
        print("\n✅ Usuarios creados exitosamente!")


if __name__ == '__main__':
    create_users_simple()
