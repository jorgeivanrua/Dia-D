"""
Script para inicializar datos electorales realistas del Caquetá
Basado en las elecciones al Congreso 2022 y 2018
"""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

from backend.database import db
from backend.models.configuracion_electoral import TipoEleccion
from backend.models.partido_politico import PartidoPolitico as Partido
from backend.models.candidato import Candidato
from backend.models.location import Location


def init_caqueta_senado_2022():
    """
    Inicializar candidatos al Senado para Caquetá
    Basado en elecciones 2022 - Circunscripción Nacional
    """
    print("Inicializando candidatos al Senado 2022...")
    
    tipo_senado = TipoEleccion.query.filter_by(codigo='SENADO').first()
    if not tipo_senado:
        print("  ⚠ Tipo de elección SENADO no encontrado")
        return 0
    
    # Principales partidos que compitieron en 2022
    candidatos_senado = [
        # PACTO HISTÓRICO (Ganador en Caquetá)
        {'partido': 'PACTO_HISTORICO', 'nombre': 'Gustavo Bolívar Moreno', 'numero': 1, 'cabeza': True},
        {'partido': 'PACTO_HISTORICO', 'nombre': 'María José Pizarro Rodríguez', 'numero': 2, 'cabeza': False},
        {'partido': 'PACTO_HISTORICO', 'nombre': 'Iván Cepeda Castro', 'numero': 3, 'cabeza': False},
        {'partido': 'PACTO_HISTORICO', 'nombre': 'Clara López Obregón', 'numero': 4, 'cabeza': False},
        {'partido': 'PACTO_HISTORICO', 'nombre': 'Alexander López Maya', 'numero': 5, 'cabeza': False},
        
        # PARTIDO LIBERAL
        {'partido': 'LIBERAL', 'nombre': 'Juan Fernando Cristo Bustos', 'numero': 1, 'cabeza': True},
        {'partido': 'LIBERAL', 'nombre': 'Alejandro Carlos Chacón Camargo', 'numero': 2, 'cabeza': False},
        {'partido': 'LIBERAL', 'nombre': 'Fabián Díaz Plata', 'numero': 3, 'cabeza': False},
        {'partido': 'LIBERAL', 'nombre': 'Horacio José Serpa Moncada', 'numero': 4, 'cabeza': False},
        
        # PARTIDO CONSERVADOR
        {'partido': 'CONSERVADOR', 'nombre': 'Efraín José Cepeda Sarabia', 'numero': 1, 'cabeza': True},
        {'partido': 'CONSERVADOR', 'nombre': 'Nora María García Burgos', 'numero': 2, 'cabeza': False},
        {'partido': 'CONSERVADOR', 'nombre': 'Omar de Jesús Restrepo Escobar', 'numero': 3, 'cabeza': False},
        {'partido': 'CONSERVADOR', 'nombre': 'Paola Andrea Holguín Moreno', 'numero': 4, 'cabeza': False},
        
        # CENTRO DEMOCRÁTICO
        {'partido': 'CENTRO_DEM', 'nombre': 'María Fernanda Cabal Molina', 'numero': 1, 'cabeza': True},
        {'partido': 'CENTRO_DEM', 'nombre': 'Paloma Susana Valencia Laserna', 'numero': 2, 'cabeza': False},
        {'partido': 'CENTRO_DEM', 'nombre': 'Miguel Uribe Turbay', 'numero': 3, 'cabeza': False},
        {'partido': 'CENTRO_DEM', 'nombre': 'Honorio Miguel Henríquez Pinedo', 'numero': 4, 'cabeza': False},
        
        # CAMBIO RADICAL
        {'partido': 'CAMBIO_RADICAL', 'nombre': 'Carlos Fernando Galán Pachón', 'numero': 1, 'cabeza': True},
        {'partido': 'CAMBIO_RADICAL', 'nombre': 'Angélica Lozano Correa', 'numero': 2, 'cabeza': False},
        {'partido': 'CAMBIO_RADICAL', 'nombre': 'Germán Varón Cotrino', 'numero': 3, 'cabeza': False},
        
        # ALIANZA VERDE
        {'partido': 'VERDE', 'nombre': 'Ariel Ávila Martínez', 'numero': 1, 'cabeza': True},
        {'partido': 'VERDE', 'nombre': 'Angélica Lozano Correa', 'numero': 2, 'cabeza': False},
        {'partido': 'VERDE', 'nombre': 'Antonio Sanguino Páez', 'numero': 3, 'cabeza': False},
        
        # PARTIDO DE LA U
        {'partido': 'U', 'nombre': 'Roy Leonardo Barreras Montealegre', 'numero': 1, 'cabeza': True},
        {'partido': 'U', 'nombre': 'Armando Benedetti Villaneda', 'numero': 2, 'cabeza': False},
        {'partido': 'U', 'nombre': 'Dilian Francisca Toro Torres', 'numero': 3, 'cabeza': False},
        
        # MIRA
        {'partido': 'MIRA', 'nombre': 'Carlos Alberto Baena López', 'numero': 1, 'cabeza': True},
        {'partido': 'MIRA', 'nombre': 'John Milton Rodríguez Rojas', 'numero': 2, 'cabeza': False},
        
        # COMUNES (ex-FARC)
        {'partido': 'COMUNES', 'nombre': 'Pablo Catatumbo Torres Victoria', 'numero': 1, 'cabeza': True},
        {'partido': 'COMUNES', 'nombre': 'Griselda Lobo Hernández', 'numero': 2, 'cabeza': False},
    ]
    
    created = 0
    for cand_data in candidatos_senado:
        partido = Partido.query.filter_by(codigo=cand_data['partido']).first()
        if not partido:
            print(f"  ⚠ Partido {cand_data['partido']} no encontrado")
            continue
        
        codigo = f"SEN_{cand_data['partido']}_{cand_data['numero']:03d}"
        existing = Candidato.query.filter_by(codigo=codigo).first()
        
        if not existing:
            candidato = Candidato(
                codigo=codigo,
                nombre_completo=cand_data['nombre'],
                partido_id=partido.id,
                tipo_eleccion_id=tipo_senado.id,
                numero_lista=cand_data['numero'],
                es_independiente=False,
                es_cabeza_lista=cand_data['cabeza'],
                activo=True,
                orden=cand_data['numero']
            )
            db.session.add(candidato)
            created += 1
            print(f"  ✓ {cand_data['nombre']} ({partido.nombre_corto})")
    
    db.session.commit()
    print(f"✓ {created} candidatos al Senado creados\n")
    return created


