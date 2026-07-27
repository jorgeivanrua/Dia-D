"""
Script para asignar ubicación al coordinador municipal
"""
from backend.models.user import User
from backend.models.location import Location
from backend.database import db
from backend.app import create_app

app = create_app()
app.app_context().push()

# Obtener coordinador
coord = User.query.filter_by(nombre='coord_mun', rol='coordinador_municipal').first()

if coord:
    print(f'Coordinador encontrado: {coord.nombre} (ID: {coord.id})')
    print(f'Ubicación actual: {coord.ubicacion_id}')
    
    # Obtener municipio de Florencia
    florencia = Location.query.filter_by(tipo='municipio', municipio_codigo='01').first()
    
    if florencia:
        print(f'\nMunicipio encontrado: {florencia.municipio_nombre} (ID: {florencia.id})')
        
        # Asignar ubicación
        coord.ubicacion_id = florencia.id
        db.session.commit()
        
        print(f'✅ Ubicación asignada correctamente')
        print(f'   Coordinador: {coord.nombre}')
        print(f'   Municipio: {florencia.municipio_nombre}')
        print(f'   Ubicación ID: {coord.ubicacion_id}')
    else:
        print('❌ No se encontró el municipio de Florencia')
else:
    print('❌ No se encontró el coordinador municipal')
