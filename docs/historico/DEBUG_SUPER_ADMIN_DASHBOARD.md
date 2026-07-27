# Debugging: Super Admin Dashboard No Carga Datos

## Problema

El dashboard de Super Admin muestra "0" en todas las estadísticas.

## Script de Debugging Agregado

Se agregó `super-admin-dashboard-debug.js` que:
- Verifica que APIClient esté disponible
- Verifica que haya token de acceso
- Prueba la carga de perfil
- Prueba la carga de estadísticas
- Actualiza la UI manualmente
- Se ejecuta automáticamente después de 2 segundos

## Cómo Usar

### 1. Abrir Consola del Navegador

1. Ir a `/admin/super-admin-dashboard`
2. Presionar F12 para abrir DevTools
3. Ir a la pestaña "Console"

### 2. Verificar Logs Automáticos

El script se ejecuta automáticamente y mostrará:

```
[Super Admin Debug] Script cargado
[Super Admin Debug] ✓ APIClient disponible
[Super Admin Debug] ✓ Token encontrado: eyJ0eXAiOiJKV1QiLCJ...
[Super Admin Debug] Ejecutando prueba automática...
[Super Admin Debug] === INICIANDO PRUEBA DE CARGA ===
[Super Admin Debug] 1. Verificando perfil...
[Super Admin Debug] Perfil: {success: true, data: {...}}
[Super Admin Debug] Usuario: Admin - Rol: super_admin
[Super Admin Debug] 2. Cargando estadísticas...
[Super Admin Debug] Respuesta stats: {success: true, data: {...}}
[Super Admin Debug] ✓ Estadísticas recibidas:
  - Total Usuarios: 10
  - Total Puestos: 5
  - Total Mesas: 25
  ...
[Super Admin Debug] 3. Actualizando UI...
[Super Admin Debug]   ✓ totalUsuarios = 10
[Super Admin Debug]   ✓ totalPuestos = 5
...
[Super Admin Debug] === PRUEBA COMPLETADA EXITOSAMENTE ===
```

### 3. Ejecutar Manualmente

Si necesitas ejecutar la prueba manualmente:

```javascript
testLoadStats()
```

## Posibles Errores y Soluciones

### Error: "APIClient no está definido"

**Causa**: El script `api-client.js` no se cargó

**Solución**:
1. Verificar que `base.html` incluya el script
2. Verificar que no haya errores de red
3. Recargar la página

### Error: "No hay token de acceso"

**Causa**: El usuario no está autenticado

**Solución**:
1. Cerrar sesión
2. Iniciar sesión nuevamente
3. Verificar que el login funcione correctamente

### Error: "Usuario no es super_admin"

**Causa**: El usuario no tiene el rol correcto

**Solución**:
1. Verificar el rol del usuario en la base de datos
2. Usar un usuario con rol `super_admin`
3. Ejecutar script de corrección de roles si es necesario

### Error: "Error en stats: ..."

**Causa**: El endpoint del backend está fallando

**Solución**:
1. Verificar que el backend esté corriendo
2. Verificar logs del servidor
3. Verificar que el endpoint `/api/super-admin/stats` exista
4. Verificar que el decorador `@role_required` esté funcionando

### Error: "Elemento X no encontrado"

**Causa**: El HTML no tiene el elemento con ese ID

**Solución**:
1. Verificar que el template tenga los elementos correctos
2. Verificar los IDs en el HTML:
   - `totalUsuarios`
   - `totalPuestos`
   - `totalMesas`
   - `totalFormularios`
   - `formulariosPendientes`
   - `totalValidados`
   - `porcentajeValidados`

## Verificar Backend

### 1. Verificar que el Endpoint Existe

```bash
# En el servidor
grep -n "def get_stats" backend/routes/super_admin.py
```

Debería mostrar la función `get_stats()` en la línea correspondiente.

### 2. Probar el Endpoint Directamente

```bash
# Obtener token
TOKEN="tu_token_aqui"

# Probar endpoint
curl -H "Authorization: Bearer $TOKEN" \
     https://dia-d-x7pe.onrender.com/api/super-admin/stats
```

Debería devolver:
```json
{
  "success": true,
  "data": {
    "totalUsuarios": 10,
    "totalPuestos": 5,
    ...
  }
}
```

### 3. Verificar Logs del Servidor

```bash
# Ver logs en Render
# Ir a Dashboard > Logs
# Buscar errores relacionados con /super-admin/stats
```

## Verificar Frontend

### 1. Verificar que los Scripts se Cargan

En la consola del navegador:

```javascript
// Verificar APIClient
console.log(typeof APIClient); // Debería ser "object"

// Verificar funciones
console.log(typeof window.loadMainStats); // Debería ser "function"
console.log(typeof window.initSuperAdminDashboard); // Debería ser "function"
```

### 2. Verificar Orden de Carga

Los scripts deben cargarse en este orden:
1. `api-client.js` (en base.html)
2. `dashboard-data-loader.js`
3. `super-admin-dashboard.js`
4. `personalizacion-sistema.js`
5. `super-admin-dashboard-debug.js`

### 3. Verificar Network Tab

1. Abrir DevTools > Network
2. Recargar la página
3. Buscar la petición a `/api/super-admin/stats`
4. Verificar:
   - Status Code: Debería ser 200
   - Response: Debería tener `success: true`
   - Headers: Debería tener `Authorization: Bearer ...`

## Solución Rápida

Si todo lo demás falla, ejecutar en la consola:

```javascript
// Cargar datos manualmente
async function fixDashboard() {
    try {
        const response = await fetch('/api/super-admin/stats', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            const stats = data.data;
            document.getElementById('totalUsuarios').textContent = stats.totalUsuarios;
            document.getElementById('totalPuestos').textContent = stats.totalPuestos;
            document.getElementById('totalMesas').textContent = stats.totalMesas;
            document.getElementById('totalFormularios').textContent = stats.totalFormularios;
            document.getElementById('formulariosPendientes').textContent = stats.formulariosPendientes;
            document.getElementById('totalValidados').textContent = stats.totalValidados;
            document.getElementById('porcentajeValidados').textContent = stats.porcentajeValidados;
            console.log('✓ Dashboard actualizado');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

fixDashboard();
```

## Contacto

Si el problema persiste después de seguir estos pasos, proporcionar:
1. Logs de la consola del navegador
2. Logs del servidor
3. Respuesta del endpoint `/api/super-admin/stats`
4. Rol del usuario actual
