# Solución a Errores 403 (Forbidden) - Sistema Electoral

## Problema

Los usuarios experimentaban errores 403 al intentar acceder a ciertos endpoints del sistema. Esto ocurría porque:

1. Los roles de los usuarios no coincidían con los roles esperados por los endpoints
2. Las contraseñas podían estar en formato incorrecto
3. Los tokens JWT antiguos contenían información desactualizada

## Solución Implementada

### 1. Herramientas Administrativas (Backend)

Se agregaron 3 nuevos endpoints en `backend/routes/admin_tools.py`:

#### `/api/admin/fix-roles` (POST)
- **Función**: Corrige los roles de usuarios de prueba
- **Acceso**: Solo super_admin
- **Acciones**:
  - Corrige roles incorrectos
  - Actualiza contraseñas a texto plano
  - Activa usuarios inactivos
  - Resetea intentos fallidos y bloqueos

#### `/api/admin/diagnostico` (GET)
- **Función**: Diagnóstico completo del sistema
- **Acceso**: Solo super_admin
- **Información**:
  - Estadísticas de usuarios
  - Usuarios por rol
  - Estado de usuarios de prueba
  - Problemas detectados

#### `/api/admin/fix-passwords` (POST)
- **Función**: Actualiza contraseñas a texto plano
- **Acceso**: Solo super_admin
- **Ya existía**: Se mantuvo sin cambios

### 2. Interfaz de Usuario (Frontend)

Se actualizó el dashboard del Super Admin con 3 nuevos botones:

#### Botón "Diagnóstico del Sistema"
- **Función JavaScript**: `runDiagnostico()`
- **Acción**: Muestra un reporte completo del estado del sistema
- **Ubicación**: Dashboard Super Admin → Testing & Diagnóstico

#### Botón "Corregir Roles"
- **Función JavaScript**: `fixRoles()`
- **Acción**: Corrige roles de usuarios de prueba
- **Ubicación**: Dashboard Super Admin → Testing & Diagnóstico

#### Botón "Arreglar Contraseñas"
- **Ya existía**: Se mantuvo sin cambios

### 3. Scripts de Línea de Comandos

Se crearon scripts para ejecutar localmente:

#### `scripts/corregir_roles_universal.py`
- **Función**: Corrige roles usando SQLAlchemy
- **Compatible con**: SQLite (local) y PostgreSQL (Render)
- **Uso**: `python scripts/corregir_roles_universal.py`

#### `scripts/verificar_y_corregir_roles.sql`
- **Función**: Queries SQL para verificar y corregir roles
- **Compatible con**: SQLite y PostgreSQL (con ajustes menores)

## Cómo Usar las Herramientas

### Opción 1: Desde el Dashboard (Recomendado para Render)

1. Iniciar sesión como Super Admin (admin / admin123)
2. Ir al Dashboard del Super Admin
3. En la sección "Testing & Diagnóstico":
   - Clic en **"Diagnóstico del Sistema"** para ver el estado actual
   - Clic en **"Corregir Roles"** para aplicar correcciones
4. Todos los usuarios deben cerrar sesión y volver a iniciar sesión

### Opción 2: Desde Línea de Comandos (Local)

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
.\venv\Scripts\activate   # Windows

# Ejecutar script
python scripts/corregir_roles_universal.py
```

### Opción 3: Desde SQL (Avanzado)

```bash
# SQLite (local)
sqlite3 instance/electoral.db < scripts/verificar_y_corregir_roles.sql

# PostgreSQL (Render)
psql $DATABASE_URL < scripts/verificar_y_corregir_roles.sql
```

## Usuarios de Prueba Corregidos

Después de ejecutar las correcciones, estos son los usuarios de prueba:

| Usuario | Rol | Contraseña |
|---------|-----|------------|
| admin | super_admin | admin123 |
| testigo | testigo_electoral | test123 |
| coordinador_puesto | coordinador_puesto | test123 |
| coordinador_municipal | coordinador_municipal | test123 |
| coordinador_departamental | coordinador_departamental | test123 |

## Importante: Tokens JWT

### ¿Por qué cerrar sesión?

Los tokens JWT incluyen el rol del usuario en sus claims:

```json
{
  "rol": "testigo_electoral",
  "ubicacion_id": 123,
  "nombre": "testigo"
}
```

Si el rol se corrige en la base de datos pero el usuario no cierra sesión, el token antiguo seguirá teniendo el rol incorrecto, causando errores 403.

### Solución

**Todos los usuarios deben**:
1. Cerrar sesión
2. Volver a iniciar sesión
3. Esto generará un nuevo token con el rol correcto

## Verificación

### Verificar que las correcciones funcionaron

1. **Diagnóstico del Sistema**:
   - Dashboard Super Admin → "Diagnóstico del Sistema"
   - Verificar que no haya problemas

2. **Probar Login**:
   - Cerrar sesión
   - Iniciar sesión con cada usuario de prueba
   - Verificar que no haya errores 403

3. **Verificar Token JWT**:
   - Abrir DevTools (F12)
   - Application → Local Storage
   - Copiar `access_token`
   - Ir a https://jwt.io
   - Pegar el token
   - Verificar que el claim `rol` sea correcto

## Diferencias entre Local y Render

### Local (SQLite)
- Base de datos: `instance/electoral.db`
- Archivo físico en disco
- Scripts SQL directos funcionan
- Más fácil de resetear

### Render (PostgreSQL)
- Base de datos: PostgreSQL en la nube
- URL de conexión en variable de entorno `DATABASE_URL`
- Usar herramientas del dashboard
- Más difícil de resetear (requiere acceso a Render)

## Archivos Modificados

### Backend
- `backend/routes/admin_tools.py` - Agregados endpoints de diagnóstico y corrección

### Frontend
- `frontend/templates/admin/super-admin-dashboard.html` - Agregados botones
- `frontend/static/js/super-admin-dashboard.js` - Agregadas funciones JavaScript

### Scripts
- `scripts/corregir_roles_universal.py` - Script universal para corrección
- `scripts/verificar_y_corregir_roles.sql` - Queries SQL de verificación

### Documentación
- `SOLUCION_ERRORES_403.md` - Este documento
- `corregir_roles_sistema.md` - Análisis técnico del problema

## Próximos Pasos

1. **Probar en Local**:
   - Ejecutar diagnóstico
   - Corregir roles si es necesario
   - Verificar que no haya errores 403

2. **Desplegar a Render**:
   - Hacer commit de los cambios
   - Push a GitHub
   - Render desplegará automáticamente

3. **Probar en Render**:
   - Iniciar sesión como admin
   - Ejecutar diagnóstico desde el dashboard
   - Corregir roles si es necesario
   - Notificar a todos los usuarios que cierren sesión

## Soporte

Si los errores 403 persisten después de aplicar estas correcciones:

1. Verificar que el usuario cerró sesión y volvió a iniciar sesión
2. Ejecutar diagnóstico del sistema
3. Verificar el token JWT en https://jwt.io
4. Revisar los logs del servidor para más detalles
5. Verificar que el endpoint tenga el decorador `@role_required` correcto

## Conclusión

El sistema ahora tiene herramientas integradas para:
- ✅ Diagnosticar problemas de roles y permisos
- ✅ Corregir roles automáticamente
- ✅ Funcionar tanto en SQLite (local) como PostgreSQL (Render)
- ✅ Ser accesible desde el dashboard sin necesidad de línea de comandos

Los errores 403 deberían resolverse después de:
1. Ejecutar "Corregir Roles"
2. Todos los usuarios cierran sesión
3. Todos los usuarios vuelven a iniciar sesión
