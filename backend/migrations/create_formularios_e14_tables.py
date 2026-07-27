"""
Migración para crear tablas de formularios E-14
"""
from backend.database import db
from backend.app import create_app


def upgrade():
    """Crear tablas de formularios E-14"""
    app = create_app()
    
    with app.app_context():
        # Importar modelos para que SQLAlchemy los registre
        from backend.models.formulario_e14 import FormularioE14, VotoPartido, VotoCandidato, HistorialFormulario
        
        # Crear tablas
        db.create_all()
        
        # Crear índices adicionales para optimización
        with db.engine.connect() as conn:
            # Índice compuesto para búsquedas frecuentes
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_formularios_mesa_estado 
                ON formularios_e14(mesa_id, estado)
            """))
            
            # Índice para ordenamiento por fecha
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_formularios_created_at 
                ON formularios_e14(created_at DESC)
            """))
            
            # Índice para búsquedas por testigo
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_formularios_testigo 
                ON formularios_e14(testigo_id)
            """))
            
            # Índice para búsquedas por validador
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_formularios_validado_por 
                ON formularios_e14(validado_por_id)
            """))
            
            # Índice para votos por partido
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_votos_partidos_formulario 
                ON votos_partidos(formulario_id)
            """))
            
            # Índice para votos por candidato
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_votos_candidatos_formulario 
                ON votos_candidatos(formulario_id)
            """))
            
            # Índice para historial
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_historial_formulario 
                ON historial_formularios(formulario_id, created_at DESC)
            """))
            
            conn.commit()
        
        print("✓ Tablas de formularios E-14 creadas exitosamente")
        print("✓ Índices de optimización creados")


def downgrade():
    """Eliminar tablas de formularios E-14"""
    app = create_app()
    
    with app.app_context():
        # Eliminar índices
        with db.engine.connect() as conn:
            conn.execute(db.text("DROP INDEX IF EXISTS idx_formularios_mesa_estado"))
            conn.execute(db.text("DROP INDEX IF EXISTS idx_formularios_created_at"))
            conn.execute(db.text("DROP INDEX IF EXISTS idx_formularios_testigo"))
            conn.execute(db.text("DROP INDEX IF EXISTS idx_formularios_validado_por"))
            conn.execute(db.text("DROP INDEX IF EXISTS idx_votos_partidos_formulario"))
            conn.execute(db.text("DROP INDEX IF EXISTS idx_votos_candidatos_formulario"))
            conn.execute(db.text("DROP INDEX IF EXISTS idx_historial_formulario"))
            conn.commit()
        
        # Eliminar tablas
        db.session.execute(db.text("DROP TABLE IF EXISTS historial_formularios CASCADE"))
        db.session.execute(db.text("DROP TABLE IF EXISTS votos_candidatos CASCADE"))
        db.session.execute(db.text("DROP TABLE IF EXISTS votos_partidos CASCADE"))
        db.session.execute(db.text("DROP TABLE IF EXISTS formularios_e14 CASCADE"))
        db.session.commit()
        
        print("✓ Tablas de formularios E-14 eliminadas")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'downgrade':
        downgrade()
    else:
        upgrade()
