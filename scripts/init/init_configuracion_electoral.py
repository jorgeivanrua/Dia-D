"""
Script para inicializar configuración electoral
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.configuracion_electoral import (
    TipoEleccion, Partido, Coalicion, PartidoCoalicion, Candidato
)


def init_configuracion():
    """Inicializar configuración electoral con datos de ejemplo"""
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("\n>> Recreando tablas de configuración electoral...")
        
        # Eliminar tablas existentes
        try:
            db.session.execute(db.text('DROP TABLE IF EXISTS candidatos'))
            db.session.execute(db.text('DROP TABLE IF EXISTS partidos_coaliciones'))
            db.session.execute(db.text('DROP TABLE IF EXISTS coaliciones'))
            db.session.execute(db.text('DROP TABLE IF EXISTS partidos'))
            db.session.execute(db.text('DROP TABLE IF EXISTS tipos_eleccion'))
            db.session.commit()
            print("✓ Tablas antiguas eliminadas")
        except Exception as e:
            print(f"⚠️  Error eliminando tablas: {e}")
            db.session.rollback()
        
        # Crear tablas nuevas
        db.create_all()
        print("✓ Tablas nuevas creadas")
        
        # Crear tipos de elección
        print("\n>> Creando tipos de elección...")
        tipos = [
            # Elecciones uninominales (un candidato por partido)
            TipoEleccion(codigo='presidencia', nombre='Presidencia de la República', orden=1, es_uninominal=True),
            TipoEleccion(codigo='gobernacion', nombre='Gobernación Departamental', orden=2, es_uninominal=True),
            TipoEleccion(codigo='alcaldia', nombre='Alcaldía Municipal', orden=3, es_uninominal=True),
            
            # Elecciones por listas
            TipoEleccion(codigo='senado', nombre='Senado de la República', orden=4, es_uninominal=False),
            TipoEleccion(codigo='camara', nombre='Cámara de Representantes', orden=5, es_uninominal=False),
            TipoEleccion(codigo='asamblea', nombre='Asamblea Departamental', orden=6, es_uninominal=False),
            TipoEleccion(codigo='concejo', nombre='Concejo Municipal', orden=7, es_uninominal=False),
            TipoEleccion(codigo='jal', nombre='Juntas Administradoras Locales (JAL)', orden=8, es_uninominal=False),
            TipoEleccion(codigo='ediles', nombre='Ediles', orden=9, es_uninominal=False),
            TipoEleccion(codigo='concejos_juventud', nombre='Concejos de Juventud', orden=10, es_uninominal=False),
            TipoEleccion(codigo='consulta', nombre='Consultas Partidistas', orden=11, es_uninominal=False),
        ]
        
        for tipo in tipos:
            db.session.add(tipo)
        
        db.session.commit()
        print(f"✓ {len(tipos)} tipos de elección creados")
        
        # Crear partidos
        print("\n>> Creando partidos políticos...")
        partidos_data = [
            {'codigo': 'LIBERAL', 'nombre': 'Partido Liberal Colombiano', 'nombre_corto': 'Liberal', 'color': '#FF0000', 'orden': 1},
            {'codigo': 'CONSERVADOR', 'nombre': 'Partido Conservador Colombiano', 'nombre_corto': 'Conservador', 'color': '#0000FF', 'orden': 2},
            {'codigo': 'VERDE', 'nombre': 'Partido Alianza Verde', 'nombre_corto': 'Verde', 'color': '#00FF00', 'orden': 3},
            {'codigo': 'CAMBIO_RADICAL', 'nombre': 'Partido Cambio Radical', 'nombre_corto': 'Cambio Radical', 'color': '#FFA500', 'orden': 4},
            {'codigo': 'CENTRO_DEMOCRATICO', 'nombre': 'Centro Democrático', 'nombre_corto': 'Centro Democrático', 'color': '#000080', 'orden': 5},
            {'codigo': 'POLO', 'nombre': 'Polo Democrático Alternativo', 'nombre_corto': 'Polo', 'color': '#FFFF00', 'orden': 6},
            {'codigo': 'MIRA', 'nombre': 'Movimiento Independiente de Renovación Absoluta', 'nombre_corto': 'MIRA', 'color': '#800080', 'orden': 7},
            {'codigo': 'COMUNES', 'nombre': 'Comunes', 'nombre_corto': 'Comunes', 'color': '#FF69B4', 'orden': 8},
            {'codigo': 'PACTO_HISTORICO', 'nombre': 'Pacto Histórico', 'nombre_corto': 'Pacto Histórico', 'color': '#8B0000', 'orden': 9},
            {'codigo': 'COLOMBIA_HUMANA', 'nombre': 'Colombia Humana', 'nombre_corto': 'Colombia Humana', 'color': '#4B0082', 'orden': 10},
        ]
        
        partidos = []
        for data in partidos_data:
            partido = Partido(**data)
            db.session.add(partido)
            partidos.append(partido)
        
        db.session.commit()
        print(f"✓ {len(partidos)} partidos creados")
        
        # Crear candidatos de ejemplo para diferentes tipos de elección
        print("\n>> Creando candidatos de ejemplo...")
        
        tipo_senado = TipoEleccion.query.filter_by(codigo='senado').first()
        tipo_camara = TipoEleccion.query.filter_by(codigo='camara').first()
        tipo_concejo = TipoEleccion.query.filter_by(codigo='concejo').first()
        tipo_asamblea = TipoEleccion.query.filter_by(codigo='asamblea').first()
        
        candidatos_data = []
        
        # Candidatos para CONCEJO MUNICIPAL (más común)
        if tipo_concejo:
            # Partido Liberal - Concejo
            candidatos_data.extend([
                {'codigo': 'CONC-LIB-001', 'nombre_completo': 'Juan Pérez García', 'numero_lista': 1, 'partido_id': partidos[0].id, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 1},
                {'codigo': 'CONC-LIB-002', 'nombre_completo': 'María López Rodríguez', 'numero_lista': 2, 'partido_id': partidos[0].id, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 2},
                {'codigo': 'CONC-LIB-003', 'nombre_completo': 'Carlos Ramírez Soto', 'numero_lista': 3, 'partido_id': partidos[0].id, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 3},
                {'codigo': 'CONC-LIB-004', 'nombre_completo': 'Ana María Gutiérrez', 'numero_lista': 4, 'partido_id': partidos[0].id, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 4},
                {'codigo': 'CONC-LIB-005', 'nombre_completo': 'Luis Fernando Castro', 'numero_lista': 5, 'partido_id': partidos[0].id, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 5},
            ])
            
            # Partido Conservador - Concejo
            candidatos_data.extend([
                {'codigo': 'CONC-CON-001', 'nombre_completo': 'Pedro Martínez Silva', 'numero_lista': 1, 'partido_id': partidos[1].id, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 6},
                {'codigo': 'CONC-CON-002', 'nombre_completo': 'Sandra Gómez Torres', 'numero_lista': 2, 'partido_id': partidos[1].id, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 7},
                {'codigo': 'CONC-CON-003', 'nombre_completo': 'Roberto Díaz Moreno', 'numero_lista': 3, 'partido_id': partidos[1].id, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 8},
                {'codigo': 'CONC-CON-004', 'nombre_completo': 'Patricia Ruiz Vargas', 'numero_lista': 4, 'partido_id': partidos[1].id, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 9},
            ])
            
            # Partido Verde - Concejo
            candidatos_data.extend([
                {'codigo': 'CONC-VER-001', 'nombre_completo': 'Andrés Sánchez Díaz', 'numero_lista': 1, 'partido_id': partidos[2].id, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 10},
                {'codigo': 'CONC-VER-002', 'nombre_completo': 'Laura Fernández Ríos', 'numero_lista': 2, 'partido_id': partidos[2].id, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 11},
                {'codigo': 'CONC-VER-003', 'nombre_completo': 'Miguel Ángel Rojas', 'numero_lista': 3, 'partido_id': partidos[2].id, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 12},
            ])
            
            # Cambio Radical - Concejo
            candidatos_data.extend([
                {'codigo': 'CONC-CR-001', 'nombre_completo': 'Diana Carolina Méndez', 'numero_lista': 1, 'partido_id': partidos[3].id, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 13},
                {'codigo': 'CONC-CR-002', 'nombre_completo': 'Jorge Enrique Parra', 'numero_lista': 2, 'partido_id': partidos[3].id, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 14},
            ])
        
        # Candidatos para CÁMARA DE REPRESENTANTES
        if tipo_camara:
            candidatos_data.extend([
                {'codigo': 'CAM-LIB-001', 'nombre_completo': 'Gloria Inés Ramírez', 'numero_lista': 1, 'partido_id': partidos[0].id, 'tipo_eleccion_id': tipo_camara.id, 'orden': 20},
                {'codigo': 'CAM-LIB-002', 'nombre_completo': 'Hernando José Gómez', 'numero_lista': 2, 'partido_id': partidos[0].id, 'tipo_eleccion_id': tipo_camara.id, 'orden': 21},
                {'codigo': 'CAM-CON-001', 'nombre_completo': 'Marta Lucía Ospina', 'numero_lista': 1, 'partido_id': partidos[1].id, 'tipo_eleccion_id': tipo_camara.id, 'orden': 22},
                {'codigo': 'CAM-VER-001', 'nombre_completo': 'Iván Darío Agudelo', 'numero_lista': 1, 'partido_id': partidos[2].id, 'tipo_eleccion_id': tipo_camara.id, 'orden': 23},
            ])
        
        # Candidatos para ASAMBLEA DEPARTAMENTAL
        if tipo_asamblea:
            candidatos_data.extend([
                {'codigo': 'ASA-LIB-001', 'nombre_completo': 'Fabio Hernán Trujillo', 'numero_lista': 1, 'partido_id': partidos[0].id, 'tipo_eleccion_id': tipo_asamblea.id, 'orden': 30},
                {'codigo': 'ASA-LIB-002', 'nombre_completo': 'Claudia Patricia Muñoz', 'numero_lista': 2, 'partido_id': partidos[0].id, 'tipo_eleccion_id': tipo_asamblea.id, 'orden': 31},
                {'codigo': 'ASA-CON-001', 'nombre_completo': 'Álvaro Uribe Vélez Jr', 'numero_lista': 1, 'partido_id': partidos[1].id, 'tipo_eleccion_id': tipo_asamblea.id, 'orden': 32},
            ])
        
        # Candidatos para ALCALDÍA (uninominal - un candidato por partido)
        tipo_alcaldia = TipoEleccion.query.filter_by(codigo='alcaldia').first()
        if tipo_alcaldia:
            candidatos_data.extend([
                {'codigo': 'ALC-LIB-001', 'nombre_completo': 'José María Rodríguez Pérez', 'numero_lista': None, 'partido_id': partidos[0].id, 'tipo_eleccion_id': tipo_alcaldia.id, 'orden': 40},
                {'codigo': 'ALC-CON-001', 'nombre_completo': 'Martha Elena Gómez Vargas', 'numero_lista': None, 'partido_id': partidos[1].id, 'tipo_eleccion_id': tipo_alcaldia.id, 'orden': 41},
                {'codigo': 'ALC-VER-001', 'nombre_completo': 'Carlos Andrés Sánchez Díaz', 'numero_lista': None, 'partido_id': partidos[2].id, 'tipo_eleccion_id': tipo_alcaldia.id, 'orden': 42},
                {'codigo': 'ALC-CR-001', 'nombre_completo': 'Diana Carolina Méndez Torres', 'numero_lista': None, 'partido_id': partidos[3].id, 'tipo_eleccion_id': tipo_alcaldia.id, 'orden': 43},
                {'codigo': 'ALC-IND-001', 'nombre_completo': 'Roberto Independiente Ciudadano', 'numero_lista': None, 'es_independiente': True, 'tipo_eleccion_id': tipo_alcaldia.id, 'orden': 44},
            ])
        
        # Candidatos para GOBERNACIÓN (uninominal)
        tipo_gobernacion = TipoEleccion.query.filter_by(codigo='gobernacion').first()
        if tipo_gobernacion:
            candidatos_data.extend([
                {'codigo': 'GOB-LIB-001', 'nombre_completo': 'Hernando José Turbay Ayala', 'numero_lista': None, 'partido_id': partidos[0].id, 'tipo_eleccion_id': tipo_gobernacion.id, 'orden': 50},
                {'codigo': 'GOB-CON-001', 'nombre_completo': 'Marta Lucía Ramírez Blanco', 'numero_lista': None, 'partido_id': partidos[1].id, 'tipo_eleccion_id': tipo_gobernacion.id, 'orden': 51},
                {'codigo': 'GOB-VER-001', 'nombre_completo': 'Claudia López Hernández', 'numero_lista': None, 'partido_id': partidos[2].id, 'tipo_eleccion_id': tipo_gobernacion.id, 'orden': 52},
            ])
        
        for data in candidatos_data:
            candidato = Candidato(**data)
            db.session.add(candidato)
        
        db.session.commit()
        print(f"✓ {len(candidatos_data)} candidatos creados")
        
        # Crear coalición de ejemplo
        print("\n>> Creando coalición de ejemplo...")
        coalicion = Coalicion(
            codigo='COALICION_CENTRO',
            nombre='Coalición por el Centro',
            descripcion='Coalición de partidos de centro'
        )
        db.session.add(coalicion)
        db.session.flush()
        
        # Agregar partidos a la coalición
        pc1 = PartidoCoalicion(partido_id=partidos[3].id, coalicion_id=coalicion.id)
        pc2 = PartidoCoalicion(partido_id=partidos[4].id, coalicion_id=coalicion.id)
        db.session.add(pc1)
        db.session.add(pc2)
        
        db.session.commit()
        print("✓ 1 coalición creada")
        
        print("\n" + "="*60)
        print("CONFIGURACIÓN ELECTORAL INICIALIZADA EXITOSAMENTE")
        print("="*60)
        print(f"\n✓ Tipos de Elección: {len(tipos)}")
        print(f"✓ Partidos: {len(partidos)}")
        print(f"✓ Candidatos: {len(candidatos_data)}")
        print(f"✓ Coaliciones: 1")
        print("\n" + "="*60)


if __name__ == '__main__':
    init_configuracion()
