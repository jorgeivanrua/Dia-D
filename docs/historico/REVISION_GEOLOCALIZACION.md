# REVISIÓN: SISTEMA DE GEOLOCALIZACIÓN

**Fecha:** 1 de Diciembre de 2025  
**Estado:** ⚠️ Parcialmente Implementado

---

## 🔍 ANÁLISIS REALIZADO

Se revisó el sistema de geolocalización en los diferentes dashboards para verificar que las ubicaciones de los puestos se muestren correctamente.

---

## ✅ LO QUE ESTÁ FUNCIONANDO

### 1. Backend - Endpoints
✅ **Archivo:** `backend/routes/locations_geo.py`

#### Endpoint: `/api/locations/puestos-geolocalizados`
- ✅ Implementado correctamente
- ✅ Filtra puestos según rol del usuario
- ✅ Retorna coordenadas (latitud, longitud)
- ✅ Incluye estadísticas (mesas, formularios, avance)
- ✅ Maneja permisos por rol:
  - Super Admin: Todos los puestos
  - Coordinador Departamental: Puestos del departamento
  - Coordinador Municipal: Puestos del municipio
  - Coordinador de Puesto: Solo su puesto
  - Testigo: Puesto de su mesa

#### Endpoint: `/api/locations/mesas-geolocalizadas`
- ✅ Implementado correctamente
- ✅ Retorna mesas con coordenadas
- ✅ Incluye información de testigos asignados

### 2. Frontend - Clase MapaGeolocalizacion
✅ **Archivo:** `frontend/static/js/mapa-geolocalizacion.js`

**Características:**
- ✅ Usa Leaflet para renderizar mapas
- ✅ Markers personalizados para puestos (azul)
- ✅ Markers personalizados para usuarios (verde/amarillo/rojo según estado)
- ✅ Popups con información detallada
- ✅ Actualización automática cada 30 segundos
- ✅ Filtrado según rol del usuario
- ✅ Estilos CSS incluidos

**Métodos principales:**
- `init()` - Inicializa el mapa
- `cargarPuestos()` - Carga puestos desde API
- `cargarUsuarios()` - Carga usuarios desde API
- `agregarMarkerPuesto()` - Agrega marker de puesto
- `agregarMarkerUsuario()` - Agrega marker de usuario
- `actualizar()` - Actualiza datos del mapa

### 3. Super Admin Dashboard
✅ **Archivo:** `frontend/templates/admin/super-admin-dashboard.html`

**Estado:** ✅ **FUNCIONANDO**

- ✅ Leaflet CSS y JS cargados
- ✅ Script `mapa-geolocalizacion.js` cargado
- ✅ Div del mapa presente: `<div id="mapa-geolocalizacion">`
- ✅ Inicialización configurada en tab "Monitoreo"
- ✅ Configuración correcta:
  ```javascript
  new MapaGeolocalizacion('mapa-geolocalizacion', {
      center: [1.6144, -75.6062], // Caquetá
      zoom: 8,
      autoUpdate: true,
      updateInterval: 30000,
      showPuestos: true,
      showUsuarios: true
  });
  ```

---

## ⚠️ LO QUE FALTA IMPLEMENTAR

### 1. Coordinador Departamental
❌ **Archivo:** `frontend/templates/coordinador/departamental.html`

**Problemas:**
- ❌ Leaflet NO está cargado
- ❌ Script `mapa-geolocalizacion.js` NO está cargado
- ❌ Div del mapa existe pero está vacío: `<div id="mapaContainer">`
- ❌ NO hay inicialización del mapa

**Solución necesaria:**
1. Agregar Leaflet CSS y JS
2. Agregar script `mapa-geolocalizacion.js`
3. Inicializar mapa en el tab "Mapa"
4. Cambiar ID del div a `mapa-departamental`

### 2. Coordinador Municipal
❌ **Archivo:** `frontend/templates/coordinador/municipal.html`

**Estado:** No revisado aún (probablemente igual que departamental)

**Solución necesaria:**
1. Verificar si tiene tab de mapa
2. Agregar Leaflet y script de geolocalización
3. Inicializar mapa con filtro municipal

### 3. Coordinador de Puesto
❌ **Archivo:** `frontend/templates/coordinador/puesto.html`

**Estado:** No revisado aún

**Solución necesaria:**
1. Verificar si tiene tab de mapa
2. Agregar Leaflet y script de geolocalización
3. Inicializar mapa con filtro de puesto

### 4. Dashboard de Monitoreo
❓ **Archivo:** `frontend/templates/monitoreo/*`

**Estado:** No revisado aún

**Solución necesaria:**
1. Verificar si existe dashboard de monitoreo
2. Agregar mapa si no existe
3. Configurar para mostrar todos los puestos

---

## 🔧 CORRECCIONES NECESARIAS

### Prioridad 1: Coordinador Departamental

#### Paso 1: Agregar Leaflet y Script
```html
<!-- En la sección {% block extra_js %} -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="{{ url_for('static', filename='js/mapa-geolocalizacion.js') }}?v=20251201"></script>
```

#### Paso 2: Cambiar ID del div
```html
<!-- Cambiar de: -->
<div id="mapaContainer" style="height: 500px;">

<!-- A: -->
<div id="mapa-departamental" style="height: 500px; border-radius: 8px;"></div>
```

