"""
Cargar Partidos Políticos de las Elecciones 2023
Con logos oficiales de Wikipedia/Registraduría
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from backend.app import create_app
from backend.database import db
from backend.models.configuracion_electoral import Partido

def cargar_partidos_2023():
    """Cargar partidos que participaron en elecciones 2023"""
    
    print("\n" + "="*70)
    print("CARGANDO PARTIDOS POLÍTICOS - ELECCIONES 2023")
    print("="*70)
    
    partidos_2023 = [
        {
            'codigo': 'PACTO',
            'nombre': 'Pacto Histórico',
            'nombre_corto': 'Pacto Histórico',
            'color': '#FF0000',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Logo_Pacto_Hist%C3%B3rico.svg/200px-Logo_Pacto_Hist%C3%B3rico.svg.png',
            'orden': 1
        },
        {
            'codigo': 'LIBERAL',
            'nombre': 'Partido Liberal Colombiano',
            'nombre_corto': 'Partido Liberal',
            'color': '#FF0000',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Partido_Liberal_Colombiano_logo.svg/200px-Partido_Liberal_Colombiano_logo.svg.png',
            'orden': 2
        },
        {
            'codigo': 'CONSERVADOR',
            'nombre': 'Partido Conservador Colombiano',
            'nombre_corto': 'Partido Conservador',
            'color': '#0000FF',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Partido_Conservador_Colombiano_logo.svg/200px-Partido_Conservador_Colombiano_logo.svg.png',
            'orden': 3
        },
        {
            'codigo': 'VERDE',
            'nombre': 'Alianza Verde',
            'nombre_corto': 'Alianza Verde',
            'color': '#00FF00',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Alianza_Verde_logo.svg/200px-Alianza_Verde_logo.svg.png',
            'orden': 4
        },
        {
            'codigo': 'CENTRO_DEM',
            'nombre': 'Centro Democrático',
            'nombre_corto': 'Centro Democrático',
            'color': '#0066CC',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Centro_Democr%C3%A1tico_logo.svg/200px-Centro_Democr%C3%A1tico_logo.svg.png',
            'orden': 5
        },
        {
            'codigo': 'CAMBIO_RADICAL',
            'nombre': 'Cambio Radical',
            'nombre_corto': 'Cambio Radical',
            'color': '#FFD700',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Cambio_Radical_logo.svg/200px-Cambio_Radical_logo.svg.png',
            'orden': 6
        },
        {
            'codigo': 'LA_U',
            'nombre': 'Partido de la U',
            'nombre_corto': 'Partido de la U',
            'color': '#FFD700',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Partido_de_la_U_logo.svg/200px-Partido_de_la_U_logo.svg.png',
            'orden': 7
        },
        {
            'codigo': 'MIRA',
            'nombre': 'Movimiento Independiente de Renovación Absoluta',
            'nombre_corto': 'MIRA',
            'color': '#800080',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/MIRA_logo.svg/200px-MIRA_logo.svg.png',
            'orden': 8
        },
        {
            'codigo': 'COMUNES',
            'nombre': 'Comunes',
            'nombre_corto': 'Comunes',
            'color': '#FF6B6B',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Comunes_logo.svg/200px-Comunes_logo.svg.png',
            'orden': 9
        },
        {
            'codigo': 'ASI',
            'nombre': 'Alianza Social Independiente',
            'nombre_corto': 'ASI',
            'color': '#FFA500',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/ASI_logo.svg/200px-ASI_logo.svg.png',
            'orden': 10
        },
        {
            'codigo': 'DIGNIDAD',
            'nombre': 'Colombia Renaciente',
            'nombre_corto': 'Dignidad',
            'color': '#8B4513',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Colombia_Renaciente_logo.svg/200px-Colombia_Renaciente_logo.svg.png',
            'orden': 11
        },
        {
            'codigo': 'NUEVO_LIBERALISMO',
            'nombre': 'Nuevo Liberalismo',
            'nombre_corto': 'Nuevo Liberalismo',
            'color': '#FF0000',
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Nuevo_Liberalismo_logo.svg/200px-Nuevo_Liberalismo_logo.svg.png',
            'orden': 12
        },
        {
            'codigo': 'BLANCO',
            'nombre': 'Voto en Blanco',
            'nombre_corto': 'Blanco',
            'color': '#FFFFFF',
            'logo_url': None,
            'orden': 999
        }
    ]
    
    partidos_creados = 0
    partidos_actualizados = 0
    
    for partido_data in partidos_2023:
        # Verificar si el partido ya existe
        partido = Partido.query.filter_by(codigo=partido_data['codigo']).first()
        
        if partido:
            # Actualizar partido existente
            print(f"📝 Actualizando: {partido_data['nombre']}")
            partido.nombre = partido_data['nombre']
            partido.nombre_corto = partido_data['nombre_corto']
            partido.color = partido_data['color']
            partido.logo_url = partido_data['logo_url']
            partido.orden = partido_data['orden']
            partido.activo = True
            partidos_actualizados += 1
        else:
            # Crear nuevo partido
            print(f"✨ Creando: {partido_data['nombre']}")
            partido = Partido(
                codigo=partido_data['codigo'],
                nombre=partido_data['nombre'],
                nombre_corto=partido_data['nombre_corto'],
                color=partido_data['color'],
                logo_url=partido_data['logo_url'],
                orden=partido_data['orden'],
                activo=True
            )
            db.session.add(partido)
            partidos_creados += 1
    
    db.session.commit()
    
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    print(f"✅ Partidos creados: {partidos_creados}")
    print(f"📝 Partidos actualizados: {partidos_actualizados}")
    print(f"📊 Total de partidos: {Partido.query.count()}")
    print("="*70 + "\n")
    
    # Mostrar todos los partidos
    print("Partidos en la base de datos:")
    for partido in Partido.query.order_by(Partido.orden).all():
        logo_status = "✅" if partido.logo_url else "❌"
        print(f"  {logo_status} {partido.nombre_corto:20} | {partido.nombre:40} | Activo: {partido.activo}")
    
    return True

def main():
    """Ejecutar carga de partidos"""
    app = create_app()
    
    with app.app_context():
        try:
            cargar_partidos_2023()
            print("\n✅ Partidos cargados exitosamente\n")
            return 0
        except Exception as e:
            print(f"\n❌ Error cargando partidos: {str(e)}\n")
            db.session.rollback()
            return 1

if __name__ == '__main__':
    sys.exit(main())
