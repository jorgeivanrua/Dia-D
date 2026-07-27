"""
Endpoints para geolocalización de ubicaciones (puestos, mesas, etc.)
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.location import Location
from backend.models.formulario_e14 import FormularioE14
from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
from backend.database import db
from backend.utils.decorators import role_required

locations_geo_bp = Blueprint('locations_geo', __name__, url_prefix='/api/locations')


@locations_geo_bp.route('/puestos-geolocalizados', methods=['GET'])
@jwt_required()
def obtener_puestos_geolocalizados():
    """
    Obtener puestos de votación con coordenadas geográficas
    Incluye indicadores visuales, filtros y búsqueda
    
    Query params:
        filtro_incidentes: 'true' para mostrar solo puestos con incidentes
        filtro_delitos: 'true' para mostrar solo puestos con delitos
        filtro_pendientes: 'true' para mostrar solo puestos con formularios pendientes
        busqueda: código de puesto, municipio o mesa para buscar
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Obtener parámetros de filtro y búsqueda
        filtro_incidentes = request.args.get('filtro_incidentes', '').lower() == 'true'
        filtro_delitos = request.args.get('filtro_delitos', '').lower() == 'true'
        filtro_pendientes = request.args.get('filtro_pendientes', '').lower() == 'true'
        busqueda = request.args.get('busqueda', '').strip()
        
        # Construir query base - SIEMPRE mostrar todos los puestos para referencia
        query = Location.query.filter(
            Location.tipo == 'puesto',
            Location.activo == True,
            Location.latitud.isnot(None),
            Location.longitud.isnot(None)
        )
        
        # Aplicar búsqueda si se proporciona
        if busqueda:
            query = query.filter(
                db.or_(
                    Location.puesto_codigo.ilike(f'%{busqueda}%'),
                    Location.puesto_nombre.ilike(f'%{busqueda}%'),
                    Location.municipio_nombre.ilike(f'%{busqueda}%'),
                    Location.mesa_codigo.ilike(f'%{busqueda}%')
                )
            )
        
        # NO filtrar por rol - los mapas siempre muestran todos los puestos como referencia
        # Esto permite a coordinadores, monitoreo y super admin ver el contexto completo
        # Nota: Los testigos no tienen acceso a mapas, solo registran formularios
        
        # Ejecutar query
        puestos = query.all()
        
        # Formatear respuesta con estadísticas
        puestos_data = []
        for puesto in puestos:
            # Contar mesas del puesto
            mesas = Location.query.filter_by(
                puesto_codigo=puesto.puesto_codigo,
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                zona_codigo=puesto.zona_codigo,
                tipo='mesa',
                activo=True
            ).count()
            
            # Contar formularios del puesto
            mesa_ids = [m.id for m in Location.query.filter_by(
                puesto_codigo=puesto.puesto_codigo,
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                zona_codigo=puesto.zona_codigo,
                tipo='mesa'
            ).all()]
            
            formularios_count = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids)
            ).count()
            
            formularios_validados = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids),
                FormularioE14.estado == 'validado'
            ).count()
            
            # Contar incidentes del puesto (activos = no resueltos)
            incidentes_activos = IncidenteElectoral.query.filter(
                IncidenteElectoral.puesto_id == puesto.id,
                IncidenteElectoral.estado.in_(['reportado', 'en_revision', 'escalado'])
            ).count()
            
            # Contar incidentes críticos
            incidentes_criticos = IncidenteElectoral.query.filter(
                IncidenteElectoral.puesto_id == puesto.id,
                IncidenteElectoral.severidad == 'critica',
                IncidenteElectoral.estado.in_(['reportado', 'en_revision', 'escalado'])
            ).count()
            
            # Contar delitos del puesto (activos = no archivados)
            delitos_activos = DelitoElectoral.query.filter(
                DelitoElectoral.puesto_id == puesto.id,
                DelitoElectoral.estado.in_(['reportado', 'en_investigacion', 'investigado', 'denunciado'])
            ).count()
            
            # Contar delitos graves
            delitos_graves = DelitoElectoral.query.filter(
                DelitoElectoral.puesto_id == puesto.id,
                DelitoElectoral.gravedad.in_(['grave', 'muy_grave']),
                DelitoElectoral.estado.in_(['reportado', 'en_investigacion', 'investigado', 'denunciado'])
            ).count()
            
            # Calcular formularios pendientes
            formularios_pendientes = mesas - formularios_count
            
            # Determinar indicador visual
            indicador = {
                'color': 'green',  # Por defecto verde (todo bien)
                'icono': 'check-circle',
                'animacion': None,
                'prioridad': 0
            }
            
            # Prioridad 3: Incidentes críticos (rojo pulsante)
            if incidentes_criticos > 0:
                indicador = {
                    'color': 'red',
                    'icono': 'exclamation-triangle',
                    'animacion': 'pulse',
                    'prioridad': 3
                }
            # Prioridad 2: Delitos graves (naranja)
            elif delitos_graves > 0:
                indicador = {
                    'color': 'orange',
                    'icono': 'alert-triangle',
                    'animacion': None,
                    'prioridad': 2
                }
            # Prioridad 1: Formularios pendientes (amarillo)
            elif formularios_pendientes > 0:
                indicador = {
                    'color': 'yellow',
                    'icono': 'clock',
                    'animacion': None,
                    'prioridad': 1
                }
            
            # Aplicar filtros
            incluir = True
            if filtro_incidentes and incidentes_activos == 0:
                incluir = False
            if filtro_delitos and delitos_activos == 0:
                incluir = False
            if filtro_pendientes and formularios_pendientes == 0:
                incluir = False
            
            if incluir:
                puestos_data.append({
                    'id': puesto.id,
                    'puesto_codigo': puesto.puesto_codigo,
                    'puesto_nombre': puesto.puesto_nombre,
                    'municipio_codigo': puesto.municipio_codigo,
                    'municipio_nombre': puesto.municipio_nombre,
                    'departamento_codigo': puesto.departamento_codigo,
                    'departamento_nombre': puesto.departamento_nombre,
                    'zona_codigo': puesto.zona_codigo,
                    'direccion': puesto.direccion,
                    'latitud': float(puesto.latitud),
                    'longitud': float(puesto.longitud),
                    'nombre_completo': puesto.nombre_completo,
                    'total_mesas': mesas,
                    'total_formularios': formularios_count,
                    'formularios_validados': formularios_validados,
                    'formularios_pendientes': formularios_pendientes,
                    'porcentaje_avance': round((formularios_validados / mesas * 100) if mesas > 0 else 0, 2),
                    'incidentes': {
                        'total': incidentes_activos,
                        'criticos': incidentes_criticos
                    },
                    'delitos': {
                        'total': delitos_activos,
                        'graves': delitos_graves
                    },
                    'tiene_alertas': (incidentes_activos > 0 or delitos_activos > 0),
                    'tiene_alertas_criticas': (incidentes_criticos > 0 or delitos_graves > 0),
                    'indicador_visual': indicador
                })
        
        return jsonify({
            'success': True,
            'data': puestos_data
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Error obteniendo puestos geolocalizados: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Error al obtener puestos geolocalizados: {str(e)}'
        }), 500


