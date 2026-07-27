@echo off
REM Script de inicialización para Windows
echo ========================================
echo SISTEMA DE TESTIGOS ELECTORALES
echo Inicializacion Completa
echo ========================================
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.8 o superior
    pause
    exit /b 1
)

echo [1/3] Verificando entorno virtual...
if not exist ".venv" (
    echo Creando entorno virtual...
    python -m venv .venv
    echo Entorno virtual creado
) else (
    echo Entorno virtual ya existe
)

echo.
echo [2/3] Activando entorno virtual e instalando dependencias...
call .venv\Scripts\activate.bat
pip install -r requirements.txt

echo.
echo [3/3] Ejecutando script de inicializacion...
python setup.py

echo.
echo ========================================
echo INICIALIZACION COMPLETADA
echo ========================================
echo.
echo Para iniciar el servidor, ejecuta:
echo   start.bat
echo.
pause
