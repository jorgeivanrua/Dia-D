"""
Callbacks para Flask-JWT-Extended
"""
from flask import jsonify
from flask_jwt_extended import JWTManager


def configure_jwt_callbacks(jwt: JWTManager):
    """
    Configurar callbacks de JWT
    
    Args:
        jwt: Instancia de JWTManager
    """
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Callback cuando el token ha expirado"""
        return jsonify({
            'success': False,
            'error': 'El token ha expirado',
            'code': 'TOKEN_EXPIRED'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Callback cuando el token es inválido"""
        return jsonify({
            'success': False,
            'error': 'Token inválido',
            'code': 'INVALID_TOKEN'
        }), 401
    
    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        """Callback cuando no se proporciona token"""
        return jsonify({
            'success': False,
            'error': 'Token de autenticación requerido',
            'code': 'MISSING_TOKEN'
        }), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """Callback cuando el token ha sido revocado"""
        return jsonify({
            'success': False,
            'error': 'El token ha sido revocado',
            'code': 'TOKEN_REVOKED'
        }), 401
    
    @jwt.token_verification_failed_loader
    def token_verification_failed_callback(jwt_header, jwt_payload):
        """Callback cuando falla la verificación del token"""
        return jsonify({
            'success': False,
            'error': 'Verificación del token fallida',
            'code': 'TOKEN_VERIFICATION_FAILED'
        }), 401
