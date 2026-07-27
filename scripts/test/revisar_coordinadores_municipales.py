"""
Revisar todos los coordinadores municipales y sus ubicaciones
"""
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.app import create_app

app = create_app()
app.app_context().push()

print("\n" + "="*70)
print("REVISIÓN DE COORDINADORES MUNICIPALES")
print("="*70)

# Obtener todos los coordinadores municipales
coordinadores = User.query.filter_by(rol='coordinador_municipal').all()

print(f"\nTotal coordinadores municipales: {len(coordinadores)}\n")

problemas = []

for coord in coordinadores:
    print(f"Usuario: {coord.nombre}")
    print(f"  ID: {coord.id}")
    print(f"  Activo: {coord.activo}")
    print(f"  Ubicación ID: {coord.ubicacion_id}")
    
    if coord.ubicacion_id:
        ubicacion = Location.query.get(coord.ubicacion_id)
        if ubicacion:
            print(f"  Tipo: {ubicacion.tipo}")
            print(f"  Municipio: {ubicacion.municipio_nombre}")
            print(f"  Departamento: {ubicacion.departamento_nombre}")
            print(f"  Código Mun: {ubicacion.municipio_codigo}")
            print(f"  Código Dept: {ubicacion.departamento_codigo}")
            
            # Verificar que sea tipo municipio
            if ubicacion.tipo != 'municipio':
                problemas.append({
                    'usuario': coord.nombre,
                    'problema': f'Ubicación no es tipo municipio (es {ubicacion.tipo})',
                    'ubicacion_id': coord.ubicacion_id
                })
            
            # Contar puestos
            puestos = Location.query.filter_by(
                municipio_codigo=ubicacion.municipio_codigo,
                departamento_codigo=ubicacion.departamento_codigo,
                tipo='puesto'
            ).count()
            print(f"  Puestos: {puestos}")
        else:
            problemas.append({
                'usuario': coord.nombre,
                'problema': 'Ubicación ID no existe en BD',
                'ubicacion_id': coord.ubicacion_id
            })
            print(f"  ⚠️ Ubicación no encontrada en BD")
    else:
        problemas.append({
            'usuario': coord.nombre,
            'problema': 'Sin ubicación asignada',
            'ubicacion_id': None
        })
        print(f"  ⚠️ Sin ubicación asignada")
    
    print()

# Mostrar resumen de problemas
if problemas:
    print("\n" + "="*70)
    print("PROBLEMAS ENCONTRADOS")
    print("="*70 + "\n")
    
    for i, p in enumerate(problemas, 1):
        print(f"{i}. Usuario: {p['usuario']}")
        print(f"   Problema: {p['problema']}")
        if p['ubicacion_id']:
            print(f"   Ubicación ID: {p['ubicacion_id']}")
        print()
else:
    print("✅ No se encontraron problemas")

# Listar municipios disponibles
print("\n" + "="*70)
print("MUNICIPIOS DISPONIBLES EN CAQUETÁ")
print("="*70 + "\n")

municipios = Location.query.filter_by(
    departamento_codigo='44',
    tipo='municipio'
).order_by(Location.municipio_nombre).all()

for mun in municipios:
    puestos = Location.query.filter_by(
        municipio_codigo=mun.municipio_codigo,
        departamento_codigo=mun.departamento_codigo,
        tipo='puesto'
    ).count()
    
    # Verificar si tiene coordinador asignado
    coord_asignado = User.query.filter_by(
        ubicacion_id=mun.id,
        rol='coordinador_municipal'
    ).first()
    
    estado = "✅ Asignado" if coord_asignado else "⚠️ Sin coordinador"
    coord_nombre = f" ({coord_asignado.nombre})" if coord_asignado else ""
    
    print(f"• {mun.municipio_nombre} (ID: {mun.id}, Código: {mun.municipio_codigo})")
    print(f"  Puestos: {puestos} | {estado}{coord_nombre}")

print("\n" + "="*70 + "\n")
