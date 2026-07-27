"""
Script para actualizar contraseñas de usuarios existentes a texto plano
Ejecutar desde Shell de Render: python actualizar_passwords_texto_plano.py
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.app import create_app
from backend.database import db
from backend.models.user import User

config_name = os.getenv('FLASK_ENV', 'production')
app = create_app(config_name)

with app.app_context():
    print("\n" + "="*80)
    print("ACTUALIZANDO CONTRASEÑAS A TEXTO PLANO")
    print("="*80)
    
    # Obtener todos los usuarios
    users = User.query.all()
    
    print(f"\n📊 Total de usuarios encontrados: {len(users)}\n")
    
    updated_count = 0
    for user in users:
        try:
            # Determinar la contraseña según el rol
            if user.rol == 'super_admin':
                new_password = 'admin123'
            else:
                new_password = 'test123'
            
            # Actualizar contraseña (ahora se guarda en texto plano)
            user.set_password(new_password)
            db.session.commit()
            
            print(f"✅ {user.nombre} ({user.rol}) → Contraseña: {new_password}")
            updated_count += 1
            
        except Exception as e:
            print(f"❌ Error actualizando {user.nombre}: {e}")
            db.session.rollback()
    
    print(f"\n📊 Total de contraseñas actualizadas: {updated_count}")
    
    print("\n" + "="*80)
    print("CREDENCIALES ACTUALIZADAS")
    print("="*80)
    print("\n🔑 Super Admin:")
    print("   Usuario: admin")
    print("   Contraseña: admin123")
    print("\n🔑 Todos los demás usuarios:")
    print("   Contraseña: test123")
    print("\n" + "="*80)
    
    print("\n✅ Actualización completada!")
