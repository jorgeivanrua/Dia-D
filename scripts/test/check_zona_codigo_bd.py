"""
Verificar zona_codigo en la base de datos
"""
from backend.database import db
from backend.models.location import Location
from backend.app import create_app

app = create_app()
app.app_context().push()

# Obtener puestos de Florencia (Caquetá)
puestos = Location.query.filter_by(
    municipio_codigo='01',
    departamento_codigo='44',
    tipo='puesto'
).limit(5).all()

print(f"\n✅ Encontrados {len(puestos)} puestos\n")

for puesto in puestos:
    print(f"Puesto: {puesto.puesto_codigo} - {puesto.puesto_nombre}")
    print(f"  zona_codigo: '{puesto.zona_codigo}'")
    print(f"  tipo: {type(puesto.zona_codigo)}")
    print()
