-- Migración: Agregar campos territoriales y de importación
-- Fecha: 2024-11-21
-- Descripción: Agregar campos para ámbito territorial, logos y diferenciación de E-24

-- Agregar campos a tabla partidos
ALTER TABLE partidos ADD COLUMN IF NOT EXISTS sigla VARCHAR(20);
ALTER TABLE partidos ADD COLUMN IF NOT EXISTS color_hex VARCHAR(7);
ALTER TABLE partidos ADD COLUMN IF NOT EXISTS ambito_territorial VARCHAR(50) DEFAULT 'nacional';
ALTER TABLE partidos ADD COLUMN IF NOT EXISTS tipo_eleccion_id INTEGER REFERENCES tipos_eleccion(id);

-- Agregar campos a tabla candidatos
ALTER TABLE candidatos ADD COLUMN IF NOT EXISTS ambito_territorial VARCHAR(50) DEFAULT 'nacional';
ALTER TABLE candidatos ADD COLUMN IF NOT EXISTS departamento_codigo VARCHAR(10);
ALTER TABLE candidatos ADD COLUMN IF NOT EXISTS municipio_codigo VARCHAR(10);
ALTER TABLE candidatos ADD COLUMN IF NOT EXISTS foto_url VARCHAR(500);
ALTER TABLE candidatos ADD COLUMN IF NOT EXISTS numero_lista INTEGER;

-- Agregar campos a tabla tipos_eleccion
ALTER TABLE tipos_eleccion ADD COLUMN IF NOT EXISTS ambito_territorial VARCHAR(50) DEFAULT 'nacional';
ALTER TABLE tipos_eleccion ADD COLUMN IF NOT EXISTS nivel_consolidacion VARCHAR(50) DEFAULT 'puesto';

-- Crear tabla para configuración de E-24
CREATE TABLE IF NOT EXISTS configuracion_e24 (
    id SERIAL PRIMARY KEY,
    nivel VARCHAR(50) NOT NULL, -- 'puesto', 'municipal', 'departamental', 'nacional'
    tipo_eleccion_id INTEGER REFERENCES tipos_eleccion(id),
    departamento_codigo VARCHAR(10),
    municipio_codigo VARCHAR(10),
    puesto_codigo VARCHAR(10),
    incluir_logos BOOLEAN DEFAULT TRUE,
    incluir_fotos_candidatos BOOLEAN DEFAULT FALSE,
    formato_salida VARCHAR(20) DEFAULT 'pdf',
    plantilla_personalizada TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices
CREATE INDEX IF NOT EXISTS idx_partidos_ambito ON partidos(ambito_territorial);
CREATE INDEX IF NOT EXISTS idx_candidatos_ambito ON candidatos(ambito_territorial);
CREATE INDEX IF NOT EXISTS idx_candidatos_territorio ON candidatos(departamento_codigo, municipio_codigo);
CREATE INDEX IF NOT EXISTS idx_config_e24_nivel ON configuracion_e24(nivel);

-- Comentarios
COMMENT ON COLUMN partidos.ambito_territorial IS 'Ámbito: nacional, departamental, municipal';
COMMENT ON COLUMN candidatos.ambito_territorial IS 'Ámbito: nacional, departamental, municipal';
COMMENT ON COLUMN tipos_eleccion.nivel_consolidacion IS 'Nivel de consolidación: puesto, municipal, departamental, nacional';
COMMENT ON TABLE configuracion_e24 IS 'Configuración personalizada para generación de E-24 por nivel territorial';
