"""
Script para inicializar la base de datos
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db

def init_database():
    """Inicializar base de datos"""
    # Usar configuración del entorno
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("✅ Base de datos inicializada correctamente")
        print(f"📁 Ubicación: {app.config['SQLALCHEMY_DATABASE_URI']}")

if __name__ == '__main__':
    init_database()
