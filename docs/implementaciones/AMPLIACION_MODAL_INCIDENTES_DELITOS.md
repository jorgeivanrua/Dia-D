# Ampliación Modal - Visualización Completa de Incidentes y Delitos

## Fecha: 2025-12-07

## Contexto

El coordinador municipal necesita ver el detalle completo de los incidentes y delitos reportados en cada puesto, incluyendo las fotografías de evidencia.

## Implementación

### 1. Backend - Endpoint Ampliado

**Archivo**: `backend/routes/coordinador_municipal.py`

**Cambios**:
- Se amplió el endpoint `/api/coordinador-municipal/puesto/<int:puesto_id>`
- Ahora devuelve información completa de incidentes y delitos
- Incluye evidencias fotográficas asociadas

**Datos Devueltos por Incidente**:
```python
{
    'id': int,
    'tipo_incidente': str,
    'tipo_incidente_label': str,
    'titulo': str,
    'descripcion': str,
    'severidad': str,
    'severidad_label': str,
    'estado': str,
    'estado_label': str,
    'fecha_incidente': str (ISO),
    'fecha_reporte': str (ISO),
    'reportado_por': str,
    'ubicacion_gps': str,
    'notas_resolucion': str,
    'evidencias': [
        {
            'id': int,
            'url': str,
            'filename': str,
            'fecha_subida': str (ISO)
        }
    ]
}
```

**Datos Devueltos por Delito**:
```python
{
    'id': int,
    'tipo_delito': str,
    'tipo_delito_label': str,
    'titulo': str,
    'descripcion': str,
    'gravedad': str,
    'gravedad_label': str,
    'estado': str,
    'estado_label': str,
    'fecha_delito': str (ISO),
    'fecha_reporte': str (ISO),
    'reportado_por': str,
    'ubicacion_gps': str,
    'denunciado_formalmente': bool,
    'numero_denuncia': str,
    'resultado_investigacion': str,
    'evidencias': [
        {
            'id': int,
            'url': str,
            'filename': str,
            'fecha_subida': str (ISO)
        }
    ]
}
```

### 2. Frontend - Modal Mejorado

**Archivo**: `frontend/static/js/coordinador-municipal-mejorado.js`

**Nuevas Pestañas en el Modal**:

1. **Pestaña "Incidentes"** (solo si hay incidentes)
   - Lista completa de incidentes del puesto
   - Cada incidente muestra:
     - Título y tipo
     - Descripción completa
     - Severidad (badge con color)
     - Estado (badge con color)
     - Reportado por y fecha
     - Ubicación GPS (si disponible)
     - Notas de resolución (si existen)
     - **Galería de fotos de evidencia**

2. **Pestaña "Delitos"** (solo si hay delitos)
   - Lista completa de delitos del puesto
   - Cada delito muestra:
     - Título y tipo
     - Descripción completa
     - Gravedad (badge con color)
     - Estado (badge con color)
     - Reportado por y fecha
     - Ubicación GPS (si disponible)
     - Información de denuncia formal (si existe)
     - Resultado de investigación (si existe)
     - **Galería de fotos de evidencia**

**Funciones Agregadas**:

1. `renderIncidentesList(incidentes)`
   - Renderiza lista de incidentes con formato de cards
   - Incluye galería de imágenes clickeables
   - Badges de severidad y estado con colores apropiados

2. `renderDelitosList(delitos)`
   - Renderiza lista de delitos con formato de cards
   - Incluye galería de imágenes clickeables
   - Badges de gravedad y estado con colores apropiados
   - Destacado especial para delitos (borde rojo)

### 3. Características de la Galería de Fotos

**Visualización**:
- Grid responsive (2 columnas en móvil, 3 en desktop)
- Imágenes con altura máxima de 150px
- Thumbnails con bordes redondeados
- Nombre del archivo debajo de cada imagen

**Interacción**:
- Click en imagen abre en nueva pestaña (tamaño completo)
- Hover muestra cursor pointer
- Imágenes mantienen proporción (object-fit: cover)

### 4. Colores y Estados

**Severidad de Incidentes**:
- Baja: Azul (info)
- Media: Amarillo (warning)
- Alta: Rojo (danger)
- Crítica: Rojo (danger)

**Estados de Incidentes**:
- Reportado: Amarillo (warning)
- En revisión: Azul (info)
- Resuelto: Verde (success)
- Escalado: Rojo (danger)

**Gravedad de Delitos**:
- Leve: Azul (info)
- Media: Amarillo (warning)
- Grave: Rojo (danger)
- Muy grave: Rojo (danger)

**Estados de Delitos**:
- Reportado: Amarillo (warning)
- En investigación: Azul (info)
- Investigado: Azul primario (primary)
- Denunciado: Verde (success)
- Archivado: Gris (secondary)

## Flujo de Usuario

1. **Coordinador Municipal** inicia sesión
2. Va a pestaña **"Puestos de Votación"**
3. Hace click en botón **"ojo"** de un puesto
4. Modal se abre mostrando:
   - Info básica del puesto
   - Estadísticas de formularios
   - **Alertas** si hay incidentes/delitos
   - Pestañas disponibles:
     - Info
     - Mesas
     - **Incidentes** (si hay)
     - **Delitos** (si hay)
     - Coordinador

5. Al hacer click en pestaña **"Incidentes"**:
   - Ve lista completa de incidentes
   - Puede ver todas las fotos de evidencia
   - Click en foto abre en tamaño completo

6. Al hacer click en pestaña **"Delitos"**:
   - Ve lista completa de delitos
   - Puede ver todas las fotos de evidencia
   - Ve información de denuncias formales
   - Click en foto abre en tamaño completo

## Archivos Modificados

1. `backend/routes/coordinador_municipal.py`
   - Líneas 385-465 (aprox)
   - Ampliado endpoint con datos completos de incidentes/delitos

2. `frontend/static/js/coordinador-municipal-mejorado.js`
   - Líneas 580-700 (aprox): Modal con nuevas pestañas
   - Líneas 700-850 (aprox): Funciones de renderizado

## Beneficios

✅ **Visibilidad Completa**: El coordinador ve todos los detalles sin necesidad de cambiar de pantalla

✅ **Evidencia Visual**: Las fotos se muestran directamente en el modal

✅ **Contexto Completo**: Toda la información relevante en un solo lugar

✅ **Responsive**: Funciona perfectamente en móvil y desktop

✅ **Interactivo**: Click en fotos para ver en tamaño completo

## Testing

Para probar:

1. Crear un incidente o delito en un puesto (usando el rol testigo o coordinador de puesto)
2. Subir fotos de evidencia
3. Iniciar sesión como `coord_mun` / `coord123`
4. Ir a "Puestos de Votación"
5. Click en "ojo" del puesto con incidentes/delitos
6. Verificar:
   - Pestañas de Incidentes/Delitos aparecen
   - Se muestra información completa
   - Fotos se visualizan correctamente
   - Click en foto abre en nueva pestaña

## Estado

✅ **COMPLETADO** - El coordinador municipal ahora puede ver el detalle completo de incidentes y delitos con sus fotos de evidencia directamente desde el modal del puesto.
