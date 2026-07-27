# Scripts de Debugging para Todos los Roles

## Descripción

Se han creado scripts de debugging automático para todos los roles principales del sistema. Estos scripts:

- ✅ Se ejecutan automáticamente 2 segundos después de cargar la página
- ✅ Verifican paso a paso todas las funcionalidades
- ✅ Muestran logs detallados en la consola del navegador
- ✅ Identifican exactamente qué está fallando
- ✅ Pueden ejecutarse manualmente cuando sea necesario

---

## Scripts Creados

### 1. Super Admin Dashboard
**Archivo**: `frontend/static/js/super-admin-dashboard-debug.js`  
**Template**: `frontend/templates/admin/super-admin-dashboard.html`  
**Función**: `testLoadStats()`

**Verifica**:
- ✅ APIClient disponible
- ✅ Token de acceso
- ✅ Perfil del usuario
- ✅ Rol super_admin
- ✅ Carga de estadísticas
- ✅ Actualización de UI

**Uso**:
```javascript
// Ejecutar manualmente en consola
testLoadStats()
```

---

### 2. Testigo Dashboard
**Archivo**: `frontend/static/js/testigo-dashboard-debug.js`  
**Template**: `frontend/templates/testigo/dashboard.html`  
**Función**: `testTestigoDashboard()`

**Verifica**:
- ✅ APIClient disponible
- ✅ Token de acceso
- ✅ Perfil del usuario
- ✅ Rol testigo_electoral
- ✅ Tipos de elección
- ✅ Partidos políticos
- ✅ Mesas disponibles
- ✅ Estado de presencia
- ✅ Botones (desktop y móvil)
- ✅ Formularios E-14
- ✅ Funciones de incidentes/delitos

**Uso**:
```javascript
// Ejecutar manualmente en consola
testTestigoDashboard()
```

---

### 3. Monitoreo Dashboard
**Archivo**: `frontend/static/js/monitoreo-dashboard-debug.js`  
**Template**: `frontend/templates/monitoreo/dashboard.html`  
**Función**: `testMonitoreoDashboard()`

**Verifica**:
- ✅ APIClient disponible
- ✅ Token de acceso
- ✅ Perfil del usuario
- ✅ Rol monitoreo
- ✅ Usuarios activos
- ✅ Estadísticas generales
- ✅ Mapa Leaflet
- ✅ Métricas de rendimiento
- ✅ Filtros

**Uso**:
```javascript
// Ejecutar manualmente en consola
testMonitoreoDashboard()
```

---

### 4. Coordinador Dashboard
**Archivo**: `frontend/static/js/coordinador-dashboard-debug.js`  
**Template**: Múltiples (puesto, municipal, departamental)  
**Función**: `testCoordinadorDashboard()`

**Verifica**:
- ✅ APIClient disponible
- ✅ Token de acceso
- ✅ Perfil del usuario
- ✅ Rol coordinador (puesto/municipal/departamental)
- ✅ Tipo de coordinador
- ✅ Formularios según nivel
- ✅ Estadísticas
- ✅ Tabla de formularios
- ✅ Funciones de validación
- ✅ Panel de mesas (para puesto)

**Uso**:
```javascript
// Ejecutar manualmente en consola
testCoordinadorDashboard()
```

---

## Cómo Usar

### Ejecución Automática

Los scripts se ejecutan automáticamente 2 segundos después de cargar la página:

1. Abrir el dashboard correspondiente
2. Abrir DevTools (F12)
3. Ir a la pestaña "Console"
4. Esperar 2 segundos
5. Ver los logs detallados

### Ejecución Manual

Si necesitas ejecutar el test nuevamente:

```javascript
// Super Admin
testLoadStats()

// Testigo
testTestigoDashboard()

// Monitoreo
testMonitoreoDashboard()

// Coordinador
testCoordinadorDashboard()
```

---

## Interpretación de Logs

### ✓ Símbolo Verde
Indica que la verificación fue exitosa.

**Ejemplo**:
```
[Testigo Debug] ✓ APIClient disponible
[Testigo Debug] ✓ Token encontrado
[Testigo Debug] ✓ Tipos de elección: 5
```

### ❌ Símbolo Rojo
Indica un error crítico que impide el funcionamiento.

**Ejemplo**:
```
[Testigo Debug] ❌ APIClient no está definido
[Testigo Debug] ❌ No hay token de acceso
[Testigo Debug] ❌ Usuario no es testigo_electoral
```

### ⚠️ Símbolo Amarillo
Indica una advertencia o funcionalidad opcional que no está disponible.

**Ejemplo**:
```
[Testigo Debug] ⚠️ No se pudieron cargar tipos de elección
[Testigo Debug] ⚠️ Selector de mesa no encontrado
```

