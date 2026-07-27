# 📁 Estructura del Proyecto - Sistema de Monitoreo

## 🎯 Organización según Buenas Prácticas

**Fecha**: 28 de Noviembre de 2025  
**Versión**: 2.0

---

## 📂 Estructura de Directorios

```
mvp/
├── scripts/                                    # Scripts de instalación y utilidades
│   ├── crear_indices_monitoreo.sql            # SQL con 24 índices de optimización
│   ├── aplicar_indices.py                     # Aplicador de índices
│   ├── verificar_monitoreo.py                 # Verificación completa del sistema
│   ├── check_monitoreo_user.py                # Verificar usuario monitoreo
│   └── instalar_monitoreo_completo.bat        # Instalador automatizado
│
├── backend/
│   └── routes/
│       └── monitoreo.py                       # 12 endpoints API (7 básicos + 5 nuevos)
│
├── frontend/
│   └── templates/
│       └── monitoreo/
│           └── dashboard.html                 # Dashboard con 9 secciones
│
├── docs/                                      # Documentación
│   ├── INICIO_RAPIDO_MONITOREO.md            # Guía de inicio rápido
│   ├── GUIA_COMPLETA_MONITOREO.md            # Guía completa (500+ líneas)
│   ├── VERIFICACION_MONITOREO_BD.md          # Verificación técnica
│   ├── ESTRUCTURA_PROYECTO_MONITOREO.md      # Este archivo
│   ├── RESUMEN_IMPLEMENTACION_COMPLETA.md    # Resumen ejecutivo
│   ├── RESUMEN_VISUAL_MONITOREO.txt          # Resumen visual ASCII
│   ├── ROL_MONITOREO_MEJORADO.md             # Documentación del rol
│   └── optimizaciones/
│       └── OPTIMIZACIONES_MONITOREO.md       # Resumen de optimizaciones
│
└── (raíz)/                                    # Índice principal
    └── README_MONITOREO.md                   # Índice y guía rápida
```

---

## 📋 Descripción de Archivos

### 🔧 Scripts (`scripts/`)

#### 1. `crear_indices_monitoreo.sql`
**Tipo**: SQL  
**Propósito**: Definición de 24 índices de optimización  
**Uso**: Ejecutado automáticamente por `aplicar_indices.py`

**Contenido**:
- 5 índices para tabla `users`
- 3 índices para tabla `locations`
- 4 índices para tabla `formularios_e14`
- 6 índices para tabla `incidentes_electorales`
- 6 índices para tabla `delitos_electorales`

#### 2. `aplicar_indices.py`
**Tipo**: Python  
**Propósito**: Aplicar índices de optimización a la BD  
**Uso**: `python scripts\aplicar_indices.py`

**Funcionalidad**:
- Lee el archivo SQL
- Ejecuta cada comando
- Maneja errores
- Genera reporte

#### 3. `verificar_monitoreo.py`
**Tipo**: Python  
**Propósito**: Verificación completa del sistema  
**Uso**: `python scripts\verificar_monitoreo.py`

**Verifica**:
- Conexión a 5 modelos de BD
- Conteo de registros
- Simulación de consultas
- Condiciones de alertas
- Reporte detallado

#### 4. `check_monitoreo_user.py`
**Tipo**: Python  
**Propósito**: Verificar usuario de monitoreo  
**Uso**: `python scripts\check_monitoreo_user.py`

**Verifica**:
- Existencia del usuario
- Rol correcto
- Estado activo
- Permisos

#### 5. `instalar_monitoreo_completo.bat`
**Tipo**: Batch  
**Propósito**: Instalación automatizada completa  
**Uso**: `scripts\instalar_monitoreo_completo.bat`

**Pasos**:
1. Verificar entorno virtual
2. Activar entorno
3. Instalar dependencias
4. Aplicar índices
5. Verificar conexiones
6. Verificar usuario

---

### 🎨 Frontend (`frontend/templates/monitoreo/`)

