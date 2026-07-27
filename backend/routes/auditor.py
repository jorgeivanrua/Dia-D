"""
Rutas para Auditor Electoral
"""
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.location import Location
from backend.models.formulario_e14 import FormularioE14
from backend.models.partido_politico import PartidoPolitico as Partido
from backend.database import db
from backend.utils.decorators import role_required
from backend.utils.exceptions import BaseAPIException, ValidationException, NotFoundException
from collections import defaultdict
import csv
import io
from datetime import datetime

auditor_bp = Blueprint('auditor', __name__, url_prefix='/api/auditor')


@auditor_bp.route('/stats', methods=['GET'])
@jwt_required()
@role_required(['auditor_electoral'])
def get_stats():
    """Estadísticas de auditoría"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        departamento = Location.query.get(user.ubicacion_id)
        
        # Obtener formularios del departamento
        mesa_ids = [m.id for m in Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()]
        
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).all() if mesa_ids else []
        
        # Analizar formularios
        formularios_completados = sum(1 for f in formularios if f.estado == 'completado')
        formularios_pendientes = sum(1 for f in formularios if f.estado == 'pendiente')
        formularios_en_revision = sum(1 for f in formularios if f.estado == 'en_revision')
        
        # TODO: Implementar detección de inconsistencias
        inconsistencias_detectadas = 0
        
        stats = {
            'total_formularios': len(formularios),
            'formularios_completados': formularios_completados,
            'formularios_pendientes': formularios_pendientes,
            'formularios_en_revision': formularios_en_revision,
            'inconsistencias_detectadas': inconsistencias_detectadas,
            'porcentaje_auditado': (formularios_completados / len(formularios) * 100) if formularios else 0,
            'departamento': {
                'id': departamento.id,
                'nombre': departamento.nombre_completo,
                'codigo': departamento.departamento_codigo
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


@auditor_bp.route('/inconsistencias', methods=['GET'])
@jwt_required()
def get_inconsistencias():
    """Obtener inconsistencias detectadas"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'auditor_electoral':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        # TODO: Implementar lógica de detección de inconsistencias
        # Por ahora retornamos lista vacía
        inconsistencias_data = []
        
        return jsonify({
            'success': True,
            'data': inconsistencias_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auditor_bp.route('/reportes', methods=['GET'])
@jwt_required()
def get_reportes():
    """Obtener reportes de auditoría"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'auditor_electoral':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        departamento = Location.query.get(user.ubicacion_id)
        
        # Obtener formularios del departamento
        mesa_ids = [m.id for m in Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()]
        
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).order_by(FormularioE14.updated_at.desc()).limit(100).all() if mesa_ids else []
        
        reportes_data = []
        for formulario in formularios:
            mesa = Location.query.get(formulario.mesa_id)
            testigo = User.query.get(formulario.testigo_id)
            
            reportes_data.append({
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
            'data': reportes_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auditor_bp.route('/formularios', methods=['GET'])
@jwt_required()
def get_formularios():
    """Obtener formularios para auditar"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'auditor_electoral':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        departamento = Location.query.get(user.ubicacion_id)
        
        # Filtrar por estado si se proporciona
        estado = request.args.get('estado')
        
        # Obtener formularios del departamento
        mesa_ids = [m.id for m in Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()]
        
        query = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ) if mesa_ids else FormularioE14.query.filter(False)
        
        if estado:
            query = query.filter_by(estado=estado)
        
        formularios = query.order_by(FormularioE14.updated_at.desc()).all()
        
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


@auditor_bp.route('/consolidado', methods=['GET'])
@jwt_required()
@role_required(['auditor_electoral'])
def get_consolidado():
    """Obtener consolidado departamental para auditoría"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        departamento = Location.query.get(user.ubicacion_id)
        
        # Obtener todos los formularios validados del departamento
        mesa_ids = [m.id for m in Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()]
        
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids),
            FormularioE14.estado == 'validado'
        ).all() if mesa_ids else []
        
        # Consolidar resultados
        consolidado = {
            'total_formularios': len(formularios),
            'total_votos': sum(f.total_votos_candidatos or 0 for f in formularios),
            'total_votantes_registrados': sum(f.votantes_registrados or 0 for f in formularios),
            'votos_validos': sum(f.votos_validos or 0 for f in formularios),
            'votos_nulos': sum(f.votos_nulos or 0 for f in formularios),
            'votos_blanco': sum(f.votos_blanco or 0 for f in formularios),
            'porcentaje_participacion': 0
        }
        
        if consolidado['total_votantes_registrados'] > 0:
            consolidado['porcentaje_participacion'] = round(
                (consolidado['total_votos'] / consolidado['total_votantes_registrados']) * 100, 2
            )
        
        # Consolidar votos por partido
        votos_por_partido = defaultdict(int)
        
        for formulario in formularios:
            if formulario.votos_partidos:
                for voto in formulario.votos_partidos:
                    votos_por_partido[voto.partido_id] += voto.votos
        
        # Obtener información de partidos
        partidos_data = []
        total_votos_partidos = sum(votos_por_partido.values())
        
        for partido_id, votos in votos_por_partido.items():
            partido = Partido.query.get(partido_id)
            if partido:
                porcentaje = (votos / total_votos_partidos * 100) if total_votos_partidos > 0 else 0
                partidos_data.append({
                    'partido_id': partido.id,
                    'partido_nombre': partido.nombre,
                    'partido_nombre_corto': partido.nombre_corto,
                    'partido_color': partido.color,
                    'total_votos': votos,
                    'porcentaje': round(porcentaje, 2)
                })
        
        # Ordenar por votos descendente
        partidos_data.sort(key=lambda x: x['total_votos'], reverse=True)
        
        consolidado['votos_por_partido'] = partidos_data
        
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


@auditor_bp.route('/discrepancias', methods=['GET'])
@jwt_required()
@role_required(['auditor_electoral'])
def get_discrepancias():
    """Obtener discrepancias detectadas en formularios"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        departamento = Location.query.get(user.ubicacion_id)
        
        # Obtener formularios del departamento
        mesa_ids = [m.id for m in Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()]
        
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).all() if mesa_ids else []
        
        discrepancias = []
        
        for formulario in formularios:
            # Verificar coherencia de datos
            if formulario.validaciones:
                validaciones = formulario.validaciones
                
                # Discrepancia en votos válidos
                if not validaciones.get('coincide_votos_validos'):
                    mesa = Location.query.get(formulario.mesa_id)
                    discrepancias.append({
                        'formulario_id': formulario.id,
                        'mesa_codigo': mesa.codigo if mesa else 'N/A',
                        'mesa_nombre': mesa.nombre_completo if mesa else 'N/A',
                        'tipo': 'votos_validos',
                        'descripcion': f"Suma de votos por partido ({validaciones.get('total_votos_calculado')}) no coincide con votos válidos ({formulario.votos_validos})",
                        'severidad': 'alta',
                        'estado': formulario.estado
                    })
                
                # Discrepancia en total de votos
                if not validaciones.get('coincide_total_votos'):
                    mesa = Location.query.get(formulario.mesa_id)
                    discrepancias.append({
                        'formulario_id': formulario.id,
                        'mesa_codigo': mesa.codigo if mesa else 'N/A',
                        'mesa_nombre': mesa.nombre_completo if mesa else 'N/A',
                        'tipo': 'total_votos',
                        'descripcion': 'Suma de votos válidos + nulos + blanco no coincide con total de votos',
                        'severidad': 'critica',
                        'estado': formulario.estado
                    })
                
                # Discrepancia en participación
                if validaciones.get('discrepancia_porcentaje', 0) > 10:
                    mesa = Location.query.get(formulario.mesa_id)
                    discrepancias.append({
                        'formulario_id': formulario.id,
                        'mesa_codigo': mesa.codigo if mesa else 'N/A',
                        'mesa_nombre': mesa.nombre_completo if mesa else 'N/A',
                        'tipo': 'participacion',
                        'descripcion': f"Discrepancia del {validaciones.get('discrepancia_porcentaje')}% entre votantes registrados y votos emitidos",
                        'severidad': 'media',
                        'estado': formulario.estado
                    })
        
        return jsonify({
            'success': True,
            'data': discrepancias
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auditor_bp.route('/exportar', methods=['GET'])
@jwt_required()
@role_required(['auditor_electoral'])
def exportar_auditoria():
    """Exportar datos de auditoría"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        departamento = Location.query.get(user.ubicacion_id)
        formato = request.args.get('formato', 'csv')
        
        # Obtener formularios del departamento
        mesa_ids = [m.id for m in Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()]
        
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).all() if mesa_ids else []
        
        if formato == 'csv':
            # Crear CSV
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Encabezados
            writer.writerow([
                'ID Formulario',
                'Mesa Código',
                'Mesa Nombre',
                'Testigo',
                'Estado',
                'Votantes Registrados',
                'Total Votos',
                'Votos Válidos',
                'Votos Nulos',
                'Votos Blanco',
                'Participación %',
                'Fecha Creación',
                'Fecha Actualización'
            ])
            
            # Datos
            for formulario in formularios:
                mesa = Location.query.get(formulario.mesa_id)
                testigo = User.query.get(formulario.testigo_id)
                
                participacion = 0
                if formulario.votantes_registrados and formulario.votantes_registrados > 0:
                    participacion = round((formulario.total_votos_candidatos / formulario.votantes_registrados) * 100, 2)
                
                writer.writerow([
                    formulario.id,
                    mesa.codigo if mesa else 'N/A',
                    mesa.nombre_completo if mesa else 'N/A',
                    testigo.nombre if testigo else 'N/A',
                    formulario.estado,
                    formulario.votantes_registrados or 0,
                    formulario.total_votos_candidatos or 0,
                    formulario.votos_validos or 0,
                    formulario.votos_nulos or 0,
                    formulario.votos_blanco or 0,
                    participacion,
                    formulario.created_at.strftime('%Y-%m-%d %H:%M:%S') if formulario.created_at else '',
                    formulario.updated_at.strftime('%Y-%m-%d %H:%M:%S') if formulario.updated_at else ''
                ])
            
            # Preparar respuesta
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8')),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'auditoria_{departamento.departamento_codigo}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            )
        
        else:
            raise ValidationException('Formato no soportado')
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auditor_bp.route('/municipios', methods=['GET'])
@jwt_required()
@role_required(['auditor_electoral'])
def get_municipios():
    """Obtener estadísticas por municipio"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        departamento = Location.query.get(user.ubicacion_id)
        
        # Obtener municipios del departamento
        municipios = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()
        
        municipios_data = []
        
        for municipio in municipios:
            # Obtener mesas del municipio
            mesas = Location.query.filter_by(
                tipo='mesa',
                departamento_codigo=municipio.departamento_codigo,
                municipio_codigo=municipio.municipio_codigo,
                activo=True
            ).all()
            
            mesa_ids = [m.id for m in mesas]
            
            # Obtener formularios
            formularios = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids)
            ).all() if mesa_ids else []
            
            validados = sum(1 for f in formularios if f.estado == 'validado')
            pendientes = sum(1 for f in formularios if f.estado == 'pendiente')
            rechazados = sum(1 for f in formularios if f.estado == 'rechazado')
            
            municipios_data.append({
                'id': municipio.id,
                'nombre': municipio.municipio_nombre,
                'codigo': municipio.municipio_codigo,
                'total_mesas': len(mesas),
                'total_formularios': len(formularios),
                'formularios_validados': validados,
                'formularios_pendientes': pendientes,
                'formularios_rechazados': rechazados,
                'porcentaje_avance': round((validados / len(mesas) * 100), 2) if mesas else 0
            })
        
        return jsonify({
            'success': True,
            'data': municipios_data
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
