#!/bin/bash
# Script de inicio para Render
# Maneja la variable PORT correctamente

# Obtener el puerto de la variable de entorno o usar 10000 por defecto
PORT=${PORT:-10000}

echo "Iniciando servidor en puerto $PORT"

# Iniciar gunicorn con el puerto correcto
gunicorn run:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
