"""
Script simple para actualizar logos de partidos
Ejecutar desde la raíz del proyecto con: python -m backend.scripts.actualizar_logos_partidos_simple
"""

# URLs de logos de partidos políticos colombianos (Wikipedia Commons)
LOGOS_PARTIDOS = {
    # Partidos principales
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
    
    # Variaciones de nombres
    'LIBERAL': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Colombian_Liberal_Party_logo.svg/200px-Colombian_Liberal_Party_logo.svg.png',
    'CONSERVADOR': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Colombian_Conservative_Party_logo.svg/200px-Colombian_Conservative_Party_logo.svg.png',
    'CD': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Democratic_Center_%28Colombia%29_logo.svg/200px-Democratic_Center_%28Colombia%29_logo.svg.png',
    'CR': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Radical_Change_logo.svg/200px-Radical_Change_logo.svg.png',
    'LA U': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Social_Party_of_National_Unity_logo.svg/200px-Social_Party_of_National_Unity_logo.svg.png',
    'VERDE': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Green_Alliance_%28Colombia%29_logo.svg/200px-Green_Alliance_%28Colombia%29_logo.svg.png',
    'POLO': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Alternative_Democratic_Pole_logo.svg/200px-Alternative_Democratic_Pole_logo.svg.png',
}

def generar_sql():
    """Generar SQL para actualizar logos"""
    print("-- SQL para actualizar logos de partidos")
    print("-- Ejecutar en PostgreSQL\n")
    
    for nombre, url in LOGOS_PARTIDOS.items():
        # Generar UPDATE para nombre exacto
        print(f"UPDATE partidos SET logo_url = '{url}' WHERE UPPER(nombre) = '{nombre}';")
        
        # Generar UPDATE para nombre_corto
        print(f"UPDATE partidos SET logo_url = '{url}' WHERE UPPER(nombre_corto) = '{nombre}';")
        
        # Generar UPDATE para búsqueda parcial
        print(f"UPDATE partidos SET logo_url = '{url}' WHERE UPPER(nombre) LIKE '%{nombre}%' AND logo_url IS NULL;")
        print()

if __name__ == '__main__':
    print("=" * 80)
    print("SCRIPT DE ACTUALIZACIÓN DE LOGOS DE PARTIDOS")
    print("=" * 80)
    print()
    generar_sql()
    print()
    print("=" * 80)
    print("Copia y ejecuta estos comandos SQL en tu base de datos PostgreSQL")
    print("=" * 80)
