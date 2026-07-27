@echo off
echo ========================================
echo   PRUEBA DE OPTIMIZACIONES
echo   Dashboard Super Admin
echo ========================================
echo.

echo [1/3] Verificando archivos...
if exist "frontend\static\js\optimizations\cache-manager.js" (
    echo   [OK] cache-manager.js
) else (
    echo   [ERROR] cache-manager.js no encontrado
)

if exist "frontend\static\js\optimizations\pagination.js" (
    echo   [OK] pagination.js
) else (
    echo   [ERROR] pagination.js no encontrado
)

if exist "frontend\static\js\optimizations\lazy-loading.js" (
    echo   [OK] lazy-loading.js
) else (
    echo   [ERROR] lazy-loading.js no encontrado
)

if exist "frontend\static\js\optimizations\advanced-search.js" (
    echo   [OK] advanced-search.js
) else (
    echo   [ERROR] advanced-search.js no encontrado
)

if exist "frontend\static\js\optimizations\table-sorting.js" (
    echo   [OK] table-sorting.js
) else (
    echo   [ERROR] table-sorting.js no encontrado
)

if exist "frontend\static\js\super-admin-dashboard-enhanced.js" (
    echo   [OK] super-admin-dashboard-enhanced.js
) else (
    echo   [ERROR] super-admin-dashboard-enhanced.js no encontrado
)

if exist "frontend\templates\admin\super-admin-dashboard.html" (
    echo   [OK] super-admin-dashboard.html
) else (
    echo   [ERROR] super-admin-dashboard.html no encontrado
)

echo.
echo [2/3] Iniciando servidor...
echo.
echo   Ejecuta: python run.py
echo   URL: http://localhost:5000
echo.

echo [3/3] Instrucciones de prueba:
echo.
echo   1. Abre http://localhost:5000 en tu navegador
echo   2. Login como super_admin
echo   3. Abre la consola del navegador (F12)
echo   4. Ejecuta: window.testOptimizations()
echo   5. Verifica que todas las pruebas pasen
echo.

echo ========================================
echo   Para iniciar el servidor:
echo   python run.py
echo ========================================
echo.

pause
