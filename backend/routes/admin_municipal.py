"""
Rutas para Admin Municipal
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.location import Location
from backend.models.formulario_e14 import FormularioE14
from backend.database import db

admin_municipal_bp = Blueprint('admin_municipal', __name__)


@admin_municipal_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Estadísticas del municipio"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'admin_municipal':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        municipio = Location.query.get(user.ubicacion_id)
        
        # Obtener ubicaciones del municipio
        zonas = Location.query.filter_by(
            tipo='zona',
            departamento_codigo=municipio.departamento_codigo,
            municipio_codigo=municipio.municipio_codigo,
            activo=True
        ).count()
        
        puestos = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo=municipio.departamento_codigo,
            municipio_codigo=municipio.municipio_codigo,
            activo=True
        ).count()
        
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=municipio.departamento_codigo,
            municipio_codigo=municipio.municipio_codigo,
            activo=True
        ).count()
        
        # Obtener formularios del municipio
        mesa_ids = [m.id for m in Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=municipio.departamento_codigo,
            municipio_codigo=municipio.municipio_codigo,
            activo=True
        ).all()]
        
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).all() if mesa_ids else []
        
        formularios_completados = sum(1 for f in formularios if f.estado == 'completado')
        
        stats = {
            'total_zonas': zonas,
            'total_puestos': puestos,
            'total_mesas': mesas,
            'total_formularios': len(formularios),
            'formularios_completados': formularios_completados,
            'formularios_pendientes': len(formularios) - formularios_completados,
            'porcentaje_avance': (formularios_completados / len(formularios) * 100) if formularios else 0,
            'municipio': {
                'id': municipio.id,
                'nombre': municipio.nombre_completo,
                'codigo': municipio.municipio_codigo
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


@admin_municipal_bp.route('/zonas', methods=['GET'])
@jwt_required()
def get_zonas():
    """Obtener zonas del municipio"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'admin_municipal':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        municipio = Location.query.get(user.ubicacion_id)
        
        zonas = Location.query.filter_by(
            tipo='zona',
            departamento_codigo=municipio.departamento_codigo,
            municipio_codigo=municipio.municipio_codigo,
            activo=True
        ).all()
        
        zonas_data = []
        for zona in zonas:
            # Contar puestos de la zona
            puestos_count = Location.query.filter_by(
                tipo='puesto',
                departamento_codigo=zona.departamento_codigo,
                municipio_codigo=zona.municipio_codigo,
                zona_codigo=zona.zona_codigo,
                activo=True
            ).count()
            
            zonas_data.append({
                'id': zona.id,
                'nombre_completo': zona.nombre_completo,
                'zona_codigo': zona.zona_codigo,
                'total_puestos': puestos_count
            })
        
        return jsonify({
            'success': True,
            'data': zonas_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_municipal_bp.route('/puestos', methods=['GET'])
@jwt_required()
def get_puestos():
    """Obtener puestos del municipio"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'admin_municipal':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        municipio = Location.query.get(user.ubicacion_id)
        
        puestos = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo=municipio.departamento_codigo,
            municipio_codigo=municipio.municipio_codigo,
            activo=True
        ).all()
        
        puestos_data = []
        for puesto in puestos:
            # Contar mesas del puesto
            mesas_count = Location.query.filter_by(
                tipo='mesa',
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                zona_codigo=puesto.zona_codigo,
                puesto_codigo=puesto.puesto_codigo,
                activo=True
            ).count()
            
            puestos_data.append({
                'id': puesto.id,
                'nombre_completo': puesto.nombre_completo,
                'puesto_codigo': puesto.puesto_codigo,
                'puesto_nombre': puesto.puesto_nombre,
                'zona_codigo': puesto.zona_codigo,
                'total_mesas': mesas_count,
                'total_votantes_registrados': puesto.total_votantes_registrados
            })
        
        return jsonify({
            'success': True,
            'data': puestos_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_municipal_bp.route('/mesas', methods=['GET'])
@jwt_required()
def get_mesas():
    """Obtener mesas del municipio"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'admin_municipal':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        municipio = Location.query.get(user.ubicacion_id)
        
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=municipio.departamento_codigo,
            municipio_codigo=municipio.municipio_codigo,
            activo=True
        ).all()
        
        mesas_data = []
        for mesa in mesas:
            # Buscar formulario de la mesa
            formulario = FormularioE14.query.filter_by(mesa_id=mesa.id).first()
            
            mesas_data.append({
                'id': mesa.id,
                'nombre_completo': mesa.nombre_completo,
                'mesa_codigo': mesa.mesa_codigo,
                'puesto_nombre': mesa.puesto_nombre,
                'zona_codigo': mesa.zona_codigo,
                'total_votantes_registrados': mesa.total_votantes_registrados,
                'tiene_formulario': formulario is not None,
                'estado_formulario': formulario.estado if formulario else None
            })
        
        return jsonify({
            'success': True,
            'data': mesas_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
