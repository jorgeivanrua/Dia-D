"""
Script para inicializar datos de prueba para el Super Admin
"""
from backend.database import db
from backend.models.configuracion_electoral import TipoEleccion
from backend.models.partido_politico import PartidoPolitico as Partido
from backend.models.candidato import Candidato
from backend.models.user import User
from backend.models.location import Location


def init_tipos_eleccion():
    """Inicializar tipos de elección"""
    print("Inicializando tipos de elección...")
    
    tipos = [
        {
            'codigo': 'PRES',
            'nombre': 'Presidencia',
            'descripcion': 'Elección de Presidente y Vicepresidente',
            'es_uninominal': True,
            'permite_lista_cerrada': False,
            'permite_lista_abierta': False,
            'permite_coaliciones': True,
            'activo': True
        },
        {
            'codigo': 'SENADO',
            'nombre': 'Senado',
            'descripcion': 'Elección de Senadores',
            'es_uninominal': False,
            'permite_lista_cerrada': True,
            'permite_lista_abierta': True,
            'permite_coaliciones': True,
            'activo': True
        },
        {
            'codigo': 'CAMARA',
            'nombre': 'Cámara de Representantes',
            'descripcion': 'Elección de Representantes a la Cámara',
            'es_uninominal': False,
            'permite_lista_cerrada': True,
            'permite_lista_abierta': True,
            'permite_coaliciones': True,
            'activo': True
        },
        {
            'codigo': 'GOB',
            'nombre': 'Gobernación',
            'descripcion': 'Elección de Gobernador',
            'es_uninominal': True,
            'permite_lista_cerrada': False,
            'permite_lista_abierta': False,
            'permite_coaliciones': True,
            'activo': True
        },
        {
            'codigo': 'ASAMBLEA',
            'nombre': 'Asamblea Departamental',
            'descripcion': 'Elección de Diputados a la Asamblea',
            'es_uninominal': False,
            'permite_lista_cerrada': True,
            'permite_lista_abierta': True,
            'permite_coaliciones': True,
            'activo': True
        },
        {
            'codigo': 'ALCALDIA',
            'nombre': 'Alcaldía',
            'descripcion': 'Elección de Alcalde',
            'es_uninominal': True,
            'permite_lista_cerrada': False,
            'permite_lista_abierta': False,
            'permite_coaliciones': True,
            'activo': True
        },
        {
            'codigo': 'CONCEJO',
            'nombre': 'Concejo Municipal',
            'descripcion': 'Elección de Concejales',
            'es_uninominal': False,
            'permite_lista_cerrada': True,
            'permite_lista_abierta': True,
            'permite_coaliciones': True,
            'activo': True
        }
    ]
    
    created = 0
    for tipo_data in tipos:
        existing = TipoEleccion.query.filter_by(codigo=tipo_data['codigo']).first()
        if not existing:
            tipo = TipoEleccion(**tipo_data)
            db.session.add(tipo)
            created += 1
            print(f"  ✓ Creado: {tipo_data['nombre']}")
        else:
            print(f"  - Ya existe: {tipo_data['nombre']}")
    
    db.session.commit()
    print(f"✓ {created} tipos de elección creados\n")


def init_partidos():
    """Inicializar partidos políticos"""
    print("Inicializando partidos políticos...")
    
    partidos = [
        {
            'codigo': 'LIBERAL',
            'nombre': 'Partido Liberal Colombiano',
            'nombre_corto': 'Liberal',
            'color': '#FF0000',
            'activo': True,
            'orden': 1
        },
        {
            'codigo': 'CONSERVADOR',
            'nombre': 'Partido Conservador Colombiano',
            'nombre_corto': 'Conservador',
            'color': '#0000FF',
            'activo': True,
            'orden': 2
        },
        {
            'codigo': 'VERDE',
            'nombre': 'Alianza Verde',
            'nombre_corto': 'Verde',
            'color': '#00FF00',
            'activo': True,
            'orden': 3
        },
        {
            'codigo': 'CENTRO_DEM',
            'nombre': 'Centro Democrático',
            'nombre_corto': 'Centro Democrático',
            'color': '#0080FF',
            'activo': True,
            'orden': 4
        },
        {
            'codigo': 'CAMBIO_RADICAL',
            'nombre': 'Cambio Radical',
            'nombre_corto': 'Cambio Radical',
            'color': '#FFA500',
            'activo': True,
            'orden': 5
        },
        {
            'codigo': 'POLO',
            'nombre': 'Polo Democrático Alternativo',
            'nombre_corto': 'Polo',
            'color': '#FFFF00',
            'activo': True,
            'orden': 6
        },
        {
            'codigo': 'PACTO_HISTORICO',
            'nombre': 'Pacto Histórico',
            'nombre_corto': 'Pacto Histórico',
            'color': '#FF1493',
            'activo': True,
            'orden': 7
        },
        {
            'codigo': 'U',
            'nombre': 'Partido de la U',
            'nombre_corto': 'La U',
            'color': '#808080',
            'activo': True,
            'orden': 8
        },
        {
            'codigo': 'MIRA',
            'nombre': 'Movimiento Independiente de Renovación Absoluta',
            'nombre_corto': 'MIRA',
            'color': '#800080',
            'activo': True,
            'orden': 9
        },
        {
            'codigo': 'COMUNES',
            'nombre': 'Comunes',
            'nombre_corto': 'Comunes',
            'color': '#8B0000',
            'activo': True,
            'orden': 10
        }
    ]
    
    created = 0
    for partido_data in partidos:
        existing = Partido.query.filter_by(codigo=partido_data['codigo']).first()
        if not existing:
            partido = Partido(**partido_data)
            db.session.add(partido)
            created += 1
            print(f"  ✓ Creado: {partido_data['nombre']}")
        else:
            print(f"  - Ya existe: {partido_data['nombre']}")
    
    db.session.commit()
    print(f"✓ {created} partidos creados\n")


