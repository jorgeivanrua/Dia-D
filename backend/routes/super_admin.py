"""
Rutas del Super Admin
"""
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.utils.decorators import role_required

super_admin_bp = Blueprint('super_admin', __name__, url_prefix='/api/super-admin')


@super_admin_bp.route('/stats', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_stats():
    """
    Obtener estadísticas globales del sistema
    """
    try:
        from backend.database import db
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.location import Location
        
        # Contar usuarios activos
        total_usuarios = User.query.filter_by(activo=True).count()
        
        # Contar puestos y mesas
        total_puestos = Location.query.filter_by(tipo='puesto').count()
        total_mesas = Location.query.filter_by(tipo='mesa').count()
        
        # Contar formularios
        total_formularios = FormularioE14.query.count()
        formularios_pendientes = FormularioE14.query.filter_by(estado='pendiente').count()
        formularios_validados = FormularioE14.query.filter_by(estado='validado').count()
        
        # Calcular porcentaje
        porcentaje_validados = (formularios_validados / total_formularios * 100) if total_formularios > 0 else 0
        
        return jsonify({
            'success': True,
            'data': {
                'totalUsuarios': total_usuarios,
                'usuariosChange': 0,  # TODO: Calcular cambio del día
                'totalPuestos': total_puestos,
                'totalMesas': total_mesas,
                'totalFormularios': total_formularios,
                'formulariosPendientes': formularios_pendientes,
                'totalValidados': formularios_validados,
                'porcentajeValidados': round(porcentaje_validados, 2)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_all_users():
    """
    Obtener todos los usuarios del sistema
    """
    try:
        from backend.models.location import Location
        
        users = User.query.all()
        
        users_data = []
        for user in users:
            user_dict = {
                'id': user.id,
                'nombre': user.nombre,
                'rol': user.rol,
                'activo': user.activo,
                'ubicacion_id': user.ubicacion_id,
                'ubicacion_nombre': None,
                'password': '••••••••',  # Las contraseñas están hasheadas, no se pueden mostrar
                'ultimo_acceso': user.ultimo_acceso.isoformat() if hasattr(user, 'ultimo_acceso') and user.ultimo_acceso else None,
                'created_at': user.created_at.isoformat() if hasattr(user, 'created_at') and user.created_at else None
            }
            
            # Obtener nombre de ubicación
            if user.ubicacion_id:
                try:
                    ubicacion = Location.query.get(user.ubicacion_id)
                    if ubicacion:
                        user_dict['ubicacion_nombre'] = ubicacion.nombre_completo
                except:
                    pass
            
            users_data.append(user_dict)
        
        return jsonify({
            'success': True,
            'data': users_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/system-health', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_system_health():
    """
    Obtener estado de salud del sistema
    """
    try:
        return jsonify({
            'success': True,
            'data': {
                'status': 'healthy',
                'cpu_percent': 0,
                'memory_percent': 0,
                'database': 'healthy',
                'timestamp': datetime.now().isoformat()
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/monitoreo-departamental', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_monitoreo_departamental():
    """
    Obtener monitoreo por departamento
    """
    try:
        from backend.models.location import Location
        from backend.models.formulario_e14 import FormularioE14
        
        # Por ahora retornar datos vacíos
        return jsonify({
            'success': True,
            'data': []
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/users', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def create_user():
    """
    Crear nuevo usuario
    """
    try:
        from backend.database import db
        from backend.models.location import Location
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        nombre = data.get('nombre')
        rol = data.get('rol')
        password = data.get('password')
        ubicacion_data = data.get('ubicacion_data', {})
        
        if not nombre or not rol or not password:
            return jsonify({
                'success': False,
                'error': 'Nombre, rol y contraseña son requeridos'
            }), 400
        
        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(nombre=nombre).first()
        if existing_user:
            return jsonify({
                'success': False,
                'error': f'Ya existe un usuario con el nombre "{nombre}"'
            }), 400
        
        # Buscar ubicación si es necesario
        ubicacion_id = None
        if rol != 'super_admin' and ubicacion_data:
            tipo = ubicacion_data.get('tipo')
            
            if tipo == 'departamento':
                ubicacion = Location.query.filter_by(
                    tipo='departamento',
                    departamento_codigo=ubicacion_data.get('departamento_codigo')
                ).first()
            elif tipo == 'municipio':
                ubicacion = Location.query.filter_by(
                    tipo='municipio',
                    departamento_codigo=ubicacion_data.get('departamento_codigo'),
                    municipio_codigo=ubicacion_data.get('municipio_codigo')
                ).first()
            elif tipo == 'puesto':
                ubicacion = Location.query.filter_by(
                    tipo='puesto',
                    departamento_codigo=ubicacion_data.get('departamento_codigo'),
                    municipio_codigo=ubicacion_data.get('municipio_codigo'),
                    zona_codigo=ubicacion_data.get('zona_codigo'),
                    puesto_codigo=ubicacion_data.get('puesto_codigo')
                ).first()
            else:
                ubicacion = None
            
            if ubicacion:
                ubicacion_id = ubicacion.id
            elif tipo:  # Si se especificó tipo pero no se encontró
                return jsonify({
                    'success': False,
                    'error': 'No se encontró la ubicación especificada'
                }), 404
        
        # Crear usuario
        new_user = User(
            nombre=nombre,
            rol=rol,
            ubicacion_id=ubicacion_id,
            activo=data.get('activo', True)
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Usuario creado exitosamente',
            'data': {
                'id': new_user.id,
                'nombre': new_user.nombre,
                'rol': new_user.rol,
                'ubicacion_id': new_user.ubicacion_id
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
        
    except Exception as e:
        import traceback
        print(f"Error en get_all_users: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required(['super_admin'])
def update_user(user_id):
    """
    Actualizar un usuario
    """
    try:
        from backend.database import db
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        data = request.get_json()
        
        # Actualizar campos permitidos
        if 'nombre' in data:
            user.nombre = data['nombre']
        if 'rol' in data:
            user.rol = data['rol']
        if 'ubicacion_id' in data:
            user.ubicacion_id = data['ubicacion_id']
        if 'activo' in data:
            user.activo = data['activo']
        if 'password' in data:
            user.set_password(data['password'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Usuario actualizado exitosamente',
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/users/<int:user_id>/reset-password', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def reset_user_password(user_id):
    """
    Resetear contraseña de un usuario
    """
    try:
        from backend.database import db
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        data = request.get_json()
        new_password = data.get('password')
        
        if not new_password:
            return jsonify({
                'success': False,
                'error': 'Se requiere una nueva contraseña'
            }), 400
        
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Contraseña reseteada exitosamente'
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



@super_admin_bp.route('/upload/users', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def upload_users():
    """
    Cargar usuarios masivamente desde archivo Excel
    
    Formato esperado del Excel:
    - nombre: Nombre del usuario
    - password: Contraseña
    - rol: Rol del usuario (testigo, coordinador_puesto, etc.)
    - ubicacion_codigo: Código de la ubicación (opcional)
    """
    try:
        from backend.database import db
        import pandas as pd
        from io import BytesIO
        
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó ningún archivo'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nombre de archivo vacío'
            }), 400
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({
                'success': False,
                'error': 'El archivo debe ser Excel (.xlsx o .xls)'
            }), 400
        
        # Leer Excel
        df = pd.read_excel(BytesIO(file.read()))
        
        # Validar columnas requeridas
        required_columns = ['nombre', 'password', 'rol']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                'success': False,
                'error': f'Faltan columnas requeridas: {", ".join(missing_columns)}'
            }), 400
        
        # Procesar usuarios
        created_users = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Verificar si el usuario ya existe
                existing_user = User.query.filter_by(nombre=row['nombre']).first()
                if existing_user:
                    errors.append(f"Fila {index + 2}: Usuario '{row['nombre']}' ya existe")
                    continue
                
                # Buscar ubicación si se proporciona código
                ubicacion_id = None
                if 'ubicacion_codigo' in row and pd.notna(row['ubicacion_codigo']):
                    from backend.models.location import Location
                    ubicacion = Location.query.filter_by(codigo=str(row['ubicacion_codigo'])).first()
                    if ubicacion:
                        ubicacion_id = ubicacion.id
                    else:
                        errors.append(f"Fila {index + 2}: Ubicación con código '{row['ubicacion_codigo']}' no encontrada")
                
                # Crear usuario
                user = User(
                    nombre=row['nombre'],
                    rol=row['rol'],
                    ubicacion_id=ubicacion_id,
                    activo=True
                )
                user.set_password(row['password'])
                
                db.session.add(user)
                created_users.append(row['nombre'])
                
            except Exception as e:
                errors.append(f"Fila {index + 2}: {str(e)}")
        
        # Commit si hay usuarios creados
        if created_users:
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(created_users)} usuarios creados exitosamente',
            'data': {
                'created': created_users,
                'errors': errors,
                'total_processed': len(df),
                'total_created': len(created_users),
                'total_errors': len(errors)
            }
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error procesando archivo: {str(e)}'
        }), 500


@super_admin_bp.route('/upload/locations', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def upload_locations():
    """
    Cargar DIVIPOLA (ubicaciones) masivamente desde archivo Excel
    
    Formato esperado del Excel:
    - codigo: Código de la ubicación
    - nombre: Nombre de la ubicación
    - tipo: Tipo (departamento, municipio, puesto, mesa)
    - departamento_codigo: Código del departamento padre (opcional)
    - municipio_codigo: Código del municipio padre (opcional)
    - puesto_codigo: Código del puesto padre (opcional)
    """
    try:
        from backend.database import db
        from backend.models.location import Location
        import pandas as pd
        from io import BytesIO
        
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó ningún archivo'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nombre de archivo vacío'
            }), 400
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({
                'success': False,
                'error': 'El archivo debe ser Excel (.xlsx o .xls)'
            }), 400
        
        # Leer Excel
        df = pd.read_excel(BytesIO(file.read()))
        
        # Validar columnas requeridas
        required_columns = ['codigo', 'nombre', 'tipo']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                'success': False,
                'error': f'Faltan columnas requeridas: {", ".join(missing_columns)}'
            }), 400
        
        # Procesar ubicaciones
        created_locations = []
        errors = []
        
        # Ordenar por tipo para crear jerarquía correctamente
        tipo_order = {'departamento': 0, 'municipio': 1, 'puesto': 2, 'mesa': 3}
        df['tipo_order'] = df['tipo'].map(tipo_order)
        df = df.sort_values('tipo_order')
        
        for index, row in df.iterrows():
            try:
                # Verificar si la ubicación ya existe
                existing_location = Location.query.filter_by(codigo=str(row['codigo'])).first()
                if existing_location:
                    errors.append(f"Fila {index + 2}: Ubicación con código '{row['codigo']}' ya existe")
                    continue
                
                # Buscar padre según tipo
                departamento_id = None
                municipio_id = None
                puesto_id = None
                
                if row['tipo'] == 'municipio' and 'departamento_codigo' in row and pd.notna(row['departamento_codigo']):
                    padre = Location.query.filter_by(codigo=str(row['departamento_codigo'])).first()
                    if padre:
                        departamento_id = padre.id
                
                if row['tipo'] == 'puesto' and 'municipio_codigo' in row and pd.notna(row['municipio_codigo']):
                    padre = Location.query.filter_by(codigo=str(row['municipio_codigo'])).first()
                    if padre:
                        municipio_id = padre.id
                        departamento_id = padre.departamento_id
                
                if row['tipo'] == 'mesa' and 'puesto_codigo' in row and pd.notna(row['puesto_codigo']):
                    padre = Location.query.filter_by(codigo=str(row['puesto_codigo'])).first()
                    if padre:
                        puesto_id = padre.id
                        municipio_id = padre.municipio_id
                        departamento_id = padre.departamento_id
                
                # Crear ubicación
                location = Location(
                    codigo=str(row['codigo']),
                    nombre=row['nombre'],
                    tipo=row['tipo'],
                    departamento_id=departamento_id,
                    municipio_id=municipio_id,
                    puesto_id=puesto_id
                )
                
                db.session.add(location)
                created_locations.append(row['nombre'])
                
            except Exception as e:
                errors.append(f"Fila {index + 2}: {str(e)}")
        
        # Commit si hay ubicaciones creadas
        if created_locations:
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(created_locations)} ubicaciones creadas exitosamente',
            'data': {
                'created': created_locations,
                'errors': errors,
                'total_processed': len(df),
                'total_created': len(created_locations),
                'total_errors': len(errors)
            }
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error procesando archivo: {str(e)}'
        }), 500


@super_admin_bp.route('/upload/partidos', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def upload_partidos():
    """
    Cargar partidos políticos masivamente desde archivo Excel
    
    Formato esperado del Excel:
    - codigo: Código del partido (opcional, se genera automático)
    - nombre: Nombre del partido
    - nombre_corto: Nombre corto del partido
    - color: Color en formato hexadecimal (ej: #FF0000)
    - logo_url: URL del logo (opcional)
    """
    try:
        from backend.database import db
        from backend.models.partido_politico import PartidoPolitico as Partido
        import pandas as pd
        from io import BytesIO
        
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó ningún archivo'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nombre de archivo vacío'
            }), 400
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({
                'success': False,
                'error': 'El archivo debe ser Excel (.xlsx o .xls)'
            }), 400
        
        # Leer Excel
        df = pd.read_excel(BytesIO(file.read()))
        
        # Validar columnas requeridas
        required_columns = ['nombre', 'nombre_corto', 'color']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                'success': False,
                'error': f'Faltan columnas requeridas: {", ".join(missing_columns)}'
            }), 400
        
        # Procesar partidos
        created_partidos = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Verificar si el partido ya existe
                existing_partido = Partido.query.filter_by(nombre=row['nombre']).first()
                if existing_partido:
                    errors.append(f"Fila {index + 2}: Partido '{row['nombre']}' ya existe")
                    continue
                
                # Generar código si no existe
                codigo = row.get('codigo') if 'codigo' in row and pd.notna(row.get('codigo')) else row['nombre'].upper().replace(' ', '_')
                
                # Crear partido
                partido = Partido(
                    codigo=codigo,
                    nombre=row['nombre'],
                    nombre_corto=row['nombre_corto'],
                    color=row['color'],
                    logo_url=row.get('logo_url') if 'logo_url' in row and pd.notna(row.get('logo_url')) else None,
                    activo=row.get('activo', True) if 'activo' in row else True
                )
                
                db.session.add(partido)
                created_partidos.append(row['nombre'])
                
            except Exception as e:
                errors.append(f"Fila {index + 2}: {str(e)}")
        
        # Commit si hay partidos creados
        if created_partidos:
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(created_partidos)} partidos creados exitosamente',
            'data': {
                'created': created_partidos,
                'errors': errors,
                'total_processed': len(df),
                'total_created': len(created_partidos),
                'total_errors': len(errors)
            }
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error procesando archivo: {str(e)}'
        }), 500


