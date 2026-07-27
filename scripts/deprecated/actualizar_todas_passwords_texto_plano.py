"""
Script para actualizar TODAS las contraseñas a texto plano
Sin borrar la base de datos
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.app import create_app
from backend.database import db
from backend.models.user import User

app = create_app(os.getenv('FLASK_ENV', 'development'))

# Mapeo de contraseñas por rol
PASSWORDS = {
    'super_admin': 'SuperAdmin123!',
    'admin_departamental': 'AdminDept123!',
    'admin_municipal': 'AdminMuni123!',
    'coordinador_departamental': 'CoordDept123!',
    'coordinador_municipal': 'CoordMuni123!',
    'auditor_electoral': 'Auditor123!',
    'coordinador_puesto': 'CoordPuesto123!',
    'testigo_electoral': 'Testigo123!'
}

with app.app_context():
    print("\n" + "="*80)
    print("ACTUALIZANDO CONTRASEÑAS A TEXTO PLANO")
    print("="*80)
    
    users = User.query.all()
    
    print(f"\n📊 Total de usuarios encontrados: {len(users)}\n")
    
    updated = 0
    for user in users:
        password = PASSWORDS.get(user.rol, 'test123')
        
        # Actualizar directamente el password_hash sin usar set_password
        # para asegurar que se guarde en texto plano
        user.password_hash = password
        
        print(f"✅ {user.nombre} ({user.rol})")
        print(f"   Nueva contraseña: {password}")
        
        updated += 1
    
    # Guardar todos los cambios
    db.session.commit()
    
    print(f"\n" + "="*80)
    print(f"✅ {updated} contraseñas actualizadas a texto plano")
    print("="*80)
    
    print("\n🔑 CONTRASEÑAS ACTUALIZADAS:")
    print("-" * 80)
    for rol, password in PASSWORDS.items():
        print(f"  {rol}: {password}")
    print("-" * 80)
