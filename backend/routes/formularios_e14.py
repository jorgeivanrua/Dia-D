"""
Rutas para gestión de formularios E-14
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.formulario_service import FormularioService
from backend.services.validacion_service import ValidacionService
from backend.services.consolidado_service import ConsolidadoService
from backend.models.user import User
from backend.models.location import Location
from backend.utils.exceptions import BaseAPIException
from backend.utils.decorators import role_required

formularios_bp = Blueprint('formularios', __name__, url_prefix='/api/formularios')


@formularios_bp.route('/todos', methods=['GET'])
@jwt_required()
@role_required(['super_admin', 'monitoreo', 'auditor_electoral'])
def obtener_todos_formularios():
    """
    Obtener todos los formularios E-14 del sistema
    Para roles de monitoreo, super admin y auditor
    
    Query params:
        estado: Filtrar por estado (opcional)
        municipio_codigo: Filtrar por municipio (opcional)
        tipo_eleccion_id: Filtrar por tipo de elección (opcional)
        page: Número de página (default: 1)
        per_page: Resultados por página (default: 100)
    """
    try:
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.candidato import Candidato
        from backend.models.partido_politico import PartidoPolitico as Partido
        from backend.models.configuracion_electoral import TipoEleccion
        
        # Obtener parámetros de query
        estado = request.args.get('estado')
        municipio_codigo = request.args.get('municipio_codigo')
        tipo_eleccion_id = request.args.get('tipo_eleccion_id', type=int)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 100, type=int)
        
        # Construir query
        query = FormularioE14.query
        
        # Aplicar filtros
        if estado:
            query = query.filter_by(estado=estado)
        
        if tipo_eleccion_id:
            query = query.filter_by(tipo_eleccion_id=tipo_eleccion_id)
        
        if municipio_codigo:
            # Filtrar por municipio a través de la mesa
            query = query.join(Location, FormularioE14.mesa_id == Location.id)\
                        .filter(Location.municipio_codigo == municipio_codigo)
        
        # Ordenar por fecha de creación (más recientes primero)
        query = query.order_by(FormularioE14.created_at.desc())
        
        # Obtener todos los formularios (sin paginación para el dashboard)
        formularios = query.all()
        
        # Serializar formularios con información completa
        formularios_data = []
        for form in formularios:
            # Obtener votos por partido
            votos_partidos = []
            for vp in form.votos_partidos:
                votos_partidos.append({
                    'partido_id': vp.partido_id,
                    'partido': {
                        'id': vp.partido.id,
                        'nombre': vp.partido.nombre,
                        'sigla': vp.partido.sigla,
                        'color': vp.partido.color
                    } if vp.partido else None,
                    'votos': vp.votos
                })
            
            formularios_data.append({
                'id': form.id,
                'mesa_id': form.mesa_id,
                'mesa': {
                    'id': form.mesa.id,
                    'mesa_nombre': form.mesa.mesa_nombre,
                    'puesto_nombre': form.mesa.puesto_nombre,
                    'municipio_nombre': form.mesa.municipio_nombre,
                    'departamento_nombre': form.mesa.departamento_nombre,
                    'zona_codigo': form.mesa.zona_codigo,
                    'puesto_codigo': form.mesa.puesto_codigo
                } if form.mesa else None,
                'testigo_id': form.testigo_id,
                'testigo': {
                    'id': form.testigo.id,
                    'nombre': form.testigo.nombre
                } if form.testigo else None,
                'tipo_eleccion_id': form.tipo_eleccion_id,
                'tipo_eleccion': {
                    'id': form.tipo_eleccion.id,
                    'nombre': form.tipo_eleccion.nombre,
                    'codigo': form.tipo_eleccion.codigo
                } if form.tipo_eleccion else None,
                'total_votos': form.total_votos,
                'votos_validos': form.votos_validos,
                'votos_nulos': form.votos_nulos,
                'votos_blanco': form.votos_blanco,
                'votos_partidos': votos_partidos,
                'estado': form.estado,
                'observaciones': form.observaciones,
                'created_at': form.created_at.isoformat() if form.created_at else None,
                'updated_at': form.updated_at.isoformat() if form.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'data': formularios_data,
            'total': len(formularios_data)
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Error obteniendo todos los formularios: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@formularios_bp.route('/puesto', methods=['GET'])
@jwt_required()
@role_required(['coordinador_puesto'])
def obtener_formularios_puesto():
    """
    Obtener formularios del puesto del coordinador
    
    Query params:
        estado: Filtrar por estado (opcional)
        page: Número de página (default: 1)
        per_page: Resultados por página (default: 20)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        # Obtener ubicación del coordinador (debe ser un puesto)
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'puesto':
            return jsonify({
                'success': False,
                'error': 'Coordinador no asignado a un puesto válido'
            }), 400
        
        # Obtener parámetros de query
        estado = request.args.get('estado')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Construir filtros
        filtros = {}
        if estado:
            filtros['estado'] = estado
        
        # Obtener formularios
        resultado = FormularioService.obtener_formularios_por_puesto(
            ubicacion.id,
            filtros=filtros,
            page=page,
            per_page=per_page
        )
        
        return jsonify({
            'success': True,
            'data': resultado
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@formularios_bp.route('/<int:formulario_id>', methods=['GET'])
@jwt_required()
@role_required(['coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental', 'auditor_electoral', 'super_admin'])
def obtener_formulario(formulario_id):
    """
    Obtener detalles completos de un formulario
    
    Path params:
        formulario_id: ID del formulario
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        # Obtener formulario con todos los detalles
        formulario_data = FormularioService.obtener_formulario_por_id(
            formulario_id,
            include_votos=True,
            include_historial=True
        )
        
        # Verificar permisos según rol
        # TODO: Implementar verificación de permisos por rol y ubicación
        
        return jsonify({
            'success': True,
            'data': formulario_data
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@formularios_bp.route('/<int:formulario_id>/validar', methods=['PUT'])
@jwt_required()
@role_required(['coordinador_puesto'])
def validar_formulario(formulario_id):
    """
    Validar un formulario E-14
    
    Path params:
        formulario_id: ID del formulario
        
    Body:
        cambios: Diccionario opcional con cambios a aplicar
        comentario: Comentario opcional del coordinador
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        
        cambios = data.get('cambios')
        comentario = data.get('comentario')
        
        # Validar formulario
        formulario = ValidacionService.validar_formulario(
            formulario_id,
            int(user_id),
            cambios=cambios,
            comentario=comentario
        )
        
        return jsonify({
            'success': True,
            'message': 'Formulario validado exitosamente',
            'data': formulario.to_dict(include_votos=True)
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@formularios_bp.route('/<int:formulario_id>/rechazar', methods=['PUT'])
@jwt_required()
@role_required(['coordinador_puesto'])
def rechazar_formulario(formulario_id):
    """
    Rechazar un formulario E-14
    
    Path params:
        formulario_id: ID del formulario
        
    Body:
        motivo: Motivo del rechazo (obligatorio)
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'motivo' not in data:
            return jsonify({
                'success': False,
                'error': 'El motivo de rechazo es obligatorio'
            }), 400
        
        motivo = data['motivo']
        
        # Rechazar formulario
        formulario = ValidacionService.rechazar_formulario(
            formulario_id,
            int(user_id),
            motivo
        )
        
        return jsonify({
            'success': True,
            'message': 'Formulario rechazado',
            'data': formulario.to_dict()
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@formularios_bp.route('/consolidado', methods=['GET'])
@jwt_required()
@role_required(['coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental'])
def obtener_consolidado():
    """
    Obtener consolidado del puesto/municipio del coordinador
    
    Query params:
        tipo_eleccion_id: ID del tipo de elección (opcional)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        ubicacion = Location.query.get(user.ubicacion_id)
        tipo_eleccion_id = request.args.get('tipo_eleccion_id', type=int)
        
        # Calcular consolidado según el tipo de ubicación
        if ubicacion.tipo == 'puesto':
            consolidado = ConsolidadoService.calcular_consolidado_puesto(
                ubicacion.id,
                tipo_eleccion_id=tipo_eleccion_id
            )
        elif ubicacion.tipo == 'municipio':
            consolidado = ConsolidadoService.calcular_consolidado_municipal(
                ubicacion.id,
                tipo_eleccion_id=tipo_eleccion_id
            )
        else:
            return jsonify({
                'success': False,
                'error': 'Tipo de ubicación no soportado para consolidado'
            }), 400
        
        if not consolidado:
            return jsonify({
                'success': False,
                'error': 'No se pudo calcular el consolidado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': consolidado
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@formularios_bp.route('/mesas', methods=['GET'])
@jwt_required()
@role_required(['coordinador_puesto'])
def obtener_mesas_puesto():
    """
    Obtener lista de mesas del puesto con estado de reporte
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'puesto':
            return jsonify({
                'success': False,
                'error': 'Coordinador no asignado a un puesto válido'
            }), 400
        
        # Obtener todas las mesas del puesto (filtrar por jerarquía completa)
        print(f"DEBUG - Filtrando mesas con:")
        print(f"  puesto_codigo: {ubicacion.puesto_codigo}")
        print(f"  departamento_codigo: {ubicacion.departamento_codigo}")
        print(f"  municipio_codigo: {ubicacion.municipio_codigo}")
        print(f"  zona_codigo: {ubicacion.zona_codigo}")
        
        mesas = Location.query.filter_by(
            puesto_codigo=ubicacion.puesto_codigo,
            tipo='mesa',
            departamento_codigo=ubicacion.departamento_codigo,
            municipio_codigo=ubicacion.municipio_codigo,
            zona_codigo=ubicacion.zona_codigo
        ).all()
        
        print(f"DEBUG - Mesas encontradas: {len(mesas)}")
        
        # Para cada mesa, obtener información del testigo y estado del formulario
        resultado = []
        for mesa in mesas:
            # Buscar testigo asignado a esta mesa
            testigo = User.query.filter_by(
                ubicacion_id=mesa.id,
                rol='testigo_electoral'
            ).first()
            
            # Buscar formulario más reciente de esta mesa
            from backend.models.formulario_e14 import FormularioE14
            formulario = FormularioE14.query.filter_by(
                mesa_id=mesa.id
            ).order_by(FormularioE14.created_at.desc()).first()
            
            mesa_data = {
                'mesa_id': mesa.id,
                'mesa_codigo': mesa.mesa_codigo,
                'mesa_nombre': mesa.nombre_completo,
                'total_votantes_registrados': mesa.total_votantes_registrados,
                'testigo_id': testigo.id if testigo else None,
                'testigo_nombre': testigo.nombre if testigo else None,
                'testigo_presente': testigo.presencia_verificada if testigo else False,
                'testigo_presente_desde': testigo.presencia_verificada_at.isoformat() if testigo and testigo.presencia_verificada_at else None,
                'tiene_formulario': formulario is not None,
                'estado_formulario': formulario.estado if formulario else None,
                'ultima_actualizacion': formulario.updated_at.isoformat() if formulario else None,
                # Datos del formulario para E-24
                'formulario_id': formulario.id if formulario else None,
                'total_votos': formulario.total_votos if formulario and formulario.estado == 'validado' else 0,
                'votos_validos': formulario.votos_validos if formulario and formulario.estado == 'validado' else 0,
                'votos_nulos': formulario.votos_nulos if formulario and formulario.estado == 'validado' else 0,
                'votos_blanco': formulario.votos_blanco if formulario and formulario.estado == 'validado' else 0
            }
            
            resultado.append(mesa_data)
        
        return jsonify({
            'success': True,
            'data': resultado
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@formularios_bp.route('/mis-formularios', methods=['GET'])
@jwt_required()
@role_required(['testigo_electoral'])
def obtener_mis_formularios():
    """
    Obtener formularios del testigo actual
    
    Query params:
        mesa_id: Filtrar por mesa (opcional)
        estado: Filtrar por estado (opcional)
        page: Número de página (default: 1)
        per_page: Resultados por página (default: 20)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Obtener parámetros de query
        mesa_id = request.args.get('mesa_id', type=int)
        estado = request.args.get('estado')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Construir filtros
        filtros = {'testigo_id': int(user_id)}
        if mesa_id:
            filtros['mesa_id'] = mesa_id
        if estado:
            filtros['estado'] = estado
        
        # Obtener formularios del testigo
        from backend.models.formulario_e14 import FormularioE14
        query = FormularioE14.query.filter_by(testigo_id=int(user_id))
        
        if mesa_id:
            query = query.filter_by(mesa_id=mesa_id)
        if estado:
            query = query.filter_by(estado=estado)
        
        # Paginar
        pagination = query.order_by(FormularioE14.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        formularios = [f.to_dict(include_votos=False) for f in pagination.items]
        
        return jsonify({
            'success': True,
            'data': {
                'formularios': formularios,
                'pagination': {
                    'page': pagination.page,
                    'per_page': pagination.per_page,
                    'total': pagination.total,
                    'pages': pagination.pages
                }
            }
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@formularios_bp.route('', methods=['POST'])
@jwt_required()
@role_required(['testigo_electoral'])
def crear_formulario():
    """
    Crear un nuevo formulario E-14
    
    Body:
        mesa_id: ID de la mesa
        tipo_eleccion_id: ID del tipo de elección
        total_votantes_registrados: Total de votantes registrados
        total_votos: Total de votos
        votos_validos: Votos válidos
        votos_nulos: Votos nulos
        votos_blanco: Votos en blanco
        tarjetas_no_marcadas: Tarjetas no marcadas
        total_tarjetas: Total de tarjetas
        estado: Estado del formulario (borrador/pendiente)
        observaciones: Observaciones (opcional)
        votos_partidos: Lista de votos por partido
        votos_candidatos: Lista de votos por candidato
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        # Crear formulario
        formulario = FormularioService.crear_formulario(data, int(user_id))
        
        return jsonify({
            'success': True,
            'message': 'Formulario creado exitosamente',
            'data': formulario.to_dict(include_votos=True)
        }), 201
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@formularios_bp.route('/<int:formulario_id>', methods=['PUT'])
@jwt_required()
@role_required(['testigo_electoral', 'coordinador_puesto'])
def actualizar_formulario(formulario_id):
    """
    Actualizar un formulario E-14
    
    Path params:
        formulario_id: ID del formulario
        
    Body:
        Campos a actualizar
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        # Actualizar formulario
        formulario = FormularioService.actualizar_formulario(
            formulario_id,
            data,
            int(user_id)
        )
        
        return jsonify({
            'success': True,
            'message': 'Formulario actualizado exitosamente',
            'data': formulario.to_dict(include_votos=True)
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



@formularios_bp.route('/testigos-puesto', methods=['GET'])
@jwt_required()
def obtener_testigos_puesto():
    """
    Obtener lista de testigos del puesto con su estado de presencia
    Solo para coordinadores de puesto
    """
    try:
        from backend.models.location import Location
        
        user_id = get_jwt_identity()
        coordinador = User.query.get(int(user_id))
        
        if not coordinador or coordinador.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'Solo coordinadores de puesto pueden acceder'
            }), 403
        
        if not coordinador.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Coordinador sin ubicación asignada'
            }), 400
        
        # Obtener el puesto del coordinador
        puesto = Location.query.get(coordinador.ubicacion_id)
        
        if not puesto or puesto.tipo != 'puesto':
            return jsonify({
                'success': False,
                'error': 'Coordinador no asignado a un puesto válido'
            }), 400
        
        # Obtener todas las mesas del puesto
        mesas = Location.query.filter_by(
            puesto_codigo=puesto.puesto_codigo,
            tipo='mesa',
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo
        ).all()
        
        # Obtener IDs de las mesas
        mesa_ids = [mesa.id for mesa in mesas]
        
        # Obtener testigos asignados a cualquiera de las mesas del puesto
        testigos = User.query.filter(
            User.ubicacion_id.in_(mesa_ids),
            User.rol == 'testigo_electoral',
            User.activo == True
        ).all()
        
        testigos_data = []
        for testigo in testigos:
            # Obtener la mesa asignada al testigo
            mesa = Location.query.get(testigo.ubicacion_id)
            
            testigos_data.append({
                'id': testigo.id,
                'nombre': testigo.nombre,
                'presencia_verificada': testigo.presencia_verificada,
                'presencia_verificada_at': testigo.presencia_verificada_at.isoformat() if testigo.presencia_verificada_at else None,
                'ultimo_acceso': testigo.ultimo_acceso.isoformat() if testigo.ultimo_acceso else None,
                'mesa_id': mesa.id if mesa else None,
                'mesa_codigo': mesa.mesa_codigo if mesa else None,
                'telefono': None  # Agregar campo teléfono si existe en el modelo
            })
        
        return jsonify({
            'success': True,
            'data': testigos_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================
# ENDPOINTS DE EXPORTACIÓN Y GENERACIÓN E-24
# ============================================

@formularios_bp.route('/puesto/exportar', methods=['GET'])
@jwt_required()
@role_required(['coordinador_puesto'])
def exportar_formularios_puesto():
    """
    Exportar formularios del puesto en diferentes formatos (CSV, Excel, PDF)
    Query params:
        formato: csv, excel, pdf (default: csv)
    """
    try:
        from flask import send_file
        import csv
        import io
        from datetime import datetime
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.configuracion_electoral import TipoEleccion
        
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        formato = request.args.get('formato', 'csv').lower()
        
        # Obtener ubicación del coordinador
        ubicacion = Location.query.get(current_user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'puesto':
            return jsonify({
                'success': False,
                'error': 'Coordinador no asignado a un puesto válido'
            }), 400
        
        # Obtener todas las mesas del puesto
        mesas = Location.query.filter_by(
            puesto_codigo=ubicacion.puesto_codigo,
            departamento_codigo=ubicacion.departamento_codigo,
            municipio_codigo=ubicacion.municipio_codigo,
            zona_codigo=ubicacion.zona_codigo,
            tipo='mesa'
        ).all()
        
        mesa_ids = [mesa.id for mesa in mesas]
        
        # Obtener formularios del puesto
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).order_by(FormularioE14.created_at.desc()).all()
        
        if formato == 'csv':
            # Generar CSV
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Encabezados
            writer.writerow([
                'ID',
                'Mesa Código',
                'Mesa Nombre',
                'Testigo',
                'Estado',
                'Tipo Elección',
                'Votantes Registrados',
                'Total Votos',
                'Votos Válidos',
                'Votos Nulos',
                'Votos Blanco',
                'Participación %',
                'Fecha Creación',
                'Validado Por',
                'Fecha Validación'
            ])
            
            # Datos
            for formulario in formularios:
                mesa = Location.query.get(formulario.mesa_id)
                testigo = User.query.get(formulario.testigo_id)
                validador = User.query.get(formulario.validado_por) if formulario.validado_por else None
                tipo_eleccion = TipoEleccion.query.get(formulario.tipo_eleccion_id) if formulario.tipo_eleccion_id else None
                
                participacion = 0
                if formulario.votantes_registrados and formulario.votantes_registrados > 0:
                    participacion = round((formulario.total_votos_candidatos / formulario.votantes_registrados) * 100, 2)
                
                writer.writerow([
                    formulario.id,
                    mesa.mesa_codigo if mesa else 'N/A',
                    mesa.nombre_completo if mesa else 'N/A',
                    testigo.nombre if testigo else 'N/A',
                    formulario.estado,
                    tipo_eleccion.nombre if tipo_eleccion else 'N/A',
                    formulario.votantes_registrados or 0,
                    formulario.total_votos_candidatos or 0,
                    formulario.votos_validos or 0,
                    formulario.votos_nulos or 0,
                    formulario.votos_blanco or 0,
                    participacion,
                    formulario.created_at.strftime('%Y-%m-%d %H:%M:%S') if formulario.created_at else '',
                    validador.nombre if validador else '',
                    formulario.validado_at.strftime('%Y-%m-%d %H:%M:%S') if formulario.validado_at else ''
                ])
            
            # Preparar respuesta
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8-sig')),  # UTF-8 con BOM para Excel
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'formularios_puesto_{ubicacion.puesto_codigo}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            )
            
        elif formato == 'excel':
            try:
                import pandas as pd
                from openpyxl import Workbook
                from openpyxl.styles import Font, PatternFill, Alignment
                
                # Preparar datos para DataFrame
                data = []
                for formulario in formularios:
                    mesa = Location.query.get(formulario.mesa_id)
                    testigo = User.query.get(formulario.testigo_id)
                    validador = User.query.get(formulario.validado_por) if formulario.validado_por else None
                    tipo_eleccion = TipoEleccion.query.get(formulario.tipo_eleccion_id) if formulario.tipo_eleccion_id else None
                    
                    participacion = 0
                    if formulario.votantes_registrados and formulario.votantes_registrados > 0:
                        participacion = round((formulario.total_votos_candidatos / formulario.votantes_registrados) * 100, 2)
                    
                    data.append({
                        'ID': formulario.id,
                        'Mesa Código': mesa.mesa_codigo if mesa else 'N/A',
                        'Mesa Nombre': mesa.nombre_completo if mesa else 'N/A',
                        'Testigo': testigo.nombre if testigo else 'N/A',
                        'Estado': formulario.estado,
                        'Tipo Elección': tipo_eleccion.nombre if tipo_eleccion else 'N/A',
                        'Votantes Registrados': formulario.votantes_registrados or 0,
                        'Total Votos': formulario.total_votos_candidatos or 0,
                        'Votos Válidos': formulario.votos_validos or 0,
                        'Votos Nulos': formulario.votos_nulos or 0,
                        'Votos Blanco': formulario.votos_blanco or 0,
                        'Participación %': participacion,
                        'Fecha Creación': formulario.created_at.strftime('%Y-%m-%d %H:%M:%S') if formulario.created_at else '',
                        'Validado Por': validador.nombre if validador else '',
                        'Fecha Validación': formulario.validado_at.strftime('%Y-%m-%d %H:%M:%S') if formulario.validado_at else ''
                    })
                
                # Crear DataFrame
                df = pd.DataFrame(data)
                
                # Guardar en memoria
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Formularios', index=False)
                    
                    # Obtener el workbook y worksheet para aplicar estilos
                    workbook = writer.book
                    worksheet = writer.sheets['Formularios']
                    
                    # Aplicar estilos al encabezado
                    for cell in worksheet[1]:
                        cell.font = Font(bold=True, color="FFFFFF")
                        cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                        cell.alignment = Alignment(horizontal="center", vertical="center")
                    
                    # Ajustar ancho de columnas
                    for column in worksheet.columns:
                        max_length = 0
                        column_letter = column[0].column_letter
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(cell.value)
                            except:
                                pass
                        adjusted_width = min(max_length + 2, 50)
                        worksheet.column_dimensions[column_letter].width = adjusted_width
                
                output.seek(0)
                
                return send_file(
                    output,
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    as_attachment=True,
                    download_name=f'formularios_puesto_{ubicacion.puesto_codigo}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
                )
                
            except ImportError as e:
                return jsonify({
                    'success': False,
                    'error': f'Dependencias no instaladas: {str(e)}. Use formato CSV.'
                }), 400
                
        elif formato == 'pdf':
            try:
                from reportlab.lib.pagesizes import letter, A4, landscape
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib import colors
                from reportlab.lib.units import inch
                
                # Crear PDF en memoria
                buffer = io.BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), topMargin=0.5*inch, bottomMargin=0.5*inch)
                
                # Estilos
                styles = getSampleStyleSheet()
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=16,
                    textColor=colors.HexColor('#366092'),
                    spaceAfter=12,
                    alignment=1  # Center
                )
                
                # Contenido
                story = []
                
                # Título
                title = Paragraph(f"Formularios E-14 - Puesto {ubicacion.puesto_codigo}", title_style)
                story.append(title)
                story.append(Spacer(1, 12))
                
                # Información del puesto
                info_text = f"<b>Puesto:</b> {ubicacion.puesto_nombre}<br/><b>Fecha:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/><b>Total Formularios:</b> {len(formularios)}"
                info = Paragraph(info_text, styles['Normal'])
                story.append(info)
                story.append(Spacer(1, 12))
                
                # Tabla de datos
                data = [['Mesa', 'Testigo', 'Estado', 'Tipo', 'Votos Válidos', 'Part. %']]
                
                for formulario in formularios:
                    mesa = Location.query.get(formulario.mesa_id)
                    testigo = User.query.get(formulario.testigo_id)
                    tipo_eleccion = TipoEleccion.query.get(formulario.tipo_eleccion_id) if formulario.tipo_eleccion_id else None
                    
                    participacion = 0
                    if formulario.votantes_registrados and formulario.votantes_registrados > 0:
                        participacion = round((formulario.total_votos_candidatos / formulario.votantes_registrados) * 100, 2)
                    
                    data.append([
                        mesa.mesa_codigo if mesa else 'N/A',
                        testigo.nombre[:20] if testigo else 'N/A',  # Truncar nombre
                        formulario.estado,
                        tipo_eleccion.nombre[:15] if tipo_eleccion else 'N/A',
                        str(formulario.votos_validos or 0),
                        f"{participacion}%"
                    ])
                
                table = Table(data, repeatRows=1)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#366092')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
                ]))
                
                story.append(table)
                
                # Construir PDF
                doc.build(story)
                buffer.seek(0)
                
                return send_file(
                    buffer,
                    mimetype='application/pdf',
                    as_attachment=True,
                    download_name=f'formularios_puesto_{ubicacion.puesto_codigo}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
                )
                
            except ImportError as e:
                return jsonify({
                    'success': False,
                    'error': f'Dependencias no instaladas: {str(e)}. Use formato CSV.'
                }), 400
        
        else:
            return jsonify({
                'success': False,
                'error': f'Formato no soportado: {formato}. Use csv, excel o pdf.'
            }), 400
        
    except Exception as e:
        import traceback
        print(f"Error exportando formularios: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Error al exportar formularios: {str(e)}'
        }), 500


@formularios_bp.route('/puesto/generar-e24', methods=['POST'])
@jwt_required()
@role_required(['coordinador_puesto'])
def generar_e24_puesto():
    """
    Generar formulario E-24 consolidado del puesto
    """
    try:
        from flask import send_file
        import io
        from datetime import datetime
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.configuracion_electoral import TipoEleccion
        from backend.models.partido_politico import PartidoPolitico as Partido
        from backend.models.formulario_e14 import VotoPartido
        
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        # Obtener ubicación del coordinador
        ubicacion = Location.query.get(current_user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'puesto':
            return jsonify({
                'success': False,
                'error': 'Coordinador no asignado a un puesto válido'
            }), 400
        
        # Obtener todas las mesas del puesto
        mesas = Location.query.filter_by(
            puesto_codigo=ubicacion.puesto_codigo,
            departamento_codigo=ubicacion.departamento_codigo,
            municipio_codigo=ubicacion.municipio_codigo,
            zona_codigo=ubicacion.zona_codigo,
            tipo='mesa'
        ).all()
        
        mesa_ids = [mesa.id for mesa in mesas]
        
        # Obtener formularios validados del puesto
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids),
            FormularioE14.estado == 'validado'
        ).all()
        
        if not formularios:
            return jsonify({
                'success': False,
                'error': 'No hay formularios validados para generar E-24'
            }), 400
        
        # Consolidar datos por tipo de elección
        consolidado_por_tipo = {}
        
        for formulario in formularios:
            tipo_id = formulario.tipo_eleccion_id
            if tipo_id not in consolidado_por_tipo:
                tipo_eleccion = TipoEleccion.query.get(tipo_id)
                consolidado_por_tipo[tipo_id] = {
                    'tipo_nombre': tipo_eleccion.nombre if tipo_eleccion else 'Desconocido',
                    'total_votantes': 0,
                    'total_votos': 0,
                    'total_validos': 0,
                    'total_nulos': 0,
                    'total_blanco': 0,
                    'votos_por_partido': {},
                    'mesas_reportadas': 0
                }
            
            consolidado_por_tipo[tipo_id]['total_votantes'] += formulario.votantes_registrados or 0
            consolidado_por_tipo[tipo_id]['total_votos'] += formulario.total_votos_candidatos or 0
            consolidado_por_tipo[tipo_id]['total_validos'] += formulario.votos_validos or 0
            consolidado_por_tipo[tipo_id]['total_nulos'] += formulario.votos_nulos or 0
            consolidado_por_tipo[tipo_id]['total_blanco'] += formulario.votos_blanco or 0
            consolidado_por_tipo[tipo_id]['mesas_reportadas'] += 1
            
            # Consolidar votos por partido
            votos_partidos = VotoPartido.query.filter_by(formulario_id=formulario.id).all()
            for voto in votos_partidos:
                partido = Partido.query.get(voto.partido_id)
                if partido:
                    partido_nombre = partido.nombre
                    if partido_nombre not in consolidado_por_tipo[tipo_id]['votos_por_partido']:
                        consolidado_por_tipo[tipo_id]['votos_por_partido'][partido_nombre] = 0
                    consolidado_por_tipo[tipo_id]['votos_por_partido'][partido_nombre] += voto.votos
        
        # Crear PDF E-24
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'E24Title',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#366092'),
            spaceAfter=20,
            alignment=1,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'E24Subtitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#366092'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        
        # Contenido
        story = []
        
        # Encabezado oficial con diferenciación por nivel
        title = Paragraph("FORMULARIO E-24", title_style)
        story.append(title)
        
        subtitle = Paragraph("CONSOLIDADO DE RESULTADOS - NIVEL PUESTO DE VOTACIÓN", subtitle_style)
        story.append(subtitle)
        
        # Identificador único del E-24
        codigo_e24 = f"E24-PUESTO-{ubicacion.puesto_codigo}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        codigo_para = Paragraph(f"<b>Código:</b> {codigo_e24}", styles['Normal'])
        story.append(codigo_para)
        story.append(Spacer(1, 20))
        
        # Información del puesto
        info_data = [
            ['DEPARTAMENTO:', ubicacion.departamento_nombre or 'N/A'],
            ['MUNICIPIO:', ubicacion.municipio_nombre or 'N/A'],
            ['ZONA:', ubicacion.zona_nombre or 'N/A'],
            ['PUESTO:', f"{ubicacion.puesto_codigo} - {ubicacion.puesto_nombre}"],
            ['FECHA GENERACIÓN:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['TOTAL MESAS:', str(len(mesas))],
            ['MESAS REPORTADAS:', str(len(formularios))]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8E8E8')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Resultados por tipo de elección
        for tipo_id, datos in consolidado_por_tipo.items():
            # Título del tipo de elección
            tipo_title = Paragraph(f"<b>{datos['tipo_nombre']}</b>", subtitle_style)
            story.append(tipo_title)
            story.append(Spacer(1, 10))
            
            # Resumen general
            participacion = 0
            if datos['total_votantes'] > 0:
                participacion = round((datos['total_votos'] / datos['total_votantes']) * 100, 2)
            
            resumen_data = [
                ['CONCEPTO', 'CANTIDAD', '%'],
                ['Votantes Registrados', str(datos['total_votantes']), '100%'],
                ['Total Votos Emitidos', str(datos['total_votos']), f"{participacion}%"],
                ['Votos Válidos', str(datos['total_validos']), f"{round((datos['total_validos']/datos['total_votos']*100) if datos['total_votos'] > 0 else 0, 2)}%"],
                ['Votos Nulos', str(datos['total_nulos']), f"{round((datos['total_nulos']/datos['total_votos']*100) if datos['total_votos'] > 0 else 0, 2)}%"],
                ['Votos en Blanco', str(datos['total_blanco']), f"{round((datos['total_blanco']/datos['total_votos']*100) if datos['total_votos'] > 0 else 0, 2)}%"]
            ]
            
            resumen_table = Table(resumen_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
            resumen_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#366092')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            story.append(resumen_table)
            story.append(Spacer(1, 15))
            
            # Votos por partido
            if datos['votos_por_partido']:
                partido_title = Paragraph("<b>Votos por Partido/Candidato:</b>", styles['Heading3'])
                story.append(partido_title)
                story.append(Spacer(1, 8))
                
                partidos_data = [['PARTIDO/CANDIDATO', 'VOTOS', '% DEL TOTAL']]
                
                # Ordenar partidos por votos (descendente)
                partidos_ordenados = sorted(datos['votos_por_partido'].items(), key=lambda x: x[1], reverse=True)
                
                for partido_nombre, votos in partidos_ordenados:
                    porcentaje = round((votos / datos['total_validos'] * 100) if datos['total_validos'] > 0 else 0, 2)
                    partidos_data.append([
                        partido_nombre,
                        str(votos),
                        f"{porcentaje}%"
                    ])
                
                partidos_table = Table(partidos_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
                partidos_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
                
                story.append(partidos_table)
            
            story.append(Spacer(1, 30))
        
        # Firmas
        story.append(Spacer(1, 40))
        firmas_data = [
            ['_' * 40, '_' * 40],
            ['Coordinador de Puesto', 'Auditor Electoral'],
            [current_user.nombre, '']
        ]
        
        firmas_table = Table(firmas_data, colWidths=[3*inch, 3*inch])
        firmas_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 10),
        ]))
        
        story.append(firmas_table)
        
        # Construir PDF
        doc.build(story)
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'E24_Puesto_{ubicacion.puesto_codigo}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )
        
    except Exception as e:
        import traceback
        print(f"Error generando E-24: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Error al generar E-24: {str(e)}'
        }), 500



