"""
Rutas para configuración del sistema
"""
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required
from backend.services.configuracion_service import ConfiguracionService
from backend.utils.decorators import role_required
import json
import io

configuracion_sistema_bp = Blueprint('configuracion_sistema', __name__, url_prefix='/api/configuracion')


@configuracion_sistema_bp.route('', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def obtener_configuraciones():
    """
    Obtener todas las configuraciones del sistema
    """
    try:
        configuraciones = ConfiguracionService.obtener_todas_configuraciones()
        
        return jsonify({
            'success': True,
            'data': configuraciones
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@configuracion_sistema_bp.route('/<clave>', methods=['GET'])
@jwt_required()
def obtener_configuracion(clave):
    """
    Obtener una configuración específica
    """
    try:
        valor = ConfiguracionService.obtener_configuracion(clave)
        
        if valor is None:
            return jsonify({
                'success': False,
                'error': 'Configuración no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'clave': clave,
                'valor': valor
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@configuracion_sistema_bp.route('/<clave>', methods=['PUT'])
@jwt_required()
@role_required(['super_admin'])
def actualizar_configuracion(clave):
    """
    Actualizar una configuración
    Body:
        valor: Nuevo valor
        tipo: Tipo de dato (text, integer, boolean, json)
        descripcion: Descripción (opcional)
    """
    try:
        from flask_jwt_extended import get_jwt_identity
        
        data = request.get_json()
        
        if 'valor' not in data:
            return jsonify({
                'success': False,
                'error': 'El valor es requerido'
            }), 400
        
        user_id = get_jwt_identity()
        
        config, error = ConfiguracionService.actualizar_configuracion(
            clave=clave,
            valor=data['valor'],
            tipo=data.get('tipo', 'text'),
            descripcion=data.get('descripcion'),
            user_id=user_id
        )
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Configuración actualizada exitosamente',
            'data': config
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@configuracion_sistema_bp.route('/exportar', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def exportar_configuracion():
    """
    Exportar configuración
    Body:
        tipo: 'partidos', 'candidatos', 'tipos_eleccion', 'completa'
    """
    try:
        data = request.get_json()
        tipo = data.get('tipo', 'completa')
        
        if tipo == 'partidos':
            resultado = ConfiguracionService.exportar_partidos()
        elif tipo == 'candidatos':
            resultado = ConfiguracionService.exportar_candidatos()
        elif tipo == 'tipos_eleccion':
            resultado = ConfiguracionService.exportar_tipos_eleccion()
        elif tipo == 'completa':
            resultado = ConfiguracionService.exportar_configuracion_completa()
        else:
            return jsonify({
                'success': False,
                'error': f'Tipo de exportación no válido: {tipo}'
            }), 400
        
        # Crear archivo JSON en memoria
        json_str = json.dumps(resultado, indent=2, ensure_ascii=False)
        json_bytes = json_str.encode('utf-8')
        
        # Crear nombre de archivo
        filename = f'configuracion_{tipo}_{resultado["fecha_exportacion"][:10]}.json'
        
        # Retornar como descarga
        return send_file(
            io.BytesIO(json_bytes),
            mimetype='application/json',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@configuracion_sistema_bp.route('/importar', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def importar_configuracion():
    """
    Importar configuración desde archivo JSON
    Form data:
        archivo: Archivo JSON con configuración
    """
    try:
        # Verificar que se envió un archivo
        if 'archivo' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó archivo'
            }), 400
        
        archivo = request.files['archivo']
        
        if archivo.filename == '':
            return jsonify({
                'success': False,
                'error': 'No se seleccionó archivo'
            }), 400
        
        # Validar extensión
        if not archivo.filename.endswith('.json'):
            return jsonify({
                'success': False,
                'error': 'El archivo debe ser JSON'
            }), 400
        
        # Leer y parsear JSON
        try:
            contenido = archivo.read().decode('utf-8')
            data = json.loads(contenido)
        except json.JSONDecodeError as e:
            return jsonify({
                'success': False,
                'error': f'Error al parsear JSON: {str(e)}'
            }), 400
        
        # Importar
        resumen, error = ConfiguracionService.importar_configuracion(data)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Configuración importada exitosamente',
            'data': resumen
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
