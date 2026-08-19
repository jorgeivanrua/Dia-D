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
        
        from sqlalchemy import text
        
        # Serializar la inicialización entre workers/replicas con advisory lock
        # de PostgreSQL. Evita que dos workers corran create_all() a la vez y
        # choquen con "duplicate key pg_type_typname_nsp_index (users, 2200)".
        conn = db.session.connection()
        locked = False
        try:
            conn.execute(text("SELECT pg_advisory_lock(82413001)"))
            locked = True
        except Exception:
            pass  # SQLite o sin soporte de advisory lock
        
        try:
            # RESET_DB=true borra todas las tablas existentes (deploy limpio).
            import os
            if os.getenv('RESET_DB', 'false').lower() == 'true':
                db.metadata.drop_all(bind=conn if locked else db.engine)
                db.session.commit()

            # Crear todas las tablas (checkfirst=True: no recrea las que ya
            # existen, por eso un reinicio normal conserva los datos).
            #
            # Si la estructura heredada de PG15 está rota (el tipo compuesto
            # "users" de la versión vieja bloquea el CREATE TABLE), create_all
            # lanza duplicate key. Entonces se limpia tabla + tipo y se
            # reintenta una sola vez.
            try:
                if locked:
                    db.metadata.create_all(bind=conn)
                else:
                    db.create_all()
            except Exception as e:
                db.session.rollback()
                if 'duplicate key' in str(e).lower() or 'pg_type' in str(e).lower():
                    db.session.execute(text("DROP TABLE IF EXISTS users CASCADE"))
                    db.session.commit()
                    db.session.execute(text("DROP TYPE IF EXISTS users CASCADE"))
                    db.session.commit()
                    if locked:
                        db.metadata.create_all(bind=conn)
                    else:
                        db.create_all()
                else:
                    raise
        finally:
            if locked:
                try:
                    conn.execute(text("SELECT pg_advisory_unlock(82413001)"))
                    db.session.commit()
                except Exception:
                    db.session.rollback()
