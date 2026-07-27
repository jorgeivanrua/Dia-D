"""
Verificar ubicaciones de coordinadores
"""
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.app import create_app

app = create_app()
app.app_context().push()

print("\n" + "="*60)
print("VERIFICACIÓN DE UBICACIONES DE COORDINADORES")
print("="*60)

# 1. Coordinador Municipal
print("\n1. COORDINADOR MUNICIPAL:")
coord_mun = User.query.filter_by(rol='coordinador_municipal').first()
if coord_mun:
    print(f"   Usuario: {coord_mun.nombre}")
    print(f"   Ubicación ID: {coord_mun.ubicacion_id}")
    
    if coord_mun.ubicacion_id:
        ubicacion = Location.query.get(coord_mun.ubicacion_id)
        print(f"   Tipo: {ubicacion.tipo}")
        print(f"   Nombre: {ubicacion.municipio_nombre}")
        print(f"   Departamento: {ubicacion.departamento_nombre}")
        print(f"   Dept Código: {ubicacion.departamento_codigo}")
        print(f"   Mun Código: {ubicacion.municipio_codigo}")
        
        # Contar puestos del municipio
        puestos = Location.query.filter_by(
            municipio_codigo=ubicacion.municipio_codigo,
            departamento_codigo=ubicacion.departamento_codigo,
            tipo='puesto'
        ).count()
        print(f"   Total Puestos: {puestos}")
    else:
        print("   ⚠️ Sin ubicación asignada")
else:
    print("   ❌ No encontrado")

# 2. Coordinadores de Puesto
print("\n2. COORDINADORES DE PUESTO:")
coords_puesto = User.query.filter_by(rol='coordinador_puesto').limit(5).all()
if coords_puesto:
    for coord in coords_puesto:
        print(f"\n   Usuario: {coord.nombre}")
        print(f"   Ubicación ID: {coord.ubicacion_id}")
        
        if coord.ubicacion_id:
            ubicacion = Location.query.get(coord.ubicacion_id)
            if ubicacion:
                print(f"   Tipo: {ubicacion.tipo}")
                print(f"   Puesto: {ubicacion.puesto_nombre or 'N/A'}")
                print(f"   Código: {ubicacion.puesto_codigo or 'N/A'}")
                print(f"   Zona: {ubicacion.zona_codigo or 'N/A'}")
            
                # Contar mesas del puesto
                if ubicacion.tipo == 'puesto':
                    mesas = Location.query.filter_by(
                        puesto_codigo=ubicacion.puesto_codigo,
                        departamento_codigo=ubicacion.departamento_codigo,
                        municipio_codigo=ubicacion.municipio_codigo,
                        zona_codigo=ubicacion.zona_codigo,
                        tipo='mesa'
                    ).count()
                    print(f"   Total Mesas: {mesas}")
            else:
                print("   ⚠️ Ubicación no encontrada en BD")
        else:
            print("   ⚠️ Sin ubicación asignada")
else:
    print("   ❌ No encontrados")

print("\n" + "="*60)
print("✅ Verificación completada")
print("="*60 + "\n")
