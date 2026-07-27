@echo off
REM ============================================================================
REM INSTALACIÓN COMPLETA DEL SISTEMA DE MONITOREO
REM ============================================================================
REM Fecha: 28 de Noviembre de 2025
REM Propósito: Instalar y configurar todo el sistema de monitoreo
REM ============================================================================

echo.
echo ========================================================================
echo INSTALACION COMPLETA DEL SISTEMA DE MONITOREO
echo ========================================================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "backend" (
    echo ERROR: No se encuentra el directorio backend
    echo Por favor ejecuta este script desde la raiz del proyecto
    pause
    exit /b 1
)

echo [1/6] Verificando entorno virtual...
if not exist ".venv" (
    echo Creando entorno virtual...
    python -m venv .venv
)

echo.
echo [2/6] Activando entorno virtual...
call .venv\Scripts\activate.bat

echo.
echo [3/6] Instalando dependencias...
pip install -r requirements.txt

echo.
echo [4/6] Aplicando indices de optimizacion a la base de datos...
python scripts\aplicar_indices.py

echo.
echo [5/6] Verificando conexiones a la base de datos...
python scripts\verificar_monitoreo.py

echo.
echo [6/6] Verificando usuario de monitoreo...
python scripts\check_monitoreo_user.py

echo.
echo ========================================================================
echo INSTALACION COMPLETADA
echo ========================================================================
echo.
echo El sistema de monitoreo esta listo para usar:
echo.
echo 1. Iniciar servidor: python run.py
echo 2. Acceder a: http://localhost:5000/monitoreo/dashboard
echo 3. Login: monitoreo / Monitoreo2025!
echo.
echo Documentacion disponible en:
echo - docs/GUIA_COMPLETA_MONITOREO.md
echo - docs/VERIFICACION_MONITOREO_BD.md
echo - docs/ROL_MONITOREO_MEJORADO.md
echo.
echo ========================================================================
echo.
pause
