@echo off
REM ============================================================================
REM INICIALIZACIÓN AUTOMÁTICA DE DATOS
REM ============================================================================

echo.
echo ========================================================================
echo INICIALIZACION AUTOMATICA DE DATOS
echo ========================================================================
echo.

REM Activar entorno virtual si existe
if exist ".venv\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call .venv\Scripts\activate.bat
)

echo.
echo Ejecutando inicializacion automatica...
python scripts\inicializar_datos_automatico.py

echo.
echo ========================================================================
echo INICIALIZACION COMPLETADA
echo ========================================================================
echo.
echo Para verificar los datos:
echo   python scripts\verificar_y_cargar_datos_completo.py
echo.
echo Para iniciar el servidor:
echo   python run.py
echo.
pause
