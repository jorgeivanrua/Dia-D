"""
Script para cargar datos DIVIPOLA desde CSV a la base de datos
Ejecutar: python cargar_divipola_v2.py
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
    csv_file = 'divipola.csv' if os.path.exists('divipola.csv') else 'divipola1.csv'
    if not os.path.exists(csv_file):
        print(f"❌ Error: No se encontró el archivo {csv_file}")
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
        
        # Procesar por tipo: departamentos → municipios → zonas → puestos → mesas
        departamentos = {}
        municipios = {}
        zonas = {}
        puestos = {}
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
                mesa_num = row['mesa'].strip().zfill(2)
                
                depto_nombre = row['departamento'].strip()
                muni_nombre = row['municipio'].strip()
                puesto_nombre = row['puesto'].strip()
                mesa_nombre = row['mesa_nombre'].strip()
                
                # Códigos completos
                depto_codigo = dd
                muni_codigo = f"{dd}{mm}"
                zona_codigo = f"{dd}{mm}{zz}"
                puesto_codigo = f"{dd}{mm}{zz}{pp}"
                mesa_codigo = f"{dd}{mm}{zz}{pp}{mesa_num}"
                
                # 1. Crear/obtener departamento
                if depto_codigo not in departamentos:
                    result = session.execute(
                        text("SELECT id FROM locations WHERE departamento_codigo = :codigo AND tipo = 'departamento'"),
                        {"codigo": depto_codigo}
                    ).fetchone()
                    
                    if result:
                        departamentos[depto_codigo] = result[0]
                    else:
                        session.execute(
                            text("""
                                INSERT INTO locations (
                                    departamento_codigo, departamento_nombre,
                                    nombre_completo, tipo, activo
                                )
                                VALUES (:codigo, :nombre, :nombre_completo, 'departamento', 1)
                            """),
                            {
                                "codigo": depto_codigo,
                                "nombre": depto_nombre,
                                "nombre_completo": depto_nombre
                            }
                        )
                        result = session.execute(
                            text("SELECT id FROM locations WHERE departamento_codigo = :codigo AND tipo = 'departamento'"),
                            {"codigo": depto_codigo}
                        ).fetchone()
                        departamentos[depto_codigo] = result[0]
                        print(f"  ✅ Departamento creado: {depto_nombre} ({depto_codigo})")
                
                depto_id = departamentos[depto_codigo]
                
                # 2. Crear/obtener municipio
                if muni_codigo not in municipios:
                    result = session.execute(
                        text("SELECT id FROM locations WHERE municipio_codigo = :codigo AND tipo = 'municipio'"),
                        {"codigo": muni_codigo}
                    ).fetchone()
                    
                    if result:
                        municipios[muni_codigo] = result[0]
                    else:
                        nombre_completo = f"{depto_nombre} - {muni_nombre}"
                        session.execute(
                            text("""
                                INSERT INTO locations (
                                    departamento_codigo, municipio_codigo,
                                    departamento_nombre, municipio_nombre,
                                    nombre_completo, tipo, parent_id, activo
                                )
                                VALUES (:depto_codigo, :muni_codigo, :depto_nombre, :muni_nombre,
                                        :nombre_completo, 'municipio', :parent_id, 1)
                            """),
                            {
                                "depto_codigo": depto_codigo,
                                "muni_codigo": muni_codigo,
                                "depto_nombre": depto_nombre,
                                "muni_nombre": muni_nombre,
                                "nombre_completo": nombre_completo,
                                "parent_id": depto_id
                            }
                        )
                        result = session.execute(
                            text("SELECT id FROM locations WHERE municipio_codigo = :codigo AND tipo = 'municipio'"),
                            {"codigo": muni_codigo}
                        ).fetchone()
                        municipios[muni_codigo] = result[0]
                        print(f"  ✅ Municipio creado: {muni_nombre} ({muni_codigo})")
                
                muni_id = municipios[muni_codigo]
                
                # 3. Crear/obtener zona
                if zona_codigo not in zonas:
                    result = session.execute(
                        text("SELECT id FROM locations WHERE zona_codigo = :codigo AND tipo = 'zona'"),
                        {"codigo": zona_codigo}
                    ).fetchone()
                    
                    if result:
                        zonas[zona_codigo] = result[0]
                    else:
                        zona_nombre = f"Zona {zz}"
                        nombre_completo = f"{depto_nombre} - {muni_nombre} - {zona_nombre}"
                        session.execute(
                            text("""
                                INSERT INTO locations (
                                    departamento_codigo, municipio_codigo, zona_codigo,
                                    departamento_nombre, municipio_nombre,
                                    nombre_completo, tipo, parent_id, activo
                                )
                                VALUES (:depto_codigo, :muni_codigo, :zona_codigo,
                                        :depto_nombre, :muni_nombre,
                                        :nombre_completo, 'zona', :parent_id, 1)
                            """),
                            {
                                "depto_codigo": depto_codigo,
                                "muni_codigo": muni_codigo,
                                "zona_codigo": zona_codigo,
                                "depto_nombre": depto_nombre,
                                "muni_nombre": muni_nombre,
                                "nombre_completo": nombre_completo,
                                "parent_id": muni_id
                            }
                        )
                        result = session.execute(
                            text("SELECT id FROM locations WHERE zona_codigo = :codigo AND tipo = 'zona'"),
                            {"codigo": zona_codigo}
                        ).fetchone()
                        zonas[zona_codigo] = result[0]
                        print(f"  ✅ Zona creada: {zona_nombre} ({zona_codigo})")
                
                zona_id = zonas[zona_codigo]
                
                # 4. Crear/obtener puesto
                if puesto_codigo not in puestos:
                    result = session.execute(
                        text("SELECT id FROM locations WHERE puesto_codigo = :codigo AND tipo = 'puesto'"),
                        {"codigo": puesto_codigo}
                    ).fetchone()
                    
                    if result:
                        puestos[puesto_codigo] = result[0]
                    else:
                        # Extraer datos adicionales
                        comuna = row.get('comuna', '').strip()
                        direccion = row.get('direccion', '').strip()
                        latitud = row.get('LATITUD', '').strip()
                        longitud = row.get('LONGITUD', '').strip()
                        
                        nombre_completo = f"{depto_nombre} - {muni_nombre} - {puesto_nombre}"
                        
                        session.execute(
                            text("""
                                INSERT INTO locations (
                                    departamento_codigo, municipio_codigo, zona_codigo, puesto_codigo,
                                    departamento_nombre, municipio_nombre, puesto_nombre,
                                    nombre_completo, tipo, parent_id,
                                    direccion, latitud, longitud, comuna, activo
                                )
                                VALUES (:depto_codigo, :muni_codigo, :zona_codigo, :puesto_codigo,
                                        :depto_nombre, :muni_nombre, :puesto_nombre,
                                        :nombre_completo, 'puesto', :parent_id,
                                        :direccion, :latitud, :longitud, :comuna, 1)
                            """),
                            {
                                "depto_codigo": depto_codigo,
                                "muni_codigo": muni_codigo,
                                "zona_codigo": zona_codigo,
                                "puesto_codigo": puesto_codigo,
                                "depto_nombre": depto_nombre,
                                "muni_nombre": muni_nombre,
                                "puesto_nombre": puesto_nombre,
                                "nombre_completo": nombre_completo,
                                "parent_id": zona_id,
                                "direccion": direccion or None,
                                "latitud": float(latitud) if latitud else None,
                                "longitud": float(longitud) if longitud else None,
                                "comuna": comuna or None
                            }
                        )
                        result = session.execute(
                            text("SELECT id FROM locations WHERE puesto_codigo = :codigo AND tipo = 'puesto'"),
                            {"codigo": puesto_codigo}
                        ).fetchone()
                        puestos[puesto_codigo] = result[0]
                        print(f"  ✅ Puesto creado: {puesto_nombre} ({puesto_codigo})")
                
                puesto_id = puestos[puesto_codigo]
                
                # 5. Crear mesa
                result_mesa = session.execute(
                    text("SELECT id FROM locations WHERE mesa_codigo = :codigo AND tipo = 'mesa'"),
                    {"codigo": mesa_codigo}
                ).fetchone()
                
                if not result_mesa:
                    mujeres = int(row.get('mujeres_mesa', 0))
                    hombres = int(row.get('hombres_mesa', 0))
                    total_votantes = int(row.get('total_mesa', 0))
                    
                    nombre_completo = f"{depto_nombre} - {muni_nombre} - {mesa_nombre}"
                    
                    session.execute(
                        text("""
                            INSERT INTO locations (
                                departamento_codigo, municipio_codigo, zona_codigo, puesto_codigo, mesa_codigo,
                                departamento_nombre, municipio_nombre, puesto_nombre, mesa_nombre,
                                nombre_completo, tipo, parent_id,
                                total_votantes_registrados, mujeres, hombres, activo
                            )
                            VALUES (:depto_codigo, :muni_codigo, :zona_codigo, :puesto_codigo, :mesa_codigo,
                                    :depto_nombre, :muni_nombre, :puesto_nombre, :mesa_nombre,
                                    :nombre_completo, 'mesa', :parent_id,
                                    :total_votantes, :mujeres, :hombres, 1)
                        """),
                        {
                            "depto_codigo": depto_codigo,
                            "muni_codigo": muni_codigo,
                            "zona_codigo": zona_codigo,
                            "puesto_codigo": puesto_codigo,
                            "mesa_codigo": mesa_codigo,
                            "depto_nombre": depto_nombre,
                            "muni_nombre": muni_nombre,
                            "puesto_nombre": puesto_nombre,
                            "mesa_nombre": mesa_nombre,
                            "nombre_completo": nombre_completo,
                            "parent_id": puesto_id,
                            "total_votantes": total_votantes,
                            "mujeres": mujeres,
                            "hombres": hombres
                        }
                    )
                    mesas_creadas += 1
                
                if idx % 1000 == 0:
                    print(f"  Procesados {idx}/{len(rows)} registros...")
                    session.commit()  # Commit parcial cada 1000 registros
                
            except Exception as e:
                errores.append(f"Fila {idx}: {str(e)}")
                print(f"  ⚠️  Error en fila {idx}: {str(e)}")
        
        # Commit final
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
        print(f"🏢 Puestos: {len(puestos)}")
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
