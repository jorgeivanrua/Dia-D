@echo off
REM Script para iniciar el servidor en Windows
echo ========================================
echo SISTEMA DE TESTIGOS ELECTORALES
echo Iniciando servidor...
echo ========================================
echo.

REM Verificar que el entorno virtual existe
if not exist ".venv" (
    echo ERROR: Entorno virtual no encontrado
    echo Por favor ejecuta primero: setup.bat
    pause
    exit /b 1
)

REM Activar entorno virtual
call .venv\Scripts\activate.bat

REM Verificar que la BD existe
if not exist "instance\electoral.db" (
    echo.
    echo ADVERTENCIA: Base de datos no encontrada
    echo Ejecutando inicializacion automatica...
    echo.
    python scripts\init_system.py
    echo.
)

REM Iniciar servidor
echo.
echo Iniciando servidor Flask...
echo La aplicacion estara disponible en: http://localhost:5000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.
python run.py
