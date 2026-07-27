# 🎯 Rol de Monitoreo - Mejorado y Completo

## ✅ Estado: MEJORADO Y OPTIMIZADO

**Fecha**: 28 de Noviembre de 2025  
**Versión**: 2.0

---

## 📋 Resumen de Mejoras

El rol de monitoreo ha sido significativamente mejorado con nuevas funcionalidades que permiten un seguimiento más completo y efectivo del sistema electoral.

---

## 🎯 Funcionalidades del Rol de Monitoreo

### 1. **Dashboard en Tiempo Real**

#### Mapa de Geolocalización
- ✅ Visualización de todos los usuarios activos en mapa interactivo
- ✅ Marcadores con colores según rol y estado
- ✅ Información detallada en popups
- ✅ Actualización automática cada 30 segundos
- ✅ Zoom automático a usuarios activos

#### Estadísticas Principales
- ✅ Testigos con geolocalización
- ✅ Testigos con presencia verificada
- ✅ Coordinadores con geolocalización
- ✅ Formularios recibidos y validados
- ✅ Porcentajes de cobertura

---

### 2. **Sistema de Alertas** (NUEVO)

El sistema ahora detecta y muestra alertas automáticas para:

#### Alertas de Geolocalización
- ⚠️ Testigos sin geolocalización
- ⚠️ Usuarios inactivos en la última hora

#### Alertas de Presencia
- ⚠️ Testigos sin presencia verificada
- ⚠️ Alta prioridad para verificación

#### Alertas de Incidentes
- 🚨 Incidentes críticos pendientes
- 🚨 Requieren atención inmediata

#### Alertas de Delitos
- 🚨 Delitos graves en investigación
- 🚨 Seguimiento prioritario

#### Alertas de Formularios
- ℹ️ Alto volumen de formularios pendientes
- ℹ️ Necesitan validación

**Características**:
- Clasificación por prioridad (crítica, alta, media, baja)
- Colores distintivos por tipo
- Contador de cantidad
- Actualización automática

---

### 3. **Actividad Reciente** (NUEVO)

Timeline de actividad del sistema:

#### Tipos de Actividad
- 📄 Formularios E-14 enviados
- ⚠️ Incidentes reportados
- 🛡️ Delitos electorales reportados
- 👤 Usuario que realizó la acción
- ⏰ Tiempo relativo (hace X minutos/horas)

**Características**:
- Últimas 15 actividades
- Filtro por últimas 24 horas
- Scroll para ver más
- Badges de estado/severidad
- Información del usuario

---

### 4. **Filtros Avanzados**

#### Filtro por Tipo de Usuario
- Todos
- Solo Testigos
- Solo Coordinadores
- Coordinadores Departamentales
- Coordinadores Municipales
- Coordinadores de Puesto
- Auditores

#### Filtro por Ubicación (Cascada)
- Departamento
- Municipio (se habilita al seleccionar departamento)
- Zona (se habilita al seleccionar municipio)
- Puesto (se habilita al seleccionar zona)

**Características**:
- Filtros en cascada
- Actualización automática del mapa
- Contador de usuarios filtrados
- Botón para limpiar filtros

---

### 5. **Exportación de Reportes** (NUEVO)

#### Reporte Completo en JSON
Incluye:
- Fecha y hora de generación
- Usuario que generó el reporte
- Estadísticas de usuarios por rol
- Estadísticas de formularios
- Estadísticas de incidentes por severidad
- Estadísticas de delitos por gravedad

**Uso**:
- Botón "Exportar Reporte" en el dashboard
- Descarga archivo JSON
- Nombre: `reporte-monitoreo-YYYY-MM-DD.json`

---

### 6. **Estadísticas Mejoradas** (MEJORADO)

#### Estadísticas Generales
- Total de testigos y porcentajes
- Total de coordinadores por tipo
- Total de auditores
- Formularios con estados detallados
- Formularios de la última hora (NUEVO)
- Incidentes por severidad (NUEVO)
- Delitos por gravedad (NUEVO)
- Usuarios activos en la última hora (NUEVO)