# ============================================
# E-24 NIVEL MUNICIPAL
# ============================================

@formularios_bp.route('/municipal/generar-e24', methods=['POST'])
@jwt_required()
@role_required(['coordinador_municipal'])
def generar_e24_municipal():
    """
    Generar formulario E-24 consolidado del municipio
    """
    try:
        from flask import send_file
        import io
        from datetime import datetime
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.configuracion_electoral import TipoEleccion
        from backend.models.partido_politico import PartidoPolitico as Partido
        from backend.models.formulario_e14 import VotoPartido
        
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        # Obtener ubicación del coordinador
        ubicacion = Location.query.get(current_user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            return jsonify({
                'success': False,
                'error': 'Coordinador no asignado a un municipio válido'
            }), 400
        
        # Obtener todos los puestos del municipio
        puestos = Location.query.filter_by(
            municipio_codigo=ubicacion.municipio_codigo,
            departamento_codigo=ubicacion.departamento_codigo,
            tipo='puesto'
        ).all()
        
        puesto_ids = [puesto.id for puesto in puestos]
        
        # Obtener todas las mesas de los puestos
        mesas = Location.query.filter(
            Location.puesto_codigo.in_([p.puesto_codigo for p in puestos]),
            Location.tipo == 'mesa',
            Location.departamento_codigo == ubicacion.departamento_codigo,
            Location.municipio_codigo == ubicacion.municipio_codigo
        ).all()
        
        mesa_ids = [mesa.id for mesa in mesas]
        
        # Obtener formularios validados del municipio
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids),
            FormularioE14.estado == 'validado'
        ).all()
        
        if not formularios:
            return jsonify({
                'success': False,
                'error': 'No hay formularios validados para generar E-24'
            }), 400
        
        # Consolidar datos por tipo de elección
        consolidado_por_tipo = {}
        
        for formulario in formularios:
            tipo_id = formulario.tipo_eleccion_id
            if tipo_id not in consolidado_por_tipo:
                tipo_eleccion = TipoEleccion.query.get(tipo_id)
                consolidado_por_tipo[tipo_id] = {
                    'tipo_nombre': tipo_eleccion.nombre if tipo_eleccion else 'Desconocido',
                    'total_votantes': 0,
                    'total_votos': 0,
                    'total_validos': 0,
                    'total_nulos': 0,
                    'total_blanco': 0,
                    'votos_por_partido': {},
                    'mesas_reportadas': 0
                }
            
            consolidado_por_tipo[tipo_id]['total_votantes'] += formulario.votantes_registrados or 0
            consolidado_por_tipo[tipo_id]['total_votos'] += formulario.total_votos_candidatos or 0
            consolidado_por_tipo[tipo_id]['total_validos'] += formulario.votos_validos or 0
            consolidado_por_tipo[tipo_id]['total_nulos'] += formulario.votos_nulos or 0
            consolidado_por_tipo[tipo_id]['total_blanco'] += formulario.votos_blanco or 0
            consolidado_por_tipo[tipo_id]['mesas_reportadas'] += 1
            
            # Consolidar votos por partido
            votos_partidos = VotoPartido.query.filter_by(formulario_id=formulario.id).all()
            for voto in votos_partidos:
                partido = Partido.query.get(voto.partido_id)
                if partido:
                    partido_nombre = partido.nombre
                    if partido_nombre not in consolidado_por_tipo[tipo_id]['votos_por_partido']:
                        consolidado_por_tipo[tipo_id]['votos_por_partido'][partido_nombre] = 0
                    consolidado_por_tipo[tipo_id]['votos_por_partido'][partido_nombre] += voto.votos
        
        # Crear PDF E-24 Municipal
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'E24Title',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#366092'),
            spaceAfter=20,
            alignment=1,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'E24Subtitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#366092'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        
        # Contenido
        story = []
        
        # Encabezado oficial - NIVEL MUNICIPAL
        title = Paragraph("FORMULARIO E-24", title_style)
        story.append(title)
        
        subtitle = Paragraph("CONSOLIDADO DE RESULTADOS - NIVEL MUNICIPAL", subtitle_style)
        story.append(subtitle)
        
        # Identificador único del E-24
        codigo_e24 = f"E24-MUNICIPAL-{ubicacion.municipio_codigo}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        codigo_para = Paragraph(f"<b>Código:</b> {codigo_e24}", styles['Normal'])
        story.append(codigo_para)
        story.append(Spacer(1, 20))
        
        # Información del municipio
        info_data = [
            ['DEPARTAMENTO:', ubicacion.departamento_nombre or 'N/A'],
            ['MUNICIPIO:', f"{ubicacion.municipio_codigo} - {ubicacion.municipio_nombre}"],
            ['FECHA GENERACIÓN:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['TOTAL PUESTOS:', str(len(puestos))],
            ['TOTAL MESAS:', str(len(mesas))],
            ['MESAS REPORTADAS:', str(len(formularios))]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8E8E8')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Resultados por tipo de elección (mismo código que puesto)
        for tipo_id, datos in consolidado_por_tipo.items():
            tipo_title = Paragraph(f"<b>{datos['tipo_nombre']}</b>", subtitle_style)
            story.append(tipo_title)
            story.append(Spacer(1, 10))
            
            participacion = 0
            if datos['total_votantes'] > 0:
                participacion = round((datos['total_votos'] / datos['total_votantes']) * 100, 2)
            
            resumen_data = [
                ['CONCEPTO', 'CANTIDAD', '%'],
                ['Votantes Registrados', str(datos['total_votantes']), '100%'],
                ['Total Votos Emitidos', str(datos['total_votos']), f"{participacion}%"],
                ['Votos Válidos', str(datos['total_validos']), f"{round((datos['total_validos']/datos['total_votos']*100) if datos['total_votos'] > 0 else 0, 2)}%"],
                ['Votos Nulos', str(datos['total_nulos']), f"{round((datos['total_nulos']/datos['total_votos']*100) if datos['total_votos'] > 0 else 0, 2)}%"],
                ['Votos en Blanco', str(datos['total_blanco']), f"{round((datos['total_blanco']/datos['total_votos']*100) if datos['total_votos'] > 0 else 0, 2)}%"]
            ]
            
            resumen_table = Table(resumen_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
            resumen_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#366092')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            story.append(resumen_table)
            story.append(Spacer(1, 15))
            
            # Votos por partido
            if datos['votos_por_partido']:
                partido_title = Paragraph("<b>Votos por Partido/Candidato:</b>", styles['Heading3'])
                story.append(partido_title)
                story.append(Spacer(1, 8))
                
                partidos_data = [['PARTIDO/CANDIDATO', 'VOTOS', '% DEL TOTAL']]
                partidos_ordenados = sorted(datos['votos_por_partido'].items(), key=lambda x: x[1], reverse=True)
                
                for partido_nombre, votos in partidos_ordenados:
                    porcentaje = round((votos / datos['total_validos'] * 100) if datos['total_validos'] > 0 else 0, 2)
                    partidos_data.append([
                        partido_nombre,
                        str(votos),
                        f"{porcentaje}%"
                    ])
                
                partidos_table = Table(partidos_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
                partidos_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
                
                story.append(partidos_table)
            
            story.append(Spacer(1, 30))
        
        # Firmas
        story.append(Spacer(1, 40))
        firmas_data = [
            ['_' * 40, '_' * 40],
            ['Coordinador Municipal', 'Auditor Electoral'],
            [current_user.nombre, '']
        ]
        
        firmas_table = Table(firmas_data, colWidths=[3*inch, 3*inch])
        firmas_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 10),
        ]))
        
        story.append(firmas_table)
        
        # Construir PDF
        doc.build(story)
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'E24_Municipal_{ubicacion.municipio_codigo}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )
        
    except Exception as e:
        import traceback
        print(f"Error generando E-24 municipal: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Error al generar E-24: {str(e)}'
        }), 500