#### `dashboard.html`
**Tipo**: HTML + JavaScript  
**Líneas**: 1000+  
**Tecnologías**: Leaflet.js, Chart.js 4.4.0

**Secciones**:
1. Estadísticas principales (4 cards)
2. Mapa interactivo con geolocalización
3. Sistema de alertas
4. Actividad reciente
5. **Métricas de rendimiento** (nuevo)
6. **Mapa de calor** (nuevo)
7. **Tendencias por hora** (nuevo)
8. **Comparativa de departamentos** (nuevo)
9. **Predicciones** (nuevo)

---

### 🔌 Backend (`backend/routes/`)

#### `monitoreo.py`
**Tipo**: Python (Flask)  
**Líneas**: 900+  
**Endpoints**: 12

**Endpoints Básicos** (7):
1. `GET /monitoreo/dashboard` - Dashboard HTML
2. `GET /monitoreo/api/usuarios-activos` - Usuarios con geolocalización
3. `GET /monitoreo/api/estadisticas` - Estadísticas generales
4. `GET /monitoreo/api/alertas` - Sistema de alertas
5. `GET /monitoreo/api/actividad-reciente` - Actividad 24h
6. `GET /monitoreo/api/estadisticas-departamento/<codigo>` - Por departamento
7. `GET /monitoreo/api/exportar-reporte` - Reporte completo

**Endpoints Nuevos** (5):
8. `GET /monitoreo/api/metricas-rendimiento` - Métricas avanzadas
9. `GET /monitoreo/api/mapa-calor` - Mapa de calor por departamento
10. `GET /monitoreo/api/tendencias` - Tendencias por hora
11. `GET /monitoreo/api/comparativa-departamentos` - Comparativa
12. `GET /monitoreo/api/predicciones` - Predicciones automáticas

---

### 📚 Documentación (`docs/`)

#### 1. `GUIA_COMPLETA_MONITOREO.md`
**Líneas**: 500+  
**Audiencia**: Usuarios, desarrolladores, administradores

**Contenido**:
- Descripción general
- Documentación de 12 endpoints
- Ejemplos de requests/responses
- Guía de uso del dashboard
- Cálculo de métricas
- Troubleshooting completo

#### 2. `VERIFICACION_MONITOREO_BD.md`
**Líneas**: 400+  
**Audiencia**: Desarrolladores, DBAs

**Contenido**:
- Verificación de 5 modelos
- 50+ consultas SQL documentadas
- Flujo de datos
- Rendimiento de consultas
- Índices recomendados

#### 3. `ROL_MONITOREO_MEJORADO.md`
**Líneas**: 300+  
**Audiencia**: Administradores

**Contenido**:
- Descripción del rol
- Permisos y accesos
- Funcionalidades
- Configuración

#### 4. `optimizaciones/OPTIMIZACIONES_MONITOREO.md`
**Líneas**: 150+  
**Audiencia**: Gerentes, líderes técnicos

**Contenido**:
- Resumen de optimizaciones
- Comparativa antes/después
- Guía de instalación
- Referencias

---

### 📄 Documentos Adicionales en `docs/`

#### 5. `docs/INICIO_RAPIDO_MONITOREO.md`
**Líneas**: 100+  
**Audiencia**: Nuevos usuarios

**Contenido**:
- Instalación en 3 pasos
- Qué verás en el dashboard
- Verificación rápida
- Problemas comunes

#### 6. `docs/RESUMEN_IMPLEMENTACION_COMPLETA.md`
**Líneas**: 400+  
**Audiencia**: Gerentes, líderes de proyecto

**Contenido**:
- Archivos creados/modificados
- Nuevas funcionalidades
- Mejoras de rendimiento
- Checklist de implementación

#### 7. `docs/RESUMEN_VISUAL_MONITOREO.txt`
**Líneas**: 300+  
**Audiencia**: Todos

**Contenido**:
- Resumen visual con ASCII art
- Estructura de archivos
- Métricas calculadas
- Guías de referencia

### 📄 Índice Principal (raíz)