#### Estadísticas por Departamento (NUEVO)
Endpoint: `/api/estadisticas-departamento/<codigo>`

Proporciona:
- Testigos del departamento
- Coordinadores del departamento
- Formularios del departamento
- Porcentajes específicos

---

## 🔌 Endpoints de API

### Endpoints Existentes

#### `GET /monitoreo/dashboard`
Dashboard principal de monitoreo

#### `GET /monitoreo/api/usuarios-activos`
Obtener todos los usuarios activos con geolocalización

**Respuesta**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nombre": "Juan Pérez",
      "rol": "testigo_electoral",
      "latitud": 4.6097,
      "longitud": -74.0817,
      "precision": 10.5,
      "ultima_actualizacion": "2025-11-28T10:30:00",
      "ubicacion": {...},
      "presencia_verificada": true
    }
  ],
  "total": 150
}
```

#### `GET /monitoreo/api/estadisticas`
Estadísticas generales del sistema (MEJORADO)

**Respuesta**:
```json
{
  "success": true,
  "data": {
    "testigos": {
      "total": 200,
      "con_geolocalizacion": 180,
      "con_presencia_verificada": 150,
      "porcentaje_geo": 90.0,
      "porcentaje_presencia": 75.0
    },
    "coordinadores": {
      "total": 50,
      "con_geolocalizacion": 45,
      "porcentaje_geo": 90.0
    },
    "formularios": {
      "total": 500,
      "validados": 450,
      "pendientes": 40,
      "rechazados": 10,
      "ultima_hora": 25,
      "porcentaje_validados": 90.0
    },
    "incidentes": {
      "total": 15,
      "criticos": 2,
      "pendientes": 5
    },
    "delitos": {
      "total": 8,
      "graves": 3,
      "pendientes": 4
    },
    "actividad": {
      "usuarios_activos_hora": 120
    }
  }
}
```

### Endpoints Nuevos

#### `GET /monitoreo/api/alertas` (NUEVO)
Obtener alertas y situaciones que requieren atención

**Respuesta**:
```json
{
  "success": true,
  "data": [
    {
      "tipo": "warning",
      "categoria": "presencia",
      "titulo": "50 testigos sin presencia verificada",
      "descripcion": "Testigos que no han verificado su presencia en el puesto",
      "prioridad": "alta",
      "cantidad": 50
    }
  ],
  "total": 5
}
```

#### `GET /monitoreo/api/actividad-reciente` (NUEVO)
Obtener actividad reciente del sistema

**Parámetros**:
- `limite`: Número de actividades (default: 20)
- `horas`: Horas hacia atrás (default: 24)

**Respuesta**:
```json
{
  "success": true,
  "data": [
    {
      "tipo": "formulario",
      "icono": "file-earmark-text",
      "titulo": "Formulario E-14 enviado",
      "descripcion": "Juan Pérez envió un formulario",
      "estado": "validado",
      "timestamp": "2025-11-28T10:30:00",
      "usuario": "Juan Pérez"
    }
  ],
  "total": 15
}
```

#### `GET /monitoreo/api/estadisticas-departamento/<codigo>` (NUEVO)
Estadísticas específicas de un departamento

**Respuesta**:
```json
{
  "success": true,
  "data": {
    "departamento_codigo": "05",
    "testigos": {
      "total": 50,
      "con_geolocalizacion": 45,
      "con_presencia": 40
    },
    "coordinadores": {
      "total": 10
    },
    "formularios": {
      "total": 120,
      "validados": 110,
      "pendientes": 10
    }
  }
}
```

#### `GET /monitoreo/api/exportar-reporte` (NUEVO)
Exportar reporte completo del estado actual

**Respuesta**:
```json
{
  "success": true,
  "data": {
    "fecha_generacion": "2025-11-28T10:30:00",
    "generado_por": "monitoreo",
    "usuarios": {...},
    "formularios": {...},
    "incidentes": {...},
    "delitos": {...}
  }
}
```

---

## 🎨 Interfaz de Usuario

### Colores de Marcadores en el Mapa

| Rol/Estado | Color | Descripción |
|------------|-------|-------------|
| Testigo con Presencia | 🟢 Verde | Presencia verificada |
| Testigo sin Presencia | 🟡 Amarillo | Pendiente de verificación |
| Coordinador Puesto | 🔵 Azul | Coordinador de puesto |
| Coordinador Municipal | 🟣 Morado | Coordinador municipal |
| Coordinador Departamental | 🔴 Rosa | Coordinador departamental |
| Auditor | 🔷 Cyan | Auditor electoral |

### Tipos de Alertas

| Tipo | Color | Uso |
|------|-------|-----|
| danger | Rojo | Situaciones críticas |
| warning | Amarillo | Advertencias importantes |
| info | Azul | Información general |

---

## 🔐 Permisos y Seguridad

### Acceso
- ✅ Solo usuarios con rol `monitoreo`
- ✅ Autenticación JWT requerida
- ✅ Decorador `@role_required('monitoreo')`

### Capacidades
- ✅ Ver todos los usuarios activos
- ✅ Ver todas las ubicaciones
- ✅ Ver todos los formularios
- ✅ Ver todos los incidentes y delitos
- ✅ Exportar reportes
- ❌ NO puede modificar datos
- ❌ NO puede crear/editar usuarios
- ❌ NO puede validar formularios

---

## 🚀 Cómo Usar

### 1. Acceso al Dashboard

```
URL: http://localhost:5000/monitoreo/dashboard
Credenciales:
  Usuario: monitoreo
  Contraseña: Monitoreo2025!
