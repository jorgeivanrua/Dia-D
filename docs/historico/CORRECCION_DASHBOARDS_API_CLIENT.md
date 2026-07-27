# Corrección de Dashboards - API Client

**Fecha**: 30 de Noviembre de 2025  
**Problema**: Los dashboards no estaban cargando datos de la base de datos

## Problema Identificado

Los dashboards (especialmente Super Admin y Testigo) no estaban cargando los datos correctamente porque faltaba la inclusión explícita del archivo `api-client.js` en algunos templates.

### Síntomas
- Dashboard mostraba 0 en todas las estadísticas
- Errores en consola del navegador sobre `APIClient is undefined`
- Las llamadas a la API no se realizaban correctamente

## Solución Aplicada

### 1. Super Admin Dashboard
**Archivo**: `frontend/templates/admin/super-admin-dashboard.html`

Se agregó la inclusión explícita de `api-client.js` antes de los otros scripts:

```html
{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>

<!-- API Client -->
<script src="{{ url_for('static', filename='js/api-client.js') }}"></script>
<!-- Cargador de datos con manejo de errores -->
<script src="{{ url_for('static', filename='js/dashboard-data-loader.js') }}"></script>
```

### 2. Testigo Dashboard
**Archivo**: `frontend/templates/testigo/dashboard.html`

Se agregó la inclusión de `api-client.js` al inicio del bloque de scripts:

```html
{% block extra_js %}
<!-- API Client (PRIMERO) -->
<script src="{{ url_for('static', filename='js/api-client.js') }}"></script>
<!-- Correcciones de dashboards -->
<script src="{{ url_for('static', filename='js/dashboard-fixes.js') }}"></script>
```

### 3. Base Template
**Archivo**: `frontend/templates/base.html`

Ya incluía `api-client.js` globalmente, pero algunos templates necesitaban la inclusión explícita en su bloque `extra_js` para asegurar el orden de carga correcto.

## Estructura de API Client

El `APIClient` es una clase que maneja todas las comunicaciones con el backend:

```javascript
class APIClient {
    static baseURL = '/api';
    
    static async get(endpoint) {
        // Construye: /api + endpoint
        // Ejemplo: /api/super-admin/stats
    }
    
    static async post(endpoint, data) {
        // POST request
    }
    
    // ... más métodos
}
```

## Endpoints Verificados

### Super Admin
- `GET /api/super-admin/stats` - Estadísticas del dashboard
- `GET /api/super-admin/users` - Lista de usuarios
- `GET /api/super-admin/locations/departamentos` - Departamentos
- `GET /api/super-admin/partidos` - Partidos políticos
- `GET /api/super-admin/candidatos` - Candidatos

### Testigo
- `GET /api/testigo/dashboard-data` - Datos del dashboard
- `POST /api/testigo/formulario` - Enviar formulario
- `GET /api/testigo/mis-formularios` - Formularios del testigo

### Monitoreo
- `GET /api/monitoreo/stats` - Estadísticas en tiempo real
- `GET /api/monitoreo/mapa-data` - Datos para el mapa

## Verificación

Para verificar que los dashboards funcionan correctamente:

1. **Abrir DevTools** (F12)
2. **Ir a Console**
3. **Verificar que no hay errores** de `APIClient is undefined`
4. **Verificar que las llamadas API** se realizan correctamente (pestaña Network)
5. **Verificar que los datos** se muestran en el dashboard

### Comandos de Verificación en Consola

```javascript
// Verificar que APIClient existe
console.log(typeof APIClient); // Debe mostrar: "function"

// Verificar baseURL
console.log(APIClient.baseURL); // Debe mostrar: "/api"

// Probar una llamada
APIClient.get('/super-admin/stats').then(console.log);
```

## Orden de Carga de Scripts

Es importante que los scripts se carguen en este orden:

1. **api-client.js** - Define APIClient
2. **utils.js** - Utilidades generales
3. **dashboard-data-loader.js** - Cargador de datos
4. **[dashboard-específico].js** - Lógica del dashboard
5. **[dashboard]-debug.js** - Scripts de debugging

## Archivos Modificados

1. `frontend/templates/admin/super-admin-dashboard.html`
2. `frontend/templates/testigo/dashboard.html`

## Archivos Relacionados

- `frontend/static/js/api-client.js` - Cliente API
- `frontend/static/js/dashboard-data-loader.js` - Cargador de datos
- `frontend/static/js/utils.js` - Utilidades
- `frontend/templates/base.html` - Template base

## Notas

- El archivo `api-client.js` ya estaba incluido en `base.html`, pero algunos dashboards necesitaban la inclusión explícita para asegurar el orden correcto
- No hay problema en incluir el mismo script múltiples veces, el navegador lo cachea
- Es importante que `api-client.js` se cargue ANTES de cualquier script que use `APIClient`

## Próximos Pasos

1. ✅ Verificar que todos los dashboards cargan datos correctamente
2. ⏳ Revisar otros templates que puedan tener el mismo problema
3. ⏳ Agregar tests automatizados para verificar la carga de datos
4. ⏳ Documentar todos los endpoints de la API

---

**Estado**: ✅ CORREGIDO  
**Probado**: Sí  
**Fecha de corrección**: 30 de Noviembre de 2025
