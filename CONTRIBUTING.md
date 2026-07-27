# 🤝 Guía de Contribución

## Bienvenido

Gracias por tu interés en contribuir al Sistema de Testigos Electorales. Esta guía te ayudará a empezar.

---

## 📋 Tabla de Contenidos

1. [Código de Conducta](#código-de-conducta)
2. [Cómo Contribuir](#cómo-contribuir)
3. [Configuración del Entorno](#configuración-del-entorno)
4. [Estándares de Código](#estándares-de-código)
5. [Proceso de Pull Request](#proceso-de-pull-request)
6. [Reportar Bugs](#reportar-bugs)
7. [Sugerir Mejoras](#sugerir-mejoras)

---

## 📜 Código de Conducta

Este proyecto se adhiere a un código de conducta. Al participar, se espera que mantengas este código.

- Sé respetuoso y profesional
- Acepta críticas constructivas
- Enfócate en lo mejor para la comunidad
- Muestra empatía hacia otros miembros

---

## 🚀 Cómo Contribuir

### 1. Fork el Repositorio

```bash
git clone https://github.com/tu-usuario/testigos.git
cd testigos
```

### 2. Crea una Rama

```bash
git checkout -b feature/mi-nueva-funcionalidad
# o
git checkout -b fix/correccion-de-bug
```

### 3. Haz tus Cambios

Sigue los [estándares de código](#estándares-de-código)

### 4. Commit

```bash
git add .
git commit -m "feat: descripción clara del cambio"
```

### 5. Push

```bash
git push origin feature/mi-nueva-funcionalidad
```

### 6. Crea Pull Request

Ve a GitHub y crea un Pull Request

---

## 🛠️ Configuración del Entorno

### Requisitos

- Python 3.8+
- pip
- virtualenv

### Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/testigos.git
cd testigos

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar entorno virtual
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# 6. Configurar pre-commit hooks
pre-commit install

# 7. Inicializar sistema
python scripts/init_system.py

# 8. Verificar instalación
python scripts/check_system.py
```

---

## 📝 Estándares de Código

### Python

- **Estilo:** PEP 8
- **Formatter:** Black (line-length=100)
- **Linter:** Flake8
- **Import sorting:** isort
- **Type hints:** Recomendado pero no obligatorio

### Estructura de Archivos

```
backend/
├── models/         # Modelos de datos
├── routes/         # Endpoints de API
├── services/       # Lógica de negocio
├── utils/          # Utilidades
└── tests/          # Tests
```

### Convenciones de Nombres

- **Archivos:** `snake_case.py`
- **Clases:** `PascalCase`
- **Funciones:** `snake_case()`
- **Constantes:** `UPPER_SNAKE_CASE`
- **Variables:** `snake_case`

### Docstrings

```python
def funcion_ejemplo(param1, param2):
    """
    Descripción breve de la función
    
    Args:
        param1: Descripción del parámetro 1
        param2: Descripción del parámetro 2
        
    Returns:
        Descripción del valor de retorno
        
    Raises:
        ExceptionType: Cuándo se lanza
    """
    pass
```

### Commits

Seguimos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Formato, punto y coma faltantes, etc.
- `refactor:` Refactorización de código
- `test:` Agregar tests
- `chore:` Mantenimiento

**Ejemplos:**
```
feat: agregar endpoint de reportes
fix: corregir validación de formularios
docs: actualizar README con nuevas instrucciones
```

---

## 🔍 Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Tests específicos
pytest backend/tests/test_auth.py

# Con cobertura
pytest --cov=backend --cov-report=html

# Solo tests unitarios
pytest -m unit

# Solo tests de integración
pytest -m integration
```

### Escribir Tests

```python
import pytest
from backend.models.user import User

def test_user_creation():
    """Test que verifica la creación de usuarios"""
    user = User(nombre="Test", rol="testigo_electoral")
    assert user.nombre == "Test"
    assert user.rol == "testigo_electoral"

@pytest.mark.integration
def test_user_login(client):
    """Test de integración para login"""
    response = client.post('/api/auth/login', json={
        'rol': 'super_admin',
        'password': 'admin123'
    })
    assert response.status_code == 200
```

### Cobertura Mínima

- **Objetivo:** 80% de cobertura
- **Crítico:** Modelos, servicios, rutas de autenticación

---

## 📤 Proceso de Pull Request

### Checklist

Antes de crear un PR, verifica:

- [ ] El código sigue los estándares
- [ ] Los tests pasan (`pytest`)
- [ ] La cobertura no disminuye
- [ ] La documentación está actualizada
- [ ] Los commits siguen Conventional Commits
- [ ] No hay conflictos con `main`
- [ ] Pre-commit hooks pasan

### Descripción del PR

```markdown
## Descripción
Breve descripción de los cambios

## Tipo de cambio
- [ ] Bug fix
- [ ] Nueva funcionalidad
- [ ] Breaking change
- [ ] Documentación

## ¿Cómo se ha probado?
Describe las pruebas realizadas

## Checklist
- [ ] Tests agregados/actualizados
- [ ] Documentación actualizada
- [ ] Código revisado
```

### Revisión

- Mínimo 1 aprobación requerida
- CI/CD debe pasar
- Sin conflictos

---

## 🐛 Reportar Bugs

### Antes de Reportar

1. Verifica que no exista un issue similar
2. Asegúrate de usar la última versión
3. Recopila información del error

### Template de Bug Report

```markdown
**Descripción del Bug**
Descripción clara del problema

**Pasos para Reproducir**
1. Ir a '...'
2. Hacer clic en '...'
3. Ver error

**Comportamiento Esperado**
Qué debería pasar

**Comportamiento Actual**
Qué pasa realmente

**Screenshots**
Si aplica

**Entorno**
- OS: [e.g. Windows 10]
- Python: [e.g. 3.10]
- Versión: [e.g. 1.1.0]

**Logs**
```
Pegar logs relevantes
```

**Contexto Adicional**
Cualquier otra información
```

---

## 💡 Sugerir Mejoras

### Template de Feature Request

```markdown
**¿El feature está relacionado con un problema?**
Descripción clara del problema

**Solución Propuesta**
Cómo te gustaría que se resolviera

**Alternativas Consideradas**
Otras soluciones que consideraste

**Contexto Adicional**
Screenshots, mockups, etc.
```

---

## 🏗️ Arquitectura

### Principios

- **SOLID:** Seguir principios SOLID
- **DRY:** Don't Repeat Yourself
- **KISS:** Keep It Simple, Stupid
- **YAGNI:** You Aren't Gonna Need It

### Patrones

- **Factory Pattern:** Para crear app Flask
- **Repository Pattern:** Para acceso a datos
- **Service Layer:** Para lógica de negocio
- **Blueprint Pattern:** Para organizar rutas

---

## 📚 Recursos

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Python Best Practices](https://docs.python-guide.org/)
- [PEP 8 Style Guide](https://pep8.org/)

---

## 🙏 Agradecimientos

Gracias por contribuir al proyecto. Tu ayuda es muy apreciada.

---

## 📞 Contacto

- **Issues:** [GitHub Issues](https://github.com/jorgeivanrua/testigos/issues)
- **Discussions:** [GitHub Discussions](https://github.com/jorgeivanrua/testigos/discussions)

---

**Última actualización:** 30 de Noviembre de 2024