---

## Solución de Problemas Comunes

### Error: "APIClient no está definido"

**Causa**: El script `api-client.js` no se cargó correctamente.

**Solución**:
1. Verificar que `base.html` incluya el script
2. Verificar la consola de red (Network tab)
3. Recargar la página

### Error: "No hay token de acceso"

**Causa**: El usuario no está autenticado.

**Solución**:
1. Cerrar sesión
2. Iniciar sesión nuevamente
3. Verificar que el login funcione

### Error: "Usuario no es [rol]"

**Causa**: El usuario no tiene el rol correcto.

**Solución**:
1. Verificar el rol en la base de datos
2. Usar un usuario con el rol correcto
3. Ejecutar script de corrección de roles

### Error: "Error cargando [recurso]"

**Causa**: El endpoint del backend no está disponible o está fallando.

**Solución**:
1. Verificar que el backend esté corriendo
2. Verificar logs del servidor
3. Verificar que el endpoint exista
4. Verificar permisos del rol

---

## Agregar Script a Nuevos Dashboards

Si necesitas agregar debugging a un nuevo dashboard:

### 1. Crear el Script

```javascript
/**
 * Script de debugging para [Nombre] Dashboard
 */

console.log('[Nombre Debug] Script cargado');

// Verificar dependencias
if (typeof APIClient === 'undefined') {
    console.error('[Nombre Debug] ❌ APIClient no está definido');
} else {
    console.log('[Nombre Debug] ✓ APIClient disponible');
}

// Función de prueba
window.testNombreDashboard = async function() {
    console.log('[Nombre Debug] === INICIANDO PRUEBA ===');
    
    try {
        // 1. Verificar perfil
        const profileResponse = await APIClient.getProfile();
        console.log('[Nombre Debug] Perfil:', profileResponse);
        
        // 2. Verificar datos específicos
        // ... tu código aquí
        
        console.log('[Nombre Debug] === PRUEBA COMPLETADA ===');
    } catch (error) {
        console.error('[Nombre Debug] ❌ Error:', error);
    }
};

// Ejecutar automáticamente
setTimeout(() => {
    window.testNombreDashboard();
}, 2000);
```

### 2. Agregar al Template

```html
<!-- Script de debugging -->
<script src="{{ url_for('static', filename='js/nombre-dashboard-debug.js') }}"></script>
```

---

## Archivos Modificados

### Scripts Creados
1. `frontend/static/js/super-admin-dashboard-debug.js`
2. `frontend/static/js/testigo-dashboard-debug.js`
3. `frontend/static/js/monitoreo-dashboard-debug.js`
4. `frontend/static/js/coordinador-dashboard-debug.js`

### Templates Modificados
1. `frontend/templates/admin/super-admin-dashboard.html`
2. `frontend/templates/testigo/dashboard.html`
3. `frontend/templates/monitoreo/dashboard.html`

### Documentación
1. `docs/DEBUG_SUPER_ADMIN_DASHBOARD.md`
2. `docs/SCRIPTS_DEBUGGING_TODOS_ROLES.md` (este archivo)

---

## Beneficios

### Para Desarrollo
- ✅ Identificación rápida de problemas
- ✅ Logs detallados para debugging
- ✅ Verificación automática de dependencias
- ✅ Pruebas de integración en tiempo real

### Para Producción
- ✅ Diagnóstico remoto de problemas
- ✅ Verificación de conectividad
- ✅ Monitoreo de funcionalidad
- ✅ Soporte técnico más eficiente

### Para Usuarios
- ✅ Problemas se identifican automáticamente
- ✅ Mensajes de error más claros
- ✅ Soluciones más rápidas
- ✅ Mejor experiencia general

---

## Desactivar en Producción (Opcional)

Si deseas desactivar los scripts de debugging en producción:

### Opción 1: Comentar en Templates

```html
<!-- Script de debugging -->
<!-- <script src="{{ url_for('static', filename='js/...-debug.js') }}"></script> -->
```

### Opción 2: Condicional por Entorno

```html
{% if config.DEBUG %}
<!-- Script de debugging -->
<script src="{{ url_for('static', filename='js/...-debug.js') }}"></script>
{% endif %}
```

### Opción 3: Mantener Activos

Los scripts son ligeros y solo se ejecutan una vez. No afectan el rendimiento significativamente y pueden ser útiles para soporte técnico.

---

## Conclusión

Los scripts de debugging proporcionan una forma sistemática y automática de verificar que todos los dashboards funcionen correctamente. Facilitan el desarrollo, el debugging y el soporte técnico.

**Recomendación**: Mantener los scripts activos incluso en producción para facilitar el diagnóstico remoto de problemas.
