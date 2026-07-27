"""
Script para verificar si existe el usuario de monitoreo
"""
from backend.database import db
from backend.models.user import User
from backend.app import create_app

app = create_app()

with app.app_context():
    # Buscar usuario de monitoreo
    user = User.query.filter_by(rol='monitoreo').first()
    
    if user:
        print(f"✓ Usuario de monitoreo existe:")
        print(f"  - Nombre: {user.nombre}")
        print(f"  - ID: {user.id}")
        print(f"  - Activo: {user.activo}")
    else:
        print("✗ No existe usuario con rol 'monitoreo'")
        print("\nCreando usuario de monitoreo...")
        
        # Crear usuario de monitoreo
        nuevo_user = User(
            nombre='monitoreo',
            rol='monitoreo',
            ubicacion_id=None,
            activo=True
        )
        nuevo_user.set_password('test123')
        
        db.session.add(nuevo_user)
        db.session.commit()
        
        print(f"✓ Usuario de monitoreo creado:")
        print(f"  - Nombre: monitoreo")
        print(f"  - Contraseña: test123")
        print(f"  - Rol: monitoreo")
