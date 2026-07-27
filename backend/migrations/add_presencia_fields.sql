-- Migración: Agregar campos de presencia para todos los roles
-- Fecha: 2024-11-21
-- Descripción: Extender verificación de presencia a coordinadores y otros roles

-- Agregar campos de geolocalización
ALTER TABLE users ADD COLUMN IF NOT EXISTS ultima_latitud DECIMAL(10, 8);
ALTER TABLE users ADD COLUMN IF NOT EXISTS ultima_longitud DECIMAL(11, 8);
ALTER TABLE users ADD COLUMN IF NOT EXISTS ultima_geolocalizacion_at TIMESTAMP;

-- Crear tabla de historial de presencia
CREATE TABLE IF NOT EXISTS historial_presencia (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tipo_evento VARCHAR(50) NOT NULL, -- 'check_in', 'check_out', 'ping', 'timeout'
    latitud DECIMAL(10, 8),
    longitud DECIMAL(11, 8),
    ubicacion_id INTEGER REFERENCES locations(id),
    dispositivo_info TEXT,
    ip_address VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices
CREATE INDEX IF NOT EXISTS idx_historial_presencia_user ON historial_presencia(user_id);
CREATE INDEX IF NOT EXISTS idx_historial_presencia_fecha ON historial_presencia(created_at);
CREATE INDEX IF NOT EXISTS idx_users_ultimo_acceso ON users(ultimo_acceso);
CREATE INDEX IF NOT EXISTS idx_users_presencia ON users(presencia_verificada, ultimo_acceso);

-- Comentarios
COMMENT ON COLUMN users.ultima_latitud IS 'Última latitud registrada del usuario';
COMMENT ON COLUMN users.ultima_longitud IS 'Última longitud registrada del usuario';
COMMENT ON COLUMN users.ultima_geolocalizacion_at IS 'Fecha de última geolocalización';
COMMENT ON TABLE historial_presencia IS 'Historial de eventos de presencia de usuarios';
