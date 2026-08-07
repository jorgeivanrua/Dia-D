# Dockerfile para la aplicación Flask
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias primero para cachear mejor la build
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el resto del proyecto
COPY . .
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 5000

ENV FLASK_ENV=production \
    PORT=5000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
