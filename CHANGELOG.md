# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [1.1.0] - 2024-11-30

### 🔒 Seguridad

- **CRÍTICO:** Implementado hashing seguro de contraseñas con Werkzeug
- Eliminado endpoint inseguro `/api/auth/reset-all-passwords-test123`
- Mejorada seguridad de endpoints de emergencia
- Agregada verificación de entorno en endpoints críticos

### ✨ Agregado

- Sistema de logging centralizado (`backend/utils/logging_config.py`)
- Script consolidado de inicialización (`scripts/init_system.py`)
- Script de verificación del sistema (`scripts/check_system.py`)
- Script de limpieza del sistema (`scripts/clean_system.py`)
- Soporte para Flask-Migrate (Alembic)
- Documentación de seguridad (`docs/SEGURIDAD.md`)
- Guía de troubleshooting (`docs/TROUBLESHOOTING.md`)
- Guía de contribución (`CONTRIBUTING.md`)
- Configuración de pre-commit hooks
- `pyproject.toml` para configuración centralizada
- `.editorconfig` para consistencia de código
- `requirements-dev.txt` para dependencias de desarrollo

### 🔄 Cambiado

- `setup.py` ahora usa `init_system.py` y crea `.env` automáticamente
- `run.py` eliminadas migraciones SQL manuales
- `Makefile` ahora es multiplataforma
- `start.bat` y `start.sh` corregidos para usar `electoral.db`
- README actualizado con nuevas instrucciones
- 15 scripts movidos a `scripts/deprecated/`

### 🐛 Corregido

- Inconsistencia en nombres de base de datos
- Contraseñas en texto plano
- Scripts duplicados causando confusión
- Falta de validación en inicialización
- Logging inconsistente

### 📚 Documentación

- Creados 8 nuevos documentos de guía
- Actualizado README principal
- Agregada documentación de API (pendiente)

---

## [1.0.0] - 2024-11-22

### ✨ Agregado

- Sistema de autenticación JWT
- Gestión de usuarios por rol
- Configuración electoral dinámica
- Formularios E-14 completos
- API REST completa
- Dashboards por rol
- Verificación de presencia con geolocalización
- Sistema de sincronización offline
- Validación de formularios
- Reportes y estadísticas

### 🎯 Funcionalidades

- 7 roles de usuario implementados
- Sistema jerárquico de ubicaciones (DIVIPOLA)
- Gestión de partidos y candidatos
- Validación automática de datos
- Historial de cambios en formularios

---

## [0.1.0] - 2024-11-01

### ✨ Agregado

- Estructura inicial del proyecto
- Modelos básicos de datos
- Autenticación básica
- CRUD de formularios

---

## Tipos de Cambios

- `Agregado` para nuevas funcionalidades
- `Cambiado` para cambios en funcionalidades existentes
- `Deprecado` para funcionalidades que serán eliminadas
- `Eliminado` para funcionalidades eliminadas
- `Corregido` para correcciones de bugs
- `Seguridad` para vulnerabilidades corregidas

---

**Formato:** [MAJOR.MINOR.PATCH]
- **MAJOR:** Cambios incompatibles con versiones anteriores
- **MINOR:** Nuevas funcionalidades compatibles
- **PATCH:** Correcciones de bugs compatibles
