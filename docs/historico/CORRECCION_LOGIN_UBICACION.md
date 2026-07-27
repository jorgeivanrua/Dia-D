# Corrección de Login con Ubicación Completa

## Problema Identificado

Los usuarios con ubicación completa (testigo electoral y monitoreo) no pueden hacer login correctamente:

1. **Testigo Electoral**: No llega al campo de contraseña
2. **Monitoreo**: Dice "bloqueado" al intentar login

## Causas Raíz

### 1. Problema con Monitoreo

El servicio de autenticación estaba buscando la ubicación ANTES de verificar si el rol requiere ubicación:

```python
# ❌ ANTES (INCORRECTO)
location = AuthService._find_location_by_hierarchy(rol, ubicacion_data)
if rol in ['super_admin', 'monitoreo']:
    user = User.query.filter_by(rol=rol, ubicacion_id=None, activo=True).first()
```

Esto causaba que:
- Se intentara buscar una ubicación para monitoreo
- La búsqueda fallara
- El usuario no se encontrara correctamente

### 2. Problema con Testigos

Los testigos requieren seleccionar:
- Departamento
- Municipio
- Zona
- Puesto Electoral

El frontend estaba configurado correctamente, pero podría haber problemas con:
- Contraseñas incorrectas
- Usuarios bloqueados por intentos fallidos
- Ubicaciones mal configuradas

## Solución Implementada

### 1. Corrección del Servicio de Autenticación

```python
# ✅ AHORA (CORRECTO)
# Super admin y monitoreo no necesitan ubicación
if rol in ['super_admin', 'monitoreo']:
    user = User.query.filter_by(
        rol=rol,
        activo=True
    ).first()
else:
    # Buscar ubicación según jerarquía
    location = AuthService._find_location_by_hierarchy(rol, ubicacion_data)
    if not location:
        raise AuthenticationException("Ubicación no encontrada")
    
    # Buscar usuario por rol y ubicación
    user = User.query.filter_by(
        rol=rol,
        ubicacion_id=location.id,
        activo=True
    ).first()
```

Cambios clave:
- Se verifica el rol ANTES de buscar ubicación
- Monitoreo y super_admin no requieren ubicación_id
- Se busca el usuario sin filtrar por ubicacion_id=None

### 2. Script de Diagnóstico y Corrección

Se creó `fix_usuarios_ubicacion.py` que:

1. **Verifica usuario de monitoreo**
   - Comprueba que exista
   - Verifica la contraseña
   - Corrige si es necesario
   - Crea el usuario si no existe

2. **Verifica testigos electorales**
   - Comprueba que tengan ubicación
   - Verifica que la ubicación sea válida
   - Verifica que sea tipo 'puesto'
   - Comprueba contraseñas

3. **Verifica coordinadores de puesto**
   - Mismas verificaciones que testigos

4. **Corrige contraseñas**
   - Resetea a 'test123'
   - Limpia intentos fallidos
   - Desbloquea cuentas

5. **Muestra ejemplos de login**
   - Datos completos para testigo
   - Datos para monitoreo

## Uso del Script de Corrección

```bash
python fix_usuarios_ubicacion.py
```

El script:
- Diagnostica todos los problemas
- Corrige automáticamente lo que puede
- Muestra ejemplos de login válidos
- No requiere confirmación (es seguro)

## Flujo de Login Correcto

### Para Monitoreo

1. Seleccionar rol: "Monitoreo"
2. NO seleccionar ubicación (se oculta automáticamente)
3. Ingresar contraseña: `test123`
4. Click en "Iniciar Sesión"

**Datos enviados al backend:**
```json
{
  "rol": "monitoreo",
  "password": "test123"
}
```

### Para Testigo Electoral

