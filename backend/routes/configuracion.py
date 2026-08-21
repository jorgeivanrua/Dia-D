"""
Rutas para configuración electoral
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.database import db
from backend.models.configuracion_electoral import (
    TipoEleccion, Coalicion, PartidoCoalicion
)
from backend.models.partido_politico import PartidoPolitico as Partido
from backend.models.candidato import Candidato
from backend.models.user import User

configuracion_bp = Blueprint('configuracion', __name__)


# ============================================================================
# TIPOS DE ELECCIÓN
# ============================================================================

@configuracion_bp.route('/tipos-eleccion', methods=['GET'])
@jwt_required()
def get_tipos_eleccion():
    """Obtener todos los tipos de elección"""
    try:
        tipos = TipoEleccion.query.filter_by(activo=True).order_by(TipoEleccion.orden).all()
        return jsonify({
            'success': True,
            'data': [tipo.to_dict() for tipo in tipos]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@configuracion_bp.route('/tipos-eleccion', methods=['POST'])
@jwt_required()
def create_tipo_eleccion():
    """Crear nuevo tipo de elección (solo admin)"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if user.rol not in ['super_admin', 'admin_departamental', 'admin_municipal']:
            return jsonify({'success': False, 'error': 'No autorizado'}), 403
        
        data = request.get_json()
        
        tipo = TipoEleccion(
            codigo=data['codigo'],
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            orden=data.get('orden', 0)
        )
        
        db.session.add(tipo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': tipo.to_dict(),
            'message': 'Tipo de elección creado exitosamente'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@configuracion_bp.route('/tipos-eleccion/<int:id>', methods=['PUT'])
@jwt_required()
def update_tipo_eleccion(id):
    """Actualizar tipo de elección"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if user.rol not in ['super_admin', 'admin_departamental', 'admin_municipal']:
            return jsonify({'success': False, 'error': 'No autorizado'}), 403
        
        tipo = TipoEleccion.query.get_or_404(id)
        data = request.get_json()
        
        tipo.nombre = data.get('nombre', tipo.nombre)
        tipo.descripcion = data.get('descripcion', tipo.descripcion)
        tipo.orden = data.get('orden', tipo.orden)
        tipo.activo = data.get('activo', tipo.activo)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': tipo.to_dict(),
            'message': 'Tipo de elección actualizado'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# PARTIDOS
# ============================================================================

@configuracion_bp.route('/partidos', methods=['GET'])
@jwt_required()
def get_partidos():
    """Obtener todos los partidos"""
    try:
        partidos = Partido.query.filter_by(activo=True).order_by(Partido.orden).all()
        return jsonify({
            'success': True,
            'data': [partido.to_dict() for partido in partidos]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@configuracion_bp.route('/partidos', methods=['POST'])
@jwt_required()
def create_partido():
    """Crear nuevo partido"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if user.rol not in ['super_admin', 'admin_departamental', 'admin_municipal']:
            return jsonify({'success': False, 'error': 'No autorizado'}), 403
        
        data = request.get_json()
        
        partido = Partido(
            codigo=data['codigo'],
            nombre=data['nombre'],
            nombre_corto=data.get('nombre_corto'),
            logo_url=data.get('logo_url'),
            color=data.get('color'),
            orden=data.get('orden', 0)
        )
        
        db.session.add(partido)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': partido.to_dict(),
            'message': 'Partido creado exitosamente'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@configuracion_bp.route('/partidos/<int:id>', methods=['PUT'])
@jwt_required()
def update_partido(id):
    """Actualizar partido"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if user.rol not in ['super_admin', 'admin_departamental', 'admin_municipal']:
            return jsonify({'success': False, 'error': 'No autorizado'}), 403
        
        partido = Partido.query.get_or_404(id)
        data = request.get_json()
        
        partido.nombre = data.get('nombre', partido.nombre)
        partido.nombre_corto = data.get('nombre_corto', partido.nombre_corto)
        partido.logo_url = data.get('logo_url', partido.logo_url)
        partido.color = data.get('color', partido.color)
        partido.orden = data.get('orden', partido.orden)
        partido.activo = data.get('activo', partido.activo)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': partido.to_dict(),
            'message': 'Partido actualizado'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# CANDIDATOS
# ============================================================================

@configuracion_bp.route('/candidatos', methods=['GET'])
@jwt_required()
def get_candidatos():
    """Obtener candidatos (opcionalmente filtrados por tipo de elección)"""
    try:
        tipo_eleccion_id = request.args.get('tipo_eleccion_id')
        partido_id = request.args.get('partido_id')
        
        query = Candidato.query.filter_by(activo=True)
        
        if tipo_eleccion_id:
            query = query.filter_by(tipo_eleccion_id=tipo_eleccion_id)
        
        if partido_id:
            query = query.filter_by(partido_id=partido_id)
        
        candidatos = query.order_by(Candidato.orden).all()
        
        return jsonify({
            'success': True,
            'data': [candidato.to_dict() for candidato in candidatos]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@configuracion_bp.route('/candidatos', methods=['POST'])
@jwt_required()
def create_candidato():
    """Crear nuevo candidato"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if user.rol not in ['super_admin', 'admin_departamental', 'admin_municipal']:
            return jsonify({'success': False, 'error': 'No autorizado'}), 403
        
        data = request.get_json()
        
        candidato = Candidato(
            codigo=data['codigo'],
            nombre_completo=data['nombre_completo'],
            numero_lista=data.get('numero_lista'),
            partido_id=data.get('partido_id'),
            tipo_eleccion_id=data.get('tipo_eleccion_id'),
            foto_url=data.get('foto_url'),
            es_independiente=data.get('es_independiente', False),
            orden=data.get('orden', 0)
        )
        
        db.session.add(candidato)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': candidato.to_dict(),
            'message': 'Candidato creado exitosamente'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@configuracion_bp.route('/candidatos/<int:id>', methods=['PUT'])
@jwt_required()
def update_candidato(id):
    """Actualizar candidato"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if user.rol not in ['super_admin', 'admin_departamental', 'admin_municipal']:
            return jsonify({'success': False, 'error': 'No autorizado'}), 403
        
        candidato = Candidato.query.get_or_404(id)
        data = request.get_json()
        
        candidato.nombre_completo = data.get('nombre_completo', candidato.nombre_completo)
        candidato.numero_lista = data.get('numero_lista', candidato.numero_lista)
        candidato.partido_id = data.get('partido_id', candidato.partido_id)
        candidato.tipo_eleccion_id = data.get('tipo_eleccion_id', candidato.tipo_eleccion_id)
        candidato.foto_url = data.get('foto_url', candidato.foto_url)
        candidato.es_independiente = data.get('es_independiente', candidato.es_independiente)
        candidato.orden = data.get('orden', candidato.orden)
        candidato.activo = data.get('activo', candidato.activo)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': candidato.to_dict(),
            'message': 'Candidato actualizado'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# COALICIONES
# ============================================================================

@configuracion_bp.route('/coaliciones', methods=['GET'])
@jwt_required()
def get_coaliciones():
    """Obtener todas las coaliciones"""
    try:
        coaliciones = Coalicion.query.filter_by(activo=True).all()
        return jsonify({
            'success': True,
            'data': [coalicion.to_dict() for coalicion in coaliciones]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@configuracion_bp.route('/coaliciones', methods=['POST'])
@jwt_required()
def create_coalicion():
    """Crear nueva coalición"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if user.rol not in ['super_admin', 'admin_departamental', 'admin_municipal']:
            return jsonify({'success': False, 'error': 'No autorizado'}), 403
        
        data = request.get_json()
        
        coalicion = Coalicion(
            codigo=data['codigo'],
            nombre=data['nombre'],
            descripcion=data.get('descripcion')
        )
        
        db.session.add(coalicion)
        db.session.flush()
        
        # Agregar partidos a la coalición
        if 'partidos_ids' in data:
            for partido_id in data['partidos_ids']:
                pc = PartidoCoalicion(
                    partido_id=partido_id,
                    coalicion_id=coalicion.id
                )
                db.session.add(pc)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': coalicion.to_dict(),
            'message': 'Coalición creada exitosamente'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@configuracion_bp.route('/territorial/departamentos', methods=['GET'])
@jwt_required()
def get_departamentos_activados():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user.rol != 'super_admin':
            return jsonify({'success': False, 'error': 'No autorizado - solo super_admin'}, 403)
        from backend.models.configuracion_sistema import ConfiguracionSistema
        import json
        config = ConfiguracionSistema.get_valor('departamentos_activados')
        departamentos_codigos = json.loads(config) if config else []
        from backend.models.location import Location
        deptos = Location.query.filter(
            Location.tipo == 'departamento',
            Location.departamento_codigo.in_(departamentos_codigos)
        ).all()
        resultado = []
        for d in deptos:
            resultado.append({
                'codigo': d.departamento_codigo,
                'nombre': d.nombre_completo,
                'activo': d.departamento_codigo in departamentos_codigos
            })
        return jsonify({
            'success': True,
            'data': resultado
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@configuracion_bp.route('/territorial/departamentos', methods=['POST'])
@jwt_required()
def set_departamentos_activados():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user.rol != 'super_admin':
            return jsonify({'success': False, 'error': 'No autorizado - solo super_admin'}, 403)
        data = request.get_json()
        departamentos = data.get('departamentos', [])
        import json
        ConfiguracionSistema.set_valor(
            'departamentos_activados',
            json.dumps(departamentos),
            tipo='json',
            descripcion='Códigos de departamentos activados para visualización',
            user_id=current_user_id
        )
        return jsonify({
            'success': True,
            'data': {'departamentos': departamentos},
            'message': 'Departamentos activados actualizados exitosamente'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@configuracion_bp.route('/territorial/municipios', methods=['GET'])
@jwt_required()
def get_municipios_activados():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user.rol != 'super_admin':
            return jsonify({'success': False, 'error': 'No autorizado - solo super_admin'}, 403)
        from backend.models.configuracion_sistema import ConfiguracionSistema
        from backend.models.location import Location
        import json
        config_dept = ConfiguracionSistema.get_valor('departamentos_activados')
        departamentos_activados = json.loads(config_dept) if config_dept else []
        query = Location.query.filter(
            Location.tipo == 'municipio',
            Location.departamento_codigo.in_(departamentos_activados)
        )
        municipios = query.all()
        resultado = []
        for m in municipios:
            resultado.append({
                'codigo': m.municipio_codigo,
                'nombre': m.nombre_completo,
                'departamento': m.departamento_nombre,
                'activo': m.departamento_codigo in departamentos_activados
            })
        return jsonify({
            'success': True,
            'data': resultado
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@configuracion_bp.route('/territorial/municipios', methods=['POST'])
@jwt_required()
def set_municipios_activados():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user.rol != 'super_admin':
            return jsonify({'success': False, 'error': 'No autorizado - solo super_admin'}, 403)
        data = request.get_json()
        municipios = data.get('municipios', [])
        departamento_filtro = data.get('departamento_codigo')
        import json
        config_str = ConfiguracionSistema.get_valor('municipios_activados')
        municipios_activados = json.loads(config_str) if config_str else {}
        nuevo_registro = {}
        for m in municipios:
            codigo = m.get('codigo', '')
            if departamento_filtro:
                clave = f'{departamento_filtro}:{codigo}'
            else:
                clave = codigo
            nuevo_registro[clave] = True
        todos = {**municipios_activados, **nuevo_registro}
        ConfiguracionSistema.set_valor(
            'municipios_activados',
            json.dumps(todos),
            tipo='json',
            descripcion='Códigos de municipios activados para visualización',
            user_id=current_user_id
        )
        return jsonify({
            'success': True,
            'data': {'municipios': municipios, 'departamento': departamento_filtro},
            'message': 'Municipios activados actualizados exitosamente'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