@super_admin_bp.route('/upload/candidatos', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def upload_candidatos():
    """
    Cargar candidatos masivamente desde archivo Excel
    
    Formato esperado del Excel:
    - codigo: Código del candidato (opcional, se genera automático)
    - nombre_completo: Nombre completo del candidato
    - partido_nombre: Nombre del partido
    - tipo_eleccion_nombre: Nombre del tipo de elección
    - numero_lista: Número de lista (opcional)
    - es_independiente: True/False (opcional, default False)
    - es_cabeza_lista: True/False (opcional, default False)
    - foto_url: URL de la foto (opcional)
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import TipoEleccion
        from backend.models.partido_politico import PartidoPolitico as Partido
        from backend.models.candidato import Candidato
        import pandas as pd
        from io import BytesIO
        
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó ningún archivo'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nombre de archivo vacío'
            }), 400
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({
                'success': False,
                'error': 'El archivo debe ser Excel (.xlsx o .xls)'
            }), 400
        
        # Leer Excel
        df = pd.read_excel(BytesIO(file.read()))
        
        # Validar columnas requeridas
        required_columns = ['nombre_completo', 'partido_nombre', 'tipo_eleccion_nombre']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                'success': False,
                'error': f'Faltan columnas requeridas: {", ".join(missing_columns)}'
            }), 400
        
        # Procesar candidatos
        created_candidatos = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Buscar partido
                partido = Partido.query.filter_by(nombre=row['partido_nombre']).first()
                if not partido:
                    errors.append(f"Fila {index + 2}: Partido '{row['partido_nombre']}' no encontrado")
                    continue
                
                # Buscar tipo de elección
                tipo_eleccion = TipoEleccion.query.filter_by(nombre=row['tipo_eleccion_nombre']).first()
                if not tipo_eleccion:
                    errors.append(f"Fila {index + 2}: Tipo de elección '{row['tipo_eleccion_nombre']}' no encontrado")
                    continue
                
                # Generar código si no existe
                if 'codigo' in row and pd.notna(row.get('codigo')):
                    codigo = row['codigo']
                else:
                    codigo = f"{tipo_eleccion.codigo}_{partido.codigo}_{index+1}"
                
                # Verificar si el candidato ya existe
                existing_candidato = Candidato.query.filter_by(codigo=codigo).first()
                
                if existing_candidato:
                    errors.append(f"Fila {index + 2}: Candidato con código '{codigo}' ya existe")
                    continue
                
                # Crear candidato
                candidato = Candidato(
                    codigo=codigo,
                    nombre_completo=row['nombre_completo'],
                    partido_id=partido.id,
                    tipo_eleccion_id=tipo_eleccion.id,
                    numero_lista=row.get('numero_lista') if 'numero_lista' in row and pd.notna(row.get('numero_lista')) else None,
                    es_independiente=row.get('es_independiente', False) if 'es_independiente' in row else False,
                    es_cabeza_lista=row.get('es_cabeza_lista', False) if 'es_cabeza_lista' in row else False,
                    foto_url=row.get('foto_url') if 'foto_url' in row and pd.notna(row.get('foto_url')) else None,
                    activo=row.get('activo', True) if 'activo' in row else True
                )
                
                db.session.add(candidato)
                created_candidatos.append(row['nombre_completo'])
                
            except Exception as e:
                errors.append(f"Fila {index + 2}: {str(e)}")
        
        # Commit si hay candidatos creados
        if created_candidatos:
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(created_candidatos)} candidatos creados exitosamente',
            'data': {
                'created': created_candidatos,
                'errors': errors,
                'total_processed': len(df),
                'total_created': len(created_candidatos),
                'total_errors': len(errors)
            }
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error procesando archivo: {str(e)}'
        }), 500



@super_admin_bp.route('/tipos-eleccion', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_tipos_eleccion():
    """
    Obtener todos los tipos de elección
    """
    try:
        from backend.models.configuracion_electoral import TipoEleccion
        
        tipos = TipoEleccion.query.all()
        
        return jsonify({
            'success': True,
            'data': [tipo.to_dict() for tipo in tipos]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/tipos-eleccion', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def create_tipo_eleccion():
    """
    Crear un nuevo tipo de elección
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import TipoEleccion
        
        data = request.get_json()
        
        if not data or 'nombre' not in data:
            return jsonify({
                'success': False,
                'error': 'El nombre es requerido'
            }), 400
        
        # Verificar que no exista
        existing = TipoEleccion.query.filter_by(nombre=data['nombre']).first()
        if existing:
            return jsonify({
                'success': False,
                'error': 'Ya existe un tipo de elección con ese nombre'
            }), 400
        
        # Generar código automático
        codigo = data.get('codigo', data['nombre'].upper().replace(' ', '_'))
        
        tipo = TipoEleccion(
            codigo=codigo,
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            es_uninominal=data.get('es_uninominal', False),
            permite_lista_cerrada=data.get('permite_lista_cerrada', not data.get('es_uninominal', False)),
            permite_lista_abierta=data.get('permite_lista_abierta', False),
            permite_coaliciones=data.get('permite_coaliciones', False),
            activo=data.get('activo', True)
        )
        
        db.session.add(tipo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tipo de elección creado exitosamente',
            'data': tipo.to_dict()
        }), 201
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/tipos-eleccion/<int:tipo_id>', methods=['PUT'])
@jwt_required()
@role_required(['super_admin'])
def update_tipo_eleccion(tipo_id):
    """
    Actualizar un tipo de elección (habilitar/deshabilitar)
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import TipoEleccion
        
        tipo = TipoEleccion.query.get(tipo_id)
        if not tipo:
            return jsonify({
                'success': False,
                'error': 'Tipo de elección no encontrado'
            }), 404
        
        data = request.get_json()
        
        if 'nombre' in data:
            tipo.nombre = data['nombre']
        if 'descripcion' in data:
            tipo.descripcion = data['descripcion']
        if 'es_uninominal' in data:
            tipo.es_uninominal = data['es_uninominal']
        if 'permite_lista_cerrada' in data:
            tipo.permite_lista_cerrada = data['permite_lista_cerrada']
        if 'permite_lista_abierta' in data:
            tipo.permite_lista_abierta = data['permite_lista_abierta']
        if 'permite_coaliciones' in data:
            tipo.permite_coaliciones = data['permite_coaliciones']
        if 'activo' in data:
            tipo.activo = data['activo']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tipo de elección actualizado exitosamente',
            'data': tipo.to_dict()
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/partidos/<int:partido_id>', methods=['PUT'])
@jwt_required()
@role_required(['super_admin'])
def update_partido(partido_id):
    """
    Actualizar un partido político
    """
    try:
        from backend.database import db
        from backend.models.partido_politico import PartidoPolitico as Partido
        
        partido = Partido.query.get(partido_id)
        if not partido:
            return jsonify({
                'success': False,
                'error': 'Partido no encontrado'
            }), 404
        
        data = request.get_json()
        
        # Actualizar campos
        if 'nombre' in data:
            partido.nombre = data['nombre']
        if 'nombre_corto' in data:
            partido.nombre_corto = data['nombre_corto']
        if 'color' in data:
            partido.color = data['color']
        if 'logo_url' in data:
            partido.logo_url = data['logo_url']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Partido actualizado exitosamente',
            'data': partido.to_dict()
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/partidos/<int:partido_id>/toggle', methods=['PUT'])
@jwt_required()
@role_required(['super_admin'])
def toggle_partido(partido_id):
    """
    Habilitar/deshabilitar un partido para recolección de datos
    """
    try:
        from backend.database import db
        from backend.models.partido_politico import PartidoPolitico as Partido
        
        partido = Partido.query.get(partido_id)
        if not partido:
            return jsonify({
                'success': False,
                'error': 'Partido no encontrado'
            }), 404
        
        data = request.get_json()
        partido.activo = data.get('activo', not partido.activo)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Partido {"habilitado" if partido.activo else "deshabilitado"} exitosamente',
            'data': partido.to_dict()
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/candidatos/<int:candidato_id>', methods=['PUT'])
@jwt_required()
@role_required(['super_admin'])
def update_candidato(candidato_id):
    """
    Actualizar un candidato
    """
    try:
        from backend.database import db
        from backend.models.candidato import Candidato
        
        candidato = Candidato.query.get(candidato_id)
        if not candidato:
            return jsonify({
                'success': False,
                'error': 'Candidato no encontrado'
            }), 404
        
        data = request.get_json()
        
        # Actualizar campos
        if 'nombre_completo' in data:
            candidato.nombre_completo = data['nombre_completo']
        if 'partido_id' in data:
            candidato.partido_id = data['partido_id'] if data['partido_id'] else None
        if 'tipo_eleccion_id' in data:
            candidato.tipo_eleccion_id = data['tipo_eleccion_id']
        if 'numero_lista' in data:
            candidato.numero_lista = data['numero_lista'] if data['numero_lista'] else None
        if 'foto_url' in data:
            candidato.foto_url = data['foto_url'] if data['foto_url'] else None
        if 'es_independiente' in data:
            candidato.es_independiente = data['es_independiente']
        if 'es_cabeza_lista' in data:
            candidato.es_cabeza_lista = data['es_cabeza_lista']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Candidato actualizado exitosamente',
            'data': candidato.to_dict()
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/candidatos/<int:candidato_id>/toggle', methods=['PUT'])
@jwt_required()
@role_required(['super_admin'])
def toggle_candidato(candidato_id):
    """
    Habilitar/deshabilitar un candidato para recolección de datos
    """
    try:
        from backend.database import db
        from backend.models.candidato import Candidato
        
        candidato = Candidato.query.get(candidato_id)
        if not candidato:
            return jsonify({
                'success': False,
                'error': 'Candidato no encontrado'
            }), 404
        
        data = request.get_json()
        candidato.activo = data.get('activo', not candidato.activo)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Candidato {"habilitado" if candidato.activo else "deshabilitado"} exitosamente',
            'data': candidato.to_dict()
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/tipos-eleccion/<int:tipo_id>/toggle', methods=['PUT'])
@jwt_required()
@role_required(['super_admin'])
def toggle_tipo_eleccion(tipo_id):
    """
    Habilitar/deshabilitar un tipo de elección para recolección de datos
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import TipoEleccion
        
        tipo = TipoEleccion.query.get(tipo_id)
        if not tipo:
            return jsonify({
                'success': False,
                'error': 'Tipo de elección no encontrado'
            }), 404
        
        data = request.get_json()
        tipo.activo = data.get('activo', not tipo.activo)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Tipo de elección {"habilitado" if tipo.activo else "deshabilitado"} exitosamente',
            'data': tipo.to_dict()
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/download/template/<template_type>', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def download_template(template_type):
    """
    Descargar plantilla Excel con datos de ejemplo
    
    Tipos: users, locations, partidos, candidatos, tipos_eleccion
    """
    try:
        import pandas as pd
        from io import BytesIO
        from flask import send_file
        
        templates = {
            'users': {
                'data': {
                    'nombre': ['Juan Perez', 'Maria Garcia', 'Carlos Lopez', 'Ana Martinez', 'Pedro Rodriguez'],
                    'password': ['password123', 'password456', 'password789', 'password101', 'password202'],
                    'rol': ['testigo', 'coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental', 'auditor'],
                    'ubicacion_codigo': ['001001001001', '001001001', '001001', '001', '']
                },
                'filename': 'plantilla_usuarios.xlsx'
            },
            'locations': {
                'data': {
                    'codigo': ['001', '001001', '001001001', '001001001001', '001001001002'],
                    'nombre': ['Departamento Ejemplo', 'Municipio Ejemplo', 'Puesto Electoral 1', 'Mesa 1', 'Mesa 2'],
                    'tipo': ['departamento', 'municipio', 'puesto', 'mesa', 'mesa'],
                    'departamento_codigo': ['', '001', '001', '001', '001'],
                    'municipio_codigo': ['', '', '001001', '001001', '001001'],
                    'puesto_codigo': ['', '', '', '001001001', '001001001']
                },
                'filename': 'plantilla_divipola.xlsx'
            },
            'partidos': {
                'data': {
                    'nombre': ['Partido Liberal', 'Partido Conservador', 'Partido Verde', 'Partido de la U', 'Polo Democrático'],
                    'sigla': ['PL', 'PC', 'PV', 'PU', 'PD'],
                    'color': ['#FF0000', '#0000FF', '#00FF00', '#FFFF00', '#FF00FF'],
                    'numero_lista': [1, 2, 3, 4, 5]
                },
                'filename': 'plantilla_partidos.xlsx'
            },
            'candidatos': {
                'data': {
                    'nombre': ['Juan Perez', 'Maria Garcia', 'Carlos Lopez', 'Ana Martinez', 'Pedro Rodriguez'],
                    'partido_nombre': ['Partido Liberal', 'Partido Conservador', 'Partido Verde', 'Partido de la U', 'Polo Democrático'],
                    'tipo_eleccion_nombre': ['Presidente', 'Senado', 'Cámara', 'Gobernador', 'Alcalde'],
                    'numero_lista': [1, 2, 3, 4, 5]
                },
                'filename': 'plantilla_candidatos.xlsx'
            },
            'tipos_eleccion': {
                'data': {
                    'nombre': ['Presidente', 'Senado', 'Cámara', 'Gobernador', 'Alcalde', 'Concejo', 'JAL'],
                    'es_uninominal': [True, False, False, True, True, False, False]
                },
                'filename': 'plantilla_tipos_eleccion.xlsx'
            }
        }
        
        if template_type not in templates:
            return jsonify({
                'success': False,
                'error': 'Tipo de plantilla no válido'
            }), 400
        
        template = templates[template_type]
        df = pd.DataFrame(template['data'])
        
        # Crear archivo Excel en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Datos')
            
            # Ajustar ancho de columnas
            worksheet = writer.sheets['Datos']
            for idx, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).apply(len).max(), len(col)) + 2
                worksheet.column_dimensions[chr(65 + idx)].width = max_length
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=template['filename']
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



