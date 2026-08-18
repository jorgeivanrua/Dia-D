@echo off
echo ============================================================
echo SCRIPT DE CONFIGURACION - USUARIO DE MONITOREO
echo ============================================================
echo.

REM Activar entorno virtual
if exist .venv\Scripts\activate.bat (
    echo Activando entorno virtual...
    call .venv\Scripts\activate.bat
) else (
    echo ERROR: No se encontro el entorno virtual en .venv
    echo Por favor ejecute setup.bat primero
    pause
    exit /b 1
)

REM Ejecutar script de Python
echo.
echo Ejecutando script de configuracion...
python backend\scripts\crear_usuario_monitoreo.py

REM Mantener ventana abierta
echo.
pause
