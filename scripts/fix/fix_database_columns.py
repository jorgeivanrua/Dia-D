"""
Script para agregar columnas faltantes a la base de datos
"""
import os
import sys
from sqlalchemy import text

# Agregar el directorio backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from database import db
from app import create_app

def agregar_columnas():
    """Agregar columnas faltantes a las tablas"""
    app = create_app()
    
    with app.app_context():
        # Obtener conexión directa
        connection = db.engine.connect()
        trans = connection.begin()
        
        try:
            # Verificar si las columnas ya existen
            print("Verificando columnas existentes...")
            
            # Intentar agregar columna 'orden' a partidos_politicos
            try:
                connection.execute(text('ALTER TABLE partidos_politicos ADD COLUMN orden INTEGER DEFAULT 0'))
                print("✓ Columna 'orden' agregada a 'partidos_politicos'")
            except Exception as e:
                if 'duplicate column name' in str(e).lower() or 'already exists' in str(e).lower():
                    print("- Columna 'orden' ya existe en 'partidos_politicos'")
                else:
                    print(f"✗ Error agregando 'orden' a 'partidos_politicos': {e}")
            
            # Intentar agregar columna 'codigo' a candidatos
            try:
                connection.execute(text('ALTER TABLE candidatos ADD COLUMN codigo VARCHAR(50)'))
                print("✓ Columna 'codigo' agregada a 'candidatos'")
            except Exception as e:
                if 'duplicate column name' in str(e).lower() or 'already exists' in str(e).lower():
                    print("- Columna 'codigo' ya existe en 'candidatos'")
                else:
                    print(f"✗ Error agregando 'codigo' a 'candidatos': {e}")
            
            # Intentar agregar columna 'orden' a candidatos
            try:
                connection.execute(text('ALTER TABLE candidatos ADD COLUMN orden INTEGER DEFAULT 0'))
                print("✓ Columna 'orden' agregada a 'candidatos'")
            except Exception as e:
                if 'duplicate column name' in str(e).lower() or 'already exists' in str(e).lower():
                    print("- Columna 'orden' ya existe en 'candidatos'")
                else:
                    print(f"✗ Error agregando 'orden' a 'candidatos': {e}")
            
            # Commit de los cambios
            trans.commit()
            print("\n✅ Cambios aplicados exitosamente")
            
        except Exception as e:
            trans.rollback()
            print(f"\n❌ Error general: {e}")
            return False
        finally:
            connection.close()
        
        return True

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
        sys.exit(1)
