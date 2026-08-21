#!/usr/bin/env python
"""Script para reescribir auth.py con estructura correcta."""

import sys

# Contenido completo y corregido de auth.py
# Basado en el patrón de las otras funciones del archivo

content = '''"""
Rutas de autenticación
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from backend.services.auth_service import AuthService
from backend.models.user import User
from backend.utils.jwt_utils import create_token_response
from backend.utils.exceptions import BaseAPIException
from backend.database import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login basado en ubicación jerárquica
    ---
    tags:
      - Autenticación
    summary: Iniciar sesión según rol y ubicación
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [rol, password]
            properties:
              rol:
                type: string
                description: Rol del usuario (super_admin, coordinador_puesto, etc.)
                example: coordinador_puesto
              departamento_codigo:
                type: string
                description: Código de departamento (opcional según rol)
                example: '44'
                municipio_codigo:
                type: string
                description: Código de módulo (opcional según rol)
                example: '4401'
                zona_codigo:
                type: string
                description: Código de zona (opcional según rol)
                example: '440101'
                puesto_codigo:
                type: string
                description: Código de puesto (opcional según rol)
                example: '44010101'
                password:
                type: string
                description: Contraseña del usuario
                example: test123
    responses:
      200:
        description: Login exitoso, retorna tokens y datos del usuario
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                data:
                  type: object
                  properties:
                    access_token:
                      type: string
                    refresh_token:
                      type: string
                    token_type:
                      type: string
                      example: Bearer
                    user:
                      type: object
                      properties:
                        id:
                          type: integer
                        rol:
                          type: string
                    ubicacion:
                      type: object
      400:
        description: Datos incompletos o credenciales inválidas
      401:
        description: Credenciales inválidas
    '''
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        rol = data.get('rol')
        password = data.get('password')
        
        if not rol or not password:
            return jsonify({
                'success': False,
                'error': 'Rol y contraseña son requeridos'
            }), 400
        
        # Construir datos de ubicación
        ubicacion_data = {}
        if 'departamento_codigo' in data:
            ubicacion_data['departamento_codigo'] = data['departamento_codigo']
        if 'municipio_codigo' in data:
            ubicacion_data['municipio_codigo'] = data['municipio_codigo']
        if 'zona_codigo' in data:
            ubicacion_data['zona_codigo'] = data['zona_codigo']
        if 'puesto_codigo' in data:
            ubicacion_data['puesto_codigo'] = data['puesto_codigo']
        
        # Autenticar
        user, access_token, refresh_token = AuthService.authenticate_location_based(
            rol, ubicacion_data, password
        )
        
        return jsonify(create_token_response(user, access_token, refresh_token)), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Cerrar sesión"""
    # Invalidar el token actual añadiendo su JTI a la blacklist
    jti = get_jwt()['jti']
    from backend.utils.jwt_utils import add_to_blacklist
    add_to_blacklist(jti)
    
    return jsonify({
        'success': True,
        'message': 'Sesión cerrada exitosamente'
    }), 200


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """Obtener perfil del usuario actual"""
    try:
        from backend.models.location import Location
        
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Obtener información de ubicación si existe
        ubicacion = None
        if user.ubicacion_id:
            location = Location.query.get(user.ubicacion_id)
            if location:
                ubicacion = location.to_dict()
        
        # ⭐ MEJORA: Agregar contexto específico para testigos
        contexto = None
        if user.rol == 'testigo_electoral' and ubicacion:
            from backend.models.formulario_e14 import FormularioE14
            
            # Obtener puesto (puede ser la ubicación actual o el puesto de la mesa)
            puesto = ubicacion
            if ubicacion['tipo'] == 'mesa':
                puesto_obj = Location.query.filter_by(
                    tipo='puesto',
                    departamento_codigo=ubicacion['departamento_codigo'],
                    municipio_codigo=ubicacion['municipio_codigo'],
                    zona_codigo=ubicacion['zona_codigo'],
                    puesto_codigo=ubicacion['puesto_codigo']
                ).first()
                if puesto_obj:
                    puesto = puesto_obj.to_dict()
            
            # Contar mesas del puesto
            total_mesas = Location.query.filter_by(
                tipo='mesa',
                departamento_codigo=puesto['departamento_codigo'],
                municipio_codigo=puesto['municipio_codigo'],
                zona_codigo=puesto['zona_codigo'],
                puesto_codigo=puesto['puesto_codigo'],
                activo=True
            ).count()
            
            # Contar formularios del testigo
            mis_formularios = FormularioE14.query.filter_by(
                testigo_id=user.id
            ).count()
            
            formularios_validados = FormularioE14.query.filter_by(
                testigo_id=user.id,
                estado='validado'
            ).count()
            
            formularios_pendientes = FormularioE14.query.filter_by(
                testigo_id=user.id,
                estado='pendiente'
            ).count()
            
            formularios_rechazados = FormularioE14.query.filter_by(
                testigo_id=user.id,
                estado='rechazado'
            ).count()
            
            contexto = {
                'puesto': {
                    'nombre': puesto.get('puesto_nombre'),
                    'codigo': puesto.get('puesto_codigo'),
                    'total_mesas': total_mesas
                },
                'mis_formularios': {
                    'total': mis_formularios,
                    'validados': formularios_validados,
                    'pendientes': formularios_pendientes,
                    'rechazados': formularios_rechazados,
                    'porcentaje_completado': round((mis_formularios / total_mesas * 100), 2) if total_mesas > 0 else 0
                },
                'presencia': {
                    'verificada': user.presencia_verificada,
                    'verificada_at': user.presencia_verificada_at.isoformat() if user.presencia_verificada_at else None,
                    'puede_crear_formularios': user.presencia_verificada
                }
            }
        
        return jsonify({
            'success': True,
            'data': {
                'user': {
                    'id': user.id,
                    'nombre': user.nombre,
                    'rol': user.rol,
                    'ubicacion_id': user.ubicacion_id,
                    'activo': user.activo,
                    'ultimo_acceso': user.ultimo_acceso.isoformat() if user.ultimo_acceso else None,
                    'presencia_verificada': user.presencia_verificada if user.rol == 'testigo_electoral' else None,
                    'presencia_verificada_at': user.presencia_verificada_at.isoformat() if user.presencia_verificada_at else None
                },
                'ubicacion': ubicacion,
                'contexto': contexto  # ⭐ NUEVO
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Cambiar contraseña del usuario actual"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({
                'success': False,
                'error': 'Contraseña actual y nueva son requeridas'
            }), 400
        
        AuthService.change_password(int(user_id), current_password, new_password)
        
        return jsonify({
            'success': True,
            'message': 'Contraseña actualizada exitosamente'
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auth_bp.route('/verificar-presencia', methods=['POST'])
@jwt_required()
def verificar_presencia():
    '''Verificar presencia del testigo en la mesa'''
    try:
        from backend.database import db
        from backend.models.location import Location
        
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        if user.rol != 'testigo_electoral':
            return jsonify({
                'success': False,
                'error': 'Solo los testigos pueden verificar presencia'
            }), 403
        
        # Verificar presencia
        user.verificar_presencia()
        db.session.commit()
        
        # Buscar coordinador del puesto para notificar
        coordinador_notificado = False
        if user.ubicacion_id:
            ubicacion = Location.query.get(user.ubicacion_id)
            if ubicacion:
                # Buscar coordinador del puesto
                coordinador = User.query.filter_by(
                    ubicacion_id=ubicacion.id,
                    rol='coordinador_puesto'
                ).first()
                
                if coordinador:
                    # TODO: Implementar sistema de notificaciones
                    # Por ahora solo registramos en logs
                    print(f'NOTIFICACIÓN: Testigo {user.nombre} verificó presencia en {ubicacion.nombre_completo}')
                    print(f'  -> Coordinador a notificar: {coordinador.nombre}')
                    coordinador_notificado = True
        
        return jsonify({
            'success': True,
            'message': 'Presencia verificada exitosamente' + (' y coordinador notificado' if coordinador_notificado else ''),
            'data': {
                'presencia_verificada': True,
                'presencia_verificada_at': user.presencia_verificada_at.isoformat(),
                'coordinador_notificado': coordinador_notificado
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auth_bp.route('/e14/search', methods=['POST'])
@jwt_required()
def search_formularios_e14():
    '''Buscar formularios E-14 por criterios'''
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'testigo_electoral':
            return jsonify({
                'success': False,
                'error': 'Solo los testigos pueden buscar formularios'
            }), 403
        
        data = request.get_json()
        
        # Criterios de búsqueda
        testigo_id = data.get('testigo_id')
        estado = data.get('estado')
        mesa_id = data.get('mesa_id')
        tipo_eleccion_id = data.get('tipo_eleccion_id')
        
        # Construir query base
        query = FormularioE14.query
        
        # Aplicar filtros
        if testigo_id:
            query = query.filter_by(testigo_id=testigo_id)
        if estado:
            query = query.filter_by(estado=estado)
        if mesa_id:
            query = query.filter_by(mesa_id=mesa_id)
        if tipo_eleccion_id:
            query = query.filter_by(tipo_eleccion_id=tipo_eleccion_id)
        
        # Ejecutar búsqueda
        formularios = query.order_by(FormularioE14.created_at.desc()).all()
        
        formularios_data = []
        for f in formularios:
            mesa = Location.query.get(f.mesa_id)
            testigo = User.query.get(f.testigo_id)
            
            formularios_data.append({
                'id': f.id,
                'mesa_id': f.mesa_id,
                'mesa_nombre': mesa.nombre_completo if mesa else None,
                'testigo_id': f.testigo_id,
                'testigo_nombre': testigo.nombre if testigo else None,
                'estado': f.estado,
                'total_votos': f.total_votos,
                'votos_validos': f.votos_validos,
                'created_at': f.created_at.isoformat() if f.created_at else None
            })
        
        return jsonify({
            'success': True,
            'data': {
                'formularios': formularios_data,
                'total': len(formularios_data)
            }
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
'''
                                
with open('backend/routes/auth.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('auth.py rewritten successfully')