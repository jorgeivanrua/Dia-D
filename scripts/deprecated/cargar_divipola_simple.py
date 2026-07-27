"""
Script simple para cargar datos DIVIPOLA desde CSV a la base de datos
"""
import csv
import sqlite3
import os

def cargar_divipola():
    print("=" * 80)
    print("CARGANDO DATOS DIVIPOLA EN LA BASE DE DATOS")
    print("=" * 80)
    print()
    
    # Verificar archivo CSV
    csv_file = 'divipola.csv' if os.path.exists('divipola.csv') else 'divipola1.csv'
    if not os.path.exists(csv_file):
        print(f"ERROR: No se encontro el archivo {csv_file}")
        return
    
    # Conectar a la base de datos
    db_path = 'instance/electoral.db'
    print(f"Conectando a: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print("Conexion exitosa")
    print()
    
    # Limpiar tabla locations
    print("Limpiando tabla locations...")
    cursor.execute("DELETE FROM locations")
    conn.commit()
    print("Tabla limpiada")
    print()
    
    # Leer CSV
    print(f"Leyendo archivo {csv_file}...")
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"Total registros: {len(rows)}")
    print()
    
    # Procesar datos
    departamentos = {}
    municipios = {}
    zonas = {}
    puestos = {}
    mesas_creadas = 0
    
    print("Procesando datos...")
    
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
            
            # Codigos completos
            depto_codigo = dd
            muni_codigo = f"{dd}{mm}"
            zona_codigo = f"{dd}{mm}{zz}"
            puesto_codigo = f"{dd}{mm}{zz}{pp}"
            mesa_codigo = f"{dd}{mm}{zz}{pp}{mesa_num}"
            
            # 1. Crear departamento
            if depto_codigo not in departamentos:
                cursor.execute(
                    "SELECT id FROM locations WHERE departamento_codigo = ? AND tipo = 'departamento'",
                    (depto_codigo,)
                )
                result = cursor.fetchone()
                
                if result:
                    departamentos[depto_codigo] = result[0]
                else:
                    cursor.execute("""
                        INSERT INTO locations (
                            departamento_codigo, departamento_nombre,
                            nombre_completo, tipo, activo
                        )
                        VALUES (?, ?, ?, 'departamento', 1)
                    """, (depto_codigo, depto_nombre, depto_nombre))
                    departamentos[depto_codigo] = cursor.lastrowid
                    print(f"  Departamento: {depto_nombre} ({depto_codigo})")
            
            depto_id = departamentos[depto_codigo]
            
            # 2. Crear municipio
            if muni_codigo not in municipios:
                cursor.execute(
                    "SELECT id FROM locations WHERE municipio_codigo = ? AND tipo = 'municipio'",
                    (muni_codigo,)
                )
                result = cursor.fetchone()
                
                if result:
                    municipios[muni_codigo] = result[0]
                else:
                    nombre_completo = f"{depto_nombre} - {muni_nombre}"
                    cursor.execute("""
                        INSERT INTO locations (
                            departamento_codigo, municipio_codigo,
                            departamento_nombre, municipio_nombre,
                            nombre_completo, tipo, parent_id, activo
                        )
                        VALUES (?, ?, ?, ?, ?, 'municipio', ?, 1)
                    """, (depto_codigo, muni_codigo, depto_nombre, muni_nombre, nombre_completo, depto_id))
                    municipios[muni_codigo] = cursor.lastrowid
                    print(f"  Municipio: {muni_nombre} ({muni_codigo})")
            
            muni_id = municipios[muni_codigo]
            
            # 3. Crear zona
            if zona_codigo not in zonas:
                cursor.execute(
                    "SELECT id FROM locations WHERE zona_codigo = ? AND tipo = 'zona'",
                    (zona_codigo,)
                )
                result = cursor.fetchone()
                
                if result:
                    zonas[zona_codigo] = result[0]
                else:
                    zona_nombre = f"Zona {zz}"
                    nombre_completo = f"{depto_nombre} - {muni_nombre} - {zona_nombre}"
                    cursor.execute("""
                        INSERT INTO locations (
                            departamento_codigo, municipio_codigo, zona_codigo,
                            departamento_nombre, municipio_nombre,
                            nombre_completo, tipo, parent_id, activo
                        )
                        VALUES (?, ?, ?, ?, ?, ?, 'zona', ?, 1)
                    """, (depto_codigo, muni_codigo, zona_codigo, depto_nombre, muni_nombre, nombre_completo, muni_id))
                    zonas[zona_codigo] = cursor.lastrowid
            
            zona_id = zonas[zona_codigo]
            
            # 4. Crear puesto
            if puesto_codigo not in puestos:
                cursor.execute(
                    "SELECT id FROM locations WHERE puesto_codigo = ? AND tipo = 'puesto'",
                    (puesto_codigo,)
                )
                result = cursor.fetchone()
                
                if result:
                    puestos[puesto_codigo] = result[0]
                else:
                    comuna = row.get('comuna', '').strip() or None
                    direccion = row.get('direccion', '').strip() or None
                    latitud = row.get('LATITUD', '').strip()
                    longitud = row.get('LONGITUD', '').strip()
                    
                    latitud = float(latitud) if latitud else None
                    longitud = float(longitud) if longitud else None
                    
                    nombre_completo = f"{depto_nombre} - {muni_nombre} - {puesto_nombre}"
                    
                    cursor.execute("""
                        INSERT INTO locations (
                            departamento_codigo, municipio_codigo, zona_codigo, puesto_codigo,
                            departamento_nombre, municipio_nombre, puesto_nombre,
                            nombre_completo, tipo, parent_id,
                            direccion, latitud, longitud, comuna, activo
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'puesto', ?, ?, ?, ?, ?, 1)
                    """, (depto_codigo, muni_codigo, zona_codigo, puesto_codigo,
                          depto_nombre, muni_nombre, puesto_nombre,
                          nombre_completo, zona_id,
                          direccion, latitud, longitud, comuna))
                    puestos[puesto_codigo] = cursor.lastrowid
            
            puesto_id = puestos[puesto_codigo]
            
            # 5. Crear mesa
            cursor.execute(
                "SELECT id FROM locations WHERE mesa_codigo = ? AND tipo = 'mesa'",
                (mesa_codigo,)
            )
            result = cursor.fetchone()
            
            if not result:
                mujeres = int(row.get('mujeres_mesa', 0) or 0)
                hombres = int(row.get('hombres_mesa', 0) or 0)
                total_votantes = int(row.get('total_mesa', 0) or 0)
                
                nombre_completo = f"{depto_nombre} - {muni_nombre} - {mesa_nombre}"
                
                cursor.execute("""
                    INSERT INTO locations (
                        departamento_codigo, municipio_codigo, zona_codigo, puesto_codigo, mesa_codigo,
                        departamento_nombre, municipio_nombre, puesto_nombre, mesa_nombre,
                        nombre_completo, tipo, parent_id,
                        total_votantes_registrados, mujeres, hombres, activo
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'mesa', ?, ?, ?, ?, 1)
                """, (depto_codigo, muni_codigo, zona_codigo, puesto_codigo, mesa_codigo,
                      depto_nombre, muni_nombre, puesto_nombre, mesa_nombre,
                      nombre_completo, puesto_id,
                      total_votantes, mujeres, hombres))
                mesas_creadas += 1
            
            if idx % 1000 == 0:
                print(f"  Procesados {idx}/{len(rows)} registros...")
                conn.commit()
        
        except Exception as e:
            print(f"  ERROR en fila {idx}: {str(e)}")
    
    # Commit final
    print()
    print("Guardando cambios...")
    conn.commit()
    print("Cambios guardados")
    print()
    
    # Resumen
    print("=" * 80)
    print("RESUMEN DE CARGA")
    print("=" * 80)
    print(f"Total registros procesados: {len(rows)}")
    print(f"Departamentos: {len(departamentos)}")
    print(f"Municipios: {len(municipios)}")
    print(f"Zonas: {len(zonas)}")
    print(f"Puestos: {len(puestos)}")
    print(f"Mesas creadas: {mesas_creadas}")
    print("=" * 80)
    
    conn.close()

if __name__ == '__main__':
    cargar_divipola()
