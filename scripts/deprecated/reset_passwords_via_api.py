"""
Script para resetear contraseñas directamente en la BD de Render
Usar este script cuando el endpoint no funcione
"""
import os
import sys

# Configurar para usar la BD de Render
os.environ['DATABASE_URL'] = 'postgresql://electoral_db_user:password@dpg-xxxxx/electoral_db'
os.environ['FLASK_ENV'] = 'production'

from backend.app import create_app
from backend.database import db
from backend.models.user import User

def reset_all_passwords():
    """Resetear todas las contraseñas"""
    
    app = create_app('production')
    
    with app.app_context():
        print("\n🔄 Reseteando contraseñas...")
        
        # Obtener todos los usuarios
        usuarios = User.query.all()
        
        if not usuarios:
            print("❌ No hay usuarios en la base de datos")
            return
        
        print(f"📋 Encontrados {len(usuarios)} usuarios")
        print("-" * 60)
        
        # Resetear contraseñas
        for usuario in usuarios:
            # Contraseña especial para admin
            if usuario.rol == 'super_admin':
                usuario.set_password('admin123')
                password = 'admin123'
            else:
                usuario.set_password('test123')
                password = 'test123'
            
            print(f"✅ {usuario.nombre} ({usuario.rol})")
            print(f"   Usuario: {usuario.nombre}")
            print(f"   Contraseña: {password}")
            print("-" * 60)
        
        db.session.commit()
        
        print(f"\n✅ {len(usuarios)} contraseñas reseteadas exitosamente!")

if __name__ == '__main__':
    print("⚠️  IMPORTANTE: Este script debe ejecutarse EN EL SERVIDOR de Render")
    print("   No funcionará desde tu máquina local")
    print()
    
    respuesta = input("¿Estás ejecutando esto en Render? (s/n): ")
    
    if respuesta.lower() == 's':
        reset_all_passwords()
    else:
        print("\n📝 Para resetear contraseñas en Render:")
        print("   1. Ve al dashboard de Render")
        print("   2. Abre la Shell de tu servicio")
        print("   3. Ejecuta: python reset_passwords_via_api.py")
