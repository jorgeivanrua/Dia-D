#!/bin/bash
# Script de inicialización para Linux/Mac

echo "========================================"
echo "SISTEMA DE TESTIGOS ELECTORALES"
echo "Inicialización Completa"
echo "========================================"
echo ""

# Verificar que Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 no está instalado"
    echo "Por favor instala Python 3.8 o superior"
    exit 1
fi

echo "[1/3] Verificando entorno virtual..."
if [ ! -d ".venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv .venv
    echo "Entorno virtual creado"
else
    echo "Entorno virtual ya existe"
fi

echo ""
echo "[2/3] Activando entorno virtual e instalando dependencias..."
source .venv/bin/activate
pip install -r requirements.txt

echo ""
echo "[3/3] Ejecutando script de inicialización..."
python setup.py

echo ""
echo "========================================"
echo "INICIALIZACIÓN COMPLETADA"
echo "========================================"
echo ""
echo "Para iniciar el servidor, ejecuta:"
echo "  ./start.sh"
echo ""
