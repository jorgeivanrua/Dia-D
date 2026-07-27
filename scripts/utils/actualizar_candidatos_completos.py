"""
Script para actualizar candidatos con listas completas
Senado: Más candidatos por partido
Cámara Caquetá: Máximo 3 por partido
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.configuracion_electoral import Partido, TipoEleccion, Candidato


def actualizar_candidatos():
    """Actualizar candidatos con listas completas"""
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("\n" + "=" * 80)
        print("ACTUALIZANDO CANDIDATOS CON LISTAS COMPLETAS")
        print("=" * 80)
        print()
        
        # Limpiar candidatos existentes
        print("1. Limpiando candidatos existentes...")
        Candidato.query.delete()
        db.session.commit()
        print("✅ Candidatos eliminados")
        print()
        
        # Obtener tipos y partidos
        tipo_senado = TipoEleccion.query.filter_by(codigo='SENADO').first()
        tipo_camara = TipoEleccion.query.filter_by(codigo='CAMARA').first()
        
        partidos = {p.codigo: p for p in Partido.query.all()}
        
        print("2. Creando candidatos por listas...")
        print("-" * 80)
        
        # SENADO - Listas más largas
        candidatos_senado = [
            # PACTO HISTÓRICO (5)
            ('Gustavo Bolívar', 'PACTO', 1),
            ('María José Pizarro', 'PACTO', 2),
            ('Iván Cepeda', 'PACTO', 3),
            ('Alexander López', 'PACTO', 4),
            ('Isabel Zuleta', 'PACTO', 5),
            # CENTRO DEMOCRÁTICO (5)
            ('Paloma Valencia', 'CENTRO_DEM', 1),
            ('Miguel Uribe Turbay', 'CENTRO_DEM', 2),
            ('María Fernanda Cabal', 'CENTRO_DEM', 3),
            ('Paola Holguín', 'CENTRO_DEM', 4),
            ('Honorio Henríquez', 'CENTRO_DEM', 5),
            # ALIANZA VERDE (4)
            ('Angélica Lozano', 'VERDE', 1),
            ('Ariel Ávila', 'VERDE', 2),
            ('Antonio Sanguino', 'VERDE', 3),
            ('Humberto de la Calle', 'VERDE', 4),
            # CONSERVADOR (4)
            ('Efraín Cepeda', 'CONSERVADOR', 1),
            ('David Barguil', 'CONSERVADOR', 2),
            ('Nora García', 'CONSERVADOR', 3),
            ('Ciro Ramírez', 'CONSERVADOR', 4),
            # LIBERAL (5)
            ('Juan Fernando Cristo', 'LIBERAL', 1),
            ('Alejandro Gaviria', 'LIBERAL', 2),
            ('Horacio José Serpa', 'LIBERAL', 3),
            ('Viviane Morales', 'LIBERAL', 4),
            ('Luis Fernando Velasco', 'LIBERAL', 5),
            # CAMBIO RADICAL (4)
            ('Germán Varón', 'CAMBIO_RAD', 1),
            ('Carlos Fernando Motoa', 'CAMBIO_RAD', 2),
            ('Rodrigo Lara', 'CAMBIO_RAD', 3),
            ('David Luna', 'CAMBIO_RAD', 4),
            # POLO (3)
            ('Alexander López Maya', 'POLO', 1),
            ('Aida Avella', 'POLO', 2),
            ('Jorge Enrique Robledo', 'POLO', 3),
            # MIRA (3)
            ('Carlos Alberto Baena', 'MIRA', 1),
            ('John Milton Rodríguez', 'MIRA', 2),
            ('Ana Paola Agudelo', 'MIRA', 3),
            # PARTIDO DE LA U (4)
            ('Roy Barreras', 'U', 1),
            ('Armando Benedetti', 'U', 2),
            ('Juan Mario Laserna', 'U', 3),
            ('Maritza Martínez', 'U', 4),
            # COMUNES (2)
            ('Pablo Catatumbo', 'COMUNES', 1),
            ('Victoria Sandino', 'COMUNES', 2),
        ]
        
        for nombre, partido_cod, numero in candidatos_senado:
            if partido_cod in partidos:
                candidato = Candidato(
                    nombre=nombre,
                    partido_id=partidos[partido_cod].id,
                    tipo_eleccion_id=tipo_senado.id,
                    numero_lista=numero,
                    departamento_codigo=None,
                    activo=True
                )
                db.session.add(candidato)
                print(f"  ✅ Senado: {nombre} ({partidos[partido_cod].sigla}) #{numero}")
        
        print()
        
        # CÁMARA CAQUETÁ - Máximo 3 por partido
        candidatos_camara = [
            # LIBERAL (3)
            ('Hernán Banguero', 'LIBERAL', 1),
            ('Deisy Gómez', 'LIBERAL', 2),
            ('Roberto Sánchez', 'LIBERAL', 3),
            # CONSERVADOR (3)
            ('Carlos Ramírez', 'CONSERVADOR', 1),
            ('Martha Villalba', 'CONSERVADOR', 2),
            ('Jairo Cristancho', 'CONSERVADOR', 3),
            # PACTO HISTÓRICO (3)
            ('Ana María Torres', 'PACTO', 1),
            ('Luis Eduardo Díaz', 'PACTO', 2),
            ('María Fernanda Rojas', 'PACTO', 3),
            # CENTRO DEMOCRÁTICO (3)
            ('Jorge Enrique Rojas', 'CENTRO_DEM', 1),
            ('Claudia Patricia Jiménez', 'CENTRO_DEM', 2),
            ('Héctor Fabio Useche', 'CENTRO_DEM', 3),
            # ALIANZA VERDE (3)
            ('Sandra Milena Gutiérrez', 'VERDE', 1),
            ('Andrés Felipe Arias', 'VERDE', 2),
            ('Diana Carolina Bernal', 'VERDE', 3),
            # CAMBIO RADICAL (3)
            ('Pedro Nel Jiménez', 'CAMBIO_RAD', 1),
            ('Luz Mery Trujillo', 'CAMBIO_RAD', 2),
            ('Oscar Darío Pérez', 'CAMBIO_RAD', 3),
            # PARTIDO DE LA U (3)
            ('Gloria Stella Díaz', 'U', 1),
            ('William Villamizar', 'U', 2),
            ('Yolanda Becerra', 'U', 3),
            # POLO (2)
            ('Jaime Caycedo', 'POLO', 1),
            ('Clara López', 'POLO', 2),
            # MIRA (2)
            ('Alexandra Moreno', 'MIRA', 1),
            ('Édgar Espíndola', 'MIRA', 2),
            # COMUNES (2)
            ('Julián Gallo', 'COMUNES', 1),
            ('Sandra Ramírez', 'COMUNES', 2),
        ]
        
        for nombre, partido_cod, numero in candidatos_camara:
            if partido_cod in partidos:
                candidato = Candidato(
                    nombre=nombre,
                    partido_id=partidos[partido_cod].id,
                    tipo_eleccion_id=tipo_camara.id,
                    numero_lista=numero,
                    departamento_codigo='44',
                    activo=True
                )
                db.session.add(candidato)
                print(f"  ✅ Cámara: {nombre} ({partidos[partido_cod].sigla}) #{numero}")
        
        db.session.commit()
        
        # Resumen
        print()
        print("=" * 80)
        print("RESUMEN")
        print("=" * 80)
        total_senado = Candidato.query.filter_by(tipo_eleccion_id=tipo_senado.id).count()
        total_camara = Candidato.query.filter_by(tipo_eleccion_id=tipo_camara.id).count()
        
        print(f"Candidatos Senado: {total_senado}")
        print(f"Candidatos Cámara (Caquetá): {total_camara}")
        print(f"TOTAL: {total_senado + total_camara}")
        print()
        print("=" * 80)
        print("✅ CANDIDATOS ACTUALIZADOS EXITOSAMENTE")
        print("=" * 80)


if __name__ == '__main__':
    actualizar_candidatos()
