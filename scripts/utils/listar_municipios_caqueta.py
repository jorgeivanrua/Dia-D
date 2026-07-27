"""
Listar municipios de Caquetá disponibles en la BD
"""
from backend.database import db
from backend.models.location import Location
from backend.app import create_app

app = create_app()
app.app_context().push()

print("\n" + "="*60)
print("MUNICIPIOS DE CAQUETÁ EN LA BASE DE DATOS")
print("="*60)

# Obtener municipios de Caquetá (código 44)
municipios = Location.query.filter_by(
    departamento_codigo='44',
    tipo='municipio'
).order_by(Location.municipio_nombre).all()

if municipios:
    print(f"\nTotal: {len(municipios)} municipios\n")
    
    for i, mun in enumerate(municipios, 1):
        # Contar puestos del municipio
        puestos = Location.query.filter_by(
            municipio_codigo=mun.municipio_codigo,
            departamento_codigo=mun.departamento_codigo,
            tipo='puesto'
        ).count()
        
        print(f"{i}. {mun.municipio_nombre}")
        print(f"   ID: {mun.id}")
        print(f"   Código: {mun.municipio_codigo}")
        print(f"   Puestos: {puestos}")
        print()
else:
    print("\n❌ No se encontraron municipios de Caquetá")

print("="*60 + "\n")
