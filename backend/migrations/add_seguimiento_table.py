"""
Migración para agregar tabla de seguimiento de reportes
"""
from backend.database import db
from backend.app import create_app


def upgrade():
    """Crear tabla de seguimiento"""
    app = create_app()
    
    with app.app_context():
        # Crear tabla usando SQLAlchemy
        from backend.models.seguimiento import SeguimientoReporte
        
        # Crear tabla
        db.create_all()
        
        print("✅ Tabla seguimiento_reportes creada")
        
        # Crear índices adicionales para optimizar queries
        with db.engine.connect() as conn:
            # Índice para buscar por incidente
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_seguimiento_incidente 
                ON seguimiento_reportes(incidente_id, fecha_accion DESC)
                WHERE incidente_id IS NOT NULL
            """))
            
            # Índice para buscar por delito
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_seguimiento_delito 
                ON seguimiento_reportes(delito_id, fecha_accion DESC)
                WHERE delito_id IS NOT NULL
            """))
            
            # Índice para buscar por usuario
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_seguimiento_usuario 
                ON seguimiento_reportes(usuario_id, fecha_accion DESC)
            """))
            
            # Índice para buscar por acción
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_seguimiento_accion 
                ON seguimiento_reportes(accion, fecha_accion DESC)
            """))
            
            conn.commit()
        
        print("✅ Índices creados para optimizar queries")


def downgrade():
    """Eliminar tabla de seguimiento"""
    app = create_app()
    
    with app.app_context():
        # Eliminar índices
        with db.engine.connect() as conn:
            conn.execute(db.text("DROP INDEX IF EXISTS idx_seguimiento_incidente"))
            conn.execute(db.text("DROP INDEX IF EXISTS idx_seguimiento_delito"))
            conn.execute(db.text("DROP INDEX IF EXISTS idx_seguimiento_usuario"))
            conn.execute(db.text("DROP INDEX IF EXISTS idx_seguimiento_accion"))
            conn.commit()
        
        # Eliminar tabla
        db.session.execute(db.text("DROP TABLE IF EXISTS seguimiento_reportes CASCADE"))
        db.session.commit()
        
        print("✅ Tabla seguimiento_reportes eliminada")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'downgrade':
        downgrade()
    else:
        upgrade()