# ============================================
# GESTIÓN DE CAMPAÑAS
# ============================================

@super_admin_bp.route('/campanas', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_campanas():
    """
    Obtener todas las campañas
    """
    try:
        from backend.models.configuracion_electoral import Campana
        
        campanas = Campana.query.order_by(Campana.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [campana.to_dict() for campana in campanas]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/campanas', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def create_campana():
    """
    Crear una nueva campaña
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import Campana
        
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if not data or 'nombre' not in data:
            return jsonify({
                'success': False,
                'error': 'El nombre es requerido'
            }), 400
        
        # Generar código automático
        codigo = data.get('codigo', data['nombre'].upper().replace(' ', '_'))
        
        # Verificar que no exista
        existing = Campana.query.filter_by(codigo=codigo).first()
        if existing:
            return jsonify({
                'success': False,
                'error': 'Ya existe una campaña con ese código'
            }), 400
        
        campana = Campana(
            codigo=codigo,
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            fecha_inicio=data.get('fecha_inicio'),
            fecha_fin=data.get('fecha_fin'),
            color_primario=data.get('color_primario', '#1e3c72'),
            color_secundario=data.get('color_secundario', '#2a5298'),
            logo_url=data.get('logo_url'),
            es_candidato_unico=data.get('es_candidato_unico', False),
            es_partido_completo=data.get('es_partido_completo', False),
            activa=False,  # No activar automáticamente
            created_by=int(user_id)
        )
        
        db.session.add(campana)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Campaña creada exitosamente',
            'data': campana.to_dict()
        }), 201
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/campanas/<int:campana_id>/activar', methods=['PUT'])
@jwt_required()
@role_required(['super_admin'])
def activar_campana(campana_id):
    """
    Activar una campaña (desactiva las demás)
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import Campana
        
        campana = Campana.query.get(campana_id)
        if not campana:
            return jsonify({
                'success': False,
                'error': 'Campaña no encontrada'
            }), 404
        
        # Desactivar todas las campañas
        Campana.query.update({'activa': False})
        
        # Activar la seleccionada
        campana.activa = True
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Campaña "{campana.nombre}" activada exitosamente',
            'data': campana.to_dict()
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/campanas/<int:campana_id>/reset', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def reset_campana(campana_id):
    """
    Resetear datos de una campaña (eliminar formularios, incidentes, delitos)
    PELIGROSO: Requiere confirmación
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import Campana
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
        
        data = request.get_json()
        confirmacion = data.get('confirmacion', '')
        
        if confirmacion != 'CONFIRMAR_RESET':
            return jsonify({
                'success': False,
                'error': 'Se requiere confirmación explícita'
            }), 400
        
        campana = Campana.query.get(campana_id)
        if not campana:
            return jsonify({
                'success': False,
                'error': 'Campaña no encontrada'
            }), 404
        
        # Contar registros antes de eliminar
        formularios_count = FormularioE14.query.filter_by(campana_id=campana_id).count()
        incidentes_count = IncidenteElectoral.query.filter_by(campana_id=campana_id).count()
        delitos_count = DelitoElectoral.query.filter_by(campana_id=campana_id).count()
        
        # Eliminar datos de la campaña
        FormularioE14.query.filter_by(campana_id=campana_id).delete()
        IncidenteElectoral.query.filter_by(campana_id=campana_id).delete()
        DelitoElectoral.query.filter_by(campana_id=campana_id).delete()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Campaña "{campana.nombre}" reseteada exitosamente',
            'data': {
                'formularios_eliminados': formularios_count,
                'incidentes_eliminados': incidentes_count,
                'delitos_eliminados': delitos_count
            }
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/campanas/<int:campana_id>', methods=['DELETE'])
@jwt_required()
@role_required(['super_admin'])
def delete_campana(campana_id):
    """
    Eliminar una campaña completa (incluyendo todos sus datos)
    PELIGROSO: Requiere confirmación
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import Campana
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
        
        data = request.get_json()
        confirmacion = data.get('confirmacion', '')
        
        if confirmacion != 'CONFIRMAR_ELIMINACION':
            return jsonify({
                'success': False,
                'error': 'Se requiere confirmación explícita'
            }), 400
        
        campana = Campana.query.get(campana_id)
        if not campana:
            return jsonify({
                'success': False,
                'error': 'Campaña no encontrada'
            }), 404
        
        if campana.activa:
            return jsonify({
                'success': False,
                'error': 'No se puede eliminar la campaña activa'
            }), 400
        
        # Eliminar todos los datos asociados
        FormularioE14.query.filter_by(campana_id=campana_id).delete()
        IncidenteElectoral.query.filter_by(campana_id=campana_id).delete()
        DelitoElectoral.query.filter_by(campana_id=campana_id).delete()
        
        # Eliminar la campaña
        db.session.delete(campana)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Campaña "{campana.nombre}" eliminada exitosamente'
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================
# GESTIÓN DE TEMAS
# ============================================

@super_admin_bp.route('/temas', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_temas():
    """
    Obtener todos los temas configurados
    """
    try:
        from backend.models.configuracion_electoral import ConfiguracionTema
        
        temas = ConfiguracionTema.query.filter_by(activo=True).all()
        
        return jsonify({
            'success': True,
            'data': [tema.to_dict() for tema in temas]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/temas', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def create_tema():
    """
    Crear una nueva configuración de tema
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import ConfiguracionTema
        
        data = request.get_json()
        
        if not data or 'nombre' not in data:
            return jsonify({
                'success': False,
                'error': 'El nombre es requerido'
            }), 400
        
        tema = ConfiguracionTema(
            nombre=data['nombre'],
            aplica_a_rol=data.get('aplica_a_rol'),
            aplica_a_tipo_eleccion_id=data.get('aplica_a_tipo_eleccion_id'),
            campana_id=data.get('campana_id'),
            color_primario=data.get('color_primario', '#1e3c72'),
            color_secundario=data.get('color_secundario', '#2a5298'),
            color_acento=data.get('color_acento', '#28a745'),
            color_fondo=data.get('color_fondo', '#f8f9fa'),
            color_texto=data.get('color_texto', '#212529'),
            logo_url=data.get('logo_url'),
            favicon_url=data.get('favicon_url'),
            activo=True
        )
        
        db.session.add(tema)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tema creado exitosamente',
            'data': tema.to_dict()
        }), 201
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



# ============================================
# TESTING Y AUDITORÍA
# ============================================

@super_admin_bp.route('/test/load-data', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def load_test_data_endpoint():
    """
    Cargar datos de prueba en el sistema
    """
    try:
        import subprocess
        import sys
        
        # Ejecutar script de carga de datos
        result = subprocess.run(
            [sys.executable, 'backend/scripts/load_test_data.py'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Datos de prueba cargados exitosamente',
                'output': result.stdout
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Error al cargar datos de prueba',
                'output': result.stderr
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/test/audit', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def system_audit():
    """
    Auditoría completa del sistema
    Verifica que todas las funcionalidades estén operativas
    """
    try:
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
        
        audit_results = {
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'success',
            'checks': []
        }
        
        # Check 1: Base de datos
        try:
            db.session.execute('SELECT 1')
            audit_results['checks'].append({
                'name': 'Database Connection',
                'status': 'pass',
                'message': 'Conexión a base de datos OK'
            })
        except Exception as e:
            audit_results['checks'].append({
                'name': 'Database Connection',
                'status': 'fail',
                'message': f'Error: {str(e)}'
            })
        
        # Check 2: Usuarios
        try:
            total_users = User.query.count()
            users_by_role = db.session.query(
                User.rol, db.func.count(User.id)
            ).group_by(User.rol).all()
            
            audit_results['checks'].append({
                'name': 'Users',
                'status': 'pass',
                'message': f'Total: {total_users} usuarios',
                'details': {role: count for role, count in users_by_role}
            })
        except Exception as e:
            audit_results['checks'].append({
                'name': 'Users',
                'status': 'fail',
                'message': f'Error: {str(e)}'
            })
        
        # Check 3: Ubicaciones
        try:
            locations_by_type = db.session.query(
                Location.tipo, db.func.count(Location.id)
            ).group_by(Location.tipo).all()
            
            audit_results['checks'].append({
                'name': 'Locations',
                'status': 'pass',
                'message': 'Ubicaciones configuradas',
                'details': {tipo: count for tipo, count in locations_by_type}
            })
        except Exception as e:
            audit_results['checks'].append({
                'name': 'Locations',
                'status': 'fail',
                'message': f'Error: {str(e)}'
            })
        
        # Check 4: Configuración Electoral
        try:
            from backend.models.configuracion_electoral import TipoEleccion
            from backend.models.partido_politico import PartidoPolitico as Partido
            from backend.models.candidato import Candidato
            
            tipos_count = TipoEleccion.query.filter_by(activo=True).count()
            partidos_count = Partido.query.filter_by(activo=True).count()
            candidatos_count = Candidato.query.filter_by(activo=True).count()
            
            audit_results['checks'].append({
                'name': 'Electoral Configuration',
                'status': 'pass',
                'message': 'Configuración electoral OK',
                'details': {
                    'tipos_eleccion': tipos_count,
                    'partidos': partidos_count,
                    'candidatos': candidatos_count
                }
            })
        except Exception as e:
            audit_results['checks'].append({
                'name': 'Electoral Configuration',
                'status': 'fail',
                'message': f'Error: {str(e)}'
            })
        
        # Check 5: Formularios
        try:
            formularios_count = FormularioE14.query.count()
            formularios_by_estado = db.session.query(
                FormularioE14.estado, db.func.count(FormularioE14.id)
            ).group_by(FormularioE14.estado).all()
            
            audit_results['checks'].append({
                'name': 'Formularios E-14',
                'status': 'pass',
                'message': f'Total: {formularios_count} formularios',
                'details': {estado: count for estado, count in formularios_by_estado}
            })
        except Exception as e:
            audit_results['checks'].append({
                'name': 'Formularios E-14',
                'status': 'fail',
                'message': f'Error: {str(e)}'
            })
        
        # Check 6: Incidentes y Delitos
        try:
            incidentes_count = IncidenteElectoral.query.count()
            delitos_count = DelitoElectoral.query.count()
            
            audit_results['checks'].append({
                'name': 'Incidents & Crimes',
                'status': 'pass',
                'message': 'Sistema de incidentes OK',
                'details': {
                    'incidentes': incidentes_count,
                    'delitos': delitos_count
                }
            })
        except Exception as e:
            audit_results['checks'].append({
                'name': 'Incidents & Crimes',
                'status': 'fail',
                'message': f'Error: {str(e)}'
            })
        
        # Check 7: Campañas
        try:
            from backend.models.configuracion_electoral import Campana
            
            campanas_count = Campana.query.count()
            campana_activa = Campana.query.filter_by(activa=True).first()
            
            audit_results['checks'].append({
                'name': 'Campaigns',
                'status': 'pass',
                'message': f'Total: {campanas_count} campañas',
                'details': {
                    'total': campanas_count,
                    'activa': campana_activa.nombre if campana_activa else 'Ninguna'
                }
            })
        except Exception as e:
            audit_results['checks'].append({
                'name': 'Campaigns',
                'status': 'fail',
                'message': f'Error: {str(e)}'
            })
        
        # Determinar estado general
        failed_checks = [c for c in audit_results['checks'] if c['status'] == 'fail']
        if failed_checks:
            audit_results['status'] = 'warning'
            audit_results['message'] = f'{len(failed_checks)} checks fallidos'
        else:
            audit_results['message'] = 'Todos los checks pasaron exitosamente'
        
        return jsonify({
            'success': True,
            'data': audit_results
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/audit-logs', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_audit_logs():
    """
    Obtener logs de auditoría del sistema
    """
    try:
        # Intentar obtener logs de la tabla AuditLog si existe
        try:
            from backend.models.coordinador_municipal import AuditLog
            
            limit = request.args.get('limit', 100, type=int)
            
            logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(limit).all()
            
            logs_data = []
            for log in logs:
                user = User.query.get(log.user_id)
                logs_data.append({
                    'id': log.id,
                    'user_id': log.user_id,
                    'user_nombre': user.nombre if user else 'Usuario eliminado',
                    'accion': log.accion,
                    'recurso': log.recurso,
                    'recurso_id': log.recurso_id,
                    'detalles': log.detalles,
                    'ip_address': log.ip_address,
                    'user_agent': log.user_agent,
                    'created_at': log.created_at.isoformat() if log.created_at else None
                })
            
            return jsonify({
                'success': True,
                'data': logs_data
            }), 200
            
        except ImportError:
            # Si no existe el modelo, devolver mensaje
            return jsonify({
                'success': True,
                'data': [],
                'message': 'Sistema de auditoría no configurado'
            }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/incidentes-delitos', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_incidentes_delitos_admin():
    """
    Obtener todos los incidentes y delitos del sistema con información completa
    """
    try:
        from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
        
        # Obtener incidentes
        incidentes = IncidenteElectoral.query.order_by(IncidenteElectoral.fecha_reporte.desc()).limit(50).all()
        
        incidentes_data = []
        for inc in incidentes:
            reportante = User.query.get(inc.reportado_por)
            mesa = Location.query.get(inc.mesa_id) if inc.mesa_id else None
            
            # Obtener ubicación completa
            ubicacion_completa = 'N/A'
            if mesa:
                puesto = Location.query.filter_by(
                    tipo='puesto',
                    departamento_codigo=mesa.departamento_codigo,
                    municipio_codigo=mesa.municipio_codigo,
                    zona_codigo=mesa.zona_codigo,
                    puesto_codigo=mesa.puesto_codigo
                ).first()
                
                municipio = Location.query.filter_by(
                    tipo='municipio',
                    departamento_codigo=mesa.departamento_codigo,
                    municipio_codigo=mesa.municipio_codigo
                ).first()
                
                departamento = Location.query.filter_by(
                    tipo='departamento',
                    departamento_codigo=mesa.departamento_codigo
                ).first()
                
                ubicacion_completa = f"{departamento.departamento_nombre if departamento else 'N/A'} > {municipio.municipio_nombre if municipio else 'N/A'} > {puesto.puesto_nombre if puesto else 'N/A'} > Mesa {mesa.mesa_codigo}"
            
            incidentes_data.append({
                'id': inc.id,
                'tipo': 'incidente',
                'titulo': inc.titulo,
                'descripcion': inc.descripcion,
                'tipo_incidente': inc.tipo_incidente,
                'severidad': inc.severidad,
                'estado': inc.estado,
                'reportado_por': reportante.nombre if reportante else 'Usuario eliminado',
                'reportado_por_rol': reportante.rol if reportante else 'N/A',
                'ubicacion': ubicacion_completa,
                'mesa_codigo': mesa.mesa_codigo if mesa else 'N/A',
                'fecha_reporte': inc.fecha_reporte.isoformat() if inc.fecha_reporte else None,
                'notas_resolucion': inc.notas_resolucion
            })
        
        # Obtener delitos
        delitos = DelitoElectoral.query.order_by(DelitoElectoral.fecha_reporte.desc()).limit(50).all()
        
        delitos_data = []
        for delito in delitos:
            reportante = User.query.get(delito.reportado_por)
            mesa = Location.query.get(delito.mesa_id) if delito.mesa_id else None
            
            # Obtener ubicación completa
            ubicacion_completa = 'N/A'
            if mesa:
                puesto = Location.query.filter_by(
                    tipo='puesto',
                    departamento_codigo=mesa.departamento_codigo,
                    municipio_codigo=mesa.municipio_codigo,
                    zona_codigo=mesa.zona_codigo,
                    puesto_codigo=mesa.puesto_codigo
                ).first()
                
                municipio = Location.query.filter_by(
                    tipo='municipio',
                    departamento_codigo=mesa.departamento_codigo,
                    municipio_codigo=mesa.municipio_codigo
                ).first()
                
                departamento = Location.query.filter_by(
                    tipo='departamento',
                    departamento_codigo=mesa.departamento_codigo
                ).first()
                
                ubicacion_completa = f"{departamento.departamento_nombre if departamento else 'N/A'} > {municipio.municipio_nombre if municipio else 'N/A'} > {puesto.puesto_nombre if puesto else 'N/A'} > Mesa {mesa.mesa_codigo}"
            
            delitos_data.append({
                'id': delito.id,
                'tipo': 'delito',
                'titulo': delito.titulo,
                'descripcion': delito.descripcion,
                'tipo_delito': delito.tipo_delito,
                'gravedad': delito.gravedad,
                'estado': delito.estado,
                'reportado_por': reportante.nombre if reportante else 'Usuario eliminado',
                'reportado_por_rol': reportante.rol if reportante else 'N/A',
                'ubicacion': ubicacion_completa,
                'mesa_codigo': mesa.mesa_codigo if mesa else 'N/A',
                'fecha_reporte': delito.fecha_reporte.isoformat() if delito.fecha_reporte else None,
                'denunciado_formalmente': delito.denunciado_formalmente,
                'resultado_investigacion': delito.resultado_investigacion
            })
        
        return jsonify({
            'success': True,
            'data': {
                'incidentes': incidentes_data,
                'delitos': delitos_data,
                'total_incidentes': len(incidentes_data),
                'total_delitos': len(delitos_data)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ENDPOINTS DE UBICACIONES (DIVIPOLA) - SOLO CAQUETÁ
# ============================================================================

@super_admin_bp.route('/locations/departamentos', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_departamentos():
    """
    Obtener departamento de Caquetá únicamente
    """
    try:
        from backend.database import db
        from backend.models.location import Location
        
        # Solo retornar Caquetá (código 44)
        departamento = db.session.query(Location).filter(
            Location.tipo == 'departamento',
            Location.departamento_codigo == '44'
        ).first()
        
        if departamento:
            return jsonify({
                'success': True,
                'data': [{
                    'departamento_codigo': departamento.departamento_codigo,
                    'departamento_nombre': departamento.departamento_nombre
                }]
            })
        else:
            return jsonify({
                'success': True,
                'data': []
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/locations/municipios/<departamento_codigo>', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_municipios(departamento_codigo):
    """
    Obtener municipios de un departamento
    """
    try:
        from backend.database import db
        from backend.models.location import Location
        
        municipios = db.session.query(Location).filter(
            Location.tipo == 'municipio',
            Location.departamento_codigo == departamento_codigo
        ).order_by(Location.municipio_nombre).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'municipio_codigo': muni.municipio_codigo,
                'municipio_nombre': muni.municipio_nombre
            } for muni in municipios]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/locations/zonas/<municipio_codigo>', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_zonas(municipio_codigo):
    """
    Obtener zonas de un municipio
    """
    try:
        from backend.database import db
        from backend.models.location import Location
        
        zonas = db.session.query(Location).filter(
            Location.tipo == 'zona',
            Location.municipio_codigo == municipio_codigo
        ).order_by(Location.zona_codigo).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'zona_codigo': zona.zona_codigo,
                'zona_nombre': f"Zona {zona.zona_codigo}"
            } for zona in zonas]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/locations/puestos/<zona_codigo>', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_puestos(zona_codigo):
    """
    Obtener puestos de una zona
    """
    try:
        from backend.database import db
        from backend.models.location import Location
        
        puestos = db.session.query(Location).filter(
            Location.tipo == 'puesto',
            Location.zona_codigo == zona_codigo
        ).order_by(Location.puesto_nombre).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'puesto_codigo': puesto.puesto_codigo,
                'puesto_nombre': puesto.puesto_nombre
            } for puesto in puestos]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/locations/mesas/<puesto_codigo>', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_mesas(puesto_codigo):
    """
    Obtener mesas de un puesto de Caquetá
    """
    try:
        from backend.database import db
        from backend.models.location import Location
        
        mesas = db.session.query(Location).filter(
            Location.tipo == 'mesa',
            Location.departamento_codigo == '44',
            Location.puesto_codigo == puesto_codigo
        ).order_by(Location.mesa_codigo).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'mesa_codigo': mesa.mesa_codigo,
                'mesa_nombre': mesa.mesa_nombre
            } for mesa in mesas]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ENDPOINTS PARA OBTENER DATOS (GET)
# ============================================================================

@super_admin_bp.route('/partidos', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_partidos():
    """
    Obtener todos los partidos políticos
    """
    try:
        from backend.models.partido_politico import PartidoPolitico as Partido
        
        partidos = Partido.query.order_by(Partido.orden, Partido.nombre).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'id': p.id,
                'sigla': p.sigla,
                'nombre': p.nombre,
                'color': p.color,
                'logo_url': p.logo_url,
                'descripcion': p.descripcion,
                'activo': p.activo,
                'orden': p.orden
            } for p in partidos]
        }), 200
        
    except Exception as e:
        print(f"Error en get_partidos: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/candidatos', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_candidatos():
    """
    Obtener todos los candidatos
    """
    try:
        from backend.models.configuracion_electoral import TipoEleccion
        from backend.models.partido_politico import PartidoPolitico as Partido
        from backend.models.candidato import Candidato
        
        candidatos = Candidato.query.order_by(Candidato.nombre_completo).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'id': c.id,
                'codigo': c.codigo,
                'nombre_completo': c.nombre_completo,
                'numero_lista': c.numero_lista,
                'partido_id': c.partido_id,
                'partido_nombre': c.partido.nombre if c.partido else None,
                'tipo_eleccion_id': c.tipo_eleccion_id,
                'tipo_eleccion_nombre': c.tipo_eleccion.nombre if c.tipo_eleccion else None,
                'foto_url': c.foto_url,
                'es_independiente': c.es_independiente,
                'es_cabeza_lista': c.es_cabeza_lista,
                'activo': c.activo,
                'orden': c.orden
            } for c in candidatos]
        }), 200
        
    except Exception as e:
        print(f"Error en get_candidatos: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ENDPOINT PARA ACTUALIZAR DATOS EDITABLES DE UBICACIONES
# ============================================================================

@super_admin_bp.route('/locations/mesa/<int:mesa_id>', methods=['PUT'])
@jwt_required()
@role_required(['super_admin'])
def update_mesa_votantes(mesa_id):
    """
    Actualizar solo los campos editables de una mesa:
    - total_votantes_registrados
    - mujeres
    - hombres
    
    Los datos de DIVIPOLA (códigos, nombres) son fijos y no se pueden editar
    """
    try:
        from backend.database import db
        from backend.models.location import Location
        
        mesa = Location.query.get(mesa_id)
        
        if not mesa:
            return jsonify({
                'success': False,
                'error': 'Mesa no encontrada'
            }), 404
        
        if mesa.tipo != 'mesa':
            return jsonify({
                'success': False,
                'error': 'Solo se pueden editar mesas'
            }), 400
        
        data = request.get_json()
        
        # Solo permitir actualizar campos específicos
        campos_editables = ['total_votantes_registrados', 'mujeres', 'hombres']
        
        for campo in campos_editables:
            if campo in data:
                valor = data[campo]
                if valor is not None and valor >= 0:
                    setattr(mesa, campo, valor)
        
        # Validar que la suma de hombres y mujeres no exceda el total
        if mesa.hombres + mesa.mujeres > mesa.total_votantes_registrados:
            return jsonify({
                'success': False,
                'error': 'La suma de hombres y mujeres no puede exceder el total de votantes'
            }), 400
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Mesa actualizada correctamente',
            'data': mesa.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error actualizando mesa: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/locations/mesa/<int:mesa_id>', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_mesa_detalle(mesa_id):
    """
    Obtener detalles de una mesa específica
    """
    try:
        from backend.models.location import Location
        
        mesa = Location.query.get(mesa_id)
        
        if not mesa:
            return jsonify({
                'success': False,
                'error': 'Mesa no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'data': mesa.to_dict()
        }), 200
        
    except Exception as e:
        print(f"Error obteniendo mesa: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ENDPOINT PARA INICIALIZAR DATOS DE PRUEBA
# ============================================================================

@super_admin_bp.route('/init-test-data', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def init_test_data():
    """
    Inicializar datos de prueba para el sistema
    Crea tipos de elección, partidos y candidatos de ejemplo
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import TipoEleccion
        from backend.models.partido_politico import PartidoPolitico as Partido
        from backend.models.candidato import Candidato
        
        results = {
            'tipos_eleccion': {'created': 0, 'existing': 0},
            'partidos': {'created': 0, 'existing': 0},
            'candidatos': {'created': 0, 'existing': 0}
        }
        
        # ========== TIPOS DE ELECCIÓN ==========
        tipos = [
            {
                'codigo': 'PRES',
                'nombre': 'Presidencia',
                'descripcion': 'Elección de Presidente y Vicepresidente',
                'es_uninominal': True,
                'permite_lista_cerrada': False,
                'permite_lista_abierta': False,
                'permite_coaliciones': True,
                'activo': True
            },
            {
                'codigo': 'SENADO',
                'nombre': 'Senado',
                'descripcion': 'Elección de Senadores',
                'es_uninominal': False,
                'permite_lista_cerrada': True,
                'permite_lista_abierta': True,
                'permite_coaliciones': True,
                'activo': True
            },
            {
                'codigo': 'CAMARA',
                'nombre': 'Cámara de Representantes',
                'descripcion': 'Elección de Representantes a la Cámara',
                'es_uninominal': False,
                'permite_lista_cerrada': True,
                'permite_lista_abierta': True,
                'permite_coaliciones': True,
                'activo': True
            },
            {
                'codigo': 'GOB',
                'nombre': 'Gobernación',
                'descripcion': 'Elección de Gobernador',
                'es_uninominal': True,
                'permite_lista_cerrada': False,
                'permite_lista_abierta': False,
                'permite_coaliciones': True,
                'activo': True
            },
            {
                'codigo': 'ASAMBLEA',
                'nombre': 'Asamblea Departamental',
                'descripcion': 'Elección de Diputados a la Asamblea',
                'es_uninominal': False,
                'permite_lista_cerrada': True,
                'permite_lista_abierta': True,
                'permite_coaliciones': True,
                'activo': True
            },
            {
                'codigo': 'ALCALDIA',
                'nombre': 'Alcaldía',
                'descripcion': 'Elección de Alcalde',
                'es_uninominal': True,
                'permite_lista_cerrada': False,
                'permite_lista_abierta': False,
                'permite_coaliciones': True,
                'activo': True
            },
            {
                'codigo': 'CONCEJO',
                'nombre': 'Concejo Municipal',
                'descripcion': 'Elección de Concejales',
                'es_uninominal': False,
                'permite_lista_cerrada': True,
                'permite_lista_abierta': True,
                'permite_coaliciones': True,
                'activo': True
            }
        ]
        
        for tipo_data in tipos:
            existing = TipoEleccion.query.filter_by(codigo=tipo_data['codigo']).first()
            if not existing:
                tipo = TipoEleccion(**tipo_data)
                db.session.add(tipo)
                results['tipos_eleccion']['created'] += 1
            else:
                results['tipos_eleccion']['existing'] += 1
        
        db.session.commit()
        
        # ========== PARTIDOS POLÍTICOS ==========
        partidos = [
            {
                'codigo': 'LIBERAL',
                'nombre': 'Partido Liberal Colombiano',
                'nombre_corto': 'Liberal',
                'color': '#FF0000',
                'activo': True,
                'orden': 1
            },
            {
                'codigo': 'CONSERVADOR',
                'nombre': 'Partido Conservador Colombiano',
                'nombre_corto': 'Conservador',
                'color': '#0000FF',
                'activo': True,
                'orden': 2
            },
            {
                'codigo': 'VERDE',
                'nombre': 'Alianza Verde',
                'nombre_corto': 'Verde',
                'color': '#00FF00',
                'activo': True,
                'orden': 3
            },
            {
                'codigo': 'CENTRO_DEM',
                'nombre': 'Centro Democrático',
                'nombre_corto': 'Centro Democrático',
                'color': '#0080FF',
                'activo': True,
                'orden': 4
            },
            {
                'codigo': 'CAMBIO_RADICAL',
                'nombre': 'Cambio Radical',
                'nombre_corto': 'Cambio Radical',
                'color': '#FFA500',
                'activo': True,
                'orden': 5
            },
            {
                'codigo': 'POLO',
                'nombre': 'Polo Democrático Alternativo',
                'nombre_corto': 'Polo',
                'color': '#FFFF00',
                'activo': True,
                'orden': 6
            },
            {
                'codigo': 'PACTO_HISTORICO',
                'nombre': 'Pacto Histórico',
                'nombre_corto': 'Pacto Histórico',
                'color': '#FF1493',
                'activo': True,
                'orden': 7
            },
            {
                'codigo': 'U',
                'nombre': 'Partido de la U',
                'nombre_corto': 'La U',
                'color': '#808080',
                'activo': True,
                'orden': 8
            },
            {
                'codigo': 'MIRA',
                'nombre': 'Movimiento Independiente de Renovación Absoluta',
                'nombre_corto': 'MIRA',
                'color': '#800080',
                'activo': True,
                'orden': 9
            },
            {
                'codigo': 'COMUNES',
                'nombre': 'Comunes',
                'nombre_corto': 'Comunes',
                'color': '#8B0000',
                'activo': True,
                'orden': 10
            }
        ]
        
        for partido_data in partidos:
            # Usar sigla en lugar de codigo (el modelo no tiene codigo)
            sigla = partido_data.pop('codigo')  # Remover codigo y usarlo como sigla
            nombre_corto = partido_data.pop('nombre_corto', sigla)  # Remover nombre_corto si existe
            
            existing = Partido.query.filter_by(sigla=sigla).first()
            if not existing:
                partido = Partido(
                    sigla=sigla,
                    nombre=partido_data['nombre'],
                    color=partido_data['color'],
                    orden=partido_data.get('orden', 0),
                    activo=partido_data.get('activo', True)
                )
                db.session.add(partido)
                results['partidos']['created'] += 1
            else:
                results['partidos']['existing'] += 1
        
        db.session.commit()
        
        # ========== CANDIDATOS DE PRUEBA ==========
        tipo_pres = TipoEleccion.query.filter_by(codigo='PRES').first()
        tipo_senado = TipoEleccion.query.filter_by(codigo='SENADO').first()
        tipo_camara = TipoEleccion.query.filter_by(codigo='CAMARA').first()
        
        partido_liberal = Partido.query.filter_by(sigla='LIBERAL').first()
        partido_conservador = Partido.query.filter_by(sigla='CONSERVADOR').first()
        partido_verde = Partido.query.filter_by(sigla='VERDE').first()
        partido_centro_dem = Partido.query.filter_by(sigla='CENTRO_DEM').first()
        
        if all([tipo_pres, tipo_senado, tipo_camara, partido_liberal, partido_conservador, partido_verde, partido_centro_dem]):
            candidatos = [
                # Presidencia
                {
                    'codigo': 'PRES_LIB_001',
                    'nombre_completo': 'Juan Pérez García',
                    'partido_id': partido_liberal.id,
                    'tipo_eleccion_id': tipo_pres.id,
                    'es_independiente': False,
                    'es_cabeza_lista': True,
                    'activo': True,
                    'orden': 1
                },
                {
                    'codigo': 'PRES_CONS_001',
                    'nombre_completo': 'María González López',
                    'partido_id': partido_conservador.id,
                    'tipo_eleccion_id': tipo_pres.id,
                    'es_independiente': False,
                    'es_cabeza_lista': True,
                    'activo': True,
                    'orden': 2
                },
                # Senado
                {
                    'codigo': 'SEN_VERDE_001',
                    'nombre_completo': 'Carlos Rodríguez Martínez',
                    'partido_id': partido_verde.id,
                    'tipo_eleccion_id': tipo_senado.id,
                    'numero_lista': 1,
                    'es_independiente': False,
                    'es_cabeza_lista': True,
                    'activo': True,
                    'orden': 1
                },
                {
                    'codigo': 'SEN_VERDE_002',
                    'nombre_completo': 'Ana Martínez Sánchez',
                    'partido_id': partido_verde.id,
                    'tipo_eleccion_id': tipo_senado.id,
                    'numero_lista': 2,
                    'es_independiente': False,
                    'es_cabeza_lista': False,
                    'activo': True,
                    'orden': 2
                },
                # Cámara
                {
                    'codigo': 'CAM_CD_001',
                    'nombre_completo': 'Pedro Ramírez Torres',
                    'partido_id': partido_centro_dem.id,
                    'tipo_eleccion_id': tipo_camara.id,
                    'numero_lista': 1,
                    'es_independiente': False,
                    'es_cabeza_lista': True,
                    'activo': True,
                    'orden': 1
                },
                {
                    'codigo': 'CAM_CD_002',
                    'nombre_completo': 'Laura Fernández Díaz',
                    'partido_id': partido_centro_dem.id,
                    'tipo_eleccion_id': tipo_camara.id,
                    'numero_lista': 2,
                    'es_independiente': False,
                    'es_cabeza_lista': False,
                    'activo': True,
                    'orden': 2
                }
            ]
            
            for candidato_data in candidatos:
                existing = Candidato.query.filter_by(codigo=candidato_data['codigo']).first()
                if not existing:
                    candidato = Candidato(**candidato_data)
                    db.session.add(candidato)
                    results['candidatos']['created'] += 1
                else:
                    results['candidatos']['existing'] += 1
            
            db.session.commit()
        
        # Preparar mensaje de respuesta
        message_parts = []
        if results['tipos_eleccion']['created'] > 0:
            message_parts.append(f"{results['tipos_eleccion']['created']} tipos de elección creados")
        if results['partidos']['created'] > 0:
            message_parts.append(f"{results['partidos']['created']} partidos creados")
        if results['candidatos']['created'] > 0:
            message_parts.append(f"{results['candidatos']['created']} candidatos creados")
        
        if not message_parts:
            message = "Todos los datos ya existían en el sistema"
        else:
            message = "Datos inicializados: " + ", ".join(message_parts)
        
        return jsonify({
            'success': True,
            'message': message,
            'data': results
        }), 200
        
    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"Error inicializando datos: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/init-caqueta-data', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def init_caqueta_electoral_data():
    """
    Inicializar datos electorales realistas del Caquetá
    Basado en elecciones al Congreso 2022 y Asamblea 2023
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import TipoEleccion
        from backend.models.partido_politico import PartidoPolitico as Partido
        from backend.models.candidato import Candidato
        
        results = {
            'senado': {'created': 0, 'existing': 0},
            'camara': {'created': 0, 'existing': 0},
            'asamblea': {'created': 0, 'existing': 0}
        }
        
        # ========== SENADO 2022 ==========
        tipo_senado = TipoEleccion.query.filter_by(codigo='SENADO').first()
        
        if tipo_senado:
            candidatos_senado = [
                # PACTO HISTÓRICO
                {'partido': 'PACTO_HISTORICO', 'nombre': 'Gustavo Bolívar Moreno', 'numero': 1, 'cabeza': True},
                {'partido': 'PACTO_HISTORICO', 'nombre': 'María José Pizarro Rodríguez', 'numero': 2, 'cabeza': False},
                {'partido': 'PACTO_HISTORICO', 'nombre': 'Iván Cepeda Castro', 'numero': 3, 'cabeza': False},
                {'partido': 'PACTO_HISTORICO', 'nombre': 'Clara López Obregón', 'numero': 4, 'cabeza': False},
                {'partido': 'PACTO_HISTORICO', 'nombre': 'Alexander López Maya', 'numero': 5, 'cabeza': False},
                
                # PARTIDO LIBERAL
                {'partido': 'LIBERAL', 'nombre': 'Juan Fernando Cristo Bustos', 'numero': 1, 'cabeza': True},
                {'partido': 'LIBERAL', 'nombre': 'Alejandro Carlos Chacón Camargo', 'numero': 2, 'cabeza': False},
                {'partido': 'LIBERAL', 'nombre': 'Fabián Díaz Plata', 'numero': 3, 'cabeza': False},
                {'partido': 'LIBERAL', 'nombre': 'Horacio José Serpa Moncada', 'numero': 4, 'cabeza': False},
                
                # PARTIDO CONSERVADOR
                {'partido': 'CONSERVADOR', 'nombre': 'Efraín José Cepeda Sarabia', 'numero': 1, 'cabeza': True},
                {'partido': 'CONSERVADOR', 'nombre': 'Nora María García Burgos', 'numero': 2, 'cabeza': False},
                {'partido': 'CONSERVADOR', 'nombre': 'Omar de Jesús Restrepo Escobar', 'numero': 3, 'cabeza': False},
                {'partido': 'CONSERVADOR', 'nombre': 'Paola Andrea Holguín Moreno', 'numero': 4, 'cabeza': False},
                
                # CENTRO DEMOCRÁTICO
                {'partido': 'CENTRO_DEM', 'nombre': 'María Fernanda Cabal Molina', 'numero': 1, 'cabeza': True},
                {'partido': 'CENTRO_DEM', 'nombre': 'Paloma Susana Valencia Laserna', 'numero': 2, 'cabeza': False},
                {'partido': 'CENTRO_DEM', 'nombre': 'Miguel Uribe Turbay', 'numero': 3, 'cabeza': False},
                {'partido': 'CENTRO_DEM', 'nombre': 'Honorio Miguel Henríquez Pinedo', 'numero': 4, 'cabeza': False},
                
                # CAMBIO RADICAL
                {'partido': 'CAMBIO_RADICAL', 'nombre': 'Carlos Fernando Galán Pachón', 'numero': 1, 'cabeza': True},
                {'partido': 'CAMBIO_RADICAL', 'nombre': 'Angélica Lozano Correa', 'numero': 2, 'cabeza': False},
                {'partido': 'CAMBIO_RADICAL', 'nombre': 'Germán Varón Cotrino', 'numero': 3, 'cabeza': False},
                
                # ALIANZA VERDE
                {'partido': 'VERDE', 'nombre': 'Ariel Ávila Martínez', 'numero': 1, 'cabeza': True},
                {'partido': 'VERDE', 'nombre': 'Angélica Lozano Correa', 'numero': 2, 'cabeza': False},
                {'partido': 'VERDE', 'nombre': 'Antonio Sanguino Páez', 'numero': 3, 'cabeza': False},
                
                # PARTIDO DE LA U
                {'partido': 'U', 'nombre': 'Roy Leonardo Barreras Montealegre', 'numero': 1, 'cabeza': True},
                {'partido': 'U', 'nombre': 'Armando Benedetti Villaneda', 'numero': 2, 'cabeza': False},
                {'partido': 'U', 'nombre': 'Dilian Francisca Toro Torres', 'numero': 3, 'cabeza': False},
                
                # MIRA
                {'partido': 'MIRA', 'nombre': 'Carlos Alberto Baena López', 'numero': 1, 'cabeza': True},
                {'partido': 'MIRA', 'nombre': 'John Milton Rodríguez Rojas', 'numero': 2, 'cabeza': False},
                
                # COMUNES
                {'partido': 'COMUNES', 'nombre': 'Pablo Catatumbo Torres Victoria', 'numero': 1, 'cabeza': True},
                {'partido': 'COMUNES', 'nombre': 'Griselda Lobo Hernández', 'numero': 2, 'cabeza': False},
            ]
            
            for cand_data in candidatos_senado:
                partido = Partido.query.filter_by(codigo=cand_data['partido']).first()
                if not partido:
                    continue
                
                codigo = f"SEN_{cand_data['partido']}_{cand_data['numero']:03d}"
                existing = Candidato.query.filter_by(codigo=codigo).first()
                
                if not existing:
                    candidato = Candidato(
                        codigo=codigo,
                        nombre_completo=cand_data['nombre'],
                        partido_id=partido.id,
                        tipo_eleccion_id=tipo_senado.id,
                        numero_lista=cand_data['numero'],
                        es_independiente=False,
                        es_cabeza_lista=cand_data['cabeza'],
                        activo=True,
                        orden=cand_data['numero']
                    )
                    db.session.add(candidato)
                    results['senado']['created'] += 1
                else:
                    results['senado']['existing'] += 1
        
        db.session.commit()
        
        # ========== CÁMARA CAQUETÁ 2022 ==========
        tipo_camara = TipoEleccion.query.filter_by(codigo='CAMARA').first()
        
        if tipo_camara:
            candidatos_camara = [
                # PACTO HISTÓRICO
                {'partido': 'PACTO_HISTORICO', 'nombre': 'Jaime Raúl Salamanca Torres', 'numero': 1, 'cabeza': True},
                {'partido': 'PACTO_HISTORICO', 'nombre': 'María Fernanda Carrascal Triana', 'numero': 2, 'cabeza': False},
                
                # PARTIDO LIBERAL
                {'partido': 'LIBERAL', 'nombre': 'Hernán Penagos Giraldo', 'numero': 1, 'cabeza': True},
                {'partido': 'LIBERAL', 'nombre': 'Deyanira Ávila Pertuz', 'numero': 2, 'cabeza': False},
                {'partido': 'LIBERAL', 'nombre': 'Jorge Eliécer Guevara Bolaños', 'numero': 3, 'cabeza': False},
                
                # PARTIDO CONSERVADOR
                {'partido': 'CONSERVADOR', 'nombre': 'Atilano Alonso Giraldo Arango', 'numero': 1, 'cabeza': True},
                {'partido': 'CONSERVADOR', 'nombre': 'Luz Marina Bernal Parra', 'numero': 2, 'cabeza': False},
                
                # CENTRO DEMOCRÁTICO
                {'partido': 'CENTRO_DEM', 'nombre': 'Alfredo Guillermo Molina Triana', 'numero': 1, 'cabeza': True},
                {'partido': 'CENTRO_DEM', 'nombre': 'Sandra Milena Ramírez Loaiza', 'numero': 2, 'cabeza': False},
                {'partido': 'CENTRO_DEM', 'nombre': 'Hernán Gustavo Estupiñán Calvache', 'numero': 3, 'cabeza': False},
                
                # CAMBIO RADICAL
                {'partido': 'CAMBIO_RADICAL', 'nombre': 'Rodrigo Rojas Lara', 'numero': 1, 'cabeza': True},
                {'partido': 'CAMBIO_RADICAL', 'nombre': 'Yolanda González Hernández', 'numero': 2, 'cabeza': False},
                
                # ALIANZA VERDE
                {'partido': 'VERDE', 'nombre': 'Guillermo Rivera Flórez', 'numero': 1, 'cabeza': True},
                {'partido': 'VERDE', 'nombre': 'Ángela María Robledo Gómez', 'numero': 2, 'cabeza': False},
                
                # PARTIDO DE LA U
                {'partido': 'U', 'nombre': 'Óscar de Jesús Hurtado Pérez', 'numero': 1, 'cabeza': True},
                {'partido': 'U', 'nombre': 'Teresita García Romero', 'numero': 2, 'cabeza': False},
                
                # MIRA
                {'partido': 'MIRA', 'nombre': 'Wilmer Leal Pérez', 'numero': 1, 'cabeza': True},
                {'partido': 'MIRA', 'nombre': 'Gloria Stella Díaz Ortiz', 'numero': 2, 'cabeza': False},
                
                # COMUNES
                {'partido': 'COMUNES', 'nombre': 'Jairo Ernesto Cala Cala', 'numero': 1, 'cabeza': True},
                {'partido': 'COMUNES', 'nombre': 'Aida Quilcué Vivas', 'numero': 2, 'cabeza': False},
                
                # POLO DEMOCRÁTICO
                {'partido': 'POLO', 'nombre': 'Wilson Arias Castillo', 'numero': 1, 'cabeza': True},
                {'partido': 'POLO', 'nombre': 'Clara Eugenia López Obregón', 'numero': 2, 'cabeza': False},
            ]
            
            for cand_data in candidatos_camara:
                partido = Partido.query.filter_by(codigo=cand_data['partido']).first()
                if not partido:
                    continue
                
                codigo = f"CAM_CAQ_{cand_data['partido']}_{cand_data['numero']:03d}"
                existing = Candidato.query.filter_by(codigo=codigo).first()
                
                if not existing:
                    candidato = Candidato(
                        codigo=codigo,
                        nombre_completo=cand_data['nombre'],
                        partido_id=partido.id,
                        tipo_eleccion_id=tipo_camara.id,
                        numero_lista=cand_data['numero'],
                        es_independiente=False,
                        es_cabeza_lista=cand_data['cabeza'],
                        activo=True,
                        orden=cand_data['numero']
                    )
                    db.session.add(candidato)
                    results['camara']['created'] += 1
                else:
                    results['camara']['existing'] += 1
        
        db.session.commit()
        
        # ========== ASAMBLEA CAQUETÁ 2023 ==========
        tipo_asamblea = TipoEleccion.query.filter_by(codigo='ASAMBLEA').first()
        
        if tipo_asamblea:
            candidatos_asamblea = [
                # PARTIDO LIBERAL
                {'partido': 'LIBERAL', 'nombre': 'Luis Eduardo Arango Jiménez', 'numero': 1, 'cabeza': True},
                {'partido': 'LIBERAL', 'nombre': 'María Cristina Lesmes Duque', 'numero': 2, 'cabeza': False},
                {'partido': 'LIBERAL', 'nombre': 'José Aldemar Rojas Rodríguez', 'numero': 3, 'cabeza': False},
                {'partido': 'LIBERAL', 'nombre': 'Sandra Milena Ortiz Cuéllar', 'numero': 4, 'cabeza': False},
                
                # PARTIDO CONSERVADOR
                {'partido': 'CONSERVADOR', 'nombre': 'Arnulfo Sánchez Motta', 'numero': 1, 'cabeza': True},
                {'partido': 'CONSERVADOR', 'nombre': 'Blanca Cecilia Gómez Ángel', 'numero': 2, 'cabeza': False},
                {'partido': 'CONSERVADOR', 'nombre': 'Héctor Fabio Useche Berdugo', 'numero': 3, 'cabeza': False},
                
                # PACTO HISTÓRICO
                {'partido': 'PACTO_HISTORICO', 'nombre': 'Fabio Amín Saleme Cruz', 'numero': 1, 'cabeza': True},
                {'partido': 'PACTO_HISTORICO', 'nombre': 'Yolanda Perea Mosquera', 'numero': 2, 'cabeza': False},
                {'partido': 'PACTO_HISTORICO', 'nombre': 'Carlos Andrés Amaya Rodríguez', 'numero': 3, 'cabeza': False},
                
                # CENTRO DEMOCRÁTICO
                {'partido': 'CENTRO_DEM', 'nombre': 'Álvaro Hernán Prada Artunduaga', 'numero': 1, 'cabeza': True},
                {'partido': 'CENTRO_DEM', 'nombre': 'Martha Lucía Ramírez Blanco', 'numero': 2, 'cabeza': False},
                {'partido': 'CENTRO_DEM', 'nombre': 'Diego Fernando Molano Aponte', 'numero': 3, 'cabeza': False},
                
                # CAMBIO RADICAL
                {'partido': 'CAMBIO_RADICAL', 'nombre': 'Germán Alcides Blanco Álvarez', 'numero': 1, 'cabeza': True},
                {'partido': 'CAMBIO_RADICAL', 'nombre': 'Claudia Patricia Jiménez Sánchez', 'numero': 2, 'cabeza': False},
                
                # ALIANZA VERDE
                {'partido': 'VERDE', 'nombre': 'Jorge Iván Ospina Gómez', 'numero': 1, 'cabeza': True},
                {'partido': 'VERDE', 'nombre': 'Catalina Ortiz Lalinde', 'numero': 2, 'cabeza': False},
                
                # PARTIDO DE LA U
                {'partido': 'U', 'nombre': 'Juan Carlos Losada Vargas', 'numero': 1, 'cabeza': True},
                {'partido': 'U', 'nombre': 'Adriana Matiz Vargas', 'numero': 2, 'cabeza': False},
                
                # MIRA
                {'partido': 'MIRA', 'nombre': 'Carlos Eduardo Guevara Villabón', 'numero': 1, 'cabeza': True},
                {'partido': 'MIRA', 'nombre': 'Doris Amanda Rodríguez Moreno', 'numero': 2, 'cabeza': False},
            ]
            
            for cand_data in candidatos_asamblea:
                partido = Partido.query.filter_by(codigo=cand_data['partido']).first()
                if not partido:
                    continue
                
                codigo = f"ASA_CAQ_{cand_data['partido']}_{cand_data['numero']:03d}"
                existing = Candidato.query.filter_by(codigo=codigo).first()
                
                if not existing:
                    candidato = Candidato(
                        codigo=codigo,
                        nombre_completo=cand_data['nombre'],
                        partido_id=partido.id,
                        tipo_eleccion_id=tipo_asamblea.id,
                        numero_lista=cand_data['numero'],
                        es_independiente=False,
                        es_cabeza_lista=cand_data['cabeza'],
                        activo=True,
                        orden=cand_data['numero']
                    )
                    db.session.add(candidato)
                    results['asamblea']['created'] += 1
                else:
                    results['asamblea']['existing'] += 1
        
        db.session.commit()
        
        # Preparar mensaje de respuesta
        total_created = results['senado']['created'] + results['camara']['created'] + results['asamblea']['created']
        total_existing = results['senado']['existing'] + results['camara']['existing'] + results['asamblea']['existing']
        
        message_parts = []
        if results['senado']['created'] > 0:
            message_parts.append(f"{results['senado']['created']} candidatos al Senado")
        if results['camara']['created'] > 0:
            message_parts.append(f"{results['camara']['created']} candidatos a la Cámara")
        if results['asamblea']['created'] > 0:
            message_parts.append(f"{results['asamblea']['created']} candidatos a la Asamblea")
        
        if not message_parts:
            message = "Todos los candidatos del Caquetá ya existían en el sistema"
        else:
            message = f"Datos del Caquetá inicializados: {', '.join(message_parts)}"
        
        return jsonify({
            'success': True,
            'message': message,
            'data': {
                'total_created': total_created,
                'total_existing': total_existing,
                'details': results
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"Error inicializando datos del Caquetá: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



# ============================================
# CARGA MASIVA CSV - SISTEMA ELECTORAL
# ============================================

@super_admin_bp.route('/bulk-upload/validate-csv', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def validate_csv_upload():
    """
    Validar archivo CSV antes de cargar
    
    Parámetros:
    - file: Archivo CSV
    - type: Tipo de carga (partidos, candidatos_uninominal, candidatos_lista_cerrada, etc.)
    - config: Configuración JSON con parámetros adicionales
    """
    try:
        import pandas as pd
        from io import StringIO
        
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó ningún archivo'
            }), 400
        
        file = request.files['file']
        upload_type = request.form.get('type')
        config = request.form.get('config', '{}')
        
        if not upload_type:
            return jsonify({
                'success': False,
                'error': 'Tipo de carga no especificado'
            }), 400
        
        # Leer CSV
        try:
            content = file.read().decode('utf-8')
            df = pd.read_csv(StringIO(content))
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error leyendo CSV: {str(e)}'
            }), 400
        
        # Validar según tipo
        validation_result = validate_csv_by_type(df, upload_type, config)
        
        return jsonify({
            'success': True,
            'data': validation_result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/bulk-upload/upload-csv', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def upload_csv_data():
    """
    Cargar datos masivamente desde CSV
    
    Parámetros:
    - file: Archivo CSV
    - type: Tipo de carga
    - config: Configuración JSON
    """
    try:
        from backend.database import db
        import pandas as pd
        from io import StringIO
        import json
        
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó ningún archivo'
            }), 400
        
        file = request.files['file']
        upload_type = request.form.get('type')
        config_str = request.form.get('config', '{}')
        config = json.loads(config_str)
        
        # Leer CSV
        content = file.read().decode('utf-8')
        df = pd.read_csv(StringIO(content))
        
        # Procesar según tipo
        result = process_csv_by_type(df, upload_type, config)
        
        if result['success']:
            db.session.commit()
        else:
            db.session.rollback()
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/bulk-upload/config', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_upload_config():
    """
    Obtener configuración para carga masiva
    """
    try:
        from backend.models.configuracion_electoral import TipoEleccion
        from backend.models.location import Location
        
        # Obtener tipos de elección
        tipos_eleccion = TipoEleccion.query.filter_by(activo=True).all()
        
        # Obtener departamentos
        departamentos = Location.query.filter_by(tipo='departamento').all()
        
        return jsonify({
            'success': True,
            'data': {
                'tipos_eleccion': [{'id': t.id, 'nombre': t.nombre, 'codigo': t.codigo} for t in tipos_eleccion],
                'departamentos': [{'codigo': d.departamento_codigo, 'nombre': d.nombre} for d in departamentos]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/bulk-upload/municipios/<dept_codigo>', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_municipios_for_upload(dept_codigo):
    """
    Obtener municipios de un departamento para carga masiva
    """
    try:
        from backend.models.location import Location
        
        municipios = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo=dept_codigo
        ).all()
        
        return jsonify({
            'success': True,
            'data': [{'codigo': m.municipio_codigo, 'nombre': m.nombre} for m in municipios]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def validate_csv_by_type(df, upload_type, config):
    """
    Validar CSV según el tipo de carga
    """
    warnings = []
    errors = []
    records = len(df)
    
    # Validaciones por tipo
    if upload_type == 'partidos':
        required_cols = ['codigo', 'nombre', 'nombre_corto', 'color']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            errors.append(f"Faltan columnas requeridas: {', '.join(missing_cols)}")
        else:
            # Validar códigos únicos
            duplicates = df[df.duplicated('codigo', keep=False)]
            if not duplicates.empty:
                errors.append(f"Códigos duplicados en filas: {duplicates.index.tolist()}")
            
            # Validar colores hexadecimales
            import re
            for idx, row in df.iterrows():
                if not re.match(r'^#[0-9A-Fa-f]{6}$', str(row['color'])):
                    errors.append(f"Línea {idx + 2}: Color inválido '{row['color']}'")
    
    elif upload_type in ['candidatos_uninominal', 'candidatos_lista_cerrada', 'candidatos_lista_abierta']:
        required_cols = ['partido_codigo', 'candidato_nombre', 'candidato_cedula']
        
        if upload_type in ['candidatos_lista_cerrada', 'candidatos_lista_abierta']:
            required_cols.extend(['numero_lista', 'es_cabeza_lista'])
        
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            errors.append(f"Faltan columnas requeridas: {', '.join(missing_cols)}")
        else:
            # Validar partidos existen
            from backend.models.partido_politico import PartidoPolitico as Partido
            partidos_unicos = df['partido_codigo'].unique()
            
            for partido_codigo in partidos_unicos:
                partido = Partido.query.filter_by(codigo=partido_codigo).first()
                if not partido:
                    warnings.append(f"Partido '{partido_codigo}' no existe (se puede crear)")
            
            # Validar cédulas únicas
            duplicates = df[df.duplicated('candidato_cedula', keep=False)]
            if not duplicates.empty:
                errors.append(f"Cédulas duplicadas en filas: {duplicates.index.tolist()}")
            
            # Validar números de lista únicos por partido (si aplica)
            if upload_type in ['candidatos_lista_cerrada', 'candidatos_lista_abierta']:
                for partido_codigo in partidos_unicos:
                    partido_df = df[df['partido_codigo'] == partido_codigo]
                    duplicates = partido_df[partido_df.duplicated('numero_lista', keep=False)]
                    if not duplicates.empty:
                        warnings.append(f"Partido '{partido_codigo}': números de lista duplicados")
                    
                    # Validar solo un cabeza de lista por partido
                    cabezas = partido_df[partido_df['es_cabeza_lista'] == True]
                    if len(cabezas) > 1:
                        errors.append(f"Partido '{partido_codigo}': múltiples cabezas de lista")
                    elif len(cabezas) == 0:
                        warnings.append(f"Partido '{partido_codigo}': sin cabeza de lista")
    
    elif upload_type == 'coaliciones':
        required_cols = ['coalicion_nombre', 'partido_codigo', 'partido_nombre']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            errors.append(f"Faltan columnas requeridas: {', '.join(missing_cols)}")
        else:
            # Validar partidos existen
            from backend.models.partido_politico import PartidoPolitico as Partido
            for idx, row in df.iterrows():
                partido = Partido.query.filter_by(codigo=row['partido_codigo']).first()
                if not partido:
                    errors.append(f"Línea {idx + 2}: Partido '{row['partido_codigo']}' no existe")
    
    elif upload_type == 'ubicaciones':
        required_cols = ['departamento_codigo', 'departamento_nombre', 'municipio_codigo', 'municipio_nombre']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            errors.append(f"Faltan columnas requeridas: {', '.join(missing_cols)}")
        else:
            # Validar coordenadas si existen
            if 'latitud' in df.columns and 'longitud' in df.columns:
                for idx, row in df.iterrows():
                    try:
                        if pd.notna(row['latitud']):
                            lat = float(row['latitud'])
                            if lat < -90 or lat > 90:
                                errors.append(f"Línea {idx + 2}: Latitud inválida")
                        if pd.notna(row['longitud']):
                            lon = float(row['longitud'])
                            if lon < -180 or lon > 180:
                                errors.append(f"Línea {idx + 2}: Longitud inválida")
                    except:
                        errors.append(f"Línea {idx + 2}: Coordenadas inválidas")
    
    return {
        'records': records,
        'warnings': warnings,
        'errors': errors,
        'valid': len(errors) == 0
    }


def process_csv_by_type(df, upload_type, config):
    """
    Procesar CSV según el tipo de carga
    """
    from backend.database import db
    from backend.models.configuracion_electoral import TipoEleccion
    from backend.models.partido_politico import PartidoPolitico as Partido
    from backend.models.candidato import Candidato
    from backend.models.location import Location
    
    created = []
    updated = []
    errors = []
    
    try:
        if upload_type == 'partidos':
            for idx, row in df.iterrows():
                try:
                    # Verificar si existe
                    partido = Partido.query.filter_by(codigo=row['codigo']).first()
                    
                    if partido and config.get('overwrite'):
                        # Actualizar
                        partido.nombre = row['nombre']
                        partido.nombre_corto = row['nombre_corto']
                        partido.color = row['color']
                        if 'logo_url' in row and pd.notna(row['logo_url']):
                            partido.logo_url = row['logo_url']
                        updated.append(row['nombre'])
                    elif not partido:
                        # Crear
                        partido = Partido(
                            codigo=row['codigo'],
                            nombre=row['nombre'],
                            nombre_corto=row['nombre_corto'],
                            color=row['color'],
                            logo_url=row.get('logo_url') if 'logo_url' in row and pd.notna(row.get('logo_url')) else None,
                            activo=row.get('activo', True) if 'activo' in row else True
                        )
                        db.session.add(partido)
                        created.append(row['nombre'])
                except Exception as e:
                    errors.append(f"Línea {idx + 2}: {str(e)}")
        
        elif upload_type in ['candidatos_uninominal', 'candidatos_lista_cerrada', 'candidatos_lista_abierta']:
            # Obtener tipo de elección
            tipo_eleccion_id = config.get('tipoEleccion')
            if not tipo_eleccion_id:
                return {'success': False, 'error': 'Tipo de elección no especificado'}
            
            tipo_eleccion = TipoEleccion.query.get(tipo_eleccion_id)
            if not tipo_eleccion:
                return {'success': False, 'error': 'Tipo de elección no encontrado'}
            
            for idx, row in df.iterrows():
                try:
                    # Buscar o crear partido
                    partido = Partido.query.filter_by(codigo=row['partido_codigo']).first()
                    
                    if not partido:
                        if config.get('createParties'):
                            # Crear partido automáticamente
                            partido = Partido(
                                codigo=row['partido_codigo'],
                                nombre=row.get('partido_nombre', row['partido_codigo']),
                                nombre_corto=row['partido_codigo'],
                                color='#CCCCCC',
                                activo=True
                            )
                            db.session.add(partido)
                            db.session.flush()
                        else:
                            errors.append(f"Línea {idx + 2}: Partido '{row['partido_codigo']}' no existe")
                            continue
                    
                    # Generar código único
                    codigo = f"{tipo_eleccion.codigo}_{partido.codigo}_{row['candidato_cedula']}"
                    
                    # Verificar si existe
                    candidato = Candidato.query.filter_by(codigo=codigo).first()
                    
                    if candidato and config.get('overwrite'):
                        # Actualizar
                        candidato.nombre_completo = row['candidato_nombre']
                        if upload_type in ['candidatos_lista_cerrada', 'candidatos_lista_abierta']:
                            candidato.numero_lista = int(row['numero_lista'])
                            candidato.es_cabeza_lista = bool(row['es_cabeza_lista'])
                        updated.append(row['candidato_nombre'])
                    elif not candidato:
                        # Crear
                        candidato = Candidato(
                            codigo=codigo,
                            nombre_completo=row['candidato_nombre'],
                            partido_id=partido.id,
                            tipo_eleccion_id=tipo_eleccion.id,
                            numero_lista=int(row['numero_lista']) if upload_type in ['candidatos_lista_cerrada', 'candidatos_lista_abierta'] else None,
                            es_independiente=bool(row.get('es_independiente', False)),
                            es_cabeza_lista=bool(row.get('es_cabeza_lista', False)) if upload_type in ['candidatos_lista_cerrada', 'candidatos_lista_abierta'] else False,
                            foto_url=row.get('foto_url') if 'foto_url' in row and pd.notna(row.get('foto_url')) else None,
                            activo=True
                        )
                        db.session.add(candidato)
                        created.append(row['candidato_nombre'])
                except Exception as e:
                    errors.append(f"Línea {idx + 2}: {str(e)}")
        
        return {
            'success': True,
            'message': f'{len(created)} registros creados, {len(updated)} actualizados',
            'data': {
                'created': created,
                'updated': updated,
                'errors': errors,
                'total_created': len(created),
                'total_updated': len(updated),
                'total_errors': len(errors)
            }
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
