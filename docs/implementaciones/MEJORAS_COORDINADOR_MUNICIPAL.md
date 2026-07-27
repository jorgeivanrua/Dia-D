# Mejoras Dashboard Coordinador Municipal

## Fecha: 2025-12-06

## Problemas Identificados

1. **Dashboard actual tiene errores de carga**
   - Errores en consola al cargar el dashboard
   - Funcionalidades incompletas
   - Falta de integración con el mapa de geolocalización

2. **Falta de funcionalidades clave**
   - No tiene tabla E-24 consolidada como el coordinador de puesto
   - No tiene gestión de incidentes y delitos
   - No tiene mapa en tiempo real
   - No tiene vista de coordinadores de puesto

## Solución Implementada

### 1. Nuevo Template HTML
**Archivo:** `frontend/templates/coordinador/municipal-mejorado.html`

**Características:**
- Basado en el dashboard del coordinador de puesto
- Escalado a nivel municipal (puestos en lugar de mesas)
- Misma estructura de pestañas y funcionalidades
- Responsive y mobile-first

**Pestañas:**
1. **Puestos** - Lista de puestos del municipio con filtros y búsqueda
2. **E-24 Consolidado** - Tabla consolidada de todos los puestos
3. **Incidentes** - Gestión de incidentes del municipio
4. **Delitos** - Gestión de delitos electorales
5. **Coordinadores** - Estado de coordinadores de puesto
6. **Mapa** - Geolocalización en tiempo real

### 2. Estadísticas Mejoradas
- Puestos Pendientes
- Puestos Completos
- Con Discrepancias
- Progreso General

### 3. Funcionalidades Principales

#### Tab Puestos
- Lista de todos los puestos del municipio
- Filtros: Todos, Completos, Incompletos, Con Discrepancias
- Búsqueda por código o nombre
- Vista de detalle de cada puesto
- Panel lateral con consolidado y alertas

#### Tab E-24
- Resumen general (Total Puestos, Validados, Votos, Participación)
- Tabla detallada por puesto
- Consolidado por partido
- Exportar datos (CSV, Excel, PDF)
- Generar E-24 Municipal

#### Tab Incidentes
- Lista de incidentes del municipio
- Filtros por estado
- Gestión y seguimiento

#### Tab Delitos
- Lista de delitos electorales
- Filtros por estado
- Gestión y seguimiento

#### Tab Coordinadores
- Estado de coordinadores de puesto
- Último acceso
- Actividad

#### Tab Mapa
- Mapa interactivo con geolocalización
- Puestos de votación
- Usuarios en tiempo real
- Filtros y búsqueda

## Archivos Creados

1. `frontend/templates/coordinador/municipal-mejorado.html` - Template HTML mejorado
2. `MEJORAS_COORDINADOR_MUNICIPAL.md` - Este documento

## Archivos a Crear/Modificar

### JavaScript Necesario
**Archivo:** `frontend/static/js/coordinador-municipal-mejorado.js`

**Funciones principales:**
```javascript
// Inicialización
- loadUserProfile()
- loadPuestos()
- loadEstadisticas()
- loadConsolidadoMunicipal()
- loadDiscrepancias()

// Gestión de Puestos
- renderPuestosTable(puestos)
- filtrarPorEstado(estado)
- buscarPuestos(query)
- seleccionarPuesto(puestoId)
- verDetallePuesto(puestoId)

// E-24 Consolidado
- cargarE24Municipal()
- renderE24Table(datos)
- exportarDatosMunicipal()
- generarPDFE24Municipal()

// Incidentes y Delitos
- cargarIncidentes()
- filtrarIncidentes(estado)
- cargarDelitos()
- filtrarDelitos(estado)

// Coordinadores
- cargarCoordinadores()
- actualizarEstadoCoordinadores()

// Mapa
- inicializarMapa()
- centrarMapaEnMunicipio()
- ajustarVistaMapa()
- actualizarMapa()
```

### Backend Necesario
**Archivo:** `backend/routes/coordinador_municipal.py`

**Endpoints a verificar/crear:**
```python
# Ya existentes (verificar)
GET /api/coordinador-municipal/puestos
GET /api/coordinador-municipal/consolidado
GET /api/coordinador-municipal/puesto/<id>
GET /api/coordinador-municipal/discrepancias

# Nuevos necesarios
GET /api/coordinador-municipal/incidentes
GET /api/coordinador-municipal/delitos
GET /api/coordinador-municipal/coordinadores
GET /api/coordinador-municipal/e24-datos
POST /api/coordinador-municipal/e24-generar
GET /api/coordinador-municipal/exportar
```

## Pasos para Implementación Completa

### 1. Actualizar Ruta en Backend
```python
# En backend/routes/frontend.py o donde corresponda
@frontend_bp.route('/coordinador/municipal')
@jwt_required()
@role_required(['coordinador_municipal'])
def coordinador_municipal_dashboard():
    return render_template('coordinador/municipal-mejorado.html')
```

### 2. Crear JavaScript Completo
El archivo JavaScript debe seguir la misma estructura que `coordinador-puesto.js` pero adaptado a nivel municipal.

### 3. Verificar Endpoints Backend
Asegurarse de que todos los endpoints necesarios existen y funcionan correctamente.

### 4. Probar Funcionalidades
- Login como coordinador municipal
- Verificar carga de puestos
- Verificar estadísticas
- Verificar mapa
- Verificar E-24
- Verificar incidentes y delitos

## Diferencias Clave: Puesto vs Municipal

| Aspecto | Coordinador Puesto | Coordinador Municipal |
|---------|-------------------|----------------------|
| **Nivel** | Puesto individual | Todos los puestos del municipio |
| **Unidad base** | Mesas | Puestos |
| **Formularios** | E-14 individuales | E-14 consolidados por puesto |
| **E-24** | E-24 del puesto | E-24 municipal |
| **Equipo** | Testigos | Coordinadores de puesto |
| **Validación** | Valida E-14 | Supervisa puestos |
| **Mapa** | Mesas del puesto | Todos los puestos |

## Beneficios de la Mejora

1. **Consistencia** - Misma UX que coordinador de puesto
2. **Funcionalidad completa** - Todas las herramientas necesarias
3. **Escalabilidad** - Fácil de mantener y extender
4. **Responsive** - Funciona en móvil y desktop
5. **Tiempo real** - Actualización automática de datos
6. **Geolocalización** - Mapa interactivo integrado

## Próximos Pasos

1. ✅ Crear template HTML mejorado
2. ⏳ Crear JavaScript completo
3. ⏳ Verificar/crear endpoints backend
4. ⏳ Actualizar rutas frontend
5. ⏳ Probar funcionalidades
6. ⏳ Documentar uso

## Notas de Implementación

- Reutilizar componentes existentes (MapaGeolocalizacion, APIClient, Utils)
- Mantener consistencia con el diseño del coordinador de puesto
- Asegurar que los permisos estén correctamente configurados
- Implementar auto-refresh para datos en tiempo real
- Agregar manejo de errores robusto
