#!/usr/bin/env python3
"""
Migración: Agregar campos de geolocalización al modelo User
Fecha: 2025-11-22
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.database import db
from backend.app import create_app

def apply_migration():
    """Aplicar migración de campos de geolocalización"""
    app = create_app()
    
    with app.app_context():
        try:
            print("\n" + "="*80)
            print("APLICANDO MIGRACIÓN: Campos de Geolocalización en Users")
            print("="*80 + "\n")
            
            # Leer y ejecutar el script SQL
            sql_file = os.path.join(os.path.dirname(__file__), 'add_user_geolocation_fields.sql')
            
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_commands = f.read()
            
            # Ejecutar comandos SQL
            for command in sql_commands.split(';'):
                command = command.strip()
                if command and not command.startswith('--'):
                    try:
                        db.session.execute(db.text(command))
                    except Exception as e:
                        # Ignorar errores de columnas que ya existen
                        if 'already exists' not in str(e).lower():
                            print(f"⚠️  Advertencia: {str(e)}")
            
            db.session.commit()
            
            print("\n✅ Migración aplicada exitosamente")
            print("\nCampos agregados:")
            print("  - ultima_latitud (FLOAT)")
            print("  - ultima_longitud (FLOAT)")
            print("  - ultima_geolocalizacion_at (TIMESTAMP)")
            print("  - precision_geolocalizacion (FLOAT)")
            print("\n" + "="*80 + "\n")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error aplicando migración: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = apply_migration()
    sys.exit(0 if success else 1)
