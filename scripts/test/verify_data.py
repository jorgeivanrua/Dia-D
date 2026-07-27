"""
Script para verificar datos cargados
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.models.location import Location

app = create_app('development')

with app.app_context():
    print("\n>> Verificando datos cargados...")
    print(f"Total ubicaciones: {Location.query.count()}")
    print(f"Departamentos: {Location.query.filter_by(tipo='departamento').count()}")
    print(f"Municipios: {Location.query.filter_by(tipo='municipio').count()}")
    print(f"Zonas: {Location.query.filter_by(tipo='zona').count()}")
    print(f"Puestos: {Location.query.filter_by(tipo='puesto').count()}")
    print(f"Mesas: {Location.query.filter_by(tipo='mesa').count()}")
    
    print("\n>> Municipios de Caqueta:")
    municipios = Location.query.filter_by(tipo='municipio').all()
    for muni in municipios:
        print(f"  - {muni.municipio_nombre}")
