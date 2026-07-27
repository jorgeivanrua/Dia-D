"""
Script de prueba para el sistema de carga masiva CSV
"""

import pandas as pd
import os

def create_test_csvs():
    """
    Crear archivos CSV de prueba para cada tipo de carga
    """
    
    # Crear carpeta de pruebas
    test_dir = 'data/test_bulk_upload'
    os.makedirs(test_dir, exist_ok=True)
    
    # 1. Partidos Políticos
    partidos_data = {
        'codigo': ['LIBERAL', 'CONSERVADOR', 'VERDE', 'U', 'POLO'],
        'nombre': [
            'Partido Liberal Colombiano',
            'Partido Conservador Colombiano',
            'Alianza Verde',
            'Partido de la U',
            'Polo Democrático Alternativo'
        ],
        'nombre_corto': ['Partido Liberal', 'Partido Conservador', 'Alianza Verde', 'Partido U', 'Polo'],
        'color': ['#FF0000', '#0000FF', '#00FF00', '#FFFF00', '#FF00FF'],
        'logo_url': ['', '', '', '', ''],
        'activo': [True, True, True, True, True]
    }
    df_partidos = pd.DataFrame(partidos_data)
    df_partidos.to_csv(f'{test_dir}/partidos.csv', index=False, encoding='utf-8')
    print(f'✅ Creado: {test_dir}/partidos.csv ({len(df_partidos)} registros)')
    
    # 2. Candidatos Uninominales (Alcaldía)
    candidatos_uninominal_data = {
        'partido_codigo': ['LIBERAL', 'CONSERVADOR', 'VERDE', 'U', 'POLO'],
        'candidato_nombre': [
            'Juan Pérez García',
            'María López Silva',
            'Carlos Ruiz Mendoza',
            'Ana Martínez Torres',
            'Pedro Gómez Ramírez'
        ],
        'candidato_cedula': ['12345678', '23456789', '34567890', '45678901', '56789012'],
        'es_independiente': [False, False, False, False, False],
        'foto_url': ['', '', '', '', '']
    }
    df_uninominal = pd.DataFrame(candidatos_uninominal_data)
    df_uninominal.to_csv(f'{test_dir}/candidatos_alcaldia.csv', index=False, encoding='utf-8')
    print(f'✅ Creado: {test_dir}/candidatos_alcaldia.csv ({len(df_uninominal)} registros)')
    
    # 3. Candidatos Lista Cerrada (Senado)
    candidatos_senado = []
    partidos = ['LIBERAL', 'CONSERVADOR', 'VERDE', 'U', 'POLO']
    cedula_base = 10000000
    
    for partido in partidos:
        for i in range(1, 6):  # 5 candidatos por partido
            candidatos_senado.append({
                'partido_codigo': partido,
                'numero_lista': i,
                'candidato_nombre': f'Candidato {i} del {partido}',
                'candidato_cedula': str(cedula_base + len(candidatos_senado)),
                'es_cabeza_lista': i == 1,
                'foto_url': ''
            })
    
    df_senado = pd.DataFrame(candidatos_senado)
    df_senado.to_csv(f'{test_dir}/candidatos_senado.csv', index=False, encoding='utf-8')
    print(f'✅ Creado: {test_dir}/candidatos_senado.csv ({len(df_senado)} registros)')
    
    # 4. Candidatos Lista Cerrada (Cámara - Caquetá)
    candidatos_camara = []
    cedula_base = 20000000
    
    for partido in partidos:
        for i in range(1, 4):  # 3 candidatos por partido
            candidatos_camara.append({
                'partido_codigo': partido,
                'numero_lista': i,
                'candidato_nombre': f'Candidato Cámara {i} - {partido}',
                'candidato_cedula': str(cedula_base + len(candidatos_camara)),
                'es_cabeza_lista': i == 1,
                'foto_url': ''
            })
    
    df_camara = pd.DataFrame(candidatos_camara)
    df_camara.to_csv(f'{test_dir}/candidatos_camara_caqueta.csv', index=False, encoding='utf-8')
    print(f'✅ Creado: {test_dir}/candidatos_camara_caqueta.csv ({len(df_camara)} registros)')
    
    # 5. Candidatos Lista Abierta (Concejo)
    candidatos_concejo = []
    cedula_base = 30000000
    
    for partido in partidos:
        for i in range(1, 8):  # 7 candidatos por partido
            candidatos_concejo.append({
                'partido_codigo': partido,
                'numero_lista': i,
                'candidato_nombre': f'Concejal {i} - {partido}',
                'candidato_cedula': str(cedula_base + len(candidatos_concejo)),
                'es_cabeza_lista': i == 1,
                'permite_voto_preferente': True,
                'foto_url': ''
            })
    
    df_concejo = pd.DataFrame(candidatos_concejo)
    df_concejo.to_csv(f'{test_dir}/candidatos_concejo.csv', index=False, encoding='utf-8')
    print(f'✅ Creado: {test_dir}/candidatos_concejo.csv ({len(df_concejo)} registros)')
    
    # 6. Coaliciones
    coaliciones_data = {
        'coalicion_nombre': [
            'Coalición Centro Esperanza',
            'Coalición Centro Esperanza',
            'Coalición Centro Esperanza',
            'Pacto Histórico',
            'Pacto Histórico'
        ],
        'partido_codigo': ['VERDE', 'U', 'LIBERAL', 'POLO', 'LIBERAL'],
        'partido_nombre': [
            'Alianza Verde',
            'Partido de la U',
            'Partido Liberal Colombiano',
            'Polo Democrático Alternativo',
            'Partido Liberal Colombiano'
        ]
    }
    df_coaliciones = pd.DataFrame(coaliciones_data)
    df_coaliciones.to_csv(f'{test_dir}/coaliciones.csv', index=False, encoding='utf-8')
    print(f'✅ Creado: {test_dir}/coaliciones.csv ({len(df_coaliciones)} registros)')
    
    # 7. CSV con errores (para probar validación)
    candidatos_error = [
        {
            'partido_codigo': 'INEXISTENTE',  # Error: partido no existe
            'numero_lista': 1,
            'candidato_nombre': 'Candidato Error 1',
            'candidato_cedula': '99999999',
            'es_cabeza_lista': True,
            'foto_url': ''
        },
        {
            'partido_codigo': 'LIBERAL',
            'numero_lista': 1,  # Error: número duplicado
            'candidato_nombre': 'Candidato Error 2',
            'candidato_cedula': '88888888',
            'es_cabeza_lista': True,  # Error: dos cabezas de lista
            'foto_url': ''
        },
        {
            'partido_codigo': 'LIBERAL',
            'numero_lista': 1,  # Error: número duplicado
            'candidato_nombre': 'Candidato Error 3',
            'candidato_cedula': '88888888',  # Error: cédula duplicada
            'es_cabeza_lista': True,  # Error: dos cabezas de lista
            'foto_url': ''
        }
    ]
    df_error = pd.DataFrame(candidatos_error)
    df_error.to_csv(f'{test_dir}/candidatos_con_errores.csv', index=False, encoding='utf-8')
    print(f'✅ Creado: {test_dir}/candidatos_con_errores.csv ({len(df_error)} registros)')
    
    print(f'\n📁 Todos los archivos CSV de prueba creados en: {test_dir}/')
    print('\n📋 Archivos creados:')
    print('   1. partidos.csv - 5 partidos políticos')
    print('   2. candidatos_alcaldia.csv - 5 candidatos uninominales')
    print('   3. candidatos_senado.csv - 25 candidatos (5 por partido)')
    print('   4. candidatos_camara_caqueta.csv - 15 candidatos (3 por partido)')
    print('   5. candidatos_concejo.csv - 35 candidatos (7 por partido)')
    print('   6. coaliciones.csv - 5 coaliciones')
    print('   7. candidatos_con_errores.csv - 3 registros con errores')
    print('\n🧪 Usa estos archivos para probar el sistema de carga masiva')


