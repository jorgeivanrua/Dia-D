"""
Excepciones personalizadas
"""


class BaseAPIException(Exception):
    """Excepción base para la API"""
    status_code = 400
    
    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['success'] = False
        rv['error'] = self.message
        return rv


class ValidationException(BaseAPIException):
    """Excepción de validación"""
    status_code = 422
    
    def __init__(self, errors):
        self.errors = errors
        super().__init__('Errores de validación')
    
    def to_dict(self):
        return {
            'success': False,
            'error': self.message,
            'errors': self.errors
        }


class AuthenticationException(BaseAPIException):
    """Excepción de autenticación"""
    status_code = 401


class PermissionDeniedException(BaseAPIException):
    """Excepción de permisos"""
    status_code = 403


class ResourceNotFoundException(BaseAPIException):
    """Excepción de recurso no encontrado"""
    status_code = 404


class AccountBlockedException(BaseAPIException):
    """Excepción de cuenta bloqueada"""
    status_code = 403
    
    def __init__(self, message, blocked_until=None):
        super().__init__(message)
        self.blocked_until = blocked_until
    
    def to_dict(self):
        rv = super().to_dict()
        if self.blocked_until:
            rv['blocked_until'] = self.blocked_until.isoformat()
        return rv


class DuplicateResourceException(BaseAPIException):
    """Excepción de recurso duplicado"""
    status_code = 409


class AuthorizationException(BaseAPIException):
    """Excepción de autorización"""
    status_code = 403


# Alias para compatibilidad
NotFoundException = ResourceNotFoundException
