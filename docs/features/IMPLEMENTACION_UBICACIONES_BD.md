# Implementación de Carga de Ubicaciones desde BD para Todos los Roles

## 📋 Resumen

Se ha implementado un sistema centralizado para cargar datos de ubicaciones (DIVIPOLA), partidos y tipos de elección desde la base de datos, accesible para todos los roles del sistema.

## ✅ Componentes Implementados

### 1. Backend - Endpoints Compartidos (`backend/routes/locations.py`)

**Ruta base:** `/api/locations`

**Endpoints disponibles:**
- `GET /departamentos` - Retorna solo Caquetá (código 44)
- `GET /municipios/<departamento_codigo>` - Municipios de Caquetá
- `GET /zonas/<municipio_codigo>` - Zonas por municipio
- `GET /puestos/<zona_codigo>` - Puestos por zona
- `GET /mesas/<puesto_codigo>` - Mesas por puesto
- `GET /partidos` - Partidos activos
- `GET /tipos-eleccion` - Tipos de elección activos

**Características:**
- ✅ Accesible para todos los roles autenticados (solo requiere JWT)
- ✅ Filtrado automático por departamento de Caquetá (código 44)
- ✅ Ordenamiento alfabético de resultados
- ✅ Solo retorna registros activos

### 2. Frontend - Librería Compartida (`frontend/static/js/location-loader.js`)

**Funciones disponibles:**

#### Carga de Datos
```javascript
loadDepartamentosForSelect(selectId)      // Carga Caquetá
loadMunicipiosForSelect(selectId, deptoId) // Carga municipios
loadZonasForSelect(selectId, muniId)       // Carga zonas
loadPuestosForSelect(selectId, zonaId)     // Carga puestos
loadMesasForSelect(selectId, puestoId)     // Carga mesas
loadPartidosForSelect(selectId)            // Carga partidos
loadTiposEleccionForSelect(selectId)       // Carga tipos de elección
```

#### Configuración de Cascada
```javascript
setupLocationCascade(prefix)  // Configura eventos de cascada automática
```

**Características:**
- ✅ Selección automática de Caquetá (único departamento)
- ✅ Cascada automática: al seleccionar un nivel, se cargan los siguientes
- ✅ Limpieza automática de selects dependientes
- ✅ Manejo de errores con console.error
- ✅ Compatible con cualquier prefijo de IDs

### 3. Integración Global

**Archivo:** `frontend/templates/base.html`

El script `location-loader.js` se incluye en el template base, haciéndolo disponible para:
- ✅ Dashboard de Super Admin
- ✅ Dashboard de Testigo
- ✅ Dashboard de Coordinador de Puesto
- ✅ Dashboard de Coordinador Municipal
- ✅ Dashboard de Coordinador Departamental
- ✅ Dashboard de Auditor
- ✅ Cualquier otro módulo del sistema

## 🎯 Uso en Dashboards

### Ejemplo de Implementación

```html
<!-- HTML -->
<select id="miDepartamento" class="form-select">
    <option value="">Seleccionar departamento...</option>
</select>

<select id="miMunicipio" class="form-select">
    <option value="">Seleccionar municipio...</option>
</select>

<select id="miZona" class="form-select">
    <option value="">Seleccionar zona...</option>
</select>
```

```javascript
// JavaScript
document.addEventListener('DOMContentLoaded', async function() {
    // Cargar departamentos
    await loadDepartamentosForSelect('miDepartamento');
    
    // Configurar cascada automática
    setupLocationCascade('mi');
});
```

### Prefijos Recomendados

- `edit` - Para formularios de edición
- `create` - Para formularios de creación
- `filter` - Para filtros de búsqueda
- Cualquier prefijo personalizado

## 📊 Datos Disponibles

### Caquetá (Código 44)
- **Departamento:** 1 (Caquetá)
- **Municipios:** 16 (Albania, Belén de los Andaquíes, Cartagena del Chairá, Curillo, El Doncello, El Paujil, Florencia, La Montañita, Milán, Morelia, Puerto Rico, San José del Fragua, San Vicente del Caguán, Solano, Solita, Valparaíso)
- **Zonas:** 38
- **Puestos:** 150
- **Mesas:** 196

### Partidos y Tipos de Elección
- Solo se cargan los registros marcados como `activo=True`
- Ordenados alfabéticamente por nombre

## 🔒 Seguridad

- ✅ Todos los endpoints requieren autenticación JWT
- ✅ Filtrado automático por Caquetá (no se pueden consultar otros departamentos)
- ✅ Solo datos activos son retornados
- ✅ Validación de parámetros en backend

## 🚀 Ventajas

1. **Centralización:** Un solo archivo para todos los roles
2. **Mantenibilidad:** Cambios en un solo lugar
3. **Consistencia:** Misma lógica en todo el sistema
4. **Escalabilidad:** Fácil agregar nuevos endpoints
5. **Reutilización:** Funciones disponibles globalmente
6. **Automatización:** Cascada automática de selects

## 📝 Notas Técnicas

- El código 44 corresponde a Caquetá según DIVIPOLA
- Los endpoints están registrados en `backend/app.py`
- El blueprint `locations_bp` ya estaba registrado previamente
- Compatible con el sistema de autenticación JWT existente

## 🔄 Próximos Pasos

Para usar en un nuevo dashboard:

1. Asegurarse que el template extienda de `base.html`
2. Crear los elementos `<select>` con IDs apropiados
3. Llamar a las funciones de carga en `DOMContentLoaded`
4. Configurar la cascada con `setupLocationCascade(prefix)`

## ✨ Ejemplo Completo

```javascript
// Inicialización completa en un dashboard
document.addEventListener('DOMContentLoaded', async function() {
    // Cargar datos iniciales
    await loadDepartamentosForSelect('filterDepartamento');
    await loadPartidosForSelect('filterPartido');
    await loadTiposEleccionForSelect('filterTipo');
    
    // Configurar cascada de ubicaciones
    setupLocationCascade('filter');
    
    // Caquetá se selecciona automáticamente y carga municipios
});
```

---

**Fecha de Implementación:** 2025-11-27  
**Versión:** 1.0  
**Estado:** ✅ Completado y Desplegado