#### `README_MONITOREO.md`
**Líneas**: 100+  
**Audiencia**: Todos

**Contenido**:
- Inicio rápido
- Índice de documentación
- Scripts disponibles
- Características principales
- Enlaces a documentación detallada

---

## 🚀 Flujo de Uso

### Para Nuevos Usuarios

1. Leer `README_MONITOREO.md` (raíz)
2. Leer `docs/INICIO_RAPIDO_MONITOREO.md`
3. Ejecutar `scripts\instalar_monitoreo_completo.bat`
4. Acceder al dashboard
5. Consultar `docs/GUIA_COMPLETA_MONITOREO.md` si necesario

### Para Desarrolladores

1. Leer `README_MONITOREO.md` (raíz)
2. Leer `docs/ESTRUCTURA_PROYECTO_MONITOREO.md`
3. Leer `docs/VERIFICACION_MONITOREO_BD.md`
4. Revisar `backend/routes/monitoreo.py`
5. Revisar `frontend/templates/monitoreo/dashboard.html`
6. Ejecutar `python scripts\verificar_monitoreo.py`

### Para Administradores

1. Leer `README_MONITOREO.md` (raíz)
2. Leer `docs/RESUMEN_IMPLEMENTACION_COMPLETA.md`
3. Ejecutar `scripts\instalar_monitoreo_completo.bat`
4. Ejecutar `python scripts\verificar_monitoreo.py`
5. Consultar `docs/GUIA_COMPLETA_MONITOREO.md`

---

## 📊 Métricas del Proyecto

| Métrica | Valor |
|---------|-------|
| Archivos creados | 11 |
| Archivos modificados | 2 |
| Líneas de código | 900+ |
| Líneas de documentación | 2000+ |
| Endpoints API | 12 |
| Secciones visuales | 9 |
| Índices de BD | 24 |
| Scripts de utilidad | 5 |

---

## ✅ Buenas Prácticas Aplicadas

### 1. Organización de Scripts
✅ Todos los scripts en carpeta `scripts/`  
✅ Nombres descriptivos  
✅ Documentación en cada archivo

### 2. Separación de Concerns
✅ Backend en `backend/`  
✅ Frontend en `frontend/`  
✅ Documentación en `docs/`  
✅ Scripts en `scripts/`

### 3. Documentación
✅ Guía completa para usuarios  
✅ Documentación técnica para desarrolladores  
✅ Resúmenes ejecutivos para gerentes  
✅ Guías de inicio rápido

### 4. Nomenclatura
✅ Nombres descriptivos en español  
✅ Consistencia en nombres de archivos  
✅ Prefijos claros (verificar_, check_, crear_)

### 5. Versionamiento
✅ Todos los archivos con fecha  
✅ Versión 2.0 documentada  
✅ Changelog implícito en documentación

---

## 🔄 Mantenimiento

### Actualizar Índices
```bash
python scripts\aplicar_indices.py
```

### Verificar Sistema
```bash
python scripts\verificar_monitoreo.py
```

### Verificar Usuario
```bash
python scripts\check_monitoreo_user.py
```

### Reinstalar Completo
```bash
scripts\instalar_monitoreo_completo.bat
```

---

## 📞 Referencias

- **Índice Principal**: `README_MONITOREO.md` (raíz)
- **Inicio Rápido**: `docs/INICIO_RAPIDO_MONITOREO.md`
- **Guía Completa**: `docs/GUIA_COMPLETA_MONITOREO.md`
- **Verificación Técnica**: `docs/VERIFICACION_MONITOREO_BD.md`
- **Resumen Visual**: `docs/RESUMEN_VISUAL_MONITOREO.txt`
- **Estructura**: `docs/ESTRUCTURA_PROYECTO_MONITOREO.md` (este archivo)

---

**Versión**: 2.0  
**Fecha**: 28 de Noviembre de 2025  
**Estado**: ✅ ORGANIZADO SEGÚN BUENAS PRÁCTICAS
