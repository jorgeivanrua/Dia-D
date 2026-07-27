"""
Rutas para gestión de Partidos Políticos
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.models.partido_politico import PartidoPolitico
from backend.database import db
from backend.utils.decorators import role_required

partidos_bp = Blueprint('partidos', __name__, url_prefix='/api/partidos')


@partidos_bp.route('', methods=['GET'])
@jwt_required()
def listar_partidos():
    """
    Listar todos los partidos políticos
    Query params:
        activo: Filtrar por estado activo (true/false)
        search: Buscar por nombre o sigla
    """
    try:
        query = PartidoPolitico.query
        
        # Filtrar por activo
        activo = request.args.get('activo')
        if activo is not None:
            activo_bool = activo.lower() == 'true'
            query = query.filter_by(activo=activo_bool)
        
        # Buscar
        search = request.args.get('search')
        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                db.or_(
                    PartidoPolitico.nombre.ilike(search_pattern),
                    PartidoPolitico.sigla.ilike(search_pattern)
                )
            )
        
        # Ordenar
        query = query.order_by(PartidoPolitico.nombre)
        
        partidos = query.all()
        
        return jsonify({
            'success': True,
            'data': [p.to_dict() for p in partidos]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@partidos_bp.route('/<int:partido_id>', methods=['GET'])
@jwt_required()
def obtener_partido(partido_id):
    """Obtener un partido específico"""
    try:
        partido = PartidoPolitico.query.get(partido_id)
        
        if not partido:
            return jsonify({
                'success': False,
                'error': 'Partido no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': partido.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@partidos_bp.route('', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def crear_partido():
    """
    Crear un nuevo partido político
    Body:
        nombre: Nombre completo del partido
        sigla: Sigla del partido
        color: Color en formato hex (#RRGGBB)
        descripcion: Descripción opcional
        activo: Estado activo (default: true)
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data.get('nombre'):
            return jsonify({
                'success': False,
                'error': 'El nombre es requerido'
            }), 400
        
        if not data.get('sigla'):
            return jsonify({
                'success': False,
                'error': 'La sigla es requerida'
            }), 400
        
        # Validar color
        color = data.get('color', '#000000')
        if not PartidoPolitico.validar_color(color):
            return jsonify({
                'success': False,
                'error': 'Color inválido. Use formato hex: #RRGGBB'
            }), 400
        
        # Verificar que no exista
        existe = PartidoPolitico.query.filter(
            db.or_(
                PartidoPolitico.nombre == data['nombre'],
                PartidoPolitico.sigla == data['sigla']
            )
        ).first()
        
        if existe:
            return jsonify({
                'success': False,
                'error': 'Ya existe un partido con ese nombre o sigla'
            }), 400
        
        # Crear partido
        partido = PartidoPolitico(
            nombre=data['nombre'],
            sigla=data['sigla'],
            color=color,
            descripcion=data.get('descripcion'),
            activo=data.get('activo', True)
        )
        
        db.session.add(partido)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Partido creado exitosamente',
            'data': partido.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@partidos_bp.route('/<int:partido_id>', methods=['PUT'])
@jwt_required()
@role_required(['super_admin'])
def actualizar_partido(partido_id):
    """Actualizar un partido político"""
    try:
        partido = PartidoPolitico.query.get(partido_id)
        
        if not partido:
            return jsonify({
                'success': False,
                'error': 'Partido no encontrado'
            }), 404
        
        data = request.get_json()
        
        # Validar color si se proporciona
        if 'color' in data and not PartidoPolitico.validar_color(data['color']):
            return jsonify({
                'success': False,
                'error': 'Color inválido. Use formato hex: #RRGGBB'
            }), 400
        
        # Verificar unicidad de nombre y sigla
        if 'nombre' in data or 'sigla' in data:
            existe = PartidoPolitico.query.filter(
                PartidoPolitico.id != partido_id,
                db.or_(
                    PartidoPolitico.nombre == data.get('nombre', partido.nombre),
                    PartidoPolitico.sigla == data.get('sigla', partido.sigla)
                )
            ).first()
            
            if existe:
                return jsonify({
                    'success': False,
                    'error': 'Ya existe otro partido con ese nombre o sigla'
                }), 400
        
        # Actualizar campos
        if 'nombre' in data:
            partido.nombre = data['nombre']
        if 'sigla' in data:
            partido.sigla = data['sigla']
        if 'color' in data:
            partido.color = data['color']
        if 'descripcion' in data:
            partido.descripcion = data['descripcion']
        if 'activo' in data:
            partido.activo = data['activo']
        if 'logo_url' in data:
            partido.logo_url = data['logo_url']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Partido actualizado exitosamente',
            'data': partido.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@partidos_bp.route('/<int:partido_id>', methods=['DELETE'])
@jwt_required()
@role_required(['super_admin'])
def eliminar_partido(partido_id):
    """Eliminar un partido político"""
    try:
        partido = PartidoPolitico.query.get(partido_id)
        
        if not partido:
            return jsonify({
                'success': False,
                'error': 'Partido no encontrado'
            }), 404
        
        # Verificar que no tenga candidatos asociados
        if partido.candidatos.count() > 0:
            return jsonify({
                'success': False,
                'error': f'No se puede eliminar. El partido tiene {partido.candidatos.count()} candidato(s) asociado(s)'
            }), 400
        
        db.session.delete(partido)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Partido eliminado exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@partidos_bp.route('/export', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def exportar_partidos():
    """Exportar todos los partidos en formato JSON"""
    try:
        partidos = PartidoPolitico.query.order_by(PartidoPolitico.nombre).all()
        
        return jsonify({
            'success': True,
            'data': [p.to_dict() for p in partidos],
            'total': len(partidos)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



@partidos_bp.route('/<int:partido_id>/logo', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def subir_logo_partido(partido_id):
    """
    Subir logo de un partido político
    Form data:
        logo: Archivo de imagen (png, jpg, jpeg, webp, svg)
    """
    try:
        from backend.services.partido_service import PartidoService
        from backend.services.upload_service import UploadService
        import os
        from flask import current_app
        
        partido = PartidoPolitico.query.get(partido_id)
        
        if not partido:
            return jsonify({
                'success': False,
                'error': 'Partido no encontrado'
            }), 404
        
        # Verificar que se envió un archivo
        if 'logo' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó archivo'
            }), 400
        
        archivo = request.files['logo']
        
        if archivo.filename == '':
            return jsonify({
                'success': False,
                'error': 'No se seleccionó archivo'
            }), 400
        
        # Validar archivo
        valid, error = PartidoService.validar_logo(archivo)
        if not valid:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        # Guardar archivo
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'frontend/static/uploads')
        partidos_folder = os.path.join(upload_folder, 'partidos')
        
        # Crear directorio si no existe
        os.makedirs(partidos_folder, exist_ok=True)
        
        # Generar nombre único
        extension = archivo.filename.rsplit('.', 1)[1].lower()
        filename = f"partido_{partido_id}_{partido.sigla.lower()}.{extension}"
        filepath = os.path.join(partidos_folder, filename)
        
        # Guardar archivo
        archivo.save(filepath)
        
        # Actualizar URL en base de datos
        logo_url = f"/static/uploads/partidos/{filename}"
        partido.logo_url = logo_url
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Logo subido exitosamente',
            'data': {
                'logo_url': logo_url,
                'partido': partido.to_dict()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
