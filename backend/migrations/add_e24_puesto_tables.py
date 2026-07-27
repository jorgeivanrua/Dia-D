"""
Migración para agregar tablas E-24 Puesto
"""
from backend.database import db
from backend.app import create_app


def upgrade():
    """Crear tablas E-24 Puesto"""
    app = create_app()
    
    with app.app_context():
        from backend.models.coordinador_municipal import FormularioE24Puesto, VotoPartidoE24Puesto
        
        print("Creando tablas E-24 Puesto...")
        
        db.create_all()
        
        # Crear índices
        with db.engine.connect() as conn:
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_e24_puesto_puesto 
                ON formularios_e24_puesto(puesto_id)
            """))
            
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_e24_puesto_coordinador 
                ON formularios_e24_puesto(coordinador_id)
            """))
            
            conn.commit()
        
        print("✓ Tablas E-24 Puesto creadas exitosamente")


def downgrade():
    """Eliminar tablas E-24 Puesto"""
    app = create_app()
    
    with app.app_context():
        print("Eliminando tablas E-24 Puesto...")
        
        with db.engine.connect() as conn:
            conn.execute(db.text("DROP INDEX IF EXISTS idx_e24_puesto_puesto"))
            conn.execute(db.text("DROP INDEX IF EXISTS idx_e24_puesto_coordinador"))
            conn.commit()
        
        db.session.execute(db.text("DROP TABLE IF EXISTS votos_partidos_e24_puesto CASCADE"))
        db.session.execute(db.text("DROP TABLE IF EXISTS formularios_e24_puesto CASCADE"))
        db.session.commit()
        
        print("✓ Tablas E-24 Puesto eliminadas")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'downgrade':
        downgrade()
    else:
        upgrade()
