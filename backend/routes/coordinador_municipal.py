"""
Rutas para el coordinador municipal
"""
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.location import Location
from backend.services.municipal_service import MunicipalService
from backend.services.discrepancia_service import DiscrepanciaService
from backend.services.e24_service import E24Service
from backend.services.consolidado_service import ConsolidadoService
from backend.models.coordinador_municipal import NotificacionCoordinador, AuditLog
from backend.database import db
from backend.utils.exceptions import BaseAPIException, ValidationException, NotFoundException
from backend.utils.decorators import role_required
import csv
import io
from datetime import datetime

coordinador_municipal_bp = Blueprint('coordinador_municipal', __name__, url_prefix='/api/coordinador-municipal')


@coordinador_municipal_bp.route('/puestos', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_puestos():
    """
    Obtener lista de puestos del municipio con estadísticas
    
    Query params:
        estado: Filtrar por estado (completo, incompleto, con_discrepancias)
        zona: Filtrar por zona
    """
    try:
        from backend.models.formulario_e14 import FormularioE14
        
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            return jsonify({
                'success': False,
                'error': 'Usuario no asignado a un municipio válido'
            }), 400
        
        # Obtener todos los puestos del municipio
        puestos = Location.query.filter_by(
            municipio_codigo=ubicacion.municipio_codigo,
            departamento_codigo=ubicacion.departamento_codigo,
            tipo='puesto',
            activo=True
        ).all()
        
        puestos_data = []
        total_puestos = len(puestos)
        puestos_completos = 0
        puestos_incompletos = 0
        puestos_con_discrepancias = 0
        
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
            
            # Obtener IDs de mesas
            mesa_ids = [m.id for m in Location.query.filter_by(
                puesto_codigo=puesto.puesto_codigo,
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                zona_codigo=puesto.zona_codigo,
                tipo='mesa'
            ).all()]
            
            # Contar formularios
            formularios_validados = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids),
                FormularioE14.estado == 'validado'
            ).count() if mesa_ids else 0
            
            formularios_pendientes = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids),
                FormularioE14.estado == 'pendiente'
            ).count() if mesa_ids else 0
            
            formularios_rechazados = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids),
                FormularioE14.estado == 'rechazado'
            ).count() if mesa_ids else 0
            
            # Calcular porcentaje de avance
            porcentaje_avance = (formularios_validados / mesas * 100) if mesas > 0 else 0
            
            # Determinar estado
            if formularios_validados == mesas and mesas > 0:
                estado = 'completo'
                puestos_completos += 1
            elif formularios_rechazados > 0:
                estado = 'con_discrepancias'
                puestos_con_discrepancias += 1
            else:
                estado = 'incompleto'
                puestos_incompletos += 1
            
            # Buscar coordinador del puesto
            coordinador = User.query.filter_by(
                ubicacion_id=puesto.id,
                rol='coordinador_puesto',
                activo=True
            ).first()
            
            puestos_data.append({
                'id': puesto.id,
                'codigo': puesto.puesto_codigo,
                'nombre': puesto.puesto_nombre,
                'zona_codigo': puesto.zona_codigo,
                'total_mesas': mesas,
                'mesas_reportadas': formularios_validados + formularios_pendientes + formularios_rechazados,
                'formularios_validados': formularios_validados,
                'formularios_pendientes': formularios_pendientes,
                'formularios_rechazados': formularios_rechazados,
                'porcentaje_avance': round(porcentaje_avance, 2),
                'estado': estado,
                'tiene_discrepancias': formularios_rechazados > 0,
                'coordinador': {
                    'id': coordinador.id,
                    'nombre': coordinador.nombre,
                    'ultimo_acceso': coordinador.ultimo_acceso.isoformat() if coordinador and coordinador.ultimo_acceso else None
                } if coordinador else None
            })
        
        # Aplicar filtros
        filtro_estado = request.args.get('estado')
        if filtro_estado:
            puestos_data = [p for p in puestos_data if p['estado'] == filtro_estado]
        
        filtro_zona = request.args.get('zona')
        if filtro_zona:
            puestos_data = [p for p in puestos_data if p['zona_codigo'] == filtro_zona]
        
        # Estadísticas
        estadisticas = {
            'total_puestos': total_puestos,
            'puestos_completos': puestos_completos,
            'puestos_incompletos': puestos_incompletos,
            'puestos_con_discrepancias': puestos_con_discrepancias,
            'cobertura_porcentaje': (puestos_completos / total_puestos * 100) if total_puestos > 0 else 0
        }
        
        return jsonify({
            'success': True,
            'data': {
                'puestos': puestos_data,
                'estadisticas': estadisticas
            }
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Error en obtener_puestos: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_municipal_bp.route('/consolidado', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_consolidado():
    """
    Obtener consolidado municipal
    
    Query params:
        tipo_eleccion_id: ID del tipo de elección (opcional)
    """
    try:
        from backend.models.formulario_e14 import FormularioE14, VotoPartido
        from backend.models.partido_politico import PartidoPolitico as Partido
        
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            return jsonify({
                'success': False,
                'error': 'Usuario no asignado a un municipio válido'
            }), 400
        
        # Obtener todos los puestos del municipio
        puestos = Location.query.filter_by(
            municipio_codigo=ubicacion.municipio_codigo,
            departamento_codigo=ubicacion.departamento_codigo,
            tipo='puesto'
        ).all()
        
        # Obtener todas las mesas de estos puestos
        mesa_ids = []
        for puesto in puestos:
            mesas = Location.query.filter_by(
                puesto_codigo=puesto.puesto_codigo,
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                zona_codigo=puesto.zona_codigo,
                tipo='mesa'
            ).all()
            mesa_ids.extend([m.id for m in mesas])
        
        # Obtener formularios validados
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids),
            FormularioE14.estado == 'validado'
        ).all()
        
        # Calcular totales
        total_votantes_registrados = sum(f.votantes_registrados or 0 for f in formularios)
        total_votos = sum(f.total_votos or 0 for f in formularios)
        votos_validos = sum(f.votos_validos or 0 for f in formularios)
        votos_nulos = sum(f.votos_nulos or 0 for f in formularios)
        votos_blanco = sum(f.votos_blanco or 0 for f in formularios)
        
        participacion_porcentaje = (total_votos / total_votantes_registrados * 100) if total_votantes_registrados > 0 else 0
        
        # Consolidar votos por partido
        votos_por_partido = {}
        for formulario in formularios:
            votos_partidos = VotoPartido.query.filter_by(formulario_id=formulario.id).all()
            for vp in votos_partidos:
                if vp.partido_id not in votos_por_partido:
                    partido = Partido.query.get(vp.partido_id)
                    votos_por_partido[vp.partido_id] = {
                        'partido_id': vp.partido_id,
                        'partido_nombre': partido.nombre if partido else 'Desconocido',
                        'partido_nombre_corto': partido.sigla if partido else 'N/A',
                        'partido_color': partido.color if partido else '#6c757d',
                        'total_votos': 0
                    }
                votos_por_partido[vp.partido_id]['total_votos'] += vp.votos
        
        # Calcular porcentajes
        votos_por_partido_lista = list(votos_por_partido.values())
        for vp in votos_por_partido_lista:
            vp['porcentaje'] = (vp['total_votos'] / votos_validos * 100) if votos_validos > 0 else 0
        
        # Ordenar por votos
        votos_por_partido_lista.sort(key=lambda x: x['total_votos'], reverse=True)
        
        consolidado = {
            'resumen': {
                'total_votantes_registrados': total_votantes_registrados,
                'total_votos': total_votos,
                'votos_validos': votos_validos,
                'votos_nulos': votos_nulos,
                'votos_blanco': votos_blanco,
                'participacion_porcentaje': round(participacion_porcentaje, 2)
            },
            'votos_por_partido': votos_por_partido_lista
        }
        
        return jsonify({
            'success': True,
            'data': consolidado
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Error en obtener_consolidado: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_municipal_bp.route('/puesto/<int:puesto_id>', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_puesto_detallado(puesto_id):
    """
    Obtener detalles completos de un puesto
    
    Path params:
        puesto_id: ID del puesto
    """
    try:
        from backend.models.formulario_e14 import FormularioE14
        
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        # Obtener puesto
        puesto = Location.query.get(puesto_id)
        
        if not puesto or puesto.tipo != 'puesto':
            return jsonify({
                'success': False,
                'error': 'Puesto no encontrado'
            }), 404
        
        # Verificar que el puesto pertenece al municipio del coordinador
        ubicacion = Location.query.get(user.ubicacion_id)
        if puesto.municipio_codigo != ubicacion.municipio_codigo:
            return jsonify({
                'success': False,
                'error': 'No tiene permisos para acceder a este puesto'
            }), 403
        
        # Obtener mesas del puesto
        mesas = Location.query.filter_by(
            puesto_codigo=puesto.puesto_codigo,
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo,
            tipo='mesa'
        ).all()
        
        mesa_ids = [m.id for m in mesas]
        
        # Contar formularios
        formularios_validados = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids),
            FormularioE14.estado == 'validado'
        ).count() if mesa_ids else 0
        
        formularios_pendientes = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids),
            FormularioE14.estado == 'pendiente'
        ).count() if mesa_ids else 0
        
        formularios_rechazados = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids),
            FormularioE14.estado == 'rechazado'
        ).count() if mesa_ids else 0
        
        # Calcular porcentaje de avance
        total_mesas = len(mesas)
        porcentaje_avance = (formularios_validados / total_mesas * 100) if total_mesas > 0 else 0
        
        # Buscar coordinador del puesto
        coordinador = User.query.filter_by(
            ubicacion_id=puesto.id,
            rol='coordinador_puesto',
            activo=True
        ).first()
        
        # Obtener información de mesas
        mesas_info = []
        for mesa in mesas[:10]:  # Limitar a 10 mesas para no sobrecargar
            formulario = FormularioE14.query.filter_by(mesa_id=mesa.id).first()
            mesas_info.append({
                'codigo': mesa.mesa_codigo or 'N/A',
                'votantes': mesa.total_votantes_registrados or 0,
                'estado': formulario.estado if formulario else 'sin_reporte'
            })
        
        # Obtener incidentes y delitos del puesto con detalles completos
        from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral, EvidenciaFotografica
        
        # Obtener incidentes con evidencias
        incidentes = IncidenteElectoral.query.filter_by(puesto_id=puesto.id).all()
        incidentes_data = []
        for inc in incidentes:
            # Obtener evidencias fotográficas
            evidencias = EvidenciaFotografica.query.filter_by(incidente_id=inc.id).all()
            
            incidentes_data.append({
                'id': inc.id,
                'tipo_incidente': inc.tipo_incidente,
                'tipo_incidente_label': inc.TIPOS_INCIDENTE.get(inc.tipo_incidente, inc.tipo_incidente),
                'titulo': inc.titulo,
                'descripcion': inc.descripcion,
                'severidad': inc.severidad,
                'severidad_label': inc.SEVERIDADES.get(inc.severidad, inc.severidad),
                'estado': inc.estado,
                'estado_label': inc.ESTADOS.get(inc.estado, inc.estado),
                'fecha_incidente': inc.fecha_incidente.isoformat() if inc.fecha_incidente else None,
                'fecha_reporte': inc.fecha_reporte.isoformat() if inc.fecha_reporte else None,
                'reportado_por': inc.reportado_por.nombre if inc.reportado_por else 'Desconocido',
                'ubicacion_gps': inc.ubicacion_gps,
                'notas_resolucion': inc.notas_resolucion,
                'evidencias': [{
                    'id': ev.id,
                    'url': ev.url,
                    'filename': ev.filename_original,
                    'fecha_subida': ev.fecha_subida.isoformat() if ev.fecha_subida else None
                } for ev in evidencias]
            })
        
        # Obtener delitos con evidencias
        delitos = DelitoElectoral.query.filter_by(puesto_id=puesto.id).all()
        delitos_data = []
        for delito in delitos:
            # Obtener evidencias fotográficas
            evidencias = EvidenciaFotografica.query.filter_by(delito_id=delito.id).all()
            
            delitos_data.append({
                'id': delito.id,
                'tipo_delito': delito.tipo_delito,
                'tipo_delito_label': delito.TIPOS_DELITO.get(delito.tipo_delito, delito.tipo_delito),
                'titulo': delito.titulo,
                'descripcion': delito.descripcion,
                'gravedad': delito.gravedad,
                'gravedad_label': delito.GRAVEDADES.get(delito.gravedad, delito.gravedad),
                'estado': delito.estado,
                'estado_label': delito.ESTADOS.get(delito.estado, delito.estado),
                'fecha_delito': delito.fecha_delito.isoformat() if delito.fecha_delito else None,
                'fecha_reporte': delito.fecha_reporte.isoformat() if delito.fecha_reporte else None,
                'reportado_por': delito.reportado_por.nombre if delito.reportado_por else 'Desconocido',
                'ubicacion_gps': delito.ubicacion_gps,
                'denunciado_formalmente': delito.denunciado_formalmente,
                'numero_denuncia': delito.numero_denuncia,
                'resultado_investigacion': delito.resultado_investigacion,
                'evidencias': [{
                    'id': ev.id,
                    'url': ev.url,
                    'filename': ev.filename_original,
                    'fecha_subida': ev.fecha_subida.isoformat() if ev.fecha_subida else None
                } for ev in evidencias]
            })
        
        puesto_detallado = {
            'puesto': {
                'id': puesto.id,
                'codigo': puesto.puesto_codigo,
                'nombre': puesto.puesto_nombre,
                'zona_codigo': puesto.zona_codigo,
                'total_mesas': total_mesas,
                'direccion': puesto.direccion
            },
            'coordinador': {
                'id': coordinador.id,
                'nombre': coordinador.nombre,
                'ultimo_acceso': coordinador.ultimo_acceso.isoformat() if coordinador.ultimo_acceso else None
            } if coordinador else None,
            'estadisticas': {
                'formularios_validados': formularios_validados,
                'formularios_pendientes': formularios_pendientes,
                'formularios_rechazados': formularios_rechazados,
                'porcentaje_avance': round(porcentaje_avance, 2),
                'incidentes': len(incidentes_data),
                'delitos': len(delitos_data)
            },
            'mesas': mesas_info,
            'incidentes': incidentes_data,
            'delitos': delitos_data
        }
        
        return jsonify({
            'success': True,
            'data': puesto_detallado
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Error en obtener_puesto_detallado: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_municipal_bp.route('/discrepancias', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_discrepancias():
    """
    Obtener puestos con discrepancias o anomalías
    """
    try:
        from backend.models.formulario_e14 import FormularioE14
        
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            return jsonify({
                'success': False,
                'error': 'Usuario no asignado a un municipio válido'
            }), 400
        
        # Obtener puestos del municipio
        puestos = Location.query.filter_by(
            municipio_codigo=ubicacion.municipio_codigo,
            departamento_codigo=ubicacion.departamento_codigo,
            tipo='puesto'
        ).all()
        
        discrepancias = []
        
        for puesto in puestos:
            # Obtener mesas del puesto
            mesas = Location.query.filter_by(
                puesto_codigo=puesto.puesto_codigo,
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                zona_codigo=puesto.zona_codigo,
                tipo='mesa'
            ).all()
            
            mesa_ids = [m.id for m in mesas]
            
            # Contar formularios rechazados
            formularios_rechazados = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids),
                FormularioE14.estado == 'rechazado'
            ).count() if mesa_ids else 0
            
            if formularios_rechazados > 0:
                discrepancias.append({
                    'puesto_id': puesto.id,
                    'puesto_nombre': puesto.puesto_nombre,
                    'puesto_codigo': puesto.puesto_codigo,
                    'descripcion': f'{formularios_rechazados} formulario(s) rechazado(s)',
                    'severidad': 'alta' if formularios_rechazados > 2 else 'media',
                    'tipo': 'formularios_rechazados',
                    'cantidad': formularios_rechazados
                })
        
        return jsonify({
            'success': True,
            'data': discrepancias
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Error en obtener_discrepancias: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



@coordinador_municipal_bp.route('/e24-municipal', methods=['POST'])
@jwt_required()
@role_required(['coordinador_municipal'])
def generar_e24_municipal():
    """
    Generar formulario E-24 Municipal
    
    Body:
        tipo_eleccion_id: ID del tipo de elección
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            raise ValidationException('Usuario no asignado a un municipio válido')
        
        data = request.get_json()
        if not data or 'tipo_eleccion_id' not in data:
            raise ValidationException('El tipo_eleccion_id es obligatorio')
        
        tipo_eleccion_id = data['tipo_eleccion_id']
        
        # Generar E-24
        e24_municipal = E24Service.generar_e24_municipal(
            ubicacion.id,
            tipo_eleccion_id,
            int(user_id)
        )
        
        # Registrar en audit log
        audit_log = AuditLog(
            user_id=int(user_id),
            accion='generar_e24_municipal',
            recurso='e24_municipal',
            recurso_id=e24_municipal.id,
            detalles={'tipo_eleccion_id': tipo_eleccion_id},
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Formulario E-24 Municipal generado exitosamente',
            'data': e24_municipal.to_dict(include_votos=True)
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_municipal_bp.route('/comparacion', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def comparar_puestos():
    """
    Comparar múltiples puestos
    
    Query params:
        puesto_ids: IDs de puestos separados por coma (ej: 1,2,3)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        # Obtener IDs de puestos
        puesto_ids_str = request.args.get('puesto_ids', '')
        if not puesto_ids_str:
            raise ValidationException('Se requiere al menos 2 puestos para comparar')
        
        try:
            puesto_ids = [int(pid) for pid in puesto_ids_str.split(',')]
        except ValueError:
            raise ValidationException('IDs de puestos inválidos')
        
        if len(puesto_ids) < 2:
            raise ValidationException('Se requiere al menos 2 puestos para comparar')
        
        if len(puesto_ids) > 5:
            raise ValidationException('Máximo 5 puestos para comparar')
        
        # Comparar puestos
        comparacion = MunicipalService.comparar_puestos(puesto_ids)
        
        if not comparacion:
            raise NotFoundException('No se pudieron comparar los puestos')
        
        return jsonify({
            'success': True,
            'data': comparacion
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_municipal_bp.route('/estadisticas', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_estadisticas():
    """
    Obtener estadísticas detalladas del municipio
    """
    try:
        from backend.models.formulario_e14 import FormularioE14
        
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            return jsonify({
                'success': False,
                'error': 'Usuario no asignado a un municipio válido'
            }), 400
        
        # Obtener puestos
        puestos = Location.query.filter_by(
            municipio_codigo=ubicacion.municipio_codigo,
            departamento_codigo=ubicacion.departamento_codigo,
            tipo='puesto'
        ).all()
        
        total_puestos = len(puestos)
        puestos_completos = 0
        puestos_incompletos = 0
        puestos_con_discrepancias = 0
        
        tasa_rechazo_por_puesto = []
        
        for puesto in puestos:
            # Obtener mesas
            mesas = Location.query.filter_by(
                puesto_codigo=puesto.puesto_codigo,
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                zona_codigo=puesto.zona_codigo,
                tipo='mesa'
            ).all()
            
            mesa_ids = [m.id for m in mesas]
            total_mesas = len(mesas)
            
            # Contar formularios
            formularios_validados = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids),
                FormularioE14.estado == 'validado'
            ).count() if mesa_ids else 0
            
            formularios_rechazados = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids),
                FormularioE14.estado == 'rechazado'
            ).count() if mesa_ids else 0
            
            total_formularios = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids)
            ).count() if mesa_ids else 0
            
            # Clasificar puesto
            if formularios_validados == total_mesas and total_mesas > 0:
                puestos_completos += 1
            elif formularios_rechazados > 0:
                puestos_con_discrepancias += 1
            else:
                puestos_incompletos += 1
            
            # Calcular tasa de rechazo
            if total_formularios > 0:
                tasa = (formularios_rechazados / total_formularios * 100)
                if tasa > 0:
                    tasa_rechazo_por_puesto.append({
                        'puesto_id': puesto.id,
                        'puesto_nombre': puesto.puesto_nombre,
                        'rechazados': formularios_rechazados,
                        'total': total_formularios,
                        'tasa_rechazo': round(tasa, 2)
                    })
        
        # Ordenar por tasa de rechazo
        tasa_rechazo_por_puesto.sort(key=lambda x: x['tasa_rechazo'], reverse=True)
        
        # Obtener consolidado
        consolidado_response = obtener_consolidado()
        consolidado_data = consolidado_response[0].get_json() if consolidado_response else {}
        consolidado = consolidado_data.get('data', {}) if consolidado_data.get('success') else {}
        
        estadisticas = {
            'resumen_general': {
                'total_puestos': total_puestos,
                'puestos_completos': puestos_completos,
                'puestos_incompletos': puestos_incompletos,
                'puestos_con_discrepancias': puestos_con_discrepancias,
                'porcentaje_avance': (puestos_completos / total_puestos * 100) if total_puestos > 0 else 0
            },
            'consolidado': consolidado.get('resumen', {}),
            'tasa_rechazo_por_puesto': tasa_rechazo_por_puesto[:10]  # Top 10
        }
        
        return jsonify({
            'success': True,
            'data': estadisticas
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Error en obtener_estadisticas: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_municipal_bp.route('/notificar', methods=['POST'])
@jwt_required()
@role_required(['coordinador_municipal'])
def enviar_notificacion():
    """
    Enviar notificación a coordinadores de puesto
    
    Body:
        puesto_ids: Lista de IDs de puestos
        mensaje: Mensaje a enviar
        prioridad: Prioridad (baja, normal, alta, urgente)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        data = request.get_json()
        if not data:
            raise ValidationException('No se proporcionaron datos')
        
        puesto_ids = data.get('puesto_ids', [])
        mensaje = data.get('mensaje', '').strip()
        prioridad = data.get('prioridad', 'normal')
        
        if not mensaje:
            raise ValidationException('El mensaje es obligatorio')
        
        if not puesto_ids:
            raise ValidationException('Debe seleccionar al menos un puesto')
        
        if prioridad not in ['baja', 'normal', 'alta', 'urgente']:
            prioridad = 'normal'
        
        # Obtener coordinadores de los puestos
        coordinadores = User.query.filter(
            User.ubicacion_id.in_(puesto_ids),
            User.rol == 'coordinador_puesto'
        ).all()
        
        if not coordinadores:
            raise NotFoundException('No se encontraron coordinadores para los puestos seleccionados')
        
        # Crear notificaciones
        notificaciones_creadas = []
        for coordinador in coordinadores:
            notificacion = Notificacion(
                remitente_id=int(user_id),
                destinatario_id=coordinador.id,
                mensaje=mensaje,
                prioridad=prioridad
            )
            db.session.add(notificacion)
            notificaciones_creadas.append(coordinador.nombre)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Notificación enviada a {len(notificaciones_creadas)} coordinador(es)',
            'data': {
                'destinatarios': notificaciones_creadas
            }
        }), 201
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_municipal_bp.route('/exportar', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def exportar_datos():
    """
    Exportar datos consolidados
    
    Query params:
        formato: Formato de exportación (csv, xlsx)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            raise ValidationException('Usuario no asignado a un municipio válido')
        
        formato = request.args.get('formato', 'csv').lower()
        
        if formato not in ['csv', 'xlsx']:
            raise ValidationException('Formato no soportado. Use csv o xlsx')
        
        # Obtener consolidado
        consolidado = ConsolidadoService.calcular_consolidado_municipal(ubicacion.id)
        
        if not consolidado:
            raise NotFoundException('No hay datos para exportar')
        
        # Generar CSV
        if formato == 'csv':
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Encabezados
            writer.writerow(['Municipio', ubicacion.municipio_nombre or ubicacion.nombre_completo])
            writer.writerow(['Código', ubicacion.municipio_codigo])
            writer.writerow(['Fecha de Generación', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow(['Coordinador', user.nombre])
            writer.writerow([])
            
            # Resumen
            resumen = consolidado.get('resumen', {})
            writer.writerow(['RESUMEN DE VOTACIÓN'])
            writer.writerow(['Total Votantes Registrados', resumen.get('total_votantes_registrados', 0)])
            writer.writerow(['Total Votos', resumen.get('total_votos', 0)])
            writer.writerow(['Votos Válidos', resumen.get('votos_validos', 0)])
            writer.writerow(['Votos Nulos', resumen.get('votos_nulos', 0)])
            writer.writerow(['Votos en Blanco', resumen.get('votos_blanco', 0)])
            writer.writerow(['Participación %', resumen.get('participacion_porcentaje', 0)])
            writer.writerow([])
            
            # Votos por partido
            writer.writerow(['VOTOS POR PARTIDO'])
            writer.writerow(['Partido', 'Votos', 'Porcentaje'])
            
            votos_por_partido = consolidado.get('votos_por_partido', [])
            for vp in votos_por_partido:
                writer.writerow([
                    vp['partido_nombre'],
                    vp['total_votos'],
                    f"{vp['porcentaje']:.2f}%"
                ])
            
            # Registrar en audit log
            audit_log = AuditLog(
                user_id=int(user_id),
                accion='exportar_datos',
                recurso='municipio',
                recurso_id=ubicacion.id,
                detalles={'formato': formato},
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent')
            )
            db.session.add(audit_log)
            db.session.commit()
            
            # Preparar respuesta
            output.seek(0)
            filename = f'consolidado_municipal_{ubicacion.municipio_codigo}_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.csv'
            
            return output.getvalue(), 200, {
                'Content-Type': 'text/csv',
                'Content-Disposition': f'attachment; filename={filename}'
            }
        
        else:
            # XLSX no implementado por ahora
            raise ValidationException('Formato XLSX no implementado aún')
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



@coordinador_municipal_bp.route('/e24-puestos', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_e24_puestos():
    """
    Obtener lista de E-24s de Puesto del municipio
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            raise ValidationException('Usuario no asignado a un municipio válido')
        
        # Obtener todos los puestos del municipio
        puestos = Location.query.filter_by(
            municipio_codigo=ubicacion.municipio_codigo,
            tipo='puesto'
        ).all()
        
        puesto_ids = [p.id for p in puestos]
        
        # Obtener E-24s de estos puestos
        from backend.models.coordinador_municipal import FormularioE24Puesto
        
        e24_puestos = FormularioE24Puesto.query.filter(
            FormularioE24Puesto.puesto_id.in_(puesto_ids)
        ).order_by(FormularioE24Puesto.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [e24.to_dict(include_votos=True) for e24 in e24_puestos]
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_municipal_bp.route('/consolidado-por-zona', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_consolidado_por_zona():
    """
    Obtener consolidado municipal agrupado por zona
    
    Query params:
        tipo_eleccion_id: ID del tipo de elección (opcional)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            raise ValidationException('Usuario no asignado a un municipio válido')
        
        tipo_eleccion_id = request.args.get('tipo_eleccion_id', type=int)
        
        # Obtener todas las zonas del municipio
        zonas = db.session.query(Location.zona_codigo, Location.zona_nombre).filter(
            Location.municipio_codigo == ubicacion.municipio_codigo,
            Location.tipo == 'puesto',
            Location.zona_codigo.isnot(None)
        ).distinct().all()
        
        consolidados_por_zona = []
        
        for zona_codigo, zona_nombre in zonas:
            # Obtener puestos de esta zona
            puestos_zona = Location.query.filter_by(
                municipio_codigo=ubicacion.municipio_codigo,
                zona_codigo=zona_codigo,
                tipo='puesto'
            ).all()
            
            # Calcular consolidado de la zona
            total_votos_zona = 0
            votos_por_partido_zona = {}
            total_puestos = len(puestos_zona)
            puestos_completos = 0
            
            for puesto in puestos_zona:
                consolidado_puesto = ConsolidadoService.calcular_consolidado_puesto(puesto.id, tipo_eleccion_id)
                
                if consolidado_puesto:
                    resumen = consolidado_puesto.get('resumen', {})
                    total_votos_zona += resumen.get('total_votos', 0)
                    
                    # Sumar votos por partido
                    for vp in consolidado_puesto.get('votos_por_partido', []):
                        partido_id = vp['partido_id']
                        if partido_id not in votos_por_partido_zona:
                            votos_por_partido_zona[partido_id] = {
                                'partido_id': partido_id,
                                'partido_nombre': vp['partido_nombre'],
                                'partido_nombre_corto': vp['partido_nombre_corto'],
                                'partido_color': vp['partido_color'],
                                'total_votos': 0
                            }
                        votos_por_partido_zona[partido_id]['total_votos'] += vp['total_votos']
                    
                    # Verificar si el puesto está completo
                    if consolidado_puesto.get('puesto', {}).get('mesas_validadas', 0) == consolidado_puesto.get('puesto', {}).get('total_mesas', 0):
                        puestos_completos += 1
            
            # Calcular porcentajes
            votos_por_partido_lista = list(votos_por_partido_zona.values())
            for vp in votos_por_partido_lista:
                vp['porcentaje'] = (vp['total_votos'] / total_votos_zona * 100) if total_votos_zona > 0 else 0
            
            # Ordenar por votos
            votos_por_partido_lista.sort(key=lambda x: x['total_votos'], reverse=True)
            
            consolidados_por_zona.append({
                'zona_codigo': zona_codigo,
                'zona_nombre': zona_nombre or f'Zona {zona_codigo}',
                'total_puestos': total_puestos,
                'puestos_completos': puestos_completos,
                'porcentaje_avance': (puestos_completos / total_puestos * 100) if total_puestos > 0 else 0,
                'total_votos': total_votos_zona,
                'votos_por_partido': votos_por_partido_lista
            })
        
        # Ordenar por zona_codigo
        consolidados_por_zona.sort(key=lambda x: x['zona_codigo'])
        
        return jsonify({
            'success': True,
            'data': consolidados_por_zona
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ENDPOINTS DE INCIDENTES
# ============================================================================

@coordinador_municipal_bp.route('/incidentes', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_incidentes():
    """
    Obtener incidentes del municipio
    
    Query params:
        estado: Filtrar por estado (reportado, en_revision, resuelto, escalado)
        severidad: Filtrar por severidad (baja, media, alta, critica)
        tipo: Filtrar por tipo de incidente
        fecha_desde: Fecha desde (YYYY-MM-DD)
        fecha_hasta: Fecha hasta (YYYY-MM-DD)
    """
    try:
      
        from backend.models.incidentes_delitos import IncidenteElectoral
        
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            return jsonify({
                'success': False,
                'error': 'Usuario no asignado a un municipio válido'
            }), 400
        
        # Obtener puestos del municipio
        puestos = Location.query.filter_by(
            municipio_codigo=ubicacion.municipio_codigo,
            departamento_codigo=ubicacion.departamento_codigo,
            tipo='puesto'
        ).all()
        
        # Obtener mesas de estos puestos
        mesa_ids = []
        for puesto in puestos:
            mesas = Location.query.filter_by(
                puesto_codigo=puesto.puesto_codigo,
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                zona_codigo=puesto.zona_codigo,
                tipo='mesa'
            ).all()
            mesa_ids.extend([m.id for m in mesas])
        
        # Query base
        query = IncidenteElectoral.query.filter(
            IncidenteElectoral.mesa_id.in_(mesa_ids)
        )
        
        # Aplicar filtros
        estado = request.args.get('estado')
        if estado:
            query = query.filter(IncidenteElectoral.estado == estado)
        
        severidad = request.args.get('severidad')
        if severidad:
            query = query.filter(IncidenteElectoral.severidad == severidad)
        
        tipo = request.args.get('tipo')
        if tipo:
            query = query.filter(IncidenteElectoral.tipo == tipo)
        
        # Ordenar por fecha de creación (más recientes primero)
        incidentes = query.order_by(IncidenteElectoral.created_at.desc()).all()
        
        # Formatear respuesta
        incidentes_data = []
        for incidente in incidentes:
            mesa = Location.query.get(incidente.mesa_id)
            reportante = User.query.get(incidente.reportado_por) if incidente.reportado_por else None
            
            incidentes_data.append({
                'id': incidente.id,
                'tipo': incidente.tipo,
                'descripcion': incidente.descripcion,
                'severidad': incidente.severidad,
                'estado': incidente.estado,
                'mesa': {
                    'id': mesa.id,
                    'codigo': mesa.mesa_codigo,
                    'nombre': mesa.nombre_completo,
                    'puesto_nombre': mesa.puesto_nombre
                } if mesa else None,
                'reportante': {
                    'id': reportante.id,
                    'nombre': reportante.nombre
                } if reportante else None,
                'fecha_reporte': incidente.created_at.isoformat() if incidente.created_at else None,
                'fecha_resolucion': incidente.fecha_resolucion.isoformat() if incidente.fecha_resolucion else None,
                'tiene_evidencia': bool(incidente.evidencia_url)
            })
        
        return jsonify({
            'success': True,
            'data': incidentes_data,
            'total': len(incidentes_data)
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Error en obtener_incidentes: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ENDPOINTS DE DELITOS
# ============================================================================

@coordinador_municipal_bp.route('/delitos', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_delitos():
    """
    Obtener delitos electorales del municipio
    
    Query params:
        estado: Filtrar por estado (reportado, en_investigacion, investigado, archivado)
        gravedad: Filtrar por gravedad (leve, grave, muy_grave)
        tipo: Filtrar por tipo de delito
    """
    try:
        from backend.models.incidentes_delitos import DelitoElectoral
        
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            return jsonify({
                'success': False,
                'error': 'Usuario no asignado a un municipio válido'
            }), 400
        
        # Obtener puestos del municipio
        puestos = Location.query.filter_by(
            municipio_codigo=ubicacion.municipio_codigo,
            departamento_codigo=ubicacion.departamento_codigo,
            tipo='puesto'
        ).all()
        
        # Obtener mesas de estos puestos
        mesa_ids = []
        for puesto in puestos:
            mesas = Location.query.filter_by(
                puesto_codigo=puesto.puesto_codigo,
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                zona_codigo=puesto.zona_codigo,
                tipo='mesa'
            ).all()
            mesa_ids.extend([m.id for m in mesas])
        
        # Query base
        query = DelitoElectoral.query.filter(
            DelitoElectoral.mesa_id.in_(mesa_ids)
        )
        
        # Aplicar filtros
        estado = request.args.get('estado')
        if estado:
            query = query.filter(DelitoElectoral.estado == estado)
        
        gravedad = request.args.get('gravedad')
        if gravedad:
            query = query.filter(DelitoElectoral.gravedad == gravedad)
        
        tipo = request.args.get('tipo')
        if tipo:
            query = query.filter(DelitoElectoral.tipo == tipo)
        
        # Ordenar por fecha de creación (más recientes primero)
        delitos = query.order_by(DelitoElectoral.created_at.desc()).all()
        
        # Formatear respuesta
        delitos_data = []
        for delito in delitos:
            mesa = Location.query.get(delito.mesa_id)
            reportante = User.query.get(delito.reportado_por) if delito.reportado_por else None
            
            delitos_data.append({
                'id': delito.id,
                'tipo': delito.tipo,
                'descripcion': delito.descripcion,
                'gravedad': delito.gravedad,
                'estado': delito.estado,
                'mesa': {
                    'id': mesa.id,
                    'codigo': mesa.mesa_codigo,
                    'nombre': mesa.nombre_completo,
                    'puesto_nombre': mesa.puesto_nombre
                } if mesa else None,
                'reportante': {
                    'id': reportante.id,
                    'nombre': reportante.nombre
                } if reportante else None,
                'fecha_reporte': delito.created_at.isoformat() if delito.created_at else None,
                'tiene_evidencia': bool(delito.evidencia_url),
                'autoridad_notificada': delito.autoridad_notificada
            })
        
        return jsonify({
            'success': True,
            'data': delitos_data,
            'total': len(delitos_data)
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Error en obtener_delitos: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ENDPOINTS DE COORDINADORES
# ============================================================================

@coordinador_municipal_bp.route('/coordinadores', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_coordinadores():
    """
    Obtener lista de coordinadores de puesto del municipio
    
    Query params:
        estado: Filtrar por estado de conexión (activo, inactivo, ausente)
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
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            return jsonify({
                'success': False,
                'error': 'Usuario no asignado a un municipio válido'
            }), 400
        
        # Obtener puestos del municipio
        puestos = Location.query.filter_by(
            municipio_codigo=ubicacion.municipio_codigo,
            departamento_codigo=ubicacion.departamento_codigo,
            tipo='puesto',
            activo=True
        ).all()
        
        puesto_ids = [p.id for p in puestos]
        
        # Obtener coordinadores de estos puestos
        coordinadores = User.query.filter(
            User.ubicacion_id.in_(puesto_ids),
            User.rol == 'coordinador_puesto',
            User.activo == True
        ).all()
        
        # Formatear respuesta
        coordinadores_data = []
        for coord in coordinadores:
            puesto = Location.query.get(coord.ubicacion_id)
            
            # Determinar estado de conexión
            from datetime import datetime, timedelta
            estado_conexion = 'ausente'
            if coord.ultimo_acceso:
                tiempo_inactivo = datetime.utcnow() - coord.ultimo_acceso
                if tiempo_inactivo < timedelta(minutes=5):
                    estado_conexion = 'activo'
                elif tiempo_inactivo < timedelta(hours=1):
                    estado_conexion = 'inactivo'
            
            # Obtener estadísticas del puesto
            mesas = Location.query.filter_by(
                puesto_codigo=puesto.puesto_codigo,
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                zona_codigo=puesto.zona_codigo,
                tipo='mesa'
            ).all() if puesto else []
            
            mesa_ids = [m.id for m in mesas]
            
            from backend.models.formulario_e14 import FormularioE14
            formularios_validados = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids),
                FormularioE14.estado == 'validado'
            ).count() if mesa_ids else 0
            
            total_mesas = len(mesas)
            porcentaje_avance = (formularios_validados / total_mesas * 100) if total_mesas > 0 else 0
            
            coordinadores_data.append({
                'id': coord.id,
                'nombre': coord.nombre,
                'puesto': {
                    'id': puesto.id,
                    'codigo': puesto.puesto_codigo,
                    'nombre': puesto.puesto_nombre,
                    'zona_codigo': puesto.zona_codigo
                } if puesto else None,
                'estado_conexion': estado_conexion,
                'ultimo_acceso': coord.ultimo_acceso.isoformat() if coord.ultimo_acceso else None,
                'estadisticas': {
                    'total_mesas': total_mesas,
                    'formularios_validados': formularios_validados,
                    'porcentaje_avance': round(porcentaje_avance, 2)
                },
                'latitud': coord.ultima_latitud,
                'longitud': coord.ultima_longitud
            })
        
        # Aplicar filtro de estado si se proporciona
        filtro_estado = request.args.get('estado')
        if filtro_estado:
            coordinadores_data = [c for c in coordinadores_data if c['estado_conexion'] == filtro_estado]
        
        # Ordenar por estado de conexión (activos primero)
        orden_estado = {'activo': 0, 'inactivo': 1, 'ausente': 2}
        coordinadores_data.sort(key=lambda x: orden_estado.get(x['estado_conexion'], 3))
        
        return jsonify({
            'success': True,
            'data': coordinadores_data,
            'total': len(coordinadores_data)
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Error en obtener_coordinadores: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ENDPOINTS DE GEOLOCALIZACIÓN
# ============================================================================

@coordinador_municipal_bp.route('/geolocalizacion', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_geolocalizacion():
    """
    Obtener datos de geolocalización del municipio para el mapa
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
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            return jsonify({
                'success': False,
                'error': 'Usuario no asignado a un municipio válido'
            }), 400
        
        # Obtener puestos del municipio con coordenadas
        puestos = Location.query.filter_by(
            municipio_codigo=ubicacion.municipio_codigo,
            departamento_codigo=ubicacion.departamento_codigo,
            tipo='puesto',
            activo=True
        ).filter(
            Location.latitud.isnot(None),
            Location.longitud.isnot(None)
        ).all()
        
        puestos_data = []
        for puesto in puestos:
            # Obtener estadísticas del puesto
            mesas = Location.query.filter_by(
                puesto_codigo=puesto.puesto_codigo,
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                zona_codigo=puesto.zona_codigo,
                tipo='mesa'
            ).all()
            
            mesa_ids = [m.id for m in mesas]
            
            from backend.models.formulario_e14 import FormularioE14
            formularios_validados = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids),
                FormularioE14.estado == 'validado'
            ).count() if mesa_ids else 0
            
            total_mesas = len(mesas)
            
            puestos_data.append({
                'id': puesto.id,
                'codigo': puesto.puesto_codigo,
                'nombre': puesto.puesto_nombre,
                'zona_codigo': puesto.zona_codigo,
                'latitud': float(puesto.latitud),
                'longitud': float(puesto.longitud),
                'direccion': puesto.direccion,
                'total_mesas': total_mesas,
                'formularios_validados': formularios_validados,
                'porcentaje_avance': (formularios_validados / total_mesas * 100) if total_mesas > 0 else 0
            })
        
        # Obtener coordinadores con geolocalización
        coordinadores = User.query.filter(
            User.ubicacion_id.in_([p.id for p in puestos]),
            User.rol == 'coordinador_puesto',
            User.activo == True
        ).filter(
            User.ultima_latitud.isnot(None),
            User.ultima_longitud.isnot(None)
        ).all()
        
        coordinadores_data = []
        for coord in coordinadores:
            puesto = Location.query.get(coord.ubicacion_id)
            
            # Determinar estado de conexión
            from datetime import datetime, timedelta
            estado_conexion = 'ausente'
            if coord.ultimo_acceso:
                tiempo_inactivo = datetime.utcnow() - coord.ultimo_acceso
                if tiempo_inactivo < timedelta(minutes=5):
                    estado_conexion = 'activo'
                elif tiempo_inactivo < timedelta(hours=1):
                    estado_conexion = 'inactivo'
            
            coordinadores_data.append({
                'id': coord.id,
                'nombre': coord.nombre,
                'latitud': float(coord.ultima_latitud),
                'longitud': float(coord.ultima_longitud),
                'estado_conexion': estado_conexion,
                'puesto': {
                    'id': puesto.id,
                    'codigo': puesto.puesto_codigo,
                    'nombre': puesto.puesto_nombre
                } if puesto else None,
                'ultimo_acceso': coord.ultimo_acceso.isoformat() if coord.ultimo_acceso else None
            })
        
        return jsonify({
            'success': True,
            'data': {
                'puestos': puestos_data,
                'coordinadores': coordinadores_data,
                'centro': {
                    'latitud': float(ubicacion.latitud) if ubicacion.latitud else 1.6,
                    'longitud': float(ubicacion.longitud) if ubicacion.longitud else -75.6
                }
            }
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Error en obtener_geolocalizacion: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ENDPOINT DE GEOLOCALIZACIÓN PARA MAPA
# ============================================================================

@coordinador_municipal_bp.route('/mapa-datos', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_datos_mapa():
    """
    Obtener datos completos para el mapa del coordinador municipal
    Incluye: puestos, coordinadores, testigos, incidentes, delitos
    
    Query params:
        zona: Filtrar por zona
        estado: Filtrar por estado (completo, incompleto, con_discrepancias)
    """
    try:
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
        from datetime import datetime, timedelta
        
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            return jsonify({
                'success': False,
                'error': 'Usuario no asignado a un municipio válido'
            }), 400
        
        # Filtros
        filtro_zona = request.args.get('zona')
        filtro_estado = request.args.get('estado')
        
        # Obtener puestos del municipio
        query_puestos = Location.query.filter_by(
            municipio_codigo=ubicacion.municipio_codigo,
            departamento_codigo=ubicacion.departamento_codigo,
            tipo='puesto',
            activo=True
        )
        
        if filtro_zona:
            query_puestos = query_puestos.filter_by(zona_codigo=filtro_zona)
        
        puestos = query_puestos.all()
        
        # Datos para el mapa
        puestos_data = []
        coordinadores_data = []
        testigos_data = []
        incidentes_data = []
        delitos_data = []
        
        for puesto in puestos:
            # Obtener mesas del puesto
            mesas = Location.query.filter_by(
                puesto_codigo=puesto.puesto_codigo,
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                zona_codigo=puesto.zona_codigo,
                tipo='mesa',
                activo=True
            ).all()
            
            mesa_ids = [m.id for m in mesas]
            total_mesas = len(mesas)
            
            # Contar formularios
            formularios_validados = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids),
                FormularioE14.estado == 'validado'
            ).count() if mesa_ids else 0
            
            formularios_rechazados = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids),
                FormularioE14.estado == 'rechazado'
            ).count() if mesa_ids else 0
            
            # Determinar estado
            if formularios_validados == total_mesas and total_mesas > 0:
                estado = 'completo'
            elif formularios_rechazados > 0:
                estado = 'con_discrepancias'
            else:
                estado = 'incompleto'
            
            # Aplicar filtro de estado
            if filtro_estado and estado != filtro_estado:
                continue
            
            # Calcular porcentaje
            porcentaje_avance = (formularios_validados / total_mesas * 100) if total_mesas > 0 else 0
            
            # Buscar coordinador del puesto
            coordinador = User.query.filter_by(
                ubicacion_id=puesto.id,
                rol='coordinador_puesto',
                activo=True
            ).first()
            
            # Contar incidentes y delitos
            incidentes_count = IncidenteElectoral.query.filter(
                IncidenteElectoral.mesa_id.in_(mesa_ids)
            ).count() if mesa_ids else 0
            
            delitos_count = DelitoElectoral.query.filter(
                DelitoElectoral.mesa_id.in_(mesa_ids)
            ).count() if mesa_ids else 0
            
            # Datos del puesto para el mapa
            puesto_info = {
                'id': puesto.id,
                'tipo': 'puesto',
                'codigo': puesto.puesto_codigo,
                'nombre': puesto.puesto_nombre,
                'zona_codigo': puesto.zona_codigo,
                'latitud': puesto.latitud,
                'longitud': puesto.longitud,
                'direccion': puesto.direccion,
                'total_mesas': total_mesas,
                'formularios_validados': formularios_validados,
                'formularios_rechazados': formularios_rechazados,
                'porcentaje_avance': round(porcentaje_avance, 2),
                'estado': estado,
                'incidentes': incidentes_count,
                'delitos': delitos_count,
                'tiene_alertas': incidentes_count > 0 or delitos_count > 0 or formularios_rechazados > 0,
                'coordinador': {
                    'id': coordinador.id,
                    'nombre': coordinador.nombre,
                    'ultimo_acceso': coordinador.ultimo_acceso.isoformat() if coordinador.ultimo_acceso else None
                } if coordinador else None
            }
            
            puestos_data.append(puesto_info)
            
            # Agregar coordinador si tiene geolocalización
            if coordinador and coordinador.ultima_latitud and coordinador.ultima_longitud:
                # Determinar estado de conexión
                estado_conexion = 'ausente'
                if coordinador.ultimo_acceso:
                    tiempo_inactivo = datetime.utcnow() - coordinador.ultimo_acceso
                    if tiempo_inactivo < timedelta(minutes=5):
                        estado_conexion = 'activo'
                    elif tiempo_inactivo < timedelta(hours=1):
                        estado_conexion = 'inactivo'
                
                coordinadores_data.append({
                    'id': coordinador.id,
                    'tipo': 'coordinador',
                    'nombre': coordinador.nombre,
                    'rol': coordinador.rol,
                    'latitud': coordinador.ultima_latitud,
                    'longitud': coordinador.ultima_longitud,
                    'precision': coordinador.precision_geolocalizacion,
                    'ultima_actualizacion': coordinador.ultima_geolocalizacion_at.isoformat() if coordinador.ultima_geolocalizacion_at else None,
                    'estado_conexion': estado_conexion,
                    'puesto': {
                        'id': puesto.id,
                        'nombre': puesto.puesto_nombre,
                        'codigo': puesto.puesto_codigo
                    }
                })
            
            # Agregar testigos con geolocalización
            testigos = User.query.filter_by(
                ubicacion_id=puesto.id,
                rol='testigo_electoral',
                activo=True
            ).filter(
                User.ultima_latitud.isnot(None),
                User.ultima_longitud.isnot(None)
            ).all()
            
            for testigo in testigos:
                # Determinar estado de conexión
                estado_conexion = 'ausente'
                if testigo.ultimo_acceso:
                    tiempo_inactivo = datetime.utcnow() - testigo.ultimo_acceso
                    if tiempo_inactivo < timedelta(minutes=5):
                        estado_conexion = 'activo'
                    elif tiempo_inactivo < timedelta(hours=1):
                        estado_conexion = 'inactivo'
                
                testigos_data.append({
                    'id': testigo.id,
                    'tipo': 'testigo',
                    'nombre': testigo.nombre,
                    'rol': testigo.rol,
                    'latitud': testigo.ultima_latitud,
                    'longitud': testigo.ultima_longitud,
                    'precision': testigo.precision_geolocalizacion,
                    'ultima_actualizacion': testigo.ultima_geolocalizacion_at.isoformat() if testigo.ultima_geolocalizacion_at else None,
                    'estado_conexion': estado_conexion,
                    'presencia_verificada': testigo.presencia_verificada,
                    'puesto': {
                        'id': puesto.id,
                        'nombre': puesto.puesto_nombre,
                        'codigo': puesto.puesto_codigo
                    }
                })
            
            # Agregar incidentes con geolocalización
            incidentes = IncidenteElectoral.query.filter(
                IncidenteElectoral.mesa_id.in_(mesa_ids),
                IncidenteElectoral.ubicacion_gps.isnot(None)
            ).all() if mesa_ids else []
            
            for incidente in incidentes:
                if incidente.ubicacion_gps:
                    try:
                        lat, lng = map(float, incidente.ubicacion_gps.split(','))
                        incidentes_data.append({
                            'id': incidente.id,
                            'tipo': 'incidente',
                            'tipo_incidente': incidente.tipo_incidente,
                            'titulo': incidente.titulo,
                            'descripcion': incidente.descripcion,
                            'severidad': incidente.severidad,
                            'estado': incidente.estado,
                            'latitud': lat,
                            'longitud': lng,
                            'fecha_reporte': incidente.fecha_reporte.isoformat() if incidente.fecha_reporte else None,
                            'puesto': {
                                'id': puesto.id,
                                'nombre': puesto.puesto_nombre,
                                'codigo': puesto.puesto_codigo
                            }
                        })
                    except:
                        pass
            
            # Agregar delitos con geolocalización
            delitos = DelitoElectoral.query.filter(
                DelitoElectoral.mesa_id.in_(mesa_ids),
                DelitoElectoral.ubicacion_gps.isnot(None)
            ).all() if mesa_ids else []
            
            for delito in delitos:
                if delito.ubicacion_gps:
                    try:
                        lat, lng = map(float, delito.ubicacion_gps.split(','))
                        delitos_data.append({
                            'id': delito.id,
                            'tipo': 'delito',
                            'tipo_delito': delito.tipo_delito,
                            'titulo': delito.titulo,
                            'descripcion': delito.descripcion,
                            'gravedad': delito.gravedad,
                            'estado': delito.estado,
                            'latitud': lat,
                            'longitud': lng,
                            'fecha_reporte': delito.fecha_reporte.isoformat() if delito.fecha_reporte else None,
                            'puesto': {
                                'id': puesto.id,
                                'nombre': puesto.puesto_nombre,
                                'codigo': puesto.puesto_codigo
                            }
                        })
                    except:
                        pass
        
        # Centro del mapa (municipio)
        centro = {
            'latitud': ubicacion.latitud or 1.6144,
            'longitud': ubicacion.longitud or -75.6062,
            'zoom': 12
        }
        
        # Estadísticas generales
        estadisticas = {
            'total_puestos': len(puestos_data),
            'puestos_completos': len([p for p in puestos_data if p['estado'] == 'completo']),
            'puestos_incompletos': len([p for p in puestos_data if p['estado'] == 'incompleto']),
            'puestos_con_discrepancias': len([p for p in puestos_data if p['estado'] == 'con_discrepancias']),
            'coordinadores_activos': len([c for c in coordinadores_data if c['estado_conexion'] == 'activo']),
            'testigos_activos': len([t for t in testigos_data if t['estado_conexion'] == 'activo']),
            'total_incidentes': len(incidentes_data),
            'total_delitos': len(delitos_data)
        }
        
        return jsonify({
            'success': True,
            'data': {
                'centro': centro,
                'puestos': puestos_data,
                'coordinadores': coordinadores_data,
                'testigos': testigos_data,
                'incidentes': incidentes_data,
                'delitos': delitos_data,
                'estadisticas': estadisticas
            }
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Error en obtener_datos_mapa: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_municipal_bp.route('/zonas', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_zonas():
    """
    Obtener lista de zonas del municipio para filtros
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
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            return jsonify({
                'success': False,
                'error': 'Usuario no asignado a un municipio válido'
            }), 400
        
        # Obtener zonas únicas del municipio
        zonas = db.session.query(
            Location.zona_codigo,
            db.func.count(Location.id).label('total_puestos')
        ).filter(
            Location.municipio_codigo == ubicacion.municipio_codigo,
            Location.departamento_codigo == ubicacion.departamento_codigo,
            Location.tipo == 'puesto',
            Location.zona_codigo.isnot(None),
            Location.activo == True
        ).group_by(Location.zona_codigo).all()
        
        zonas_data = [{
            'codigo': zona.zona_codigo,
            'nombre': f'Zona {zona.zona_codigo}',
            'total_puestos': zona.total_puestos
        } for zona in zonas]
        
        # Ordenar por código
        zonas_data.sort(key=lambda x: x['codigo'])
        
        return jsonify({
            'success': True,
            'data': zonas_data
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Error en obtener_zonas: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
