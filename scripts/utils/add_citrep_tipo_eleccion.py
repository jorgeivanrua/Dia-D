"""
Script para agregar el tipo de elección CITREP
"""
from backend.database import db
from backend.models.configuracion_electoral import TipoEleccion
from backend.app import create_app

app = create_app()

with app.app_context():
    # Verificar si ya existe
    citrep = TipoEleccion.query.filter_by(codigo='CITREP').first()
    
    if citrep:
        print('✅ CITREP ya existe en la base de datos')
        print(f'   ID: {citrep.id}')
        print(f'   Nombre: {citrep.nombre}')
    else:
        # Obtener el orden máximo actual
        max_orden = db.session.query(db.func.max(TipoEleccion.orden)).scalar() or 0
        
        # Crear nuevo tipo de elección CITREP
        citrep = TipoEleccion(
            codigo='CITREP',
            nombre='Circunscripciones Transitorias Especiales de Paz',
            descripcion='Elección de representantes de las Circunscripciones Transitorias Especiales de Paz',
            es_uninominal=False,  # Por listas
            permite_lista_cerrada=True,
            permite_lista_abierta=True,
            permite_coaliciones=True,
            orden=max_orden + 1,
            activo=True
        )
        
        db.session.add(citrep)
        db.session.commit()
        
        print('✅ CITREP agregado exitosamente')
        print(f'   ID: {citrep.id}')
        print(f'   Código: {citrep.codigo}')
        print(f'   Nombre: {citrep.nombre}')
        print(f'   Orden: {citrep.orden}')