```

### 2. Navegación

#### Vista Principal
- Mapa interactivo con usuarios activos
- Estadísticas en cards superiores
- Alertas destacadas
- Filtros en panel lateral

#### Interacción con el Mapa
- Click en marcadores para ver detalles
- Zoom con scroll o botones
- Pan arrastrando el mapa

#### Uso de Filtros
1. Seleccionar tipo de usuario
2. Seleccionar ubicación (cascada)
3. El mapa se actualiza automáticamente
4. Usar botón "Limpiar" para resetear

#### Exportar Reporte
1. Click en "Exportar Reporte"
2. Se descarga archivo JSON
3. Contiene snapshot completo del sistema

### 3. Actualización Automática

- ✅ Cada 30 segundos por defecto
- ✅ Toggle para activar/desactivar
- ✅ Botón manual de actualización
- ✅ Timestamp de última actualización

---

## 📊 Casos de Uso

### Caso 1: Monitoreo de Cobertura
**Objetivo**: Verificar que todos los testigos estén en sus puestos

1. Abrir dashboard de monitoreo
2. Revisar estadística "Testigos con Presencia Verificada"
3. Si hay alertas, revisar "Testigos sin presencia verificada"
4. Filtrar por departamento para ver cobertura regional
5. Contactar coordinadores de áreas con baja cobertura

### Caso 2: Respuesta a Incidentes
**Objetivo**: Atender incidentes críticos rápidamente

1. Revisar sección de alertas
2. Identificar "Incidentes críticos pendientes"
3. Ver actividad reciente para detalles
4. Filtrar mapa por ubicación del incidente
5. Coordinar respuesta con personal cercano

### Caso 3: Análisis de Actividad
**Objetivo**: Entender el flujo de trabajo del día

1. Revisar "Actividad Reciente"
2. Ver timeline de formularios enviados
3. Identificar picos de actividad
4. Verificar que formularios se estén validando
5. Exportar reporte para análisis posterior

### Caso 4: Supervisión Regional
**Objetivo**: Monitorear un departamento específico

1. Usar filtro de departamento
2. Revisar estadísticas específicas
3. Ver usuarios activos en el mapa
4. Identificar zonas sin cobertura
5. Tomar acciones correctivas

---

## 🔧 Configuración

### Auto-Refresh
```javascript
// Cambiar intervalo de actualización
// En el código: línea ~580
autoRefreshInterval = setInterval(cargarDatos, 30000); // 30 segundos

