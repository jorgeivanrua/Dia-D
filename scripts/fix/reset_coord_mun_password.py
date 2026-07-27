"""
Resetear contraseña del coordinador municipal
"""
from backend.database import db
from backend.models.user import User
from backend.app import create_app

app = create_app()
app.app_context().push()

# Buscar coordinador municipal
coord = User.query.filter_by(nombre='coord_mun', rol='coordinador_municipal').first()

if coord:
    # Resetear contraseña a 'coord123'
    coord.set_password('coord123')
    db.session.commit()
    
    print(f"✅ Contraseña reseteada para usuario: {coord.nombre}")
    print(f"   Rol: {coord.rol}")
    print(f"   Nueva contraseña: coord123")
    print(f"   Ubicación ID: {coord.ubicacion_id}")
else:
    print("❌ Usuario coordinador municipal no encontrado")
