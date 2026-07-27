"""
Rutas para gestión de notificaciones
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.notificacion_service import NotificacionService
from backend.models.user import User
import logging

logger = logging.getLogger(__name__)

notificaciones_bp = Blueprint('notificaciones', __name__)


@notificaciones_bp.route('/api/notificaciones', methods=['GET'])
@jwt_required()
def obtener_notificaciones():
    """
    Obtener notificaciones del usuario actual
    
    Query params:
        - solo_no_leidas: bool (opcional)
        - limit: int (opcional, default 50)
        - offset: int (opcional, default 0)
    """
    try:
        user_id = get_jwt_identity()
        
        # Obtener parámetros
        solo_no_leidas = request.args.get('solo_no_leidas', 'false').lower() == 'true'
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        # Validar límites
        if limit > 100:
            limit = 100
        if limit < 1:
            limit = 50
        
        # Obtener notificaciones
        notificaciones = NotificacionService.obtener_notificaciones(
            user_id,
            solo_no_leidas=solo_no_leidas,
            limit=limit,
            offset=offset
        )
        
        # Obtener contador de no leídas
        no_leidas = NotificacionService.contar_no_leidas(user_id)
        
        return jsonify({
            'success': True,
            'notificaciones': [n.to_dict() for n in notificaciones],
            'no_leidas': no_leidas,
            'total': len(notificaciones)
        }), 200
        
    except Exception as e:
        logger.error(f'Error obteniendo notificaciones: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Error obteniendo notificaciones'
        }), 500


@notificaciones_bp.route('/api/notificaciones/<int:notificacion_id>/leer', methods=['POST'])
@jwt_required()
def marcar_leida(notificacion_id):
    """
    Marcar notificación como leída
    """
    try:
        user_id = get_jwt_identity()
        
        # Marcar como leída
        success = NotificacionService.marcar_leida(notificacion_id, user_id)
        
        if success:
            # Obtener contador actualizado
            no_leidas = NotificacionService.contar_no_leidas(user_id)
            
            return jsonify({
                'success': True,
                'no_leidas': no_leidas
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Notificación no encontrada o sin permisos'
            }), 404
            
    except Exception as e:
        logger.error(f'Error marcando notificación como leída: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Error marcando notificación'
        }), 500


@notificaciones_bp.route('/api/notificaciones/marcar-todas-leidas', methods=['POST'])
@jwt_required()
def marcar_todas_leidas():
    """
    Marcar todas las notificaciones como leídas
    """
    try:
        user_id = get_jwt_identity()
        
        # Obtener todas las no leídas
        notificaciones = NotificacionService.obtener_notificaciones(
            user_id,
            solo_no_leidas=True,
            limit=1000
        )
        
        # Marcar cada una como leída
        count = 0
        for notif in notificaciones:
            if NotificacionService.marcar_leida(notif.id, user_id):
                count += 1
        
        return jsonify({
            'success': True,
            'marcadas': count
        }), 200
        
    except Exception as e:
        logger.error(f'Error marcando todas como leídas: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Error marcando notificaciones'
        }), 500


@notificaciones_bp.route('/api/notificaciones/contador', methods=['GET'])
@jwt_required()
def obtener_contador():
    """
    Obtener solo el contador de notificaciones no leídas
    """
    try:
        user_id = get_jwt_identity()
        no_leidas = NotificacionService.contar_no_leidas(user_id)
        
        return jsonify({
            'success': True,
            'no_leidas': no_leidas
        }), 200
        
    except Exception as e:
        logger.error(f'Error obteniendo contador: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Error obteniendo contador'
        }), 500
