"""
Migración para crear tablas del coordinador municipal
"""
from backend.database import db
from backend.app import create_app


def upgrade():
    """Crear tablas del coordinador municipal"""
    app = create_app()
    
    with app.app_context():
        # Importar modelos para que SQLAlchemy los registre
        from backend.models.coordinador_municipal import (
            FormularioE24Municipal,
            VotoPartidoE24Municipal,
            Notificacion,
            AuditLog
        )
        
        print("Creando tablas para coordinador municipal...")
        
        # Crear todas las tablas definidas en los modelos
        db.create_all()
        
        # Crear índices adicionales para optimización
        with db.engine.connect() as conn:
            # Índice para búsquedas de E-24 por municipio
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_e24_municipal_municipio 
                ON formularios_e24_municipal(municipio_id)
            """))
            
            # Índice para búsquedas de E-24 por coordinador
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_e24_municipal_coordinador 
                ON formularios_e24_municipal(coordinador_id)
            """))
            
            # Índice para notificaciones no leídas por destinatario
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_notificaciones_destinatario_leida 
                ON notificaciones(destinatario_id, leida)
            """))
            
            # Índice para logs de auditoría por usuario y fecha
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_audit_logs_user_created 
                ON audit_logs(user_id, created_at DESC)
            """))
            
            # Índice para logs de auditoría por recurso
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_audit_logs_recurso 
                ON audit_logs(recurso, recurso_id)
            """))
            
            conn.commit()
        
        print("✓ Tablas del coordinador municipal creadas exitosamente")
        print("✓ Índices de optimización creados")


def downgrade():
    """Eliminar tablas del coordinador municipal"""
    app = create_app()
    
    with app.app_context():
        print("Eliminando tablas del coordinador municipal...")
        
        # Eliminar índices primero
        with db.engine.connect() as conn:
            conn.execute(db.text("DROP INDEX IF EXISTS idx_e24_municipal_municipio"))
            conn.execute(db.text("DROP INDEX IF EXISTS idx_e24_municipal_coordinador"))
            conn.execute(db.text("DROP INDEX IF EXISTS idx_notificaciones_destinatario_leida"))
            conn.execute(db.text("DROP INDEX IF EXISTS idx_audit_logs_user_created"))
            conn.execute(db.text("DROP INDEX IF EXISTS idx_audit_logs_recurso"))
            conn.commit()
        
        # Eliminar tablas
        db.session.execute(db.text("DROP TABLE IF EXISTS audit_logs CASCADE"))
        db.session.execute(db.text("DROP TABLE IF EXISTS notificaciones CASCADE"))
        db.session.execute(db.text("DROP TABLE IF EXISTS votos_partidos_e24_municipal CASCADE"))
        db.session.execute(db.text("DROP TABLE IF EXISTS formularios_e24_municipal CASCADE"))
        db.session.commit()
        
        print("✓ Tablas del coordinador municipal eliminadas")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'downgrade':
        downgrade()
    else:
        upgrade()
