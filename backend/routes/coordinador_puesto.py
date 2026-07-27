"""
Rutas para Coordinador de Puesto
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.location import Location
from backend.models.formulario_e14 import FormularioE14
from backend.database import db

coordinador_puesto_bp = Blueprint('coordinador_puesto', __name__)


@coordinador_puesto_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Estadísticas del puesto"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        puesto = Location.query.get(user.ubicacion_id)
        
        # Obtener mesas del puesto
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo,
            puesto_codigo=puesto.puesto_codigo,
            activo=True
        ).all()
        
        # Obtener testigos del puesto
        testigos = User.query.filter_by(
            ubicacion_id=puesto.id,
            rol='testigo_electoral',
            activo=True
        ).all()
        
        # Obtener formularios del puesto
        mesa_ids = [m.id for m in mesas]
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).all() if mesa_ids else []
        
        formularios_completados = sum(1 for f in formularios if f.estado == 'completado')
        
        stats = {
            'total_mesas': len(mesas),
            'total_testigos': len(testigos),
            'testigos_presentes': sum(1 for t in testigos if t.presencia_verificada),
            'total_formularios': len(formularios),
            'formularios_completados': formularios_completados,
            'formularios_pendientes': len(formularios) - formularios_completados,
            'porcentaje_avance': (formularios_completados / len(formularios) * 100) if formularios else 0,
            'puesto': {
                'id': puesto.id,
                'nombre': puesto.nombre_completo,
                'codigo': puesto.puesto_codigo
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


@coordinador_puesto_bp.route('/mesas', methods=['GET'])
@jwt_required()
def get_mesas():
    """Obtener mesas del puesto"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        puesto = Location.query.get(user.ubicacion_id)
        
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
            # Buscar formulario de la mesa
            formulario = FormularioE14.query.filter_by(mesa_id=mesa.id).first()
            
            mesas_data.append({
                'id': mesa.id,
                'nombre_completo': mesa.nombre_completo,
                'mesa_codigo': mesa.mesa_codigo,
                'total_votantes_registrados': mesa.total_votantes_registrados,
                'mujeres': mesa.mujeres,
                'hombres': mesa.hombres,
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


@coordinador_puesto_bp.route('/testigos', methods=['GET'])
@jwt_required()
def get_testigos():
    """Obtener testigos del puesto"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        testigos = User.query.filter_by(
            ubicacion_id=user.ubicacion_id,
            rol='testigo_electoral',
            activo=True
        ).all()
        
        testigos_data = []
        for testigo in testigos:
            testigos_data.append({
                'id': testigo.id,
                'nombre': testigo.nombre,
                'presencia_verificada': testigo.presencia_verificada,
                'presencia_verificada_at': testigo.presencia_verificada_at.isoformat() if testigo.presencia_verificada_at else None,
                'ultimo_acceso': testigo.ultimo_acceso.isoformat() if testigo.ultimo_acceso else None
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


@coordinador_puesto_bp.route('/incidentes', methods=['GET'])
@jwt_required()
def get_incidentes():
    """Obtener incidentes del puesto con evidencias fotográficas"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        puesto = Location.query.get(user.ubicacion_id)
        
        # Importar modelos de incidentes y delitos
        from backend.models.incidente_electoral import IncidenteElectoral
        from backend.models.evidencia_fotografica import EvidenciaFotografica
        
        # Obtener incidentes del puesto
        incidentes = IncidenteElectoral.query.join(
            Location, IncidenteElectoral.mesa_id == Location.id
        ).filter(
            Location.puesto_codigo == puesto.puesto_codigo,
            Location.municipio_codigo == puesto.municipio_codigo,
            Location.departamento_codigo == puesto.departamento_codigo
        ).order_by(IncidenteElectoral.fecha_reporte.desc()).all()
        
        incidentes_data = []
        for inc in incidentes:
            # Obtener evidencias fotográficas
            evidencias = EvidenciaFotografica.query.filter_by(
                incidente_id=inc.id
            ).all()
            
            mesa = Location.query.get(inc.mesa_id)
            reportado_por = User.query.get(inc.reportado_por_id)
            
            incidentes_data.append({
                'id': inc.id,
                'titulo': inc.titulo,
                'descripcion': inc.descripcion,
                'tipo_incidente': inc.tipo_incidente,
                'tipo_incidente_label': inc.get_tipo_incidente_label(),
                'severidad': inc.severidad,
                'severidad_label': inc.get_severidad_label(),
                'estado': inc.estado,
                'estado_label': inc.get_estado_label(),
                'fecha_reporte': inc.fecha_reporte.isoformat() if inc.fecha_reporte else None,
                'ubicacion_gps': inc.ubicacion_gps,
                'notas_resolucion': inc.notas_resolucion,
                'mesa_id': inc.mesa_id,
                'mesa_codigo': mesa.mesa_codigo if mesa else None,
                'reportado_por_id': inc.reportado_por_id,
                'reportado_por_nombre': reportado_por.nombre if reportado_por else 'Desconocido',
                'evidencias': [{
                    'id': ev.id,
                    'filename': ev.filename,
                    'url': ev.url,
                    'tipo': ev.tipo,
                    'descripcion': ev.descripcion
                } for ev in evidencias]
            })
        
        return jsonify({
            'success': True,
            'data': incidentes_data,
            'total': len(incidentes_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_puesto_bp.route('/delitos', methods=['GET'])
@jwt_required()
def get_delitos():
    """Obtener delitos del puesto con evidencias fotográficas"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        puesto = Location.query.get(user.ubicacion_id)
        
        # Importar modelos de delitos
        from backend.models.delito_electoral import DelitoElectoral
        from backend.models.evidencia_fotografica import EvidenciaFotografica
        
        # Obtener delitos del puesto
        delitos = DelitoElectoral.query.join(
            Location, DelitoElectoral.mesa_id == Location.id
        ).filter(
            Location.puesto_codigo == puesto.puesto_codigo,
            Location.municipio_codigo == puesto.municipio_codigo,
            Location.departamento_codigo == puesto.departamento_codigo
        ).order_by(DelitoElectoral.fecha_reporte.desc()).all()
        
        delitos_data = []
        for delito in delitos:
            # Obtener evidencias fotográficas
            evidencias = EvidenciaFotografica.query.filter_by(
                delito_id=delito.id
            ).all()
            
            mesa = Location.query.get(delito.mesa_id)
            reportado_por = User.query.get(delito.reportado_por_id)
            
            delitos_data.append({
                'id': delito.id,
                'titulo': delito.titulo,
                'descripcion': delito.descripcion,
                'tipo_delito': delito.tipo_delito,
                'tipo_delito_label': delito.get_tipo_delito_label(),
                'gravedad': delito.gravedad,
                'gravedad_label': delito.get_gravedad_label(),
                'estado': delito.estado,
                'estado_label': delito.get_estado_label(),
                'fecha_reporte': delito.fecha_reporte.isoformat() if delito.fecha_reporte else None,
                'ubicacion_gps': delito.ubicacion_gps,
                'testigos_adicionales': delito.testigos_adicionales,
                'denunciado_formalmente': delito.denunciado_formalmente,
                'numero_denuncia': delito.numero_denuncia,
                'resultado_investigacion': delito.resultado_investigacion,
                'mesa_id': delito.mesa_id,
                'mesa_codigo': mesa.mesa_codigo if mesa else None,
                'reportado_por_id': delito.reportado_por_id,
                'reportado_por_nombre': reportado_por.nombre if reportado_por else 'Desconocido',
                'evidencias': [{
                    'id': ev.id,
                    'filename': ev.filename,
                    'url': ev.url,
                    'tipo': ev.tipo,
                    'descripcion': ev.descripcion
                } for ev in evidencias]
            })
        
        return jsonify({
            'success': True,
            'data': delitos_data,
            'total': len(delitos_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_puesto_bp.route('/formularios', methods=['GET'])
@jwt_required()
def get_formularios():
    """Obtener formularios del puesto"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        puesto = Location.query.get(user.ubicacion_id)
        
        # Obtener mesas del puesto
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo,
            puesto_codigo=puesto.puesto_codigo,
            activo=True
        ).all()
        
        mesa_ids = [m.id for m in mesas]
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).all() if mesa_ids else []
        
        formularios_data = []
        for formulario in formularios:
            mesa = Location.query.get(formulario.mesa_id)
            testigo = User.query.get(formulario.testigo_id)
            
            formularios_data.append({
                'id': formulario.id,
                'mesa_id': formulario.mesa_id,
                'mesa_nombre': mesa.nombre_completo if mesa else None,
                'testigo_id': formulario.testigo_id,
                'testigo_nombre': testigo.nombre if testigo else None,
                'estado': formulario.estado,
                'created_at': formulario.created_at.isoformat() if formulario.created_at else None,
                'updated_at': formulario.updated_at.isoformat() if formulario.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'data': formularios_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
