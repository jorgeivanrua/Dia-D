"""
Script para cargar partidos políticos colombianos y candidatos de ejemplo
Basado en las elecciones al Congreso de Colombia
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.configuracion_electoral import Partido, TipoEleccion, Candidato


def cargar_partidos_y_candidatos():
    """Cargar partidos políticos y candidatos de ejemplo"""
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("\n" + "=" * 80)
        print("CARGANDO PARTIDOS POLÍTICOS Y CANDIDATOS")
        print("=" * 80)
        print()
        
        # 1. Crear tipos de elección
        print("1. CREANDO TIPOS DE ELECCIÓN")
        print("-" * 80)
        
        tipos_eleccion = [
            {
                'codigo': 'SENADO',
                'nombre': 'Senado de la República',
                'descripcion': 'Elección para Senadores de la República de Colombia',
                'activo': True
            },
            {
                'codigo': 'CAMARA',
                'nombre': 'Cámara de Representantes',
                'descripcion': 'Elección para Representantes a la Cámara por el Departamento del Caquetá',
                'activo': True
            }
        ]
        
        tipos_creados = []
        for tipo_data in tipos_eleccion:
            tipo = TipoEleccion.query.filter_by(codigo=tipo_data['codigo']).first()
            if not tipo:
                tipo = TipoEleccion(**tipo_data)
                db.session.add(tipo)
                db.session.flush()
                print(f"✅ Creado: {tipo_data['nombre']}")
            else:
                print(f"⚠️  Ya existe: {tipo_data['nombre']}")
            tipos_creados.append(tipo)
        
        db.session.commit()
        print()
        
        # 2. Crear partidos políticos
        print("2. CREANDO PARTIDOS POLÍTICOS")
        print("-" * 80)
        
        partidos = [
            {
                'codigo': 'LIBERAL',
                'nombre': 'Partido Liberal Colombiano',
                'sigla': 'PLC',
                'color': '#FF0000',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Partido_Liberal_Colombiano_logo.svg/200px-Partido_Liberal_Colombiano_logo.svg.png',
                'activo': True
            },
            {
                'codigo': 'CONSERVADOR',
                'nombre': 'Partido Conservador Colombiano',
                'sigla': 'PCC',
                'color': '#0000FF',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Partido_Conservador_Colombiano_logo.svg/200px-Partido_Conservador_Colombiano_logo.svg.png',
                'activo': True
            },
            {
                'codigo': 'PACTO',
                'nombre': 'Pacto Histórico',
                'sigla': 'PH',
                'color': '#FF1493',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Pacto_Hist%C3%B3rico_logo.svg/200px-Pacto_Hist%C3%B3rico_logo.svg.png',
                'activo': True
            },
            {
                'codigo': 'CENTRO_DEM',
                'nombre': 'Centro Democrático',
                'sigla': 'CD',
                'color': '#00BFFF',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Centro_Democr%C3%A1tico_logo.svg/200px-Centro_Democr%C3%A1tico_logo.svg.png',
                'activo': True
            },
            {
                'codigo': 'CAMBIO_RAD',
                'nombre': 'Cambio Radical',
                'sigla': 'CR',
                'color': '#FFD700',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Cambio_Radical_logo.svg/200px-Cambio_Radical_logo.svg.png',
                'activo': True
            },
            {
                'codigo': 'VERDE',
                'nombre': 'Alianza Verde',
                'sigla': 'AV',
                'color': '#00FF00',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Alianza_Verde_logo.svg/200px-Alianza_Verde_logo.svg.png',
                'activo': True
            },
            {
                'codigo': 'POLO',
                'nombre': 'Polo Democrático Alternativo',
                'sigla': 'PDA',
                'color': '#FFD700',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Polo_Democr%C3%A1tico_Alternativo_logo.svg/200px-Polo_Democr%C3%A1tico_Alternativo_logo.svg.png',
                'activo': True
            },
            {
                'codigo': 'MIRA',
                'nombre': 'Movimiento Independiente de Renovación Absoluta',
                'sigla': 'MIRA',
                'color': '#800080',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/MIRA_logo.svg/200px-MIRA_logo.svg.png',
                'activo': True
            },
            {
                'codigo': 'U',
                'nombre': 'Partido de la U',
                'sigla': 'U',
                'color': '#FFA500',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Partido_de_la_U_logo.svg/200px-Partido_de_la_U_logo.svg.png',
                'activo': True
            },
            {
                'codigo': 'COMUNES',
                'nombre': 'Comunes',
                'sigla': 'COMUNES',
                'color': '#DC143C',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Comunes_logo.svg/200px-Comunes_logo.svg.png',
                'activo': True
            },
            {
                'codigo': 'VOTO_BLANCO',
                'nombre': 'Voto en Blanco',
                'sigla': 'BLANCO',
                'color': '#FFFFFF',
                'logo_url': None,
                'activo': True
            }
        ]
        
        partidos_creados = {}
        for partido_data in partidos:
            partido = Partido.query.filter_by(codigo=partido_data['codigo']).first()
            if not partido:
                partido = Partido(**partido_data)
                db.session.add(partido)
                db.session.flush()
                print(f"✅ Creado: {partido_data['nombre']} ({partido_data['sigla']})")
            else:
                print(f"⚠️  Ya existe: {partido_data['nombre']}")
            partidos_creados[partido_data['codigo']] = partido
        
        db.session.commit()
        print()
        
        # 3. Crear candidatos de ejemplo
        print("3. CREANDO CANDIDATOS DE EJEMPLO")
        print("-" * 80)
        
        tipo_senado = tipos_creados[0]
        tipo_camara = tipos_creados[1]
        
        candidatos = [
            # SENADO
            {
                'nombre': 'Gustavo Bolívar',
                'partido_id': partidos_creados['PACTO'].id,
                'tipo_eleccion_id': tipo_senado.id,
                'numero_lista': 1,
                'departamento_codigo': None,  # Senado es nacional
                'activo': True
            },
            {
                'nombre': 'María José Pizarro',
                'partido_id': partidos_creados['PACTO'].id,
                'tipo_eleccion_id': tipo_senado.id,
                'numero_lista': 2,
                'departamento_codigo': None,
                'activo': True
            },
            {
                'nombre': 'Paloma Valencia',
                'partido_id': partidos_creados['CENTRO_DEM'].id,
                'tipo_eleccion_id': tipo_senado.id,
                'numero_lista': 1,
                'departamento_codigo': None,
                'activo': True
            },
            {
                'nombre': 'Miguel Uribe Turbay',
                'partido_id': partidos_creados['CENTRO_DEM'].id,
                'tipo_eleccion_id': tipo_senado.id,
                'numero_lista': 2,
                'departamento_codigo': None,
                'activo': True
            },
            {
                'nombre': 'Angélica Lozano',
                'partido_id': partidos_creados['VERDE'].id,
                'tipo_eleccion_id': tipo_senado.id,
                'numero_lista': 1,
                'departamento_codigo': None,
                'activo': True
            },
            {
                'nombre': 'Ariel Ávila',
                'partido_id': partidos_creados['VERDE'].id,
                'tipo_eleccion_id': tipo_senado.id,
                'numero_lista': 2,
                'departamento_codigo': None,
                'activo': True
            },
            
            # CÁMARA - CAQUETÁ
            {
                'nombre': 'Hernán Banguero',
                'partido_id': partidos_creados['LIBERAL'].id,
                'tipo_eleccion_id': tipo_camara.id,
                'numero_lista': 1,
                'departamento_codigo': '44',
                'activo': True
            },
            {
                'nombre': 'Deisy Gómez',
                'partido_id': partidos_creados['LIBERAL'].id,
                'tipo_eleccion_id': tipo_camara.id,
                'numero_lista': 2,
                'departamento_codigo': '44',
                'activo': True
            },
            {
                'nombre': 'Carlos Ramírez',
                'partido_id': partidos_creados['CONSERVADOR'].id,
                'tipo_eleccion_id': tipo_camara.id,
                'numero_lista': 1,
                'departamento_codigo': '44',
                'activo': True
            },
            {
                'nombre': 'Ana María Torres',
                'partido_id': partidos_creados['PACTO'].id,
                'tipo_eleccion_id': tipo_camara.id,
                'numero_lista': 1,
                'departamento_codigo': '44',
                'activo': True
            },
            {
                'nombre': 'Jorge Enrique Rojas',
                'partido_id': partidos_creados['CENTRO_DEM'].id,
                'tipo_eleccion_id': tipo_camara.id,
                'numero_lista': 1,
                'departamento_codigo': '44',
                'activo': True
            },
            {
                'nombre': 'Sandra Milena Gutiérrez',
                'partido_id': partidos_creados['VERDE'].id,
                'tipo_eleccion_id': tipo_camara.id,
                'numero_lista': 1,
                'departamento_codigo': '44',
                'activo': True
            }
        ]
        
        candidatos_creados = 0
        for candidato_data in candidatos:
            candidato = Candidato.query.filter_by(
                nombre=candidato_data['nombre'],
                partido_id=candidato_data['partido_id'],
                tipo_eleccion_id=candidato_data['tipo_eleccion_id']
            ).first()
            
            if not candidato:
                candidato = Candidato(**candidato_data)
                db.session.add(candidato)
                candidatos_creados += 1
                
                tipo = 'Senado' if candidato_data['tipo_eleccion_id'] == tipo_senado.id else 'Cámara'
                partido = next(p for p in partidos_creados.values() if p.id == candidato_data['partido_id'])
                print(f"✅ {candidato_data['nombre']} - {partido.sigla} ({tipo})")
        
        db.session.commit()
        print()
        
        # Resumen
        print("=" * 80)
        print("RESUMEN")
        print("=" * 80)
        print(f"Tipos de Elección: {len(tipos_creados)}")
        print(f"Partidos Políticos: {len(partidos_creados)}")
        print(f"Candidatos Creados: {candidatos_creados}")
        print()
        
        # Estadísticas por tipo
        senado_count = Candidato.query.filter_by(tipo_eleccion_id=tipo_senado.id).count()
        camara_count = Candidato.query.filter_by(tipo_eleccion_id=tipo_camara.id).count()
        
        print("Candidatos por tipo:")
        print(f"  - Senado: {senado_count}")
        print(f"  - Cámara (Caquetá): {camara_count}")
        print()
        
        print("=" * 80)
        print("✅ PARTIDOS Y CANDIDATOS CARGADOS EXITOSAMENTE")
        print("=" * 80)
        print()
        print("NOTA: Los logos se cargan desde Wikipedia Commons")
        print("Si algún logo no se muestra, puede actualizarse desde el Super Admin")


if __name__ == '__main__':
    cargar_partidos_y_candidatos()
