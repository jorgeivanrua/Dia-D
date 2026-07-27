"""
Tests para verificar que los fixtures funcionan correctamente
"""
import pytest
from backend.tests.helpers import get_auth_token, assert_response_success


@pytest.mark.unit
def test_app_fixture(app):
    """Test del fixture de aplicación"""
    assert app is not None
    assert app.config['TESTING'] is True
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'


@pytest.mark.unit
def test_db_fixture(db):
    """Test del fixture de base de datos"""
    assert db is not None
    # Verificar que podemos ejecutar queries
    result = db.session.execute(db.text('SELECT 1')).scalar()
    assert result == 1


@pytest.mark.unit
def test_client_fixture(client):
    """Test del fixture de cliente"""
    assert client is not None
    # Hacer una petición de prueba
    response = client.get('/')
    assert response is not None


@pytest.mark.unit
def test_auth_headers_fixture(auth_headers):
    """Test del fixture de headers de autenticación"""
    token = 'test_token_123'
    headers = auth_headers(token)
    
    assert 'Authorization' in headers
    assert headers['Authorization'] == f'Bearer {token}'
    assert headers['Content-Type'] == 'application/json'


@pytest.mark.unit
def test_sample_user_data_fixture(sample_user_data):
    """Test del fixture de datos de usuario"""
    assert 'nombre' in sample_user_data
    assert 'rol' in sample_user_data
    assert sample_user_data['rol'] == 'testigo_electoral'


@pytest.mark.unit
def test_sample_location_data_fixture(sample_location_data):
    """Test del fixture de datos de ubicación"""
    assert 'departamento_codigo' in sample_location_data
    assert 'tipo' in sample_location_data
    assert sample_location_data['tipo'] == 'mesa'


@pytest.mark.unit
def test_sample_form_e14_data_fixture(sample_form_e14_data):
    """Test del fixture de datos de formulario E-14"""
    assert 'mesa_id' in sample_form_e14_data
    assert 'total_votos' in sample_form_e14_data
    assert 'votos_partidos' in sample_form_e14_data


@pytest.mark.unit
def test_get_auth_token_helper():
    """Test del helper para generar tokens"""
    token = get_auth_token(1, 'testigo_electoral', 1)
    
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


@pytest.mark.unit
@pytest.mark.database
def test_session_fixture(session, db):
    """Test del fixture de sesión de base de datos"""
    assert session is not None
    
    # Verificar que podemos hacer queries
    from sqlalchemy import text
    result = session.execute(text('SELECT 1')).scalar()
    assert result == 1
