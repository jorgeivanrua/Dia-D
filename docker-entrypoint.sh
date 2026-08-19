#!/bin/sh
set -eu

DB_HOST=${DB_HOST:-postgres}
DB_PORT=${DB_PORT:-5432}

printf 'Esperando PostgreSQL en %s:%s...\n' "$DB_HOST" "$DB_PORT"
until python - <<'PY'
import os
import socket
import sys

host = os.getenv('DB_HOST', 'postgres')
port = int(os.getenv('DB_PORT', '5432'))

sock = socket.socket()
sock.settimeout(2)
try:
    sock.connect((host, port))
except OSError:
    sys.exit(1)
finally:
    sock.close()
PY

do
  sleep 2
done

printf 'PostgreSQL listo. Iniciando aplicación...\n'
exec gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 1 run:app
