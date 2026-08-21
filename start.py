#!/usr/bin/env python3
# Script de inicio para RenderHeroku/Python
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

from backend.app import create_app

app = create_env = os.getenv('FLASK_ENV', 'production')
app = create_app()

if __name__ == 'main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)