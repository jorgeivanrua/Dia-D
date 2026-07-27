# Simple Dockerfile for the Flask app
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y build-essential gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

ENV FLASK_ENV=production
ENV PORT=5000

CMD ["python", "run.py"]
