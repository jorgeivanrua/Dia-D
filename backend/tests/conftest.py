"""
Configuración de fixtures para pytest
"""
import pytest
from backend.app import create_app
from backend.database import db as _db


@pytest.fixture(scope='session')
def app():
    """
    Fixture de aplicación Flask para toda la sesión de tests
    """
    app = create_app('testing')
    
    # Establecer contexto de aplicación
    ctx = app.app_context()
    ctx.push()
    
    yield app
    
    ctx.pop()


@pytest.fixture(scope='session')
def db(app):
    """
    Fixture de base de datos para toda la sesión de tests
    """
    # Crear todas las tablas
    _db.create_all()
    
    yield _db
    
    # Limpiar después de los tests
    _db.drop_all()


@pytest.fixture(scope='function')
def session(db):
    """
    Fixture de sesión de base de datos para cada test
    Crea una transacción que se revierte después de cada test
    """
    connection = db.engine.connect()
    transaction = connection.begin()
    
    # Usar la sesión existente
    session = db.session
    session.bind = connection
    
    yield session
    
    # Revertir transacción
    session.rollback()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope='function')
def client(app):
    """
    Fixture de cliente de prueba para cada test
    """
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """
    Fixture de CLI runner para cada test
    """
    return app.test_cli_runner()


@pytest.fixture
def auth_headers():
    """
    Fixture para generar headers de autenticación
    """
    def _auth_headers(token):
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    return _auth_headers


@pytest.fixture
def sample_user_data():
    """
    Fixture con datos de usuario de ejemplo
    """
    return {
        'nombre': 'Usuario Test',
        'rol': 'testigo_electoral',
        'ubicacion_id': 1,
        'activo': True
    }


@pytest.fixture
def sample_location_data():
    """
    Fixture con datos de ubicación de ejemplo
    """
    return {
        'departamento_codigo': '18',
        'municipio_codigo': '001',
        'zona_codigo': '01',
        'puesto_codigo': '001',
        'mesa_codigo': '001',
        'nombre_completo': 'Caquetá - Florencia - Zona 1 - Puesto 1 - Mesa 1',
        'tipo': 'mesa',
        'total_votantes_registrados': 350
    }


@pytest.fixture
def sample_form_e14_data():
    """
    Fixture con datos de formulario E-14 de ejemplo
    """
    return {
        'mesa_id': 1,
        'testigo_id': 1,
        'total_votantes': 300,
        'total_votos': 280,
        'votos_partidos': {
            'partido_1': 120,
            'partido_2': 100,
            'partido_3': 50
        },
        'votos_nulos': 5,
        'votos_no_marcados': 5,
        'observaciones': 'Sin novedad'
    }
