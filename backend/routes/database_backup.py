"""
Rutas para backup y restauración de base de datos
Solo accesible para Super Admin
"""
from flask import Blueprint, request, jsonify, send_file, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.database import db
from backend.models.location import Location
from backend.models.formulario_e14 import FormularioE14, VotoPartido
from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral, EvidenciaFotografica
from datetime import datetime
import json
import os
import tempfile
import traceback

database_backup_bp = Blueprint('database_backup', __name__)


def serialize_datetime(obj):
    """Serializar objetos datetime a string"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


def role_required(roles):
    """Decorador para verificar roles"""
    def decorator(f):
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id))
            if not user or user.rol not in roles:
                return jsonify({
                    'success': False,
                    'error': 'No autorizado'
                }), 403
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator


@database_backup_bp.route('/export', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def export_database():
    """Exportar toda la base de datos a JSON"""
    try:
        # Exportar usuarios (sin contraseñas)
        users = User.query.all()
        users_data = [{
            'id': u.id,
            'nombre': u.nombre,
            'rol': u.rol,
            'ubicacion_id': u.ubicacion_id,
            'activo': u.activo,
            'es_usuario_basico': u.es_usuario_basico,
            'presencia_verificada': u.presencia_verificada,
            'presencia_verificada_at': serialize_datetime(u.presencia_verificada_at),
            'ultimo_acceso': serialize_datetime(u.ultimo_acceso),
            'ultima_latitud': u.ultima_latitud,
            'ultima_longitud': u.ultima_longitud,
            'ultima_geolocalizacion_at': serialize_datetime(u.ultima_geolocalizacion_at),
            'precision_geolocalizacion': u.precision_geolocalizacion,
            'created_at': serialize_datetime(u.created_at),
            'updated_at': serialize_datetime(u.updated_at),
        } for u in users]
        
        # Exportar ubicaciones
        locations = Location.query.all()
        locations_data = []
        for l in locations:
            loc_dict = {
                'id': l.id,
                'tipo': l.tipo,
                'departamento_codigo': l.departamento_codigo,
                'municipio_codigo': l.municipio_codigo,
                'zona_codigo': l.zona_codigo,
                'puesto_codigo': l.puesto_codigo,
                'mesa_codigo': l.mesa_codigo,
                'nombre_completo': l.nombre_completo,
                'total_votantes_registrados': l.total_votantes_registrados or 0,
                'mujeres': l.mujeres or 0,
                'hombres': l.hombres or 0,
                'latitud': l.latitud,
                'longitud': l.longitud,
                'activo': l.activo,
            }
            
            # Agregar campos opcionales si existen
            optional_fields = ['departamento_nombre', 'municipio_nombre', 'puesto_nombre', 'mesa_nombre', 'comuna', 'direccion', 'parent_id']
            for field in optional_fields:
                if hasattr(l, field):
                    loc_dict[field] = getattr(l, field)
            
            locations_data.append(loc_dict)
        
        # Exportar formularios
        formularios = FormularioE14.query.all()
        formularios_data = [{
            'id': f.id,
            'mesa_id': f.mesa_id,
            'testigo_id': f.testigo_id,
            'tipo_eleccion_id': getattr(f, 'tipo_eleccion_id', None),
            'total_votantes_registrados': f.total_votantes_registrados,
            'total_votos': f.total_votos,
            'votos_validos': f.votos_validos,
            'votos_nulos': f.votos_nulos,
            'votos_blanco': f.votos_blanco,
            'tarjetas_no_marcadas': f.tarjetas_no_marcadas,
            'total_tarjetas': f.total_tarjetas,
            'estado': f.estado,
            'validado_por_id': getattr(f, 'validado_por_id', None),
            'validado_at': serialize_datetime(getattr(f, 'validado_at', None)),
            'motivo_rechazo': getattr(f, 'motivo_rechazo', None),
            'imagen_url': getattr(f, 'imagen_url', None),
            'observaciones': getattr(f, 'observaciones', None),
            'created_at': serialize_datetime(f.created_at),
            'updated_at': serialize_datetime(f.updated_at),
        } for f in formularios]
        
        # Exportar votos por partido
        votos = VotoPartido.query.all()
        votos_data = [{
            'id': v.id,
            'formulario_id': v.formulario_id,
            'partido_id': v.partido_id,
            'votos': v.votos,
            'created_at': serialize_datetime(v.created_at),
        } for v in votos]
        
        # Exportar incidentes
        incidentes = IncidenteElectoral.query.all()
        incidentes_data = [{
            'id': i.id,
            'titulo': i.titulo,
            'descripcion': i.descripcion,
            'tipo_incidente': i.tipo_incidente,
            'severidad': i.severidad,
            'estado': i.estado,
            'fecha_reporte': serialize_datetime(i.fecha_reporte),
            'ubicacion_gps': i.ubicacion_gps,
            'notas_resolucion': i.notas_resolucion,
            'mesa_id': i.mesa_id,
            'reportado_por_id': i.reportado_por_id,
            'created_at': serialize_datetime(i.created_at),
            'updated_at': serialize_datetime(i.updated_at),
        } for i in incidentes]
        
        # Exportar delitos
        delitos = DelitoElectoral.query.all()
        delitos_data = [{
            'id': d.id,
            'titulo': d.titulo,
            'descripcion': d.descripcion,
            'tipo_delito': d.tipo_delito,
            'gravedad': d.gravedad,
            'estado': d.estado,
            'fecha_reporte': serialize_datetime(d.fecha_reporte),
            'ubicacion_gps': d.ubicacion_gps,
            'testigos_adicionales': d.testigos_adicionales,
            'denunciado_formalmente': d.denunciado_formalmente,
            'numero_denuncia': d.numero_denuncia,
            'resultado_investigacion': d.resultado_investigacion,
            'mesa_id': d.mesa_id,
            'reportado_por_id': d.reportado_por_id,
            'created_at': serialize_datetime(d.created_at),
            'updated_at': serialize_datetime(d.updated_at),
        } for d in delitos]
        
        # Exportar evidencias
        evidencias = EvidenciaFotografica.query.all()
        evidencias_data = [{
            'id': e.id,
            'filename': e.filename,
            'url': e.url,
            'tipo': e.tipo,
            'descripcion': e.descripcion,
            'incidente_id': e.incidente_id,
            'delito_id': e.delito_id,
            'created_at': serialize_datetime(e.created_at),
        } for e in evidencias]
        
        # Crear archivo JSON
        data = {
            'export_date': datetime.now().isoformat(),
            'database': 'Export from application',
            'stats': {
                'users': len(users_data),
                'locations': len(locations_data),
                'formularios': len(formularios_data),
                'votos_partidos': len(votos_data),
                'incidentes': len(incidentes_data),
                'delitos': len(delitos_data),
                'evidencias': len(evidencias_data),
            },
            'users': users_data,
            'locations': locations_data,
            'formularios': formularios_data,
            'votos_partidos': votos_data,
            'incidentes': incidentes_data,
            'delitos': delitos_data,
            'evidencias': evidencias_data,
        }
        
        # Guardar en archivo temporal
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', encoding='utf-8')
        json.dump(data, temp_file, indent=2, ensure_ascii=False)
        temp_file.close()
        
        # Enviar archivo
        filename = f'database_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=filename,
            mimetype='application/json'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@database_backup_bp.route('/import', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def import_database():
    """Importar base de datos desde JSON"""
    try:
        # Verificar que se envió un archivo
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se envió ningún archivo'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nombre de archivo vacío'
            }), 400
        
        # Leer y parsear JSON
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            return jsonify({
                'success': False,
                'error': f'Error al parsear JSON: {str(e)}'
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error al leer archivo: {str(e)}'
            }), 400
        
        stats = {
            'users_imported': 0,
            'locations_imported': 0,
            'formularios_imported': 0,
            'votos_imported': 0,
            'incidentes_imported': 0,
            'delitos_imported': 0,
            'evidencias_imported': 0,
        }
        
        # Importar ubicaciones primero (sin dependencias)
        for loc_data in data.get('locations', []):
            # Verificar si ya existe por código completo
            existing = None
            if loc_data.get('mesa_codigo'):
                existing = Location.query.filter_by(
                    departamento_codigo=loc_data.get('departamento_codigo'),
                    municipio_codigo=loc_data.get('municipio_codigo'),
                    puesto_codigo=loc_data.get('puesto_codigo'),
                    mesa_codigo=loc_data.get('mesa_codigo')
                ).first()
            elif loc_data.get('puesto_codigo'):
                existing = Location.query.filter_by(
                    departamento_codigo=loc_data.get('departamento_codigo'),
                    municipio_codigo=loc_data.get('municipio_codigo'),
                    puesto_codigo=loc_data.get('puesto_codigo'),
                    mesa_codigo=None
                ).first()
            elif loc_data.get('municipio_codigo'):
                existing = Location.query.filter_by(
                    departamento_codigo=loc_data.get('departamento_codigo'),
                    municipio_codigo=loc_data.get('municipio_codigo'),
                    puesto_codigo=None,
                    mesa_codigo=None
                ).first()
            else:
                existing = Location.query.filter_by(
                    departamento_codigo=loc_data.get('departamento_codigo'),
                    municipio_codigo=None,
                    puesto_codigo=None,
                    mesa_codigo=None
                ).first()
            
            if not existing:
                # Preparar datos con valores por defecto para campos requeridos
                location_data = {
                    'tipo': loc_data['tipo'],
                    'departamento_codigo': loc_data.get('departamento_codigo'),
                    'municipio_codigo': loc_data.get('municipio_codigo'),
                    'zona_codigo': loc_data.get('zona_codigo'),
                    'puesto_codigo': loc_data.get('puesto_codigo'),
                    'mesa_codigo': loc_data.get('mesa_codigo'),
                    'nombre_completo': loc_data.get('nombre_completo', ''),
                    'total_votantes_registrados': loc_data.get('total_votantes_registrados', 0),
                    'mujeres': loc_data.get('mujeres', 0),
                    'hombres': loc_data.get('hombres', 0),
                    'latitud': loc_data.get('latitud'),
                    'longitud': loc_data.get('longitud'),
                    'activo': loc_data.get('activo', True),
                }
                
                # Agregar campos opcionales solo si existen en el modelo
                optional_fields = ['departamento_nombre', 'municipio_nombre', 'puesto_nombre', 'mesa_nombre', 'comuna', 'direccion', 'parent_id']
                for field in optional_fields:
                    if field in loc_data and loc_data[field] is not None:
                        location_data[field] = loc_data[field]
                
                location = Location(**location_data)
                db.session.add(location)
                stats['locations_imported'] += 1
        
        db.session.commit()
        
        # Importar usuarios (PROTEGER USUARIOS BÁSICOS DEL SISTEMA)
        for user_data in data.get('users', []):
            try:
                # Verificar si ya existe un usuario con el mismo nombre y rol
                existing = User.query.filter_by(
                    nombre=user_data['nombre'],
                    rol=user_data['rol']
                ).first()
                
                # NO importar si:
                # 1. Ya existe un usuario con ese nombre y rol
                # 2. El usuario existente es un usuario básico del sistema
                if existing:
                    if existing.es_usuario_basico:
                        print(f"⚠️  Omitiendo usuario básico del sistema: {user_data['nombre']} ({user_data['rol']})")
                        continue
                    else:
                        # Actualizar usuario existente que NO es básico
                        existing.ubicacion_id = user_data.get('ubicacion_id')
                        existing.activo = user_data.get('activo', True)
                        existing.presencia_verificada = user_data.get('presencia_verificada', False)
                        stats['users_imported'] += 1
                        continue
                
                # Crear nuevo usuario solo si no existe
                user = User(
                    nombre=user_data['nombre'],
                    rol=user_data['rol'],
                    ubicacion_id=user_data.get('ubicacion_id'),
                    activo=user_data.get('activo', True),
                    es_usuario_basico=user_data.get('es_usuario_basico', False),
                    presencia_verificada=user_data.get('presencia_verificada', False),
                )
                user.set_password('test123')  # Contraseña temporal
                db.session.add(user)
                stats['users_imported'] += 1
            except Exception as e:
                print(f"Error importando usuario {user_data.get('nombre')}: {str(e)}")
                continue
        
        db.session.commit()
        
        # Importar formularios
        for form_data in data.get('formularios', []):
            try:
                existing = FormularioE14.query.get(form_data['id'])
                if not existing:
                    formulario = FormularioE14(
                        mesa_id=form_data['mesa_id'],
                        testigo_id=form_data['testigo_id'],
                        total_votantes_registrados=form_data['total_votantes_registrados'],
                        total_votos=form_data['total_votos'],
                        votos_validos=form_data['votos_validos'],
                        votos_nulos=form_data['votos_nulos'],
                        votos_blanco=form_data['votos_blanco'],
                        tarjetas_no_marcadas=form_data['tarjetas_no_marcadas'],
                        total_tarjetas=form_data['total_tarjetas'],
                        estado=form_data['estado'],
                    )
                    db.session.add(formulario)
                    stats['formularios_imported'] += 1
            except Exception as e:
                print(f"Error importando formulario {form_data.get('id')}: {str(e)}")
                continue
        
        db.session.commit()
        
        # Importar votos por partido
        for voto_data in data.get('votos_partidos', []):
            try:
                voto = VotoPartido(
                    formulario_id=voto_data['formulario_id'],
                    partido_id=voto_data['partido_id'],
                    votos=voto_data['votos'],
                )
                db.session.add(voto)
                stats['votos_imported'] += 1
            except Exception as e:
                print(f"Error importando voto: {str(e)}")
                continue
        
        db.session.commit()
        
        # Importar incidentes
        for inc_data in data.get('incidentes', []):
            try:
                incidente = IncidenteElectoral(
                    titulo=inc_data['titulo'],
                    descripcion=inc_data['descripcion'],
                    tipo_incidente=inc_data['tipo_incidente'],
                    severidad=inc_data['severidad'],
                    estado=inc_data['estado'],
                    mesa_id=inc_data.get('mesa_id'),
                    reportado_por_id=inc_data.get('reportado_por_id'),
                )
                db.session.add(incidente)
                stats['incidentes_imported'] += 1
            except Exception as e:
                print(f"Error importando incidente: {str(e)}")
                continue
        
        db.session.commit()
        
        # Importar delitos
        for del_data in data.get('delitos', []):
            try:
                delito = DelitoElectoral(
                    titulo=del_data['titulo'],
                    descripcion=del_data['descripcion'],
                    tipo_delito=del_data['tipo_delito'],
                    gravedad=del_data['gravedad'],
                    estado=del_data['estado'],
                    mesa_id=del_data.get('mesa_id'),
                    reportado_por_id=del_data.get('reportado_por_id'),
                )
                db.session.add(delito)
                stats['delitos_imported'] += 1
            except Exception as e:
                print(f"Error importando delito: {str(e)}")
                continue
        
        db.session.commit()
        
        # Importar evidencias
        for ev_data in data.get('evidencias', []):
            try:
                evidencia = EvidenciaFotografica(
                    filename=ev_data['filename'],
                    url=ev_data['url'],
                    tipo=ev_data['tipo'],
                    incidente_id=ev_data.get('incidente_id'),
                    delito_id=ev_data.get('delito_id'),
                )
                db.session.add(evidencia)
                stats['evidencias_imported'] += 1
            except Exception as e:
                print(f"Error importando evidencia: {str(e)}")
                continue
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Base de datos importada exitosamente',
            'stats': stats
        }), 200
        
    except Exception as e:
        db.session.rollback()
        error_trace = traceback.format_exc()
        current_app.logger.error(f"Error en importación: {error_trace}")
        return jsonify({
            'success': False,
            'error': str(e),
            'trace': error_trace if current_app.debug else None
        }), 500


@database_backup_bp.route('/stats', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_database_stats():
    """Obtener estadísticas de la base de datos"""
    try:
        stats = {
            'users': User.query.count(),
            'locations': Location.query.count(),
            'formularios': FormularioE14.query.count(),
            'votos_partidos': VotoPartido.query.count(),
            'incidentes': IncidenteElectoral.query.count(),
            'delitos': DelitoElectoral.query.count(),
            'evidencias': EvidenciaFotografica.query.count(),
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
