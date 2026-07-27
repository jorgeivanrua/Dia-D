"""
Script para cargar logos de partidos directamente en la BD
Ejecutar: python cargar_logos_bd.py
"""
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
except ImportError:
    print("❌ Error: SQLAlchemy no está instalado")
    print("   Instalar con: pip install sqlalchemy")
    sys.exit(1)

# URLs de logos de partidos políticos colombianos
LOGOS_PARTIDOS = {
    'PARTIDO LIBERAL': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Colombian_Liberal_Party_logo.svg/200px-Colombian_Liberal_Party_logo.svg.png',
    'PARTIDO CONSERVADOR': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Colombian_Conservative_Party_logo.svg/200px-Colombian_Conservative_Party_logo.svg.png',
    'CENTRO DEMOCRÁTICO': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Democratic_Center_%28Colombia%29_logo.svg/200px-Democratic_Center_%28Colombia%29_logo.svg.png',
    'PACTO HISTÓRICO': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Logo_Pacto_Hist%C3%B3rico.svg/200px-Logo_Pacto_Hist%C3%B3rico.svg.png',
    'CAMBIO RADICAL': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Radical_Change_logo.svg/200px-Radical_Change_logo.svg.png',
    'PARTIDO DE LA U': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Social_Party_of_National_Unity_logo.svg/200px-Social_Party_of_National_Unity_logo.svg.png',
    'ALIANZA VERDE': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Green_Alliance_%28Colombia%29_logo.svg/200px-Green_Alliance_%28Colombia%29_logo.svg.png',
    'POLO DEMOCRÁTICO': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Alternative_Democratic_Pole_logo.svg/200px-Alternative_Democratic_Pole_logo.svg.png',
    'MIRA': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/MIRA_logo.svg/200px-MIRA_logo.svg.png',
    'COMUNES': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Comunes_logo.svg/200px-Comunes_logo.svg.png',
    'LIBERAL': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Colombian_Liberal_Party_logo.svg/200px-Colombian_Liberal_Party_logo.svg.png',
    'CONSERVADOR': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Colombian_Conservative_Party_logo.svg/200px-Colombian_Conservative_Party_logo.svg.png',
    'CD': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Democratic_Center_%28Colombia%29_logo.svg/200px-Democratic_Center_%28Colombia%29_logo.svg.png',
    'CR': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Radical_Change_logo.svg/200px-Radical_Change_logo.svg.png',
    'LA U': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Social_Party_of_National_Unity_logo.svg/200px-Social_Party_of_National_Unity_logo.svg.png',
    'VERDE': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Green_Alliance_%28Colombia%29_logo.svg/200px-Green_Alliance_%28Colombia%29_logo.svg.png',
    'POLO': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Alternative_Democratic_Pole_logo.svg/200px-Alternative_Democratic_Pole_logo.svg.png',
}

def get_database_url():
    """Obtener URL de la base de datos"""
    database_url = os.getenv('DATABASE_URL', 'sqlite:///instance/electoral.db')
    
    # Render usa postgres:// pero SQLAlchemy necesita postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    return database_url

def cargar_logos():
    """Cargar logos en la base de datos"""
    print("=" * 80)
    print("CARGANDO LOGOS DE PARTIDOS EN LA BASE DE DATOS")
    print("=" * 80)
    print()
    
    # Obtener URL de la BD
    database_url = get_database_url()
    print(f"📊 Conectando a la base de datos...")
    print(f"   URL: {database_url[:50]}...")
    print()
    
    try:
        # Crear engine y sesión
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Verificar conexión
        session.execute(text("SELECT 1"))
        print("✅ Conexión exitosa a la base de datos")
        print()
        
        # Consultar partidos existentes
        result = session.execute(text("SELECT id, nombre, nombre_corto, logo_url FROM partidos ORDER BY id"))
        partidos = result.fetchall()
        
        if not partidos:
            print("❌ No hay partidos en la base de datos")
            print("   Primero debes crear los partidos")
            session.close()
            return
        
        print(f"📋 Encontrados {len(partidos)} partidos en la BD:")
        print()
        
        actualizados = 0
        sin_cambios = 0
        sin_logo = 0
        
        for partido in partidos:
            partido_id, nombre, nombre_corto, logo_actual = partido
            
            print(f"  {partido_id}. {nombre} ({nombre_corto or 'Sin sigla'})")
            print(f"     Logo actual: {logo_actual or 'Sin logo'}")
            
            # Buscar logo
            logo_url = None
            nombre_upper = nombre.upper() if nombre else ''
            nombre_corto_upper = nombre_corto.upper() if nombre_corto else ''
            
            # Intentar con nombre exacto
            if nombre_upper in LOGOS_PARTIDOS:
                logo_url = LOGOS_PARTIDOS[nombre_upper]
            
            # Intentar con nombre_corto exacto
            if not logo_url and nombre_corto_upper in LOGOS_PARTIDOS:
                logo_url = LOGOS_PARTIDOS[nombre_corto_upper]
            
            # Intentar búsqueda parcial
            if not logo_url:
                for key, url in LOGOS_PARTIDOS.items():
                    if key in nombre_upper or nombre_upper in key:
                        logo_url = url
                        break
            
            # Actualizar si encontramos logo y es diferente al actual
            if logo_url:
                if logo_url != logo_actual:
                    session.execute(
                        text("UPDATE partidos SET logo_url = :logo WHERE id = :id"),
                        {"logo": logo_url, "id": partido_id}
                    )
                    actualizados += 1
                    print(f"     ✅ Logo actualizado")
                else:
                    sin_cambios += 1
                    print(f"     ℹ️  Logo ya estaba actualizado")
            else:
                sin_logo += 1
                print(f"     ⚠️  No se encontró logo para este partido")
            
            print()
        
        # Commit de cambios
        if actualizados > 0:
            session.commit()
            print("💾 Cambios guardados en la base de datos")
            print()
        
        # Resumen
        print("=" * 80)
        print("RESUMEN DE ACTUALIZACIÓN")
        print("=" * 80)
        print(f"✅ Logos actualizados: {actualizados}")
        print(f"ℹ️  Sin cambios (ya actualizados): {sin_cambios}")
        print(f"⚠️  Sin logo encontrado: {sin_logo}")
        print(f"📊 Total de partidos: {len(partidos)}")
        print("=" * 80)
        
        session.close()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return

if __name__ == '__main__':
    cargar_logos()
