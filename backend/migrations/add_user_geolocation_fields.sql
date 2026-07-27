-- Agregar campos de geolocalización al modelo User
-- Fecha: 2025-11-22

-- Agregar campos de geolocalización
ALTER TABLE users ADD COLUMN IF NOT EXISTS ultima_latitud FLOAT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS ultima_longitud FLOAT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS ultima_geolocalizacion_at TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS precision_geolocalizacion FLOAT;

-- Crear índice para búsquedas geográficas
CREATE INDEX IF NOT EXISTS idx_users_geolocation ON users(ultima_latitud, ultima_longitud) WHERE ultima_latitud IS NOT NULL AND ultima_longitud IS NOT NULL;

-- Comentarios
COMMENT ON COLUMN users.ultima_latitud IS 'Última latitud reportada por el usuario';
COMMENT ON COLUMN users.ultima_longitud IS 'Última longitud reportada por el usuario';
COMMENT ON COLUMN users.ultima_geolocalizacion_at IS 'Fecha y hora de la última geolocalización';
COMMENT ON COLUMN users.precision_geolocalizacion IS 'Precisión de la geolocalización en metros';
