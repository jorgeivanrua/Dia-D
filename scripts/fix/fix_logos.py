"""
Limpiar URLs de logos que no funcionan
"""
from backend.app import create_app
from backend.models.configuracion_electoral import Partido
from backend.database import db

app = create_app()
with app.app_context():
    partidos = Partido.query.filter(Partido.logo_url.isnot(None)).all()
    
    print("=" * 80)
    print("LIMPIANDO LOGOS QUE NO FUNCIONAN")
    print("=" * 80)
    
    for partido in partidos:
        print(f"Limpiando: {partido.nombre}")
        partido.logo_url = None
    
    db.session.commit()
    
    print("\n✅ Logos limpiados. Ahora se mostrarán los colores de los partidos.")
    print("=" * 80)
