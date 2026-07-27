"""
Script para crear/actualizar usuarios BÁSICOS FIJOS del sistema
Estos 6 usuarios SIEMPRE deben existir, independientemente de las ubicaciones
Se ejecuta en cada despliegue para garantizar que existan y tengan las contraseñas correctas
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from werkzeug.security import generate_password_hash


def crear_usuarios_basicos_fijos():
    """Crear o actualizar los 6 usuarios básicos fijos del sistema"""
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("\n" + "=" * 80)
        print("CREANDO/ACTUALIZANDO USUARIOS BÁSICOS FIJOS")
        print("=" * 80)
        print()
        
        # Definir los 6 usuarios básicos FIJOS (sin ubicación)
        usuarios_basicos = [
            {
                'nombre': 'Super Admin',
                'rol': 'super_admin',
                'password': 'admin123',
                'descripcion': 'Administrador principal del sistema'
            },
            {
                'nombre': 'Monitoreo',
                'rol': 'monitoreo',
                'password': 'test123',
                'descripcion': 'Usuario de monitoreo en tiempo real'
            },
            {
                'nombre': 'Coordinador Departamental',
                'rol': 'coordinador_departamental',
                'password': 'test123',
                'descripcion': 'Coordinador a nivel departamental'
            },
            {
                'nombre': 'Coordinador Municipal',
                'rol': 'coordinador_municipal',
                'password': 'test123',
                'descripcion': 'Coordinador a nivel municipal'
            },
            {
                'nombre': 'Coordinador Puesto',
                'rol': 'coordinador_puesto',
                'password': 'test123',
                'descripcion': 'Coordinador de puesto de votación'
            },
            {
                'nombre': 'Auditor Electoral',
                'rol': 'auditor_electoral',
                'password': 'test123',
                'descripcion': 'Auditor del proceso electoral'
            }
        ]
        
        usuarios_creados = 0
        usuarios_actualizados = 0
        
        print("Procesando usuarios básicos fijos...")
        print("-" * 80)
        
        for usuario_data in usuarios_basicos:
            # Buscar usuario por rol y nombre
            usuario = User.query.filter_by(
                rol=usuario_data['rol'],
                nombre=usuario_data['nombre']
            ).first()
            
            if usuario:
                # Usuario existe - ACTUALIZAR contraseña y desbloquear
                print(f"[UPDATE] {usuario_data['nombre']} ({usuario_data['rol']})")
                
                usuario.password_hash = generate_password_hash(usuario_data['password'])
                usuario.activo = True
                usuario.intentos_fallidos = 0
                usuario.bloqueado_hasta = None
                usuario.ubicacion_id = None  # Sin ubicación
                usuario.es_usuario_basico = True  # Marcar como usuario básico fijo
                
                print(f"         ✅ Contraseña actualizada: {usuario_data['password']}")
                print(f"         ✅ Usuario desbloqueado y activado")
                print(f"         🔒 Marcado como usuario básico fijo")
                usuarios_actualizados += 1
                
            else:
                # Usuario NO existe - CREAR
                print(f"[CREATE] {usuario_data['nombre']} ({usuario_data['rol']})")
                
                usuario = User(
                    nombre=usuario_data['nombre'],
                    password_hash=generate_password_hash(usuario_data['password']),
                    rol=usuario_data['rol'],
                    ubicacion_id=None,  # Sin ubicación
                    activo=True,
                    es_usuario_basico=True  # Marcar como usuario básico fijo
                )
                
                db.session.add(usuario)
                print(f"         ✅ Usuario creado con contraseña: {usuario_data['password']}")
                print(f"         🔒 Marcado como usuario básico fijo")
                usuarios_creados += 1
            
            print()
        
        # Commit de todos los cambios
        try:
            db.session.commit()
            print("=" * 80)
            print("✅ CAMBIOS GUARDADOS EXITOSAMENTE")
            print("=" * 80)
        except Exception as e:
            db.session.rollback()
            print("=" * 80)
            print(f"❌ ERROR AL GUARDAR: {e}")
            print("=" * 80)
            return False
        
        # Resumen
        print()
        print("=" * 80)
        print("RESUMEN")
        print("=" * 80)
        print(f"✅ Usuarios creados: {usuarios_creados}")
        print(f"🔄 Usuarios actualizados: {usuarios_actualizados}")
        print(f"📊 Total procesados: {len(usuarios_basicos)}")
        print()
        
        # Verificar que todos existen
        print("=" * 80)
        print("VERIFICACIÓN FINAL")
        print("=" * 80)
        
        for usuario_data in usuarios_basicos:
            usuario = User.query.filter_by(
                rol=usuario_data['rol'],
                nombre=usuario_data['nombre']
            ).first()
            
            if usuario:
                estado = "✅ ACTIVO" if usuario.activo else "❌ INACTIVO"
                bloqueado = "🔒 BLOQUEADO" if usuario.bloqueado_hasta else "🔓 DESBLOQUEADO"
                print(f"{estado} | {bloqueado} | {usuario.nombre} ({usuario.rol})")
                print(f"         ID: {usuario.id} | Password: {usuario_data['password']}")
            else:
                print(f"❌ ERROR | {usuario_data['nombre']} ({usuario_data['rol']}) NO EXISTE")
            print()
        
        # Credenciales finales
        print("=" * 80)
        print("CREDENCIALES DE ACCESO")
        print("=" * 80)
        print()
        print("🔐 SUPER ADMIN:")
        print("   Rol: super_admin")
        print("   Contraseña: admin123")
        print()
        print("✅ TODOS LOS DEMÁS USUARIOS:")
        print("   Contraseña: test123")
        print()
        print("📋 Lista de usuarios:")
        print("   - Super Admin (super_admin)")
        print("   - Monitoreo (monitoreo)")
        print("   - Coordinador Departamental (coordinador_departamental)")
        print("   - Coordinador Municipal (coordinador_municipal)")
        print("   - Coordinador Puesto (coordinador_puesto)")
        print("   - Auditor Electoral (auditor_electoral)")
        print()
        print("=" * 80)
        print("✅ USUARIOS BÁSICOS FIJOS LISTOS")
        print("=" * 80)
        print()
        
        return True


if __name__ == '__main__':
    try:
        success = crear_usuarios_basicos_fijos()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
