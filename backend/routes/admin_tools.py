"""
Rutas de herramientas administrativas
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.database import db
import os

admin_tools_bp = Blueprint('admin_tools', __name__, url_prefix='/api/admin')


@admin_tools_bp.route('/reset-database', methods=['POST'])
@jwt_required()
def reset_database():
    """
    Borrar la base de datos para forzar reinicialización
    Solo super_admin puede ejecutar esto
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'super_admin':
            return jsonify({
                'success': False,
                'error': 'Solo super_admin puede resetear la base de datos'
            }), 403
        
        # Cerrar todas las conexiones
        db.session.remove()
        db.engine.dispose()
        
        # Borrar el archivo de base de datos
        db_path = 'instance/electoral.db'
        if os.path.exists(db_path):
            os.remove(db_path)
            return jsonify({
                'success': True,
                'message': 'Base de datos borrada. La aplicación se reiniciará automáticamente.'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Archivo de base de datos no encontrado'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_tools_bp.route('/fix-passwords', methods=['POST'])
@jwt_required()
def fix_passwords():
    """
    Actualizar todas las contraseñas a texto plano sin borrar la BD
    Solo super_admin puede ejecutar esto
    """
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user or current_user.rol != 'super_admin':
            return jsonify({
                'success': False,
                'error': 'Solo super_admin puede actualizar contraseñas'
            }), 403
        
        # Mapeo de contraseñas por rol
        PASSWORDS = {
            'super_admin': 'SuperAdmin123!',
            'admin_departamental': 'AdminDept123!',
            'admin_municipal': 'AdminMuni123!',
            'coordinador_departamental': 'CoordDept123!',
            'coordinador_municipal': 'CoordMuni123!',
            'auditor_electoral': 'Auditor123!',
            'coordinador_puesto': 'CoordPuesto123!',
            'testigo_electoral': 'Testigo123!'
        }
        
        users = User.query.all()
        updated = 0
        
        for user in users:
            password = PASSWORDS.get(user.rol, 'test123')
            # Actualizar directamente sin usar set_password para asegurar texto plano
            user.password_hash = password
            updated += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{updated} contraseñas actualizadas a texto plano',
            'passwords': PASSWORDS
        }), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_tools_bp.route('/fix-roles', methods=['POST'])
@jwt_required()
def fix_roles():
    """
    Corregir roles de usuarios de prueba
    Solo super_admin puede ejecutar esto
    """
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user or current_user.rol != 'super_admin':
            return jsonify({
                'success': False,
                'error': 'Solo super_admin puede corregir roles'
            }), 403
        
        # Obtener TODOS los usuarios y corregir problemas comunes
        usuarios = User.query.all()
        
        resultados = []
        cambios_totales = 0
        
        for user in usuarios:
            cambios = []
            
            # Activar usuario si está inactivo
            if not user.activo:
                user.activo = True
                cambios.append("activado")
            
            # Resetear bloqueos
            if user.intentos_fallidos > 0:
                user.intentos_fallidos = 0
                cambios.append("intentos fallidos reseteados")
            
            if user.bloqueado_hasta:
                user.bloqueado_hasta = None
                cambios.append("desbloqueo de cuenta")
            
            # Verificar que la contraseña no esté hasheada (debe ser texto plano)
            # Si la contraseña tiene más de 50 caracteres, probablemente está hasheada
            if len(user.password_hash) > 50:
                # Asignar contraseña por defecto según rol
                password_por_rol = {
                    'super_admin': 'SuperAdmin123!',
                    'admin_departamental': 'AdminDept123!',
                    'admin_municipal': 'AdminMuni123!',
                    'coordinador_departamental': 'CoordDept123!',
                    'coordinador_municipal': 'CoordMuni123!',
                    'auditor_electoral': 'Auditor123!',
                    'coordinador_puesto': 'CoordPuesto123!',
                    'testigo_electoral': 'Testigo123!'
                }
                
                nueva_password = password_por_rol.get(user.rol, 'test123')
                user.password_hash = nueva_password
                cambios.append(f"contraseña actualizada a {nueva_password}")
            
            if cambios:
                resultados.append({
                    'usuario': user.nombre,
                    'rol': user.rol,
                    'cambios': cambios,
                    'status': 'corregido'
                })
                cambios_totales += len(cambios)
        
        # Guardar cambios
        if cambios_totales > 0:
            db.session.commit()
        
        # Resumen por rol
        resumen_roles = {}
        for user in usuarios:
            if user.rol not in resumen_roles:
                resumen_roles[user.rol] = 0
            resumen_roles[user.rol] += 1
        
        return jsonify({
            'success': True,
            'message': f'{cambios_totales} cambios aplicados en {len(usuarios)} usuarios',
            'resultados': resultados[:10],  # Solo mostrar primeros 10
            'total_usuarios': len(usuarios),
            'resumen_roles': resumen_roles,
            'importante': [
                'Todos los usuarios deben cerrar sesión',
                'Volver a iniciar sesión para obtener nuevos tokens JWT',
                'Los tokens antiguos tendrán roles incorrectos'
            ]
        }), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_tools_bp.route('/diagnostico', methods=['GET'])
