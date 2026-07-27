# Sistema de Usuarios Básicos y Backup de Base de Datos

**Fecha**: 2025-12-07  
**Autor**: Kiro AI  
**Estado**: ✅ Implementado

## Resumen

Sistema completo para gestionar usuarios básicos persistentes del sistema y realizar backup/restauración de la base de datos con protección de usuarios críticos.

## Problema

1. **Usuarios no persistentes**: Al cambiar de SQLite (local) a PostgreSQL (Render), los usuarios se perdían
2. **Datos de prueba mezclados**: Usuarios de prueba mezclados con usuarios del sistema
3. **Importación sin protección**: Al importar BD, se podían sobrescribir usuarios críticos del sistema
4. **Falta de backup automático**: No había forma fácil de exportar/importar la BD completa

## Solución Implementada

### 1. Campo `es_usuario_basico` en User Model

```python
# backend/models/user.py
es_usuario_basico = db.Column(db.Boolean, default=False, nullable=False)
```

Este campo marca usuarios que son parte del sistema y NO deben eliminarse.

### 2. Inicialización Automática de Usuarios Básicos

**Archivo**: `backend/utils/init_usuarios_basicos.py`

Se ejecuta automáticamente al iniciar la aplicación (ver `backend/app.py`):

```python
from backend.utils.init_usuarios_basicos import init_usuarios_basicos
init_usuarios_basicos()
```

**Usuarios básicos creados automáticamente al iniciar la app**:
- **Super Admin** (admin123) - Acceso global sin ubicación
- **Monitoreo** (test123) - Acceso global de solo lectura

**Usuarios básicos que deben marcarse manualmente** (1 por ubicación):
- **Coordinador Departamental** - 1 por departamento
- **Coordinador Municipal** - 1 por municipio
- **Coordinador de Puesto** - 1 por puesto
- **Testigo Electoral** - 1 por puesto

**IMPORTANTE**: Usar el script `marcar_usuarios_definitivos_basicos.py` para marcar automáticamente el primer usuario de cada ubicación como básico.

### 3. Sistema de Backup y Restauración

**Endpoints** (`backend/routes/database_backup.py`):

#### GET `/api/database/export`
- Exporta toda la BD a JSON
- NO exporta contraseñas (seguridad)
- Incluye: usuarios, ubicaciones, formularios, votos, incidentes, delitos, evidencias
- Genera archivo `database_backup_YYYYMMDD_HHMMSS.json`

#### POST `/api/database/import`
- Importa BD desde archivo JSON
- **PROTEGE usuarios básicos**: No sobrescribe usuarios con `es_usuario_basico=True`
- Asigna contraseña temporal `test123` a usuarios importados
- Manejo robusto de errores (continúa si un registro falla)
- Commits parciales por tipo de entidad

#### GET `/api/database/stats`
- Retorna estadísticas de la BD actual

### 4. Interfaz de Usuario

**Ubicación**: Super Admin Dashboard (`frontend/templates/admin/super-admin-dashboard.html`)

**Botones agregados**:
- 📊 **Estadísticas de BD**: Muestra contadores de registros
- 💾 **Exportar Base de Datos**: Descarga JSON con toda la BD
- 📥 **Importar Base de Datos**: Sube JSON para restaurar BD

**Modal de importación**:
- Selector de archivo
- Barra de progreso
- Resultados detallados por tipo de entidad
- Manejo de errores con mensajes claros

### 5. Scripts de Utilidades

#### `scripts/utils/verificar_usuarios_basicos.py`
Verifica que todos los usuarios básicos del sistema existan:
```bash
python scripts/utils/verificar_usuarios_basicos.py
```

**Salida**:
- Lista de usuarios básicos requeridos (✅ o ❌)
- Cantidad de testigos básicos
- Estadísticas generales

#### `scripts/utils/limpiar_usuarios_prueba.py`
Elimina todos los usuarios que NO son usuarios básicos:
```bash
python scripts/utils/limpiar_usuarios_prueba.py
```

**Características**:
- Solicita confirmación antes de eliminar
- Muestra usuarios que serán eliminados
- Protege usuarios con `es_usuario_basico=True`
- Muestra usuarios restantes después de limpieza

#### `scripts/utils/marcar_usuarios_definitivos_basicos.py` ⭐ RECOMENDADO
Marca todos los usuarios definitivos como básicos (1 por ubicación):
```bash
python scripts/utils/marcar_usuarios_definitivos_basicos.py
```

