"""
Desbloquear cuenta del coordinador municipal
"""
from backend.database import db
from backend.models.user import User
from backend.app import create_app
from datetime import datetime

app = create_app()
app.app_context().push()

# Buscar coordinador municipal
coord = User.query.filter_by(nombre='coord_mun', rol='coordinador_municipal').first()

if coord:
    # Desbloquear cuenta
    coord.intentos_fallidos = 0
    coord.bloqueado_hasta = None
    db.session.commit()
    
    print(f"✅ Cuenta desbloqueada: {coord.nombre}")
    print(f"   Rol: {coord.rol}")
    print(f"   Intentos fallidos: {coord.intentos_fallidos}")
    print(f"   Bloqueado hasta: {coord.bloqueado_hasta}")
    print(f"   Activo: {coord.activo}")
    print(f"\n   Puedes hacer login con:")
    print(f"   Usuario: coord_mun")
    print(f"   Contraseña: coord123")
else:
    print("❌ Usuario coordinador municipal no encontrado")