@jwt_required()
def diagnostico():
    """
    Diagnóstico del sistema
    Solo super_admin puede ejecutar esto
    """
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user or current_user.rol != 'super_admin':
            return jsonify({
                'success': False,
                'error': 'Solo super_admin puede ver el diagnóstico'
            }), 403
        
        from sqlalchemy import func
        
        # Estadísticas generales
        total_usuarios = User.query.count()
        usuarios_activos = User.query.filter_by(activo=True).count()
        usuarios_bloqueados = User.query.filter(User.bloqueado_hasta.isnot(None)).count()
        
        # Usuarios por rol
        roles_count = db.session.query(
            User.rol, 
            func.count(User.id)
        ).group_by(User.rol).all()
        
        roles_dict = {rol: count for rol, count in roles_count}
        
        # Usuarios de prueba
        usuarios_prueba = []
        for nombre in ['admin', 'testigo', 'coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental']:
            user = User.query.filter_by(nombre=nombre).first()
            if user:
                usuarios_prueba.append({
                    'nombre': user.nombre,
                    'rol': user.rol,
                    'activo': user.activo,
                    'bloqueado': user.bloqueado_hasta is not None,
                    'presencia_verificada': user.presencia_verificada if user.rol == 'testigo_electoral' else None,
                    'ubicacion_id': user.ubicacion_id
                })
        
        # Problemas detectados
        problemas = []
        
        # Testigos sin ubicación
        testigos_sin_ubicacion = User.query.filter_by(
            rol='testigo_electoral',
            ubicacion_id=None
        ).count()
        if testigos_sin_ubicacion > 0:
            problemas.append(f"{testigos_sin_ubicacion} testigos sin ubicación")
        
        # Usuarios bloqueados
        if usuarios_bloqueados > 0:
            problemas.append(f"{usuarios_bloqueados} usuarios bloqueados")
        
        # Usuarios inactivos
        usuarios_inactivos = total_usuarios - usuarios_activos
        if usuarios_inactivos > 0:
            problemas.append(f"{usuarios_inactivos} usuarios inactivos")
        
        return jsonify({
            'success': True,
            'data': {
                'estadisticas': {
                    'total_usuarios': total_usuarios,
                    'usuarios_activos': usuarios_activos,
                    'usuarios_bloqueados': usuarios_bloqueados,
                    'usuarios_inactivos': usuarios_inactivos
                },
                'roles': roles_dict,
                'usuarios_prueba': usuarios_prueba,
                'problemas': problemas,
                'database_url': os.getenv('DATABASE_URL', 'sqlite:///instance/electoral.db')[:50] + '...'
            }
        }), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
