"""
Migración para crear tablas del coordinador departamental
"""
from backend.database import db
from backend.app import create_app


def upgrade():
    """Crear tablas del coordinador departamental"""
    app = create_app()
    
    with app.app_context():
        # Importar modelos para que SQLAlchemy los registre
        from backend.models.coordinador_departamental import (
            ReporteDepartamental,
            VotoPartidoReporteDepartamental
        )
        
        print("Creando tablas para coordinador departamental...")
        
        # Crear todas las tablas definidas en los modelos
        db.create_all()
        
        # Crear índices adicionales para optimización
        with db.engine.connect() as conn:
            # Índice para búsquedas de reportes por departamento
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_reporte_departamental_departamento 
                ON reportes_departamentales(departamento_id)
            """))
            
            # Índice para búsquedas de reportes por coordinador
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_reporte_departamental_coordinador 
                ON reportes_departamentales(coordinador_id)
            """))
            
            conn.commit()
        
        print("✓ Tablas del coordinador departamental creadas exitosamente")
        print("✓ Índices de optimización creados")


def downgrade():
    """Eliminar tablas del coordinador departamental"""
    app = create_app()
    
    with app.app_context():
        print("Eliminando tablas del coordinador departamental...")
        
        # Eliminar índices primero
        with db.engine.connect() as conn:
            conn.execute(db.text("DROP INDEX IF EXISTS idx_reporte_departamental_departamento"))
            conn.execute(db.text("DROP INDEX IF EXISTS idx_reporte_departamental_coordinador"))
            conn.commit()
        
        # Eliminar tablas
        db.session.execute(db.text("DROP TABLE IF EXISTS votos_partidos_reporte_departamental CASCADE"))
        db.session.execute(db.text("DROP TABLE IF EXISTS reportes_departamentales CASCADE"))
        db.session.commit()
        
        print("✓ Tablas del coordinador departamental eliminadas")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'downgrade':
        downgrade()
    else:
        upgrade()
