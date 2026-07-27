"""
Migración para crear tablas de partidos políticos y candidatos
"""
from backend.database import db
from backend.app import create_app

def create_tables():
    """Crear tablas de partidos y candidatos"""
    app = create_app()
    
    with app.app_context():
        # SQL para crear tabla de partidos políticos
        sql_partidos = """
        CREATE TABLE IF NOT EXISTS partidos_politicos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(200) NOT NULL UNIQUE,
            sigla VARCHAR(20) NOT NULL UNIQUE,
            color VARCHAR(7) NOT NULL DEFAULT '#000000',
            logo_url VARCHAR(500),
            descripcion TEXT,
            activo BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_partidos_activo ON partidos_politicos(activo);
        CREATE INDEX IF NOT EXISTS idx_partidos_nombre ON partidos_politicos(nombre);
        CREATE INDEX IF NOT EXISTS idx_partidos_sigla ON partidos_politicos(sigla);
        """
        
        # SQL para crear tabla de candidatos
        sql_candidatos = """
        CREATE TABLE IF NOT EXISTS candidatos (
            id SERIAL PRIMARY KEY,
            nombre_completo VARCHAR(200) NOT NULL,
            partido_id INTEGER NOT NULL REFERENCES partidos_politicos(id),
            tipo_eleccion_id INTEGER NOT NULL REFERENCES tipos_eleccion(id),
            cargo VARCHAR(100) NOT NULL,
            numero_lista INTEGER,
            foto_url VARCHAR(500),
            biografia TEXT,
            activo BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_candidatos_partido ON candidatos(partido_id);
        CREATE INDEX IF NOT EXISTS idx_candidatos_tipo_eleccion ON candidatos(tipo_eleccion_id);
        CREATE INDEX IF NOT EXISTS idx_candidatos_activo ON candidatos(activo);
        CREATE INDEX IF NOT EXISTS idx_candidatos_nombre ON candidatos(nombre_completo);
        """
        
        try:
            # Ejecutar SQL
            db.session.execute(db.text(sql_partidos))
            print("✅ Tabla partidos_politicos creada")
            
            db.session.execute(db.text(sql_candidatos))
            print("✅ Tabla candidatos creada")
            
            db.session.commit()
            print("✅ Migración completada exitosamente")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error en migración: {str(e)}")
            raise

if __name__ == '__main__':
    create_tables()
