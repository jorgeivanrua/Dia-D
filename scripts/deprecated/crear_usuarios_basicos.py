"""
Crear o actualizar usuarios básicos del sistema
Estos usuarios deben existir siempre en la base de datos
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from werkzeug.security import generate_password_hash

def crear_usuarios_basicos():
    """Crear o actualizar usuarios básicos del sistema"""
    
    print("\n" + "="*70)
    print("CREANDO/ACTUALIZANDO USUARIOS BÁSICOS DEL SISTEMA")
    print("="*70)
    
    # Definir usuarios básicos
    usuarios_basicos = [
        {
            'nombre': 'Super Admin',
            'password': 'admin123',
            'rol': 'super_admin',
            'activo': True,
            'descripcion': 'Administrador principal del sistema'
        },
        {
            'nombre': 'Monitoreo',
            'password': 'test123',
            'rol': 'monitoreo',
            'activo': True,
            'descripcion': 'Usuario de monitoreo en tiempo real'
        },
        {
            'nombre': 'Coordinador Departamental',
            'password': 'test123',
            'rol': 'coordinador_departamental',
            'activo': True,
            'descripcion': 'Coordinador a nivel departamental'
        },
        {
            'nombre': 'Coordinador Municipal',
            'password': 'test123',
            'rol': 'coordinador_municipal',
            'activo': True,
            'descripcion': 'Coordinador a nivel municipal'
        },
        {
            'nombre': 'Coordinador Puesto',
            'password': 'test123',
            'rol': 'coordinador_puesto',
            'activo': True,
            'descripcion': 'Coordinador de puesto de votación'
        },
        {
            'nombre': 'Auditor Electoral',
            'password': 'test123',
            'rol': 'auditor_electoral',
            'activo': True,
            'descripcion': 'Auditor del proceso electoral'
        }
    ]
    
    usuarios_creados = 0
    usuarios_actualizados = 0
    
    for usuario_data in usuarios_basicos:
        # Buscar usuario por rol (asumiendo que solo hay uno por rol básico)
        usuario = User.query.filter_by(
            rol=usuario_data['rol'],
            nombre=usuario_data['nombre']
        ).first()
        
        if usuario:
            # Actualizar usuario existente
            print(f"[UPDATE] Actualizando: {usuario_data['nombre']} ({usuario_data['rol']})")
            usuario.activo = usuario_data['activo']
            # Solo actualizar password si es necesario
            # usuario.password_hash = generate_password_hash(usuario_data['password'])
            usuarios_actualizados += 1
        else:
            # Crear nuevo usuario
            print(f"[CREATE] Creando: {usuario_data['nombre']} ({usuario_data['rol']})")
            usuario = User(
                nombre=usuario_data['nombre'],
                password_hash=generate_password_hash(usuario_data['password']),
                rol=usuario_data['rol'],
                activo=usuario_data['activo']
            )
            db.session.add(usuario)
            usuarios_creados += 1
    
    db.session.commit()
    
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    print(f"[OK] Usuarios creados: {usuarios_creados}")
    print(f"[OK] Usuarios actualizados: {usuarios_actualizados}")
    print(f"[OK] Total de usuarios basicos: {len(usuarios_basicos)}")
    print("="*70 + "\n")
    
    # Mostrar todos los usuarios básicos
    print("Usuarios basicos en la base de datos:")
    print("-" * 70)
    for usuario_data in usuarios_basicos:
        usuario = User.query.filter_by(
            rol=usuario_data['rol'],
            nombre=usuario_data['nombre']
        ).first()
        
        if usuario:
            estado = "[ACTIVO]" if usuario.activo else "[INACTIVO]"
            print(f"  {estado} | {usuario.nombre:30} | {usuario.rol:30}")
            print(f"           Password: {usuario_data['password']}")
            print(f"           ID: {usuario.id}")
            print()
    
    print("\n" + "="*70)
    print("[WARNING] IMPORTANTE: Cambiar las contrasenas en produccion")
    print("="*70 + "\n")
    
    return True

def main():
    """Ejecutar creación de usuarios básicos"""
    app = create_app()
    
    with app.app_context():
        try:
            crear_usuarios_basicos()
            print("[OK] Usuarios basicos creados/actualizados exitosamente\n")
            return 0
        except Exception as e:
            print(f"\n[ERROR] Error creando usuarios basicos: {str(e)}\n")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return 1

if __name__ == '__main__':
    sys.exit(main())
