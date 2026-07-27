"""
Rutas para importación de datos administrativos
Permite al admin cargar logos, partidos, candidatos, etc.
"""
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from backend.models.user import User
from backend.models.configuracion_electoral import TipoEleccion
from backend.models.partido_politico import PartidoPolitico as Partido
from backend.models.candidato import Candidato
from backend.utils.decorators import role_required
from backend.database import db
import os
import csv
import io
from datetime import datetime

admin_import_bp = Blueprint('admin_import', __name__, url_prefix='/api/admin/import')

# Configuración de uploads
UPLOAD_FOLDER = 'frontend/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_folder():
    """Asegurar que existan las carpetas de upload"""
    folders = [
        UPLOAD_FOLDER,
        os.path.join(UPLOAD_FOLDER, 'logos_partidos'),
        os.path.join(UPLOAD_FOLDER, 'fotos_candidatos')
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)


# ============================================
# IMPORTACIÓN DE PARTIDOS
# ============================================

@admin_import_bp.route('/partidos/template', methods=['GET'])
@jwt_required()
@role_required(['super_admin', 'admin'])
def descargar_template_partidos():
    """
    Descargar plantilla CSV para importar partidos
    """
    try:
        # Crear CSV template
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Encabezados
        writer.writerow([
            'codigo',
            'nombre',
            'sigla',
            'color_hex',
            'activo',
            'tipo_eleccion_codigo',
            'ambito_territorial'
        ])
        
        # Ejemplos
        writer.writerow([
            'PART001',
            'Partido Liberal',
            'PL',
            '#FF0000',
            'SI',
            'PRES',
            'nacional'
        ])
        writer.writerow([
            'PART002',
            'Partido Conservador',
            'PC',
            '#0000FF',
            'SI',
            'PRES',
            'nacional'
        ])
        writer.writerow([
            'PART003',
            'Movimiento Regional',
            'MR',
            '#00FF00',
            'SI',
            'CONC_MUN',
            'municipal:florencia'
        ])
        
        output.seek(0)
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'template_partidos_{datetime.now().strftime("%Y%m%d")}.csv'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error generando template: {str(e)}'
        }), 500


@admin_import_bp.route('/partidos', methods=['POST'])
@jwt_required()
@role_required(['super_admin', 'admin'])
def importar_partidos():
    """
    Importar partidos desde archivo CSV
    """
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se encontró archivo'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No se seleccionó archivo'
            }), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({
                'success': False,
                'error': 'Solo se permiten archivos CSV'
            }), 400
        
        # Leer CSV
        stream = io.StringIO(file.stream.read().decode("UTF-8"), newline=None)
        csv_reader = csv.DictReader(stream)
        
        partidos_creados = 0
        partidos_actualizados = 0
        errores = []
        
        for row_num, row in enumerate(csv_reader, start=2):
            try:
                codigo = row.get('codigo', '').strip()
                nombre = row.get('nombre', '').strip()
                sigla = row.get('sigla', '').strip()
                color_hex = row.get('color_hex', '#000000').strip()
                activo = row.get('activo', 'SI').strip().upper() == 'SI'
                tipo_eleccion_codigo = row.get('tipo_eleccion_codigo', '').strip()
                ambito_territorial = row.get('ambito_territorial', 'nacional').strip()
                
                if not codigo or not nombre:
                    errores.append(f"Fila {row_num}: Código y nombre son obligatorios")
                    continue
                
                # Buscar tipo de elección
                tipo_eleccion = None
                if tipo_eleccion_codigo:
                    tipo_eleccion = TipoEleccion.query.filter_by(codigo=tipo_eleccion_codigo).first()
                
                # Buscar o crear partido
                partido = Partido.query.filter_by(codigo=codigo).first()
                
                if partido:
                    # Actualizar
                    partido.nombre = nombre
                    partido.sigla = sigla
                    partido.color_hex = color_hex
                    partido.activo = activo
                    partido.tipo_eleccion_id = tipo_eleccion.id if tipo_eleccion else None
                    partido.ambito_territorial = ambito_territorial
                    partidos_actualizados += 1
                else:
                    # Crear nuevo
                    partido = Partido(
                        codigo=codigo,
                        nombre=nombre,
                        sigla=sigla,
                        color_hex=color_hex,
                        activo=activo,
                        tipo_eleccion_id=tipo_eleccion.id if tipo_eleccion else None,
                        ambito_territorial=ambito_territorial
                    )
                    db.session.add(partido)
                    partidos_creados += 1
                
            except Exception as e:
                errores.append(f"Fila {row_num}: {str(e)}")
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'creados': partidos_creados,
                'actualizados': partidos_actualizados,
                'errores': errores
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error importando partidos: {str(e)}'
        }), 500


# ============================================
# IMPORTACIÓN DE CANDIDATOS
# ============================================

@admin_import_bp.route('/candidatos/template', methods=['GET'])
@jwt_required()
@role_required(['super_admin', 'admin'])
def descargar_template_candidatos():
    """
    Descargar plantilla CSV para importar candidatos
    """
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Encabezados
        writer.writerow([
            'codigo',
            'nombre',
            'partido_codigo',
            'tipo_eleccion_codigo',
            'numero_lista',
            'ambito_territorial',
            'departamento_codigo',
            'municipio_codigo',
            'activo'
        ])
        
        # Ejemplos
        writer.writerow([
            'CAND001',
            'Juan Pérez',
            'PART001',
            'PRES',
            '1',
            'nacional',
            '',
            '',
            'SI'
        ])
        writer.writerow([
            'CAND002',
            'María García',
            'PART002',
            'CONC_MUN',
            '5',
            'municipal',
            '18',
            '001',
            'SI'
        ])
        
        output.seek(0)
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'template_candidatos_{datetime.now().strftime("%Y%m%d")}.csv'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error generando template: {str(e)}'
        }), 500


