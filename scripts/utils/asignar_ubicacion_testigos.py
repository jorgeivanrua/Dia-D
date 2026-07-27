"""
Script para asignar ubicaciones a testigos que no las tienen
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

app = create_app()

with app.app_context():
    print("🔍 Buscando testigos sin ubicación...")
    
    testigos = User.query.filter_by(rol='testigo_electoral').all()
    
    print(f"\n📊 Total testigos: {len(testigos)}")
    
    for testigo in testigos:
        print(f"\n👤 Testigo: {testigo.nombre} (ID: {testigo.id})")
        print(f"   Ubicación actual: {testigo.ubicacion_id}")
        
        if not testigo.ubicacion_id:
            # Buscar una mesa disponible en Florencia
            mesa = Location.query.filter_by(
                tipo='mesa',
                municipio_codigo='18001',  # Florencia
                activo=True
            ).first()
            
            if mesa:
                testigo.ubicacion_id = mesa.id
                db.session.commit()
                print(f"   ✅ Asignado a mesa: {mesa.mesa_codigo} - {mesa.puesto_nombre}")
            else:
                print(f"   ⚠️  No hay mesas disponibles")
        else:
            location = Location.query.get(testigo.ubicacion_id)
            if location:
                print(f"   ✅ Ya tiene ubicación: {location.tipo} - {location.mesa_codigo if location.tipo == 'mesa' else location.puesto_nombre}")
    
    print("\n✅ Proceso completado")