// Para cambiar a 1 minuto:
autoRefreshInterval = setInterval(cargarDatos, 60000);
```

### Límite de Actividad Reciente
```javascript
// Cambiar número de actividades mostradas
// En el código: línea ~490
const response = await APIClient.get('/monitoreo/api/actividad-reciente?limite=15&horas=24');

// Para mostrar 30 actividades de las últimas 48 horas:
const response = await APIClient.get('/monitoreo/api/actividad-reciente?limite=30&horas=48');
```

---

## 📝 Notas Técnicas

### Dependencias
- Leaflet.js 1.9.4 (mapas)
- Bootstrap 5 (UI)
- Bootstrap Icons (iconos)
- API Client (comunicación con backend)

### Rendimiento
- Actualización eficiente con filtros en cliente
- Caché de usuarios en memoria
- Actualización parcial del DOM
- Lazy loading de actividad

### Compatibilidad
- ✅ Chrome/Edge (recomendado)
- ✅ Firefox
- ✅ Safari
- ✅ Responsive (móviles y tablets)

---

## 🎯 Mejoras Futuras Sugeridas

### Corto Plazo
1. ⏳ Notificaciones push para alertas críticas
2. ⏳ Filtro por rango de tiempo
3. ⏳ Búsqueda de usuarios por nombre
4. ⏳ Exportación a PDF/Excel

### Mediano Plazo
1. ⏳ Dashboard de métricas históricas
2. ⏳ Gráficos de tendencias
3. ⏳ Comparación entre departamentos
4. ⏳ Predicción de cobertura

### Largo Plazo
1. ⏳ Machine Learning para detección de anomalías
2. ⏳ Integración con sistemas externos
3. ⏳ App móvil dedicada
4. ⏳ Alertas por SMS/WhatsApp

---

## ✅ Checklist de Funcionalidades

### Visualización
- [x] Mapa interactivo con Leaflet
- [x] Marcadores con colores por rol
- [x] Popups con información detallada
- [x] Zoom automático a usuarios
- [x] Leyenda de colores

### Estadísticas
- [x] Testigos con geolocalización
- [x] Testigos con presencia
- [x] Coordinadores activos
- [x] Formularios por estado
- [x] Incidentes por severidad
- [x] Delitos por gravedad
- [x] Usuarios activos última hora

### Alertas
- [x] Detección automática
- [x] Clasificación por prioridad
- [x] Colores distintivos
- [x] Contador de cantidad
- [x] Actualización automática

### Actividad
- [x] Timeline de eventos
- [x] Filtro por tiempo
- [x] Información del usuario
- [x] Badges de estado
- [x] Scroll infinito

### Filtros
- [x] Por tipo de usuario
- [x] Por departamento
- [x] Por municipio
- [x] Por zona
- [x] Por puesto
- [x] Cascada automática
- [x] Botón limpiar

### Exportación
- [x] Reporte completo en JSON
- [x] Timestamp de generación
- [x] Todas las estadísticas
- [x] Descarga automática

### UX
- [x] Actualización automática
- [x] Toggle de auto-refresh
- [x] Botón de actualización manual
- [x] Timestamp de última actualización
- [x] Responsive design
- [x] Loading states

---

## 🎉 Conclusión

El rol de monitoreo ahora es una herramienta completa y poderosa para supervisar el sistema electoral en tiempo real. Con las nuevas funcionalidades de alertas, actividad reciente y exportación de reportes, los usuarios con rol de monitoreo pueden:

✅ **Supervisar** - Ver todos los usuarios activos en tiempo real  
✅ **Detectar** - Identificar problemas automáticamente  
✅ **Responder** - Actuar rápidamente ante situaciones críticas  
✅ **Analizar** - Entender el flujo de trabajo del sistema  
✅ **Reportar** - Exportar datos para análisis posterior  

---

**Desarrollado por**: Sistema de Optimización Automática  
**Fecha**: 28 de Noviembre de 2025  
**Versión**: 2.0  
**Estado**: ✅ Mejorado y Completo
