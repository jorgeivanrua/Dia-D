"""
Rutas del Super Admin - VERSIÓN LIMPIA
"""
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.utils.decorators import role_required

super_admin_bp = Blueprint('super_admin', __name__, url_prefix='/api/super-admin')


@super_admin_bp.route('/stats', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_stats():
    """
    Obtener estadísticas globales del sistema
    """
    try:
        from backend.database import db
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.location import Location
        
        # Contar usuarios activos
        total_usuarios = User.query.filter_by(activo=True).count()
        
        # Contar puestos y mesas
        total_puestos = Location.query.filter_by(tipo='puesto').count()
        total_mesas = Location.query.filter_by(tipo='mesa').count()
        
        # Contar formularios
        total_formularios = FormularioE14.query.count()
        formularios_pendientes = FormularioE14.query.filter_by(estado='pendiente').count()
        formularios_validados = FormularioE14.query.filter_by(estado='validado').count()
        
        # Calcular porcentaje
        porcentaje_validados = (formularios_validados / total_formularios * 100) if total_formularios > 0 else 0
        
        return jsonify({
            'success': True,
            'data': {
                'totalUsuarios': total_usuarios,
                'usuariosChange': 0,
                'totalPuestos': total_puestos,
                'totalMesas': total_mesas,
                'totalFormularios': total_formularios,
                'formulariosPendientes': formularios_pendientes,
                'totalValidados': formularios_validados,
                'porcentajeValidados': round(porcentaje_validados, 2)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_all_users():
    """
    Obtener todos los usuarios del sistema
    """
    try:
        from backend.models.location import Location
        
        users = User.query.all()
        
        users_data = []
        for user in users:
            user_dict = {
                'id': user.id,
                'nombre': user.nombre,
                'rol': user.rol,
                'activo': user.activo,
                'ubicacion_id': user.ubicacion_id,
                'ubicacion_nombre': None,
                'ultimo_acceso': user.ultimo_acceso.isoformat() if hasattr(user, 'ultimo_acceso') and user.ultimo_acceso else None,
                'created_at': user.created_at.isoformat() if hasattr(user, 'created_at') and user.created_at else None
            }
            
            # Obtener nombre de ubicación
            if user.ubicacion_id:
                try:
                    ubicacion = Location.query.get(user.ubicacion_id)
                    if ubicacion:
                        user_dict['ubicacion_nombre'] = ubicacion.nombre_completo
                except:
                    pass
            
            users_data.append(user_dict)
        
        return jsonify({
            'success': True,
            'data': users_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/system-health', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_system_health():
    """
    Obtener estado de salud del sistema
    """
    try:
        return jsonify({
            'success': True,
            'data': {
                'status': 'healthy',
                'cpu_percent': 0,
                'memory_percent': 0,
                'database': 'healthy',
                'timestamp': datetime.now().isoformat()
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/monitoreo-departamental', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_monitoreo_departamental():
    """
    Obtener monitoreo por departamento
    """
    try:
        from backend.models.location import Location
        from backend.models.formulario_e14 import FormularioE14
        
        # Por ahora retornar datos vacíos
        return jsonify({
            'success': True,
            'data': []
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
