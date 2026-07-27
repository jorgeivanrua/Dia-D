"""Script para verificar datos en la BD"""
from backend.app import create_app
from backend.models.location import Location

app = create_app()

with app.app_context():
    print("=" * 60)
    print("VERIFICACIÓN DE BASE DE DATOS")
    print("=" * 60)
    
    # Contar ubicaciones
    total_locations = Location.query.count()
    departamentos = Location.query.filter_by(tipo='departamento').count()
    municipios = Location.query.filter_by(tipo='municipio').count()
    zonas = Location.query.filter_by(tipo='zona').count()
    puestos = Location.query.filter_by(tipo='puesto').count()
    
    print(f"\nTotal ubicaciones: {total_locations}")
    print(f"Departamentos: {departamentos}")
    print(f"Municipios: {municipios}")
    print(f"Zonas: {zonas}")
    print(f"Puestos: {puestos}")
    
    # Verificar Caquetá
    print("\n" + "=" * 60)
    print("VERIFICACIÓN DEL CAQUETÁ")
    print("=" * 60)
    
    caqueta = Location.query.filter_by(
        tipo='departamento',
        departamento_codigo='44'
    ).first()
    
    if caqueta:
        print(f"✅ Caquetá encontrado:")
        print(f"   Código: {caqueta.departamento_codigo}")
        print(f"   Nombre: {caqueta.departamento_nombre}")
        print(f"   Activo: {caqueta.activo}")
        
        # Contar municipios del Caquetá
        municipios_caqueta = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo='44'
        ).count()
        print(f"   Municipios: {municipios_caqueta}")
        
        # Mostrar algunos municipios
        if municipios_caqueta > 0:
            print("\n   Primeros 5 municipios:")
            munis = Location.query.filter_by(
                tipo='municipio',
                departamento_codigo='44'
            ).limit(5).all()
            for muni in munis:
                print(f"   - {muni.municipio_codigo}: {muni.municipio_nombre}")
    else:
        print("❌ Caquetá NO encontrado en la base de datos")
        print("\nDepartamentos disponibles:")
        deptos = Location.query.filter_by(tipo='departamento').all()
        for dept in deptos:
            print(f"   - {dept.departamento_codigo}: {dept.departamento_nombre}")
