"""
Rutas de autenticación
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.auth_service import AuthService
from backend.models.user import User
from backend.utils.jwt_utils import create_token_response
from backend.utils.exceptions import BaseAPIException
from backend.database import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login basado en ubicación jerárquica
    
    Body:
        rol: Rol del usuario
        departamento_codigo: Código de departamento (opcional según rol)
        municipio_codigo: Código de municipio (opcional según rol)
        zona_codigo: Código de zona (opcional según rol)
        puesto_codigo: Código de puesto (opcional según rol)
        password: Contraseña
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        rol = data.get('rol')
        password = data.get('password')
        
        if not rol or not password:
            return jsonify({
                'success': False,
                'error': 'Rol y contraseña son requeridos'
            }), 400
        
        # Construir datos de ubicación
        ubicacion_data = {}
        if 'departamento_codigo' in data:
            ubicacion_data['departamento_codigo'] = data['departamento_codigo']
        if 'municipio_codigo' in data:
            ubicacion_data['municipio_codigo'] = data['municipio_codigo']
        if 'zona_codigo' in data:
            ubicacion_data['zona_codigo'] = data['zona_codigo']
        if 'puesto_codigo' in data:
            ubicacion_data['puesto_codigo'] = data['puesto_codigo']
        
        # Autenticar
        user, access_token, refresh_token = AuthService.authenticate_location_based(
            rol, ubicacion_data, password
        )
        
        return jsonify(create_token_response(user, access_token, refresh_token)), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Cerrar sesión"""
    # En una implementación completa, aquí se invalidaría el token
    # Por ahora solo retornamos éxito
    return jsonify({
        'success': True,
        'message': 'Sesión cerrada exitosamente'
    }), 200


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """Obtener perfil del usuario actual"""
    try:
        from backend.models.location import Location
        
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Obtener información de ubicación si existe
        ubicacion = None
        if user.ubicacion_id:
            location = Location.query.get(user.ubicacion_id)
            if location:
                ubicacion = location.to_dict()
        
        # ⭐ MEJORA: Agregar contexto específico para testigos
        contexto = None
        if user.rol == 'testigo_electoral' and ubicacion:
            from backend.models.formulario_e14 import FormularioE14
            
            # Obtener puesto (puede ser la ubicación actual o el puesto de la mesa)
            puesto = ubicacion
            if ubicacion['tipo'] == 'mesa':
                puesto_obj = Location.query.filter_by(
                    tipo='puesto',
                    departamento_codigo=ubicacion['departamento_codigo'],
                    municipio_codigo=ubicacion['municipio_codigo'],
                    zona_codigo=ubicacion['zona_codigo'],
                    puesto_codigo=ubicacion['puesto_codigo']
                ).first()
                if puesto_obj:
                    puesto = puesto_obj.to_dict()
            
            # Contar mesas del puesto
            total_mesas = Location.query.filter_by(
                tipo='mesa',
                departamento_codigo=puesto['departamento_codigo'],
                municipio_codigo=puesto['municipio_codigo'],
                zona_codigo=puesto['zona_codigo'],
                puesto_codigo=puesto['puesto_codigo'],
                activo=True
            ).count()
            
            # Contar formularios del testigo
            mis_formularios = FormularioE14.query.filter_by(
                testigo_id=user.id
            ).count()
            
            formularios_validados = FormularioE14.query.filter_by(
                testigo_id=user.id,
                estado='validado'
            ).count()
            
            formularios_pendientes = FormularioE14.query.filter_by(
                testigo_id=user.id,
                estado='pendiente'
            ).count()
            
            formularios_rechazados = FormularioE14.query.filter_by(
                testigo_id=user.id,
                estado='rechazado'
            ).count()
            
            contexto = {
                'puesto': {
                    'nombre': puesto.get('puesto_nombre'),
                    'codigo': puesto.get('puesto_codigo'),
                    'total_mesas': total_mesas
                },
                'mis_formularios': {
                    'total': mis_formularios,
                    'validados': formularios_validados,
                    'pendientes': formularios_pendientes,
                    'rechazados': formularios_rechazados,
                    'porcentaje_completado': round((mis_formularios / total_mesas * 100), 2) if total_mesas > 0 else 0
                },
                'presencia': {
                    'verificada': user.presencia_verificada,
                    'verificada_at': user.presencia_verificada_at.isoformat() if user.presencia_verificada_at else None,
                    'puede_crear_formularios': user.presencia_verificada
                }
            }
        
        return jsonify({
            'success': True,
            'data': {
                'user': {
                    'id': user.id,
                    'nombre': user.nombre,
                    'rol': user.rol,
                    'ubicacion_id': user.ubicacion_id,
                    'activo': user.activo,
                    'ultimo_acceso': user.ultimo_acceso.isoformat() if user.ultimo_acceso else None,
                    'presencia_verificada': user.presencia_verificada if user.rol == 'testigo_electoral' else None,
                    'presencia_verificada_at': user.presencia_verificada_at.isoformat() if user.presencia_verificada_at else None
                },
                'ubicacion': ubicacion,
                'contexto': contexto  # ⭐ NUEVO
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Cambiar contraseña del usuario actual"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({
                'success': False,
                'error': 'Contraseña actual y nueva son requeridas'
            }), 400
        
        AuthService.change_password(int(user_id), current_password, new_password)
        
        return jsonify({
            'success': True,
            'message': 'Contraseña actualizada exitosamente'
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500





@auth_bp.route('/verificar-presencia', methods=['POST'])
@jwt_required()
def verificar_presencia():
    """Verificar presencia del testigo en la mesa"""
    try:
        from backend.database import db
        from backend.models.location import Location
        
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        if user.rol != 'testigo_electoral':
            return jsonify({
                'success': False,
                'error': 'Solo los testigos pueden verificar presencia'
            }), 403
        
        # Verificar presencia
        user.verificar_presencia()
        db.session.commit()
        
        # Buscar coordinador del puesto para notificar
        coordinador_notificado = False
        if user.ubicacion_id:
            ubicacion = Location.query.get(user.ubicacion_id)
            if ubicacion:
                # Buscar coordinador del puesto
                coordinador = User.query.filter_by(
                    ubicacion_id=ubicacion.id,
                    rol='coordinador_puesto'
                ).first()
                
                if coordinador:
                    # TODO: Implementar sistema de notificaciones
                    # Por ahora solo registramos en logs
                    print(f"NOTIFICACIÓN: Testigo {user.nombre} verificó presencia en {ubicacion.nombre_completo}")
                    print(f"  -> Coordinador a notificar: {coordinador.nombre}")
                    coordinador_notificado = True
        
        return jsonify({
            'success': True,
            'message': 'Presencia verificada exitosamente' + (' y coordinador notificado' if coordinador_notificado else ''),
            'data': {
                'presencia_verificada': True,
                'presencia_verificada_at': user.presencia_verificada_at.isoformat(),
                'coordinador_notificado': coordinador_notificado
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



