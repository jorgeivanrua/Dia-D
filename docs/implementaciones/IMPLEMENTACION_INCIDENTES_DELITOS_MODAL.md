# Implementación de Incidentes y Delitos en Modal de Puesto

## Fecha: 2025-12-07

## Problema Identificado

El modal de detalle del puesto mostraba contadores de incidentes y delitos en 0 porque:
1. Los modelos no estaban importados correctamente
2. Las queries no estaban implementadas
3. Se había comentado que "los modelos no están implementados aún"

## Solución Implementada

### 1. Imports Correctos

Se agregó el import correcto de los modelos que YA EXISTEN en el sistema:

```python
from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
```

### 2. Queries Implementadas

Se implementaron las queries para contar incidentes y delitos del puesto:

```python
# Contar incidentes y delitos del puesto
incidentes_count = IncidenteElectoral.query.filter_by(
    puesto_id=puesto.id
).count()

delitos_count = DelitoElectoral.query.filter_by(
    puesto_id=puesto.id
).count()
```

### 3. Modelos Existentes

Los modelos ya estaban implementados en `backend/models/incidentes_delitos.py`:

- **IncidenteElectoral**: Tabla `incidentes_electorales`
  - Campos: tipo_incidente, titulo, descripcion, severidad, estado
  - Relaciones: reportado_por, mesa, puesto, municipio, departamento
  - Estados: reportado, en_revision, resuelto, escalado

- **DelitoElectoral**: Tabla `delitos_electorales`
  - Campos: tipo_delito, titulo, descripcion, gravedad, estado
  - Relaciones: reportado_por, investigado_por, mesa, puesto, municipio, departamento
  - Estados: reportado, en_investigacion, investigado, denunciado, archivado

### 4. Tablas en Base de Datos

Las tablas ya existen en la base de datos:
- `incidentes_electorales`
- `delitos_electorales`
- `notificaciones_reportes`
- `evidencias_fotograficas`
- `seguimiento_reportes`

## Archivos Modificados

### 1. backend/routes/coordinador_municipal.py (líneas 385-395)
- Endpoint: `/api/coordinador-municipal/puesto/<int:puesto_id>`
- Función: `obtener_puesto_detallado()`
- Cambios:
  - Agregado import: `from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral`
  - Implementadas queries para contar incidentes y delitos del puesto

### 2. backend/routes/super_admin.py (múltiples líneas)
- Corregidos imports incorrectos en 4 funciones diferentes
- Cambios realizados:
  - `Incidente` → `IncidenteElectoral`
  - `Delito` → `DelitoElectoral`
- Funciones afectadas:
  1. `reset_campana_data()` - Línea ~1446
  2. `eliminar_campana()` - Línea ~1507
  3. `auditoria_sistema()` - Línea ~1687
  4. `obtener_incidentes_delitos()` - Línea ~1920

## Funcionalidad del Modal

El modal ahora muestra correctamente:

1. **Encabezado con color de zona**
   - Zona del puesto con color distintivo
   - Barra de progreso del avance

2. **Estadísticas en Cards**
   - Formularios validados (verde)
   - Formularios pendientes (amarillo)
   - Formularios rechazados (rojo)
   - Total de mesas (azul)

3. **Alertas de Incidentes y Delitos**
   - Badge con contador de incidentes (si > 0)
   - Badge con contador de delitos (si > 0)

4. **Pestañas de Información**
   - **Info**: Datos básicos del puesto
   - **Mesas**: Lista de primeras 10 mesas con estado
   - **Coordinador**: Información del coordinador asignado

## Próximos Pasos (Opcional)

Si se desea ampliar la funcionalidad:

1. **Detalle de Incidentes**: Agregar pestaña con lista de incidentes del puesto
2. **Detalle de Delitos**: Agregar pestaña con lista de delitos del puesto
3. **Filtros**: Permitir filtrar por tipo de incidente/delito
4. **Acciones**: Botones para resolver/escalar incidentes desde el modal

## Verificación

Para verificar que funciona:

1. Iniciar sesión como `coord_mun` / `coord123`
2. Ir a la pestaña "Puestos de Votación"
3. Hacer clic en el botón "ojo" de cualquier puesto
4. El modal debe mostrar:
   - Información completa del puesto
   - Contadores de incidentes y delitos (actualmente en 0 si no hay reportes)
   - Sin errores en consola

## Correcciones Adicionales

Durante la implementación se descubrieron y corrigieron imports incorrectos en `super_admin.py`:

### Problema
El código usaba nombres de modelos que no existen:
- `Incidente` (incorrecto)
- `Delito` (incorrecto)

### Solución
Se corrigieron todos los imports y queries para usar los modelos correctos:
- `IncidenteElectoral` (correcto)
- `DelitoElectoral` (correcto)

### Impacto
Esto corrige errores potenciales en:
- Reset de datos de campaña
- Eliminación de campañas
- Auditoría del sistema
- Obtención de incidentes y delitos para super admin

## Estado

✅ **COMPLETADO** - Los contadores de incidentes y delitos ahora funcionan correctamente usando los modelos existentes.

✅ **BONUS** - Se corrigieron imports incorrectos en super_admin.py que causarían errores en producción.
