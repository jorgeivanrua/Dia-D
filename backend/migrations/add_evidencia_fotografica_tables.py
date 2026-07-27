"""
Migración para agregar tabla de evidencias fotográficas y campos de geolocalización
"""
from backend.database import db
from backend.app import create_app


def upgrade():
    """Crear tabla evidencias_fotograficas y agregar campos a incidentes/delitos"""
    app = create_app()
    
    with app.app_context():
        # Importar modelos para que SQLAlchemy los registre
        from backend.models.incidentes_delitos import (
            IncidenteElectoral, 
            DelitoElectoral, 
            EvidenciaFotografica
        )
        
        # Crear tabla de evidencias fotográficas
        db.create_all()
        
        # Agregar nuevos campos a incidentes_electorales
        with db.engine.connect() as conn:
            # Campos de geolocalización del reporte
            conn.execute(db.text("""
                ALTER TABLE incidentes_electorales 
                ADD COLUMN IF NOT EXISTS latitud_reporte FLOAT
            """))
            conn.execute(db.text("""
                ALTER TABLE incidentes_electorales 
                ADD COLUMN IF NOT EXISTS longitud_reporte FLOAT
            """))
            conn.execute(db.text("""
                ALTER TABLE incidentes_electorales 
                ADD COLUMN IF NOT EXISTS precision_gps FLOAT
            """))
            
            # Campos de sincronización offline
            conn.execute(db.text("""
                ALTER TABLE incidentes_electorales 
                ADD COLUMN IF NOT EXISTS sincronizado BOOLEAN DEFAULT TRUE
            """))
            conn.execute(db.text("""
                ALTER TABLE incidentes_electorales 
                ADD COLUMN IF NOT EXISTS fecha_sincronizacion TIMESTAMP
            """))
            conn.execute(db.text("""
                ALTER TABLE incidentes_electorales 
                ADD COLUMN IF NOT EXISTS dispositivo_id VARCHAR(100)
            """))
            
            # Agregar nuevos campos a delitos_electorales
            conn.execute(db.text("""
                ALTER TABLE delitos_electorales 
                ADD COLUMN IF NOT EXISTS latitud_reporte FLOAT
            """))
            conn.execute(db.text("""
                ALTER TABLE delitos_electorales 
                ADD COLUMN IF NOT EXISTS longitud_reporte FLOAT
            """))
            conn.execute(db.text("""
                ALTER TABLE delitos_electorales 
                ADD COLUMN IF NOT EXISTS precision_gps FLOAT
            """))
            conn.execute(db.text("""
                ALTER TABLE delitos_electorales 
                ADD COLUMN IF NOT EXISTS sincronizado BOOLEAN DEFAULT TRUE
            """))
            conn.execute(db.text("""
                ALTER TABLE delitos_electorales 
                ADD COLUMN IF NOT EXISTS fecha_sincronizacion TIMESTAMP
            """))
            conn.execute(db.text("""
                ALTER TABLE delitos_electorales 
                ADD COLUMN IF NOT EXISTS dispositivo_id VARCHAR(100)
            """))
            
            # Crear índices para evidencias fotográficas
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_evidencias_incidente 
                ON evidencias_fotograficas(incidente_id)
            """))
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_evidencias_delito 
                ON evidencias_fotograficas(delito_id)
            """))
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_evidencias_subido_por 
                ON evidencias_fotograficas(subido_por_id)
            """))
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_evidencias_fecha_subida 
                ON evidencias_fotograficas(fecha_subida DESC)
            """))
            
            # Índices para geolocalización
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_incidentes_geolocalizacion 
                ON incidentes_electorales(latitud_reporte, longitud_reporte)
            """))
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_delitos_geolocalizacion 
                ON delitos_electorales(latitud_reporte, longitud_reporte)
            """))
            
            # Índices para sincronización
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_incidentes_sincronizado 
                ON incidentes_electorales(sincronizado)
            """))
            conn.execute(db.text("""
                CREATE INDEX IF NOT EXISTS idx_delitos_sincronizado 
                ON delitos_electorales(sincronizado)
            """))
            
            conn.commit()
        
        print("✓ Tabla evidencias_fotograficas creada exitosamente")
        print("✓ Campos de geolocalización agregados a incidentes y delitos")
        print("✓ Campos de sincronización offline agregados")
        print("✓ Índices creados exitosamente")


def downgrade():
    """Revertir cambios"""
    app = create_app()
    
    with app.app_context():
        with db.engine.connect() as conn:
            # Eliminar tabla de evidencias
            conn.execute(db.text("DROP TABLE IF EXISTS evidencias_fotograficas CASCADE"))
            
            # Eliminar campos de incidentes
            conn.execute(db.text("ALTER TABLE incidentes_electorales DROP COLUMN IF EXISTS latitud_reporte"))
            conn.execute(db.text("ALTER TABLE incidentes_electorales DROP COLUMN IF EXISTS longitud_reporte"))
            conn.execute(db.text("ALTER TABLE incidentes_electorales DROP COLUMN IF EXISTS precision_gps"))
            conn.execute(db.text("ALTER TABLE incidentes_electorales DROP COLUMN IF EXISTS sincronizado"))
            conn.execute(db.text("ALTER TABLE incidentes_electorales DROP COLUMN IF EXISTS fecha_sincronizacion"))
            conn.execute(db.text("ALTER TABLE incidentes_electorales DROP COLUMN IF EXISTS dispositivo_id"))
            
            # Eliminar campos de delitos
            conn.execute(db.text("ALTER TABLE delitos_electorales DROP COLUMN IF EXISTS latitud_reporte"))
            conn.execute(db.text("ALTER TABLE delitos_electorales DROP COLUMN IF EXISTS longitud_reporte"))
            conn.execute(db.text("ALTER TABLE delitos_electorales DROP COLUMN IF EXISTS precision_gps"))
            conn.execute(db.text("ALTER TABLE delitos_electorales DROP COLUMN IF EXISTS sincronizado"))
            conn.execute(db.text("ALTER TABLE delitos_electorales DROP COLUMN IF EXISTS fecha_sincronizacion"))
            conn.execute(db.text("ALTER TABLE delitos_electorales DROP COLUMN IF EXISTS dispositivo_id"))
            
            conn.commit()
        
        print("✓ Migración revertida exitosamente")


if __name__ == '__main__':
    upgrade()