@locations_geo_bp.route('/mesas-geolocalizadas', methods=['GET'])
@jwt_required()
def obtener_mesas_geolocalizadas():
    """
    Obtener mesas de votación con coordenadas geográficas
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Construir query base
        query = Location.query.filter(
            Location.tipo == 'mesa',
            Location.activo == True,
            Location.latitud.isnot(None),
            Location.longitud.isnot(None)
        )
        
        # Filtrar según rol
        if user.rol == 'coordinador_puesto' and user.ubicacion_id:
            ubicacion = Location.query.get(user.ubicacion_id)
            if ubicacion:
                query = query.filter_by(
                    puesto_codigo=ubicacion.puesto_codigo,
                    municipio_codigo=ubicacion.municipio_codigo,
                    zona_codigo=ubicacion.zona_codigo
                )
        
        elif user.rol == 'coordinador_municipal' and user.ubicacion_id:
            ubicacion = Location.query.get(user.ubicacion_id)
            if ubicacion:
                query = query.filter_by(
                    municipio_codigo=ubicacion.municipio_codigo
                )
        
        # Ejecutar query
        mesas = query.all()
        
        # Formatear respuesta
        mesas_data = []
        for mesa in mesas:
            # Obtener testigo asignado
            testigo = User.query.filter_by(
                ubicacion_id=mesa.id,
                rol='testigo_electoral',
                activo=True
            ).first()
            
            # Obtener formulario
            formulario = FormularioE14.query.filter_by(mesa_id=mesa.id).first()
            
            mesas_data.append({
                'id': mesa.id,
                'mesa_codigo': mesa.mesa_codigo,
                'puesto_codigo': mesa.puesto_codigo,
                'puesto_nombre': mesa.puesto_nombre,
                'latitud': float(mesa.latitud),
                'longitud': float(mesa.longitud),
                'nombre_completo': mesa.nombre_completo,
                'testigo_asignado': testigo.nombre if testigo else None,
                'testigo_presente': testigo.presencia_verificada if testigo else False,
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
            'error': f'Error al obtener mesas geolocalizadas: {str(e)}'
        }), 500