def validate_csv_structure():
    """
    Validar que los CSV tienen la estructura correcta
    """
    test_dir = 'data/test_bulk_upload'
    
    print('\n🔍 Validando estructura de archivos CSV...\n')
    
    # Validar partidos
    df = pd.read_csv(f'{test_dir}/partidos.csv')
    required_cols = ['codigo', 'nombre', 'nombre_corto', 'color', 'logo_url', 'activo']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        print(f'❌ partidos.csv - Faltan columnas: {missing}')
    else:
        print(f'✅ partidos.csv - Estructura correcta ({len(df)} registros)')
    
    # Validar candidatos uninominales
    df = pd.read_csv(f'{test_dir}/candidatos_alcaldia.csv')
    required_cols = ['partido_codigo', 'candidato_nombre', 'candidato_cedula', 'es_independiente', 'foto_url']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        print(f'❌ candidatos_alcaldia.csv - Faltan columnas: {missing}')
    else:
        print(f'✅ candidatos_alcaldia.csv - Estructura correcta ({len(df)} registros)')
    
    # Validar candidatos lista cerrada
    df = pd.read_csv(f'{test_dir}/candidatos_senado.csv')
    required_cols = ['partido_codigo', 'numero_lista', 'candidato_nombre', 'candidato_cedula', 'es_cabeza_lista', 'foto_url']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        print(f'❌ candidatos_senado.csv - Faltan columnas: {missing}')
    else:
        print(f'✅ candidatos_senado.csv - Estructura correcta ({len(df)} registros)')
    
    print('\n✅ Validación completada')


if __name__ == '__main__':
    print('🚀 Generando archivos CSV de prueba para carga masiva...\n')
    create_test_csvs()
    validate_csv_structure()
    print('\n✨ Proceso completado exitosamente!')
