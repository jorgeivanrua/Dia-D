"""
Corregir coordinador municipal genérico sin ubicación
"""
from backend.database import db
from backend.models.user import User
from backend.app import create_app

app = create_app()
app.app_context().push()

# Buscar coordinador genérico
coord_generico = User.query.filter_by(nombre='Coordinador Municipal', rol='coordinador_municipal').first()

if coord_generico:
    print(f"Encontrado: {coord_generico.nombre}")
    print(f"  ID: {coord_generico.id}")
    print(f"  Ubicación: {coord_generico.ubicacion_id}")
    print(f"  Activo: {coord_generico.activo}")
    
    # Desactivar este usuario genérico ya que no tiene ubicación
    coord_generico.activo = False
    db.session.commit()
    
    print(f"\n✅ Usuario desactivado (no tiene ubicación asignada)")
    print(f"   Los coordinadores específicos por municipio siguen activos")
else:
    print("No se encontró el coordinador genérico")
