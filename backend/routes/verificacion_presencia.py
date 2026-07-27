"""
Sistema de verificación de presencia para todos los roles
Permite verificar que coordinadores y otros usuarios estén activos en sus ubicaciones
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.location import Location
from backend.database import db
from datetime import datetime, timedelta
from backend.utils.decorators import role_required

verificacion_bp = Blueprint('verificacion', __name__, url_prefix='/api/verificacion')


@verificacion_bp.route('/presencia', methods=['POST'])
@jwt_required()
def verificar_presencia():
    """
    Verificar presencia del usuario en su ubicación asignada
    Funciona para todos los roles: testigos, coordinadores, auditores
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Obtener datos de verificación del request
        data = request.get_json() or {}
        latitud = data.get('latitud')
        longitud = data.get('longitud')
        
        # Actualizar presencia
        user.presencia_verificada = True
        user.presencia_verificada_at = datetime.now()
        user.ultimo_acceso = datetime.now()
        
        # Guardar coordenadas si se proporcionan
        if latitud and longitud:
            user.ultima_latitud = latitud
            user.ultima_longitud = longitud
            user.ultima_geolocalizacion_at = datetime.now()
        
        db.session.commit()
        
        # Obtener información de ubicación
        ubicacion = None
        if user.ubicacion_id:
            ubicacion = Location.query.get(user.ubicacion_id)
        
        return jsonify({
            'success': True,
            'message': f'Presencia verificada exitosamente para {user.rol}',
            'data': {
                'presencia_verificada': True,
                'presencia_verificada_at': user.presencia_verificada_at.isoformat(),
                'rol': user.rol,
                'ubicacion': {
                    'id': ubicacion.id if ubicacion else None,
                    'nombre': ubicacion.nombre_completo if ubicacion else None,
                    'tipo': ubicacion.tipo if ubicacion else None
                } if ubicacion else None
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error al verificar presencia: {str(e)}'
        }), 500


@verificacion_bp.route('/estado-equipo', methods=['GET'])
@jwt_required()
@role_required(['coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental', 'super_admin'])
def obtener_estado_equipo():
    """
    Obtener estado de presencia del equipo bajo supervisión
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
        equipo = []
        
        # Según el rol, obtener el equipo correspondiente
        if user.rol == 'coordinador_puesto':
            # Obtener testigos del puesto
            mesas = Location.query.filter_by(
                puesto_codigo=ubicacion.puesto_codigo,
                departamento_codigo=ubicacion.departamento_codigo,
                municipio_codigo=ubicacion.municipio_codigo,
                zona_codigo=ubicacion.zona_codigo,
                tipo='mesa'
            ).all()
            
            mesa_ids = [mesa.id for mesa in mesas]
            testigos = User.query.filter(
                User.ubicacion_id.in_(mesa_ids),
                User.rol == 'testigo_electoral',
                User.activo == True
            ).all()
            
            for testigo in testigos:
                mesa = Location.query.get(testigo.ubicacion_id)
                equipo.append({
                    'id': testigo.id,
                    'nombre': testigo.nombre,
                    'rol': 'Testigo Electoral',
                    'ubicacion': mesa.mesa_codigo if mesa else 'N/A',
                    'presencia_verificada': testigo.presencia_verificada,
                    'presencia_verificada_at': testigo.presencia_verificada_at.isoformat() if testigo.presencia_verificada_at else None,
                    'ultimo_acceso': testigo.ultimo_acceso.isoformat() if testigo.ultimo_acceso else None,
                    'minutos_inactivo': calcular_minutos_inactivo(testigo.ultimo_acceso),
                    'estado': determinar_estado_usuario(testigo)
                })
        
        elif user.rol == 'coordinador_municipal':
            # Obtener coordinadores de puesto del municipio
            puestos = Location.query.filter_by(
                municipio_codigo=ubicacion.municipio_codigo,
                departamento_codigo=ubicacion.departamento_codigo,
                tipo='puesto'
            ).all()
            
            puesto_ids = [puesto.id for puesto in puestos]
            coordinadores = User.query.filter(
                User.ubicacion_id.in_(puesto_ids),
                User.rol == 'coordinador_puesto',
                User.activo == True
            ).all()
            
            for coord in coordinadores:
                puesto = Location.query.get(coord.ubicacion_id)
                equipo.append({
                    'id': coord.id,
                    'nombre': coord.nombre,
                    'rol': 'Coordinador de Puesto',
                    'ubicacion': f"{puesto.puesto_codigo} - {puesto.puesto_nombre}" if puesto else 'N/A',
                    'presencia_verificada': coord.presencia_verificada,
                    'presencia_verificada_at': coord.presencia_verificada_at.isoformat() if coord.presencia_verificada_at else None,
                    'ultimo_acceso': coord.ultimo_acceso.isoformat() if coord.ultimo_acceso else None,
                    'minutos_inactivo': calcular_minutos_inactivo(coord.ultimo_acceso),
                    'estado': determinar_estado_usuario(coord)
                })
        
        elif user.rol == 'coordinador_departamental':
            # Obtener coordinadores municipales del departamento
            municipios = Location.query.filter_by(
                departamento_codigo=ubicacion.departamento_codigo,
                tipo='municipio'
            ).all()
            
            municipio_ids = [mun.id for mun in municipios]
            coordinadores = User.query.filter(
                User.ubicacion_id.in_(municipio_ids),
                User.rol == 'coordinador_municipal',
                User.activo == True
            ).all()
            
            for coord in coordinadores:
                municipio = Location.query.get(coord.ubicacion_id)
                equipo.append({
                    'id': coord.id,
                    'nombre': coord.nombre,
                    'rol': 'Coordinador Municipal',
                    'ubicacion': f"{municipio.municipio_codigo} - {municipio.municipio_nombre}" if municipio else 'N/A',
                    'presencia_verificada': coord.presencia_verificada,
                    'presencia_verificada_at': coord.presencia_verificada_at.isoformat() if coord.presencia_verificada_at else None,
                    'ultimo_acceso': coord.ultimo_acceso.isoformat() if coord.ultimo_acceso else None,
                    'minutos_inactivo': calcular_minutos_inactivo(coord.ultimo_acceso),
                    'estado': determinar_estado_usuario(coord)
                })
        
        elif user.rol == 'super_admin':
            # Obtener todos los coordinadores departamentales
            coordinadores = User.query.filter_by(
                rol='coordinador_departamental',
                activo=True
            ).all()
            
            for coord in coordinadores:
                depto = Location.query.get(coord.ubicacion_id) if coord.ubicacion_id else None
                equipo.append({
                    'id': coord.id,
                    'nombre': coord.nombre,
                    'rol': 'Coordinador Departamental',
                    'ubicacion': f"{depto.departamento_codigo} - {depto.departamento_nombre}" if depto else 'N/A',
                    'presencia_verificada': coord.presencia_verificada,
                    'presencia_verificada_at': coord.presencia_verificada_at.isoformat() if coord.presencia_verificada_at else None,
                    'ultimo_acceso': coord.ultimo_acceso.isoformat() if coord.ultimo_acceso else None,
                    'minutos_inactivo': calcular_minutos_inactivo(coord.ultimo_acceso),
                    'estado': determinar_estado_usuario(coord)
                })
        
        # Calcular estadísticas
        total = len(equipo)
        presentes = sum(1 for e in equipo if e['estado'] == 'activo')
        inactivos = sum(1 for e in equipo if e['estado'] == 'inactivo')
        ausentes = sum(1 for e in equipo if e['estado'] == 'ausente')
        
        return jsonify({
            'success': True,
            'data': {
                'equipo': equipo,
                'estadisticas': {
                    'total': total,
                    'presentes': presentes,
                    'inactivos': inactivos,
                    'ausentes': ausentes,
                    'porcentaje_presencia': round((presentes / total * 100) if total > 0 else 0, 2)
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener estado del equipo: {str(e)}'
        }), 500


def calcular_minutos_inactivo(ultimo_acceso):
    """Calcular minutos desde el último acceso"""
    if not ultimo_acceso:
        return None
    
    delta = datetime.now() - ultimo_acceso
    return int(delta.total_seconds() / 60)


def determinar_estado_usuario(usuario):
    """
    Determinar estado del usuario basado en último acceso
    - activo: menos de 15 minutos
    - inactivo: entre 15 y 60 minutos
    - ausente: más de 60 minutos o nunca conectado
    """
    if not usuario.ultimo_acceso:
        return 'ausente'
    
    minutos = calcular_minutos_inactivo(usuario.ultimo_acceso)
    
    if minutos < 15:
        return 'activo'
    elif minutos < 60:
        return 'inactivo'
    else:
        return 'ausente'


@verificacion_bp.route('/ping', methods=['POST'])
@jwt_required()
def ping_presencia():
    """
    Ping rápido para mantener presencia activa
    Se llama automáticamente cada 5 minutos desde el frontend
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Actualizar último acceso
        user.ultimo_acceso = datetime.now()
        
        # Si no ha verificado presencia, marcarla
        if not user.presencia_verificada:
            user.presencia_verificada = True
            user.presencia_verificada_at = datetime.now()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'ultimo_acceso': user.ultimo_acceso.isoformat(),
                'presencia_verificada': user.presencia_verificada
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error en ping: {str(e)}'
        }), 500



