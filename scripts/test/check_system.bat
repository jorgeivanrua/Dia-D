@echo off
echo ========================================
echo DIAGNOSTICO RAPIDO DEL SISTEMA
echo ========================================
echo.

echo [1] Verificando Python...
python --version
if errorlevel 1 (
    echo ERROR: Python no encontrado
    goto :end
)
echo.

echo [2] Verificando estructura...
if exist "backend" (
    echo OK: Directorio backend existe
) else (
    echo ERROR: Directorio backend no encontrado
)

if exist "frontend" (
    echo OK: Directorio frontend existe
) else (
    echo ERROR: Directorio frontend no encontrado
)

if exist "scripts" (
    echo OK: Directorio scripts existe
) else (
    echo ERROR: Directorio scripts no encontrado
)
echo.

echo [3] Verificando archivos principales...
if exist "run.py" (
    echo OK: run.py existe
) else (
    echo ERROR: run.py no encontrado
)

if exist "setup.py" (
    echo OK: setup.py existe
) else (
    echo ERROR: setup.py no encontrado
)

if exist "requirements.txt" (
    echo OK: requirements.txt existe
) else (
    echo ERROR: requirements.txt no encontrado
)
echo.

echo [4] Verificando entorno virtual...
if exist ".venv" (
    echo OK: Directorio .venv existe
    if exist ".venv\Scripts\python.exe" (
        echo OK: Python en entorno virtual existe
    ) else (
        echo ERROR: Entorno virtual corrupto o incompleto
        echo SOLUCION: Elimina .venv y ejecuta setup.bat
    )
) else (
    echo ADVERTENCIA: Entorno virtual no existe
    echo SOLUCION: Ejecuta setup.bat
)
echo.

echo [5] Verificando base de datos...
if exist "instance\testigos.db" (
    echo OK: Base de datos existe
) else (
    echo ADVERTENCIA: Base de datos no existe
    echo SOLUCION: Ejecuta setup.bat o python setup.py
)
echo.

echo [6] Verificando archivo DIVIPOLA...
if exist "todos los datos\divipola.csv" (
    echo OK: divipola.csv encontrado
) else if exist "divipola.csv" (
    echo OK: divipola.csv encontrado
) else (
    echo ADVERTENCIA: divipola.csv no encontrado
    echo El sistema funcionara pero sin ubicaciones
)
echo.

echo ========================================
echo RECOMENDACIONES
echo ========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo 1. El entorno virtual esta corrupto
    echo    Ejecuta: rmdir /s /q .venv
    echo    Luego: setup.bat
    echo.
)

if not exist "instance\testigos.db" (
    echo 2. La base de datos no existe
    echo    Ejecuta: setup.bat
    echo.
)

echo Para inicializar el sistema completo:
echo   setup.bat
echo.
echo Para iniciar el servidor:
echo   start.bat
echo.

:end
pause
