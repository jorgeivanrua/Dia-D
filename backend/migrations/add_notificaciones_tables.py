"""
Migración para agregar tablas de notificaciones
"""
from backend.database import db
from backend.app import create_app

def upgrade():
    """Crear tablas de notificaciones"""
    app = create_app()
    
    with app.app_context():
        # Crear tablas usando SQLAlchemy
        from backend.models.notificacion import Notificacion, ConfiguracionNotificaciones
        
        # Crear tablas
        db.create_all()
        
        print("✅ Tablas de notificaciones creadas:")
        print("   - notificaciones")
        print("   - configuracion_notificaciones")
        
        # Crear índices adicionales para optimizar queries
        with db.engine.connect() as conn:
            # Índice para buscar notificaciones no leídas por usuario
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_notificaciones_usuario_leida 
                ON notificaciones(usuario_id, leida, fecha_creacion DESC)
            """))
            
            # Índice para buscar notificaciones por incidente
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_notificaciones_incidente 
                ON notificaciones(incidente_id) 
                WHERE incidente_id IS NOT NULL
            """))
            
            # Índice para buscar notificaciones por delito
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_notificaciones_delito 
                ON notificaciones(delito_id) 
                WHERE delito_id IS NOT NULL
            """))
            
            conn.commit()
        
        print("✅ Índices creados para optimizar queries")

def downgrade():
    """Eliminar tablas de notificaciones"""
    app = create_app()
    
    with app.app_context():
        # Eliminar índices
        with db.engine.connect() as conn:
            conn.execute(db.text("DROP INDEX IF EXISTS idx_notificaciones_usuario_leida"))
            conn.execute(db.text("DROP INDEX IF EXISTS idx_notificaciones_incidente"))
            conn.execute(db.text("DROP INDEX IF EXISTS idx_notificaciones_delito"))
            conn.commit()
        
        # Eliminar tablas
        db.session.execute(db.text("DROP TABLE IF EXISTS notificaciones CASCADE"))
        db.session.execute(db.text("DROP TABLE IF EXISTS configuracion_notificaciones CASCADE"))
        db.session.commit()
        
        print("✅ Tablas de notificaciones eliminadas")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'downgrade':
        downgrade()
    else:
        upgrade()
