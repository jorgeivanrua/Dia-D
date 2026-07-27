"""
Script para agregar columnas faltantes a las tablas de incidentes y delitos electorales
"""
import sqlite3
import sys

def agregar_columnas_incidentes():
    """Agregar columnas faltantes a incidentes_electorales"""
    try:
        conn = sqlite3.connect('instance/electoral.db')
        cursor = conn.cursor()
        
        print("=" * 60)
        print("AGREGANDO COLUMNAS A incidentes_electorales")
        print("=" * 60)
        
        # Columnas a agregar
        columnas = [
            ('latitud_reporte', 'REAL'),
            ('longitud_reporte', 'REAL'),
            ('precision_gps', 'REAL'),
            ('sincronizado', 'BOOLEAN', 1),  # default True
            ('fecha_sincronizacion', 'DATETIME'),
            ('dispositivo_id', 'VARCHAR(100)')
        ]
        
        for columna_info in columnas:
            columna = columna_info[0]
            tipo = columna_info[1]
            default = columna_info[2] if len(columna_info) > 2 else None
            
            try:
                if default is not None:
                    sql = f"ALTER TABLE incidentes_electorales ADD COLUMN {columna} {tipo} DEFAULT {default}"
                else:
                    sql = f"ALTER TABLE incidentes_electorales ADD COLUMN {columna} {tipo}"
                
                cursor.execute(sql)
                print(f"✓ Columna '{columna}' agregada exitosamente")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e).lower():
                    print(f"⚠ Columna '{columna}' ya existe")
                else:
                    print(f"✗ Error agregando columna '{columna}': {e}")
        
        conn.commit()
        
        # Verificar columnas
        print("\n" + "=" * 60)
        print("VERIFICANDO ESTRUCTURA DE incidentes_electorales")
        print("=" * 60)
        cursor.execute("PRAGMA table_info(incidentes_electorales)")
        columnas_actuales = cursor.fetchall()
        for col in columnas_actuales:
            print(f"  {col[1]} ({col[2]})")
        
        conn.close()
        print("\n✓ Columnas de incidentes agregadas exitosamente")
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def agregar_columnas_delitos():
    """Agregar columnas faltantes a delitos_electorales"""
    try:
        conn = sqlite3.connect('instance/electoral.db')
        cursor = conn.cursor()
        
        print("\n" + "=" * 60)
        print("AGREGANDO COLUMNAS A delitos_electorales")
        print("=" * 60)
        
        # Columnas a agregar
        columnas = [
            ('latitud_reporte', 'REAL'),
            ('longitud_reporte', 'REAL'),
            ('precision_gps', 'REAL'),
            ('sincronizado', 'BOOLEAN', 1),  # default True
            ('fecha_sincronizacion', 'DATETIME'),
            ('dispositivo_id', 'VARCHAR(100)')
        ]
        
        for columna_info in columnas:
            columna = columna_info[0]
            tipo = columna_info[1]
            default = columna_info[2] if len(columna_info) > 2 else None
            
            try:
                if default is not None:
                    sql = f"ALTER TABLE delitos_electorales ADD COLUMN {columna} {tipo} DEFAULT {default}"
                else:
                    sql = f"ALTER TABLE delitos_electorales ADD COLUMN {columna} {tipo}"
                
                cursor.execute(sql)
                print(f"✓ Columna '{columna}' agregada exitosamente")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e).lower():
                    print(f"⚠ Columna '{columna}' ya existe")
                else:
                    print(f"✗ Error agregando columna '{columna}': {e}")
        
        conn.commit()
        
        # Verificar columnas
        print("\n" + "=" * 60)
        print("VERIFICANDO ESTRUCTURA DE delitos_electorales")
        print("=" * 60)
        cursor.execute("PRAGMA table_info(delitos_electorales)")
        columnas_actuales = cursor.fetchall()
        for col in columnas_actuales:
            print(f"  {col[1]} ({col[2]})")
        
        conn.close()
        print("\n✓ Columnas de delitos agregadas exitosamente")
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("Iniciando actualización de base de datos...")
    print("Agregando columnas de geolocalización y sincronización offline\n")
    
    success_incidentes = agregar_columnas_incidentes()
    success_delitos = agregar_columnas_delitos()
    
    if success_incidentes and success_delitos:
        print("\n" + "=" * 60)
        print("✓ ACTUALIZACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("\nColumnas agregadas:")
        print("  - latitud_reporte (REAL)")
        print("  - longitud_reporte (REAL)")
        print("  - precision_gps (REAL)")
        print("  - sincronizado (BOOLEAN)")
        print("  - fecha_sincronizacion (DATETIME)")
        print("  - dispositivo_id (VARCHAR)")
        print("\nPuedes reiniciar el servidor Flask ahora.")
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("✗ ACTUALIZACIÓN FALLÓ")
        print("=" * 60)
        sys.exit(1)
