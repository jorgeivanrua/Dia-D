"""
Aplicación principal Flask
OPTIMIZADO para múltiples usuarios simultáneos
"""
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_compress import Compress
# from flask_socketio import SocketIO  # Comentado temporalmente - instalar con: pip install flask-socketio
from whitenoise import WhiteNoise
# Flasgger for API documentation
from flasgger import Swagger

from backend.config import config
from backend.database import init_db
from backend.utils.jwt_callbacks import configure_jwt_callbacks
from backend.utils.logging_config import setup_logging

# Inicializar extensiones
jwt = JWTManager()
compress = Compress()
# socketio = SocketIO()  # Comentado temporalmente
socketio = None  # Placeholder


def create_app(config_name='default'):
    """
    Factory para crear la aplicación Flask
    
    Args:
        config_name: Nombre de la configuración a usar
        
    Returns:
        Flask app configurada
    """
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Configurar logging
    setup_logging(app)
    
    # Inicializar extensiones
    init_db(app)
    jwt.init_app(app)
    configure_jwt_callbacks(jwt)
    CORS(app, resources={r"/*": {"origins": "*"}})
    compress.init_app(app)  # Compresión GZIP para respuestas
    
    # Configurar SocketIO (comentado temporalmente)
    if socketio:
        socketio.init_app(
            app,
            cors_allowed_origins="*",
            async_mode='threading',
            message_queue=app.config.get('SOCKETIO_MESSAGE_QUEUE'),
            logger=app.debug,
            engineio_logger=app.debug
        )
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Registrar manejadores de errores
    register_error_handlers(app)
    
    # Registrar event handlers de SocketIO
    with app.app_context():
        from backend.services import websocket_service  # Importar para registrar handlers
    
# Configurar WhiteNoise para servir archivos estáticos en producción
    if not app.debug:
        app.wsgi_app = WhiteNoise(
            app.wsgi_app,
            root='frontend/static',
            prefix='static/',
            max_age=31536000 if not app.debug else 0
        )

    # Configurar Flasgger para documentación de API
    app.config['SWAGGER'] = {
        'title': 'Dia-D API',
        'uiversion': 3,
        'openapi': '3.0.2',
        'description': 'API para el sistema de gestión electoral Dia-D',
        'version': '1.0.0',
        'termsOfService': '',
        'contact': {
            'name': 'Dia-D Support',
            'url': 'https://dia-d.example.com/support',
            'email': 'support@dia-d.example.com'
        },
        'license': {
            'name': 'MIT',
            'url': 'https://opensource.org/licenses/MIT'
        },
        'schemes': [
            'http',
            'https'
        ],
        'specs': [
            {
                'endpoint': 'apispec',
                'route': '/apispec.json',
                'rule_filter': lambda rule: True,  # all in
                'definition': {
                    'security': [{}]
                }
            }
        ],
        'security_definitions': {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': 'JWT Authorization header usando el esquema: Bearer <token>'
            }
        },
        'security': [
            {
                'Bearer': []
            }
        ],
        'specs_route': '/api/docs/'
    }
    swagger = Swagger(app)

    # Inicializar usuarios básicos automáticamente
    with app.app_context():
        try:
            from backend.utils.init_usuarios_basicos import init_usuarios_basicos
            init_usuarios_basicos()
        except Exception as e:
            app.logger.warning(f'No se pudieron inicializar usuarios básicos: {str(e)}')
    
    return app