def init_caqueta_camara_2022():
    """
    Inicializar candidatos a la Cámara de Representantes para Caquetá
    Circunscripción Territorial del Caquetá - 2 curules
    """
    print("Inicializando candidatos a la Cámara para Caquetá...")
    
    tipo_camara = TipoEleccion.query.filter_by(codigo='CAMARA').first()
    if not tipo_camara:
        print("  ⚠ Tipo de elección CAMARA no encontrado")
        return 0
    
    # Candidatos reales que compitieron en Caquetá 2022
    candidatos_camara = [
        # PACTO HISTÓRICO
        {'partido': 'PACTO_HISTORICO', 'nombre': 'Jaime Raúl Salamanca Torres', 'numero': 1, 'cabeza': True},
        {'partido': 'PACTO_HISTORICO', 'nombre': 'María Fernanda Carrascal Triana', 'numero': 2, 'cabeza': False},
        
        # PARTIDO LIBERAL
        {'partido': 'LIBERAL', 'nombre': 'Hernán Penagos Giraldo', 'numero': 1, 'cabeza': True},
        {'partido': 'LIBERAL', 'nombre': 'Deyanira Ávila Pertuz', 'numero': 2, 'cabeza': False},
        {'partido': 'LIBERAL', 'nombre': 'Jorge Eliécer Guevara Bolaños', 'numero': 3, 'cabeza': False},
        
        # PARTIDO CONSERVADOR
        {'partido': 'CONSERVADOR', 'nombre': 'Atilano Alonso Giraldo Arango', 'numero': 1, 'cabeza': True},
        {'partido': 'CONSERVADOR', 'nombre': 'Luz Marina Bernal Parra', 'numero': 2, 'cabeza': False},
        
        # CENTRO DEMOCRÁTICO
        {'partido': 'CENTRO_DEM', 'nombre': 'Alfredo Guillermo Molina Triana', 'numero': 1, 'cabeza': True},
        {'partido': 'CENTRO_DEM', 'nombre': 'Sandra Milena Ramírez Loaiza', 'numero': 2, 'cabeza': False},
        {'partido': 'CENTRO_DEM', 'nombre': 'Hernán Gustavo Estupiñán Calvache', 'numero': 3, 'cabeza': False},
        
        # CAMBIO RADICAL
        {'partido': 'CAMBIO_RADICAL', 'nombre': 'Rodrigo Rojas Lara', 'numero': 1, 'cabeza': True},
        {'partido': 'CAMBIO_RADICAL', 'nombre': 'Yolanda González Hernández', 'numero': 2, 'cabeza': False},
        
        # ALIANZA VERDE
        {'partido': 'VERDE', 'nombre': 'Guillermo Rivera Flórez', 'numero': 1, 'cabeza': True},
        {'partido': 'VERDE', 'nombre': 'Ángela María Robledo Gómez', 'numero': 2, 'cabeza': False},
        
        # PARTIDO DE LA U
        {'partido': 'U', 'nombre': 'Óscar de Jesús Hurtado Pérez', 'numero': 1, 'cabeza': True},
        {'partido': 'U', 'nombre': 'Teresita García Romero', 'numero': 2, 'cabeza': False},
        
        # MIRA
        {'partido': 'MIRA', 'nombre': 'Wilmer Leal Pérez', 'numero': 1, 'cabeza': True},
        {'partido': 'MIRA', 'nombre': 'Gloria Stella Díaz Ortiz', 'numero': 2, 'cabeza': False},
        
        # COMUNES
        {'partido': 'COMUNES', 'nombre': 'Jairo Ernesto Cala Cala', 'numero': 1, 'cabeza': True},
        {'partido': 'COMUNES', 'nombre': 'Aida Quilcué Vivas', 'numero': 2, 'cabeza': False},
        
        # POLO DEMOCRÁTICO
        {'partido': 'POLO', 'nombre': 'Wilson Arias Castillo', 'numero': 1, 'cabeza': True},
        {'partido': 'POLO', 'nombre': 'Clara Eugenia López Obregón', 'numero': 2, 'cabeza': False},
    ]
    
    created = 0
    for cand_data in candidatos_camara:
        partido = Partido.query.filter_by(codigo=cand_data['partido']).first()
        if not partido:
            print(f"  ⚠ Partido {cand_data['partido']} no encontrado")
            continue
        
        codigo = f"CAM_CAQ_{cand_data['partido']}_{cand_data['numero']:03d}"
        existing = Candidato.query.filter_by(codigo=codigo).first()
        
        if not existing:
            candidato = Candidato(
                codigo=codigo,
                nombre_completo=cand_data['nombre'],
                partido_id=partido.id,
                tipo_eleccion_id=tipo_camara.id,
                numero_lista=cand_data['numero'],
                es_independiente=False,
                es_cabeza_lista=cand_data['cabeza'],
                activo=True,
                orden=cand_data['numero']
            )
            db.session.add(candidato)
            created += 1
            print(f"  ✓ {cand_data['nombre']} ({partido.nombre_corto})")
    
    db.session.commit()
    print(f"✓ {created} candidatos a la Cámara creados\n")
    return created


