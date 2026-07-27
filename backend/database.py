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
    
    # Importar modelos para que Alembic los detecte (cuando existan)
    with app.app_context():
        try:
            from backend.models import user, location, form_e14, political_party, notification, audit_log
        except ImportError:
            # Los modelos aún no están creados
            pass
        
        # Crear todas las tablas si no existen
        db.create_all()
