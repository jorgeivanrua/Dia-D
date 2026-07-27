"""
Script para aplicar migración del rol monitoreo
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db

app = create_app()

with app.app_context():
    print("🔄 Aplicando migración para rol monitoreo...")
    
    try:
        # Leer SQL
        with open('backend/migrations/add_rol_monitoreo.sql', 'r') as f:
            sql = f.read()
        
        # Ejecutar cada statement
        for statement in sql.split(';'):
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                print(f"Ejecutando: {statement[:50]}...")
                db.session.execute(db.text(statement))
        
        db.session.commit()
        print("✅ Migración aplicada exitosamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.session.rollback()
