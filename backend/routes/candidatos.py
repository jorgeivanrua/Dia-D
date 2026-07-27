"""
Rutas para gestión de Candidatos
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.models.candidato import Candidato
from backend.models.partido_politico import PartidoPolitico
from backend.database import db
from backend.utils.decorators import role_required

candidatos_bp = Blueprint('candidatos', __name__, url_prefix='/api/candidatos')


@candidatos_bp.route('', methods=['GET'])
@jwt_required()
def listar_candidatos():
    """
    Listar todos los candidatos
    Query params:
        activo: Filtrar por estado activo (true/false)
        partido_id: Filtrar por partido
        tipo_eleccion_id: Filtrar por tipo de elección
        search: Buscar por nombre
    """
    try:
        query = Candidato.query
        
        # Filtrar por activo
        activo = request.args.get('activo')
        if activo is not None:
            activo_bool = activo.lower() == 'true'
            query = query.filter_by(activo=activo_bool)
        
        # Filtrar por partido
        partido_id = request.args.get('partido_id')
        if partido_id:
            query = query.filter_by(partido_id=int(partido_id))
        
        # Filtrar por tipo de elección
        tipo_eleccion_id = request.args.get('tipo_eleccion_id')
        if tipo_eleccion_id:
            query = query.filter_by(tipo_eleccion_id=int(tipo_eleccion_id))
        
        # Buscar
        search = request.args.get('search')
        if search:
            search_pattern = f'%{search}%'
            query = query.filter(Candidato.nombre_completo.ilike(search_pattern))
        
        # Ordenar
        query = query.order_by(Candidato.nombre_completo)
        
        candidatos = query.all()
        
        return jsonify({
            'success': True,
            'data': [c.to_dict() for c in candidatos]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@candidatos_bp.route('/<int:candidato_id>', methods=['GET'])
@jwt_required()
def obtener_candidato(candidato_id):
    """Obtener un candidato específico"""
    try:
        candidato = Candidato.query.get(candidato_id)
        
        if not candidato:
            return jsonify({
                'success': False,
                'error': 'Candidato no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': candidato.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@candidatos_bp.route('', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def crear_candidato():
    """
    Crear un nuevo candidato
    Body:
        nombre_completo: Nombre completo del candidato
        partido_id: ID del partido
        tipo_eleccion_id: ID del tipo de elección
        cargo: Cargo al que se postula
        numero_lista: Número en la lista (opcional)
        biografia: Biografía (opcional)
        activo: Estado activo (default: true)
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data.get('nombre_completo'):
            return jsonify({
                'success': False,
                'error': 'El nombre completo es requerido'
            }), 400
        
        if not data.get('partido_id'):
            return jsonify({
                'success': False,
                'error': 'El partido es requerido'
            }), 400
        
        if not data.get('tipo_eleccion_id'):
            return jsonify({
                'success': False,
                'error': 'El tipo de elección es requerido'
            }), 400
        
        if not data.get('cargo'):
            return jsonify({
                'success': False,
                'error': 'El cargo es requerido'
            }), 400
        
        # Verificar que el partido exista
        partido = PartidoPolitico.query.get(data['partido_id'])
        if not partido:
            return jsonify({
                'success': False,
                'error': 'Partido no encontrado'
            }), 404
        
        # Crear candidato
        candidato = Candidato(
            nombre_completo=data['nombre_completo'],
            partido_id=data['partido_id'],
            tipo_eleccion_id=data['tipo_eleccion_id'],
            cargo=data['cargo'],
            numero_lista=data.get('numero_lista'),
            biografia=data.get('biografia'),
            activo=data.get('activo', True)
        )
        
        db.session.add(candidato)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Candidato creado exitosamente',
            'data': candidato.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@candidatos_bp.route('/<int:candidato_id>', methods=['PUT'])
