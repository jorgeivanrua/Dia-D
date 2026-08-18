"""
Rutas para Coordinador Departamental
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.location import Location
from backend.models.formulario_e14 import FormularioE14
from backend.database import db

bp = Blueprint('coordinador_departamental', __name__, url_prefix='/api/coordinador-departamental')


@bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Estadísticas departamentales"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_departamental':
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
        
        # Obtener ubicaciones del departamento
        municipios = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).count()
        
        puestos = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).count()
        
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).count()
        
        # Obtener formularios del departamento
        mesa_ids = [m.id for m in Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()]
        
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).all() if mesa_ids else []
        
        formularios_completados = sum(1 for f in formularios if f.estado == 'completado')
        
        stats = {
            'total_municipios': municipios,
            'total_puestos': puestos,
            'total_mesas': mesas,
            'total_formularios': len(formularios),
            'formularios_completados': formularios_completados,
            'formularios_pendientes': len(formularios) - formularios_completados,
            'porcentaje_avance': (formularios_completados / len(formularios) * 100) if formularios else 0,
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


@bp.route('/municipios', methods=['GET'])
@jwt_required()
def get_municipios():
    """Obtener municipios del departamento"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_departamental':
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
        
        municipios = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()
        
        municipios_data = []
        for municipio in municipios:
            # Contar puestos y mesas del municipio
            puestos_count = Location.query.filter_by(
                tipo='puesto',
                departamento_codigo=municipio.departamento_codigo,
                municipio_codigo=municipio.municipio_codigo,
                activo=True
            ).count()
            
            mesas_count = Location.query.filter_by(
                tipo='mesa',
                departamento_codigo=municipio.departamento_codigo,
                municipio_codigo=municipio.municipio_codigo,
                activo=True
            ).count()
            
            # Obtener formularios del municipio
            mesa_ids = [m.id for m in Location.query.filter_by(
                tipo='mesa',
                departamento_codigo=municipio.departamento_codigo,
                municipio_codigo=municipio.municipio_codigo,
                activo=True
            ).all()]
            
            formularios = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids)
            ).all() if mesa_ids else []
            
            formularios_completados = sum(1 for f in formularios if f.estado == 'completado')
            
            municipios_data.append({
                'id': municipio.id,
                'nombre': municipio.municipio_nombre,
                'nombre_completo': municipio.nombre_completo,
                'municipio_codigo': municipio.municipio_codigo,
                'total_puestos': puestos_count,
                'total_mesas': mesas_count,
                'total_formularios': len(formularios),
                'formularios_completados': formularios_completados,
                'porcentaje_avance': (formularios_completados / len(formularios) * 100) if formularios else 0
            })
        
        return jsonify({
            'success': True,
            'data': municipios_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/resumen', methods=['GET'])
@jwt_required()
def get_resumen():
    """Resumen de avance departamental"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_departamental':
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
        
        # Obtener resumen por municipio
        municipios = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()
        
        resumen_municipios = []
        total_mesas_depto = 0
        total_formularios_depto = 0
        total_completados_depto = 0
        
        for municipio in municipios:
            mesa_ids = [m.id for m in Location.query.filter_by(
                tipo='mesa',
                departamento_codigo=municipio.departamento_codigo,
                municipio_codigo=municipio.municipio_codigo,
                activo=True
            ).all()]
            
            mesas_count = len(mesa_ids)
            formularios = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids)
            ).all() if mesa_ids else []
            
            formularios_completados = sum(1 for f in formularios if f.estado == 'completado')
            
            total_mesas_depto += mesas_count
            total_formularios_depto += len(formularios)
            total_completados_depto += formularios_completados
            
            resumen_municipios.append({
                'municipio': municipio.municipio_nombre,
                'total_mesas': mesas_count,
                'formularios_completados': formularios_completados,
                'porcentaje_avance': (formularios_completados / mesas_count * 100) if mesas_count > 0 else 0
            })
        
        resumen = {
            'departamento': departamento.nombre_completo,
            'total_municipios': len(municipios),
            'total_mesas': total_mesas_depto,
            'total_formularios': total_formularios_depto,
            'formularios_completados': total_completados_depto,
            'porcentaje_avance_general': (total_completados_depto / total_mesas_depto * 100) if total_mesas_depto > 0 else 0,
            'resumen_por_municipio': resumen_municipios
        }
        
        return jsonify({
            'success': True,
            'data': resumen
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/consolidado', methods=['GET'])
@jwt_required()
def get_consolidado():
    """Obtener consolidado de resultados del departamento"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_departamental':
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
        from collections import defaultdict
        votos_por_partido = defaultdict(int)
        
        for formulario in formularios:
            if formulario.votos_partidos:
                for voto in formulario.votos_partidos:
                    votos_por_partido[voto.partido_id] += voto.votos
        
        # Obtener información de partidos
        from backend.models.partido_politico import PartidoPolitico as Partido
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
        consolidado['resumen'] = {
            'total_votos': consolidado['total_votos'],
            'participacion_porcentaje': consolidado['porcentaje_participacion']
        }
        
        return jsonify({
            'success': True,
            'data': consolidado
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/estadisticas', methods=['GET'])
@jwt_required()
def get_estadisticas():
    """Obtener estadísticas detalladas del departamento"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_departamental':
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
        
        # Obtener todas las mesas del departamento
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()
        
        mesa_ids = [m.id for m in mesas]
        
        # Obtener formularios
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).all() if mesa_ids else []
        
        # Estadísticas por estado
        estados = {
            'pendiente': 0,
            'validado': 0,
            'rechazado': 0,
            'sin_reporte': len(mesas) - len(formularios)
        }
        
        for formulario in formularios:
            if formulario.estado in estados:
                estados[formulario.estado] += 1
        
        # Estadísticas por municipio
        municipios = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()
        
        stats_municipios = []
        for municipio in municipios:
            mesas_municipio = [m for m in mesas if m.municipio_codigo == municipio.municipio_codigo]
            mesa_ids_municipio = [m.id for m in mesas_municipio]
            
            formularios_municipio = [f for f in formularios if f.mesa_id in mesa_ids_municipio]
            validados = sum(1 for f in formularios_municipio if f.estado == 'validado')
            
            stats_municipios.append({
                'municipio': municipio.municipio_nombre,
                'total_mesas': len(mesas_municipio),
                'formularios_recibidos': len(formularios_municipio),
                'formularios_validados': validados,
                'porcentaje_avance': round((validados / len(mesas_municipio) * 100), 2) if mesas_municipio else 0
            })
        
        estadisticas = {
            'total_mesas': len(mesas),
            'total_formularios': len(formularios),
            'estados': estados,
            'porcentaje_completado': round((len(formularios) / len(mesas) * 100), 2) if mesas else 0,
            'porcentaje_validado': round((estados['validado'] / len(mesas) * 100), 2) if mesas else 0,
            'estadisticas_por_municipio': stats_municipios
        }
        
        return jsonify({
            'success': True,
            'data': estadisticas
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/exportar', methods=['GET'])
@jwt_required()
def exportar():
    """
    Exportar datos consolidados del departamento en formato CSV

    Query params:
        formato: Formato de exportación (csv, excel, pdf -> todos generan CSV)
    """
    try:
        import csv
        import io

        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))

        if not user or user.rol != 'coordinador_departamental':
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

        # Reutilizar el consolidado del departamento
        mesa_ids = [m.id for m in Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()]

        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids),
            FormularioE14.estado == 'validado'
        ).all() if mesa_ids else []

        # Consolidar votos por partido
        from collections import defaultdict
        from backend.models.partido_politico import PartidoPolitico as Partido

        votos_por_partido = defaultdict(int)
        for formulario in formularios:
            if formulario.votos_partidos:
                for voto in formulario.votos_partidos:
                    votos_por_partido[voto.partido_id] += voto.votos

        partidos_data = []
        total_votos_partidos = sum(votos_por_partido.values())
        for partido_id, votos in votos_por_partido.items():
            partido = Partido.query.get(partido_id)
            if partido:
                porcentaje = (votos / total_votos_partidos * 100) if total_votos_partidos > 0 else 0
                partidos_data.append({
                    'partido_nombre': partido.nombre,
                    'total_votos': votos,
                    'porcentaje': round(porcentaje, 2)
                })
        partidos_data.sort(key=lambda x: x['total_votos'], reverse=True)

        total_votos = sum(f.total_votos_candidatos or 0 for f in formularios)
        total_votantes = sum(f.votantes_registrados or 0 for f in formularios)

        # Generar CSV
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(['Departamento', departamento.nombre_completo])
        writer.writerow(['Código', departamento.departamento_codigo])
        writer.writerow(['Fecha de Generación', ''])
        writer.writerow(['Coordinador', user.nombre])
        writer.writerow([])
        writer.writerow(['RESUMEN DE VOTACIÓN'])
        writer.writerow(['Total Votantes Registrados', total_votantes])
        writer.writerow(['Total Votos', total_votos])
        writer.writerow(['Participación %', round((total_votos / total_votantes * 100), 2) if total_votantes else 0])
        writer.writerow([])
        writer.writerow(['VOTOS POR PARTIDO'])
        writer.writerow(['Partido', 'Votos', 'Porcentaje'])
        for vp in partidos_data:
            writer.writerow([vp['partido_nombre'], vp['total_votos'], f"{vp['porcentaje']:.2f}%"])

        csv_data = output.getvalue()

        from flask import Response
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=consolidado_departamental.csv'}
        ), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/generar-e24', methods=['POST'])
@jwt_required()
def generar_e24():
    """Generar formulario E-24 consolidado del departamento"""
    try:
        from flask import send_file
        import io
        from datetime import datetime
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from backend.models.formulario_e14 import VotoPartido
        from backend.models.configuracion_electoral import TipoEleccion
        from backend.models.partido_politico import PartidoPolitico as Partido

        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))

        if not user or user.rol != 'coordinador_departamental':
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

        # Obtener todas las mesas del departamento
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()

        mesa_ids = [mesa.id for mesa in mesas]

        # Obtener formularios validados del departamento
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids),
            FormularioE14.estado == 'validado'
        ).all() if mesa_ids else []

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

            votos_partidos = VotoPartido.query.filter_by(formulario_id=formulario.id).all()
            for voto in votos_partidos:
                partido = Partido.query.get(voto.partido_id)
                if partido:
                    partido_nombre = partido.nombre
                    if partido_nombre not in consolidado_por_tipo[tipo_id]['votos_por_partido']:
                        consolidado_por_tipo[tipo_id]['votos_por_partido'][partido_nombre] = 0
                    consolidado_por_tipo[tipo_id]['votos_por_partido'][partido_nombre] += voto.votos

        # Crear PDF E-24 Departamental
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), topMargin=0.5*inch, bottomMargin=0.5*inch)

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

        story = []

        title = Paragraph("FORMULARIO E-24", title_style)
        story.append(title)

        subtitle = Paragraph("CONSOLIDADO DE RESULTADOS - NIVEL DEPARTAMENTAL", subtitle_style)
        story.append(subtitle)

        codigo_e24 = f"E24-DEPARTAMENTAL-{departamento.departamento_codigo}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        codigo_para = Paragraph(f"<b>Código:</b> {codigo_e24}", styles['Normal'])
        story.append(codigo_para)
        story.append(Spacer(1, 20))

        info_data = [
            ['DEPARTAMENTO:', f"{departamento.departamento_codigo} - {departamento.nombre_completo}"],
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
            ['Coordinador Departamental', 'Auditor Electoral'],
            [user.nombre, '']
        ]

        firmas_table = Table(firmas_data, colWidths=[3*inch, 3*inch])
        firmas_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 10),
        ]))

        story.append(firmas_table)

        doc.build(story)
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'E24_Departamental_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al generar E-24: {str(e)}'
        }), 500
