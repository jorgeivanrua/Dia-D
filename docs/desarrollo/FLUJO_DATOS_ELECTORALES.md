# Flujo de Datos Electorales

## Resumen Ejecutivo

Este documento explica cómo fluyen los datos electorales desde la configuración del Super Admin hasta la consolidación final en formularios E-24.

> 📖 **Ver también**: [ROLES_Y_FLUJOS.md](./ROLES_Y_FLUJOS.md) para detalles completos de cada rol y sus responsabilidades.

### ⚠️ PUNTO CRÍTICO

**Los partidos, candidatos y tipos de elección configurados por el Super Admin son la BASE de todo el sistema**:

- Sin **partidos activos** → Los testigos NO pueden registrar votos
- Sin **candidatos activos** → Los testigos NO pueden registrar votos completos
- Sin **tipos de elección** → No se pueden crear formularios E-14
- Los **E-24** (consolidados) suman los votos por `partido_id` y `candidato_id`

### Flujo Simplificado

```
Super Admin → Testigos → Coordinadores → E-24
(Configura)   (E-14)     (Validan)      (Consolidan)
```

1. **Super Admin**: Configura partidos, candidatos y tipos de elección
2. **Testigos**: Registran votos en E-14 usando esos partidos/candidatos
3. **Coordinadores de Puesto**: Validan los E-14 (estado → 'validado')
4. **Coordinadores Municipales/Departamentales**: Generan E-24 que suman todos los E-14 validados

### Roles del Sistema

- **Super Admin**: Configuración global y supervisión total
- **Coordinador Departamental**: Supervisa municipios, genera E-24 departamental
- **Coordinador Municipal**: Supervisa puestos, genera E-24 municipal
- **Coordinador de Puesto**: Valida E-14, genera E-24 de puesto
- **Testigo Electoral**: Registra votos en E-14
- **Auditor Electoral**: Supervisa y audita (solo lectura)

## Arquitectura de Datos

### 1. Configuración Electoral (Super Admin)

El Super Admin configura tres entidades principales:

#### A. Tipos de Elección (`tipos_eleccion`)
- **Tabla**: `tipos_eleccion`
- **Endpoint GET**: `/api/super-admin/tipos-eleccion`
- **Endpoint POST**: `/api/super-admin/tipos-eleccion`
- **Campos principales**:
  - `id`, `codigo`, `nombre`
  - `es_uninominal`: True para presidencia/alcaldía, False para corporaciones
  - `activo`: Solo los activos se muestran a testigos

**Ejemplos**:
- Presidencia (uninominal)
- Senado (lista cerrada)
- Cámara de Representantes (lista cerrada)
- Gobernación (uninominal)
- Asamblea Departamental (lista cerrada)

