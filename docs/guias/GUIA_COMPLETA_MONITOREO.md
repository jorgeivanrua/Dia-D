# 📊 Guía Completa del Sistema de Monitoreo Electoral

## 🎯 Descripción General

El Sistema de Monitoreo Electoral es una plataforma completa de supervisión en tiempo real que permite:

- Seguimiento de testigos y coordinadores con geolocalización
- Monitoreo de formularios E-14 y su estado de validación
- Gestión de incidentes y delitos electorales
- Análisis de métricas y tendencias
- Predicciones basadas en datos históricos
- Comparativas entre departamentos

---

## 📋 Tabla de Contenidos

1. [Características Principales](#características-principales)
2. [Endpoints API](#endpoints-api)
3. [Métricas Avanzadas](#métricas-avanzadas)
4. [Optimizaciones de Base de Datos](#optimizaciones-de-base-de-datos)
5. [Guía de Uso](#guía-de-uso)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Características Principales

### 1. Dashboard en Tiempo Real

**Actualización automática cada 30 segundos**

- Mapa interactivo con geolocalización de usuarios
- Estadísticas en tiempo real
- Sistema de alertas automáticas
- Filtros por ubicación y tipo de usuario

### 2. Métricas de Rendimiento

- Actividad de usuarios por período (1h, 6h, 12h, 24h)
- Formularios recibidos y validados
- Tiempo promedio de respuesta a incidentes
- Tasas de cambio y tendencias


### 3. Mapa de Calor

Visualización de actividad por departamento:
- Usuarios activos
- Formularios enviados
- Incidentes reportados
- Delitos registrados
- Índice de actividad calculado

### 4. Análisis de Tendencias

- Actividad por hora del día
- Identificación de horas pico
- Patrones de comportamiento
- Gráficos interactivos

### 5. Comparativa de Departamentos

- Ranking de rendimiento
- Top 5 departamentos
- Departamentos que necesitan atención
- Score de rendimiento (0-100)

### 6. Predicciones

- Predicción de formularios próximas 24h
- Predicción de incidentes
- Tendencias porcentuales
- Tiempo estimado para completar pendientes

---

## 🔌 Endpoints API

### Endpoints Básicos

#### 1. `GET /monitoreo/dashboard`
Dashboard principal (HTML)

**Autenticación**: JWT + Rol monitoreo

#### 2. `GET /monitoreo/api/usuarios-activos`
Obtener usuarios con geolocalización

**Response**:
```json
{
  "success": true,
  "usuarios": [
    {
      "id": 1,
      "nombre": "Juan Pérez",
      "rol": "testigo_electoral",
      "latitud": 4.6097,
      "longitud": -74.0817,
      "ultima_geolocalizacion": "2025-11-28T10:30:00",
      "ubicacion": {
        "departamento_nombre": "Cundinamarca",
        "municipio_nombre": "Bogotá"
      }
    }
  ]
}
```

#### 3. `GET /monitoreo/api/estadisticas`
Estadísticas generales del sistema

**Response**:
```json
{
  "success": true,
  "estadisticas": {
    "testigos": {
      "total": 100,
      "con_geolocalizacion": 85,
      "porcentaje_geo": 85.0,
      "con_presencia_verificada": 75,
      "porcentaje_presencia": 75.0
    },
    "coordinadores": {
      "total": 30,
      "con_geolocalizacion": 28,
      "porcentaje_geo": 93.33
    },
    "formularios": {
      "total": 500,
      "validados": 450,
      "pendientes": 40,
      "rechazados": 10
    },
    "incidentes": {
      "total": 15,
      "criticos": 2,
      "pendientes": 8
    },
    "delitos": {
      "total": 8,
      "graves": 4,
      "pendientes": 5
    }
  }
}
```

#### 4. `GET /monitoreo/api/alertas`
Sistema de alertas automáticas

**Response**:
```json
{
  "success": true,
  "alertas": [
    {
      "tipo": "danger",
      "categoria": "incidentes",
      "titulo": "Incidentes Críticos Pendientes",
      "descripcion": "Hay 2 incidentes críticos que requieren atención inmediata",
      "cantidad": 2
    }
  ]
}
```

#### 5. `GET /monitoreo/api/actividad-reciente`
Actividad de las últimas 24 horas

**Query Parameters**:
- `limite` (opcional): Número de registros (default: 15)

**Response**:
```json
{
  "success": true,
  "actividad": {
    "formularios": [...],
    "incidentes": [...],
    "delitos": [...]
  }
}
```

#### 6. `GET /monitoreo/api/estadisticas-departamento/<codigo>`
Estadísticas de un departamento específico

**Response**:
```json
{
  "success": true,
  "departamento": {
    "codigo": "05",
    "nombre": "Antioquia",
    "testigos": 50,
    "coordinadores": 10,
    "formularios": 200
  }
}
```

#### 7. `GET /monitoreo/api/exportar-reporte`
Exportar reporte completo en JSON

---

### Endpoints Avanzados (Nuevos)

#### 8. `GET /monitoreo/api/metricas-rendimiento`
Métricas de rendimiento del sistema

**Response**:
```json
{
  "success": true,
  "metricas": {
    "actividad_usuarios": {
      "ultima_hora": 25,
      "ultimas_6_horas": 120,
      "ultimas_12_horas": 180,
      "ultimas_24_horas": 250,
      "tasa_cambio": 5.5
    },
    "formularios": {
      "ultima_hora": 10,
      "ultimas_6_horas": 45,
      "ultimas_12_horas": 80,
      "ultimas_24_horas": 150,
      "tasa_cambio": 8.2,
      "promedio_por_hora": 6.25
    },
    "incidentes": {
      "ultima_hora": 2,
      "ultimas_6_horas": 8,
      "ultimas_12_horas": 12,
      "ultimas_24_horas": 20,
      "tasa_cambio": -10.5,
      "tiempo_promedio_respuesta_minutos": 45.5
    }
  }
}
```

#### 9. `GET /monitoreo/api/mapa-calor`
Datos para mapa de calor por departamento

**Response**:
```json
{
  "success": true,
  "mapa_calor": [
    {
      "departamento_codigo": "05",
      "departamento_nombre": "Antioquia",
      "usuarios": 50,
      "formularios": 200,
      "incidentes": 5,
      "delitos": 2,
      "indice_actividad": 264
    }
  ]
}
```

#### 10. `GET /monitoreo/api/tendencias`
Análisis de tendencias por hora

**Response**:
```json
{
  "success": true,
  "tendencias": [
    {
      "hora": 0,
      "formularios": 5,
      "incidentes": 1,
      "usuarios_activos": 20
    },
    ...
  ],
  "hora_pico": {
    "hora": 14,
    "actividad_total": 45
  }
}
```

#### 11. `GET /monitoreo/api/comparativa-departamentos`
Comparativa de rendimiento entre departamentos

**Response**:
```json
{
  "success": true,
  "comparativa": [...],
  "top_5": [
    {
      "departamento_codigo": "05",
      "departamento_nombre": "Antioquia",
      "testigos": {
        "total": 50,
        "con_presencia": 48,
        "porcentaje_presencia": 96.0
      },
      "formularios": {
        "total": 200,
        "validados": 195,
        "porcentaje_validados": 97.5
      },
      "incidentes": {
        "total": 5,
        "criticos": 0
      },
      "score_rendimiento": 96.7
    }
  ],
  "bottom_5": [...]
}
```

#### 12. `GET /monitoreo/api/predicciones`
Predicciones basadas en tendencias

**Response**:
```json
{
  "success": true,
  "predicciones": {
    "formularios": {
      "ultimas_24h": 150,
      "tendencia_porcentaje": 8.5,
      "prediccion_proximas_24h": 163,
      "pendientes": 40,
      "horas_estimadas_completar": 6.4
    },
    "incidentes": {
      "ultimas_24h": 20,
      "tendencia_porcentaje": -5.2,
      "prediccion_proximas_24h": 19
    }
  }
}
```

---

## 📊 Métricas Avanzadas

### Cálculo del Score de Rendimiento

El score de rendimiento de un departamento se calcula con la siguiente fórmula:

```
Score = (Presencia% × 0.4) + (Validados% × 0.4) + (Penalización_Incidentes × 0.2)

Donde:
- Presencia% = (Testigos con presencia / Total testigos) × 100
- Validados% = (Formularios validados / Total formularios) × 100
- Penalización_Incidentes = max(0, 100 - (Incidentes críticos × 10))
```

**Interpretación**:
- 90-100: Excelente
- 75-89: Bueno
- 60-74: Regular
- 0-59: Necesita atención

### Índice de Actividad

```
Índice = Usuarios + Formularios + (Incidentes × 2) + (Delitos × 3)
```

Los incidentes y delitos tienen mayor peso por su importancia.

### Tasa de Cambio

```
Tasa = ((Valor_Actual - Valor_Anterior) / Valor_Anterior) × 100
```

**Interpretación**:
- Positivo: Incremento de actividad
- Negativo: Disminución de actividad
- Cercano a 0: Estable

---

## 🗄️ Optimizaciones de Base de Datos

### Índices Creados

El sistema incluye 20+ índices optimizados para mejorar el rendimiento:

**Tabla `users`**:
- `idx_users_rol_activo` - Consultas por rol y estado
- `idx_users_geolocalizacion` - Usuarios con geolocalización
- `idx_users_geolocalizacion_at` - Actividad reciente
- `idx_users_presencia` - Presencia verificada
- `idx_users_ubicacion` - JOINs con locations

**Tabla `formularios_e14`**:
- `idx_formularios_estado` - Filtros por estado
- `idx_formularios_created_at` - Ordenamiento temporal
- `idx_formularios_usuario` - JOINs con users
- `idx_formularios_estado_fecha` - Consultas combinadas

**Tabla `incidentes_electorales`**:
- `idx_incidentes_severidad` - Filtros por severidad
- `idx_incidentes_estado` - Filtros por estado
- `idx_incidentes_fecha_reporte` - Actividad reciente
- `idx_incidentes_criticos` - Alertas críticas
- `idx_incidentes_completo` - Consultas complejas

**Tabla `delitos_electorales`**:
- `idx_delitos_gravedad` - Filtros por gravedad
- `idx_delitos_estado` - Filtros por estado
- `idx_delitos_fecha_reporte` - Actividad reciente
- `idx_delitos_graves` - Alertas de delitos graves
- `idx_delitos_completo` - Consultas complejas

### Aplicar Índices

```bash
# Ejecutar script SQL
python scripts/aplicar_indices.py
```

### Mejoras de Rendimiento Esperadas

- Consultas simples: **50-80% más rápidas**
- Consultas con JOIN: **60-90% más rápidas**
- Consultas de agregación: **40-70% más rápidas**
- Dashboard completo: **50-75% más rápido**

---

## 📖 Guía de Uso

### Acceso al Dashboard

1. **Login**:
   ```
   URL: http://localhost:5000/login
   Usuario: monitoreo
   Contraseña: Monitoreo2025!
   ```

2. **Dashboard**:
   ```
   URL: http://localhost:5000/monitoreo/dashboard
   ```

### Navegación

#### Sección 1: Estadísticas Principales
- Testigos con geolocalización
- Testigos con presencia verificada
- Coordinadores activos
- Formularios recibidos

#### Sección 2: Mapa Interactivo
- Visualización de usuarios en tiempo real
- Filtros por tipo de usuario
- Filtros por ubicación (departamento, municipio, zona, puesto)
- Marcadores con colores por rol

#### Sección 3: Alertas
- Alertas críticas (rojas)
- Alertas de advertencia (amarillas)
- Alertas informativas (azules)

#### Sección 4: Actividad Reciente
- Formularios enviados
- Incidentes reportados
- Delitos registrados

#### Sección 5: Métricas de Rendimiento
- Gráfico de actividad de usuarios
- Gráfico de formularios por período
- Tiempo promedio de respuesta

#### Sección 6: Mapa de Calor
- Tabla con actividad por departamento
- Índice de actividad visual
- Ordenado por mayor actividad

#### Sección 7: Tendencias
- Gráfico de actividad por hora
- Identificación de hora pico
- Múltiples métricas en un gráfico

#### Sección 8: Comparativa
- Top 5 departamentos con mejor rendimiento
- Departamentos que necesitan atención
- Score de rendimiento visual

#### Sección 9: Predicciones
- Predicción de formularios
- Predicción de incidentes
- Tendencias porcentuales

### Actualización de Datos

**Automática**: Cada 30 segundos (configurable)

**Manual**: Click en botón de actualización (esquina inferior derecha)

---

## 🔧 Troubleshooting

### Problema: Dashboard no carga datos

**Solución**:
1. Verificar que el servidor esté corriendo
2. Verificar autenticación JWT
3. Revisar logs del backend
4. Verificar conexión a base de datos

```bash
# Ver logs
python run.py
```

### Problema: Mapa no muestra usuarios

**Solución**:
1. Verificar que haya usuarios con geolocalización
2. Revisar filtros aplicados
3. Verificar permisos de geolocalización

```bash
# Verificar usuarios con geo
python scripts\verificar_monitoreo.py
```

### Problema: Gráficos no se muestran

**Solución**:
1. Verificar que Chart.js esté cargado
2. Revisar consola del navegador
3. Verificar que haya datos disponibles

### Problema: Rendimiento lento

**Solución**:
1. Aplicar índices de base de datos
2. Reducir frecuencia de actualización
3. Optimizar consultas

```bash
# Aplicar índices
python scripts/aplicar_indices.py
```

### Problema: Alertas no aparecen

**Solución**:
1. Verificar que existan condiciones de alerta
2. Revisar endpoint `/api/alertas`
3. Verificar lógica de alertas en backend

---

## 🧪 Testing

### Verificar Conexiones

```bash
python scripts\verificar_monitoreo.py
```

### Probar Endpoints

```bash
# Obtener token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"monitoreo","password":"Monitoreo2025!"}'

# Probar endpoint
curl -X GET http://localhost:5000/monitoreo/api/estadisticas \
  -H "Authorization: Bearer <TOKEN>"
```

---

## 📝 Notas Adicionales

### Seguridad

- Todos los endpoints requieren autenticación JWT
- Solo el rol `monitoreo` tiene acceso
- No se exponen datos sensibles
- Logs de acceso registrados

### Escalabilidad

- Índices optimizados para grandes volúmenes
- Consultas paginadas donde sea necesario
- Caché de datos frecuentes (futuro)
- CDN para assets estáticos (futuro)

### Mantenimiento

- Ejecutar `ANALYZE` periódicamente
- Monitorear tamaño de índices
- Revisar logs de rendimiento
- Actualizar estadísticas de BD

---

**Versión**: 2.0  
**Fecha**: 28 de Noviembre de 2025  
**Autor**: Sistema de Optimización Automática
