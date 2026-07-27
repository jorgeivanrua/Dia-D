"""
Configuración centralizada de logging
"""
import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(app):
    """
    Configurar sistema de logging para la aplicación
    
    Args:
        app: Instancia de Flask
    """
    # Nivel de logging según entorno
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    # Formato de logs
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_handler.setFormatter(formatter)
    
    # Handler para archivo (solo en producción)
    if not app.debug:
        # Crear directorio de logs si no existe
        logs_dir = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        # Archivo de logs con rotación
        file_handler = RotatingFileHandler(
            os.path.join(logs_dir, 'app.log'),
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        
        app.logger.addHandler(file_handler)
    
    # Agregar handler de consola
    app.logger.addHandler(console_handler)
    app.logger.setLevel(getattr(logging, log_level))
    
    # Configurar loggers de bibliotecas externas
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    
    app.logger.info(f'Logging configurado - Nivel: {log_level}')


def get_logger(name):
    """
    Obtener logger configurado para un módulo
    
    Args:
        name: Nombre del módulo
        
    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Configurar handler si no existe
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(name)s: %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Nivel según variable de entorno
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        logger.setLevel(getattr(logging, log_level))
    
    return logger