**Lógica**:
1. Marca Super Admin y Monitoreo como básicos
2. Marca 1 coordinador departamental por departamento
3. Marca 1 coordinador municipal por municipio
4. Marca 1 coordinador de puesto por puesto
5. Marca 1 testigo por puesto
6. Si hay múltiples usuarios en una ubicación, marca solo el primero
7. Reporta ubicaciones sin usuarios

**Este es el script principal que debes ejecutar antes de exportar la BD.**

#### `scripts/utils/marcar_testigos_basicos.py`
Marca solo testigos como usuarios básicos (1 por puesto):
```bash
python scripts/utils/marcar_testigos_basicos.py
```

**Uso**: Solo si necesitas marcar testigos específicamente sin tocar coordinadores.

#### Scripts manuales de backup
- `scripts/utils/export_data_to_json.py` - Exportar BD manualmente
- `scripts/utils/import_data_from_json.py` - Importar BD manualmente

### 6. Integración con Render

**Archivo**: `scripts/init/render_setup.py`

Modificado para:
- NO crear usuarios manualmente
- Confiar en `init_usuarios_basicos()` que se ejecuta automáticamente
- Verificar que usuarios básicos existan después de inicialización

## Flujo de Trabajo

### Desarrollo Local

1. **Marcar usuarios definitivos como básicos**:
```bash
python scripts/utils/marcar_usuarios_definitivos_basicos.py
```
Este script marca automáticamente:
- Super Admin y Monitoreo
- 1 coordinador departamental por departamento
- 1 coordinador municipal por municipio
- 1 coordinador de puesto por puesto
- 1 testigo por puesto

2. **Verificar que todos estén marcados**:
```bash
python scripts/utils/verificar_usuarios_basicos.py
```

3. **Limpiar usuarios de prueba** (antes de exportar):
```bash
python scripts/utils/limpiar_usuarios_prueba.py
```

4. **Exportar BD limpia**:
```bash
python scripts/utils/export_data_to_json.py
# O usar el botón en Super Admin Dashboard
```

### Despliegue en Render

1. **Primera vez**:
   - Render ejecuta `scripts/init/render_setup.py`
   - Se crea estructura de BD (PostgreSQL)
   - `init_usuarios_basicos()` crea usuarios del sistema automáticamente

2. **Importar datos**:
   - Acceder a Super Admin Dashboard
   - Clic en "Importar Base de Datos"
   - Seleccionar archivo JSON exportado
   - Los usuarios básicos NO se sobrescriben

3. **Credenciales iniciales**:
   - Usuario: `admin` o `Super Admin`
   - Password: `admin123`

### Mantenimiento

```bash
# Después de agregar nuevas ubicaciones o usuarios
python scripts/utils/marcar_usuarios_definitivos_basicos.py

# Verificar estado del sistema
python scripts/utils/verificar_usuarios_basicos.py

# Backup periódico
python scripts/utils/export_data_to_json.py

# Restaurar desde backup
python scripts/utils/import_data_from_json.py
```

## Protecciones Implementadas

### 1. Protección en Importación
```python
# backend/routes/database_backup.py
if existing.es_usuario_basico:
    print(f"⚠️  Omitiendo usuario básico del sistema: {user_data['nombre']}")
    continue
```

### 2. Protección en Limpieza
```python
# scripts/utils/limpiar_usuarios_prueba.py
usuarios_eliminados = User.query.filter_by(es_usuario_basico=False).delete()
```

### 3. Inicialización Automática
```python
# backend/app.py
with app.app_context():
    from backend.utils.init_usuarios_basicos import init_usuarios_basicos
    init_usuarios_basicos()
```

## Seguridad

1. **Contraseñas NO se exportan**: Por seguridad, las contraseñas no se incluyen en el JSON
2. **Contraseña temporal en importación**: Usuarios importados reciben `test123`
3. **Solo Super Admin**: Endpoints de backup solo accesibles para `super_admin`
4. **JWT requerido**: Todos los endpoints requieren autenticación

## Archivos Modificados

### Backend
- `backend/models/user.py` - Campo `es_usuario_basico`
- `backend/routes/database_backup.py` - Endpoints de backup (MODIFICADO: protección de usuarios básicos)
- `backend/app.py` - Registro de blueprint y llamada a `init_usuarios_basicos()`
- `backend/utils/init_usuarios_basicos.py` - Inicialización automática

### Frontend
- `frontend/templates/admin/super-admin-dashboard.html` - Botones y modal de importación

