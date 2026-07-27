#!/bin/bash
# Script para iniciar el servidor en Linux/Mac

echo "========================================"
echo "SISTEMA DE TESTIGOS ELECTORALES"
echo "Iniciando servidor..."
echo "========================================"
echo ""

# Verificar que el entorno virtual existe
if [ ! -d ".venv" ]; then
    echo "ERROR: Entorno virtual no encontrado"
    echo "Por favor ejecuta primero: ./setup.sh"
    exit 1
fi

# Activar entorno virtual
source .venv/bin/activate

# Verificar que la BD existe
if [ ! -f "instance/electoral.db" ]; then
    echo ""
    echo "ADVERTENCIA: Base de datos no encontrada"
    echo "Ejecutando inicialización automática..."
    echo ""
    python scripts/init_system.py
    echo ""
fi

# Iniciar servidor
echo ""
echo "Iniciando servidor Flask..."
echo "La aplicación estará disponible en: http://localhost:5000"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""
python run.py