@jwt_required()
@role_required(['super_admin'])
def actualizar_candidato(candidato_id):
    """Actualizar un candidato"""
    try:
        candidato = Candidato.query.get(candidato_id)
        
        if not candidato:
            return jsonify({
                'success': False,
                'error': 'Candidato no encontrado'
            }), 404
        
        data = request.get_json()
        
        # Verificar partido si se actualiza
        if 'partido_id' in data:
            partido = PartidoPolitico.query.get(data['partido_id'])
            if not partido:
                return jsonify({
                    'success': False,
                    'error': 'Partido no encontrado'
                }), 404
        
        # Actualizar campos
        if 'nombre_completo' in data:
            candidato.nombre_completo = data['nombre_completo']
        if 'partido_id' in data:
            candidato.partido_id = data['partido_id']
        if 'tipo_eleccion_id' in data:
            candidato.tipo_eleccion_id = data['tipo_eleccion_id']
        if 'cargo' in data:
            candidato.cargo = data['cargo']
        if 'numero_lista' in data:
            candidato.numero_lista = data['numero_lista']
        if 'biografia' in data:
            candidato.biografia = data['biografia']
        if 'foto_url' in data:
            candidato.foto_url = data['foto_url']
        if 'activo' in data:
            candidato.activo = data['activo']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Candidato actualizado exitosamente',
            'data': candidato.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@candidatos_bp.route('/<int:candidato_id>', methods=['DELETE'])
@jwt_required()
@role_required(['super_admin'])
def eliminar_candidato(candidato_id):
    """Eliminar un candidato"""
    try:
        candidato = Candidato.query.get(candidato_id)
        
        if not candidato:
            return jsonify({
                'success': False,
                'error': 'Candidato no encontrado'
            }), 404
        
        # TODO: Verificar que no tenga votos registrados
        # votos_count = VotoCandidato.query.filter_by(candidato_id=candidato_id).count()
        # if votos_count > 0:
        #     return jsonify({
        #         'success': False,
        #         'error': f'No se puede eliminar. El candidato tiene {votos_count} voto(s) registrado(s)'
        #     }), 400
        
        db.session.delete(candidato)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Candidato eliminado exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@candidatos_bp.route('/export', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def exportar_candidatos():
    """Exportar todos los candidatos en formato JSON"""
    try:
        candidatos = Candidato.query.order_by(Candidato.nombre_completo).all()
        
        return jsonify({
            'success': True,
            'data': [c.to_dict() for c in candidatos],
            'total': len(candidatos)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



@candidatos_bp.route('/<int:candidato_id>/foto', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def subir_foto_candidato(candidato_id):
    """
    Subir foto de un candidato
    Form data:
        foto: Archivo de imagen (png, jpg, jpeg, webp)
    """
    try:
        from backend.services.candidato_service import CandidatoService
        import os
        from flask import current_app
        
        candidato = Candidato.query.get(candidato_id)
        
        if not candidato:
            return jsonify({
                'success': False,
                'error': 'Candidato no encontrado'
            }), 404
        
        # Verificar que se envió un archivo
        if 'foto' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó archivo'
            }), 400
        
        archivo = request.files['foto']
        
        if archivo.filename == '':
            return jsonify({
                'success': False,
                'error': 'No se seleccionó archivo'
            }), 400
        
        # Validar archivo
        valid, error = CandidatoService.validar_foto(archivo)
        if not valid:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        # Guardar archivo
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'frontend/static/uploads')
        candidatos_folder = os.path.join(upload_folder, 'candidatos')
        
        # Crear directorio si no existe
        os.makedirs(candidatos_folder, exist_ok=True)
        
        # Generar nombre único
        extension = archivo.filename.rsplit('.', 1)[1].lower()
        filename = f"candidato_{candidato_id}_{candidato.nombre_completo.replace(' ', '_')[:30]}.{extension}"
        filepath = os.path.join(candidatos_folder, filename)
        
        # Guardar archivo
        archivo.save(filepath)
        
        # Actualizar URL en base de datos
        foto_url = f"/static/uploads/candidatos/{filename}"
        candidato.foto_url = foto_url
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Foto subida exitosamente',
            'data': {
                'foto_url': foto_url,
                'candidato': candidato.to_dict()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
