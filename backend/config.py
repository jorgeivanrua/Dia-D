"""
Configuración de la aplicación
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración base"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    
    # Database
    database_url = os.getenv('DATABASE_URL', 'sqlite:///instance/electoral.db')
    if database_url.startswith('sqlite:///'):
        sqlite_path = database_url.replace('sqlite:///', '', 1)
        if not os.path.isabs(sqlite_path):
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            abs_path = os.path.abspath(os.path.join(project_root, sqlite_path))
            database_url = 'sqlite:///' + abs_path.replace('\\', '/')
    # Render usa postgres:// pero SQLAlchemy necesita postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # Upload (local by default; can use S3/MinIO)
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 5 * 1024 * 1024))  # bytes
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,pdf').split(','))

    # S3 / MinIO settings (optional)
    S3_ENABLED = os.getenv('S3_ENABLED', 'False') == 'True'
    S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL', '')  # e.g. http://minio:9000
    S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY', '')
    S3_SECRET_KEY = os.getenv('S3_SECRET_KEY', '')
    S3_REGION = os.getenv('S3_REGION', 'us-east-1')
    S3_BUCKET = os.getenv('S3_BUCKET', 'electoral-evidencias')
    S3_USE_SSL = os.getenv('S3_USE_SSL', 'False') == 'True'

    # Chroma (vector DB) settings
    CHROMA_ENABLED = os.getenv('CHROMA_ENABLED', 'False') == 'True'
    CHROMA_PERSIST_DIR = os.getenv('CHROMA_PERSIST_DIR', 'chroma_db')
    CHROMA_SERVER_HOST = os.getenv('CHROMA_SERVER_HOST', '')  # optional chroma server host
    CHROMA_SERVER_PORT = int(os.getenv('CHROMA_SERVER_PORT', 8000))

    # Pagination
    ITEMS_PER_PAGE = 20
    MAX_ITEMS_PER_PAGE = 100

    # SocketIO / Redis
    SOCKETIO_MESSAGE_QUEUE = os.getenv('REDIS_URL', None)  # None para desarrollo sin Redis
    SOCKETIO_ASYNC_MODE = 'threading'


class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Configuración de producción"""
    DEBUG = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """Configuración de testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
