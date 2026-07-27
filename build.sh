#!/usr/bin/env bash
# Script de build para Render

set -o errexit

echo "🔧 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🗄️ Inicializando base de datos..."
python scripts/init_db.py

echo "🔄 Ejecutando migraciones..."
python backend/migrations/add_es_usuario_basico.py

echo "📍 Cargando ubicaciones..."
python scripts/load_divipola.py

echo "👥 Creando/actualizando usuarios del sistema (básicos + testigos)..."
python scripts/fix_usuarios_completo.py

echo "⚙️ Configurando sistema electoral..."
python scripts/init_configuracion_electoral.py

echo "📋 Creando tablas de formularios..."
python scripts/create_formularios_e14_tables.py

echo "✅ Build completado exitosamente"
