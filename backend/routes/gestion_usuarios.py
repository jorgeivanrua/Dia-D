"""
Blueprint para gestión de usuarios por ubicación
Permite crear testigos, coordinadores y administradores basados en DIVIPOLA
"""

from flask import Blueprint, request, jsonify
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from flask_jwt_extended import jwt_required
from backend.utils.decorators import role_required
from flask_jwt_extended import get_jwt_identity
import secrets
import string

gestion_usuarios_bp = Blueprint('gestion_usuarios', __name__, url_prefix='/api/gestion-usuarios')

def generar_password_seguro(longitud=12):
    """Generar contraseña segura"""
    caracteres = string.ascii_letters + string.digits + "!@#$%&*"
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

def generar_username(rol, ubicacion):
    """Generar username basado en rol y ubicación"""
    prefijos = {
        'testigo_electoral': 'testigo',
        'coordinador_puesto': 'coord.puesto',
        'coordinador_municipal': 'coord.mun',
        'coordinador_departamental': 'coord.dept',
        'admin_municipal': 'admin.mun',
        'admin_departamental': 'admin.dept'
    }
    
    prefijo = prefijos.get(rol, rol)
    
    if ubicacion.tipo == 'mesa':
        return f"{prefijo}.{ubicacion.puesto_codigo}.{ubicacion.mesa_codigo}"
    elif ubicacion.tipo == 'puesto':
        return f"{prefijo}.{ubicacion.puesto_codigo}"
    elif ubicacion.tipo == 'municipio':
        return f"{prefijo}.{ubicacion.municipio_codigo}"
    elif ubicacion.tipo == 'departamento':
        return f"{prefijo}.{ubicacion.departamento_codigo}"
    
    return f"{prefijo}.{ubicacion.id}"