@admin_import_bp.route('/candidatos', methods=['POST'])
@jwt_required()
@role_required(['super_admin', 'admin'])
def importar_candidatos():
    """
    Importar candidatos desde archivo CSV
    """
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se encontró archivo'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No se seleccionó archivo'
            }), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({
                'success': False,
                'error': 'Solo se permiten archivos CSV'
            }), 400
        
        # Leer CSV
        stream = io.StringIO(file.stream.read().decode("UTF-8"), newline=None)
        csv_reader = csv.DictReader(stream)
        
        candidatos_creados = 0
        candidatos_actualizados = 0
        errores = []
        
        for row_num, row in enumerate(csv_reader, start=2):
            try:
                codigo = row.get('codigo', '').strip()
                nombre = row.get('nombre', '').strip()
                partido_codigo = row.get('partido_codigo', '').strip()
                tipo_eleccion_codigo = row.get('tipo_eleccion_codigo', '').strip()
                numero_lista = row.get('numero_lista', '').strip()
                ambito_territorial = row.get('ambito_territorial', 'nacional').strip()
                departamento_codigo = row.get('departamento_codigo', '').strip()
                municipio_codigo = row.get('municipio_codigo', '').strip()
                activo = row.get('activo', 'SI').strip().upper() == 'SI'
                
                if not codigo or not nombre:
                    errores.append(f"Fila {row_num}: Código y nombre son obligatorios")
                    continue
                
                # Buscar partido
                partido = None
                if partido_codigo:
                    partido = Partido.query.filter_by(codigo=partido_codigo).first()
                    if not partido:
                        errores.append(f"Fila {row_num}: Partido {partido_codigo} no encontrado")
                        continue
                
                # Buscar tipo de elección
                tipo_eleccion = None
                if tipo_eleccion_codigo:
                    tipo_eleccion = TipoEleccion.query.filter_by(codigo=tipo_eleccion_codigo).first()
                
                # Buscar o crear candidato
                candidato = Candidato.query.filter_by(codigo=codigo).first()
                
                if candidato:
                    # Actualizar
                    candidato.nombre = nombre
                    candidato.partido_id = partido.id if partido else None
                    candidato.tipo_eleccion_id = tipo_eleccion.id if tipo_eleccion else None
                    candidato.numero_lista = int(numero_lista) if numero_lista else None
                    candidato.ambito_territorial = ambito_territorial
                    candidato.departamento_codigo = departamento_codigo if departamento_codigo else None
                    candidato.municipio_codigo = municipio_codigo if municipio_codigo else None
                    candidato.activo = activo
                    candidatos_actualizados += 1
                else:
                    # Crear nuevo
                    candidato = Candidato(
                        codigo=codigo,
                        nombre=nombre,
                        partido_id=partido.id if partido else None,
                        tipo_eleccion_id=tipo_eleccion.id if tipo_eleccion else None,
                        numero_lista=int(numero_lista) if numero_lista else None,
                        ambito_territorial=ambito_territorial,
                        departamento_codigo=departamento_codigo if departamento_codigo else None,
                        municipio_codigo=municipio_codigo if municipio_codigo else None,
                        activo=activo
                    )
                    db.session.add(candidato)
                    candidatos_creados += 1
                
            except Exception as e:
                errores.append(f"Fila {row_num}: {str(e)}")
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'creados': candidatos_creados,
                'actualizados': candidatos_actualizados,
                'errores': errores
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error importando candidatos: {str(e)}'
        }), 500


# ============================================
# IMPORTACIÓN DE LOGOS
# ============================================

@admin_import_bp.route('/logos/partido/<partido_codigo>', methods=['POST'])
@jwt_required()
@role_required(['super_admin', 'admin'])
def subir_logo_partido(partido_codigo):
    """
    Subir logo de un partido
    """
    try:
        ensure_upload_folder()
        
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se encontró archivo'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No se seleccionó archivo'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Formato de archivo no permitido. Use PNG, JPG o GIF'
            }), 400
        
        # Buscar partido
        partido = Partido.query.filter_by(codigo=partido_codigo).first()
        
        if not partido:
            return jsonify({
                'success': False,
                'error': f'Partido {partido_codigo} no encontrado'
            }), 404
        
        # Guardar archivo
        filename = secure_filename(f"{partido_codigo}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, 'logos_partidos', filename)
        file.save(filepath)
        
        # Actualizar partido
        partido.logo_url = f'/static/uploads/logos_partidos/{filename}'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'partido_codigo': partido_codigo,
                'logo_url': partido.logo_url
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error subiendo logo: {str(e)}'
        }), 500


@admin_import_bp.route('/fotos/candidato/<candidato_codigo>', methods=['POST'])
@jwt_required()
@role_required(['super_admin', 'admin'])
def subir_foto_candidato(candidato_codigo):
    """
    Subir foto de un candidato
    """
    try:
        ensure_upload_folder()
        
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se encontró archivo'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No se seleccionó archivo'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Formato de archivo no permitido. Use PNG, JPG o GIF'
            }), 400
        
        # Buscar candidato
        candidato = Candidato.query.filter_by(codigo=candidato_codigo).first()
        
        if not candidato:
            return jsonify({
                'success': False,
                'error': f'Candidato {candidato_codigo} no encontrado'
            }), 404
        
        # Guardar archivo
        filename = secure_filename(f"{candidato_codigo}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, 'fotos_candidatos', filename)
        file.save(filepath)
        
        # Actualizar candidato
        candidato.foto_url = f'/static/uploads/fotos_candidatos/{filename}'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'candidato_codigo': candidato_codigo,
                'foto_url': candidato.foto_url
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error subiendo foto: {str(e)}'
        }), 500
