"""
Endpoint de healthcheck para monitoreo
"""
from flask import Blueprint, jsonify
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.models.configuracion_electoral import TipoEleccion
from backend.models.partido_politico import PartidoPolitico as Partido
from datetime import datetime
import os

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de healthcheck
    Retorna el estado del sistema y estadísticas básicas
    """
    try:
        # Verificar conexión a BD
        db.session.execute(db.text('SELECT 1'))
        db_status = 'connected'
        
        # Obtener estadísticas
        users_count = User.query.count()
        locations_count = Location.query.count()
        tipos_eleccion_count = TipoEleccion.query.count()
        partidos_count = Partido.query.count()
        
        # Información del sistema
        system_info = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.1.0',
            'environment': os.getenv('FLASK_ENV', 'development'),
            'database': {
                'status': db_status,
                'type': 'sqlite' if 'sqlite' in str(db.engine.url) else 'postgresql'
            },
            'statistics': {
                'users': users_count,
                'locations': locations_count,
                'tipos_eleccion': tipos_eleccion_count,
                'partidos': partidos_count
            }
        }
        
        return jsonify(system_info), 200
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e),
            'database': {
                'status': 'disconnected'
            }
        }), 503


@health_bp.route('/health/ready', methods=['GET'])
def readiness_check():
    """
    Endpoint de readiness para Kubernetes/Docker
    Verifica que el sistema esté listo para recibir tráfico
    """
    try:
        # Verificar BD
        db.session.execute(db.text('SELECT 1'))
        
        # Verificar que hay usuarios básicos
        users_count = User.query.count()
        if users_count == 0:
            return jsonify({
                'ready': False,
                'reason': 'No users in database'
            }), 503
        
        return jsonify({
            'ready': True,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'ready': False,
            'reason': str(e)
        }), 503


@health_bp.route('/health/live', methods=['GET'])
def liveness_check():
    """
    Endpoint de liveness para Kubernetes/Docker
    Verifica que la aplicación esté viva
    """
    return jsonify({
        'alive': True,
        'timestamp': datetime.utcnow().isoformat()
    }), 200
