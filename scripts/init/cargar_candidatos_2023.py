"""
Cargar Candidatos de las Elecciones 2023
Candidatos principales para alcaldías y gobernaciones
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from backend.app import create_app
from backend.database import db
from backend.models.configuracion_electoral import Candidato, Partido, TipoEleccion

def cargar_candidatos_2023():
    """Cargar candidatos principales de elecciones 2023"""
    
    print("\n" + "="*70)
    print("CARGANDO CANDIDATOS - ELECCIONES 2023")
    print("="*70)
    
    # Obtener tipos de elección
    tipo_alcaldia = TipoEleccion.query.filter_by(codigo='ALCALDIA').first()
    tipo_gobernacion = TipoEleccion.query.filter_by(codigo='GOBERNACION').first()
    
    if not tipo_alcaldia or not tipo_gobernacion:
        print("❌ Error: Tipos de elección no encontrados")
        return False
    
    # Candidatos ejemplo para diferentes ciudades/departamentos
    candidatos_data = [
        # Bogotá - Alcaldía
        {
            'codigo': 'GALAN_BOG_2023',
            'nombre_completo': 'Carlos Fernando Galán',
            'partido_codigo': 'NUEVO_LIBERALISMO',
            'tipo_eleccion_id': tipo_alcaldia.id,
            'numero_lista': 1,
            'foto_url': None,
            'es_cabeza_lista': True
        },
        {
            'codigo': 'OVIEDO_BOG_2023',
            'nombre_completo': 'Juan Daniel Oviedo',
            'partido_codigo': 'PACTO',
            'tipo_eleccion_id': tipo_alcaldia.id,
            'numero_lista': 2,
            'foto_url': None,
            'es_cabeza_lista': True
        },
        {
            'codigo': 'LARA_BOG_2023',
            'nombre_completo': 'Rodrigo Lara',
            'partido_codigo': 'VERDE',
            'tipo_eleccion_id': tipo_alcaldia.id,
            'numero_lista': 3,
            'foto_url': None,
            'es_cabeza_lista': True
        },
        
        # Cundinamarca - Gobernación
        {
            'codigo': 'REY_CUN_2023',
            'nombre_completo': 'Jorge Emilio Rey',
            'partido_codigo': 'LIBERAL',
            'tipo_eleccion_id': tipo_gobernacion.id,
            'numero_lista': 1,
            'foto_url': None,
            'es_cabeza_lista': True
        },
        {
            'codigo': 'GARCIA_CUN_2023',
            'nombre_completo': 'Nicolás García',
            'partido_codigo': 'CONSERVADOR',
            'tipo_eleccion_id': tipo_gobernacion.id,
            'numero_lista': 2,
            'foto_url': None,
            'es_cabeza_lista': True
        },
        
        # Antioquia - Gobernación
        {
            'codigo': 'RENDON_ANT_2023',
            'nombre_completo': 'Andrés Julián Rendón',
            'partido_codigo': 'CENTRO_DEM',
            'tipo_eleccion_id': tipo_gobernacion.id,
            'numero_lista': 3,
            'foto_url': None,
            'es_cabeza_lista': True
        },
        {
            'codigo': 'UPEGUI_ANT_2023',
            'nombre_completo': 'Juan Carlos Upegui',
            'partido_codigo': 'LIBERAL',
            'tipo_eleccion_id': tipo_gobernacion.id,
            'numero_lista': 4,
            'foto_url': None,
            'es_cabeza_lista': True
        },
        
        # Valle del Cauca - Gobernación
        {
            'codigo': 'TORO_VAL_2023',
            'nombre_completo': 'Dilian Francisca Toro',
            'partido_codigo': 'CONSERVADOR',
            'tipo_eleccion_id': tipo_gobernacion.id,
            'numero_lista': 5,
            'foto_url': None,
            'es_cabeza_lista': True
        },
    ]
    
    candidatos_creados = 0
    candidatos_actualizados = 0
    
    for candidato_data in candidatos_data:
        # Buscar el partido
        partido = Partido.query.filter_by(codigo=candidato_data['partido_codigo']).first()
        
        if not partido:
            print(f"⚠️  Partido {candidato_data['partido_codigo']} no encontrado para {candidato_data['nombre_completo']}")
            continue
        
        # Verificar si el candidato ya existe por código
        candidato = Candidato.query.filter_by(codigo=candidato_data['codigo']).first()
        
        if candidato:
            print(f"📝 Actualizando: {candidato_data['nombre_completo']} ({partido.nombre_corto})")
            candidato.nombre_completo = candidato_data['nombre_completo']
            candidato.partido_id = partido.id
            candidato.tipo_eleccion_id = candidato_data['tipo_eleccion_id']
            candidato.numero_lista = candidato_data['numero_lista']
            candidato.foto_url = candidato_data['foto_url']
            candidato.es_cabeza_lista = candidato_data.get('es_cabeza_lista', False)
            candidato.activo = True
            candidatos_actualizados += 1
        else:
            print(f"✨ Creando: {candidato_data['nombre_completo']} ({partido.nombre_corto})")
            candidato = Candidato(
                codigo=candidato_data['codigo'],
                nombre_completo=candidato_data['nombre_completo'],
                partido_id=partido.id,
                tipo_eleccion_id=candidato_data['tipo_eleccion_id'],
                numero_lista=candidato_data['numero_lista'],
                foto_url=candidato_data['foto_url'],
                es_cabeza_lista=candidato_data.get('es_cabeza_lista', False),
                activo=True
            )
            db.session.add(candidato)
            candidatos_creados += 1
    
    db.session.commit()
    
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    print(f"✅ Candidatos creados: {candidatos_creados}")
    print(f"📝 Candidatos actualizados: {candidatos_actualizados}")
    print(f"📊 Total de candidatos: {Candidato.query.count()}")
    print("="*70 + "\n")
    
    # Mostrar todos los candidatos
    print("Candidatos en la base de datos:")
    for candidato in Candidato.query.order_by(Candidato.numero_lista).all():
        tipo = candidato.tipo_eleccion.nombre if candidato.tipo_eleccion else "N/A"
        partido = candidato.partido.nombre_corto if candidato.partido else "N/A"
        cabeza = "🎯" if candidato.es_cabeza_lista else "  "
        print(f"  {cabeza} #{candidato.numero_lista:2} {candidato.nombre_completo:30} | {partido:20} | {tipo:15} | Activo: {candidato.activo}")
    
    return True

def main():
    """Ejecutar carga de candidatos"""
    app = create_app()
    
    with app.app_context():
        try:
            cargar_candidatos_2023()
            print("\n✅ Candidatos cargados exitosamente\n")
            return 0
        except Exception as e:
            print(f"\n❌ Error cargando candidatos: {str(e)}\n")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return 1

if __name__ == '__main__':
    sys.exit(main())
