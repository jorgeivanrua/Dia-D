"""
Script para agregar columnas faltantes directamente a SQLite
"""
import sqlite3
import os

def agregar_columnas():
    """Agregar columnas faltantes a las tablas"""
    db_path = os.path.join('instance', 'electoral.db')
    
    if not os.path.exists(db_path):
        print(f"❌ No se encontró la base de datos en: {db_path}")
        return False
    
    print(f"Conectando a: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Intentar agregar columna 'orden' a partidos_politicos
        try:
            cursor.execute('ALTER TABLE partidos_politicos ADD COLUMN orden INTEGER DEFAULT 0')
            print("✓ Columna 'orden' agregada a 'partidos_politicos'")
        except sqlite3.OperationalError as e:
            if 'duplicate column name' in str(e).lower():
                print("- Columna 'orden' ya existe en 'partidos_politicos'")
            else:
                print(f"✗ Error: {e}")
        
        # Intentar agregar columna 'codigo' a candidatos
        try:
            cursor.execute('ALTER TABLE candidatos ADD COLUMN codigo VARCHAR(50)')
            print("✓ Columna 'codigo' agregada a 'candidatos'")
        except sqlite3.OperationalError as e:
            if 'duplicate column name' in str(e).lower():
                print("- Columna 'codigo' ya existe en 'candidatos'")
            else:
                print(f"✗ Error: {e}")
        
        # Intentar agregar columna 'orden' a candidatos
        try:
            cursor.execute('ALTER TABLE candidatos ADD COLUMN orden INTEGER DEFAULT 0')
            print("✓ Columna 'orden' agregada a 'candidatos'")
        except sqlite3.OperationalError as e:
            if 'duplicate column name' in str(e).lower():
                print("- Columna 'orden' ya existe en 'candidatos'")
            else:
                print(f"✗ Error: {e}")
        
        # Commit de los cambios
        conn.commit()
        print("\n✅ Cambios aplicados exitosamente")
        
        # Verificar las columnas
        print("\n--- Verificando estructura de tablas ---")
        cursor.execute("PRAGMA table_info(partidos_politicos)")
        print("\nColumnas en 'partidos_politicos':")
        for col in cursor.fetchall():
            print(f"  - {col[1]} ({col[2]})")
        
        cursor.execute("PRAGMA table_info(candidatos)")
        print("\nColumnas en 'candidatos':")
        for col in cursor.fetchall():
            print(f"  - {col[1]} ({col[2]})")
        
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error general: {e}")
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    print("=" * 60)
    print("AGREGANDO COLUMNAS FALTANTES A LA BASE DE DATOS")
    print("=" * 60)
    print()
    
    success = agregar_columnas()
    
    if success:
        print("\n" + "=" * 60)
        print("PROCESO COMPLETADO")
        print("=" * 60)
        print("\nPor favor, reinicie el servidor Flask para aplicar los cambios.")
    else:
        print("\n" + "=" * 60)
        print("PROCESO FALLIDO")
        print("=" * 60)
