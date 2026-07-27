"""
Script consolidado de inicialización del sistema
Este es el ÚNICO script que debes usar para inicializar el sistema
Reemplaza a todos los scripts antiguos de inicialización
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location


def init_system(force_reset_passwords=False):
    """
    Inicializar sistema completo
    
    Args:
        force_reset_passwords: Si True, resetea todas las contraseñas a valores por defecto
    """
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("\n" + "=" * 80)
        print("INICIALIZACIÓN DEL SISTEMA ELECTORAL")
        print("=" * 80)
        print()
        
        # 1. Verificar/crear tablas
        print("📋 Paso 1: Verificando estructura de base de datos...")
        db.create_all()
        print("   ✅ Tablas verificadas/creadas")
        print()
        
        # 2. Verificar usuarios básicos
        print("👥 Paso 2: Verificando usuarios básicos del sistema...")
        usuarios_creados = _init_usuarios_basicos(force_reset_passwords)
        print(f"   ✅ {usuarios_creados} usuarios procesados")
        print()
        
        # 3. Verificar ubicaciones
        print("📍 Paso 3: Verificando ubicaciones (DIVIPOLA)...")
        total_locations = Location.query.count()
        if total_locations == 0:
            print("   ⚠️  No hay ubicaciones cargadas")
            print("   💡 Ejecuta: python scripts/load_divipola.py")
        else:
            print(f"   ✅ {total_locations} ubicaciones en la base de datos")
        print()
        
        # 4. Verificar configuración electoral
        print("⚙️  Paso 4: Verificando configuración electoral...")
        from backend.models.configuracion_electoral import TipoEleccion
        from backend.models.partido_politico import PartidoPolitico
        tipos = TipoEleccion.query.count()
        partidos = PartidoPolitico.query.count()
        
        if tipos == 0 or partidos == 0:
            print("   ⚠️  Configuración electoral incompleta")
            print("   💡 Ejecuta: python scripts/init_configuracion_electoral.py")
        else:
            print(f"   ✅ {tipos} tipos de elección, {partidos} partidos configurados")
        print()
        
        # Resumen final
        print("=" * 80)
        print("RESUMEN DE INICIALIZACIÓN")
        print("=" * 80)
        print()
        print("✅ Sistema inicializado correctamente")
        print()
        print("🔐 CREDENCIALES DE ACCESO:")
        print()
        print("   Super Admin:")
        print("   - Rol: super_admin")
        print("   - Contraseña: admin123")
        print()
        print("   Otros usuarios:")
        print("   - Monitoreo (monitoreo): test123")
        print("   - Coordinador Departamental (coordinador_departamental): test123")
        print("   - Coordinador Municipal (coordinador_municipal): test123")
        print("   - Coordinador Puesto (coordinador_puesto): test123")
        print("   - Auditor Electoral (auditor_electoral): test123")
        print()
        print("⚠️  IMPORTANTE: Cambia todas las contraseñas después del primer acceso")
        print()
        print("=" * 80)
        print()
        
        return True


def _init_usuarios_basicos(force_reset=False):
    """
    Inicializar usuarios básicos del sistema
    
    Args:
        force_reset: Si True, resetea contraseñas incluso si el usuario existe
        
    Returns:
        int: Número de usuarios procesados
    """
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
    
    usuarios_procesados = 0
    
    for usuario_data in usuarios_basicos:
        # Buscar usuario por rol y nombre
        usuario = User.query.filter_by(
            rol=usuario_data['rol'],
            nombre=usuario_data['nombre']
        ).first()
        
        if usuario:
            # Usuario existe
            if force_reset:
                # Resetear contraseña
                usuario.set_password(usuario_data['password'])
                usuario.activo = True
                usuario.intentos_fallidos = 0
                usuario.bloqueado_hasta = None
                print(f"   🔄 {usuario_data['nombre']} - contraseña reseteada")
            else:
                # Solo asegurar que esté activo
                if not usuario.activo:
                    usuario.activo = True
                    print(f"   ✅ {usuario_data['nombre']} - activado")
                else:
                    print(f"   ✅ {usuario_data['nombre']} - OK")
        else:
            # Usuario NO existe - CREAR
            usuario = User(
                nombre=usuario_data['nombre'],
                rol=usuario_data['rol'],
                ubicacion_id=None,
                activo=True,
                es_usuario_basico=True
            )
            usuario.set_password(usuario_data['password'])
            db.session.add(usuario)
            print(f"   ➕ {usuario_data['nombre']} - creado")
        
        usuarios_procesados += 1
    
    # Commit de todos los cambios
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"   ❌ Error al guardar: {e}")
        raise
    
    return usuarios_procesados


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Inicializar sistema electoral')
    parser.add_argument(
        '--reset-passwords',
        action='store_true',
        help='Resetear contraseñas de usuarios básicos a valores por defecto'
    )
    
    args = parser.parse_args()
    
    try:
        success = init_system(force_reset_passwords=args.reset_passwords)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