### Scripts
- `scripts/init/render_setup.py` - Integración con Render (MODIFICADO)
- `scripts/utils/verificar_usuarios_basicos.py` - Verificación (NUEVO)
- `scripts/utils/limpiar_usuarios_prueba.py` - Limpieza (NUEVO)
- `scripts/utils/marcar_testigos_basicos.py` - Marcar testigos (NUEVO)
- `scripts/utils/export_data_to_json.py` - Exportar manual
- `scripts/utils/import_data_from_json.py` - Importar manual
- `scripts/utils/README.md` - Documentación actualizada

## Testing

### Verificar usuarios básicos
```bash
python scripts/utils/verificar_usuarios_basicos.py
```

**Resultado esperado**:
```
📋 1. Usuarios Globales:
--------------------------------------------------------------------------------
✅ Super Admin                      | Super Admin                    | ID: 1
✅ Monitoreo                        | Monitoreo                      | ID: 2
--------------------------------------------------------------------------------

📋 2. Coordinadores Departamentales (1 por departamento):
--------------------------------------------------------------------------------
   Departamentos: 1
   Coordinadores básicos: 1
   ✅ Todos los departamentos tienen coordinador básico
--------------------------------------------------------------------------------

📋 3. Coordinadores Municipales (1 por municipio):
--------------------------------------------------------------------------------
   Municipios: 16
   Coordinadores básicos: 16
   ✅ Todos los municipios tienen coordinador básico
--------------------------------------------------------------------------------

📋 4. Coordinadores de Puesto (1 por puesto):
--------------------------------------------------------------------------------
   Puestos: 50
   Coordinadores básicos: 50
   ✅ Todos los puestos tienen coordinador básico
--------------------------------------------------------------------------------

📋 5. Testigos (1 por puesto):
--------------------------------------------------------------------------------
   Puestos: 50
   Testigos básicos: 50
   ✅ Todos los puestos tienen testigo básico
--------------------------------------------------------------------------------

📊 Estadísticas generales:
   Total de usuarios: 150
   Usuarios básicos del sistema: 119
   Usuarios de prueba/temporales: 31
```

### Exportar BD
1. Acceder a Super Admin Dashboard
2. Clic en "Exportar Base de Datos"
3. Verificar que se descarga archivo JSON

### Importar BD
1. Acceder a Super Admin Dashboard
2. Clic en "Importar Base de Datos"
3. Seleccionar archivo JSON
4. Verificar que se importan registros
5. Verificar que usuarios básicos NO se sobrescriben

## Próximos Pasos

1. ✅ Implementar protección de usuarios básicos en importación
2. ✅ Crear scripts de utilidades para gestión de usuarios
3. ✅ Actualizar documentación
4. ⏳ Probar en Render con PostgreSQL
5. ⏳ Configurar backup automático periódico (opcional)
6. ⏳ Implementar versionado de backups (opcional)

## Notas Importantes

- **Usuarios básicos son persistentes**: Super Admin y Monitoreo se crean automáticamente al iniciar la app
- **Usuarios definitivos**: Cada ubicación debe tener exactamente 1 coordinador y 1 testigo marcados como básicos
- **Marcar usuarios**: Usar `marcar_usuarios_definitivos_basicos.py` para marcar automáticamente usuarios definitivos
- **Contraseñas temporales**: Usuarios importados tienen `test123`
- **Protección multicapa**: Usuarios básicos protegidos en importación y limpieza
- **Sin pérdida de datos**: Importación continúa aunque fallen registros individuales
- **Render**: PostgreSQL se configura automáticamente desde `DATABASE_URL`

### ¿Qué son usuarios básicos definitivos?

Son los usuarios **mínimos necesarios** para que el sistema funcione:

**Usuarios Globales** (sin ubicación):
- **Super Admin** (1) - Administración completa
- **Monitoreo** (1) - Visualización en tiempo real

**Usuarios por Ubicación** (1 por cada):
- **Coordinador Departamental** - 1 por departamento (ej: 1 para Caquetá)
- **Coordinador Municipal** - 1 por municipio (ej: 1 para Florencia)
- **Coordinador de Puesto** - 1 por puesto (ej: 1 para Puesto 001)
- **Testigo Electoral** - 1 por puesto (ej: 1 para Puesto 001)

**Regla**: Si hay múltiples usuarios en una ubicación, solo el primero se marca como básico. Los demás son usuarios adicionales/de respaldo que pueden eliminarse en limpieza.

## Referencias

- Modelo User: `backend/models/user.py`
- Inicialización: `backend/utils/init_usuarios_basicos.py`
- Endpoints: `backend/routes/database_backup.py`
- Scripts: `scripts/utils/`
- Documentación: `scripts/utils/README.md`

