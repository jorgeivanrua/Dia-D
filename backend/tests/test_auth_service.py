"""
Tests para AuthService
"""

from backend.models.location import Location
from backend.models.user import User
from backend.services.auth_service import AuthService


def test_authenticate_location_based_falls_back_to_mesa_user(session):
    """Debe autenticar un testigo ubicado en una mesa cuando no hay usuario en el puesto."""
    # Crear ubicación de puesto y una mesa asociada
    puesto = Location(
        departamento_codigo='44',
        municipio_codigo='070',
        zona_codigo='01',
        puesto_codigo='44070000',
        mesa_codigo=None,
        departamento_nombre='Test Dept',
        municipio_nombre='Test Municipio',
        puesto_nombre='Puesto 1',
        mesa_nombre=None,
        nombre_completo='Dept - Municipio - Zona 1 - Puesto 1',
        tipo='puesto',
        total_votantes_registrados=100,
        activo=True
    )
    session.add(puesto)
    session.commit()

    mesa = Location(
        departamento_codigo='44',
        municipio_codigo='070',
        zona_codigo='01',
        puesto_codigo='44070000',
        mesa_codigo='001',
        departamento_nombre='Test Dept',
        municipio_nombre='Test Municipio',
        puesto_nombre='Puesto 1',
        mesa_nombre='Mesa 1',
        nombre_completo='Dept - Municipio - Zona 1 - Puesto 1 - Mesa 1',
        tipo='mesa',
        total_votantes_registrados=50,
        activo=True
    )
    session.add(mesa)
    session.commit()

    # Crear usuario testigo asociado a la mesa
    user = User(
        nombre='Testigo Mesa',
        rol='testigo_electoral',
        ubicacion_id=mesa.id,
        activo=True
    )
    user.set_password('test123')
    session.add(user)
    session.commit()

    ubicacion_data = {
        'departamento_codigo': '44',
        'municipio_codigo': '070',
        'zona_codigo': '01',
        'puesto_codigo': '44070000'
    }

    authenticated_user, access_token, refresh_token = AuthService.authenticate_location_based(
        'testigo_electoral',
        ubicacion_data,
        'test123'
    )

    assert authenticated_user.id == user.id
    assert authenticated_user.rol == 'testigo_electoral'
    assert access_token is not None
    assert refresh_token is not None
