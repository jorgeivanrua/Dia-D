"""
Script de inicialización de la aplicación
Se ejecuta al iniciar para asegurar que la BD esté lista
"""
import os
from backend.app import create_app
from backend.database import db

def init_database():
    """Inicializar base de datos si no existe"""
    app = create_app('production')
    
    with app.app_context():
        # Verificar si la BD tiene datos
        from backend.models.locations import Departamento
        
        departamentos_count = Departamento.query.count()
        
        if departamentos_count == 0:
            print("⚠️  Base de datos vacía. Inicializando con datos de prueba...")
            
            # Importar y ejecutar el script de carga
            import sys
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            from backend.scripts.load_complete_test_data import load_complete_data
            load_complete_data()
            
            print("✅ Base de datos inicializada correctamente")
        else:
            print(f"✅ Base de datos ya tiene datos ({departamentos_count} departamentos)")

if __name__ == '__main__':
    init_database()