def register_blueprints(app):
    """Registrar blueprints de rutas"""
    from backend.routes.auth import auth_bp
    from backend.routes.locations import locations_bp
    from backend.routes.frontend import frontend_bp
    from backend.routes.configuracion import configuracion_bp
    from backend.routes.formularios_e14 import formularios_bp
    from backend.routes.coordinador_municipal import coordinador_municipal_bp
    from backend.routes.coordinador_departamental import bp as coordinador_departamental_bp
    from backend.routes.incidentes_delitos import incidentes_delitos_bp
    from backend.routes.super_admin import super_admin_bp
    from backend.routes.testigo import testigo_bp
    from backend.routes.coordinador_puesto import coordinador_puesto_bp
    from backend.routes.admin import admin_bp
    from backend.routes.admin_municipal import admin_municipal_bp
    from backend.routes.auditor import auditor_bp
    from backend.routes.gestion_usuarios import gestion_usuarios_bp
    from backend.routes.admin_tools import admin_tools_bp
    from backend.routes.admin_data_import import admin_import_bp
    from backend.routes.verificacion_presencia import verificacion_bp
    from backend.routes.locations_geo import locations_geo_bp
    from backend.routes.configuracion_sistema import configuracion_sistema_bp
    from backend.routes.monitoreo import monitoreo_bp
    from backend.routes.cargar_logos import cargar_logos_bp
    from backend.routes.notificaciones import notificaciones_bp
    from backend.routes.evidencia import evidencia_bp
    from backend.routes.seguimiento import seguimiento_bp
    from backend.routes.partidos import partidos_bp
    from backend.routes.candidatos import candidatos_bp
    from backend.routes.database_backup import database_backup_bp
    
    # API routes
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(locations_bp, url_prefix='/api/locations')
    app.register_blueprint(locations_geo_bp)
    app.register_blueprint(configuracion_bp, url_prefix='/api/configuracion')
    app.register_blueprint(configuracion_sistema_bp)  # Configuración del sistema
    app.register_blueprint(formularios_bp)
    app.register_blueprint(coordinador_municipal_bp)
    app.register_blueprint(coordinador_departamental_bp)
    app.register_blueprint(incidentes_delitos_bp)
    app.register_blueprint(super_admin_bp)
    app.register_blueprint(testigo_bp, url_prefix='/api/testigo')
    app.register_blueprint(coordinador_puesto_bp, url_prefix='/api/coordinador-puesto')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(admin_municipal_bp, url_prefix='/api/admin-municipal')
    app.register_blueprint(auditor_bp, url_prefix='/api/auditor')
    app.register_blueprint(gestion_usuarios_bp)
    app.register_blueprint(admin_tools_bp)
    app.register_blueprint(admin_import_bp)
    app.register_blueprint(verificacion_bp)
    app.register_blueprint(monitoreo_bp)
    app.register_blueprint(cargar_logos_bp)
    app.register_blueprint(notificaciones_bp)
    app.register_blueprint(evidencia_bp)
    app.register_blueprint(seguimiento_bp)
    app.register_blueprint(partidos_bp)  # Gestión de partidos políticos
    app.register_blueprint(candidatos_bp)  # Gestión de candidatos
    app.register_blueprint(database_backup_bp, url_prefix='/api/database')  # Backup y restauración
    
    # Public routes (sin autenticación)
    from backend.routes.public import public_bp
    app.register_blueprint(public_bp)
    
    # Init DB route (para inicializar BD en producción sin Pre-Deploy Command)
    from backend.routes.init_db_route import init_db_bp
    app.register_blueprint(init_db_bp)
    
    # Emergency routes (para resetear contraseñas sin shell access)
    from backend.routes.emergency_reset import emergency_bp
    app.register_blueprint(emergency_bp, url_prefix='/api/emergency')
    
    # Health check routes
    from backend.routes.health import health_bp
    app.register_blueprint(health_bp)
    
    # Frontend routes
    app.register_blueprint(frontend_bp)


def register_error_handlers(app):
    """Registrar manejadores de errores"""
    from backend.utils.exceptions import BaseAPIException
    
    @app.errorhandler(BaseAPIException)
    def handle_api_exception(error):
        """Manejar excepciones personalizadas de la API"""
        response = error.to_dict()
        return response, error.status_code
    
    @app.errorhandler(404)
    def not_found(error):
        return {'success': False, 'error': 'Recurso no encontrado'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Error interno: {error}')
        return {'success': False, 'error': 'Error interno del servidor'}, 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return {'success': False, 'error': 'Petición inválida'}, 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return {'success': False, 'error': 'No autorizado'}, 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return {'success': False, 'error': 'Acceso prohibido'}, 403
