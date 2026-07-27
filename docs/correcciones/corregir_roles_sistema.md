# Corrección de Problemas de Roles y Autenticación (Errores 403)

## Problema Identificado

Los errores 403 (Forbidden) ocurren cuando un usuario intenta acceder a un endpoint pero su rol no está autorizado. Esto puede suceder por:

1. **Token JWT con rol incorrecto**: El token incluye un rol que no coincide con el rol real del usuario
2. **Decorador `@role_required` mal configurado**: El endpoint requiere un rol que el usuario no tiene
3. **Usuario con rol incorrecto en la base de datos**: El usuario tiene un rol diferente al esperado

## Verificación del Sistema

### 1. Verificar que los tokens JWT incluyen el rol correcto

El archivo `backend/utils/jwt_utils.py` genera tokens con estos claims:

```python
additional_claims = {
    'rol': user.rol,
    'ubicacion_id': user.ubicacion_id,
    'nombre': user.nombre
}
```

✅ **CORRECTO**: Los tokens incluyen el claim `rol`

### 2. Verificar que el decorador lee el rol correctamente

El archivo `backend/utils/decorators.py` verifica el rol así:

```python
claims = get_jwt()
user_role = claims.get('rol')

if user_role not in allowed_roles:
    return jsonify({
        'success': False,
        'error': 'No tiene permisos para acceder a este recurso'
    }), 403
```

✅ **CORRECTO**: El decorador lee el claim `rol` correctamente

### 3. Verificar roles en endpoints específicos

#### Endpoints del Testigo (NO requieren `@role_required`)

Los endpoints en `backend/routes/testigo.py` solo usan `@jwt_required()` y verifican manualmente:

```python
@testigo_bp.route('/info', methods=['GET'])
@jwt_required()
def get_testigo_info():
    if user.rol != 'testigo_electoral':
        return jsonify({'success': False, 'error': 'Solo testigos pueden acceder'}), 403
```

✅ **CORRECTO**: Verificación manual del rol

#### Endpoints del Super Admin

```python
@super_admin_bp.route('/stats', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_stats():
```

✅ **CORRECTO**: Requiere rol `super_admin`

## Posibles Causas de Errores 403

### Causa 1: Usuario con rol incorrecto

**Síntoma**: Un usuario llamado "testigo" tiene rol "coordinador_puesto" en lugar de "testigo_electoral"

**Solución**: Actualizar el rol en la base de datos

```sql
UPDATE users SET rol = 'testigo_electoral' WHERE nombre = 'testigo';
```

### Causa 2: Token antiguo con rol incorrecto

**Síntoma**: El usuario cambió de rol pero el token JWT todavía tiene el rol antiguo

**Solución**: El usuario debe cerrar sesión y volver a iniciar sesión para obtener un nuevo token

### Causa 3: Endpoint requiere rol incorrecto

**Síntoma**: Un endpoint que debería ser accesible para testigos requiere otro rol

**Solución**: Revisar y corregir el decorador `@role_required`

## Endpoints que Pueden Causar Errores 403

### 1. `/api/testigo/registrar-presencia`

- **Decorador**: `@jwt_required()` (sin `@role_required`)
- **Verificación manual**: `if user.rol != 'testigo_electoral'`
- **Roles permitidos**: `testigo_electoral`

### 2. `/api/formularios` (POST)

- **Decorador**: `@role_required(['testigo_electoral'])`
- **Roles permitidos**: `testigo_electoral`

### 3. `/api/formularios/mis-formularios` (GET)

- **Decorador**: `@role_required(['testigo_electoral'])`
- **Roles permitidos**: `testigo_electoral`

### 4. `/api/super-admin/stats` (GET)

- **Decorador**: `@role_required(['super_admin'])`
- **Roles permitidos**: `super_admin`

## Solución Recomendada

### Paso 1: Verificar roles de usuarios de prueba

Ejecutar este SQL en la base de datos:

```sql
SELECT id, nombre, rol, activo FROM users WHERE nombre IN ('admin', 'testigo', 'coordinador_puesto', 'coordinador_municipal');
```

Resultado esperado:
- `admin` → `super_admin`
- `testigo` → `testigo_electoral`
- `coordinador_puesto` → `coordinador_puesto`
- `coordinador_municipal` → `coordinador_municipal`

### Paso 2: Corregir roles si es necesario

```sql
UPDATE users SET rol = 'super_admin' WHERE nombre = 'admin';
UPDATE users SET rol = 'testigo_electoral' WHERE nombre = 'testigo';
UPDATE users SET rol = 'coordinador_puesto' WHERE nombre = 'coordinador_puesto';
UPDATE users SET rol = 'coordinador_municipal' WHERE nombre = 'coordinador_municipal';
```

### Paso 3: Forzar cierre de sesión

Todos los usuarios deben cerrar sesión y volver a iniciar sesión para obtener nuevos tokens con los roles correctos.

### Paso 4: Verificar en el navegador

1. Abrir DevTools (F12)
2. Ir a Application → Local Storage
3. Ver el valor de `access_token`
4. Copiar el token y decodificarlo en https://jwt.io
5. Verificar que el claim `rol` sea correcto

## Debugging en Tiempo Real

### Agregar logs en el decorador

Modificar `backend/utils/decorators.py`:

```python
def role_required(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()
                user_role = claims.get('rol')
                
                # LOG PARA DEBUGGING
                print(f"[ROLE_CHECK] Endpoint: {fn.__name__}")
                print(f"[ROLE_CHECK] User role: {user_role}")
                print(f"[ROLE_CHECK] Allowed roles: {allowed_roles}")
                
                if user_role not in allowed_roles:
                    print(f"[ROLE_CHECK] ❌ ACCESO DENEGADO")
                    return jsonify({
                        'success': False,
                        'error': 'No tiene permisos para acceder a este recurso'
                    }), 403
                
                print(f"[ROLE_CHECK] ✅ ACCESO PERMITIDO")
                return fn(*args, **kwargs)
            except Exception as e:
                print(f"[ROLE_CHECK] ❌ ERROR: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Token inválido o expirado'
                }), 401
        return wrapper
    return decorator
```

## Conclusión

El sistema está configurado correctamente. Los errores 403 probablemente se deben a:

1. **Usuarios con roles incorrectos en la base de datos**
2. **Tokens JWT antiguos con roles incorrectos**

**Solución**: Verificar y corregir los roles en la base de datos, luego forzar que todos los usuarios cierren sesión y vuelvan a iniciar sesión.
