"""
Script simple para ejecutar en la consola de Render
Copia y pega este código completo en la consola de Render
"""

# Importar dependencias
from backend.app import create_app
from backend.database import db
from backend.models.user import User
from werkzeug.security import generate_password_hash

# Crear app context
app = create_app()

with app.app_context():
    print("\n=== RESETEANDO CONTRASEÑAS ===\n")
    
    # Definir contraseñas
    passwords = {
        'super_admin': 'admin123',
        'monitoreo': 'test123',
        'coordinador_departamental': 'test123',
        'coordinador_municipal': 'test123',
        'coordinador_puesto': 'test123',
        'auditor_electoral': 'test123'
    }
    
    # Actualizar cada usuario
    for rol, password in passwords.items():
        usuario = User.query.filter_by(rol=rol).first()
        
        if usuario:
            usuario.password_hash = generate_password_hash(password)
            usuario.activo = True
            usuario.intentos_fallidos = 0
            usuario.bloqueado_hasta = None
            print(f"✓ {usuario.nombre} ({rol}) → {password}")
        else:
            print(f"✗ Usuario no encontrado: {rol}")
    
    # Guardar cambios
    db.session.commit()
    print("\n✓ Contraseñas actualizadas exitosamente\n")
    
    # Verificar usuarios
    print("=== USUARIOS EN LA BASE DE DATOS ===\n")
    usuarios = User.query.all()
    for u in usuarios:
        print(f"ID: {u.id} | {u.nombre} | {u.rol} | Activo: {u.activo}")
    
    print(f"\nTotal: {len(usuarios)} usuarios\n")
