#!/bin/sh
set -e

echo "=== INICIANDO INICIALIZACIÓN DE BD ==="
python /app/backend/database.py

echo "=== INICIANDO GUNICORN ==="
exec gunicorn \
  --bind 0.0.0.0:${PORT:-5000} \
  --workers 1 \
  --worker-class sync \
  --worker-tmp-dir /dev/shm \
  --access-logfile - \
  --error-logfile - \
  --log-level info \
  --timeout 120 \
  run:app
