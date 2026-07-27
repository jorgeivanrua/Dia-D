"""
Migración: Agregar campos de verificación de presencia a la tabla users
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.database import db
from backend.app import create_app


def upgrade():
    """Agregar campos de presencia verificada"""
    
    print("Agregando campos de verificación de presencia a la tabla users...")
    
    # Obtener conexión
    connection = db.engine.raw_connection()
    cursor = connection.cursor()
    
    try:
        # Verificar si las columnas ya existen
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # Agregar presencia_verificada si no existe
        if 'presencia_verificada' not in columns:
            print("  - Agregando columna presencia_verificada...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN presencia_verificada BOOLEAN DEFAULT 0 NOT NULL
            """)
            print("    ✅ Columna presencia_verificada agregada")
        else:
            print("    ℹ️  Columna presencia_verificada ya existe")
        
        # Agregar presencia_verificada_at si no existe
        if 'presencia_verificada_at' not in columns:
            print("  - Agregando columna presencia_verificada_at...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN presencia_verificada_at DATETIME
            """)
            print("    ✅ Columna presencia_verificada_at agregada")
        else:
            print("    ℹ️  Columna presencia_verificada_at ya existe")
        
        connection.commit()
        print("\n✅ Migración completada exitosamente")
        
    except Exception as e:
        connection.rollback()
        print(f"\n❌ Error en la migración: {str(e)}")
        raise
    finally:
        cursor.close()
        connection.close()


def downgrade():
    """Revertir cambios (SQLite no soporta DROP COLUMN fácilmente)"""
    print("⚠️  SQLite no soporta DROP COLUMN directamente.")
    print("Para revertir, necesitaría recrear la tabla sin estas columnas.")


if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("MIGRACIÓN: Agregar Verificación de Presencia")
        print("="*60 + "\n")
        
        upgrade()
        
        print("\n" + "="*60)
        print("Migración finalizada")
        print("="*60 + "\n")