#### B. Partidos Políticos (`partidos`)
- **Tabla**: `partidos`
- **Endpoint GET**: `/api/super-admin/partidos`
- **Endpoint POST**: `/api/super-admin/upload/partidos` (carga masiva Excel)
- **Campos principales**:
  - `id`, `codigo`, `nombre`, `nombre_corto`
  - `color`: Color hexadecimal (#RRGGBB)
  - `logo_url`: URL del logo
  - `activo`: Solo los activos se muestran a testigos
  - `orden`: Orden de visualización

**Usado por testigos**: `/api/testigo/partidos` (solo activos)

#### C. Candidatos (`candidatos`)
- **Tabla**: `candidatos`
- **Endpoint GET**: `/api/super-admin/candidatos`
- **Endpoint POST**: `/api/super-admin/upload/candidatos` (carga masiva Excel)
- **Campos principales**:
  - `id`, `codigo`, `nombre_completo`
  - `partido_id`: FK a `partidos`
  - `tipo_eleccion_id`: FK a `tipos_eleccion`
  - `numero_lista`: Número en la lista (opcional)
  - `es_independiente`: True si es candidato independiente
  - `activo`: Solo los activos se muestran a testigos
  - `orden`: Orden de visualización

**Usado por testigos**: `/api/testigo/candidatos?tipo_eleccion_id=X` (solo activos)

### 2. Registro de Votos (Testigos)

Los testigos registran votos en el Formulario E-14:

#### A. Formulario E-14 (`formularios_e14`)
- **Tabla**: `formularios_e14`
- **Restricción**: Una mesa solo puede tener un formulario por tipo de elección
- **Campos principales**:
  - `mesa_id`: FK a `locations` (tipo='mesa')
  - `testigo_id`: FK a `users` (rol='testigo')
  - `tipo_eleccion_id`: FK a `tipos_eleccion`
  - `total_votantes_registrados`, `total_votos`
  - `votos_validos`, `votos_nulos`, `votos_blancos`
  - `estado`: 'pendiente', 'validado', 'rechazado'

#### B. Votos por Partido (`votos_partidos`)
- **Tabla**: `votos_partidos`
- **Relación**: Muchos votos por formulario
- **Campos**:
  - `formulario_id`: FK a `formularios_e14`
  - `partido_id`: FK a `partidos`
  - `votos`: Cantidad de votos

**Usado por coordinadores**: Estos votos se suman en los E-24

#### C. Votos por Candidato (`votos_candidatos`)
- **Tabla**: `votos_candidatos`
- **Relación**: Muchos votos por formulario
- **Campos**:
  - `formulario_id`: FK a `formularios_e14`
  - `candidato_id`: FK a `candidatos`
  - `votos`: Cantidad de votos

**Usado por coordinadores**: Estos votos se suman en los E-24

### 3. Consolidación (Coordinadores)

Los coordinadores consolidan los E-14 en formularios E-24:

#### A. E-24 de Puesto (`formularios_e24_puesto`)
- **Generado por**: Coordinador de Puesto
- **Consolida**: Todos los E-14 validados del puesto
- **Proceso**:
  1. Suma votos de todas las mesas del puesto
  2. Agrupa por partido y candidato
  3. Genera PDF con totales
  4. Calcula hash del PDF para integridad

#### B. E-24 Municipal (`formularios_e24_municipal`)
- **Generado por**: Coordinador Municipal
- **Consolida**: Todos los E-14 validados del municipio
- **Requisito**: Mínimo 80% de puestos con datos completos
- **Proceso**:
  1. Suma votos de todos los puestos del municipio
  2. Agrupa por partido y candidato
  3. Genera PDF con totales
  4. Calcula hash del PDF para integridad
  5. Guarda votos consolidados en `votos_partidos_e24_municipal`

#### C. E-24 Departamental
- **Generado por**: Coordinador Departamental
- **Consolida**: Todos los E-14 validados del departamento
- **Proceso**: Similar al municipal pero a nivel departamental

## Flujo Completo

```
1. SUPER ADMIN configura:
   ├── Tipos de Elección (Presidencia, Senado, etc.)
   ├── Partidos Políticos (con logos y colores)
   └── Candidatos (asociados a partidos y tipos de elección)
   
   ⚠️ CRÍTICO: Sin esta configuración, el sistema no funciona

2. TESTIGO accede al sistema:
   ├── Ve su mesa asignada
   ├── Selecciona tipo de elección
   ├── Sistema carga:
   │   ├── Partidos activos (/api/testigo/partidos)
   │   └── Candidatos activos (/api/testigo/candidatos?tipo_eleccion_id=X)
   └── Registra votos en Formulario E-14
       ├── Datos generales (total votos, nulos, blancos)
       ├── Votos por partido (VotoPartido)
       └── Votos por candidato (VotoCandidato)

3. COORDINADOR DE PUESTO:
   ├── Ve todos los formularios E-14 de su puesto
   ├── Valida formularios (cambia estado a 'validado')
   ├── Consulta consolidado del puesto
   └── Genera E-24 de Puesto (PDF)
       └── Suma todos los E-14 validados del puesto

4. COORDINADOR MUNICIPAL:
   ├── Ve todos los E-24 de los puestos de su municipio
   ├── Consulta consolidado municipal
   └── Genera E-24 Municipal (PDF)
       └── Suma todos los E-14 validados del municipio
       └── Requiere mínimo 80% de puestos completos

5. COORDINADOR DEPARTAMENTAL:
   ├── Ve todos los E-24 municipales de su departamento
   ├── Consulta consolidado departamental
   └── Genera E-24 Departamental (PDF)
       └── Suma todos los E-14 validados del departamento

6. AUDITOR:
   └── Consulta y valida todos los formularios y consolidados
```

## Dependencias Críticas

### Para que TODO el sistema funcione:

1. **Debe existir al menos un Tipo de Elección activo**
   - Sin esto, no se puede crear formulario E-14
   - Los coordinadores no pueden generar E-24

2. **Deben existir Partidos activos**
   - Los testigos necesitan ver los partidos para registrar votos
   - Los E-24 agrupan votos por partido
   - **Si no hay partidos, los testigos no pueden registrar votos**

3. **Deben existir Candidatos activos**
   - Asociados al tipo de elección correcto
   - Asociados a un partido válido
   - Los E-24 también consolidan votos por candidato
   - **Si no hay candidatos, los testigos no pueden registrar votos completos**

4. **La mesa debe estar configurada**
   - Con ubicación (departamento, municipio, puesto, mesa)
   - Con testigo asignado

5. **Los E-14 deben estar validados**
   - Solo los E-14 con estado 'validado' se incluyen en E-24
   - Los coordinadores de puesto validan los E-14

### Cadena de Dependencias:

```
Super Admin configura → Testigos registran → Coordinadores validan → E-24 consolidan
     (Partidos,              (E-14 con           (Estado =              (Suman votos
      Candidatos,             votos por           'validado')            por partido
      Tipos)                  partido/candidato)                         y candidato)
```

**⚠️ IMPORTANTE**: Si el Super Admin no configura correctamente los partidos, candidatos y tipos de elección, toda la cadena se rompe y los testigos no pueden trabajar.

## Correcciones Aplicadas

### Problema Identificado
El dashboard del Super Admin no mostraba partidos, candidatos ni tipos de elección porque:
- Los IDs de los contenedores HTML no coincidían con los usados en JavaScript

### Solución Implementada
Archivo: `frontend/static/js/super-admin-init-fix.js`

**IDs corregidos**:
- `partiesList` → Muestra partidos
- `candidatesTableBody` → Muestra candidatos en tabla
- `electionTypesList` → Muestra tipos de elección

**Endpoints usados**:
- `/api/super-admin/partidos` → GET todos los partidos
- `/api/super-admin/candidatos` → GET todos los candidatos
- `/api/super-admin/tipos-eleccion` → GET todos los tipos

## Diagrama Visual del Flujo

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SUPER ADMIN                                  │
│  Configura:                                                          │
│  • Tipos de Elección (Presidencia, Senado, etc.)                   │
│  • Partidos Políticos (nombre, logo, color)                         │
│  • Candidatos (asociados a partido y tipo de elección)             │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          TESTIGOS                                    │
│  Mesa 001 → E-14 (Presidencia)                                      │
│    ├── Partido A: 150 votos                                         │
│    ├── Partido B: 120 votos                                         │
│    ├── Candidato X (Partido A): 150 votos                          │
│    └── Candidato Y (Partido B): 120 votos                          │
│                                                                      │
│  Mesa 002 → E-14 (Presidencia)                                      │
│    ├── Partido A: 180 votos                                         │
│    ├── Partido B: 140 votos                                         │
│    └── ...                                                           │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   COORDINADOR DE PUESTO                              │
│  Valida E-14 (estado → 'validado')                                  │
│  Genera E-24 de Puesto:                                             │
│    ├── Suma Mesa 001 + Mesa 002 + ... + Mesa N                     │
│    ├── Partido A: 330 votos (150+180)                              │
│    ├── Partido B: 260 votos (120+140)                              │
│    └── Genera PDF con totales                                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   COORDINADOR MUNICIPAL                              │
│  Genera E-24 Municipal:                                             │
│    ├── Suma Puesto 1 + Puesto 2 + ... + Puesto N                   │
│    ├── Partido A: 5,420 votos                                       │
│    ├── Partido B: 4,890 votos                                       │
│    ├── Requiere 80% de puestos completos                           │
│    └── Genera PDF con totales                                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 COORDINADOR DEPARTAMENTAL                            │
│  Genera E-24 Departamental:                                         │
│    ├── Suma Municipio 1 + Municipio 2 + ... + Municipio N          │
│    ├── Partido A: 125,340 votos                                     │
│    ├── Partido B: 98,760 votos                                      │
│    └── Genera PDF con totales                                       │
└─────────────────────────────────────────────────────────────────────┘

CLAVE:
• E-14 = Formulario de mesa (registrado por testigo)
• E-24 = Formulario consolidado (generado por coordinador)
• Los votos se suman por partido_id y candidato_id
• Solo se incluyen E-14 con estado 'validado'
```

## Verificación

Para verificar que todo funciona:

1. **Super Admin Dashboard**:
   - Abrir consola del navegador
   - Buscar logs: `[Fix] X partidos recibidos`
   - Verificar que se muestran en pantalla

2. **Testigo Dashboard**:
   - Iniciar sesión como testigo
   - Crear nuevo formulario
   - Verificar que se cargan partidos y candidatos

3. **Coordinador Dashboard**:
   - Ver consolidados de su nivel (puesto/municipal/departamental)
   - Generar E-24 y verificar que suma correctamente

4. **Base de Datos**:
   ```sql
   -- Verificar configuración
   SELECT COUNT(*) FROM tipos_eleccion WHERE activo = 1;
   SELECT COUNT(*) FROM partidos WHERE activo = 1;
   SELECT COUNT(*) FROM candidatos WHERE activo = 1;
   
   -- Verificar E-14
   SELECT COUNT(*) FROM formularios_e14 WHERE estado = 'validado';
   
   -- Verificar votos registrados
   SELECT p.nombre, SUM(vp.votos) as total_votos
   FROM votos_partidos vp
   JOIN partidos p ON vp.partido_id = p.id
   JOIN formularios_e14 f ON vp.formulario_id = f.id
   WHERE f.estado = 'validado'
   GROUP BY p.nombre
   ORDER BY total_votos DESC;
   ```

## Consolidación en E-24: Cómo se Suman los Votos

### Proceso de Consolidación

Los E-24 son formularios consolidados que suman los votos de múltiples E-14:

#### 1. E-24 de Puesto
```python
# Pseudocódigo del proceso
e14_validados = obtener_e14_validados_del_puesto(puesto_id, tipo_eleccion_id)

consolidado = {
    'votos_por_partido': {},
    'votos_por_candidato': {},
    'total_votos': 0,
    'votos_nulos': 0,
    'votos_blancos': 0
}

for e14 in e14_validados:
    # Sumar votos por partido
    for voto_partido in e14.votos_partidos:
        consolidado['votos_por_partido'][voto_partido.partido_id] += voto_partido.votos
    
    # Sumar votos por candidato
    for voto_candidato in e14.votos_candidatos:
        consolidado['votos_por_candidato'][voto_candidato.candidato_id] += voto_candidato.votos
    
    # Sumar totales
    consolidado['total_votos'] += e14.total_votos
    consolidado['votos_nulos'] += e14.votos_nulos
    consolidado['votos_blancos'] += e14.votos_blancos

# Generar PDF con los totales
generar_pdf_e24(consolidado)
```

#### 2. E-24 Municipal
- Suma TODOS los E-14 validados del municipio (de todos los puestos)
- Requiere mínimo 80% de puestos con datos completos
- Genera PDF y guarda en `formularios_e24_municipal`
- Los votos por partido se guardan en `votos_partidos_e24_municipal`

#### 3. E-24 Departamental
- Suma TODOS los E-14 validados del departamento (de todos los municipios)
- Similar al municipal pero a nivel departamental

### Tablas de E-24

```
formularios_e24_municipal
├── id
├── municipio_id
├── coordinador_id
├── tipo_eleccion_id
├── total_puestos
├── puestos_incluidos
├── total_mesas
├── total_votantes_registrados
├── total_votos
├── votos_validos
├── votos_nulos
├── votos_blanco
├── pdf_url (ruta del PDF generado)
├── pdf_hash (hash SHA-256 para integridad)
└── version (permite múltiples versiones)

votos_partidos_e24_municipal
├── id
├── e24_municipal_id
├── partido_id (FK a partidos)
└── votos (suma de todos los E-14)
```

### Importancia de los Datos del Super Admin

**Los partidos y candidatos configurados por el Super Admin son CRÍTICOS porque**:

1. **Los testigos los usan para registrar votos**
   - Sin partidos activos → No pueden registrar votos por partido
   - Sin candidatos activos → No pueden registrar votos por candidato

2. **Los E-24 los usan para consolidar**
   - Los votos se agrupan por `partido_id` y `candidato_id`
   - Si un partido se desactiva después, los votos históricos se mantienen
   - Los reportes muestran nombres de partidos/candidatos desde la BD

3. **Los reportes y estadísticas dependen de ellos**
   - Gráficos por partido
   - Tablas de resultados por candidato
   - Comparativas entre tipos de elección

## Notas Importantes

- Solo los registros con `activo = True` se muestran a los testigos
- El campo `orden` determina el orden de visualización
- Los candidatos deben estar asociados a un partido Y un tipo de elección
- Un formulario E-14 es único por mesa y tipo de elección
- Los E-24 solo incluyen E-14 con estado 'validado'
- Los votos se suman por `partido_id` y `candidato_id`, no por nombre
- Si se desactiva un partido/candidato, los votos históricos se mantienen
- Los E-24 generan PDFs con hash SHA-256 para garantizar integridad
