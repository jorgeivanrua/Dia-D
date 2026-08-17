"""
Rutas para el rol de Monitoreo
Dashboard de monitoreo en tiempo real con geolocalización
OPTIMIZADO para múltiples usuarios simultáneos
"""
from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.location import Location
from backend.models.formulario_e14 import FormularioE14
from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
from backend.database import db
from backend.utils.decorators import role_required
from backend.utils.cache import cache_monitoreo, cache_estadisticas, cache_ubicaciones, invalidate_cache
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_

monitoreo_bp = Blueprint('monitoreo', __name__, url_prefix='/api/monitoreo')


# Dashboard se sirve desde frontend_bp para evitar conflictos con JWT
# Ver backend/routes/frontend.py


@monitoreo_bp.route('/usuarios-activos', methods=['GET'])
@jwt_required()
@role_required('monitoreo')
@cache_monitoreo(timeout=20)  # Caché de 20 segundos
def get_usuarios_activos():
    """
    Obtener todos los usuarios activos con su última geolocalización
    OPTIMIZADO: Con caché y consulta eficiente
    """
    try:
        # Paginación opcional
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 1000, type=int)  # Límite alto por defecto
        
        # Consulta optimizada con índices
        query = User.query.filter(
            User.activo == True,
            User.ultima_latitud.isnot(None),
            User.ultima_longitud.isnot(None)
        ).order_by(User.ultima_geolocalizacion_at.desc())
        
        # Aplicar paginación si se solicita
        if per_page < 1000:
            usuarios = query.paginate(page=page, per_page=per_page, error_out=False).items
        else:
            usuarios = query.all()
        
        usuarios_data = []
        for usuario in usuarios:
            ubicacion = None
            if usuario.ubicacion_id:
                location = Location.query.get(usuario.ubicacion_id)
                if location:
                    ubicacion = location.to_dict()
            
            usuarios_data.append({
                'id': usuario.id,
                'nombre': usuario.nombre,
                'rol': usuario.rol,
                'latitud': usuario.ultima_latitud,
                'longitud': usuario.ultima_longitud,
                'precision': usuario.precision_geolocalizacion,
                'ultima_actualizacion': usuario.ultima_geolocalizacion_at.isoformat() if usuario.ultima_geolocalizacion_at else None,
                'ubicacion': ubicacion,
                'presencia_verificada': usuario.presencia_verificada if usuario.rol == 'testigo_electoral' else None
            })
        
        return jsonify({
            'success': True,
            'data': usuarios_data,
            'total': len(usuarios_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@monitoreo_bp.route('/estadisticas', methods=['GET'])
@jwt_required()
@role_required('monitoreo')
@cache_estadisticas(timeout=30)  # Caché de 30 segundos
def get_estadisticas():
    """
    Obtener estadísticas generales del sistema
    OPTIMIZADO: Con caché y consultas agregadas eficientes
    """
    try:
        from backend.models.formulario_e14 import FormularioE14
        
        # Consulta optimizada con agregación en una sola query
        testigos_stats = db.session.query(
            func.count(User.id).label('total'),
            func.sum(func.cast(User.ultima_latitud.isnot(None), db.Integer)).label('con_geo'),
            func.sum(func.cast(User.presencia_verificada, db.Integer)).label('con_presencia')
        ).filter(
            User.rol == 'testigo_electoral',
            User.activo == True
        ).first()
        
        coordinadores_stats = db.session.query(
            func.count(User.id).label('total'),
            func.sum(func.cast(User.ultima_latitud.isnot(None), db.Integer)).label('con_geo')
        ).filter(
            User.rol.in_(['coordinador_departamental', 'coordinador_municipal', 'coordinador_puesto']),
            User.activo == True
        ).first()
        
        # Contar formularios (sin agregación compleja que causa problemas en SQLite)
        # Contar formularios
        formularios_total = FormularioE14.query.count()
        formularios_validados = FormularioE14.query.filter_by(estado='validado').count()
        formularios_pendientes = FormularioE14.query.filter_by(estado='pendiente').count()
        formularios_rechazados = FormularioE14.query.filter_by(estado='rechazado').count()
        
        # Calcular formularios esperados: mesas × tipos de elección activos
        from backend.models.configuracion_electoral import TipoEleccion
        total_mesas = Location.query.filter_by(tipo='mesa').count()
        tipos_eleccion_activos = TipoEleccion.query.filter_by(activo=True).count()
        formularios_esperados = total_mesas * tipos_eleccion_activos
        
        testigos_total = testigos_stats.total or 0
        testigos_con_geo = testigos_stats.con_geo or 0
        testigos_presencia = testigos_stats.con_presencia or 0
        
        coordinadores_total = coordinadores_stats.total or 0
        coordinadores_con_geo = coordinadores_stats.con_geo or 0
        
        # Formularios de la última hora
        una_hora_atras = datetime.utcnow() - timedelta(hours=1)
        formularios_ultima_hora = FormularioE14.query.filter(
            FormularioE14.created_at >= una_hora_atras
        ).count()
        
        # Contar incidentes y delitos
        incidentes_total = IncidenteElectoral.query.count()
        incidentes_criticos = IncidenteElectoral.query.filter_by(severidad='critica').count()
        incidentes_pendientes = IncidenteElectoral.query.filter_by(estado='reportado').count()
        
        delitos_total = DelitoElectoral.query.count()
        delitos_graves = DelitoElectoral.query.filter(
            DelitoElectoral.gravedad.in_(['grave', 'muy_grave'])
        ).count()
        delitos_pendientes = DelitoElectoral.query.filter_by(estado='reportado').count()
        
        # Usuarios activos en la última hora (con geolocalización actualizada)
        usuarios_activos_hora = User.query.filter(
            User.activo == True,
            User.ultima_geolocalizacion_at >= una_hora_atras
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'testigos': {
                    'total': testigos_total,
                    'con_geolocalizacion': testigos_con_geo,
                    'con_presencia_verificada': testigos_presencia,
                    'porcentaje_geo': round((testigos_con_geo / testigos_total * 100), 2) if testigos_total > 0 else 0,
                    'porcentaje_presencia': round((testigos_presencia / testigos_total * 100), 2) if testigos_total > 0 else 0
                },
                'coordinadores': {
                    'total': coordinadores_total,
                    'con_geolocalizacion': coordinadores_con_geo,
                    'porcentaje_geo': round((coordinadores_con_geo / coordinadores_total * 100), 2) if coordinadores_total > 0 else 0
                },
                'formularios': {
                    'total': formularios_total,
                    'esperados': formularios_esperados,
                    'validados': formularios_validados,
                    'pendientes': formularios_pendientes,
                    'rechazados': formularios_rechazados,
                    'ultima_hora': formularios_ultima_hora,
                    'porcentaje_validados': round((formularios_validados / formularios_total * 100), 2) if formularios_total > 0 else 0,
                    'porcentaje_recibidos': round((formularios_total / formularios_esperados * 100), 2) if formularios_esperados > 0 else 0,
                    'total_mesas': total_mesas,
                    'tipos_eleccion': tipos_eleccion_activos
                },
                'incidentes': {
                    'total': incidentes_total,
                    'criticos': incidentes_criticos,
                    'pendientes': incidentes_pendientes
                },
                'delitos': {
                    'total': delitos_total,
                    'graves': delitos_graves,
                    'pendientes': delitos_pendientes
                },
                'actividad': {
                    'usuarios_activos_hora': usuarios_activos_hora
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



@monitoreo_bp.route('/alertas', methods=['GET'])
@jwt_required()
@role_required('monitoreo')
def get_alertas():
    """
    Obtener alertas y situaciones que requieren atención
    """
    try:
        from datetime import datetime, timedelta
        from backend.models.formulario_e14 import FormularioE14
        
        
        
        alertas = []
        
        # Testigos sin geolocalización
        testigos_sin_geo = User.query.filter(
            User.rol == 'testigo_electoral',
            User.activo == True,
            User.ultima_latitud.is_(None)
        ).count()
        
        if testigos_sin_geo > 0:
            alertas.append({
                'tipo': 'warning',
                'categoria': 'geolocalizacion',
                'titulo': f'{testigos_sin_geo} testigos sin geolocalización',
                'descripcion': 'Hay testigos activos que no han compartido su ubicación',
                'prioridad': 'media',
                'cantidad': testigos_sin_geo
            })
        
        # Testigos sin presencia verificada
        testigos_sin_presencia = User.query.filter(
            User.rol == 'testigo_electoral',
            User.activo == True,
            User.presencia_verificada == False
        ).count()
        
        if testigos_sin_presencia > 0:
            alertas.append({
                'tipo': 'warning',
                'categoria': 'presencia',
                'titulo': f'{testigos_sin_presencia} testigos sin presencia verificada',
                'descripcion': 'Testigos que no han verificado su presencia en el puesto',
                'prioridad': 'alta',
                'cantidad': testigos_sin_presencia
            })
        
        # Incidentes críticos pendientes
        incidentes_criticos = IncidenteElectoral.query.filter(
            IncidenteElectoral.severidad == 'critica',
            IncidenteElectoral.estado.in_(['reportado', 'en_revision'])
        ).count()
        
        if incidentes_criticos > 0:
            alertas.append({
                'tipo': 'danger',
                'categoria': 'incidentes',
                'titulo': f'{incidentes_criticos} incidentes críticos pendientes',
                'descripcion': 'Incidentes de alta severidad que requieren atención inmediata',
                'prioridad': 'critica',
                'cantidad': incidentes_criticos
            })
        
        # Delitos graves pendientes
        delitos_graves = DelitoElectoral.query.filter(
            DelitoElectoral.gravedad.in_(['grave', 'muy_grave']),
            DelitoElectoral.estado.in_(['reportado', 'en_investigacion'])
        ).count()
        
        if delitos_graves > 0:
            alertas.append({
                'tipo': 'danger',
                'categoria': 'delitos',
                'titulo': f'{delitos_graves} delitos graves en investigación',
                'descripcion': 'Delitos electorales graves que requieren seguimiento',
                'prioridad': 'critica',
                'cantidad': delitos_graves
            })
        
        # Formularios pendientes de validación
        formularios_pendientes = FormularioE14.query.filter_by(estado='pendiente').count()
        
        if formularios_pendientes > 50:
            alertas.append({
                'tipo': 'info',
                'categoria': 'formularios',
                'titulo': f'{formularios_pendientes} formularios pendientes de validación',
                'descripcion': 'Hay un alto volumen de formularios esperando validación',
                'prioridad': 'media',
                'cantidad': formularios_pendientes
            })
        
        # Usuarios inactivos en la última hora (que deberían estar activos)
        una_hora_atras = datetime.utcnow() - timedelta(hours=1)
        usuarios_inactivos = User.query.filter(
            User.activo == True,
            User.rol.in_(['testigo_electoral', 'coordinador_puesto']),
            User.ultima_geolocalizacion_at < una_hora_atras
        ).count()
        
        if usuarios_inactivos > 10:
            alertas.append({
                'tipo': 'warning',
                'categoria': 'actividad',
                'titulo': f'{usuarios_inactivos} usuarios sin actividad reciente',
                'descripcion': 'Usuarios que no han actualizado su ubicación en la última hora',
                'prioridad': 'baja',
                'cantidad': usuarios_inactivos
            })
        
        # Ordenar por prioridad
        prioridad_orden = {'critica': 0, 'alta': 1, 'media': 2, 'baja': 3}
        alertas.sort(key=lambda x: prioridad_orden.get(x['prioridad'], 4))
        
        return jsonify({
            'success': True,
            'data': alertas,
            'total': len(alertas)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@monitoreo_bp.route('/actividad-reciente', methods=['GET'])
@jwt_required()
@role_required('monitoreo')
def get_actividad_reciente():
    """
    Obtener actividad reciente del sistema
    """
    try:
        from datetime import datetime, timedelta
        from backend.models.formulario_e14 import FormularioE14
        
        
        
        limite = int(request.args.get('limite', 20))
        horas = int(request.args.get('horas', 24))
        
        tiempo_limite = datetime.utcnow() - timedelta(hours=horas)
        
        actividades = []
        
        # Formularios recientes
        formularios = FormularioE14.query.filter(
            FormularioE14.created_at >= tiempo_limite
        ).order_by(FormularioE14.created_at.desc()).limit(limite).all()
        
        for form in formularios:
            usuario = User.query.get(form.usuario_id)
            actividades.append({
                'tipo': 'formulario',
                'icono': 'file-earmark-text',
                'titulo': 'Formulario E-14 enviado',
                'descripcion': f'{usuario.nombre if usuario else "Usuario"} envió un formulario',
                'estado': form.estado,
                'timestamp': form.created_at.isoformat(),
                'usuario': usuario.nombre if usuario else None
            })
        
        # Incidentes recientes
        incidentes = IncidenteElectoral.query.filter(
            IncidenteElectoral.fecha_reporte >= tiempo_limite
        ).order_by(IncidenteElectoral.fecha_reporte.desc()).limit(limite).all()
        
        for inc in incidentes:
            usuario = User.query.get(inc.reportado_por_id)
            actividades.append({
                'tipo': 'incidente',
                'icono': 'exclamation-triangle',
                'titulo': f'Incidente reportado: {inc.titulo}',
                'descripcion': inc.descripcion[:100] + '...' if len(inc.descripcion) > 100 else inc.descripcion,
                'severidad': inc.severidad,
                'timestamp': inc.fecha_reporte.isoformat(),
                'usuario': usuario.nombre if usuario else None
            })
        
        # Delitos recientes
        delitos = DelitoElectoral.query.filter(
            DelitoElectoral.fecha_reporte >= tiempo_limite
        ).order_by(DelitoElectoral.fecha_reporte.desc()).limit(limite).all()
        
        for delito in delitos:
            usuario = User.query.get(delito.reportado_por_id)
            actividades.append({
                'tipo': 'delito',
                'icono': 'shield-exclamation',
                'titulo': f'Delito electoral reportado: {delito.titulo}',
                'descripcion': delito.descripcion[:100] + '...' if len(delito.descripcion) > 100 else delito.descripcion,
                'gravedad': delito.gravedad,
                'timestamp': delito.fecha_reporte.isoformat(),
                'usuario': usuario.nombre if usuario else None
            })
        
        # Ordenar por timestamp
        actividades.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Limitar resultados
        actividades = actividades[:limite]
        
        return jsonify({
            'success': True,
            'data': actividades,
            'total': len(actividades)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@monitoreo_bp.route('/estadisticas-departamento/<departamento_codigo>', methods=['GET'])
@jwt_required()
@role_required('monitoreo')
def get_estadisticas_departamento(departamento_codigo):
    """
    Obtener estadísticas específicas de un departamento
    """
    try:
        from backend.models.formulario_e14 import FormularioE14
        
        # Usuarios del departamento
        usuarios_depto = User.query.join(Location).filter(
            Location.departamento_codigo == departamento_codigo,
            User.activo == True
        ).all()
        
        testigos = [u for u in usuarios_depto if u.rol == 'testigo_electoral']
        coordinadores = [u for u in usuarios_depto if 'coordinador' in u.rol]
        
        testigos_con_geo = len([t for t in testigos if t.ultima_latitud is not None])
        testigos_con_presencia = len([t for t in testigos if t.presencia_verificada])
        
        # Formularios del departamento
        formularios_depto = FormularioE14.query.join(User).join(Location).filter(
            Location.departamento_codigo == departamento_codigo
        ).all()
        
        formularios_validados = len([f for f in formularios_depto if f.estado == 'validado'])
        formularios_pendientes = len([f for f in formularios_depto if f.estado == 'pendiente'])
        
        return jsonify({
            'success': True,
            'data': {
                'departamento_codigo': departamento_codigo,
                'testigos': {
                    'total': len(testigos),
                    'con_geolocalizacion': testigos_con_geo,
                    'con_presencia': testigos_con_presencia
                },
                'coordinadores': {
                    'total': len(coordinadores)
                },
                'formularios': {
                    'total': len(formularios_depto),
                    'validados': formularios_validados,
                    'pendientes': formularios_pendientes
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@monitoreo_bp.route('/exportar-reporte', methods=['GET'])
@jwt_required()
@role_required('monitoreo')
def exportar_reporte():
    """
    Exportar reporte completo del estado actual del sistema
    """
    try:
        from datetime import datetime
        from backend.models.formulario_e14 import FormularioE14
        
        
        
        # Recopilar todas las estadísticas
        reporte = {
            'fecha_generacion': datetime.utcnow().isoformat(),
            'generado_por': get_jwt_identity(),
            'usuarios': {
                'testigos': {
                    'total': User.query.filter_by(rol='testigo_electoral', activo=True).count(),
                    'con_geolocalizacion': User.query.filter(
                        User.rol == 'testigo_electoral',
                        User.activo == True,
                        User.ultima_latitud.isnot(None)
                    ).count(),
                    'con_presencia_verificada': User.query.filter(
                        User.rol == 'testigo_electoral',
                        User.activo == True,
                        User.presencia_verificada == True
                    ).count()
                },
                'coordinadores': {
                    'departamentales': User.query.filter_by(rol='coordinador_departamental', activo=True).count(),
                    'municipales': User.query.filter_by(rol='coordinador_municipal', activo=True).count(),
                    'puestos': User.query.filter_by(rol='coordinador_puesto', activo=True).count()
                },
                'auditores': User.query.filter_by(rol='auditor_electoral', activo=True).count()
            },
            'formularios': {
                'total': FormularioE14.query.count(),
                'validados': FormularioE14.query.filter_by(estado='validado').count(),
                'pendientes': FormularioE14.query.filter_by(estado='pendiente').count(),
                'rechazados': FormularioE14.query.filter_by(estado='rechazado').count()
            },
            'incidentes': {
                'total': IncidenteElectoral.query.count(),
                'criticos': IncidenteElectoral.query.filter_by(severidad='critica').count(),
                'altos': IncidenteElectoral.query.filter_by(severidad='alta').count(),
                'medios': IncidenteElectoral.query.filter_by(severidad='media').count(),
                'bajos': IncidenteElectoral.query.filter_by(severidad='baja').count()
            },
            'delitos': {
                'total': DelitoElectoral.query.count(),
                'muy_graves': DelitoElectoral.query.filter_by(gravedad='muy_grave').count(),
                'graves': DelitoElectoral.query.filter_by(gravedad='grave').count(),
                'leves': DelitoElectoral.query.filter_by(gravedad='leve').count()
            }
        }
        
        return jsonify({
            'success': True,
            'data': reporte
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# NUEVOS ENDPOINTS - FUNCIONALIDADES AVANZADAS
# ============================================================================

@monitoreo_bp.route('/metricas-rendimiento', methods=['GET'])
@jwt_required()
@role_required('monitoreo')
def get_metricas_rendimiento():
    """
    Métricas de rendimiento del sistema electoral
    """
    try:
        from datetime import datetime, timedelta
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
        
        ahora = datetime.utcnow()
        
        # Métricas de las últimas 24 horas
        hace_24h = ahora - timedelta(hours=24)
        hace_12h = ahora - timedelta(hours=12)
        hace_6h = ahora - timedelta(hours=6)
        hace_1h = ahora - timedelta(hours=1)
        
        # Actividad de usuarios
        usuarios_24h = User.query.filter(
            User.activo == True,
            User.ultima_geolocalizacion_at >= hace_24h
        ).count()
        
        usuarios_12h = User.query.filter(
            User.activo == True,
            User.ultima_geolocalizacion_at >= hace_12h
        ).count()
        
        usuarios_6h = User.query.filter(
            User.activo == True,
            User.ultima_geolocalizacion_at >= hace_6h
        ).count()
        
        usuarios_1h = User.query.filter(
            User.activo == True,
            User.ultima_geolocalizacion_at >= hace_1h
        ).count()
        
        # Formularios por período
        formularios_24h = FormularioE14.query.filter(
            FormularioE14.created_at >= hace_24h
        ).count()
        
        formularios_12h = FormularioE14.query.filter(
            FormularioE14.created_at >= hace_12h
        ).count()
        
        formularios_6h = FormularioE14.query.filter(
            FormularioE14.created_at >= hace_6h
        ).count()
        
        formularios_1h = FormularioE14.query.filter(
            FormularioE14.created_at >= hace_1h
        ).count()
        
        # Incidentes por período
        incidentes_24h = IncidenteElectoral.query.filter(
            IncidenteElectoral.fecha_reporte >= hace_24h
        ).count()
        
        incidentes_12h = IncidenteElectoral.query.filter(
            IncidenteElectoral.fecha_reporte >= hace_12h
        ).count()
        
        incidentes_6h = IncidenteElectoral.query.filter(
            IncidenteElectoral.fecha_reporte >= hace_6h
        ).count()
        
        incidentes_1h = IncidenteElectoral.query.filter(
            IncidenteElectoral.fecha_reporte >= hace_1h
        ).count()
        
        # Calcular tasas de cambio
        tasa_usuarios = ((usuarios_1h - usuarios_6h) / usuarios_6h * 100) if usuarios_6h > 0 else 0
        tasa_formularios = ((formularios_1h - formularios_6h) / formularios_6h * 100) if formularios_6h > 0 else 0
        tasa_incidentes = ((incidentes_1h - incidentes_6h) / incidentes_6h * 100) if incidentes_6h > 0 else 0
        
        # Tiempo promedio de respuesta a incidentes
        incidentes_resueltos = IncidenteElectoral.query.filter(
            IncidenteElectoral.estado == 'resuelto',
            IncidenteElectoral.fecha_reporte >= hace_24h
        ).all()
        
        tiempos_respuesta = []
        for inc in incidentes_resueltos:
            if inc.updated_at and inc.fecha_reporte:
                tiempo = (inc.updated_at - inc.fecha_reporte).total_seconds() / 60  # en minutos
                tiempos_respuesta.append(tiempo)
        
        tiempo_promedio_respuesta = sum(tiempos_respuesta) / len(tiempos_respuesta) if tiempos_respuesta else 0
        
        return jsonify({
            'success': True,
            'metricas': {
                'actividad_usuarios': {
                    'ultima_hora': usuarios_1h,
                    'ultimas_6_horas': usuarios_6h,
                    'ultimas_12_horas': usuarios_12h,
                    'ultimas_24_horas': usuarios_24h,
                    'tasa_cambio': round(tasa_usuarios, 2)
                },
                'formularios': {
                    'ultima_hora': formularios_1h,
                    'ultimas_6_horas': formularios_6h,
                    'ultimas_12_horas': formularios_12h,
                    'ultimas_24_horas': formularios_24h,
                    'tasa_cambio': round(tasa_formularios, 2),
                    'promedio_por_hora': round(formularios_24h / 24, 2)
                },
                'incidentes': {
                    'ultima_hora': incidentes_1h,
                    'ultimas_6_horas': incidentes_6h,
                    'ultimas_12_horas': incidentes_12h,
                    'ultimas_24_horas': incidentes_24h,
                    'tasa_cambio': round(tasa_incidentes, 2),
                    'tiempo_promedio_respuesta_minutos': round(tiempo_promedio_respuesta, 2)
                },
                'timestamp': ahora.isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@monitoreo_bp.route('/mapa-calor', methods=['GET'])
@jwt_required()
@role_required('monitoreo')
def get_mapa_calor():
    """
    Datos para mapa de calor de actividad por ubicación
    """
    try:
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
        from datetime import datetime, timedelta
        
        # Obtener actividad por departamento
        departamentos = db.session.query(
            Location.departamento_codigo,
            Location.departamento_nombre
        ).filter(
            Location.tipo == 'departamento'
        ).distinct().all()
        
        mapa_data = []
        
        for dept_codigo, dept_nombre in departamentos:
            # Usuarios en el departamento
            usuarios_dept = User.query.join(Location, User.ubicacion_id == Location.id).filter(
                Location.departamento_codigo == dept_codigo,
                User.activo == True
            ).count()
            
            # Formularios del departamento
            formularios_dept = FormularioE14.query.join(User, FormularioE14.testigo_id == User.id).join(
                Location, User.ubicacion_id == Location.id
            ).filter(
                Location.departamento_codigo == dept_codigo
            ).count()
            
            # Incidentes del departamento
            incidentes_dept = IncidenteElectoral.query.join(
                User, IncidenteElectoral.reportado_por_id == User.id
            ).join(Location, User.ubicacion_id == Location.id).filter(
                Location.departamento_codigo == dept_codigo
            ).count()
            
            # Delitos del departamento
            delitos_dept = DelitoElectoral.query.join(
                User, DelitoElectoral.reportado_por_id == User.id
            ).join(Location, User.ubicacion_id == Location.id).filter(
                Location.departamento_codigo == dept_codigo
            ).count()
            
            # Calcular índice de actividad (0-100)
            actividad_total = usuarios_dept + formularios_dept + (incidentes_dept * 2) + (delitos_dept * 3)
            
            mapa_data.append({
                'departamento_codigo': dept_codigo,
                'departamento_nombre': dept_nombre,
                'usuarios': usuarios_dept,
                'formularios': formularios_dept,
                'incidentes': incidentes_dept,
                'delitos': delitos_dept,
                'indice_actividad': actividad_total
            })
        
        # Ordenar por índice de actividad
        mapa_data.sort(key=lambda x: x['indice_actividad'], reverse=True)
        
        return jsonify({
            'success': True,
            'mapa_calor': mapa_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@monitoreo_bp.route('/tendencias', methods=['GET'])
@jwt_required()
@role_required('monitoreo')
def get_tendencias():
    """
    Análisis de tendencias por hora del día
    """
    try:
        from datetime import datetime, timedelta
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.incidentes_delitos import IncidenteElectoral
        
        ahora = datetime.utcnow()
        hace_24h = ahora - timedelta(hours=24)
        
        # Inicializar contadores por hora
        tendencias_por_hora = {i: {'formularios': 0, 'incidentes': 0, 'usuarios_activos': 0} for i in range(24)}
        
        # Formularios por hora
        formularios = FormularioE14.query.filter(
            FormularioE14.created_at >= hace_24h
        ).all()
        
        for form in formularios:
            hora = form.created_at.hour
            tendencias_por_hora[hora]['formularios'] += 1
        
        # Incidentes por hora
        incidentes = IncidenteElectoral.query.filter(
            IncidenteElectoral.fecha_reporte >= hace_24h
        ).all()
        
        for inc in incidentes:
            hora = inc.fecha_reporte.hour
            tendencias_por_hora[hora]['incidentes'] += 1
        
        # Usuarios activos por hora
        usuarios = User.query.filter(
            User.activo == True,
            User.ultima_geolocalizacion_at >= hace_24h
        ).all()
        
        for user in usuarios:
            if user.ultima_geolocalizacion_at:
                hora = user.ultima_geolocalizacion_at.hour
                tendencias_por_hora[hora]['usuarios_activos'] += 1
        
        # Convertir a lista ordenada
        tendencias_lista = [
            {
                'hora': hora,
                'formularios': datos['formularios'],
                'incidentes': datos['incidentes'],
                'usuarios_activos': datos['usuarios_activos']
            }
            for hora, datos in sorted(tendencias_por_hora.items())
        ]
        
        # Identificar hora pico
        hora_pico = max(tendencias_por_hora.items(), key=lambda x: x[1]['formularios'] + x[1]['incidentes'])
        
        return jsonify({
            'success': True,
            'tendencias': tendencias_lista,
            'hora_pico': {
                'hora': hora_pico[0],
                'actividad_total': hora_pico[1]['formularios'] + hora_pico[1]['incidentes']
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@monitoreo_bp.route('/comparativa-departamentos', methods=['GET'])
@jwt_required()
@role_required('monitoreo')
def get_comparativa_departamentos():
    """
    Comparativa de rendimiento entre departamentos
    """
    try:
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
        
        # Obtener todos los departamentos
        departamentos = db.session.query(
            Location.departamento_codigo,
            Location.departamento_nombre
        ).filter(
            Location.tipo == 'departamento'
        ).distinct().all()
        
        comparativa = []
        
        for dept_codigo, dept_nombre in departamentos:
            # Testigos del departamento
            testigos_total = User.query.join(Location, User.ubicacion_id == Location.id).filter(
                Location.departamento_codigo == dept_codigo,
                User.rol == 'testigo_electoral',
                User.activo == True
            ).count()
            
            testigos_con_presencia = User.query.join(Location, User.ubicacion_id == Location.id).filter(
                Location.departamento_codigo == dept_codigo,
                User.rol == 'testigo_electoral',
                User.activo == True,
                User.presencia_verificada == True
            ).count()
            
            # Formularios del departamento
            formularios_total = FormularioE14.query.join(User, FormularioE14.testigo_id == User.id).join(
                Location, User.ubicacion_id == Location.id
            ).filter(
                Location.departamento_codigo == dept_codigo
            ).count()
            
            formularios_validados = FormularioE14.query.join(User, FormularioE14.testigo_id == User.id).join(
                Location, User.ubicacion_id == Location.id
            ).filter(
                Location.departamento_codigo == dept_codigo,
                FormularioE14.estado == 'validado'
            ).count()
            
            # Incidentes del departamento
            incidentes_total = IncidenteElectoral.query.join(
                User, IncidenteElectoral.reportado_por_id == User.id
            ).join(Location, User.ubicacion_id == Location.id).filter(
                Location.departamento_codigo == dept_codigo
            ).count()
            
            incidentes_criticos = IncidenteElectoral.query.join(
                User, IncidenteElectoral.reportado_por_id == User.id
            ).join(Location, User.ubicacion_id == Location.id).filter(
                Location.departamento_codigo == dept_codigo,
                IncidenteElectoral.severidad == 'critica'
            ).count()
            
            # Calcular porcentajes
            porcentaje_presencia = round((testigos_con_presencia / testigos_total * 100), 2) if testigos_total > 0 else 0
            porcentaje_validados = round((formularios_validados / formularios_total * 100), 2) if formularios_total > 0 else 0
            
            # Calcular score de rendimiento (0-100)
            score = (
                (porcentaje_presencia * 0.4) +  # 40% peso a presencia
                (porcentaje_validados * 0.4) +  # 40% peso a formularios validados
                (max(0, 100 - (incidentes_criticos * 10)) * 0.2)  # 20% peso a incidentes (penalización)
            )
            
            comparativa.append({
                'departamento_codigo': dept_codigo,
                'departamento_nombre': dept_nombre,
                'testigos': {
                    'total': testigos_total,
                    'con_presencia': testigos_con_presencia,
                    'porcentaje_presencia': porcentaje_presencia
                },
                'formularios': {
                    'total': formularios_total,
                    'validados': formularios_validados,
                    'porcentaje_validados': porcentaje_validados
                },
                'incidentes': {
                    'total': incidentes_total,
                    'criticos': incidentes_criticos
                },
                'score_rendimiento': round(score, 2)
            })
        
        # Ordenar por score de rendimiento
        comparativa.sort(key=lambda x: x['score_rendimiento'], reverse=True)
        
        # Identificar top 5 y bottom 5
        top_5 = comparativa[:5]
        bottom_5 = comparativa[-5:] if len(comparativa) > 5 else []
        
        return jsonify({
            'success': True,
            'comparativa': comparativa,
            'top_5': top_5,
            'bottom_5': bottom_5
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@monitoreo_bp.route('/predicciones', methods=['GET'])
@jwt_required()
@role_required('monitoreo')
def get_predicciones():
    """
    Predicciones simples basadas en tendencias actuales
    """
    try:
        from datetime import datetime, timedelta
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.incidentes_delitos import IncidenteElectoral
        
        ahora = datetime.utcnow()
        hace_24h = ahora - timedelta(hours=24)
        hace_48h = ahora - timedelta(hours=48)
        
        # Formularios últimas 24h vs 24-48h
        formularios_24h = FormularioE14.query.filter(
            FormularioE14.created_at >= hace_24h
        ).count()
        
        formularios_48h = FormularioE14.query.filter(
            FormularioE14.created_at >= hace_48h,
            FormularioE14.created_at < hace_24h
        ).count()
        
        # Calcular tendencia
        if formularios_48h > 0:
            tendencia_formularios = ((formularios_24h - formularios_48h) / formularios_48h) * 100
            prediccion_proximas_24h = int(formularios_24h * (1 + (tendencia_formularios / 100)))
        else:
            tendencia_formularios = 0
            prediccion_proximas_24h = formularios_24h
        
        # Incidentes últimas 24h vs 24-48h
        incidentes_24h = IncidenteElectoral.query.filter(
            IncidenteElectoral.fecha_reporte >= hace_24h
        ).count()
        
        incidentes_48h = IncidenteElectoral.query.filter(
            IncidenteElectoral.fecha_reporte >= hace_48h,
            IncidenteElectoral.fecha_reporte < hace_24h
        ).count()
        
        # Calcular tendencia
        if incidentes_48h > 0:
            tendencia_incidentes = ((incidentes_24h - incidentes_48h) / incidentes_48h) * 100
            prediccion_incidentes_24h = int(incidentes_24h * (1 + (tendencia_incidentes / 100)))
        else:
            tendencia_incidentes = 0
            prediccion_incidentes_24h = incidentes_24h
        
        # Calcular tiempo estimado para completar formularios pendientes
        formularios_pendientes = FormularioE14.query.filter_by(estado='pendiente').count()
        tasa_validacion_hora = formularios_24h / 24 if formularios_24h > 0 else 1
        horas_para_completar = formularios_pendientes / tasa_validacion_hora if tasa_validacion_hora > 0 else 0
        
        return jsonify({
            'success': True,
            'predicciones': {
                'formularios': {
                    'ultimas_24h': formularios_24h,
                    'tendencia_porcentaje': round(tendencia_formularios, 2),
                    'prediccion_proximas_24h': prediccion_proximas_24h,
                    'pendientes': formularios_pendientes,
                    'horas_estimadas_completar': round(horas_para_completar, 2)
                },
                'incidentes': {
                    'ultimas_24h': incidentes_24h,
                    'tendencia_porcentaje': round(tendencia_incidentes, 2),
                    'prediccion_proximas_24h': prediccion_incidentes_24h
                },
                'recomendaciones': []
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