@verificacion_bp.route('/usuarios-geolocalizados', methods=['GET'])
@jwt_required()
@role_required(['coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental', 'super_admin', 'auditor_electoral', 'monitoreo'])
def obtener_usuarios_geolocalizados():
    """
    Obtener usuarios con geolocalización activa
    Filtra según el rol del usuario que consulta
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
        query = User.query.filter(
            User.activo == True,
            User.ultima_latitud.isnot(None),
            User.ultima_longitud.isnot(None)
        )
        
        # Filtrar según rol
        if user.rol == 'coordinador_puesto' and user.ubicacion_id:
            # Solo testigos del puesto
            ubicacion = Location.query.get(user.ubicacion_id)
            if ubicacion:
                mesas = Location.query.filter_by(
                    puesto_codigo=ubicacion.puesto_codigo,
                    departamento_codigo=ubicacion.departamento_codigo,
                    municipio_codigo=ubicacion.municipio_codigo,
                    zona_codigo=ubicacion.zona_codigo,
                    tipo='mesa'
                ).all()
                
                mesa_ids = [mesa.id for mesa in mesas]
                query = query.filter(
                    User.ubicacion_id.in_(mesa_ids),
                    User.rol == 'testigo_electoral'
                )
        
        elif user.rol == 'coordinador_municipal' and user.ubicacion_id:
            # Coordinadores de puesto y testigos del municipio
            ubicacion = Location.query.get(user.ubicacion_id)
            if ubicacion:
                puestos = Location.query.filter_by(
                    municipio_codigo=ubicacion.municipio_codigo,
                    departamento_codigo=ubicacion.departamento_codigo,
                    tipo='puesto'
                ).all()
                
                puesto_ids = [puesto.id for puesto in puestos]
                
                # Obtener mesas de los puestos
                mesas = Location.query.filter(
                    Location.puesto_codigo.in_([p.puesto_codigo for p in puestos]),
                    Location.tipo == 'mesa',
                    Location.departamento_codigo == ubicacion.departamento_codigo,
                    Location.municipio_codigo == ubicacion.municipio_codigo
                ).all()
                
                mesa_ids = [mesa.id for mesa in mesas]
                
                query = query.filter(
                    db.or_(
                        db.and_(User.ubicacion_id.in_(puesto_ids), User.rol == 'coordinador_puesto'),
                        db.and_(User.ubicacion_id.in_(mesa_ids), User.rol == 'testigo_electoral')
                    )
                )
        
        elif user.rol == 'coordinador_departamental' and user.ubicacion_id:
            # Coordinadores municipales y de puesto del departamento
            ubicacion = Location.query.get(user.ubicacion_id)
            if ubicacion:
                municipios = Location.query.filter_by(
                    departamento_codigo=ubicacion.departamento_codigo,
                    tipo='municipio'
                ).all()
                
                municipio_ids = [mun.id for mun in municipios]
                
                query = query.filter(
                    User.rol.in_(['coordinador_municipal', 'coordinador_puesto', 'testigo_electoral'])
                )
        
        elif user.rol == 'super_admin':
            # Todos los usuarios
            pass
        
        elif user.rol == 'auditor_electoral':
            # Todos los usuarios que puede auditar
            pass
        
        # Ejecutar query
        usuarios = query.all()
        
        # Formatear respuesta
        usuarios_data = []
        for usuario in usuarios:
            ubicacion = Location.query.get(usuario.ubicacion_id) if usuario.ubicacion_id else None
            
            usuarios_data.append({
                'id': usuario.id,
                'nombre': usuario.nombre,
                'rol': usuario.rol,
                'latitud': float(usuario.ultima_latitud),
                'longitud': float(usuario.ultima_longitud),
                'ultima_geolocalizacion_at': usuario.ultima_geolocalizacion_at.isoformat() if usuario.ultima_geolocalizacion_at else None,
                'ultimo_acceso': usuario.ultimo_acceso.isoformat() if usuario.ultimo_acceso else None,
                'minutos_inactivo': calcular_minutos_inactivo(usuario.ultimo_acceso),
                'estado': determinar_estado_usuario(usuario),
                'ubicacion_nombre': ubicacion.nombre_completo if ubicacion else None,
                'ubicacion_tipo': ubicacion.tipo if ubicacion else None
            })
        
        return jsonify({
            'success': True,
            'data': usuarios_data
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Error obteniendo usuarios geolocalizados: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Error al obtener usuarios geolocalizados: {str(e)}'
        }), 500