#### Paso 3: Inicializar Mapa
```javascript
// Cuando se abre el tab de mapa
const mapaTab = document.getElementById('mapa-tab');
if (mapaTab) {
    mapaTab.addEventListener('shown.bs.tab', function() {
        if (!window.mapaDepartamental) {
            console.log('Inicializando mapa departamental...');
            window.mapaDepartamental = new MapaGeolocalizacion('mapa-departamental', {
                center: [1.6144, -75.6062], // Caquetá
                zoom: 9,
                autoUpdate: true,
                updateInterval: 30000,
                showPuestos: true,
                showUsuarios: true
            });
            window.mapaDepartamental.init();
        }
    });
}
```

### Prioridad 2: Coordinador Municipal

Similar al departamental, pero con:
- ID: `mapa-municipal`
- Zoom: 11 (más cercano)
- Filtrado automático por municipio del coordinador

### Prioridad 3: Coordinador de Puesto

Similar, pero con:
- ID: `mapa-puesto`
- Zoom: 15 (muy cercano)
- Centrado en el puesto específico
- Solo muestra su puesto y usuarios asignados

---

## 📊 RESUMEN DE ESTADO

| Dashboard | Leaflet | Script Geo | Div Mapa | Inicialización | Estado |
|-----------|---------|------------|----------|----------------|--------|
| Super Admin | ✅ | ✅ | ✅ | ✅ | ✅ Funcionando |
| Coordinador Dept | ❌ | ❌ | ⚠️ | ❌ | ❌ No funciona |
| Coordinador Mun | ❓ | ❓ | ❓ | ❓ | ❓ Por revisar |
| Coordinador Puesto | ❓ | ❓ | ❓ | ❓ | ❓ Por revisar |
| Monitoreo | ❓ | ❓ | ❓ | ❓ | ❓ Por revisar |

---

## 🎯 PLAN DE ACCIÓN

### Fase 1: Coordinador Departamental (Inmediato)
1. ✅ Agregar Leaflet CSS y JS
2. ✅ Agregar script de geolocalización
3. ✅ Cambiar ID del div del mapa
4. ✅ Agregar inicialización del mapa
5. ✅ Probar funcionamiento

### Fase 2: Coordinador Municipal (Siguiente)
1. Revisar template actual
2. Agregar componentes necesarios
3. Configurar filtrado por municipio
4. Probar funcionamiento

### Fase 3: Coordinador de Puesto (Siguiente)
1. Revisar template actual
2. Agregar componentes necesarios
3. Configurar filtrado por puesto
4. Centrar en ubicación específica
5. Probar funcionamiento

### Fase 4: Dashboard de Monitoreo (Opcional)
1. Verificar si existe
2. Agregar mapa si es necesario
3. Configurar vista general

---

## 🔍 VERIFICACIÓN

### Para verificar que funciona:

1. **Super Admin (Ya funciona):**
   - Login como super_admin
   - Ir a dashboard
   - Click en tab "Monitoreo"
   - Verificar que aparece el mapa
   - Verificar que se muestran puestos (markers azules)
   - Verificar que se muestran usuarios (markers verde/amarillo/rojo)

2. **Coordinador Departamental (Después de corrección):**
   - Login como coordinador_departamental
   - Ir a dashboard
   - Click en tab "Mapa"
   - Verificar que aparece el mapa
   - Verificar que solo se muestran puestos del departamento
   - Verificar que se muestran usuarios del departamento

3. **Coordinador Municipal (Después de corrección):**
   - Login como coordinador_municipal
   - Ir a dashboard
   - Click en tab "Mapa"
   - Verificar que aparece el mapa
   - Verificar que solo se muestran puestos del municipio

4. **Coordinador de Puesto (Después de corrección):**
   - Login como coordinador_puesto
   - Ir a dashboard
   - Click en tab "Mapa"
   - Verificar que aparece el mapa centrado en su puesto
   - Verificar que solo se muestra su puesto

---

## 📝 NOTAS TÉCNICAS

### Requisitos de Datos:
Para que los puestos aparezcan en el mapa, deben tener:
- ✅ `latitud` no nula
- ✅ `longitud` no nula
- ✅ `activo = True`
- ✅ `tipo = 'puesto'`

### Formato de Coordenadas:
- Latitud: -90 a 90 (decimal)
- Longitud: -180 a 180 (decimal)
- Ejemplo Caquetá: `1.6144, -75.6062`

### Carga de Datos DIVIPOLA:
Si los puestos no tienen coordenadas, se pueden cargar usando el sistema de carga masiva CSV con el formato:
```csv
departamento_codigo,departamento_nombre,municipio_codigo,municipio_nombre,zona_codigo,puesto_codigo,puesto_nombre,direccion,latitud,longitud
18,CAQUETÁ,001,FLORENCIA,00,01,Puesto Centro,Calle 11 # 5-42,1.6143,-75.6062
```

---

## ✅ CONCLUSIÓN

**Estado Actual:**
- ✅ Super Admin: **FUNCIONANDO**
- ❌ Coordinadores: **NO FUNCIONANDO** (falta implementar)

**Próximo Paso:**
Implementar geolocalización en los dashboards de coordinadores siguiendo el plan de acción.

---

**Sistema Electoral del Caquetá**  
**Revisión de Geolocalización**  
**Versión 1.0.0 - Diciembre 2025**
