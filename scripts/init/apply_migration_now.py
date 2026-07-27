#!/usr/bin/env python3
"""
Script para aplicar migración de geolocalización inmediatamente
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

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
            
            # Ejecutar comandos SQL directamente
            commands = [
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS ultima_latitud FLOAT;",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS ultima_longitud FLOAT;",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS ultima_geolocalizacion_at TIMESTAMP;",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS precision_geolocalizacion FLOAT;"
            ]
            
            for command in commands:
                try:
                    db.session.execute(db.text(command))
                    print(f"✓ {command}")
                except Exception as e:
                    if 'already exists' not in str(e).lower() and 'duplicate' not in str(e).lower():
                        print(f"⚠️  {command}: {str(e)}")
            
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
