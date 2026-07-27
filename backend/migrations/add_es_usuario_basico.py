"""
Migración: Agregar campo es_usuario_basico a la tabla users
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import create_app
from backend.database import db


def upgrade():
    """Agregar campo es_usuario_basico"""
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("\n" + "=" * 80)
        print("MIGRACIÓN: Agregar campo es_usuario_basico")
        print("=" * 80)
        print()
        
        try:
            # Verificar si la columna ya existe
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('users')]
            
            if 'es_usuario_basico' in columns:
                print("✅ La columna 'es_usuario_basico' ya existe")
                return True
            
            # Agregar columna
            print("📝 Agregando columna 'es_usuario_basico'...")
            db.engine.execute(
                'ALTER TABLE users ADD COLUMN es_usuario_basico BOOLEAN DEFAULT FALSE NOT NULL'
            )
            
            print("✅ Columna agregada exitosamente")
            print()
            
            # Marcar usuarios básicos existentes
            print("🔄 Marcando usuarios básicos existentes...")
            
            roles_basicos = [
                'super_admin',
                'monitoreo',
                'coordinador_departamental',
                'coordinador_municipal',
                'coordinador_puesto',
                'auditor_electoral'
            ]
            
            from backend.models.user import User
            
            for rol in roles_basicos:
                usuarios = User.query.filter_by(rol=rol, ubicacion_id=None).all()
                for usuario in usuarios:
                    usuario.es_usuario_basico = True
                    print(f"   ✅ {usuario.nombre} ({usuario.rol})")
            
            db.session.commit()
            
            print()
            print("=" * 80)
            print("✅ MIGRACIÓN COMPLETADA")
            print("=" * 80)
            print()
            
            return True
            
        except Exception as e:
            print(f"❌ Error en migración: {e}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == '__main__':
    success = upgrade()
    sys.exit(0 if success else 1)
