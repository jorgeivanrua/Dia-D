"""
Script para actualizar el campo total_votantes_registrados en mesas existentes
desde el archivo DIVIPOLA CSV
Ejecutar: python scripts/actualizar_votantes_mesas.py
"""
import csv
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
except ImportError:
    print("❌ Error: SQLAlchemy no está instalado")
    print("   Instalar con: pip install sqlalchemy")
    sys.exit(1)

def get_database_url():
    """Obtener URL de la base de datos"""
    database_url = os.getenv('DATABASE_URL', 'sqlite:///instance/electoral.db')
    
    # Render usa postgres:// pero SQLAlchemy necesita postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    return database_url

def actualizar_votantes():
    """Actualizar total_votantes_registrados desde CSV"""
    print("=" * 80)
    print("ACTUALIZANDO VOTANTES REGISTRADOS EN MESAS")
    print("=" * 80)
    print()
    
    # Buscar archivo CSV
    csv_file = None
    for filename in ['data/divipola.csv', 'divipola.csv', 'divipola1.csv']:
        if os.path.exists(filename):
            csv_file = filename
            break
    
    if not csv_file:
        print("❌ Error: No se encontró el archivo DIVIPOLA CSV")
        return
    
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
        
        # Leer CSV
        print(f"📖 Leyendo archivo {csv_file}...")
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        print(f"✅ {len(rows)} registros encontrados en el CSV")
        print()
        
        actualizadas = 0
        no_encontradas = 0
        errores = []
        
        # Primero, agrupar por puesto para contar mesas y calcular división
        puestos_data = {}
        
        print("🔄 Agrupando datos por puesto (solo Caquetá - código 44)...")
        for row in rows:
            dd = row['dd'].strip().zfill(2)
            
            # Filtrar solo Caquetá (código 44)
            if dd != '44':
                continue
            
            mm = row['mm'].strip().zfill(2)
            zz = row['zz'].strip().zfill(2)
            pp = row['pp'].strip().zfill(2)
            
            puesto_codigo = f"{dd}{mm}{zz}{pp}"
            
            if puesto_codigo not in puestos_data:
                puestos_data[puesto_codigo] = {
                    'total_puesto': int(row.get('total_mesa', 0)),
                    'mujeres_puesto': int(row.get('mujeres_mesa', 0)),
                    'hombres_puesto': int(row.get('hombres_mesa', 0)),
                    'mesas': []
                }
            
            mesa_num = row['mesa'].strip().zfill(2)
            mesa_codigo = f"{dd}{mm}{zz}{pp}{mesa_num}"
            puestos_data[puesto_codigo]['mesas'].append(mesa_codigo)
            # Primero, agrupar por puesto para contar mesas y recolectar valores originales
            puestos_data = {}

            print("🔄 Agrupando datos por puesto (solo Caquetá - código 44)...")
            for row in rows:
                dd = row['dd'].strip().zfill(2)

                # Filtrar solo Caquetá (código 44)
                if dd != '44':
                    continue

                mm = row['mm'].strip().zfill(2)
                zz = row['zz'].strip().zfill(2)
                pp = row['pp'].strip().zfill(2)

                puesto_codigo = f"{dd}{mm}{zz}{pp}"

                mesa_num = row['mesa'].strip().zfill(2)
                mesa_codigo = f"{dd}{mm}{zz}{pp}{mesa_num}"

                # Valores originales por fila (por mesa en CSV)
                total_mesa_row = int(row.get('total_mesa', 0) or 0)
                mujeres_mesa_row = int(row.get('mujeres_mesa', 0) or 0)
                hombres_mesa_row = int(row.get('hombres_mesa', 0) or 0)
                puesto_nombre = (row.get('puesto') or row.get('puesto_nombre') or '').strip()

                if puesto_codigo not in puestos_data:
                    puestos_data[puesto_codigo] = {
                        'mesas': [],
                        'puesto_nombre': puesto_nombre
                    }

                puestos_data[puesto_codigo]['mesas'].append({
                    'mesa_codigo': mesa_codigo,
                    'mesa_num': mesa_num,
                    'total_original': total_mesa_row,
                    'mujeres_original': mujeres_mesa_row,
                    'hombres_original': hombres_mesa_row
                })
        
        print(f"✅ {len(puestos_data)} puestos encontrados")
        print()
        print("🔄 Actualizando mesas...")
        print()
        
        for puesto_codigo, data in puestos_data.items():
            num_mesas = len(data['mesas'])
            
            # Calcular votantes por mesa (división)
            total_por_mesa = data['total_puesto'] // num_mesas
            mujeres_por_mesa = data['mujeres_puesto'] // num_mesas
            hombres_por_mesa = data['hombres_puesto'] // num_mesas
            
            # Calcular residuos para distribuir
            residuo_total = data['total_puesto'] % num_mesas
            residuo_mujeres = data['mujeres_puesto'] % num_mesas
            residuo_hombres = data['hombres_puesto'] % num_mesas
            
            for idx, mesa_codigo_completo in enumerate(data['mesas']):
                try:
                    # Extraer códigos individuales del código completo
                    # Formato: DDMMZZPPMM (44 01 01 01 01)
                    dd = mesa_codigo_completo[0:2]
                    mm = mesa_codigo_completo[2:4]
                    zz = mesa_codigo_completo[4:6]
                    pp = mesa_codigo_completo[6:8]
                    mesa_num = mesa_codigo_completo[8:10]
                    
                    # Distribuir residuos en las primeras mesas
                    total_mesa = total_por_mesa + (1 if idx < residuo_total else 0)
                    mujeres_mesa = mujeres_por_mesa + (1 if idx < residuo_mujeres else 0)
                    hombres_mesa = hombres_por_mesa + (1 if idx < residuo_hombres else 0)
                    
                    # Buscar mesa en la BD por códigos individuales
                    result = session.execute(
                        text("""
                            SELECT id FROM locations 
                            WHERE departamento_codigo = :dd
                            AND municipio_codigo = :mm
                            AND zona_codigo = :zz
                            AND puesto_codigo = :pp
                            AND mesa_codigo = :mesa
                            AND tipo = 'mesa'
                        """),
                        {
                            "dd": dd,
                            "mm": mm,
                            "zz": zz,
                            "pp": pp,
                            "mesa": mesa_num
                        }
                    ).fetchone()
                    
                    if result:
                        # Actualizar mesa
                        session.execute(
                            text("""
                                UPDATE locations 
                                SET total_votantes_registrados = :total,
                                    mujeres = :mujeres,
                                    hombres = :hombres
                                WHERE id = :id
                            """),
                            {
                                "id": result[0],
                                "total": total_mesa,
                                "mujeres": mujeres_mesa,
                                "hombres": hombres_mesa
                            }
                        )
                        actualizadas += 1
                        
                        if actualizadas % 100 == 0:
                            print(f"  ✅ {actualizadas} mesas actualizadas...")
                            session.commit()
                    else:
                        no_encontradas += 1
                        if no_encontradas <= 5:  # Mostrar solo las primeras 5
                            print(f"  ⚠️ Mesa no encontrada: {dd}-{mm}-{zz}-{pp}-{mesa_num}")
                    
                except Exception as e:
                    errores.append(f"Mesa {mesa_codigo_completo}: {str(e)}")
                    if len(errores) <= 5:  # Mostrar solo los primeros 5 errores
                        print(f"  ❌ Error en mesa {mesa_codigo_completo}: {str(e)}")
            for puesto_codigo, data in puestos_data.items():
                num_mesas = len(data['mesas'])

                # Detectar si el puesto es cabecera municipal o especial (preservar valores originales)
                puesto_nombre = (data.get('puesto_nombre') or '').upper()
                es_cabecera_o_especial = any(k in puesto_nombre for k in [
                    'CABECERA', 'PUESTO CABECERA', 'ESPECIAL', 'CABECERA MUNICIPAL'
                ])

                # Si no es especial, sumar totales originales y distribuir aplicando regla "mínimo 400 por mesa"
                if not es_cabecera_o_especial:
                    total_puesto = sum(m.get('total_original', 0) for m in data['mesas'])
                    mujeres_puesto = sum(m.get('mujeres_original', 0) for m in data['mesas'])
                    hombres_puesto = sum(m.get('hombres_original', 0) for m in data['mesas'])

                    # Calcular votantes por mesa (división) y aplicar mínimo de 400 por mesa
                    base_por_mesa = total_puesto // num_mesas if num_mesas > 0 else 0
                    total_por_mesa = max(400, base_por_mesa)
                    mujeres_por_mesa = mujeres_puesto // num_mesas if num_mesas > 0 else 0
                    hombres_por_mesa = hombres_puesto // num_mesas if num_mesas > 0 else 0

                    # Calcular residuos para distribuir
                    residuo_total = total_puesto - (total_por_mesa * num_mesas)
                    residuo_mujeres = mujeres_puesto % num_mesas
                    residuo_hombres = hombres_puesto % num_mesas

                    for idx, mesa_info in enumerate(data['mesas']):
                        try:
                            mesa_codigo_completo = mesa_info['mesa_codigo']

                            # Extraer códigos individuales del código completo
                            # Formato: DDMMZZPPMM (44 01 01 01 01)
                            dd = mesa_codigo_completo[0:2]
                            mm = mesa_codigo_completo[2:4]
                            zz = mesa_codigo_completo[4:6]
                            pp = mesa_codigo_completo[6:8]
                            mesa_num = mesa_codigo_completo[8:10]

                            # Distribuir residuos (residuo_total puede ser negativo if base_por_mesa > total_puesto)
                            # Si residuo_total > 0 distribuimos +1 a las primeras mesas
                            total_mesa = total_por_mesa + (1 if residuo_total > 0 and idx < residuo_total else 0)
                            mujeres_mesa = mujeres_por_mesa + (1 if idx < residuo_mujeres else 0)
                            hombres_mesa = hombres_por_mesa + (1 if idx < residuo_hombres else 0)

                            # Buscar mesa en la BD por códigos individuales
                            result = session.execute(
                                text("""
                                    SELECT id FROM locations 
                                    WHERE departamento_codigo = :dd
                                    AND municipio_codigo = :mm
                                    AND zona_codigo = :zz
                                    AND puesto_codigo = :pp
                                    AND mesa_codigo = :mesa
                                    AND tipo = 'mesa'
                                """),
                                {
                                    "dd": dd,
                                    "mm": mm,
                                    "zz": zz,
                                    "pp": pp,
                                    "mesa": mesa_num
                                }
                            ).fetchone()

                            if result:
                                # Actualizar mesa
                                session.execute(
                                    text("""
                                        UPDATE locations 
                                        SET total_votantes_registrados = :total,
                                            mujeres = :mujeres,
                                            hombres = :hombres
                                        WHERE id = :id
                                    """),
                                    {
                                        "id": result[0],
                                        "total": total_mesa,
                                        "mujeres": mujeres_mesa,
                                        "hombres": hombres_mesa
                                    }
                                )
                                actualizadas += 1

                                if actualizadas % 100 == 0:
                                    print(f"  ✅ {actualizadas} mesas actualizadas...")
                            else:
                                no_encontradas += 1
                                if no_encontradas <= 5:  # Mostrar solo las primeras 5
                                    print(f"  ⚠️ Mesa no encontrada: {dd}-{mm}-{zz}-{pp}-{mesa_num}")

                        except Exception as e:
                            errores.append(f"Mesa {mesa_codigo_completo}: {str(e)}")
                            if len(errores) <= 5:  # Mostrar solo los primeros 5 errores
                                print(f"  ❌ Error en mesa {mesa_codigo_completo}: {str(e)}")
                else:
                    # Puesto especial: mantener los valores originales por fila (CSV)
                    for mesa_info in data['mesas']:
                        try:
                            mesa_codigo_completo = mesa_info['mesa_codigo']
                            total_mesa = mesa_info.get('total_original', 0)
                            mujeres_mesa = mesa_info.get('mujeres_original', 0)
                            hombres_mesa = mesa_info.get('hombres_original', 0)

                            dd = mesa_codigo_completo[0:2]
                            mm = mesa_codigo_completo[2:4]
                            zz = mesa_codigo_completo[4:6]
                            pp = mesa_codigo_completo[6:8]
                            mesa_num = mesa_codigo_completo[8:10]

                            result = session.execute(
                                text("""
                                    SELECT id FROM locations 
                                    WHERE departamento_codigo = :dd
                                    AND municipio_codigo = :mm
                                    AND zona_codigo = :zz
                                    AND puesto_codigo = :pp
                                    AND mesa_codigo = :mesa
                                    AND tipo = 'mesa'
                                """),
                                {
                                    "dd": dd,
                                    "mm": mm,
                                    "zz": zz,
                                    "pp": pp,
                                    "mesa": mesa_num
                                }
                            ).fetchone()

                            if result:
                                session.execute(
                                    text("""
                                        UPDATE locations 
                                        SET total_votantes_registrados = :total,
                                            mujeres = :mujeres,
                                            hombres = :hombres
                                        WHERE id = :id
                                    """),
                                    {
                                        "id": result[0],
                                        "total": total_mesa,
                                        "mujeres": mujeres_mesa,
                                        "hombres": hombres_mesa
                                    }
                                )
                                actualizadas += 1
                                if actualizadas % 100 == 0:
                                    print(f"  ✅ {actualizadas} mesas actualizadas...")
                            else:
                                no_encontradas += 1
                                if no_encontradas <= 5:
                                    print(f"  ⚠️ Mesa no encontrada: {dd}-{mm}-{zz}-{pp}-{mesa_num}")

                        except Exception as e:
                            errores.append(f"Mesa {mesa_codigo_completo}: {str(e)}")
                            if len(errores) <= 5:
                                print(f"  ❌ Error en mesa {mesa_codigo_completo}: {str(e)}")
        
        # Commit final
        session.commit()
        
        print()
        print("=" * 80)
        print("RESUMEN")
        print("=" * 80)
        print(f"✅ Mesas actualizadas: {actualizadas}")
        print(f"⚠️ Mesas no encontradas: {no_encontradas}")
        print(f"❌ Errores: {len(errores)}")
        print()
        
        if actualizadas > 0:
            print("✅ Actualización completada exitosamente")
        else:
            print("⚠️ No se actualizó ninguna mesa")
        
        session.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    actualizar_votantes()
