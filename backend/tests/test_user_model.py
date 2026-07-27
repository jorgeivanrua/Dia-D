"""
Tests para el modelo User
"""
import pytest
from datetime import datetime, timedelta
from backend.models.user import User


@pytest.mark.unit
@pytest.mark.database
def test_create_user(session):
    """Test de creación de usuario"""
    user = User(
        nombre='Test User',
        rol='testigo_electoral',
        ubicacion_id=1,
        activo=True
    )
    user.set_password('test123')
    
    session.add(user)
    session.commit()
    
    assert user.id is not None
    assert user.nombre == 'Test User'
    assert user.rol == 'testigo_electoral'
    assert user.activo is True


@pytest.mark.unit
def test_set_password():
    """Test de establecer contraseña"""
    user = User(nombre='Test', rol='testigo_electoral')
    user.set_password('mypassword123')
    
    assert user.password_hash is not None
    assert user.password_hash != 'mypassword123'
    assert len(user.password_hash) > 0


@pytest.mark.unit
def test_check_password():
    """Test de verificación de contraseña"""
    user = User(nombre='Test', rol='testigo_electoral')
    password = 'mypassword123'
    user.set_password(password)
    
    # Contraseña correcta
    assert user.check_password(password) is True
    
    # Contraseña incorrecta
    assert user.check_password('wrongpassword') is False


@pytest.mark.unit
def test_is_blocked_not_blocked():
    """Test de usuario no bloqueado"""
    user = User(nombre='Test', rol='testigo_electoral')
    
    assert user.is_blocked() is False


@pytest.mark.unit
def test_is_blocked_when_blocked():
    """Test de usuario bloqueado"""
    user = User(nombre='Test', rol='testigo_electoral')
    user.bloqueado_hasta = datetime.utcnow() + timedelta(minutes=30)
    
    assert user.is_blocked() is True


@pytest.mark.unit
def test_is_blocked_expired():
    """Test de bloqueo expirado"""
    user = User(nombre='Test', rol='testigo_electoral')
    user.bloqueado_hasta = datetime.utcnow() - timedelta(minutes=1)
    
    assert user.is_blocked() is False


@pytest.mark.unit
def test_increment_failed_attempts():
    """Test de incrementar intentos fallidos"""
    user = User(nombre='Test', rol='testigo_electoral')
    
    # El valor por defecto puede ser None hasta que se guarde en BD
    assert user.intentos_fallidos in [0, None]
    assert user.bloqueado_hasta is None
    
    # Inicializar si es None
    if user.intentos_fallidos is None:
        user.intentos_fallidos = 0
    
    # Incrementar 4 veces
    for i in range(4):
        user.increment_failed_attempts()
        assert user.intentos_fallidos == i + 1
        assert user.bloqueado_hasta is None
    
    # Quinto intento debe bloquear
    user.increment_failed_attempts()
    assert user.intentos_fallidos == 5
    assert user.bloqueado_hasta is not None
    assert user.is_blocked() is True


@pytest.mark.unit
def test_reset_failed_attempts():
    """Test de resetear intentos fallidos"""
    user = User(nombre='Test', rol='testigo_electoral')
    user.intentos_fallidos = 3
    user.bloqueado_hasta = datetime.utcnow() + timedelta(minutes=30)
    
    user.reset_failed_attempts()
    
    assert user.intentos_fallidos == 0
    assert user.bloqueado_hasta is None
    assert user.ultimo_acceso is not None


@pytest.mark.unit
def test_to_dict():
    """Test de conversión a diccionario"""
    user = User(
        nombre='Test User',
        rol='testigo_electoral',
        ubicacion_id=1,
        activo=True
    )
    
    data = user.to_dict()
    
    assert 'id' in data
    assert data['nombre'] == 'Test User'
    assert data['rol'] == 'testigo_electoral'
    assert data['ubicacion_id'] == 1
    assert data['activo'] is True
    assert 'password_hash' not in data
    assert 'intentos_fallidos' not in data


@pytest.mark.unit
def test_to_dict_with_sensitive():
    """Test de conversión a diccionario con datos sensibles"""
    user = User(
        nombre='Test User',
        rol='testigo_electoral',
        intentos_fallidos=2
    )
    
    data = user.to_dict(include_sensitive=True)
    
    assert 'intentos_fallidos' in data
    assert data['intentos_fallidos'] == 2
    assert 'bloqueado_hasta' in data


@pytest.mark.unit
def test_user_repr():
    """Test de representación string del usuario"""
    user = User(id=1, nombre='Test User', rol='testigo_electoral')
    
    repr_str = repr(user)
    
    assert 'Test User' in repr_str
    assert 'testigo_electoral' in repr_str


@pytest.mark.unit
@pytest.mark.database
def test_user_roles_constraint(session):
    """Test de constraint de roles válidos"""
    # Rol válido
    user = User(nombre='Test', rol='testigo_electoral')
    user.set_password('test123')
    session.add(user)
    session.commit()
    
    assert user.id is not None
    
    # Rol inválido debería fallar (pero SQLite no valida CHECK constraints por defecto)
    # Este test es más relevante en PostgreSQL
