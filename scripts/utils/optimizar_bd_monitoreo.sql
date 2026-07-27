-- ============================================================================
-- OPTIMIZACIÓN DE BASE DE DATOS PARA MONITOREO
-- Índices para mejorar rendimiento de consultas
-- ============================================================================

-- Índices para tabla users (geolocalización y filtros)
CREATE INDEX IF NOT EXISTS idx_users_geo 
ON users(ultima_latitud, ultima_longitud) 
WHERE ultima_latitud IS NOT NULL AND ultima_longitud IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_users_rol_activo 
ON users(rol, activo);

CREATE INDEX IF NOT EXISTS idx_users_presencia 
ON users(presencia_verificada, presencia_verificada_at) 
WHERE rol = 'testigo_electoral';

CREATE INDEX IF NOT EXISTS idx_users_ubicacion 
ON users(ubicacion_id, activo);

CREATE INDEX IF NOT EXISTS idx_users_ultimo_acceso 
ON users(ultimo_acceso DESC);

-- Índices para tabla formularios_e14
CREATE INDEX IF NOT EXISTS idx_formularios_created 
ON formularios_e14(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_formularios_estado 
ON formularios_e14(estado, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_formularios_testigo 
ON formularios_e14(testigo_id, estado);

CREATE INDEX IF NOT EXISTS idx_formularios_ubicacion 
ON formularios_e14(ubicacion_id, created_at DESC);

-- Índices para tabla incidentes_electorales
CREATE INDEX IF NOT EXISTS idx_incidentes_created 
ON incidentes_electorales(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_incidentes_estado 
ON incidentes_electorales(estado, severidad);

CREATE INDEX IF NOT EXISTS idx_incidentes_ubicacion 
ON incidentes_electorales(ubicacion_id, created_at DESC);

-- Índices para tabla delitos_electorales
CREATE INDEX IF NOT EXISTS idx_delitos_created 
ON delitos_electorales(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_delitos_estado 
ON delitos_electorales(estado, gravedad);

CREATE INDEX IF NOT EXISTS idx_delitos_ubicacion 
ON delitos_electorales(ubicacion_id, created_at DESC);

-- Índices para tabla locations
CREATE INDEX IF NOT EXISTS idx_locations_tipo 
ON locations(tipo, activo);

CREATE INDEX IF NOT EXISTS idx_locations_departamento 
ON locations(departamento_codigo, tipo);

CREATE INDEX IF NOT EXISTS idx_locations_municipio 
ON locations(departamento_codigo, municipio_codigo, tipo);

CREATE INDEX IF NOT EXISTS idx_locations_zona 
ON locations(departamento_codigo, municipio_codigo, zona_codigo, tipo);

-- Índices para tabla audit_logs (si existe)
CREATE INDEX IF NOT EXISTS idx_audit_created 
ON audit_logs(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_audit_user 
ON audit_logs(user_id, created_at DESC);

-- Índices compuestos para consultas complejas
CREATE INDEX IF NOT EXISTS idx_users_rol_geo_activo 
ON users(rol, activo, ultima_latitud, ultima_longitud);

CREATE INDEX IF NOT EXISTS idx_formularios_estado_created 
ON formularios_e14(estado, created_at DESC, testigo_id);

-- ============================================================================
-- ANÁLISIS Y ESTADÍSTICAS
-- ============================================================================

-- Analizar tablas para actualizar estadísticas
ANALYZE users;
ANALYZE formularios_e14;
ANALYZE incidentes_electorales;
ANALYZE delitos_electorales;
ANALYZE locations;

-- ============================================================================
-- VERIFICACIÓN DE ÍNDICES
-- ============================================================================

-- Ver todos los índices creados
SELECT 
    name as index_name,
    tbl_name as table_name,
    sql
FROM sqlite_master 
WHERE type = 'index' 
AND name LIKE 'idx_%'
ORDER BY tbl_name, name;

-- ============================================================================
-- NOTAS
-- ============================================================================
-- Estos índices mejoran significativamente el rendimiento de:
-- 1. Consultas de geolocalización (mapa)
-- 2. Filtros por rol y estado
-- 3. Ordenamiento por fecha
-- 4. Joins entre tablas
-- 5. Agregaciones y conteos
--
-- Ejecutar este script después de cada migración o cambio en el esquema
-- ============================================================================
