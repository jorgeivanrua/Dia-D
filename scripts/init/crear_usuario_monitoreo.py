"""
Crear o actualizar usuario de monitoreo
"""
from backend.app import create_app
from backend.models.user import User
from backend.database import db
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Buscar usuario monitoreo
    usuario = User.query.filter_by(rol='monitoreo', nombre='monitoreo').first()
    
    if usuario:
        print(f'Usuario encontrado: {usuario.nombre}')
        # Actualizar contraseña
        usuario.password_hash = generate_password_hash('monitoreo123')
        usuario.activo = True
        db.session.commit()
        print('✓ Contraseña actualizada a: monitoreo123')
    else:
        # Crear nuevo usuario
        nuevo_usuario = User(
            nombre='monitoreo',
            password_hash=generate_password_hash('monitoreo123'),
            rol='monitoreo',
            activo=True
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        print('✓ Usuario creado: monitoreo / monitoreo123')
