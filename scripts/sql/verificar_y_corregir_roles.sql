-- Script para verificar y corregir roles de usuarios
-- Sistema Electoral

-- ============================================
-- 1. VERIFICAR ROLES ACTUALES
-- ============================================

SELECT '=== USUARIOS DE PRUEBA ===' as info;

SELECT 
    id,
    nombre,
    rol,
    activo,
    ubicacion_id,
    presencia_verificada
FROM users 
WHERE nombre IN ('admin', 'testigo', 'coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental')
ORDER BY nombre;

SELECT '=== CONTEO POR ROL ===' as info;

SELECT 
    rol,
    COUNT(*) as cantidad,
    SUM(CASE WHEN activo = 1 THEN 1 ELSE 0 END) as activos,
    SUM(CASE WHEN activo = 0 THEN 1 ELSE 0 END) as inactivos
FROM users
GROUP BY rol
ORDER BY rol;

-- ============================================
-- 2. IDENTIFICAR PROBLEMAS
-- ============================================

SELECT '=== USUARIOS CON POSIBLES PROBLEMAS ===' as info;

-- Testigos sin ubicación
SELECT 
    'Testigos sin ubicación' as problema,
    COUNT(*) as cantidad
FROM users
WHERE rol = 'testigo_electoral' AND ubicacion_id IS NULL;

-- Usuarios inactivos
SELECT 
    'Usuarios inactivos' as problema,
    COUNT(*) as cantidad
FROM users
WHERE activo = 0;

-- Usuarios con contraseñas no estándar (no test123 ni admin123)
SELECT 
    'Usuarios con contraseñas no estándar' as problema,
    COUNT(*) as cantidad
FROM users
WHERE password_hash NOT IN ('test123', 'admin123');

-- ============================================
-- 3. CORRECCIONES (COMENTADAS - DESCOMENTAR PARA EJECUTAR)
-- ============================================

-- Corregir rol del usuario admin
-- UPDATE users SET rol = 'super_admin' WHERE nombre = 'admin';

-- Corregir rol del usuario testigo
-- UPDATE users SET rol = 'testigo_electoral' WHERE nombre = 'testigo';

-- Corregir rol del coordinador de puesto
-- UPDATE users SET rol = 'coordinador_puesto' WHERE nombre = 'coordinador_puesto';

-- Corregir rol del coordinador municipal
-- UPDATE users SET rol = 'coordinador_municipal' WHERE nombre = 'coordinador_municipal';

-- Corregir rol del coordinador departamental
-- UPDATE users SET rol = 'coordinador_departamental' WHERE nombre = 'coordinador_departamental';

-- Activar todos los usuarios de prueba
-- UPDATE users SET activo = 1 WHERE nombre IN ('admin', 'testigo', 'coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental');

-- Resetear contraseñas a test123 (SOLO PARA DESARROLLO)
-- UPDATE users SET password_hash = 'test123' WHERE nombre != 'admin';
-- UPDATE users SET password_hash = 'admin123' WHERE nombre = 'admin';

-- ============================================
-- 4. VERIFICACIÓN FINAL
-- ============================================

SELECT '=== VERIFICACIÓN FINAL ===' as info;

SELECT 
    nombre,
    rol,
    activo,
    password_hash,
    ubicacion_id
FROM users 
WHERE nombre IN ('admin', 'testigo', 'coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental')
ORDER BY nombre;
