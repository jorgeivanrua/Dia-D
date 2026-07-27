"""
Script para resetear contraseñas de usuarios básicos en Render
Ejecutar este script en la consola de Render o localmente conectado a la BD de Render
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from werkzeug.security import generate_password_hash

def resetear_passwords():
    """Resetear contraseñas de usuarios básicos"""
    
    print("\n" + "="*70)
    print("RESETEANDO CONTRASEÑAS DE USUARIOS BÁSICOS")
    print("="*70 + "\n")
    
    # Contraseñas por defecto
    passwords = {
        'super_admin': 'admin123',
        'monitoreo': 'test123',
        'coordinador_departamental': 'test123',
        'coordinador_municipal': 'test123',
        'coordinador_puesto': 'test123',
        'auditor_electoral': 'test123'
    }
    
    usuarios_actualizados = []
    usuarios_no_encontrados = []
    
    for rol, password in passwords.items():
        # Buscar usuario por rol
        usuario = User.query.filter_by(rol=rol).first()
        
        if usuario:
            print(f"[UPDATE] Actualizando contraseña de: {usuario.nombre} ({rol})")
            usuario.password_hash = generate_password_hash(password)
            usuario.activo = True
            usuario.intentos_fallidos = 0
            usuario.bloqueado_hasta = None
            
            usuarios_actualizados.append({
                'id': usuario.id,
                'nombre': usuario.nombre,
                'rol': rol,
                'password': password
            })
        else:
            print(f"[WARNING] Usuario no encontrado: {rol}")
            usuarios_no_encontrados.append(rol)
    
    # Commit de cambios
    try:
        db.session.commit()
        print("\n[OK] Contraseñas actualizadas exitosamente\n")
    except Exception as e:
        db.session.rollback()
        print(f"\n[ERROR] Error al actualizar contraseñas: {str(e)}\n")
        return False
    
    # Mostrar resumen
    print("="*70)
    print("RESUMEN DE CONTRASEÑAS ACTUALIZADAS")
    print("="*70)
    
    for usuario in usuarios_actualizados:
        print(f"\n  Usuario: {usuario['nombre']}")
        print(f"  Rol: {usuario['rol']}")
        print(f"  Contraseña: {usuario['password']}")
        print(f"  ID: {usuario['id']}")
    
    if usuarios_no_encontrados:
        print("\n" + "="*70)
        print("USUARIOS NO ENCONTRADOS")
        print("="*70)
        for rol in usuarios_no_encontrados:
            print(f"  - {rol}")
    
    print("\n" + "="*70)
    print(f"[OK] Total actualizados: {len(usuarios_actualizados)}")
    print(f"[WARNING] No encontrados: {len(usuarios_no_encontrados)}")
    print("="*70 + "\n")
    
    return True

def verificar_usuarios():
    """Verificar todos los usuarios en la base de datos"""
    
    print("\n" + "="*70)
    print("VERIFICANDO USUARIOS EN LA BASE DE DATOS")
    print("="*70 + "\n")
    
    usuarios = User.query.all()
    
    if not usuarios:
        print("[WARNING] No hay usuarios en la base de datos\n")
        return
    
    print(f"Total de usuarios: {len(usuarios)}\n")
    
    for usuario in usuarios:
        estado = "[ACTIVO]" if usuario.activo else "[INACTIVO]"
        bloqueado = "[BLOQUEADO]" if usuario.bloqueado_hasta else ""
        
        print(f"{estado} {bloqueado}")
        print(f"  ID: {usuario.id}")
        print(f"  Nombre: {usuario.nombre}")
        print(f"  Rol: {usuario.rol}")
        print(f"  Intentos fallidos: {usuario.intentos_fallidos}")
        print(f"  Último acceso: {usuario.ultimo_acceso}")
        print()
    
    print("="*70 + "\n")

def main():
    """Ejecutar script"""
    app = create_app()
    
    with app.app_context():
        try:
            # Primero verificar usuarios existentes
            verificar_usuarios()
            
            # Preguntar si desea resetear
            print("\n¿Desea resetear las contraseñas? (s/n): ", end='')
            respuesta = input().lower()
            
            if respuesta == 's':
                resetear_passwords()
                print("\n[OK] Proceso completado exitosamente\n")
            else:
                print("\n[INFO] Operación cancelada\n")
            
            return 0
            
        except Exception as e:
            print(f"\n[ERROR] Error: {str(e)}\n")
            import traceback
            traceback.print_exc()
            return 1

if __name__ == '__main__':
    sys.exit(main())
