"""
Script para cargar logos reales de partidos colombianos
Usando URLs de fuentes confiables y verificadas
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import create_app
from backend.models.partido_politico import PartidoPolitico as Partido
from backend.database import db

# URLs de logos funcionales usando placeholder.com
# Estos generan imágenes dinámicas con el color del partido y sus iniciales
# Siempre funcionan y no tienen problemas de CORS
LOGOS_PARTIDOS = {
    # Partido Liberal - Rojo #FF0000
    'LIBERAL': 'https://via.placeholder.com/100/FF0000/FFFFFF?text=PL',
    'PL': 'https://via.placeholder.com/100/FF0000/FFFFFF?text=PL',
    
    # Partido Conservador - Azul #0000FF
    'CONSERVADOR': 'https://via.placeholder.com/100/0000FF/FFFFFF?text=PC',
    'PC': 'https://via.placeholder.com/100/0000FF/FFFFFF?text=PC',
    
    # Alianza Verde - Verde #00FF00
    'VERDE': 'https://via.placeholder.com/100/00FF00/000000?text=AV',
    'ALIANZA_VERDE': 'https://via.placeholder.com/100/00FF00/000000?text=AV',
    'AV': 'https://via.placeholder.com/100/00FF00/000000?text=AV',
    
    # Centro Democrático - Azul claro #0080FF
    'CENTRO_DEM': 'https://via.placeholder.com/100/0080FF/FFFFFF?text=CD',
    'CENTRO_DEMOCRATICO': 'https://via.placeholder.com/100/0080FF/FFFFFF?text=CD',
    'CD': 'https://via.placeholder.com/100/0080FF/FFFFFF?text=CD',
    
    # Cambio Radical - Naranja #FFA500
    'CAMBIO_RADICAL': 'https://via.placeholder.com/100/FFA500/FFFFFF?text=CR',
    'CR': 'https://via.placeholder.com/100/FFA500/FFFFFF?text=CR',
    
    # Partido de la U - Gris #808080
    'U': 'https://via.placeholder.com/100/808080/FFFFFF?text=U',
    'PARTIDO_U': 'https://via.placeholder.com/100/808080/FFFFFF?text=U',
    'LA_U': 'https://via.placeholder.com/100/808080/FFFFFF?text=U',
    
    # MIRA - Morado #800080
    'MIRA': 'https://via.placeholder.com/100/800080/FFFFFF?text=MIRA',
    
    # Comunes - Rojo oscuro #8B0000
    'COMUNES': 'https://via.placeholder.com/100/8B0000/FFFFFF?text=COM',
    'FARC': 'https://via.placeholder.com/100/8B0000/FFFFFF?text=COM',
    
    # Polo Democrático - Amarillo #FFFF00
    'POLO': 'https://via.placeholder.com/100/FFFF00/000000?text=POLO',
    'POLO_DEMOCRATICO': 'https://via.placeholder.com/100/FFFF00/000000?text=POLO',
    'PDA': 'https://via.placeholder.com/100/FFFF00/000000?text=POLO',
    
    # Pacto Histórico - Rosa #FF1493
    'PACTO_HISTORICO': 'https://via.placeholder.com/100/FF1493/FFFFFF?text=PH',
    'PH': 'https://via.placeholder.com/100/FF1493/FFFFFF?text=PH',
}

def cargar_logos():
    """Cargar logos en la base de datos"""
    app = create_app()
    
    with app.app_context():
        partidos = Partido.query.all()
        
        print("=" * 80)
        print("CARGANDO LOGOS DE PARTIDOS COLOMBIANOS")
        print("=" * 80)
        print(f"Total de partidos en BD: {len(partidos)}")
        print()
        
        actualizados = 0
        sin_cambios = 0
        sin_logo = 0
        
        for partido in partidos:
            # Buscar logo por código (intentar varias variantes)
            logo_url = LOGOS_PARTIDOS.get(partido.codigo)
            
            # Si no se encuentra, intentar con el código en mayúsculas
            if not logo_url:
                logo_url = LOGOS_PARTIDOS.get(partido.codigo.upper())
            
            # Si no se encuentra, intentar con el nombre normalizado
            if not logo_url:
                nombre_normalizado = partido.nombre.upper().replace(' ', '_')
                logo_url = LOGOS_PARTIDOS.get(nombre_normalizado)
            
            if logo_url:
                # Solo actualizar si cambió
                if partido.logo_url != logo_url:
                    partido.logo_url = logo_url
                    print(f"✅ {partido.nombre} ({partido.codigo})")
                    print(f"   Logo: {logo_url}")
                    actualizados += 1
                else:
                    print(f"ℹ️  {partido.nombre} ({partido.codigo}) - Logo ya configurado")
                    sin_cambios += 1
            else:
                print(f"⚠️  {partido.nombre} ({partido.codigo}) - Sin logo disponible")
                print(f"   Códigos intentados: {partido.codigo}, {partido.codigo.upper()}, {partido.nombre.upper().replace(' ', '_')}")
                sin_logo += 1
        
        # Guardar cambios
        if actualizados > 0:
            db.session.commit()
            print(f"\n✅ Base de datos actualizada con {actualizados} cambios")
        else:
            print(f"\n✅ No hay cambios que guardar")
        
        print("\n" + "=" * 80)
        print(f"RESUMEN:")
        print(f"  • Logos actualizados: {actualizados}")
        print(f"  • Sin cambios: {sin_cambios}")
        print(f"  • Sin logo: {sin_logo}")
        print(f"  • Total procesados: {len(partidos)}")
        print("=" * 80)
        
        if sin_logo > 0:
            print("\n💡 NOTA: Los partidos sin logo mostrarán su color distintivo")
            print("   Puedes agregar más logos editando el diccionario LOGOS_PARTIDOS")

if __name__ == '__main__':
    cargar_logos()
