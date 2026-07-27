"""
Rutas para gestión de evidencia fotográfica
"""
from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.upload_service import UploadService
from backend.models.incidentes_delitos import EvidenciaFotografica
from backend.models.user import User
import logging
import os

logger = logging.getLogger(__name__)

evidencia_bp = Blueprint('evidencia', __name__)


@evidencia_bp.route('/api/evidencia/upload', methods=['POST'])
@jwt_required()
def upload_evidencia():
    """
    Upload de evidencia fotográfica
    
    Form data:
        - file: Archivo de imagen
        - tipo_reporte: 'incidente' o 'delito'
        - reporte_id: ID del reporte
    """
    try:
        user_id = get_jwt_identity()
        
        # Validar que hay archivo
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó archivo'
            }), 400
        
        file = request.files['file']
        tipo_reporte = request.form.get('tipo_reporte')
        reporte_id = request.form.get('reporte_id')
        
        # Validar parámetros
        if not tipo_reporte or not reporte_id:
            return jsonify({
                'success': False,
                'error': 'Faltan parámetros requeridos'
            }), 400
        
        try:
            reporte_id = int(reporte_id)
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'reporte_id debe ser un número'
            }), 400
        
        # TODO: Validar permisos del usuario para subir evidencia a este reporte
        # Por ahora permitimos a cualquier usuario autenticado
        
        # Upload
        result = UploadService.upload_evidencia(file, tipo_reporte, reporte_id, user_id)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        logger.error(f'Error en upload de evidencia: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Error interno al subir evidencia'
        }), 500


@evidencia_bp.route('/api/evidencia/<filename>', methods=['GET'])
@jwt_required()
def get_evidencia(filename):
    """
    Obtener archivo de evidencia
    
    Args:
        filename: Nombre del archivo
    """
    try:
        user_id = get_jwt_identity()
        
        # Buscar evidencia en base de datos
        evidencia = EvidenciaFotografica.query.filter_by(filename=filename).first()
        
        if not evidencia:
            return jsonify({
                'success': False,
                'error': 'Evidencia no encontrada'
            }), 404
        
        # TODO: Validar permisos del usuario para acceder a esta evidencia
        # Por ahora permitimos a cualquier usuario autenticado
        
        # Obtener ruta del archivo
        file_path = UploadService.get_evidencia_path(filename)
        
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': 'Archivo no encontrado en el servidor'
            }), 404
        
        # Servir archivo
        return send_file(
            file_path,
            mimetype=evidencia.mime_type,
            as_attachment=False,
            download_name=evidencia.filename_original
        )
        
    except Exception as e:
        logger.error(f'Error sirviendo evidencia: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Error interno al obtener evidencia'
        }), 500


@evidencia_bp.route('/api/evidencia/<int:evidencia_id>', methods=['DELETE'])
@jwt_required()
def delete_evidencia(evidencia_id):
    """
    Eliminar evidencia fotográfica
    
    Args:
        evidencia_id: ID de la evidencia
    """
    try:
        user_id = get_jwt_identity()
        
        # Buscar evidencia
        evidencia = EvidenciaFotografica.query.get(evidencia_id)
        
        if not evidencia:
            return jsonify({
                'success': False,
                'error': 'Evidencia no encontrada'
            }), 404
        
        # Validar permisos: solo el que subió o admin puede eliminar
        user = User.query.get(user_id)
        if evidencia.subido_por_id != user_id and user.rol not in ['super_admin', 'auditor']:
            return jsonify({
                'success': False,
                'error': 'No tiene permisos para eliminar esta evidencia'
            }), 403
        
        # Eliminar
        success = UploadService.delete_evidencia(evidencia_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Evidencia eliminada exitosamente'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Error al eliminar evidencia'
            }), 500
            
    except Exception as e:
        logger.error(f'Error eliminando evidencia: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Error interno al eliminar evidencia'
        }), 500


@evidencia_bp.route('/api/evidencia/reporte/<tipo_reporte>/<int:reporte_id>', methods=['GET'])
@jwt_required()
def get_evidencias_reporte(tipo_reporte, reporte_id):
    """
    Obtener todas las evidencias de un reporte
    
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
        
        # Buscar evidencias
        if tipo_reporte == 'incidente':
            evidencias = EvidenciaFotografica.query.filter_by(incidente_id=reporte_id).all()
        else:
            evidencias = EvidenciaFotografica.query.filter_by(delito_id=reporte_id).all()
        
        # TODO: Validar permisos del usuario para ver este reporte
        
        # Convertir a diccionario
        evidencias_data = []
        for ev in evidencias:
            evidencias_data.append({
                'id': ev.id,
                'filename': ev.filename,
                'filename_original': ev.filename_original,
                'url': ev.url,
                'mime_type': ev.mime_type,
                'size_bytes': ev.size_bytes,
                'width': ev.width,
                'height': ev.height,
                'latitud': ev.latitud,
                'longitud': ev.longitud,
                'fecha_captura': ev.fecha_captura.isoformat() if ev.fecha_captura else None,
                'dispositivo': ev.dispositivo,
                'subido_por_id': ev.subido_por_id,
                'fecha_subida': ev.fecha_subida.isoformat()
            })
        
        return jsonify({
            'success': True,
            'evidencias': evidencias_data,
            'total': len(evidencias_data)
        }), 200
        
    except Exception as e:
        logger.error(f'Error obteniendo evidencias: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Error interno al obtener evidencias'
        }), 500
