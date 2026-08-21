"""
Utilidades para manejo de JWT
"""
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, jwt_required
from datetime import timedelta
from backend.utils.exceptions import BaseAPIException

# Blacklist para invalidar tokens JWT
BLACKLIST = set()

def is_token_blacklisted(jti):
    """Verificar si un token ha sido añadido a la blacklist"""
    return jti in BLACKLIST

def add_to_blacklist(jti):
    """Añadir un JTI a la blacklist"""
    BLACKLIST.add(jti)


def generate_tokens(user):
    """
    Generar tokens de acceso y renovación para un usuario
    
    Args:
        user: Objeto User
        
    Returns:
        tuple: (access_token, refresh_token)
    """
    # Claims adicionales para incluir en el token
    additional_claims = {
        'rol': user.rol,
        'ubicacion_id': user.ubicacion_id,
        'nombre': user.nombre
    }
    
    # Generar tokens (identity debe ser string)
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims=additional_claims
    )
    
    refresh_token = create_refresh_token(
        identity=str(user.id),
        additional_claims=additional_claims
    )
    
    return access_token, refresh_token


def create_token_response(user, access_token, refresh_token):
    """
    Crear respuesta con tokens y datos de usuario
    
    Args:
        user: Objeto User
        access_token: Token de acceso
        refresh_token: Token de renovación
        
    Returns:
        dict: Respuesta con tokens y usuario
    """
    from backend.models.location import Location
    
    # Obtener información de ubicación si existe
    ubicacion = None
    if user.ubicacion_id:
        location = Location.query.get(user.ubicacion_id)
        if location:
            ubicacion = {
                'id': location.id,
                'nombre_completo': location.nombre_completo,
                'tipo': location.tipo,
                'departamento_codigo': location.departamento_codigo,
                'municipio_codigo': location.municipio_codigo,
                'zona_codigo': location.zona_codigo,
                'puesto_codigo': location.puesto_codigo,
                'puesto_nombre': location.puesto_nombre
            }
    
    return {
        'success': True,
        'data': {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': 3600,
            'user': {
                'id': user.id,
                'nombre': user.nombre,
                'rol': user.rol,
                'ubicacion_id': user.ubicacion_id,
                'activo': user.activo
            },
            'ubicacion': ubicacion
        }
    }
