"""
Actualizar contraseña del usuario Monitoreo (con mayúscula)
"""
from backend.app import create_app
from backend.models.user import User
from backend.database import db
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Buscar usuario Monitoreo (con mayúscula)
    usuario = User.query.filter_by(rol='monitoreo', nombre='Monitoreo').first()
    
    if usuario:
        print(f'Usuario encontrado: {usuario.nombre}')
        print(f'Rol: {usuario.rol}')
        print(f'Activo: {usuario.activo}')
        
        # Actualizar contraseña
        usuario.password_hash = generate_password_hash('monitoreo123')
        usuario.activo = True
        db.session.commit()
        
        print('✓ Contraseña actualizada a: monitoreo123')
        print('✓ Usuario activado')
        print('\nCredenciales para login:')
        print('  Rol: monitoreo')
        print('  Nombre: Monitoreo')
        print('  Contraseña: monitoreo123')
    else:
        print('✗ Usuario Monitoreo no encontrado')
        print('\nBuscando todos los usuarios con rol monitoreo...')
        usuarios = User.query.filter_by(rol='monitoreo').all()
        print(f'Encontrados: {len(usuarios)}')
        for u in usuarios:
            print(f'  - {u.nombre} (activo: {u.activo})')
