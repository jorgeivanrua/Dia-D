"""
Script para cargar datos DIVIPOLA desde CSV a la base de datos
Ejecutar: python cargar_divipola.py
"""
import csv
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

def get_database_url():
    """Obtener URL de la base de datos"""
    database_url = os.getenv('DATABASE_URL', 'sqlite:///instance/electoral.db')
    
    # Render usa postgres:// pero SQLAlchemy necesita postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    return database_url

def cargar_divipola():
    """Cargar datos DIVIPOLA desde CSV"""
    print("=" * 80)
    print("CARGANDO DATOS DIVIPOLA EN LA BASE DE DATOS")
    print("=" * 80)
    print()
    
    # Verificar que existe el archivo CSV
    if not os.path.exists('divipola1.csv'):
        print("❌ Error: No se encontró el archivo divipola1.csv")
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
        print("📖 Leyendo archivo divipola1.csv...")
        with open('divipola1.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        print(f"✅ {len(rows)} registros encontrados en el CSV")
        print()
        
        # Procesar por tipo: departamentos → municipios → zonas → puestos → mesas
        departamentos = {}
        municipios = {}
        zonas = {}
        puestos_creados = 0
        mesas_creadas = 0
        errores = []
        
        print("🔄 Procesando datos...")
        print()
        
        for idx, row in enumerate(rows, 1):
            try:
                dd = row['dd'].strip().zfill(2)
                mm = row['mm'].strip().zfill(2)
                zz = row['zz'].strip().zfill(2)
                pp = row['pp'].strip().zfill(2)
                
                depto_nombre = row['departamento'].strip()
                muni_nombre = row['municipio'].strip()
                puesto_nombre = row['puesto'].strip()
                
                # 1. Crear/obtener departamento
                depto_codigo = dd
                if depto_codigo not in departamentos:
                    # Verificar si existe
                    result = session.execute(
                        text("SELECT id FROM locations WHERE codigo = :codigo AND tipo = 'departamento'"),
                        {"codigo": depto_codigo}
                    ).fetchone()
                    
                    if result:
                        departamentos[depto_codigo] = result[0]
                    else:
                        # Crear departamento
                        session.execute(
                            text("""
                                INSERT INTO locations (codigo, nombre, tipo, departamento_id, municipio_id, puesto_id)
                                VALUES (:codigo, :nombre, 'departamento', NULL, NULL, NULL)
                                RETURNING id
                            """),
                            {"codigo": depto_codigo, "nombre": depto_nombre}
                        )
                        result = session.execute(
                            text("SELECT id FROM locations WHERE codigo = :codigo AND tipo = 'departamento'"),
                            {"codigo": depto_codigo}
                        ).fetchone()
                        departamentos[depto_codigo] = result[0]
                        print(f"  ✅ Departamento creado: {depto_nombre} ({depto_codigo})")
                
                depto_id = departamentos[depto_codigo]
                
                # 2. Crear/obtener municipio
                muni_codigo = f"{dd}{mm}"
                if muni_codigo not in municipios:
                    result = session.execute(
                        text("SELECT id FROM locations WHERE codigo = :codigo AND tipo = 'municipio'"),
                        {"codigo": muni_codigo}
                    ).fetchone()
                    
                    if result:
                        municipios[muni_codigo] = result[0]
                    else:
                        session.execute(
                            text("""
                                INSERT INTO locations (codigo, nombre, tipo, departamento_id, municipio_id, puesto_id)
                                VALUES (:codigo, :nombre, 'municipio', :depto_id, NULL, NULL)
                                RETURNING id
                            """),
                            {"codigo": muni_codigo, "nombre": muni_nombre, "depto_id": depto_id}
                        )
                        result = session.execute(
                            text("SELECT id FROM locations WHERE codigo = :codigo AND tipo = 'municipio'"),
                            {"codigo": muni_codigo}
                        ).fetchone()
                        municipios[muni_codigo] = result[0]
                        print(f"  ✅ Municipio creado: {muni_nombre} ({muni_codigo})")
                
                muni_id = municipios[muni_codigo]
                
                # 3. Crear/obtener zona
                zona_codigo = f"{dd}{mm}{zz}"
                if zona_codigo not in zonas:
                    result = session.execute(
                        text("SELECT id FROM locations WHERE codigo = :codigo AND tipo = 'zona'"),
                        {"codigo": zona_codigo}
                    ).fetchone()
                    
                    if result:
                        zonas[zona_codigo] = result[0]
                    else:
                        zona_nombre = f"Zona {zz}"
                        session.execute(
                            text("""
                                INSERT INTO locations (codigo, nombre, tipo, departamento_id, municipio_id, puesto_id)
                                VALUES (:codigo, :nombre, 'zona', :depto_id, :muni_id, NULL)
                                RETURNING id
                            """),
                            {"codigo": zona_codigo, "nombre": zona_nombre, "depto_id": depto_id, "muni_id": muni_id}
                        )
                        result = session.execute(
                            text("SELECT id FROM locations WHERE codigo = :codigo AND tipo = 'zona'"),
                            {"codigo": zona_codigo}
                        ).fetchone()
                        zonas[zona_codigo] = result[0]
                        print(f"  ✅ Zona creada: {zona_nombre} ({zona_codigo})")
                
                zona_id = zonas[zona_codigo]
                
                # 4. Crear puesto
                puesto_codigo = f"{dd}{mm}{zz}{pp}"
                
                # Verificar si el puesto ya existe
                result = session.execute(
                    text("SELECT id FROM locations WHERE codigo = :codigo AND tipo = 'puesto'"),
                    {"codigo": puesto_codigo}
                ).fetchone()
                
                if not result:
                    # Extraer datos adicionales
                    comuna = row.get('comuna', '').strip()
                    direccion = row.get('direccion', '').strip()
                    latitud = row.get('LATITUD', '').strip()
                    longitud = row.get('LONGITUD', '').strip()
                    
                    # Crear puesto
                    session.execute(
                        text("""
                            INSERT INTO locations (
                                codigo, nombre, tipo, 
                                departamento_id, municipio_id, puesto_id,
                                direccion, latitud, longitud, comuna
                            )
                            VALUES (
                                :codigo, :nombre, 'puesto',
                                :depto_id, :muni_id, :zona_id,
                                :direccion, :latitud, :longitud, :comuna
                            )
                            RETURNING id
                        """),
                        {
                            "codigo": puesto_codigo,
                            "nombre": puesto_nombre,
                            "depto_id": depto_id,
                            "muni_id": muni_id,
                            "zona_id": zona_id,
                            "direccion": direccion or None,
                            "latitud": float(latitud) if latitud else None,
                            "longitud": float(longitud) if longitud else None,
                            "comuna": comuna or None
                        }
                    )
                    
                    result = session.execute(
                        text("SELECT id FROM locations WHERE codigo = :codigo AND tipo = 'puesto'"),
                        {"codigo": puesto_codigo}
                    ).fetchone()
                    
                    puesto_id = result[0]
                    puestos_creados += 1
                    
                    # 5. Crear mesas
                    # El CSV tiene una fila por mesa, así que solo creamos esta mesa
                    num_mesa = int(row.get('mesa', 1))
                    mujeres = int(row.get('mujeres_mesa', 0))
                    hombres = int(row.get('hombres_mesa', 0))
                    votantes = mujeres + hombres
                    
                    mesa_codigo = f"{puesto_codigo}_{num_mesa:02d}"
                    mesa_nombre = row.get('mesa_nombre', f"{puesto_nombre} - Mesa {num_mesa}").strip()
                    
                    # Verificar si la mesa ya existe
                    result_mesa = session.execute(
                        text("SELECT id FROM locations WHERE codigo = :codigo AND tipo = 'mesa'"),
                        {"codigo": mesa_codigo}
                    ).fetchone()
                    
                    if not result_mesa:
                        session.execute(
                            text("""
                                INSERT INTO locations (
                                    codigo, nombre, tipo,
                                    departamento_id, municipio_id, puesto_id,
                                    votantes_registrados
                                )
                                VALUES (
                                    :codigo, :nombre, 'mesa',
                                    :depto_id, :muni_id, :puesto_id,
                                    :votantes
                                )
                            """),
                            {
                                "codigo": mesa_codigo,
                                "nombre": mesa_nombre,
                                "depto_id": depto_id,
                                "muni_id": muni_id,
                                "puesto_id": puesto_id,
                                "votantes": votantes
                            }
                        )
                        mesas_creadas += 1
                    
                    if idx % 10 == 0:
                        print(f"  Procesados {idx}/{len(rows)} registros...")
                
            except Exception as e:
                errores.append(f"Fila {idx}: {str(e)}")
                print(f"  ⚠️  Error en fila {idx}: {str(e)}")
        
        # Commit de cambios
        print()
        print("💾 Guardando cambios en la base de datos...")
        session.commit()
        print("✅ Cambios guardados exitosamente")
        print()
        
        # Resumen
        print("=" * 80)
        print("RESUMEN DE CARGA")
        print("=" * 80)
        print(f"📊 Total de registros procesados: {len(rows)}")
        print(f"🏛️  Departamentos: {len(departamentos)}")
        print(f"🏙️  Municipios: {len(municipios)}")
        print(f"📍 Zonas: {len(zonas)}")
        print(f"🏢 Puestos creados: {puestos_creados}")
        print(f"📋 Mesas creadas: {mesas_creadas}")
        print(f"⚠️  Errores: {len(errores)}")
        print("=" * 80)
        
        if errores:
            print()
            print("❌ Errores encontrados:")
            for error in errores[:10]:  # Mostrar solo los primeros 10
                print(f"  - {error}")
            if len(errores) > 10:
                print(f"  ... y {len(errores) - 10} errores más")
        
        session.close()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return

if __name__ == '__main__':
    cargar_divipola()
