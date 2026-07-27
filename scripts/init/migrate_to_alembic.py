"""
Script para migrar a Flask-Migrate (Alembic) correctamente
Este script configura las migraciones de base de datos de forma profesional
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from flask_migrate import Migrate, init, migrate, upgrade
import subprocess


def setup_migrations():
    """Configurar sistema de migraciones con Alembic"""
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("\n" + "=" * 80)
        print("CONFIGURACIÓN DE MIGRACIONES CON FLASK-MIGRATE (ALEMBIC)")
        print("=" * 80)
        print()
        
        # Verificar si ya existe el directorio de migraciones
        migrations_dir = os.path.join(os.getcwd(), 'migrations')
        
        if os.path.exists(migrations_dir):
            print("⚠️  El directorio 'migrations' ya existe")
            print()
            response = input("¿Deseas reinicializar las migraciones? (s/n): ")
            
            if response.lower() != 's':
                print("Operación cancelada")
                return False
            
            # Eliminar directorio existente
            import shutil
            shutil.rmtree(migrations_dir)
            print("   ✅ Directorio de migraciones eliminado")
        
        print("📋 Paso 1: Inicializando Flask-Migrate...")
        try:
            # Inicializar migraciones
            from flask_migrate import init as flask_migrate_init
            flask_migrate_init()
            print("   ✅ Flask-Migrate inicializado")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
        
        print()
        print("📋 Paso 2: Creando migración inicial...")
        try:
            # Crear migración inicial
            subprocess.run([
                sys.executable, '-m', 'flask', 'db', 'migrate',
                '-m', 'Migración inicial del sistema'
            ], check=True)
            print("   ✅ Migración inicial creada")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
        
        print()
        print("📋 Paso 3: Aplicando migraciones...")
        try:
            # Aplicar migraciones
            subprocess.run([
                sys.executable, '-m', 'flask', 'db', 'upgrade'
            ], check=True)
            print("   ✅ Migraciones aplicadas")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
        
        print()
        print("=" * 80)
        print("✅ MIGRACIONES CONFIGURADAS CORRECTAMENTE")
        print("=" * 80)
        print()
        print("📚 Comandos útiles:")
        print()
        print("   Crear nueva migración:")
        print("   $ flask db migrate -m 'Descripción del cambio'")
        print()
        print("   Aplicar migraciones:")
        print("   $ flask db upgrade")
        print()
        print("   Ver historial:")
        print("   $ flask db history")
        print()
        print("   Revertir última migración:")
        print("   $ flask db downgrade")
        print()
        print("=" * 80)
        print()
        
        return True


if __name__ == '__main__':
    try:
        success = setup_migrations()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
