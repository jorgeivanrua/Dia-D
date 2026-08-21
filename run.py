# Punto de entrada para ejecuci�n directa de Flask (sin Docker)
import os
from backend.app import create_app

# Configurar entorno
env = os.getenv('FLASK_ENV', 'production')
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = env == 'development'
    print(f'Iniciando Dia-D en {env} mode, puerto {port}')
    app.run(host='0.0.0.0', port=port, debug=debug)