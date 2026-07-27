"""Rutas para incidentes y delitos electorales"""

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.incidentes_delitos_service import IncidentesDelitosService
from backend.services.upload_service import UploadService
from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral, EvidenciaFotografica
from backend.models.user import User
import os

incidentes_delitos_bp = Blueprint('incidentes_delitos', __name__)


@incidentes_delitos_bp.route('/api/incidentes', methods=['POST'])
@jwt_required()
def crear_incidente():
    """Crear un nuevo incidente electoral"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user:
            return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('tipo_incidente'):
            return jsonify({'success': False, 'error': 'Tipo de incidente es requerido'}), 400
        if not data.get('titulo'):
            return jsonify({'success': False, 'error': 'Título es requerido'}), 400
        if not data.get('descripcion'):
            return jsonify({'success': False, 'error': 'Descripción es requerida'}), 400
        
        incidente = IncidentesDelitosService.crear_incidente(data, current_user.id)
        
        return jsonify({
            'success': True,
            'message': 'Incidente creado exitosamente',
            'data': incidente.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/incidentes', methods=['GET'])
@jwt_required()
def obtener_incidentes():
    """Obtener incidentes según permisos del usuario"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user:
            return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404
        
        # Obtener filtros de query params
        filtros = {}
        if request.args.get('estado'):
            filtros['estado'] = request.args.get('estado')
        if request.args.get('severidad'):
            filtros['severidad'] = request.args.get('severidad')
        if request.args.get('tipo_incidente'):
            filtros['tipo_incidente'] = request.args.get('tipo_incidente')
        if request.args.get('fecha_desde'):
            filtros['fecha_desde'] = request.args.get('fecha_desde')
        if request.args.get('fecha_hasta'):
            filtros['fecha_hasta'] = request.args.get('fecha_hasta')
        if request.args.get('mesa_id'):
            filtros['mesa_id'] = request.args.get('mesa_id')
        
        incidentes = IncidentesDelitosService.obtener_incidentes(
            filtros=filtros,
            usuario_id=current_user.id,
            rol_usuario=current_user.rol
        )
        
        return jsonify({'success': True, 'data': incidentes}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/incidentes/<int:incidente_id>', methods=['GET'])
@jwt_required()
def obtener_incidente(incidente_id):
    """Obtener detalle de un incidente"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user:
            return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404
        
        incidente = IncidenteElectoral.query.get(incidente_id)
        if not incidente:
            return jsonify({'success': False, 'error': 'Incidente no encontrado'}), 404
        
        # Verificar permisos
        if current_user.rol == 'testigo_electoral' and incidente.reportado_por_id != current_user.id:
            return jsonify({'success': False, 'error': 'No tiene permisos para ver este incidente'}), 403
        
        # Obtener seguimiento
        seguimiento = IncidentesDelitosService.obtener_seguimiento('incidente', incidente_id)
        
        return jsonify({
            'success': True,
            'data': {
                'incidente': incidente.to_dict(),
                'seguimiento': seguimiento
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/incidentes/<int:incidente_id>/estado', methods=['PUT'])
@jwt_required()
def actualizar_estado_incidente(incidente_id):
    """Actualizar estado de un incidente"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user:
            return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404
        
        # Solo coordinadores y superiores pueden cambiar estado
        if current_user.rol not in ['coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental', 'auditor_electoral', 'super_admin']:
            return jsonify({'success': False, 'error': 'No tiene permisos para actualizar incidentes'}), 403
        
        data = request.get_json()
        nuevo_estado = data.get('estado')
        comentario = data.get('comentario')
        
        if not nuevo_estado:
            return jsonify({'success': False, 'error': 'Estado es requerido'}), 400
        
        incidente = IncidentesDelitosService.actualizar_estado_incidente(
            incidente_id, nuevo_estado, current_user.id, comentario
        )
        
        return jsonify({
            'success': True,
            'message': 'Estado actualizado exitosamente',
            'data': incidente.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/delitos', methods=['POST'])
@jwt_required()
def crear_delito():
    """Crear un nuevo delito electoral"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user:
            return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('tipo_delito'):
            return jsonify({'success': False, 'error': 'Tipo de delito es requerido'}), 400
        if not data.get('titulo'):
            return jsonify({'success': False, 'error': 'Título es requerido'}), 400
        if not data.get('descripcion'):
            return jsonify({'success': False, 'error': 'Descripción es requerida'}), 400
        
        delito = IncidentesDelitosService.crear_delito(data, current_user.id)
        
        return jsonify({
            'success': True,
            'message': 'Delito creado exitosamente',
            'data': delito.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/delitos', methods=['GET'])
@jwt_required()
def obtener_delitos():
    """Obtener delitos según permisos del usuario"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user:
            return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404
        
        # Obtener filtros de query params
        filtros = {}
        if request.args.get('estado'):
            filtros['estado'] = request.args.get('estado')
        if request.args.get('gravedad'):
            filtros['gravedad'] = request.args.get('gravedad')
        if request.args.get('tipo_delito'):
            filtros['tipo_delito'] = request.args.get('tipo_delito')
        if request.args.get('fecha_desde'):
            filtros['fecha_desde'] = request.args.get('fecha_desde')
        if request.args.get('fecha_hasta'):
            filtros['fecha_hasta'] = request.args.get('fecha_hasta')
        if request.args.get('mesa_id'):
            filtros['mesa_id'] = request.args.get('mesa_id')
        
        delitos = IncidentesDelitosService.obtener_delitos(
            filtros=filtros,
            usuario_id=current_user.id,
            rol_usuario=current_user.rol
        )
        
        return jsonify({'success': True, 'data': delitos}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/delitos/<int:delito_id>', methods=['GET'])
@jwt_required()
def obtener_delito(delito_id):
    """Obtener detalle de un delito"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user:
            return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404
        
        delito = DelitoElectoral.query.get(delito_id)
        if not delito:
            return jsonify({'success': False, 'error': 'Delito no encontrado'}), 404
        
        # Verificar permisos
        if current_user.rol == 'testigo_electoral' and delito.reportado_por_id != current_user.id:
            return jsonify({'success': False, 'error': 'No tiene permisos para ver este delito'}), 403
        
        # Obtener seguimiento
        seguimiento = IncidentesDelitosService.obtener_seguimiento('delito', delito_id)
        
        return jsonify({
            'success': True,
            'data': {
                'delito': delito.to_dict(),
                'seguimiento': seguimiento
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/delitos/<int:delito_id>/estado', methods=['PUT'])
@jwt_required()
def actualizar_estado_delito(delito_id):
    """Actualizar estado de un delito"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user:
            return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404
        
        # Solo coordinadores y superiores pueden cambiar estado
        if current_user.rol not in ['coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental', 'auditor_electoral', 'super_admin']:
            return jsonify({'success': False, 'error': 'No tiene permisos para actualizar delitos'}), 403
        
        data = request.get_json()
        nuevo_estado = data.get('estado')
        comentario = data.get('comentario')
        
        if not nuevo_estado:
            return jsonify({'success': False, 'error': 'Estado es requerido'}), 400
        
        delito = IncidentesDelitosService.actualizar_estado_delito(
            delito_id, nuevo_estado, current_user.id, comentario
        )
        
        return jsonify({
            'success': True,
            'message': 'Estado actualizado exitosamente',
            'data': delito.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/delitos/<int:delito_id>/denunciar', methods=['POST'])
@jwt_required()
def denunciar_delito(delito_id):
    """Denunciar formalmente un delito"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user:
            return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404
        
        # Solo auditores y super_admin pueden denunciar formalmente
        if current_user.rol not in ['auditor_electoral', 'super_admin']:
            return jsonify({'success': False, 'error': 'No tiene permisos para denunciar formalmente'}), 403
        
        data = request.get_json()
        numero_denuncia = data.get('numero_denuncia')
        autoridad_competente = data.get('autoridad_competente')
        
        if not numero_denuncia or not autoridad_competente:
            return jsonify({'success': False, 'error': 'Número de denuncia y autoridad competente son requeridos'}), 400
        
        delito = IncidentesDelitosService.denunciar_formalmente(
            delito_id, current_user.id, numero_denuncia, autoridad_competente
        )
        
        return jsonify({
            'success': True,
            'message': 'Delito denunciado formalmente',
            'data': delito.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/reportes/estadisticas', methods=['GET'])
@jwt_required()
def obtener_estadisticas():
    """Obtener estadísticas de incidentes y delitos"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user:
            return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404
        
        estadisticas = IncidentesDelitosService.obtener_estadisticas(
            usuario_id=current_user.id,
            rol_usuario=current_user.rol
        )
        
        return jsonify({'success': True, 'data': estadisticas}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/notificaciones', methods=['GET'])
@jwt_required()
def obtener_notificaciones():
    """Obtener notificaciones del usuario"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user:
            return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404
        
        solo_no_leidas = request.args.get('solo_no_leidas', 'false').lower() == 'true'
        
        notificaciones = IncidentesDelitosService.obtener_notificaciones(
            current_user.id, solo_no_leidas
        )
        
        return jsonify({'success': True, 'data': notificaciones}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/notificaciones/<int:notificacion_id>/leer', methods=['PUT'])
@jwt_required()
def marcar_notificacion_leida(notificacion_id):
    """Marcar notificación como leída"""
    try:
        IncidentesDelitosService.marcar_notificacion_leida(notificacion_id)
        
        return jsonify({'success': True, 'message': 'Notificación marcada como leída'}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/incidentes/tipos', methods=['GET'])
@jwt_required()
def obtener_tipos_incidentes():
    """Obtener tipos de incidentes disponibles"""
    return jsonify({'success': True, 'tipos': IncidenteElectoral.TIPOS_INCIDENTE}), 200


@incidentes_delitos_bp.route('/api/delitos/tipos', methods=['GET'])
@jwt_required()
def obtener_tipos_delitos():
    """Obtener tipos de delitos disponibles"""
    return jsonify({'success': True, 'tipos': DelitoElectoral.TIPOS_DELITO}), 200



@incidentes_delitos_bp.route('/api/evidencia/upload', methods=['POST'])
@jwt_required()
def upload_evidencia():
    """
    Upload de evidencia fotográfica
    
    Form Data:
        - file: Archivo de imagen
        - tipo_reporte: 'incidente' o 'delito'
        - reporte_id: ID del reporte
    
    Returns:
        JSON con información de la evidencia subida
    """
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Validar que se envió un archivo
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó ningún archivo'
            }), 400
        
        file = request.files['file']
        tipo_reporte = request.form.get('tipo_reporte')
        reporte_id = request.form.get('reporte_id')
        
        # Validar parámetros
        if not tipo_reporte or not reporte_id:
            return jsonify({
                'success': False,
                'error': 'tipo_reporte y reporte_id son requeridos'
            }), 400
        
        try:
            reporte_id = int(reporte_id)
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'reporte_id debe ser un número'
            }), 400
        
        # Validar que el reporte existe y el usuario tiene permisos
        if tipo_reporte == 'incidente':
            reporte = IncidenteElectoral.query.get(reporte_id)
            if not reporte:
                return jsonify({
                    'success': False,
                    'error': 'Incidente no encontrado'
                }), 404
            
            # Validar permisos: solo el reportante o coordinadores pueden subir evidencia
            if current_user.rol == 'testigo_electoral' and reporte.reportado_por_id != current_user.id:
                return jsonify({
                    'success': False,
                    'error': 'No tiene permisos para agregar evidencia a este incidente'
                }), 403
                
        elif tipo_reporte == 'delito':
            reporte = DelitoElectoral.query.get(reporte_id)
            if not reporte:
                return jsonify({
                    'success': False,
                    'error': 'Delito no encontrado'
                }), 404
            
            # Validar permisos
            if current_user.rol == 'testigo_electoral' and reporte.reportado_por_id != current_user.id:
                return jsonify({
                    'success': False,
                    'error': 'No tiene permisos para agregar evidencia a este delito'
                }), 403
        else:
            return jsonify({
                'success': False,
                'error': 'tipo_reporte debe ser "incidente" o "delito"'
            }), 400
        
        # Subir evidencia
        result = UploadService.upload_evidencia(file, tipo_reporte, reporte_id, current_user.id)
        
        return jsonify({
            'success': True,
            'message': 'Evidencia subida exitosamente',
            'data': result
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        import traceback
        print(f"Error subiendo evidencia: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Error al subir evidencia: {str(e)}'
        }), 500


@incidentes_delitos_bp.route('/api/evidencia/<filename>', methods=['GET'])
@jwt_required()
def get_evidencia(filename):
    """
    Obtener archivo de evidencia
    
    Args:
        filename: Nombre del archivo
    
    Returns:
        Archivo de imagen
    """
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Buscar evidencia en base de datos
        evidencia = EvidenciaFotografica.query.filter_by(filename=filename).first()
        
        if not evidencia:
            return jsonify({
                'success': False,
                'error': 'Evidencia no encontrada'
            }), 404
        
        # Validar permisos de acceso
        # Obtener el reporte asociado
        if evidencia.incidente_id:
            reporte = IncidenteElectoral.query.get(evidencia.incidente_id)
            tipo_reporte = 'incidente'
        elif evidencia.delito_id:
            reporte = DelitoElectoral.query.get(evidencia.delito_id)
            tipo_reporte = 'delito'
        else:
            return jsonify({
                'success': False,
                'error': 'Evidencia no asociada a ningún reporte'
            }), 404
        
        # Validar permisos según rol
        tiene_permiso = False
        
        if current_user.rol in ['super_admin', 'auditor_electoral']:
            tiene_permiso = True
        elif current_user.rol == 'testigo_electoral':
            # Testigos solo ven evidencia de sus propios reportes
            tiene_permiso = (reporte.reportado_por_id == current_user.id)
        elif current_user.rol == 'coordinador_puesto':
            # Coordinadores de puesto ven evidencia de su puesto
            tiene_permiso = (reporte.puesto_id == current_user.ubicacion_id)
        elif current_user.rol == 'coordinador_municipal':
            # Coordinadores municipales ven evidencia de su municipio
            tiene_permiso = (reporte.municipio_id == current_user.ubicacion_id)
        elif current_user.rol == 'coordinador_departamental':
            # Coordinadores departamentales ven evidencia de su departamento
            tiene_permiso = (reporte.departamento_id == current_user.ubicacion_id)
        
        if not tiene_permiso:
            return jsonify({
                'success': False,
                'error': 'No tiene permisos para acceder a esta evidencia'
            }), 403
        
        # Obtener ruta del archivo
        file_path = UploadService.get_evidencia_path(filename)
        
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': 'Archivo no encontrado en el sistema'
            }), 404
        
        # Servir archivo
        return send_file(
            file_path,
            mimetype=evidencia.mime_type,
            as_attachment=False,
            download_name=evidencia.filename_original
        )
        
    except Exception as e:
        import traceback
        print(f"Error obteniendo evidencia: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Error al obtener evidencia: {str(e)}'
        }), 500


@incidentes_delitos_bp.route('/api/evidencia/<int:evidencia_id>', methods=['DELETE'])
@jwt_required()
def delete_evidencia(evidencia_id):
    """
    Eliminar evidencia fotográfica
    
    Args:
        evidencia_id: ID de la evidencia
    
    Returns:
        JSON con resultado de la operación
    """
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Buscar evidencia
        evidencia = EvidenciaFotografica.query.get(evidencia_id)
        
        if not evidencia:
            return jsonify({
                'success': False,
                'error': 'Evidencia no encontrada'
            }), 404
        
        # Solo el usuario que subió la evidencia o super_admin pueden eliminarla
        if current_user.id != evidencia.subido_por_id and current_user.rol != 'super_admin':
            return jsonify({
                'success': False,
                'error': 'No tiene permisos para eliminar esta evidencia'
            }), 403
        
        # Eliminar evidencia
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
        import traceback
        print(f"Error eliminando evidencia: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Error al eliminar evidencia: {str(e)}'
        }), 500