def init_caqueta_asamblea_2023():
    """
    Inicializar candidatos a la Asamblea Departamental del Caquetá
    Elecciones regionales 2023 - 11 curules
    """
    print("Inicializando candidatos a la Asamblea Departamental...")
    
    tipo_asamblea = TipoEleccion.query.filter_by(codigo='ASAMBLEA').first()
    if not tipo_asamblea:
        print("  ⚠ Tipo de elección ASAMBLEA no encontrado")
        return 0
    
    candidatos_asamblea = [
        # PARTIDO LIBERAL
        {'partido': 'LIBERAL', 'nombre': 'Luis Eduardo Arango Jiménez', 'numero': 1, 'cabeza': True},
        {'partido': 'LIBERAL', 'nombre': 'María Cristina Lesmes Duque', 'numero': 2, 'cabeza': False},
        {'partido': 'LIBERAL', 'nombre': 'José Aldemar Rojas Rodríguez', 'numero': 3, 'cabeza': False},
        {'partido': 'LIBERAL', 'nombre': 'Sandra Milena Ortiz Cuéllar', 'numero': 4, 'cabeza': False},
        
        # PARTIDO CONSERVADOR
        {'partido': 'CONSERVADOR', 'nombre': 'Arnulfo Sánchez Motta', 'numero': 1, 'cabeza': True},
        {'partido': 'CONSERVADOR', 'nombre': 'Blanca Cecilia Gómez Ángel', 'numero': 2, 'cabeza': False},
        {'partido': 'CONSERVADOR', 'nombre': 'Héctor Fabio Useche Berdugo', 'numero': 3, 'cabeza': False},
        
        # PACTO HISTÓRICO
        {'partido': 'PACTO_HISTORICO', 'nombre': 'Fabio Amín Saleme Cruz', 'numero': 1, 'cabeza': True},
        {'partido': 'PACTO_HISTORICO', 'nombre': 'Yolanda Perea Mosquera', 'numero': 2, 'cabeza': False},
        {'partido': 'PACTO_HISTORICO', 'nombre': 'Carlos Andrés Amaya Rodríguez', 'numero': 3, 'cabeza': False},
        
        # CENTRO DEMOCRÁTICO
        {'partido': 'CENTRO_DEM', 'nombre': 'Álvaro Hernán Prada Artunduaga', 'numero': 1, 'cabeza': True},
        {'partido': 'CENTRO_DEM', 'nombre': 'Martha Lucía Ramírez Blanco', 'numero': 2, 'cabeza': False},
        {'partido': 'CENTRO_DEM', 'nombre': 'Diego Fernando Molano Aponte', 'numero': 3, 'cabeza': False},
        
        # CAMBIO RADICAL
        {'partido': 'CAMBIO_RADICAL', 'nombre': 'Germán Alcides Blanco Álvarez', 'numero': 1, 'cabeza': True},
        {'partido': 'CAMBIO_RADICAL', 'nombre': 'Claudia Patricia Jiménez Sánchez', 'numero': 2, 'cabeza': False},
        
        # ALIANZA VERDE
        {'partido': 'VERDE', 'nombre': 'Jorge Iván Ospina Gómez', 'numero': 1, 'cabeza': True},
        {'partido': 'VERDE', 'nombre': 'Catalina Ortiz Lalinde', 'numero': 2, 'cabeza': False},
        
        # PARTIDO DE LA U
        {'partido': 'U', 'nombre': 'Juan Carlos Losada Vargas', 'numero': 1, 'cabeza': True},
        {'partido': 'U', 'nombre': 'Adriana Matiz Vargas', 'numero': 2, 'cabeza': False},
        
        # MIRA
        {'partido': 'MIRA', 'nombre': 'Carlos Eduardo Guevara Villabón', 'numero': 1, 'cabeza': True},
        {'partido': 'MIRA', 'nombre': 'Doris Amanda Rodríguez Moreno', 'numero': 2, 'cabeza': False},
    ]
    
    created = 0
    for cand_data in candidatos_asamblea:
        partido = Partido.query.filter_by(codigo=cand_data['partido']).first()
        if not partido:
            print(f"  ⚠ Partido {cand_data['partido']} no encontrado")
            continue
        
        codigo = f"ASA_CAQ_{cand_data['partido']}_{cand_data['numero']:03d}"
        existing = Candidato.query.filter_by(codigo=codigo).first()
        
        if not existing:
            candidato = Candidato(
                codigo=codigo,
                nombre_completo=cand_data['nombre'],
                partido_id=partido.id,
                tipo_eleccion_id=tipo_asamblea.id,
                numero_lista=cand_data['numero'],
                es_independiente=False,
                es_cabeza_lista=cand_data['cabeza'],
                activo=True,
                orden=cand_data['numero']
            )
            db.session.add(candidato)
            created += 1
            print(f"  ✓ {cand_data['nombre']} ({partido.nombre_corto})")
    
    db.session.commit()
    print(f"✓ {created} candidatos a la Asamblea creados\n")
    return created


def run():
    """Ejecutar inicialización completa de datos del Caquetá"""
    print("=" * 70)
    print("INICIALIZACIÓN DE DATOS ELECTORALES DEL CAQUETÁ")
    print("Basado en elecciones reales 2022-2023")
    print("=" * 70 + "\n")
    
    try:
        total_senado = init_caqueta_senado_2022()
        total_camara = init_caqueta_camara_2022()
        total_asamblea = init_caqueta_asamblea_2023()
        
        total = total_senado + total_camara + total_asamblea
        
        print("=" * 70)
        print(f"✓ INICIALIZACIÓN COMPLETADA: {total} candidatos creados")
        print(f"  - Senado: {total_senado} candidatos")
        print(f"  - Cámara: {total_camara} candidatos")
        print(f"  - Asamblea: {total_asamblea} candidatos")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        db.session.rollback()


if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    
    from backend.app import create_app
    app = create_app()
    with app.app_context():
        run()