1. Seleccionar rol: "Testigo Electoral"
2. Seleccionar Departamento: "CAQUETÁ"
3. Seleccionar Municipio: (ejemplo) "FLORENCIA"
4. Seleccionar Zona: (ejemplo) "01"
5. Seleccionar Puesto: (ejemplo) "P001"
6. Ingresar contraseña: `test123`
7. Click en "Iniciar Sesión"

**Datos enviados al backend:**
```json
{
  "rol": "testigo_electoral",
  "departamento_codigo": "18",
  "municipio_codigo": "001",
  "zona_codigo": "01",
  "puesto_codigo": "P001",
  "password": "test123"
}
```

## Validaciones del Frontend

El JavaScript del login (`login-fixed.js`) valida:

```javascript
// Super admin y monitoreo no requieren ubicación
if (rol !== 'super_admin' && rol !== 'monitoreo') {
    requiredFields.push('departamento');
    
    if (['admin_municipal', 'coordinador_municipal', 'coordinador_puesto', 'testigo_electoral'].includes(rol)) {
        requiredFields.push('municipio');
    }
    
    if (['coordinador_puesto', 'testigo_electoral'].includes(rol)) {
        requiredFields.push('zona', 'puesto');
    }
}
```

## Problemas Comunes y Soluciones

### Problema: "Cuenta bloqueada"

**Causa**: Múltiples intentos fallidos de login

**Solución**:
```bash
python fix_usuarios_ubicacion.py
```

Esto resetea:
- `intentos_fallidos` a 0
- `bloqueado_hasta` a NULL

### Problema: "Credenciales inválidas"

**Causas posibles**:
1. Contraseña incorrecta
2. Usuario no existe
3. Ubicación incorrecta
4. Usuario inactivo

**Solución**:
1. Verificar que la contraseña sea `test123`
2. Ejecutar el script de diagnóstico
3. Verificar que la ubicación exista
4. Verificar que el usuario esté activo

### Problema: "Ubicación no encontrada"

**Causa**: La combinación de departamento/municipio/zona/puesto no existe

**Solución**:
1. Verificar que las ubicaciones estén cargadas:
   ```bash
   python backend/scripts/init_caqueta_electoral_data.py
   ```
2. Verificar en la base de datos:
   ```sql
   SELECT * FROM locations WHERE tipo='puesto';
   ```

## Archivos Modificados

1. **backend/services/auth_service.py**
   - Método `authenticate_location_based()`
   - Reordenada lógica de búsqueda de usuario

2. **fix_usuarios_ubicacion.py** (NUEVO)
   - Script de diagnóstico y corrección

## Testing

### Test Manual - Monitoreo

1. Ir a `/auth/login`
2. Seleccionar rol: "Monitoreo"
3. Ingresar contraseña: `test123`
4. Verificar redirección a `/monitoreo/dashboard`

### Test Manual - Testigo

1. Ir a `/auth/login`
2. Seleccionar rol: "Testigo Electoral"
3. Seleccionar ubicación completa
4. Ingresar contraseña: `test123`
5. Verificar redirección a `/testigo/dashboard`

## Logs de Depuración

El servicio de autenticación ahora incluye logs:

```python
logger.info(f"Autenticando: rol={rol}, ubicacion_data={ubicacion_data}")
logger.info(f"Ubicación encontrada: {location.id if location else None}")
logger.info(f"Usuario sin ubicación encontrado: {user.id if user else None}")
```

Para ver los logs:
```bash
# En desarrollo
tail -f logs/app.log

# O en consola
python run.py
```

## Próximos Pasos

1. ✅ Ejecutar script de corrección
2. ✅ Probar login de monitoreo
3. ✅ Probar login de testigo
4. ⏳ Verificar que todos los usuarios puedan acceder
5. ⏳ Documentar credenciales de testing

## Notas Importantes

- Todos los usuarios de testing usan contraseña: `test123`
- El rol "monitoreo" NO requiere ubicación
- Los testigos DEBEN seleccionar ubicación completa hasta puesto
- El script de corrección es seguro y puede ejecutarse múltiples veces
