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
        
        # Inicialización sobre una conexión propia del engine (NO la de la
        # sesión): la sesión cierra su conexión en cada commit, lo que rompe
        # operaciones largas tipo create_all. Con engine.connect() la conexión
        # queda viva hasta el final del bloque y todas las operaciones (lock,
        # drop, create) van sobre la MISMA conexión.
        with db.engine.connect() as conn:
            locked = False
            try:
                # Serializar la inicialización entre workers/replicas con
                # advisory lock de PostgreSQL. Evita la carrera de create_all()
                # que producía "duplicate key pg_type_typname_nsp_index".
                conn.execute(text("SELECT pg_advisory_lock(82413001)"))
                locked = True
            except Exception:
                pass  # SQLite o sin soporte de advisory lock
            
            try:
                # RESET_DB=true borra todas las tablas existentes (deploy limpio).
                if os.getenv('RESET_DB', 'false').lower() == 'true':
                    db.metadata.drop_all(bind=conn)
                    conn.commit()
                
                # Crear todas las tablas (checkfirst=True: no recrea las que ya
                # existen, por eso un reinicio normal conserva los datos).
                #
                # Si la estructura heredada de PG15 está rota (el tipo compuesto
                # "users" de la versión vieja bloquea el CREATE TABLE), create_all
                # lanza duplicate key. Entonces se limpia tabla + tipo y se
                # reintenta una sola vez.
                try:
                    db.metadata.create_all(bind=conn)
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    if 'duplicate key' in str(e).lower() or 'pg_type' in str(e).lower():
                        conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
                        conn.commit()
                        conn.execute(text("DROP TYPE IF EXISTS users CASCADE"))
                        conn.commit()
                        db.metadata.create_all(bind=conn)
                        conn.commit()
                    else:
                        raise
            finally:
                if locked:
                    try:
                        conn.execute(text("SELECT pg_advisory_unlock(82413001)"))
                        conn.commit()
                    except Exception:
                        conn.rollback()
