"""
Script para descargar y actualizar logos de partidos políticos colombianos
Los logos se descargan de fuentes oficiales y se guardan en la BD
"""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import requests
from backend.app import create_app
from backend.models.configuracion_electoral import Partido
from backend.database import db

# URLs de logos oficiales de partidos colombianos
LOGOS_PARTIDOS = {
    'LIBERAL': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Colombian_Liberal_Party_logo.svg/200px-Colombian_Liberal_Party_logo.svg.png',
        'color': '#FF0000'
    },
    'PL': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Colombian_Liberal_Party_logo.svg/200px-Colombian_Liberal_Party_logo.svg.png',
        'color': '#FF0000'
    },
    'CONSERVADOR': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Colombian_Conservative_Party_logo.svg/200px-Colombian_Conservative_Party_logo.svg.png',
        'color': '#0000FF'
    },
    'PC': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Colombian_Conservative_Party_logo.svg/200px-Colombian_Conservative_Party_logo.svg.png',
        'color': '#0000FF'
    },
    'VERDE': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Alianza_Verde_logo.svg/200px-Alianza_Verde_logo.svg.png',
        'color': '#00C853'
    },
    'ALIANZA_VERDE': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Alianza_Verde_logo.svg/200px-Alianza_Verde_logo.svg.png',
        'color': '#00C853'
    },
    'AV': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Alianza_Verde_logo.svg/200px-Alianza_Verde_logo.svg.png',
        'color': '#00C853'
    },
    'CENTRO_DEM': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Centro_Democr%C3%A1tico_logo.svg/200px-Centro_Democr%C3%A1tico_logo.svg.png',
        'color': '#0080FF'
    },
    'CENTRO_DEMOCRATICO': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Centro_Democr%C3%A1tico_logo.svg/200px-Centro_Democr%C3%A1tico_logo.svg.png',
        'color': '#0080FF'
    },
    'CD': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Centro_Democr%C3%A1tico_logo.svg/200px-Centro_Democr%C3%A1tico_logo.svg.png',
        'color': '#0080FF'
    },
    'CAMBIO_RADICAL': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Cambio_Radical_logo.svg/200px-Cambio_Radical_logo.svg.png',
        'color': '#FFA500'
    },
    'CR': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Cambio_Radical_logo.svg/200px-Cambio_Radical_logo.svg.png',
        'color': '#FFA500'
    },
    'U': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Partido_de_la_U_logo.svg/200px-Partido_de_la_U_logo.svg.png',
        'color': '#808080'
    },
    'PARTIDO_U': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Partido_de_la_U_logo.svg/200px-Partido_de_la_U_logo.svg.png',
        'color': '#808080'
    },
    'LA_U': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Partido_de_la_U_logo.svg/200px-Partido_de_la_U_logo.svg.png',
        'color': '#808080'
    },
    'MIRA': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/MIRA_logo.svg/200px-MIRA_logo.svg.png',
        'color': '#800080'
    },
    'COMUNES': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Comunes_logo.svg/200px-Comunes_logo.svg.png',
        'color': '#8B0000'
    },
    'FARC': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Comunes_logo.svg/200px-Comunes_logo.svg.png',
        'color': '#8B0000'
    },
    'POLO': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Polo_Democr%C3%A1tico_Alternativo_logo.svg/200px-Polo_Democr%C3%A1tico_Alternativo_logo.svg.png',
        'color': '#FFD700'
    },
    'POLO_DEMOCRATICO': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Polo_Democr%C3%A1tico_Alternativo_logo.svg/200px-Polo_Democr%C3%A1tico_Alternativo_logo.svg.png',
        'color': '#FFD700'
    },
    'PDA': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Polo_Democr%C3%A1tico_Alternativo_logo.svg/200px-Polo_Democr%C3%A1tico_Alternativo_logo.svg.png',
        'color': '#FFD700'
    },
    'PACTO_HISTORICO': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Pacto_Hist%C3%B3rico_logo.svg/200px-Pacto_Hist%C3%B3rico_logo.svg.png',
        'color': '#FF1493'
    },
    'PH': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Pacto_Hist%C3%B3rico_logo.svg/200px-Pacto_Hist%C3%B3rico_logo.svg.png',
        'color': '#FF1493'
    }
}

def actualizar_logos():
    """Actualizar logos de partidos en la base de datos"""
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("ACTUALIZACIÓN DE LOGOS DE PARTIDOS")
        print("=" * 80)
        print()
        
        partidos_actualizados = 0
        partidos_sin_logo = 0
        
        # Obtener todos los partidos
        partidos = Partido.query.all()
        print(f"Total de partidos en BD: {len(partidos)}")
        print()
        
        for partido in partidos:
            codigo_upper = partido.codigo.upper()
            
            if codigo_upper in LOGOS_PARTIDOS:
                logo_info = LOGOS_PARTIDOS[codigo_upper]
                
                # Actualizar URL y color
                partido.logo_url = logo_info['url']
                partido.color = logo_info['color']
                
                print(f"✅ {partido.nombre} ({partido.codigo})")
                print(f"   Logo: {logo_info['url'][:60]}...")
                print(f"   Color: {logo_info['color']}")
                
                partidos_actualizados += 1
            else:
                print(f"⚠️  {partido.nombre} ({partido.codigo}) - Sin logo configurado")
                partidos_sin_logo += 1
        
        # Guardar cambios
        db.session.commit()
        
        print()
        print("=" * 80)
        print("RESUMEN")
        print("=" * 80)
        print(f"✅ Partidos actualizados: {partidos_actualizados}")
        print(f"⚠️  Partidos sin logo: {partidos_sin_logo}")
        print()
        print("Los logos se cargarán desde Wikipedia Commons")
        print("Si no hay internet, el sistema usará SVG con colores del partido")
        print("=" * 80)

if __name__ == "__main__":
    try:
        actualizar_logos()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