def init_candidatos():
    """Inicializar candidatos de prueba"""
    print("Inicializando candidatos de prueba...")
    
    # Obtener tipos de elección y partidos
    tipo_pres = TipoEleccion.query.filter_by(codigo='PRES').first()
    tipo_senado = TipoEleccion.query.filter_by(codigo='SENADO').first()
    tipo_camara = TipoEleccion.query.filter_by(codigo='CAMARA').first()
    
    partido_liberal = Partido.query.filter_by(codigo='LIBERAL').first()
    partido_conservador = Partido.query.filter_by(codigo='CONSERVADOR').first()
    partido_verde = Partido.query.filter_by(codigo='VERDE').first()
    partido_centro_dem = Partido.query.filter_by(codigo='CENTRO_DEM').first()
    
    if not all([tipo_pres, tipo_senado, tipo_camara, partido_liberal, partido_conservador, partido_verde, partido_centro_dem]):
        print("  ⚠ Faltan tipos de elección o partidos. Ejecute primero init_tipos_eleccion() e init_partidos()")
        return
    
    candidatos = [
        # Presidencia
        {
            'codigo': 'PRES_LIB_001',
            'nombre_completo': 'Juan Pérez García',
            'partido_id': partido_liberal.id,
            'tipo_eleccion_id': tipo_pres.id,
            'es_independiente': False,
            'es_cabeza_lista': True,
            'activo': True,
            'orden': 1
        },
        {
            'codigo': 'PRES_CONS_001',
            'nombre_completo': 'María González López',
            'partido_id': partido_conservador.id,
            'tipo_eleccion_id': tipo_pres.id,
            'es_independiente': False,
            'es_cabeza_lista': True,
            'activo': True,
            'orden': 2
        },
        # Senado
        {
            'codigo': 'SEN_VERDE_001',
            'nombre_completo': 'Carlos Rodríguez Martínez',
            'partido_id': partido_verde.id,
            'tipo_eleccion_id': tipo_senado.id,
            'numero_lista': 1,
            'es_independiente': False,
            'es_cabeza_lista': True,
            'activo': True,
            'orden': 1
        },
        {
            'codigo': 'SEN_VERDE_002',
            'nombre_completo': 'Ana Martínez Sánchez',
            'partido_id': partido_verde.id,
            'tipo_eleccion_id': tipo_senado.id,
            'numero_lista': 2,
            'es_independiente': False,
            'es_cabeza_lista': False,
            'activo': True,
            'orden': 2
        },
        # Cámara
        {
            'codigo': 'CAM_CD_001',
            'nombre_completo': 'Pedro Ramírez Torres',
            'partido_id': partido_centro_dem.id,
            'tipo_eleccion_id': tipo_camara.id,
            'numero_lista': 1,
            'es_independiente': False,
            'es_cabeza_lista': True,
            'activo': True,
            'orden': 1
        },
        {
            'codigo': 'CAM_CD_002',
            'nombre_completo': 'Laura Fernández Díaz',
            'partido_id': partido_centro_dem.id,
            'tipo_eleccion_id': tipo_camara.id,
            'numero_lista': 2,
            'es_independiente': False,
            'es_cabeza_lista': False,
            'activo': True,
            'orden': 2
        }
    ]
    
    created = 0
    for candidato_data in candidatos:
        existing = Candidato.query.filter_by(codigo=candidato_data['codigo']).first()
        if not existing:
            candidato = Candidato(**candidato_data)
            db.session.add(candidato)
            created += 1
            print(f"  ✓ Creado: {candidato_data['nombre_completo']}")
        else:
            print(f"  - Ya existe: {candidato_data['nombre_completo']}")
    
    db.session.commit()
    print(f"✓ {created} candidatos creados\n")


def run():
    """Ejecutar inicialización completa"""
    print("=" * 60)
    print("INICIALIZACIÓN DE DATOS PARA SUPER ADMIN")
    print("=" * 60 + "\n")
    
    try:
        init_tipos_eleccion()
        init_partidos()
        init_candidatos()
        
        print("=" * 60)
        print("✓ INICIALIZACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        db.session.rollback()


if __name__ == '__main__':
    import sys
    import os
    # Agregar el directorio raíz al path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    
    from backend.app import create_app
    app = create_app()
    with app.app_context():
        run()
