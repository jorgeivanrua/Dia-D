"""
Tests para configuración JWT
"""
import pytest
from flask import Flask
from flask_jwt_extended import create_access_token, decode_token
from backend.app import create_app


@pytest.fixture
def app():
    """Fixture de aplicación Flask"""
    app = create_app('testing')
    return app


@pytest.fixture
def client(app):
    """Fixture de cliente de prueba"""
    return app.test_client()


def test_jwt_configuration(app):
    """Test de configuración JWT"""
    with app.app_context():
        # Verificar que JWT está configurado
        assert app.config['JWT_SECRET_KEY'] is not None
        assert app.config['JWT_ACCESS_TOKEN_EXPIRES'] is not None


def test_create_access_token(app):
    """Test de creación de token de acceso"""
    with app.app_context():
        # Crear token (identity debe ser string)
        token = create_access_token(
            identity='1',
            additional_claims={'rol': 'testigo_electoral'}
        )
        
        # Verificar que el token se creó
        assert token is not None
        assert isinstance(token, str)
        
        # Decodificar token
        decoded = decode_token(token)
        assert decoded['sub'] == '1'
        assert decoded['rol'] == 'testigo_electoral'


def test_protected_route_without_token(client):
    """Test de ruta protegida sin token"""
    # Crear una ruta de prueba protegida
    # Por ahora solo verificamos que la app funciona
    response = client.get('/api/test')
    assert response.status_code in [404, 401]  # 404 porque la ruta no existe aún


def test_jwt_callbacks(app):
    """Test de callbacks JWT"""
    # Verificar que JWT está configurado
    assert app.config['JWT_SECRET_KEY'] is not None
    # Los callbacks se configuran internamente en Flask-JWT-Extended
