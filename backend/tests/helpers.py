"""
Funciones helper para tests
"""
from flask_jwt_extended import create_access_token


def create_test_user(session, **kwargs):
    """
    Crear usuario de prueba
    
    Args:
        session: Sesión de base de datos
        **kwargs: Datos del usuario
        
    Returns:
        User: Usuario creado
    """
    from backend.models.user import User
    
    defaults = {
        'nombre': 'Usuario Test',
        'rol': 'testigo_electoral',
        'ubicacion_id': 1,
        'activo': True
    }
    defaults.update(kwargs)
    
    user = User(**defaults)
    user.set_password('test123')
    
    session.add(user)
    session.commit()
    
    return user


def create_test_location(session, **kwargs):
    """
    Crear ubicación de prueba
    
    Args:
        session: Sesión de base de datos
        **kwargs: Datos de la ubicación
        
    Returns:
        Location: Ubicación creada
    """
    from backend.models.location import Location
    
    defaults = {
        'departamento_codigo': '18',
        'municipio_codigo': '001',
        'zona_codigo': '01',
        'puesto_codigo': '001',
        'mesa_codigo': '001',
        'nombre_completo': 'Test Location',
        'tipo': 'mesa',
        'total_votantes_registrados': 350
    }
    defaults.update(kwargs)
    
    location = Location(**defaults)
    
    session.add(location)
    session.commit()
    
    return location


def create_test_form_e14(session, **kwargs):
    """
    Crear formulario E-14 de prueba
    
    Args:
        session: Sesión de base de datos
        **kwargs: Datos del formulario
        
    Returns:
        FormE14: Formulario creado
    """
    from backend.models.form_e14 import FormE14
    
    defaults = {
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
        'estado': 'borrador'
    }
    defaults.update(kwargs)
    
    form = FormE14(**defaults)
    
    session.add(form)
    session.commit()
    
    return form


def get_auth_token(user_id, rol='testigo_electoral', ubicacion_id=1):
    """
    Generar token de autenticación para tests
    
    Args:
        user_id: ID del usuario
        rol: Rol del usuario
        ubicacion_id: ID de ubicación
        
    Returns:
        str: Token JWT
    """
    return create_access_token(
        identity=str(user_id),
        additional_claims={
            'rol': rol,
            'ubicacion_id': ubicacion_id,
            'nombre': 'Usuario Test'
        }
    )


def assert_response_success(response, status_code=200):
    """
    Verificar que la respuesta es exitosa
    
    Args:
        response: Respuesta de Flask
        status_code: Código de estado esperado
    """
    assert response.status_code == status_code
    data = response.get_json()
    assert data is not None
    assert data.get('success') is True
    return data


def assert_response_error(response, status_code=400):
    """
    Verificar que la respuesta es un error
    
    Args:
        response: Respuesta de Flask
        status_code: Código de estado esperado
    """
    assert response.status_code == status_code
    data = response.get_json()
    assert data is not None
    assert data.get('success') is False
    assert 'error' in data
    return data


def assert_validation_error(response, field=None):
    """
    Verificar que la respuesta es un error de validación
    
    Args:
        response: Respuesta de Flask
        field: Campo específico con error (opcional)
    """
    data = assert_response_error(response, 422)
    assert 'errors' in data
    
    if field:
        assert field in data['errors']
    
    return data
