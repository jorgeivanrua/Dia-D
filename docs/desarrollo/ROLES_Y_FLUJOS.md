# Roles y Flujos del Sistema Electoral

## Índice de Roles

1. [Super Admin](#1-super-admin)
2. [Coordinador Departamental](#2-coordinador-departamental)
3. [Coordinador Municipal](#3-coordinador-municipal)
4. [Coordinador de Puesto](#4-coordinador-de-puesto)
5. [Testigo Electoral](#5-testigo-electoral)
6. [Auditor Electoral](#6-auditor-electoral)
7. [Monitoreo](#7-monitoreo)

---

## 1. Super Admin

### Descripción
Rol con máximos privilegios. Configura todo el sistema y supervisa todas las operaciones.

### Ubicación
- **Nivel**: Nacional (sin ubicación específica)
- **Alcance**: Todo el sistema

### Responsabilidades Principales

#### A. Configuración Electoral
- ✅ Crear y gestionar **Tipos de Elección**
- ✅ Crear y gestionar **Partidos Políticos**
- ✅ Crear y gestionar **Candidatos**
- ✅ Cargar datos masivos desde Excel

#### B. Configuración Territorial (DIVIPOLA)
- ✅ Cargar **Departamentos**
- ✅ Cargar **Municipios**
- ✅ Cargar **Puestos de Votación**
- ✅ Cargar **Mesas**
- ✅ Configurar votantes por mesa

#### C. Gestión de Usuarios
- ✅ Crear usuarios de todos los roles
- ✅ Asignar ubicaciones a usuarios
- ✅ Resetear contraseñas
- ✅ Activar/desactivar usuarios
- ✅ Ver todos los usuarios del sistema

#### D. Monitoreo y Supervisión
- ✅ Ver estadísticas globales
- ✅ Monitorear estado del sistema
- ✅ Ver consolidados de todos los niveles
- ✅ Acceder a todos los formularios E-14
- ✅ Ver todos los E-24 generados

#### E. Configuración del Sistema
- ✅ Gestionar fondos de pantalla
- ✅ Configurar temas visuales
- ✅ Configurar parámetros del sistema

### Endpoints Principales

```
GET  /api/super-admin/stats                    # Estadísticas globales
GET  /api/super-admin/users                    # Todos los usuarios
POST /api/super-admin/users                    # Crear usuario
PUT  /api/super-admin/users/:id                # Actualizar usuario

GET  /api/super-admin/partidos                 # Todos los partidos
POST /api/super-admin/upload/partidos          # Cargar partidos Excel
PUT  /api/super-admin/partidos/:id             # Actualizar partido

GET  /api/super-admin/candidatos               # Todos los candidatos
POST /api/super-admin/upload/candidatos        # Cargar candidatos Excel
PUT  /api/super-admin/candidatos/:id           # Actualizar candidato

GET  /api/super-admin/tipos-eleccion           # Tipos de elección
POST /api/super-admin/tipos-eleccion           # Crear tipo
PUT  /api/super-admin/tipos-eleccion/:id       # Actualizar tipo

POST /api/super-admin/upload/locations         # Cargar DIVIPOLA Excel
GET  /api/super-admin/system-health            # Estado del sistema
```

### Flujo de Trabajo

```
1. CONFIGURACIÓN INICIAL (Antes de las elecciones)
   ├── Cargar DIVIPOLA (departamentos → municipios → puestos → mesas)
   ├── Configurar tipos de elección
   ├── Cargar partidos políticos
   ├── Cargar candidatos
   ├── Crear coordinadores departamentales
   └── Verificar configuración completa

2. DURANTE LAS ELECCIONES
   ├── Monitorear estadísticas en tiempo real
   ├── Supervisar generación de E-24
   ├── Resolver incidencias escaladas
   └── Generar reportes globales

3. POST-ELECCIONES
   ├── Consolidar resultados finales
   ├── Generar reportes oficiales
   ├── Archivar datos
   └── Auditoría completa
```

### Dashboard
- **Ruta**: `/super-admin-dashboard`
- **Secciones**:
  - Estadísticas globales
  - Gestión de usuarios
  - Partidos políticos
  - Candidatos
  - Tipos de elección
  - Monitoreo departamental
  - Configuración del sistema

---

## 2. Coordinador Departamental

### Descripción
Supervisa todas las operaciones electorales de un departamento.

### Ubicación
- **Nivel**: Departamental
- **Alcance**: Un departamento completo

### Responsabilidades Principales

#### A. Gestión de Usuarios
- ✅ Crear coordinadores municipales de su departamento
- ✅ Crear coordinadores de puesto
- ✅ Resetear contraseñas de usuarios de su departamento

#### B. Supervisión Municipal
- ✅ Ver consolidados de todos los municipios
- ✅ Monitorear progreso de cada municipio
- ✅ Ver E-24 municipales

#### C. Consolidación Departamental (Pestaña Consolidado)
- ✅ Ver consolidado departamental en **tabla automática**
- ✅ Tabla se llena automáticamente con datos de E-14 validados
- ✅ Agrupación por **municipios** y **zonas**
- ✅ Generar PDF E-24 Departamental
- ✅ Validar consistencia de datos
- ✅ Ver estadísticas en tiempo real:
  - Total de municipios
  - Municipios completos
  - Total de votos por municipio
  - Votos por partido (tabla consolidada)

#### D. Monitoreo
- ✅ Ver estadísticas del departamento
- ✅ Identificar discrepancias
- ✅ Monitorear geolocalización de usuarios

### Endpoints Principales

```
GET  /api/coordinador-departamental/municipios           # Municipios del departamento
GET  /api/coordinador-departamental/consolidado          # Consolidado departamental
GET  /api/coordinador-departamental/estadisticas         # Estadísticas
POST /api/coordinador-departamental/e24-departamental    # Generar E-24
GET  /api/coordinador-departamental/e24-municipales      # E-24 de municipios
GET  /api/coordinador-departamental/discrepancias        # Discrepancias detectadas
```

### Flujo de Trabajo

```
1. PREPARACIÓN
   ├── Verificar que todos los municipios tienen coordinador
   ├── Verificar configuración de puestos
   └── Coordinar con coordinadores municipales

2. DURANTE LAS ELECCIONES
   ├── Monitorear progreso de municipios
   ├── Ver consolidados en tiempo real
   ├── Identificar y resolver discrepancias
   └── Apoyar a coordinadores municipales

3. CONSOLIDACIÓN
   ├── Esperar E-24 de todos los municipios
   ├── Verificar consistencia de datos
   ├── Generar E-24 Departamental
   └── Enviar resultados al nivel nacional
```

---

## 3. Coordinador Municipal

### Descripción
Supervisa todas las operaciones electorales de un municipio.

### Ubicación
- **Nivel**: Municipal
- **Alcance**: Un municipio completo

### Responsabilidades Principales

#### A. Gestión de Puestos
- ✅ Ver todos los puestos del municipio
- ✅ Monitorear progreso de cada puesto
- ✅ Ver E-24 de puestos

#### B. Consolidación Municipal (Pestaña Consolidado)
- ✅ Ver consolidado municipal en **tabla automática**
- ✅ Tabla se llena automáticamente con datos de E-14 validados
- ✅ Agrupación por **zonas** y **puestos**
- ✅ Generar PDF E-24 Municipal
- ✅ Requiere mínimo 80% de puestos completos
- ✅ Ver estadísticas en tiempo real:
  - Total de puestos
  - Puestos completos
  - Total de votos por zona
  - Votos por partido (tabla consolidada)

#### C. Análisis y Comparación
- ✅ Comparar resultados entre puestos
- ✅ Identificar discrepancias
- ✅ Ver consolidado por zona

#### D. Comunicación
- ✅ Enviar notificaciones a coordinadores de puesto
- ✅ Reportar incidencias

#### E. Exportación
- ✅ Exportar datos del municipio
- ✅ Generar reportes

### Endpoints Principales

```
GET  /api/coordinador-municipal/puestos                  # Puestos del municipio
GET  /api/coordinador-municipal/consolidado              # Consolidado municipal
GET  /api/coordinador-municipal/puesto/:id               # Detalle de puesto
POST /api/coordinador-municipal/e24-municipal            # Generar E-24
GET  /api/coordinador-municipal/e24-puestos              # E-24 de puestos
GET  /api/coordinador-municipal/discrepancias            # Discrepancias
GET  /api/coordinador-municipal/comparacion              # Comparar puestos
GET  /api/coordinador-municipal/estadisticas             # Estadísticas
POST /api/coordinador-municipal/notificar                # Enviar notificación
GET  /api/coordinador-municipal/exportar                 # Exportar datos
GET  /api/coordinador-municipal/consolidado-por-zona     # Por zona
```

### Flujo de Trabajo

```
1. PREPARACIÓN
   ├── Verificar que todos los puestos tienen coordinador
   ├── Verificar configuración de mesas
   └── Coordinar con coordinadores de puesto

2. DURANTE LAS ELECCIONES
   ├── Monitorear progreso de puestos
   ├── Ver consolidados en tiempo real
   ├── Identificar discrepancias
   ├── Enviar notificaciones a puestos
   └── Apoyar a coordinadores de puesto

3. CONSOLIDACIÓN
   ├── Esperar E-24 de todos los puestos
   ├── Verificar que se cumple el 80% mínimo
   ├── Revisar discrepancias
   ├── Generar E-24 Municipal
   └── Enviar al coordinador departamental
```

---

## 4. Coordinador de Puesto

### Descripción
Supervisa las operaciones electorales de un puesto de votación.

### Ubicación
- **Nivel**: Puesto de Votación
- **Alcance**: Un puesto específico con sus mesas

### Responsabilidades Principales

#### A. Gestión de Testigos
- ✅ Crear testigos para las mesas de su puesto
- ✅ Asignar testigos a mesas
- ✅ Resetear contraseñas de testigos

#### B. Validación de Formularios
- ✅ Ver todos los E-14 de su puesto
- ✅ **VALIDAR** formularios E-14 (cambiar estado a 'validado')
- ✅ **RECHAZAR** formularios con errores
- ✅ Solicitar correcciones a testigos

#### C. Consolidación de Puesto (Pestaña E-24)
- ✅ Ver consolidado del puesto en **tabla automática**
- ✅ Tabla se llena automáticamente con datos de E-14 validados
- ✅ Generar PDF E-24 de Puesto
- ✅ Exportar datos del puesto
- ✅ Ver estadísticas en tiempo real:
  - Total de mesas
  - Mesas validadas
  - Total de votos
  - Votos por partido (tabla)

#### D. Monitoreo de Mesas
- ✅ Ver estado de cada mesa
- ✅ Identificar mesas sin formulario
- ✅ Verificar presencia de testigos (geolocalización)
- ✅ Ver testigos activos/inactivos
- ✅ Monitorear última actividad de testigos

#### E. Gestión de Incidentes y Delitos
- ✅ Ver incidentes reportados en su puesto
- ✅ Ver delitos reportados en su puesto
- ✅ Cambiar estado de incidentes
- ✅ Resolver incidentes
- ✅ Escalar incidentes graves
- ✅ Investigar delitos reportados
- ✅ Agregar seguimiento a reportes

### Endpoints Principales

```
GET  /api/formularios/puesto                             # E-14 del puesto
GET  /api/formularios/:id                                # Detalle de E-14
PUT  /api/formularios/:id/validar                        # VALIDAR E-14
PUT  /api/formularios/:id/rechazar                       # RECHAZAR E-14
GET  /api/formularios/consolidado                        # Consolidado del puesto
GET  /api/formularios/mesas                              # Mesas del puesto
POST /api/formularios/puesto/generar-e24                 # Generar E-24
GET  /api/formularios/puesto/exportar                    # Exportar datos

POST /api/gestion-usuarios/crear-testigos-puesto         # Crear testigos
GET  /api/gestion-usuarios/listar-usuarios-ubicacion/:id # Usuarios del puesto

GET  /api/verificacion/estado-equipo                     # Ver presencia de testigos
GET  /api/verificacion/usuarios-geolocalizados           # Ver ubicación GPS

GET  /api/incidentes                                     # Incidentes del puesto
GET  /api/incidentes/:id                                 # Detalle de incidente
PUT  /api/incidentes/:id                                 # Actualizar/resolver
POST /api/incidentes/:id/escalar                         # Escalar incidente

GET  /api/delitos                                        # Delitos del puesto
GET  /api/delitos/:id                                    # Detalle de delito
PUT  /api/delitos/:id                                    # Actualizar/investigar
```

### Flujo de Trabajo

```
1. PREPARACIÓN
   ├── Verificar que todas las mesas tienen testigo
   ├── Verificar configuración de mesas
   └── Coordinar con testigos

2. DURANTE LAS ELECCIONES
   ├── Monitorear ingreso de E-14
   ├── VALIDAR formularios correctos
   ├── RECHAZAR formularios con errores
   ├── Solicitar correcciones
   └── Ver consolidado en tiempo real

3. CONSOLIDACIÓN
   ├── Verificar que todas las mesas tienen E-14 validado
   ├── Revisar consolidado del puesto
   ├── Generar E-24 de Puesto
   └── Enviar al coordinador municipal
```

### ⚠️ CRÍTICO
**Solo los E-14 con estado 'validado' se incluyen en los E-24**. El coordinador de puesto es el único que puede validar formularios.

---

## 5. Testigo Electoral

### Descripción
Registra los votos de una mesa específica en el Formulario E-14.

### Ubicación
- **Nivel**: Mesa
- **Alcance**: Una o más mesas específicas

### Responsabilidades Principales

#### A. Registro de Votos
- ✅ Crear formularios E-14 para sus mesas
- ✅ Registrar votos por partido
- ✅ Registrar votos por candidato
- ✅ Registrar votos nulos y blancos
- ✅ Registrar datos generales (votantes, participación)

#### B. Gestión de Formularios
- ✅ Ver sus formularios creados
- ✅ Editar formularios en estado 'pendiente'
- ✅ No puede editar formularios 'validados'

#### C. Verificación de Presencia (Geolocalización)
- ✅ Registrar geolocalización (GPS)
- ✅ Confirmar presencia en el puesto
- ✅ Actualizar ubicación periódicamente
- ✅ Visible para coordinadores

#### D. Reporte de Incidentes y Delitos
- ✅ Reportar incidentes electorales
  - Retraso en apertura
  - Falta de material
  - Problemas técnicos
  - Irregularidades
  - Ausencia de funcionarios
  - Disturbios
- ✅ Reportar delitos electorales
  - Compra de votos
  - Coacción al votante
  - Fraude electoral
  - Suplantación de identidad
  - Violencia electoral
- ✅ Adjuntar evidencia (fotos, videos)
- ✅ Registrar ubicación GPS del incidente
- ✅ Ver estado de sus reportes

### Endpoints Principales

```
# Datos electorales
GET  /api/testigo/partidos                               # Partidos activos
GET  /api/testigo/candidatos?tipo_eleccion_id=X          # Candidatos activos
GET  /api/testigo/tipos-eleccion                         # Tipos de elección
GET  /api/testigo/mi-mesa                                # Información de su mesa

# Formularios E-14
POST /api/formularios                                    # Crear E-14
PUT  /api/formularios/:id                                # Actualizar E-14
GET  /api/formularios/mis-formularios                    # Sus E-14

# Verificación de presencia
POST /api/verificacion/presencia                         # Registrar presencia (GPS)
GET  /api/verificacion/mi-estado                         # Ver su estado

# Incidentes y delitos
POST /api/incidentes                                     # Reportar incidente
GET  /api/incidentes                                     # Ver sus incidentes
GET  /api/incidentes/:id                                 # Detalle de incidente
PUT  /api/incidentes/:id                                 # Actualizar incidente

POST /api/delitos                                        # Reportar delito
GET  /api/delitos                                        # Ver sus delitos
GET  /api/delitos/:id                                    # Detalle de delito
```

### Flujo de Trabajo

```
1. PREPARACIÓN
   ├── Iniciar sesión
   ├── Verificar información de su mesa
   └── Registrar presencia (geolocalización GPS)

2. DURANTE LAS ELECCIONES
   ├── Mantener presencia activa (actualizar GPS)
   ├── Observar el proceso electoral
   ├── Reportar incidentes si ocurren:
   │   ├── Retrasos
   │   ├── Falta de material
   │   ├── Problemas técnicos
   │   └── Irregularidades
   ├── Reportar delitos si detecta:
   │   ├── Compra de votos
   │   ├── Coacción
   │   ├── Fraude
   │   └── Violencia
   ├── Tomar nota de los resultados
   └── Esperar cierre de mesa

3. REGISTRO DE VOTOS
   ├── Crear nuevo formulario E-14
   ├── Seleccionar tipo de elección
   ├── Registrar datos generales:
   │   ├── Total votantes registrados
   │   ├── Total votos emitidos
   │   ├── Votos nulos
   │   └── Votos en blanco
   ├── Registrar votos por partido
   ├── Registrar votos por candidato
   ├── Verificar que los totales cuadren
   └── Guardar formulario

4. POST-REGISTRO
   ├── Esperar validación del coordinador
   ├── Si es rechazado: corregir y reenviar
   ├── Si es validado: proceso completado
   └── Mantener disponibilidad para aclaraciones
```

### ⚠️ IMPORTANTE
- El testigo **NO puede validar** sus propios formularios
- Solo puede editar formularios en estado 'pendiente'
- Debe usar los partidos y candidatos configurados por el Super Admin
- Un formulario E-14 es único por mesa y tipo de elección

---

## 6. Auditor Electoral

### Descripción
Supervisa y audita todas las operaciones sin poder modificar datos.

### Ubicación
- **Nivel**: Variable (puede ser nacional, departamental o municipal)
- **Alcance**: Según su asignación

### Responsabilidades Principales

#### A. Consulta de Datos
- ✅ Ver todos los formularios E-14
- ✅ Ver todos los E-24 generados
- ✅ Ver consolidados de todos los niveles
- ✅ Ver usuarios geolocalizados

#### B. Auditoría
- ✅ Identificar inconsistencias
- ✅ Verificar integridad de datos
- ✅ Generar reportes de auditoría
- ✅ Verificar hash de PDFs

#### C. Monitoreo
- ✅ Ver estadísticas en tiempo real
- ✅ Monitorear progreso de carga
- ✅ Ver discrepancias

### Endpoints Principales

```
GET  /api/formularios/:id                                # Ver E-14
GET  /api/auditor/consolidados                           # Consolidados
GET  /api/auditor/discrepancias                          # Discrepancias
GET  /api/auditor/estadisticas                           # Estadísticas
GET  /api/verificacion-presencia/usuarios-geolocalizados # Geolocalización
```

### Flujo de Trabajo

```
1. DURANTE LAS ELECCIONES
   ├── Monitorear ingreso de E-14
   ├── Verificar validaciones
   ├── Identificar discrepancias
   └── Generar alertas

2. POST-ELECCIONES
   ├── Auditar E-24 generados
   ├── Verificar hash de PDFs
   ├── Comparar consolidados
   ├── Generar informe de auditoría
   └── Certificar resultados
```

### ⚠️ IMPORTANTE
- El auditor **NO puede modificar** datos
- Solo tiene permisos de lectura
- Puede acceder a todos los niveles según su asignación

---

## Matriz de Permisos

| Acción | Super Admin | Coord. Depto | Coord. Muni | Coord. Puesto | Testigo | Auditor | Monitoreo |
|--------|-------------|--------------|-------------|---------------|---------|---------|-----------|
| **Configuración** |
| Configurar partidos/candidatos | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Crear usuarios | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Formularios E-14** |
| Crear E-14 | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Editar E-14 | ❌ | ❌ | ❌ | ❌ | ✅* | ❌ | ❌ |
| Validar E-14 | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Ver E-14 | ✅ | ✅** | ✅** | ✅** | ✅*** | ✅ | ✅ |
| **Consolidación E-24** |
| Generar E-24 Puesto | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Generar E-24 Municipal | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Generar E-24 Depto | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Ver consolidados | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| **Incidentes y Delitos** |
| Reportar incidente | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Ver incidentes | ✅ | ✅** | ✅** | ✅** | ✅*** | ✅ | ✅ |
| Resolver incidente | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Reportar delito | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Investigar delito | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| Denunciar formalmente | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| **Verificación de Presencia** |
| Registrar presencia | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Ver estado de equipo | ✅ | ✅** | ✅** | ✅** | ❌ | ✅ | ✅ |
| Ver geolocalización | ✅ | ✅** | ✅** | ✅** | ❌ | ✅ | ✅ |
| **Monitoreo** |
| Ver dashboard monitoreo | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Ver estadísticas globales | ✅ | ✅** | ✅** | ✅** | ❌ | ✅ | ✅ |
| Ver mapa en tiempo real | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Ver alertas del sistema | ✅ | ✅** | ✅** | ✅** | ❌ | ✅ | ✅ |
| Exportar reportes | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |

*Solo sus propios E-14 en estado 'pendiente'  
**Solo de su jurisdicción  
***Solo los propios

---

## Flujo Completo del Sistema

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SUPER ADMIN                                  │
│  • Configura partidos, candidatos, tipos de elección               │
│  • Carga DIVIPOLA (departamentos, municipios, puestos, mesas)      │
│  • Crea coordinadores departamentales                               │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   COORDINADOR DEPARTAMENTAL                          │
│  • Crea coordinadores municipales                                   │
│  • Supervisa municipios                                             │
│  • Genera E-24 Departamental                                        │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   COORDINADOR MUNICIPAL                              │
│  • Crea coordinadores de puesto                                     │
│  • Supervisa puestos                                                │
│  • Genera E-24 Municipal (requiere 80% de puestos)                 │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   COORDINADOR DE PUESTO                              │
│  • Crea testigos para sus mesas                                     │
│  • VALIDA formularios E-14                                          │
│  • Genera E-24 de Puesto                                            │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      TESTIGO ELECTORAL                               │
│  • Registra votos en E-14                                           │
│  • Reporta incidentes y delitos                                     │
│  • Registra presencia (GPS)                                         │
│  • Espera validación del coordinador                                │
└─────────────────────────────────────────────────────────────────────┘

                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      AUDITOR ELECTORAL                               │
│  • Supervisa todo el proceso                                        │
│  • Verifica integridad de datos                                     │
│  • Genera informes de auditoría                                     │
└─────────────────────────────────────────────────────────────────────┘

                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         MONITOREO                                    │
│  • Visualiza todo en tiempo real                                    │
│  • Dashboard con mapa de geolocalización                            │
│  • Estadísticas y alertas                                           │
│  • Exporta reportes (solo lectura)                                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Dependencias Críticas

### Para que el sistema funcione:

1. **Super Admin debe configurar**:
   - ✅ Tipos de elección (al menos 1 activo)
   - ✅ Partidos políticos (al menos 2 activos)
   - ✅ Candidatos (al menos 2 activos)
   - ✅ DIVIPOLA completo (departamentos → municipios → puestos → mesas)

2. **Coordinadores deben crear usuarios**:
   - ✅ Cada nivel crea usuarios del nivel inferior
   - ✅ Cada usuario debe estar asociado a su ubicación

3. **Testigos deben registrar votos**:
   - ✅ Crear E-14 para cada mesa
   - ✅ Usar partidos y candidatos configurados

4. **Coordinadores de puesto deben validar**:
   - ✅ Solo E-14 validados se incluyen en E-24
   - ✅ Sin validación, no hay consolidación

5. **Para generar E-24**:
   - ✅ E-24 Puesto: Requiere E-14 validados
   - ✅ E-24 Municipal: Requiere 80% de puestos completos
   - ✅ E-24 Departamental: Requiere E-24 municipales

---

## Verificación por Rol

### Super Admin
```sql
-- Verificar configuración
SELECT COUNT(*) FROM tipos_eleccion WHERE activo = 1;  -- Debe ser > 0
SELECT COUNT(*) FROM partidos WHERE activo = 1;        -- Debe ser > 1
SELECT COUNT(*) FROM candidatos WHERE activo = 1;      -- Debe ser > 1
SELECT COUNT(*) FROM locations WHERE tipo = 'mesa';    -- Debe ser > 0
```

### Coordinador de Puesto
```sql
-- Verificar E-14 de su puesto
SELECT estado, COUNT(*) 
FROM formularios_e14 f
JOIN locations m ON f.mesa_id = m.id
WHERE m.puesto_id = :puesto_id
GROUP BY estado;
```

### Coordinador Municipal
```sql
-- Verificar progreso de puestos
SELECT 
    p.nombre,
    COUNT(DISTINCT f.id) as formularios,
    COUNT(DISTINCT CASE WHEN f.estado = 'validado' THEN f.id END) as validados
FROM locations p
LEFT JOIN locations m ON m.puesto_id = p.id
LEFT JOIN formularios_e14 f ON f.mesa_id = m.id
WHERE p.municipio_id = :municipio_id AND p.tipo = 'puesto'
GROUP BY p.id, p.nombre;
```

---

## 7. Monitoreo

### Descripción
Rol especializado en monitoreo en tiempo real del proceso electoral. Visualiza datos agregados, geolocalización de usuarios, estadísticas y alertas sin poder modificar datos.

### Ubicación
- **Nivel**: Nacional (sin ubicación específica)
- **Alcance**: Todo el sistema (solo lectura)

### Responsabilidades Principales

#### A. Monitoreo en Tiempo Real
- ✅ Ver usuarios activos con geolocalización
- ✅ Monitorear presencia de testigos
- ✅ Ver actividad reciente del sistema
- ✅ Monitorear formularios E-14 en tiempo real
- ✅ Ver estado de consolidación

#### B. Estadísticas y Métricas
- ✅ Ver estadísticas globales
- ✅ Ver estadísticas por departamento
- ✅ Ver métricas de rendimiento
- ✅ Ver tendencias de participación
- ✅ Ver comparativas entre departamentos

#### C. Alertas y Notificaciones
- ✅ Ver alertas del sistema
- ✅ Monitorear incidentes reportados
- ✅ Monitorear delitos reportados
- ✅ Ver usuarios inactivos
- ✅ Ver mesas sin formulario

#### D. Visualizaciones
- ✅ Mapa de calor de actividad
- ✅ Gráficos de tendencias
- ✅ Dashboard en tiempo real
- ✅ Comparativas visuales
- ✅ Predicciones de participación

#### E. Reportes
- ✅ Exportar reportes en tiempo real
- ✅ Generar reportes por departamento
- ✅ Exportar datos de actividad
- ✅ Generar reportes de incidentes

### Endpoints Principales

```
# Monitoreo en tiempo real
GET  /monitoreo/usuarios-activos                         # Usuarios con GPS
GET  /monitoreo/estadisticas                             # Estadísticas globales
GET  /monitoreo/alertas                                  # Alertas del sistema
GET  /monitoreo/actividad-reciente                       # Actividad reciente

# Estadísticas por nivel
GET  /monitoreo/estadisticas-departamento/:codigo        # Stats por depto
GET  /monitoreo/comparativa-departamentos                # Comparar deptos

# Visualizaciones
GET  /monitoreo/mapa-calor                               # Mapa de calor
GET  /monitoreo/tendencias                               # Tendencias
GET  /monitoreo/predicciones                             # Predicciones

# Métricas
GET  /monitoreo/metricas-rendimiento                     # Métricas del sistema

# Reportes
GET  /monitoreo/exportar-reporte                         # Exportar reporte
```

### Flujo de Trabajo

```
1. INICIO DE JORNADA
   ├── Iniciar sesión
   ├── Abrir dashboard de monitoreo
   ├── Verificar que todos los sistemas están activos
   └── Configurar alertas

2. DURANTE LAS ELECCIONES
   ├── Monitorear usuarios activos en tiempo real
   ├── Ver geolocalización de testigos
   ├── Monitorear ingreso de E-14
   ├── Ver estadísticas en tiempo real
   ├── Identificar alertas:
   │   ├── Testigos inactivos
   │   ├── Mesas sin formulario
   │   ├── Incidentes reportados
   │   └── Delitos reportados
   ├── Ver tendencias de participación
   └── Generar reportes periódicos

3. ANÁLISIS
   ├── Ver comparativas entre departamentos
   ├── Analizar mapa de calor
   ├── Ver predicciones de participación
   ├── Identificar patrones anómalos
   └── Generar reportes de análisis

4. FIN DE JORNADA
   ├── Generar reporte final
   ├── Exportar datos del día
   ├── Documentar observaciones
   └── Archivar información
```

### Características Especiales

#### Optimización
- ✅ **Caché inteligente**: Datos cacheados por 20-30 segundos
- ✅ **Consultas optimizadas**: Agregaciones eficientes en BD
- ✅ **Paginación**: Manejo de grandes volúmenes de datos
- ✅ **Actualización automática**: Dashboard se actualiza solo

#### Visualizaciones
- ✅ **Mapa en tiempo real**: Geolocalización de todos los usuarios
- ✅ **Gráficos dinámicos**: Tendencias y estadísticas
- ✅ **Alertas visuales**: Notificaciones en pantalla
- ✅ **Dashboard responsive**: Funciona en cualquier dispositivo

#### Datos Monitoreados

```javascript
// Usuarios activos
{
  "total_usuarios": 1500,
  "usuarios_con_geolocalizacion": 1450,
  "testigos_activos": 1200,
  "testigos_con_presencia": 1180,
  "coordinadores_activos": 250
}

// Formularios E-14
{
  "total_formularios": 800,
  "formularios_pendientes": 150,
  "formularios_validados": 600,
  "formularios_rechazados": 50,
  "porcentaje_completado": 66.7
}

// Incidentes y delitos
{
  "total_incidentes": 45,
  "incidentes_criticos": 5,
  "incidentes_resueltos": 30,
  "total_delitos": 12,
  "delitos_en_investigacion": 8
}

// Alertas
{
  "testigos_inactivos": 20,
  "mesas_sin_formulario": 200,
  "incidentes_sin_resolver": 15,
  "usuarios_fuera_de_rango": 5
}
```

### ⚠️ IMPORTANTE
- El rol de Monitoreo **NO puede modificar** datos
- Solo tiene permisos de **lectura**
- No puede validar formularios
- No puede resolver incidentes
- No puede crear usuarios
- Su función es **observar y reportar**

### Dashboard de Monitoreo

**Ruta**: `/monitoreo/dashboard`

**Secciones**:
1. **Mapa en tiempo real**
   - Geolocalización de todos los usuarios
   - Código de colores por rol
   - Información al hacer clic

2. **Estadísticas globales**
   - Total de usuarios activos
   - Formularios registrados
   - Porcentaje de avance
   - Incidentes y delitos

3. **Alertas activas**
   - Testigos inactivos
   - Mesas sin formulario
   - Incidentes críticos
   - Delitos reportados

4. **Gráficos de tendencias**
   - Participación por hora
   - Formularios por departamento
   - Incidentes por tipo
   - Actividad en tiempo real

5. **Actividad reciente**
   - Últimos formularios registrados
   - Últimos incidentes reportados
   - Últimas validaciones
   - Últimas geolocalizaciones

---

## Sistema de Incidentes y Delitos Electorales

### Descripción
Sistema para reportar, gestionar y dar seguimiento a incidentes y delitos durante el proceso electoral.

### Tipos de Incidentes

| Tipo | Descripción | Severidad Típica |
|------|-------------|------------------|
| Retraso en apertura | Mesa no abre a tiempo | Media |
| Falta de material | Material electoral faltante | Alta |
| Problemas técnicos | Fallas en equipos | Media |
| Irregularidades | Irregularidades en el proceso | Alta |
| Ausencia de funcionarios | Jurados o funcionarios ausentes | Alta |
| Problemas de acceso | Dificultad para acceder al puesto | Media |
| Disturbios | Alteración del orden | Crítica |
| Otros | Otros incidentes | Variable |

### Tipos de Delitos

| Tipo | Descripción | Gravedad Típica |
|------|-------------|-----------------|
| Compra de votos | Ofrecer dinero/bienes por votos | Grave |
| Coacción al votante | Amenazas o presión | Muy grave |
| Fraude electoral | Manipulación de resultados | Muy grave |
| Suplantación de identidad | Votar con identidad falsa | Grave |
| Alteración de resultados | Cambiar actas o resultados | Muy grave |
| Violencia electoral | Agresiones físicas | Muy grave |
| Propaganda ilegal | Propaganda en lugares prohibidos | Media |
| Financiación ilegal | Financiación irregular de campaña | Grave |
| Otros delitos | Otros delitos electorales | Variable |

### Flujo de Gestión de Incidentes

```
1. REPORTE (Testigo)
   ├── Detecta incidente
   ├── Registra en el sistema
   ├── Adjunta evidencia (opcional)
   ├── Registra GPS
   └── Estado: 'reportado'

2. REVISIÓN (Coordinador de Puesto)
   ├── Recibe notificación
   ├── Revisa incidente
   ├── Evalúa severidad
   ├── Decide acción:
   │   ├── Resolver localmente
   │   ├── Escalar a municipal
   │   └── Escalar a departamental
   └── Estado: 'en_revision'

3. RESOLUCIÓN
   ├── Se toman acciones correctivas
   ├── Se documenta la solución
   ├── Se notifica al reportante
   └── Estado: 'resuelto'

4. ESCALAMIENTO (si es necesario)
   ├── Se escala al nivel superior
   ├── Coordinador superior revisa
   ├── Se toman acciones de mayor alcance
   └── Estado: 'escalado'
```

### Flujo de Gestión de Delitos

```
1. REPORTE (Testigo/Coordinador)
   ├── Detecta delito
   ├── Registra en el sistema
   ├── Adjunta evidencia
   ├── Registra testigos adicionales
   ├── Registra GPS
   └── Estado: 'reportado'

2. INVESTIGACIÓN (Coordinador/Auditor)
   ├── Recibe notificación
   ├── Inicia investigación
   ├── Recopila evidencia adicional
   ├── Entrevista testigos
   ├── Documenta hallazgos
   └── Estado: 'en_investigacion'

3. EVALUACIÓN
   ├── Se evalúa la gravedad
   ├── Se determina si procede denuncia
   ├── Se documenta resultado
   └── Estado: 'investigado'

4. DENUNCIA FORMAL (si procede)
   ├── Se prepara denuncia
   ├── Se presenta ante autoridad competente
   ├── Se registra número de denuncia
   ├── Se hace seguimiento
   └── Estado: 'denunciado'

5. ARCHIVO (si no procede)
   ├── Se documenta razón
   ├── Se archiva el caso
   └── Estado: 'archivado'
```

### Niveles de Severidad/Gravedad

#### Incidentes
- **Baja**: No afecta el proceso electoral
- **Media**: Afecta parcialmente el proceso
- **Alta**: Afecta significativamente el proceso
- **Crítica**: Impide el proceso electoral

#### Delitos
- **Leve**: Infracción menor
- **Media**: Delito que requiere investigación
- **Grave**: Delito que afecta la integridad electoral
- **Muy grave**: Delito que compromete el proceso

### Permisos por Rol

| Acción | Testigo | Coord. Puesto | Coord. Muni | Coord. Depto | Auditor | Super Admin |
|--------|---------|---------------|-------------|--------------|---------|-------------|
| Reportar incidente | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ver incidentes propios | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ver todos incidentes | ❌ | ✅* | ✅** | ✅*** | ✅ | ✅ |
| Resolver incidente | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |
| Escalar incidente | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Reportar delito | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Investigar delito | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Denunciar formalmente | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |

*Solo de su puesto  
**Solo de su municipio  
***Solo de su departamento

### Datos Registrados

#### Incidente
```json
{
  "id": 123,
  "tipo_incidente": "falta_material",
  "titulo": "Falta de bolígrafos",
  "descripcion": "La mesa no tiene suficientes bolígrafos",
  "severidad": "media",
  "estado": "reportado",
  "reportado_por": "Juan Pérez (Testigo)",
  "mesa": "Mesa 001",
  "puesto": "Puesto Central",
  "evidencia_url": "/uploads/foto123.jpg",
  "ubicacion_gps": "4.6097,-74.0817",
  "fecha_incidente": "2024-11-30T08:30:00",
  "fecha_reporte": "2024-11-30T08:35:00"
}
```

#### Delito
```json
{
  "id": 456,
  "tipo_delito": "compra_votos",
  "titulo": "Intento de compra de votos",
  "descripcion": "Persona ofreciendo dinero por votos",
  "gravedad": "grave",
  "estado": "en_investigacion",
  "reportado_por": "María García (Testigo)",
  "mesa": "Mesa 002",
  "evidencia_url": "/uploads/video456.mp4",
  "testigos_adicionales": "Pedro López, Ana Martínez",
  "ubicacion_gps": "4.6097,-74.0817",
  "fecha_delito": "2024-11-30T09:00:00",
  "investigado_por": "Carlos Rodríguez (Coordinador)",
  "denunciado_formalmente": true,
  "numero_denuncia": "DEN-2024-001",
  "autoridad_competente": "Fiscalía Electoral"
}
```

---

## Sistema de Verificación de Presencia

### Descripción
Sistema de geolocalización para verificar que testigos y coordinadores estén presentes en sus ubicaciones asignadas.

### Funcionamiento

#### 1. Registro de Presencia
```javascript
// El testigo/coordinador registra su presencia
POST /api/verificacion/presencia
{
  "latitud": 4.6097,
  "longitud": -74.0817
}

// Respuesta
{
  "success": true,
  "presencia_verificada": true,
  "presencia_verificada_at": "2024-11-30T08:00:00",
  "rol": "testigo_electoral",
  "ubicacion": {
    "nombre": "Mesa 001 - Puesto Central",
    "tipo": "mesa"
  }
}
```

#### 2. Monitoreo de Equipo
```javascript
// Coordinador ve estado de su equipo
GET /api/verificacion/estado-equipo

// Respuesta
{
  "success": true,
  "data": [
    {
      "id": 123,
      "nombre": "Juan Pérez",
      "rol": "Testigo Electoral",
      "ubicacion": "Mesa 001",
      "presencia_verificada": true,
      "presencia_verificada_at": "2024-11-30T08:00:00",
      "ultimo_acceso": "2024-11-30T08:30:00",
      "minutos_inactivo": 5,
      "estado": "activo"
    },
    {
      "id": 124,
      "nombre": "María García",
      "rol": "Testigo Electoral",
      "ubicacion": "Mesa 002",
      "presencia_verificada": false,
      "ultimo_acceso": "2024-11-30T07:00:00",
      "minutos_inactivo": 95,
      "estado": "inactivo"
    }
  ]
}
```

### Estados de Presencia

| Estado | Descripción | Criterio |
|--------|-------------|----------|
| Activo | Usuario presente y activo | Última actividad < 15 min |
| Inactivo | Usuario sin actividad reciente | Última actividad 15-60 min |
| Ausente | Usuario no ha registrado presencia | Sin presencia verificada |
| Desconectado | Usuario sin actividad prolongada | Última actividad > 60 min |

### Datos Registrados

```sql
-- Tabla users (campos adicionales)
presencia_verificada BOOLEAN
presencia_verificada_at DATETIME
ultima_latitud DECIMAL(10,8)
ultima_longitud DECIMAL(11,8)
ultima_geolocalizacion_at DATETIME
ultimo_acceso DATETIME
```

### Alertas Automáticas

El sistema genera alertas cuando:
- ✅ Testigo no registra presencia 30 min antes del inicio
- ✅ Testigo inactivo por más de 30 minutos
- ✅ Testigo fuera del rango GPS del puesto (> 500m)
- ✅ Coordinador sin actividad por más de 60 minutos

### Permisos

| Acción | Testigo | Coord. Puesto | Coord. Muni | Coord. Depto | Super Admin |
|--------|---------|---------------|-------------|--------------|-------------|
| Registrar su presencia | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ver su estado | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ver equipo de puesto | ❌ | ✅ | ✅ | ✅ | ✅ |
| Ver equipo municipal | ❌ | ❌ | ✅ | ✅ | ✅ |
| Ver equipo departamental | ❌ | ❌ | ❌ | ✅ | ✅ |
| Ver todos los usuarios | ❌ | ❌ | ❌ | ❌ | ✅ |

---

**Última actualización**: 30 de Noviembre de 2025
**Versión**: 1.1
**Cambios**: Agregado sistema de incidentes/delitos y verificación de presencia
