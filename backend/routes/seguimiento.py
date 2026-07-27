"""
Rutas para gestión de seguimiento de reportes
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.seguimiento import SeguimientoReporte
from backend.models.user import User
import logging

logger = logging.getLogger(__name__)

seguimiento_bp = Blueprint('seguimiento', __name__)


@seguimiento_bp.route('/api/seguimiento/<tipo_reporte>/<int:reporte_id>', methods=['GET'])
@jwt_required()
def obtener_seguimiento(tipo_reporte, reporte_id):
    """
    Obtener seguimiento de un reporte
    
    Args:
        tipo_reporte: 'incidente' o 'delito'
        reporte_id: ID del reporte
    """
    try:
        user_id = get_jwt_identity()
        
        # Validar tipo de reporte
        if tipo_reporte not in ['incidente', 'delito']:
            return jsonify({
                'success': False,
                'error': 'Tipo de reporte inválido'
            }), 400
        
        # TODO: Validar permisos del usuario para ver este reporte
        
        # Obtener seguimiento
        seguimientos = SeguimientoReporte.obtener_seguimiento(tipo_reporte, reporte_id)
        
        return jsonify({
            'success': True,
            'seguimientos': [s.to_dict() for s in seguimientos],
            'total': len(seguimientos)
        }), 200
        
    except Exception as e:
        logger.error(f'Error obteniendo seguimiento: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Error interno al obtener seguimiento'
        }), 500


@seguimiento_bp.route('/api/seguimiento', methods=['POST'])
@jwt_required()
def registrar_seguimiento():
    """
    Registrar una acción de seguimiento manualmente
    
    Body:
        - tipo_reporte: 'incidente' o 'delito'
        - reporte_id: ID del reporte
        - accion: Tipo de acción
        - comentario: Comentario (opcional)
        - metadatos: Metadatos adicionales (opcional)
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validar datos requeridos
        tipo_reporte = data.get('tipo_reporte')
        reporte_id = data.get('reporte_id')
        accion = data.get('accion')
        
        if not all([tipo_reporte, reporte_id, accion]):
            return jsonify({
                'success': False,
                'error': 'Faltan parámetros requeridos'
            }), 400
        
        if tipo_reporte not in ['incidente', 'delito']:
            return jsonify({
                'success': False,
                'error': 'Tipo de reporte inválido'
            }), 400
        
        # TODO: Validar permisos del usuario
        
        # Registrar seguimiento
        seguimiento = SeguimientoReporte.registrar_accion(
            tipo_reporte=tipo_reporte,
            reporte_id=reporte_id,
            accion=accion,
            usuario_id=user_id,
            comentario=data.get('comentario'),
            metadatos=data.get('metadatos'),
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        
        return jsonify({
            'success': True,
            'seguimiento': seguimiento.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f'Error registrando seguimiento: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Error interno al registrar seguimiento'
        }), 500
