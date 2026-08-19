"""
Configuración de base de datos
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instancias globales
db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    """
    Inicializar base de datos con la aplicación Flask
    
    Args:
        app: Instancia de Flask
    """
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Asegurar que el directorio instance/ existe (necesario para SQLite en producción)
    import os
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    instance_dir = os.path.join(project_root, 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    
    # Importar modelos para que Alembic los detecte (cuando existan)
    with app.app_context():
        try:
            from backend.models import user, location, form_e14, political_party, notification, audit_log
        except ImportError:
            # Los modelos aún no están creados
            pass
        
        # Solucionar conflicto: tipo "users" ya existe en pg_catalog de PG 15/17
        # Los datos viejos de PG15 tienen una tabla/users con estructura distinta.
        # La secuencia correcta es: 1) DROP TABLE users CASCADE, 2) DROP TYPE IF EXISTS users CASCADE, 3) db.create_all()
        try:
            from sqlalchemy import text
            db.session.execute(text("DROP TABLE IF EXISTS users CASCADE"))
            db.session.commit()
        except Exception:
            # Si la tabla no existe, continúa sin error
            pass
        
        try:
            from sqlalchemy import text
            db.session.execute(text("DROP TYPE IF EXISTS users CASCADE"))
            db.session.commit()
        except Exception:
            # Si el tipo no existe, continúa sin error
            pass
        
        # Crear todas las tablas si no existen
        db.create_all()
