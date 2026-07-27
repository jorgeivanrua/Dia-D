"""
Rutas para testigos electorales
OPTIMIZADO para múltiples testigos simultáneos
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.location import Location
from backend.models.configuracion_electoral import TipoEleccion
from backend.models.partido_politico import PartidoPolitico as Partido
from backend.database import db
from backend.utils.cache import cache_result, invalidate_cache
from datetime import datetime

testigo_bp = Blueprint('testigo', __name__)


@testigo_bp.route('/info', methods=['GET'])
@jwt_required()
def get_testigo_info():
    """
    Obtener información del testigo actual
    """
    try:
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
                'error': 'Solo testigos pueden acceder a este endpoint'
            }), 403
        
        # Obtener ubicación
        ubicacion = None
        if user.ubicacion_id:
            location = Location.query.get(user.ubicacion_id)
            if location:
                ubicacion = {
                    'id': location.id,
                    'nombre_completo': location.nombre_completo,
                    'tipo': location.tipo,
                    'departamento_codigo': location.departamento_codigo,
                    'municipio_codigo': location.municipio_codigo,
                    'zona_codigo': location.zona_codigo,
                    'puesto_codigo': location.puesto_codigo,
                    'puesto_nombre': location.puesto_nombre
                }
        
        return jsonify({
            'success': True,
            'data': {
                'user': {
                    'id': user.id,
                    'nombre': user.nombre,
                    'rol': user.rol,
                    'activo': user.activo,
                    'presencia_verificada': user.presencia_verificada,
                    'presencia_verificada_at': user.presencia_verificada_at.isoformat() if user.presencia_verificada_at else None,
                    'ultimo_acceso': user.ultimo_acceso.isoformat() if user.ultimo_acceso else None
                },
                'ubicacion': ubicacion
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@testigo_bp.route('/mesa', methods=['GET'])
@jwt_required()
def get_testigo_mesa():
    """
    Obtener información de la mesa asignada al testigo
    """
    try:
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
                'error': 'Solo testigos pueden acceder a este endpoint'
            }), 403
        
        # El testigo está asignado a un puesto, no a una mesa específica
        # Obtener todas las mesas del puesto
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Testigo sin ubicación asignada'
            }), 400
        
        puesto = Location.query.get(user.ubicacion_id)
        if not puesto or puesto.tipo != 'puesto':
            return jsonify({
                'success': False,
                'error': 'Ubicación inválida'
            }), 400
        
        # Obtener mesas del puesto
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo,
            puesto_codigo=puesto.puesto_codigo,
            activo=True
        ).all()
        
        mesas_data = []
        for mesa in mesas:
            mesas_data.append({
                'id': mesa.id,
                'nombre_completo': mesa.nombre_completo,
                'mesa_codigo': mesa.mesa_codigo,
                'puesto_nombre': mesa.puesto_nombre,
                'total_votantes_registrados': mesa.total_votantes_registrados,
                'mujeres': mesa.mujeres,
                'hombres': mesa.hombres
            })
        
        return jsonify({
            'success': True,
            'data': {
                'puesto': {
                    'id': puesto.id,
                    'nombre_completo': puesto.nombre_completo,
                    'puesto_codigo': puesto.puesto_codigo,
                    'puesto_nombre': puesto.puesto_nombre
                },
                'mesas': mesas_data
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@testigo_bp.route('/tipos-eleccion', methods=['GET'])
@jwt_required()
def get_tipos_eleccion():
    """
    Obtener tipos de elección disponibles
    """
    try:
        tipos = TipoEleccion.query.filter_by(activo=True).order_by(TipoEleccion.orden).all()
        
        tipos_data = []
        for tipo in tipos:
            tipos_data.append({
                'id': tipo.id,
                'codigo': tipo.codigo,
                'nombre': tipo.nombre,
                'descripcion': tipo.descripcion,
                'es_uninominal': tipo.es_uninominal,
                'permite_lista_cerrada': tipo.permite_lista_cerrada,
                'permite_lista_abierta': tipo.permite_lista_abierta,
                'permite_coaliciones': tipo.permite_coaliciones
            })
        
        return jsonify({
            'success': True,
            'data': tipos_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@testigo_bp.route('/partidos', methods=['GET'])
@jwt_required()
def get_partidos():
    """
    Obtener partidos políticos disponibles
    """
    try:
        partidos = Partido.query.filter_by(activo=True).order_by(Partido.orden).all()
        
        partidos_data = []
        for partido in partidos:
            partidos_data.append({
                'id': partido.id,
                'sigla': partido.sigla,
                'nombre': partido.nombre,
                'color': partido.color,
                'logo_url': partido.logo_url
            })
        
        return jsonify({
            'success': True,
            'data': partidos_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@testigo_bp.route('/candidatos', methods=['GET'])
@jwt_required()
def get_candidatos():
    """
    Obtener candidatos por tipo de elección
    Query params:
        - tipo_eleccion_id: ID del tipo de elección (opcional)
    """
    try:
        from backend.models.candidato import Candidato
        
        tipo_eleccion_id = request.args.get('tipo_eleccion_id', type=int)
        
        query = Candidato.query.filter_by(activo=True)
        
        if tipo_eleccion_id:
            query = query.filter_by(tipo_eleccion_id=tipo_eleccion_id)
        
        candidatos = query.order_by(Candidato.orden).all()
        
        candidatos_data = []
        for candidato in candidatos:
            partido = Partido.query.get(candidato.partido_id) if candidato.partido_id else None
            tipo_eleccion = TipoEleccion.query.get(candidato.tipo_eleccion_id) if candidato.tipo_eleccion_id else None
            
            candidatos_data.append({
                'id': candidato.id,
                'codigo': candidato.codigo,
                'nombre_completo': candidato.nombre_completo,
                'numero_lista': candidato.numero_lista,
                'partido_id': candidato.partido_id,
                'partido_nombre': partido.nombre if partido else None,
                'partido_sigla': partido.sigla if partido else None,
                'partido_color': partido.color if partido else None,
                'tipo_eleccion_id': candidato.tipo_eleccion_id,
                'tipo_eleccion_nombre': tipo_eleccion.nombre if tipo_eleccion else None,
                'foto_url': candidato.foto_url,
                'es_independiente': candidato.es_independiente,
                'es_cabeza_lista': candidato.es_cabeza_lista
            })
        
        return jsonify({
            'success': True,
            'data': candidatos_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@testigo_bp.route('/registrar-presencia', methods=['POST'])
@jwt_required()
def registrar_presencia():
    """
    Registrar presencia del testigo en la mesa
    """
    try:
        from datetime import datetime
        
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
        
        data = request.get_json()
        mesa_id = data.get('mesa_id')
        
        if not mesa_id:
            return jsonify({
                'success': False,
                'error': 'Se requiere el ID de la mesa'
            }), 400
        
        # Verificar que la mesa exista
        mesa = Location.query.get(mesa_id)
        if not mesa:
            return jsonify({
                'success': False,
                'error': 'Mesa no encontrada'
            }), 404
        
        # Obtener el puesto del testigo
        puesto_testigo = Location.query.get(user.ubicacion_id)
        if not puesto_testigo:
            return jsonify({
                'success': False,
                'error': 'No tienes un puesto asignado'
            }), 400
        
        # Verificar que la mesa pertenezca al puesto del testigo
        if (mesa.departamento_codigo != puesto_testigo.departamento_codigo or
            mesa.municipio_codigo != puesto_testigo.municipio_codigo or
            mesa.zona_codigo != puesto_testigo.zona_codigo or
            mesa.puesto_codigo != puesto_testigo.puesto_codigo):
            return jsonify({
                'success': False,
                'error': 'Esta mesa no pertenece a tu puesto asignado'
            }), 403
        
        # Registrar presencia y actualizar ubicación del testigo a la mesa específica
        user.presencia_verificada = True
        user.presencia_verificada_at = datetime.now()
        user.ubicacion_id = mesa_id  # Actualizar ubicación del testigo a la mesa
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Presencia verificada exitosamente',
            'data': {
                'presencia_verificada': True,
                'presencia_verificada_at': user.presencia_verificada_at.isoformat(),
                'mesa_id': mesa_id,
                'mesa_nombre': mesa.nombre_completo,
                'ubicacion_actualizada': True
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@testigo_bp.route('/mesas-puesto', methods=['GET'])
@jwt_required()
def get_mesas_puesto_testigo():
    """
    Obtener mesas del puesto del testigo con información de estado
    Endpoint específico para testigos con filtrado automático
    """
    try:
        from backend.models.formulario_e14 import FormularioE14
        
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
                'error': 'Solo testigos pueden acceder a este endpoint'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'No tienes ubicación asignada'
            }), 400
        
        # Obtener ubicación del testigo
        ubicacion = Location.query.get(user.ubicacion_id)
        
        # Si ya verificó presencia, su ubicación es una mesa
        # Obtener el puesto de esa mesa
        puesto = ubicacion
        if ubicacion.tipo == 'mesa':
            puesto = Location.query.filter_by(
                tipo='puesto',
                departamento_codigo=ubicacion.departamento_codigo,
                municipio_codigo=ubicacion.municipio_codigo,
                zona_codigo=ubicacion.zona_codigo,
                puesto_codigo=ubicacion.puesto_codigo
            ).first()
        
        if not puesto:
            return jsonify({
                'success': False,
                'error': 'No se pudo determinar el puesto'
            }), 400
        
        # Obtener todas las mesas del puesto
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo,
            puesto_codigo=puesto.puesto_codigo,
            activo=True
        ).all()
        
        # Agregar información de estado de cada mesa
        mesas_data = []
        for mesa in mesas:
            # Verificar si hay formulario para esta mesa del testigo
            formulario = FormularioE14.query.filter_by(
                mesa_id=mesa.id,
                testigo_id=user.id
            ).first()
            
            mesa_dict = mesa.to_dict()
            mesa_dict['tiene_formulario'] = formulario is not None
            mesa_dict['estado_formulario'] = formulario.estado if formulario else None
            mesa_dict['puede_crear_formulario'] = (
                user.presencia_verificada and 
                user.ubicacion_id == mesa.id
            )
            mesa_dict['es_mi_mesa'] = user.ubicacion_id == mesa.id
            
            mesas_data.append(mesa_dict)
        
        return jsonify({
            'success': True,
            'data': mesas_data,
            'puesto': {
                'nombre': puesto.puesto_nombre,
                'codigo': puesto.puesto_codigo,
                'total_mesas': len(mesas)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

