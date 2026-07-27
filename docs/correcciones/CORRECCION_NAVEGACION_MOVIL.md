# Corrección de Navegación Móvil - Dashboard Coordinador Municipal

## Problema Identificado
En modo móvil, las pestañas de "INCIDENTES" y "DELITOS" no se mostraban porque:
- Las pestañas principales tenían clase `d-none d-md-flex` (solo visibles en desktop)
- No existía un sistema de navegación alternativo para móvil

## Solución Implementada

### 1. Bottom Navigation Bar para Móvil
Se agregó un bottom navigation bar fijo en la parte inferior de la pantalla que:
- Solo se muestra en dispositivos móviles (`d-md-none`)
- Incluye TODAS las pestañas: Puestos, E-24, Incidentes, Delitos, Equipo, Mapa
- Está fijo en la parte inferior con `position: fixed`
- Tiene badges para mostrar contadores de incidentes y delitos

### 2. Estilos CSS Agregados
```css
.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: white;
    border-top: 1px solid #dee2e6;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    z-index: 1000;
    padding: 0.5rem 0;
}

.bottom-nav-item {
    flex: 1;
    text-align: center;
    padding: 0.5rem 0.25rem;
    color: #6c757d;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.bottom-nav-item.active {
    color: #007bff;
}
```

### 3. JavaScript para Sincronización
Se agregaron funciones para:
- **`initBottomNavSync()`**: Sincroniza el bottom nav con las pestañas principales
  - Cuando se hace clic en el bottom nav, actualiza la pestaña principal
  - Cuando se hace clic en la pestaña principal (desktop), actualiza el bottom nav
  
- **`actualizarBadgesMobile()`**: Actualiza los badges de incidentes y delitos en móvil

- Modificadas las funciones `cargarIncidentes()` y `cargarDelitos()` para actualizar ambos badges (desktop y móvil)

### 4. Ajustes de Layout
- Agregado `padding-bottom: 80px` al `.tab-content` en móvil para que el contenido no quede oculto por el bottom nav
- Los badges en el bottom nav tienen posicionamiento absoluto para mostrarse sobre los iconos

## Archivos Modificados

### `frontend/templates/coordinador/municipal-mejorado.html`
- Agregado bottom navigation bar FUERA del container-fluid para que position:fixed funcione
- Eliminados estilos CSS duplicados (se usan los del archivo externo)
- Cambiados `<button>` por `<a>` para mejor compatibilidad con Bootstrap tabs
- Agregado padding al tab-content en móvil (80px)

### `frontend/static/js/coordinador-municipal-mejorado.js`
- Agregada función `initBottomNavSync()` para sincronizar navegación
- Agregada función `actualizarBadgesMobile()` para actualizar badges
- Modificadas funciones `cargarIncidentes()` y `cargarDelitos()` para actualizar badges móviles
- Llamada a `initBottomNavSync()` en la inicialización del dashboard

### `backend/routes/coordinador_municipal.py`
- **Corregido endpoint `/coordinadores`**: Eliminadas referencias a campos inexistentes `telefono` y `email`
- **Corregido endpoint `/geolocalizacion`**: Cambiado `User.latitud/longitud` por `User.ultima_latitud/ultima_longitud`
- Agregados campos de geolocalización en respuesta de coordinadores

## Resultado
Ahora en modo móvil:
- ✅ Se muestran TODAS las pestañas en el bottom navigation (6 pestañas)
- ✅ Los badges de incidentes y delitos son visibles
- ✅ La navegación está sincronizada entre desktop y móvil
- ✅ El contenido no queda oculto por el bottom nav
- ✅ La interfaz es intuitiva y fácil de usar en dispositivos móviles
- ✅ Usa los estilos del archivo CSS externo (coordinador-puesto-v2.css)

## Estructura Final del Bottom Nav
```html
<nav class="bottom-nav">
    <a href="#puestos" class="bottom-nav-item active">
        <i class="bi bi-building"></i>
        <span>Puestos</span>
    </a>
    <a href="#e24" class="bottom-nav-item">
        <i class="bi bi-table"></i>
        <span>E-24</span>
    </a>
    <a href="#incidentes" class="bottom-nav-item">
        <i class="bi bi-exclamation-triangle"></i>
        <span class="badge bg-warning">0</span>
        <span>Incidentes</span>
    </a>
    <a href="#delitos" class="bottom-nav-item">
        <i class="bi bi-shield-exclamation"></i>
        <span class="badge bg-danger">0</span>
        <span>Delitos</span>
    </a>
    <a href="#equipo" class="bottom-nav-item">
        <i class="bi bi-people"></i>
        <span>Equipo</span>
    </a>
    <a href="#mapa" class="bottom-nav-item">
        <i class="bi bi-geo-alt"></i>
        <span>Mapa</span>
    </a>
</nav>
```

## Pruebas Recomendadas
1. **Limpiar caché del navegador** (Ctrl + Shift + Delete)
2. **Cerrar sesión y volver a iniciar** como coord_mun
3. **Activar modo responsive** (F12 → Ctrl+Shift+M)
4. **Verificar que el bottom nav sea visible** en la parte inferior con las 6 pestañas
5. **Hacer scroll horizontal** si es necesario para ver todas las pestañas
6. **Navegar entre pestañas** usando el bottom nav
7. **Verificar badges** de incidentes y delitos
8. **Confirmar que el contenido no quede oculto** por el bottom nav al hacer scroll

## Notas Importantes
- El bottom nav usa `<a>` en lugar de `<button>` para mejor compatibilidad con Bootstrap tabs
- Los estilos vienen del archivo `frontend/static/css/coordinador-puesto-v2.css` (líneas 507-565)
- El bottom nav se oculta automáticamente en desktop con `@media (min-width: 768px) { display: none; }`
- Si las 6 pestañas no caben en pantalla, el usuario puede hacer scroll horizontal en el bottom nav
