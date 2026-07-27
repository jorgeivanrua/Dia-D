-- ============================================================================
-- ÍNDICES PARA OPTIMIZACIÓN DEL ROL DE MONITOREO
-- ============================================================================
-- Fecha: 28 de Noviembre de 2025
-- Propósito: Mejorar el rendimiento de las consultas del dashboard de monitoreo
-- ============================================================================

-- ============================================================================
-- ÍNDICES PARA TABLA USERS
-- ============================================================================

-- Índice compuesto para consultas de usuarios activos por rol
CREATE INDEX IF NOT EXISTS idx_users_rol_activo 
ON users(rol, activo);

-- Índice para usuarios con geolocalización
CREATE INDEX IF NOT EXISTS idx_users_geolocalizacion 
ON users(ultima_latitud) 
WHERE ultima_latitud IS NOT NULL;

-- Índice para timestamp de última geolocalización (actividad reciente)
CREATE INDEX IF NOT EXISTS idx_users_geolocalizacion_at 
ON users(ultima_geolocalizacion_at);

-- Índice para presencia verificada
CREATE INDEX IF NOT EXISTS idx_users_presencia 
ON users(presencia_verificada, rol, activo);

-- Índice para ubicación (JOIN con locations)
CREATE INDEX IF NOT EXISTS idx_users_ubicacion 
ON users(ubicacion_id);

-- ============================================================================
-- ÍNDICES PARA TABLA LOCATIONS
-- ============================================================================

-- Índice para tipo de ubicación
CREATE INDEX IF NOT EXISTS idx_locations_tipo 
ON locations(tipo_ubicacion);

-- Índice para código de departamento
CREATE INDEX IF NOT EXISTS idx_locations_departamento 
ON locations(departamento_codigo);

-- Índice compuesto para búsquedas jerárquicas
CREATE INDEX IF NOT EXISTS idx_locations_jerarquia 
ON locations(departamento_codigo, municipio_codigo, zona_codigo);

-- ============================================================================
-- ÍNDICES PARA TABLA FORMULARIOS_E14
-- ============================================================================

-- Índice para estado de formularios
CREATE INDEX IF NOT EXISTS idx_formularios_estado 
ON formularios_e14(estado);

-- Índice para fecha de creación (actividad reciente)
CREATE INDEX IF NOT EXISTS idx_formularios_created_at 
ON formularios_e14(created_at DESC);

-- Índice para usuario que envió (JOIN con users)
CREATE INDEX IF NOT EXISTS idx_formularios_usuario 
ON formularios_e14(usuario_id);

-- Índice compuesto para consultas de estado y fecha
CREATE INDEX IF NOT EXISTS idx_formularios_estado_fecha 
ON formularios_e14(estado, created_at DESC);

-- ============================================================================
-- ÍNDICES PARA TABLA INCIDENTES_ELECTORALES
-- ============================================================================

-- Índice para severidad de incidentes
CREATE INDEX IF NOT EXISTS idx_incidentes_severidad 
ON incidentes_electorales(severidad);

-- Índice para estado de incidentes
CREATE INDEX IF NOT EXISTS idx_incidentes_estado 
ON incidentes_electorales(estado);

-- Índice para fecha de reporte (actividad reciente)
CREATE INDEX IF NOT EXISTS idx_incidentes_fecha_reporte 
ON incidentes_electorales(fecha_reporte DESC);

-- Índice compuesto para alertas críticas
CREATE INDEX IF NOT EXISTS idx_incidentes_criticos 
ON incidentes_electorales(severidad, estado) 
WHERE severidad = 'critica';

-- Índice para usuario que reportó (JOIN con users)
CREATE INDEX IF NOT EXISTS idx_incidentes_reportado_por 
ON incidentes_electorales(reportado_por_id);

-- Índice compuesto para consultas de severidad, estado y fecha
CREATE INDEX IF NOT EXISTS idx_incidentes_completo 
ON incidentes_electorales(severidad, estado, fecha_reporte DESC);

-- ============================================================================
-- ÍNDICES PARA TABLA DELITOS_ELECTORALES
-- ============================================================================

-- Índice para gravedad de delitos
CREATE INDEX IF NOT EXISTS idx_delitos_gravedad 
ON delitos_electorales(gravedad);

-- Índice para estado de delitos
CREATE INDEX IF NOT EXISTS idx_delitos_estado 
ON delitos_electorales(estado);

-- Índice para fecha de reporte (actividad reciente)
CREATE INDEX IF NOT EXISTS idx_delitos_fecha_reporte 
ON delitos_electorales(fecha_reporte DESC);

-- Índice compuesto para alertas de delitos graves
CREATE INDEX IF NOT EXISTS idx_delitos_graves 
ON delitos_electorales(gravedad, estado) 
WHERE gravedad IN ('grave', 'muy_grave');

-- Índice para usuario que reportó (JOIN con users)
CREATE INDEX IF NOT EXISTS idx_delitos_reportado_por 
ON delitos_electorales(reportado_por_id);

-- Índice compuesto para consultas de gravedad, estado y fecha
CREATE INDEX IF NOT EXISTS idx_delitos_completo 
ON delitos_electorales(gravedad, estado, fecha_reporte DESC);

-- ============================================================================
-- ANÁLISIS Y ESTADÍSTICAS
-- ============================================================================

-- Actualizar estadísticas de las tablas para el optimizador de consultas
ANALYZE users;
ANALYZE locations;
ANALYZE formularios_e14;
ANALYZE incidentes_electorales;
ANALYZE delitos_electorales;

-- ============================================================================
-- VERIFICACIÓN DE ÍNDICES CREADOS
-- ============================================================================

-- Para PostgreSQL:
-- SELECT tablename, indexname, indexdef 
-- FROM pg_indexes 
-- WHERE tablename IN ('users', 'locations', 'formularios_e14', 'incidentes_electorales', 'delitos_electorales')
-- ORDER BY tablename, indexname;

-- Para MySQL:
-- SHOW INDEX FROM users;
-- SHOW INDEX FROM locations;
-- SHOW INDEX FROM formularios_e14;
-- SHOW INDEX FROM incidentes_electorales;
-- SHOW INDEX FROM delitos_electorales;

-- ============================================================================
-- NOTAS DE RENDIMIENTO
-- ============================================================================

-- Estos índices optimizan:
-- 1. Consultas de usuarios activos por rol (testigos, coordinadores)
-- 2. Búsquedas de usuarios con geolocalización
-- 3. Filtros de formularios por estado
-- 4. Consultas de incidentes por severidad
-- 5. Búsquedas de delitos por gravedad
-- 6. Actividad reciente (últimas 24 horas)
-- 7. Alertas críticas (incidentes y delitos graves)
-- 8. JOINs entre tablas relacionadas

-- Mejora esperada de rendimiento:
-- - Consultas simples: 50-80% más rápidas
-- - Consultas con JOIN: 60-90% más rápidas
-- - Consultas de agregación: 40-70% más rápidas
-- - Dashboard completo: 50-75% más rápido

-- ============================================================================
