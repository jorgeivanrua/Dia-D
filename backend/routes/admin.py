"""
Rutas para Admin Departamental
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.location import Location
from backend.models.formulario_e14 import FormularioE14
from backend.database import db

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Estadísticas del departamento"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'admin_departamental':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        departamento = Location.query.get(user.ubicacion_id)
        
        # Obtener ubicaciones del departamento
        municipios = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).count()
        
        puestos = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).count()
        
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).count()
        
        # Obtener usuarios del departamento
        usuarios = User.query.join(Location).filter(
            Location.departamento_codigo == departamento.departamento_codigo,
            User.activo == True
        ).count()
        
        # Obtener formularios del departamento
        mesa_ids = [m.id for m in Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()]
        
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).all() if mesa_ids else []
        
        formularios_completados = sum(1 for f in formularios if f.estado == 'completado')
        
        stats = {
            'total_municipios': municipios,
            'total_puestos': puestos,
            'total_mesas': mesas,
            'total_usuarios': usuarios,
            'total_formularios': len(formularios),
            'formularios_completados': formularios_completados,
            'formularios_pendientes': len(formularios) - formularios_completados,
            'porcentaje_avance': (formularios_completados / len(formularios) * 100) if formularios else 0,
            'departamento': {
                'id': departamento.id,
                'nombre': departamento.nombre_completo,
                'codigo': departamento.departamento_codigo
            }
        }
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_bp.route('/usuarios', methods=['GET'])
@jwt_required()
def get_usuarios():
    """Obtener usuarios del departamento"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'admin_departamental':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        departamento = Location.query.get(user.ubicacion_id)
        
        # Obtener usuarios del departamento
        usuarios = User.query.join(Location).filter(
            Location.departamento_codigo == departamento.departamento_codigo,
            User.activo == True
        ).all()
        
        usuarios_data = []
        for usuario in usuarios:
            ubicacion = Location.query.get(usuario.ubicacion_id) if usuario.ubicacion_id else None
            
            usuarios_data.append({
                'id': usuario.id,
                'nombre': usuario.nombre,
                'rol': usuario.rol,
                'ubicacion': ubicacion.nombre_completo if ubicacion else None,
                'activo': usuario.activo,
                'ultimo_acceso': usuario.ultimo_acceso.isoformat() if usuario.ultimo_acceso else None
            })
        
        return jsonify({
            'success': True,
            'data': usuarios_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_bp.route('/ubicaciones', methods=['GET'])
@jwt_required()
def get_ubicaciones():
    """Obtener ubicaciones del departamento"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'admin_departamental':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        departamento = Location.query.get(user.ubicacion_id)
        
        # Obtener tipo de ubicación solicitado
        tipo = request.args.get('tipo', 'municipio')
        
        ubicaciones = Location.query.filter_by(
            tipo=tipo,
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()
        
        ubicaciones_data = []
        for ubicacion in ubicaciones:
            ubicaciones_data.append({
                'id': ubicacion.id,
                'nombre_completo': ubicacion.nombre_completo,
                'tipo': ubicacion.tipo,
                'departamento_codigo': ubicacion.departamento_codigo,
                'municipio_codigo': ubicacion.municipio_codigo,
                'zona_codigo': ubicacion.zona_codigo,
                'puesto_codigo': ubicacion.puesto_codigo,
                'total_votantes_registrados': ubicacion.total_votantes_registrados
            })
        
        return jsonify({
            'success': True,
            'data': ubicaciones_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_bp.route('/formularios', methods=['GET'])
@jwt_required()
def get_formularios():
    """Obtener formularios del departamento"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'admin_departamental':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        departamento = Location.query.get(user.ubicacion_id)
        
        # Obtener mesas del departamento
        mesa_ids = [m.id for m in Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()]
        
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).all() if mesa_ids else []
        
        formularios_data = []
        for formulario in formularios:
            mesa = Location.query.get(formulario.mesa_id)
            testigo = User.query.get(formulario.testigo_id)
            
            formularios_data.append({
                'id': formulario.id,
                'mesa_id': formulario.mesa_id,
                'mesa_nombre': mesa.nombre_completo if mesa else None,
                'testigo_id': formulario.testigo_id,
                'testigo_nombre': testigo.nombre if testigo else None,
                'estado': formulario.estado,
                'created_at': formulario.created_at.isoformat() if formulario.created_at else None,
                'updated_at': formulario.updated_at.isoformat() if formulario.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'data': formularios_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
