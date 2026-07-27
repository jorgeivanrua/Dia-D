"""
Rutas públicas (sin autenticación)
"""
from flask import Blueprint, jsonify, request
from backend.models.configuracion_electoral import Campana
from backend.database import db
import os

public_bp = Blueprint('public', __name__, url_prefix='/api/public')


@public_bp.route('/campaign-info', methods=['GET'])
def get_campaign_info():
    """
    Obtener información de la campaña activa (público)
    """
    try:
        # Buscar campaña activa
        campana = Campana.query.filter_by(activa=True).first()
        
        if not campana:
            # Si no hay campaña activa, usar valores por defecto
            return jsonify({
                'success': True,
                'data': {
                    'nombre': 'Sistema Electoral',
                    'descripcion': 'Recolección de Datos Electorales',
                    'color_primario': '#1e3c72',
                    'color_secundario': '#2a5298'
                },
                'testing_mode': os.getenv('TESTING_MODE', 'false').lower() == 'true'
            }), 200
        
        return jsonify({
            'success': True,
            'data': campana.to_dict(),
            'testing_mode': os.getenv('TESTING_MODE', 'false').lower() == 'true'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@public_bp.route('/test-users', methods=['GET'])
def get_test_users():
    """
    Obtener lista de usuarios de prueba (solo en modo testing)
    """
    try:
        # Solo disponible en modo testing
        if os.getenv('TESTING_MODE', 'false').lower() != 'true':
            return jsonify({
                'success': False,
                'error': 'Endpoint solo disponible en modo testing'
            }), 403
        
        from backend.models.user import User
        
        # Obtener usuarios de prueba (que terminan en _test)
        test_users = User.query.filter(
            User.nombre.like('%_test%')
        ).all()
        
        users_by_role = {}
        for user in test_users:
            if user.rol not in users_by_role:
                users_by_role[user.rol] = []
            users_by_role[user.rol].append({
                'nombre': user.nombre,
                'password': 'test123',  # Contraseña conocida para testing
                'ubicacion': user.ubicacion.nombre if user.ubicacion else None
            })
        
        return jsonify({
            'success': True,
            'data': users_by_role
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
