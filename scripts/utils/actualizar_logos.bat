@echo off
echo Activando entorno virtual...
call .venv\Scripts\activate.bat

echo.
echo Ejecutando script de actualizacion de logos...
python actualizar_logos_partidos.py

echo.
echo Presiona cualquier tecla para salir...
pause > nul