@gestion_usuarios_bp.route('/crear-testigos-puesto', methods=['POST'])
@jwt_required()
@role_required(['super_admin', 'admin_departamental', 'admin_municipal', 'coordinador_puesto'])
def crear_testigos_puesto():
    """
    Crear testigos a nivel de puesto (no de mesa)
    Los testigos seleccionan su mesa al hacer login
    Cantidad máxima de testigos = cantidad de mesas del puesto
    """
    try:
        data = request.get_json()
        puesto_id = data.get('puesto_id')
        cantidad = data.get('cantidad')  # Opcional: cantidad específica
        
        if not puesto_id:
            return jsonify({
                'success': False,
                'error': 'puesto_id es requerido'
            }), 400
        
        # Verificar que el puesto existe
        puesto = Location.query.get(puesto_id)
        if not puesto or puesto.tipo != 'puesto':
            return jsonify({
                'success': False,
                'error': 'Puesto no encontrado'
            }), 404
        
        # Contar mesas del puesto
        total_mesas = Location.query.filter_by(
            tipo='mesa',
            puesto_codigo=puesto.puesto_codigo,
            zona_codigo=puesto.zona_codigo,
            municipio_codigo=puesto.municipio_codigo,
            departamento_codigo=puesto.departamento_codigo
        ).count()
        
        if total_mesas == 0:
            return jsonify({
                'success': False,
                'error': 'No se encontraron mesas para este puesto'
            }), 404
        
        # Contar testigos existentes para este puesto
        testigos_existentes = User.query.filter_by(
            rol='testigo_electoral',
            ubicacion_id=puesto.id
        ).all()
        
        testigos_existentes_count = len(testigos_existentes)
        
        # Si no se especifica cantidad, crear tantos como mesas falten
        if cantidad is None:
            cantidad_a_crear = total_mesas - testigos_existentes_count
        else:
            cantidad_a_crear = cantidad
        
        # Validar que no se exceda el límite
        if testigos_existentes_count >= total_mesas:
            return jsonify({
                'success': False,
                'error': f'Ya existen {testigos_existentes_count} testigos para este puesto (máximo: {total_mesas} mesas)',
                'testigos_existentes': [{
                    'username': t.nombre,
                    'id': t.id
                } for t in testigos_existentes]
            }), 400
        
        # Ajustar cantidad si excede el límite
        if testigos_existentes_count + cantidad_a_crear > total_mesas:
            cantidad_a_crear = total_mesas - testigos_existentes_count
        
        if cantidad_a_crear <= 0:
            return jsonify({
                'success': False,
                'error': 'No se pueden crear más testigos para este puesto'
            }), 400
        
        testigos_creados = []
        
        # Crear testigos asignados al PUESTO
        for i in range(cantidad_a_crear):
            numero_testigo = testigos_existentes_count + i + 1
            
            # Crear username: testigo.{puesto_codigo}.{numero}
            username = f"testigo.{puesto.puesto_codigo}.{numero_testigo:02d}"
            
            # Verificar que el username no exista (por si acaso)
            while User.query.filter_by(nombre=username).first():
                numero_testigo += 1
                username = f"testigo.{puesto.puesto_codigo}.{numero_testigo:02d}"
            
            password = generar_password_seguro()
            
            testigo = User(
                nombre=username,
                rol='testigo_electoral',
                ubicacion_id=puesto.id,  # Asignado al PUESTO, no a la mesa
                activo=True
            )
            testigo.set_password(password)
            
            db.session.add(testigo)
            
            testigos_creados.append({
                'username': username,
                'password': password,
                'numero': numero_testigo
            })
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'puesto': puesto.nombre_completo,
                'puesto_codigo': puesto.puesto_codigo,
                'total_mesas': total_mesas,
                'testigos_creados': testigos_creados,
                'testigos_existentes': [{
                    'username': t.nombre
                } for t in testigos_existentes],
                'total_existentes_previos': testigos_existentes_count,
                'total_testigos_ahora': testigos_existentes_count + len(testigos_creados),
                'total_creados': len(testigos_creados),
                'espacios_disponibles': total_mesas - (testigos_existentes_count + len(testigos_creados))
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gestion_usuarios_bp.route('/crear-coordinador-puesto', methods=['POST'])
@jwt_required()
@role_required(['super_admin', 'admin_departamental', 'admin_municipal'])
def crear_coordinador_puesto():
    """
    Crear coordinador para un puesto específico
    """
    try:
        data = request.get_json()
        puesto_id = data.get('puesto_id')
        
        if not puesto_id:
            return jsonify({
                'success': False,
                'error': 'puesto_id es requerido'
            }), 400
        
        # Verificar que el puesto existe
        puesto = Location.query.get(puesto_id)
        if not puesto or puesto.tipo != 'puesto':
            return jsonify({
                'success': False,
                'error': 'Puesto no encontrado'
            }), 404
        
        # Verificar si ya existe un coordinador para este puesto
        coordinador_existente = User.query.filter_by(
            rol='coordinador_puesto',
            ubicacion_id=puesto.id
        ).first()
        
        if coordinador_existente:
            return jsonify({
                'success': False,
                'error': 'Ya existe un coordinador para este puesto',
                'coordinador': coordinador_existente.nombre
            }), 400
        
        # Crear nuevo coordinador
        username = generar_username('coordinador_puesto', puesto)
        password = generar_password_seguro()
        
        coordinador = User(
            nombre=username,
            rol='coordinador_puesto',
            ubicacion_id=puesto.id,
            activo=True
        )
        coordinador.set_password(password)
        
        db.session.add(coordinador)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'username': username,
                'password': password,
                'puesto': puesto.nombre_completo,
                'rol': 'coordinador_puesto'
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gestion_usuarios_bp.route('/crear-usuarios-municipio', methods=['POST'])
@jwt_required()
@role_required(['super_admin', 'admin_departamental'])
def crear_usuarios_municipio():
    """
    Crear coordinador y admin municipal para un municipio
    """
    try:
        data = request.get_json()
        municipio_id = data.get('municipio_id')
        crear_coordinador = data.get('crear_coordinador', True)
        crear_admin = data.get('crear_admin', True)
        
        if not municipio_id:
            return jsonify({
                'success': False,
                'error': 'municipio_id es requerido'
            }), 400
        
        # Verificar que el municipio existe
        municipio = Location.query.get(municipio_id)
        if not municipio or municipio.tipo != 'municipio':
            return jsonify({
                'success': False,
                'error': 'Municipio no encontrado'
            }), 404
        
        usuarios_creados = []
        
        # Crear coordinador municipal
        if crear_coordinador:
            coord_existente = User.query.filter_by(
                rol='coordinador_municipal',
                ubicacion_id=municipio.id
            ).first()
            
            if not coord_existente:
                username = generar_username('coordinador_municipal', municipio)
                password = generar_password_seguro()
                
                coordinador = User(
                    nombre=username,
                    rol='coordinador_municipal',
                    ubicacion_id=municipio.id,
                    activo=True
                )
                coordinador.set_password(password)
                db.session.add(coordinador)
                
                usuarios_creados.append({
                    'rol': 'coordinador_municipal',
                    'username': username,
                    'password': password
                })
        
        # Crear admin municipal
        if crear_admin:
            admin_existente = User.query.filter_by(
                rol='admin_municipal',
                ubicacion_id=municipio.id
            ).first()
            
            if not admin_existente:
                username = generar_username('admin_municipal', municipio)
                password = generar_password_seguro()
                
                admin = User(
                    nombre=username,
                    rol='admin_municipal',
                    ubicacion_id=municipio.id,
                    activo=True
                )
                admin.set_password(password)
                db.session.add(admin)
                
                usuarios_creados.append({
                    'rol': 'admin_municipal',
                    'username': username,
                    'password': password
                })
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'municipio': municipio.nombre_completo,
                'usuarios_creados': usuarios_creados
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gestion_usuarios_bp.route('/crear-usuarios-departamento', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def crear_usuarios_departamento():
    """
    Crear coordinador y admin departamental
    """
    try:
        data = request.get_json()
        departamento_id = data.get('departamento_id')
        crear_coordinador = data.get('crear_coordinador', True)
        crear_admin = data.get('crear_admin', True)
        
        if not departamento_id:
            return jsonify({
                'success': False,
                'error': 'departamento_id es requerido'
            }), 400
        
        # Verificar que el departamento existe
        departamento = Location.query.get(departamento_id)
        if not departamento or departamento.tipo != 'departamento':
            return jsonify({
                'success': False,
                'error': 'Departamento no encontrado'
            }), 404
        
        usuarios_creados = []
        
        # Crear coordinador departamental
        if crear_coordinador:
            coord_existente = User.query.filter_by(
                rol='coordinador_departamental',
                ubicacion_id=departamento.id
            ).first()
            
            if not coord_existente:
                username = generar_username('coordinador_departamental', departamento)
                password = generar_password_seguro()
                
                coordinador = User(
                    nombre=username,
                    rol='coordinador_departamental',
                    ubicacion_id=departamento.id,
                    activo=True
                )
                coordinador.set_password(password)
                db.session.add(coordinador)
                
                usuarios_creados.append({
                    'rol': 'coordinador_departamental',
                    'username': username,
                    'password': password
                })
        
        # Crear admin departamental
        if crear_admin:
            admin_existente = User.query.filter_by(
                rol='admin_departamental',
                ubicacion_id=departamento.id
            ).first()
            
            if not admin_existente:
                username = generar_username('admin_departamental', departamento)
                password = generar_password_seguro()
                
                admin = User(
                    nombre=username,
                    rol='admin_departamental',
                    ubicacion_id=departamento.id,
                    activo=True
                )
                admin.set_password(password)
                db.session.add(admin)
                
                usuarios_creados.append({
                    'rol': 'admin_departamental',
                    'username': username,
                    'password': password
                })
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'departamento': departamento.nombre_completo,
                'usuarios_creados': usuarios_creados
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gestion_usuarios_bp.route('/listar-usuarios-ubicacion/<int:ubicacion_id>', methods=['GET'])
@jwt_required()
@role_required(['super_admin', 'admin_departamental', 'admin_municipal', 'coordinador_puesto'])
def listar_usuarios_ubicacion(ubicacion_id):
    """
    Listar todos los usuarios de una ubicación específica
    """
    try:
        ubicacion = Location.query.get(ubicacion_id)
        if not ubicacion:
            return jsonify({
                'success': False,
                'error': 'Ubicación no encontrada'
            }), 404
        
        usuarios = User.query.filter_by(ubicacion_id=ubicacion_id).all()
        
        return jsonify({
            'success': True,
            'data': {
                'ubicacion': ubicacion.nombre_completo,
                'tipo': ubicacion.tipo,
                'usuarios': [{
                    'id': u.id,
                    'username': u.nombre,
                    'rol': u.rol,
                    'activo': u.activo,
                    'ultimo_acceso': u.ultimo_acceso.isoformat() if u.ultimo_acceso else None
                } for u in usuarios]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gestion_usuarios_bp.route('/resetear-password/<int:usuario_id>', methods=['POST'])
@jwt_required()
@role_required(['super_admin', 'admin_departamental', 'admin_municipal'])
def resetear_password(usuario_id):
    """
    Resetear contraseña de un usuario
    """
    try:
        usuario = User.query.get(usuario_id)
        if not usuario:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        nueva_password = generar_password_seguro()
        usuario.set_password(nueva_password)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'username': usuario.nombre,
                'nueva_password': nueva_password
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gestion_usuarios_bp.route('/puestos', methods=['GET'])
@jwt_required()
@role_required(['super_admin', 'admin_departamental', 'admin_municipal', 'coordinador_puesto'])
def listar_puestos():
    """
    Listar todos los puestos de votación disponibles
    """
    try:
        puestos = Location.query.filter_by(tipo='puesto').order_by(
            Location.departamento_nombre,
            Location.municipio_nombre,
            Location.puesto_nombre
        ).all()
        
        return jsonify({
            'success': True,
            'puestos': [{
                'id': p.id,
                'codigo': p.puesto_codigo,
                'nombre': p.puesto_nombre,
                'municipio': p.municipio_nombre,
                'departamento': p.departamento_nombre,
                'nombre_completo': p.nombre_completo,
                'total_mesas': Location.query.filter_by(
                    tipo='mesa',
                    puesto_codigo=p.puesto_codigo,
                    zona_codigo=p.zona_codigo,
                    municipio_codigo=p.municipio_codigo,
                    departamento_codigo=p.departamento_codigo
                ).count()
            } for p in puestos]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gestion_usuarios_bp.route('/municipios', methods=['GET'])
@jwt_required()
@role_required(['super_admin', 'admin_departamental'])
def listar_municipios():
    """
    Listar todos los municipios disponibles
    """
    try:
        municipios = Location.query.filter_by(tipo='municipio').order_by(
            Location.departamento_nombre,
            Location.municipio_nombre
        ).all()
        
        return jsonify({
            'success': True,
            'municipios': [{
                'id': m.id,
                'codigo': m.municipio_codigo,
                'nombre': m.municipio_nombre,
                'departamento': m.departamento_nombre,
                'nombre_completo': m.nombre_completo,
                'total_puestos': Location.query.filter_by(
                    tipo='puesto',
                    municipio_codigo=m.municipio_codigo,
                    departamento_codigo=m.departamento_codigo
                ).count()
            } for m in municipios]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gestion_usuarios_bp.route('/departamentos', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def listar_departamentos():
    """
    Listar todos los departamentos disponibles
    """
    try:
        departamentos = Location.query.filter_by(tipo='departamento').order_by(
            Location.departamento_nombre
        ).all()
        
        return jsonify({
            'success': True,
            'departamentos': [{
                'id': d.id,
                'codigo': d.departamento_codigo,
                'nombre': d.departamento_nombre,
                'nombre_completo': d.nombre_completo,
                'total_municipios': Location.query.filter_by(
                    tipo='municipio',
                    departamento_codigo=d.departamento_codigo
                ).count()
            } for d in departamentos]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
