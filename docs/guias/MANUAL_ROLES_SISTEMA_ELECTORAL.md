# MANUAL DEL SISTEMA ELECTORAL POR ROLES
## Sistema de Gestión Electoral - Guía Completa por Rol

---

## INTRODUCCIÓN AL SISTEMA

### ¿Qué es este sistema?

Sistema web para gestionar y reportar resultados electorales en tiempo real. Permite que testigos electorales reporten desde sus mesas, coordinadores monitoreen el proceso, y administradores gestionen toda la configuración.

### Datos Precargados en el Sistema

El sistema viene con **TODA la información de DIVIPOLA** (División Político-Administrativa de Colombia):

- ✅ **33 Departamentos** de Colombia
- ✅ **1,103 Municipios** completos
- ✅ **Zonas electorales** por municipio
- ✅ **Puestos de votación** configurables
- ✅ **Mesas** por cada puesto
- ✅ **Votantes registrados** por mesa (datos DIVIPOLA)

### Roles del Sistema

El sistema tiene **8 roles diferentes**, cada uno con funciones específicas:

1. **Super Administrador** - Control total del sistema
2. **Admin Departamental** - Gestión a nivel departamento
3. **Admin Municipal** - Gestión a nivel municipio
4. **Coordinador Departamental** - Monitoreo departamental
5. **Coordinador Municipal** - Monitoreo municipal
6. **Coordinador de Puesto** - Supervisión de puesto específico
7. **Testigo Electoral** - Reporte desde las mesas
8. **Auditor Electoral** - Revisión y validación

---

## ROL 1: SUPER ADMINISTRADOR

### ¿Qué hace el Super Administrador?

Es el rol con **control total** del sistema. Configura todo antes de las elecciones y gestiona usuarios.

### Credenciales por Defecto

```
Usuario: admin
Contraseña: admin123
```

⚠️ **IMPORTANTE**: Cambiar esta contraseña inmediatamente después de la primera instalación.

### Funciones Principales

#### 1. Gestión de Configuración Electoral

**Tipos de Elección**
- Crear y configurar tipos de elección (Presidente, Gobernador, Alcalde, Senado, etc.)
- Definir si es uninominal (un solo candidato) o por listas
- Activar/desactivar tipos según la jornada electoral

**Partidos Políticos**
- Registrar todos los partidos que participan
- Configurar colores y logos de cada partido
- Activar/desactivar partidos

**Candidatos**
- Registrar candidatos por cada tipo de elección
- Asignar candidatos a partidos
- Configurar números de lista (para elecciones por listas)
- Subir fotos de candidatos

#### 2. Gestión de Usuarios

**Crear Usuarios**
- Crear cuentas para todos los roles
- Asignar ubicaciones (departamento, municipio, zona, puesto)
- Generar credenciales de acceso

**Gestionar Usuarios Existentes**
- Activar/desactivar usuarios
- Resetear contraseñas
- Cambiar roles
- Reasignar ubicaciones

#### 3. Gestión de Ubicaciones

**Configurar Estructura Electoral**
- Verificar datos de DIVIPOLA cargados
- Crear/editar puestos de votación
- Configurar mesas por puesto
- Asignar votantes registrados por mesa

#### 4. Monitoreo General

**Dashboard del Super Admin**
- Ver estadísticas globales del sistema
- Monitorear todos los formularios E-14 enviados
- Ver cobertura por departamento/municipio
- Identificar problemas en tiempo real

### Flujo de Trabajo del Super Admin

#### ANTES DE LAS ELECCIONES

**Paso 1: Configurar Tipos de Elección**
1. Login al sistema
2. Ir a "Configuración Electoral" → "Tipos de Elección"
3. Crear cada tipo (ej: Gobernación, Asamblea, Alcaldía, Concejo)
4. Configurar si es uninominal o por listas

**Paso 2: Registrar Partidos**
1. Ir a "Configuración Electoral" → "Partidos"
2. Crear cada partido político
3. Asignar colores y logos
4. Activar los que participan en esta elección

**Paso 3: Registrar Candidatos**
1. Ir a "Configuración Electoral" → "Candidatos"
2. Para cada tipo de elección, crear candidatos
3. Asignar partido a cada candidato
4. Si es por listas, asignar número de lista

**Paso 4: Crear Coordinadores**
1. Ir a "Gestión de Usuarios" → "Crear Usuario"
2. Crear coordinadores departamentales (uno por departamento)
3. Crear coordinadores municipales (uno por municipio)
4. Crear coordinadores de puesto (uno por puesto)
5. Asignar ubicaciones correctamente

**Paso 5: Crear Testigos**
1. Ir a "Gestión de Usuarios" → "Crear Usuario"
2. Rol: "Testigo Electoral"
3. Asignar a puesto específico
4. Generar credenciales
5. Entregar credenciales a cada testigo

**Paso 6: Verificar Configuración**
1. Revisar que todos los datos estén correctos
2. Hacer pruebas con usuarios de prueba
3. Verificar que los formularios E-14 funcionen

#### DURANTE LAS ELECCIONES

**Monitoreo en Tiempo Real**
1. Ver dashboard principal
2. Monitorear presencia de testigos
3. Ver formularios E-14 que llegan
4. Identificar puestos sin reporte
5. Contactar coordinadores si hay problemas

**Soporte Técnico**
1. Resetear contraseñas si testigos olvidan
2. Desbloquear cuentas bloqueadas
3. Resolver problemas técnicos

#### DESPUÉS DE LAS ELECCIONES

**Consolidación de Resultados**
1. Verificar que todos los formularios estén completos
2. Exportar datos para análisis
3. Generar reportes finales
4. Hacer backup de la base de datos

---

## ROL 2: TESTIGO ELECTORAL

### ¿Qué hace el Testigo Electoral?

Es la persona en el puesto de votación que **reporta los resultados** de las mesas. Es el rol más importante el día de las elecciones.

### ¿Qué necesita el Testigo?

- ✅ Celular o tablet con internet
- ✅ Usuario y contraseña (proporcionados por el coordinador)
- ✅ Estar físicamente en el puesto asignado
- ✅ Acceso a los formularios E-14 físicos de las mesas

### Funciones del Testigo

1. **Registrar presencia** en el puesto
2. **Llenar formularios E-14** digitales
3. **Reportar resultados** de cada mesa
4. **Enviar datos** en tiempo real

### Flujo de Trabajo del Testigo - DÍA DE ELECCIONES

#### PASO 1: Preparación (Antes de las 8:00 AM)

**Antes de salir de casa:**
1. Cargar completamente el celular
2. Llevar cargador portátil
3. Verificar que tienes tus credenciales (usuario y contraseña)
4. Probar que puedes acceder al sistema

**Al llegar al puesto:**
1. Llegar temprano (antes de las 8:00 AM)
2. Ubicar las mesas asignadas
3. Presentarse con los jurados de votación
4. Ubicarse en un lugar donde puedas ver el proceso

#### PASO 2: Registrar Presencia (8:00 AM)

**¿Por qué es importante?**
- El sistema necesita saber que estás en el puesto
- Sin registrar presencia, NO podrás enviar formularios
- Los coordinadores monitorean quién está presente

**Cómo hacerlo:**
1. Abrir el navegador en tu celular
2. Ir a la URL del sistema (te la dará tu coordinador)
3. Ingresar tu usuario y contraseña
4. Clic en "Iniciar Sesión"
5. En el dashboard, verás un botón grande: **"Registrar Presencia"**
6. Clic en ese botón
7. Confirmar tu ubicación
8. ✅ Listo! El botón "Nuevo Formulario E-14" se habilitará automáticamente

⚠️ **MUY IMPORTANTE**: Si no registras presencia, el botón para crear formularios estará deshabilitado.

#### PASO 3: Esperar el Cierre (8:00 AM - 4:00 PM)

**Durante la votación:**
- Permanecer en el puesto
- Observar el proceso
- NO interferir con la votación
- Mantener el celular cargado
- Estar atento al cierre de las mesas

**A las 4:00 PM:**
- Las mesas cierran
- Comienza el escrutinio (conteo de votos)
- Observar el proceso de conteo
- Tomar fotos del formulario E-14 físico (como respaldo)

#### PASO 4: Llenar Formulario E-14 Digital (Después de las 4:00 PM)

**Cuando el escrutinio termine:**

1. **Abrir el sistema**
   - Ir al dashboard del testigo
   - Clic en **"Nuevo Formulario E-14"**

2. **Seleccionar Mesa**
   - Aparece un selector con todas las mesas del puesto
   - Elegir el número de mesa (ej: Mesa 001)
   - Los votantes registrados se cargan automáticamente

3. **Seleccionar Tipo de Elección**
   - Elegir qué elección vas a reportar (ej: Gobernación)
   - Los candidatos de ese tipo se cargan automáticamente

4. **Ingresar Votos por Candidato**
   - Aparece la lista de candidatos
   - Para cada candidato, ingresar el número de votos
   - Verificar que coincida con el E-14 físico
   - El sistema suma automáticamente

5. **Ingresar Otros Votos**
   - **Votos en blanco**: Tarjetas depositadas sin marcar ningún candidato
   - **Votos nulos**: Tarjetas marcadas incorrectamente (ej: marcaron 2 candidatos)
   - **Tarjetas no marcadas**: Tarjetas que no se usaron

6. **Verificar Totales**
   - El sistema calcula el total automáticamente
   - Verificar que coincida con el E-14 físico
   - Si hay diferencia, revisar los números

7. **Enviar Formulario**
   - Clic en "Enviar Formulario"
   - Esperar mensaje de confirmación
   - Guardar el número de confirmación

#### PASO 5: Formularios Adicionales

**Si hay múltiples tipos de elección:**
- Repetir el proceso para cada tipo
- Usar el mismo número de mesa
- Cambiar el tipo de elección
- Ingresar los votos correspondientes

**Ejemplo:**
- Formulario 1: Gobernación
- Formulario 2: Asamblea Departamental
- Formulario 3: Alcaldía
- Formulario 4: Concejo Municipal

### Pantallas del Testigo

#### Dashboard Principal
```
┌─────────────────────────────────────┐
│  DASHBOARD DEL TESTIGO              │
├─────────────────────────────────────┤
│                                     │
│  Puesto: Colegio San José           │
│  Mesas asignadas: 1, 2, 3, 4, 5    │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  REGISTRAR PRESENCIA        │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  NUEVO FORMULARIO E-14      │   │
│  │  (Deshabilitado hasta       │   │
│  │   registrar presencia)      │   │
│  └─────────────────────────────┘   │
│                                     │
│  Formularios enviados: 0            │
│                                     │
└─────────────────────────────────────┘
```

#### Formulario E-14
```
┌─────────────────────────────────────┐
│  FORMULARIO E-14                    │
├─────────────────────────────────────┤
│                                     │
│  Mesa: [Selector ▼]                 │
│  Votantes registrados: 300          │
│                                     │
│  Tipo de elección: [Selector ▼]    │
│                                     │
│  VOTOS POR CANDIDATO:               │
│  ┌─────────────────────────────┐   │
│  │ Juan Pérez (PL)    [  150 ] │   │
│  │ María García (PC)  [  100 ] │   │
│  │ Pedro López (PV)   [   30 ] │   │
│  └─────────────────────────────┘   │
│                                     │
│  Votos en blanco:    [   10 ]      │
│  Votos nulos:        [    5 ]      │
│  Tarjetas no marcadas: [  5 ]      │
│                                     │
│  TOTAL: 300 ✓                       │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  ENVIAR FORMULARIO          │   │
│  └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

### Consejos para el Testigo

#### ✅ SÍ Hacer

- Llegar temprano al puesto
- Registrar presencia inmediatamente
- Tomar fotos del E-14 físico como respaldo
- Verificar conexión a internet antes de enviar
- Enviar formularios lo más pronto posible
- Guardar confirmaciones de envío
- Contactar al coordinador si hay problemas
- Verificar dos veces los números antes de enviar

#### ❌ NO Hacer

- No compartir tu usuario y contraseña
- No registrar datos de otras mesas sin autorización
- No modificar datos después de enviar
- No abandonar el puesto antes del cierre
- No enviar datos sin verificar
- No inventar números si no estás seguro

### Problemas Comunes del Testigo

#### "No puedo iniciar sesión"
**Solución:**
1. Verificar usuario y contraseña (distingue mayúsculas/minúsculas)
2. Verificar conexión a internet
3. Contactar al coordinador para resetear contraseña

#### "El botón Nuevo Formulario está deshabilitado"
**Solución:**
1. Debes registrar presencia primero
2. Clic en "Registrar Presencia"
3. Esperar confirmación
4. El botón se habilitará automáticamente

#### "No aparecen los candidatos"
**Solución:**
1. Verificar que seleccionaste el tipo de elección correcto
2. Algunos tipos pueden no tener candidatos configurados
3. Contactar al coordinador

#### "Error al enviar formulario"
**Solución:**
1. Verificar conexión a internet
2. Verificar que todos los campos estén llenos
3. Verificar que los totales coincidan
4. Intentar nuevamente
5. Si persiste, contactar coordinador

#### "Los totales no coinciden"
**Solución:**
1. Revisar cada número ingresado
2. Verificar votos en blanco, nulos y no marcados
3. Comparar con E-14 físico
4. La suma debe ser igual a votantes registrados

---

## ROL 3: COORDINADOR DE PUESTO

### ¿Qué hace el Coordinador de Puesto?

Supervisa **un puesto de votación específico**. Monitorea a los testigos de ese puesto y verifica que envíen los formularios correctamente.

### Ubicación en la Jerarquía

```
Super Admin
    └── Coordinador Departamental
            └── Coordinador Municipal
                    └── COORDINADOR DE PUESTO ← Tú estás aquí
                            └── Testigos Electorales
```

### Funciones del Coordinador de Puesto

1. **Monitorear testigos** de su puesto
2. **Verificar presencia** de testigos
3. **Revisar formularios E-14** enviados
4. **Validar datos** antes de aprobar
5. **Contactar testigos** si hay problemas
6. **Reportar al coordinador municipal**

### Flujo de Trabajo del Coordinador de Puesto

#### ANTES DE LAS ELECCIONES

**Preparación:**
1. Recibir credenciales del coordinador municipal
2. Conocer el puesto asignado
3. Conocer a los testigos asignados
4. Tener contacto (teléfono) de cada testigo
5. Probar acceso al sistema

**Verificación:**
1. Verificar que todos los testigos tengan credenciales
2. Verificar que los testigos sepan usar el sistema
3. Coordinar hora de llegada al puesto

#### DÍA DE ELECCIONES

**Mañana (8:00 AM):**
1. Login al sistema
2. Ver dashboard del puesto
3. Verificar que testigos registren presencia
4. Contactar testigos que no lleguen

**Durante el día:**
1. Monitorear estado del puesto
2. Estar disponible para dudas de testigos
3. Verificar conexión de testigos

**Tarde (4:00 PM en adelante):**
1. Monitorear llegada de formularios E-14
2. Revisar cada formulario recibido
3. Validar que los datos sean correctos
4. Aprobar o rechazar formularios
5. Contactar testigos si hay errores

### Dashboard del Coordinador de Puesto

```
┌─────────────────────────────────────────────┐
│  COORDINADOR DE PUESTO                      │
│  Puesto: Colegio San José                   │
├─────────────────────────────────────────────┤
│                                             │
│  RESUMEN                                    │
│  ┌─────────────────────────────────────┐   │
│  │ Testigos asignados:        5        │   │
│  │ Testigos presentes:        4  ⚠️    │   │
│  │ Formularios recibidos:    12        │   │
│  │ Formularios validados:     8        │   │
│  │ Formularios pendientes:    4        │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  TESTIGOS                                   │
│  ┌─────────────────────────────────────┐   │
│  │ ✅ Juan Pérez      Presente          │   │
│  │    Formularios: 3/5                  │   │
│  │                                      │   │
│  │ ✅ María García    Presente          │   │
│  │    Formularios: 2/5                  │   │
│  │                                      │   │
│  │ ❌ Pedro López     Ausente  ⚠️       │   │
│  │    Formularios: 0/5                  │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  FORMULARIOS PENDIENTES                     │
│  ┌─────────────────────────────────────┐   │
│  │ Mesa 001 - Gobernación              │   │
│  │ Testigo: Juan Pérez                 │   │
│  │ [Ver] [Aprobar] [Rechazar]          │   │
│  └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

### Validación de Formularios

**Qué verificar:**
1. ✅ Que los totales coincidan
2. ✅ Que no haya números imposibles
3. ✅ Que esté completo
4. ✅ Que sea de una mesa del puesto

**Acciones:**
- **Aprobar**: Si todo está correcto
- **Rechazar**: Si hay errores (con motivo)
- **Contactar testigo**: Si hay dudas

---

## ROL 4: COORDINADOR MUNICIPAL

### ¿Qué hace el Coordinador Municipal?

Supervisa **todos los puestos de un municipio**. Monitorea a los coordinadores de puesto y consolida resultados municipales.

### Ubicación en la Jerarquía

```
Super Admin
    └── Coordinador Departamental
            └── COORDINADOR MUNICIPAL ← Tú estás aquí
                    └── Coordinadores de Puesto
                            └── Testigos Electorales
```

### Funciones del Coordinador Municipal

1. **Monitorear todos los puestos** del municipio
2. **Supervisar coordinadores de puesto**
3. **Consolidar resultados** municipales
4. **Identificar problemas** en puestos
5. **Reportar al coordinador departamental**
6. **Generar reportes** municipales

### Dashboard del Coordinador Municipal

```
┌─────────────────────────────────────────────┐
│  COORDINADOR MUNICIPAL                      │
│  Municipio: Florencia                       │
├─────────────────────────────────────────────┤
│                                             │
│  RESUMEN MUNICIPAL                          │
│  ┌─────────────────────────────────────┐   │
│  │ Puestos totales:          25        │   │
│  │ Puestos con reporte:      20  80%   │   │
│  │ Testigos presentes:      120/150    │   │
│  │ Formularios recibidos:   450/750    │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  PUESTOS POR ZONA                           │
│  ┌─────────────────────────────────────┐   │
│  │ Zona 1: 5/5 puestos ✅              │   │
│  │ Zona 2: 4/5 puestos ⚠️              │   │
│  │ Zona 3: 3/5 puestos ❌              │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  MAPA DE COBERTURA                          │
│  [Mapa con puestos en verde/amarillo/rojo]  │
│                                             │
│  RESULTADOS CONSOLIDADOS                    │
│  [Gráficos de resultados por candidato]     │
│                                             │
└─────────────────────────────────────────────┘
```

### Flujo de Trabajo del Coordinador Municipal

#### ANTES DE LAS ELECCIONES
1. Crear coordinadores de puesto
2. Asignar testigos a cada puesto
3. Entregar credenciales
4. Capacitar coordinadores y testigos

#### DÍA DE ELECCIONES
1. Monitorear cobertura en tiempo real
2. Identificar puestos sin reporte
3. Contactar coordinadores de puesto
4. Resolver problemas
5. Consolidar resultados

---

## ROL 5: COORDINADOR DEPARTAMENTAL

### ¿Qué hace el Coordinador Departamental?

Supervisa **todo un departamento**. Monitorea a los coordinadores municipales y consolida resultados departamentales.

### Ubicación en la Jerarquía

```
Super Admin
    └── COORDINADOR DEPARTAMENTAL ← Tú estás aquí
            └── Coordinadores Municipales
                    └── Coordinadores de Puesto
                            └── Testigos Electorales
```

### Funciones del Coordinador Departamental

1. **Monitorear todos los municipios** del departamento
2. **Supervisar coordinadores municipales**
3. **Consolidar resultados** departamentales
4. **Identificar problemas** regionales
5. **Reportar al super admin**
6. **Generar reportes** departamentales

### Dashboard del Coordinador Departamental

```
┌─────────────────────────────────────────────┐
│  COORDINADOR DEPARTAMENTAL                  │
│  Departamento: Caquetá                      │
├─────────────────────────────────────────────┤
│                                             │
│  RESUMEN DEPARTAMENTAL                      │
│  ┌─────────────────────────────────────┐   │
│  │ Municipios: 16                      │   │
│  │ Puestos totales: 350                │   │
│  │ Cobertura: 85%                      │   │
│  │ Formularios: 2,450/3,500            │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  MUNICIPIOS                                 │
│  ┌─────────────────────────────────────┐   │
│  │ ✅ Florencia      95% cobertura     │   │
│  │ ✅ San Vicente    90% cobertura     │   │
│  │ ⚠️  El Paujil     75% cobertura     │   │
│  │ ❌ Solano         45% cobertura     │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  RESULTADOS CONSOLIDADOS                    │
│  [Gráficos departamentales]                 │
│                                             │
└─────────────────────────────────────────────┘
```

---

## ROL 6: ADMIN DEPARTAMENTAL

### ¿Qué hace el Admin Departamental?

Gestiona la **configuración y usuarios** a nivel departamental. Similar al Super Admin pero limitado a su departamento.

### Diferencia con Coordinador Departamental

| Admin Departamental | Coordinador Departamental |
|---------------------|---------------------------|
| Crea y gestiona usuarios | Solo monitorea |
| Configura puestos y mesas | Solo visualiza |
| Asigna testigos | No asigna |
| Gestiona configuración | No gestiona |

### Funciones del Admin Departamental

1. **Crear usuarios** del departamento
2. **Gestionar coordinadores** municipales
3. **Configurar puestos** de votación
4. **Asignar testigos** a puestos
5. **Gestionar mesas** por puesto
6. **Resetear contraseñas** de su departamento

### Flujo de Trabajo

#### ANTES DE LAS ELECCIONES
1. Crear coordinadores municipales
2. Crear coordinadores de puesto
3. Crear testigos electorales
4. Configurar puestos y mesas
5. Asignar testigos a puestos
6. Entregar credenciales

#### DURANTE LAS ELECCIONES
1. Soporte técnico a usuarios
2. Resetear contraseñas
3. Desbloquear cuentas
4. Monitorear cobertura

---

## ROL 7: ADMIN MUNICIPAL

### ¿Qué hace el Admin Municipal?

Gestiona la **configuración y usuarios** a nivel municipal. Similar al Admin Departamental pero limitado a su municipio.

### Funciones del Admin Municipal

1. **Crear usuarios** del municipio
2. **Gestionar coordinadores** de puesto
3. **Configurar puestos** del municipio
4. **Asignar testigos** a puestos
5. **Gestionar mesas** por puesto
6. **Resetear contraseñas** de su municipio

### Alcance

- ✅ Puede gestionar su municipio
- ❌ No puede ver otros municipios
- ❌ No puede cambiar configuración departamental

---

## ROL 8: AUDITOR ELECTORAL

### ¿Qué hace el Auditor Electoral?

**Revisa y valida** todos los formularios E-14. Es un rol de control de calidad.

### Funciones del Auditor

1. **Revisar formularios E-14** enviados
2. **Validar datos** contra E-14 físicos
3. **Aprobar o rechazar** formularios
4. **Identificar inconsistencias**
5. **Generar reportes** de auditoría
6. **Marcar formularios sospechosos**

### Dashboard del Auditor

```
┌─────────────────────────────────────────────┐
│  AUDITOR ELECTORAL                          │
├─────────────────────────────────────────────┤
│                                             │
│  FORMULARIOS PARA AUDITAR                   │
│  ┌─────────────────────────────────────┐   │
│  │ Pendientes:        150              │   │
│  │ Auditados hoy:     320              │   │
│  │ Aprobados:         280              │   │
│  │ Rechazados:         40              │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  FORMULARIOS PENDIENTES                     │
│  ┌─────────────────────────────────────┐   │
│  │ Mesa 001 - Gobernación              │   │
│  │ Puesto: Colegio San José            │   │
│  │ Testigo: Juan Pérez                 │   │
│  │ Total votos: 300                    │   │
│  │ [Ver Detalle] [Aprobar] [Rechazar]  │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ALERTAS                                    │
│  ┌─────────────────────────────────────┐   │
│  │ ⚠️  Mesa 045: Totales no coinciden  │   │
│  │ ⚠️  Mesa 102: Votos > Registrados   │   │
│  └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

### Proceso de Auditoría

**Para cada formulario:**
1. Ver datos del formulario
2. Comparar con E-14 físico (si disponible)
3. Verificar totales
4. Verificar consistencia
5. Aprobar o rechazar con motivo

**Criterios de Rechazo:**
- Totales no coinciden
- Votos > Votantes registrados
- Datos incompletos
- Números imposibles
- Inconsistencias evidentes

---

## JERARQUÍA COMPLETA DEL SISTEMA

### Estructura Organizacional

```
┌─────────────────────────────────────────────────────────┐
│                    SUPER ADMINISTRADOR                  │
│              (Control total del sistema)                │
└────────────────────────┬────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
┌────────▼────────┐            ┌─────────▼────────┐
│ ADMIN           │            │ COORDINADOR      │
│ DEPARTAMENTAL   │            │ DEPARTAMENTAL    │
│ (Gestión)       │            │ (Monitoreo)      │
└────────┬────────┘            └─────────┬────────┘
         │                               │
         │        ┌──────────────────────┘
         │        │
┌────────▼────────▼──────┐
│ ADMIN MUNICIPAL        │
│ (Gestión municipal)    │
└────────┬────────────────┘
         │
         │        ┌──────────────────────┐
         │        │                      │
┌────────▼────────▼──────┐      ┌───────▼──────────┐
│ COORDINADOR MUNICIPAL  │      │ AUDITOR          │
│ (Monitoreo municipal)  │      │ ELECTORAL        │
└────────┬────────────────┘      │ (Validación)     │
         │                       └──────────────────┘
         │
┌────────▼────────────────┐
│ COORDINADOR DE PUESTO   │
│ (Supervisión puesto)    │
└────────┬────────────────┘
         │
┌────────▼────────────────┐
│ TESTIGO ELECTORAL       │
│ (Reporte desde mesa)    │
└─────────────────────────┘
```

### Permisos por Rol

| Función | Super Admin | Admin Dept | Admin Mun | Coord Dept | Coord Mun | Coord Puesto | Testigo | Auditor |
|---------|-------------|------------|-----------|------------|-----------|--------------|---------|---------|
| Configurar tipos elección | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Configurar partidos | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Configurar candidatos | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Crear usuarios (todos) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Crear usuarios (dept) | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Crear usuarios (mun) | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Ver todo el país | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Ver departamento | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| Ver municipio | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Ver puesto | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| Ver su mesa | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Registrar presencia | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Enviar formulario E-14 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Validar formularios | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| Aprobar formularios | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| Generar reportes | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |

---

## DATOS PRECARGADOS EN EL SISTEMA

### DIVIPOLA Completa

El sistema viene con **TODA la información oficial de DIVIPOLA**:

#### Departamentos (33)
```
05 - Antioquia         47 - Magdalena
08 - Atlántico         50 - Meta
11 - Bogotá D.C.       52 - Nariño
13 - Bolívar           54 - Norte de Santander
15 - Boyacá            63 - Quindío
17 - Caldas            66 - Risaralda
19 - Cauca             68 - Santander
20 - Cesar             70 - Sucre
23 - Córdoba           73 - Tolima
25 - Cundinamarca      76 - Valle del Cauca
27 - Chocó             81 - Arauca
41 - Huila             85 - Casanare
44 - Caquetá           86 - Putumayo
88 - San Andrés        91 - Amazonas
94 - Guainía           95 - Guaviare
97 - Vaupés            99 - Vichada
```

#### Municipios (1,103)

Todos los municipios de Colombia están precargados con:
- Código DIVIPOLA oficial
- Nombre completo
- Departamento al que pertenecen

#### Ejemplo: Caquetá (16 municipios)

```
44001 - Florencia (Capital)
44029 - Albania
44094 - Belén de los Andaquíes
44150 - Cartagena del Chairá
44205 - Curillo
44247 - El Doncello
44256 - El Paujil
44410 - La Montañita
44460 - Milán
44479 - Morelia
44592 - Puerto Rico
44610 - San José del Fragua
44753 - San Vicente del Caguán
44756 - Solano
44785 - Solita
44860 - Valparaíso
```

### Estructura de Ubicaciones

Cada ubicación en el sistema tiene esta jerarquía:

```
DEPARTAMENTO
    └── MUNICIPIO
            └── ZONA
                    └── PUESTO
                            └── MESA
```

**Ejemplo completo:**
```
Caquetá (Departamento)
    └── Florencia (Municipio)
            └── Zona 01 (Zona)
                    └── Colegio San José (Puesto)
                            └── Mesa 001 (Mesa)
                            └── Mesa 002 (Mesa)
                            └── Mesa 003 (Mesa)
```

### Datos de Votantes

Cada **mesa** tiene:
- Total de votantes registrados
- Número de mujeres
- Número de hombres

Estos datos vienen de DIVIPOLA y se cargan automáticamente.

---

## INICIALIZACIÓN DEL SISTEMA

### Primera Vez - Instalación

#### Opción 1: Desde Interfaz Web

1. Ejecutar `python run.py`
2. Abrir navegador en `http://localhost:5000`
3. Ir a `/init-db`
4. Clic en "Inicializar Base de Datos"
5. Esperar a que termine (puede tomar 2-3 minutos)
6. ✅ Sistema listo

#### Opción 2: Desde Línea de Comandos

```bash
python backend/scripts/load_basic_data_simple.py
```

### Qué se Carga Automáticamente

1. **Usuario Super Admin**
   - Usuario: `admin`
   - Contraseña: `admin123`

2. **Toda la DIVIPOLA**
   - 33 departamentos
   - 1,103 municipios
   - Códigos oficiales

3. **Tipos de Elección Básicos**
   - Presidente
   - Gobernador
   - Alcalde
   - Senado
   - Cámara
   - Asamblea
   - Concejo
   - JAL
   - Concejo de Juventudes

4. **Partidos Políticos Principales**
   - Partido Liberal
   - Partido Conservador
   - Partido Verde
   - Centro Democrático
   - Polo Democrático
   - Cambio Radical
   - (Y otros configurables)

### Después de Inicializar

**Pasos obligatorios:**

1. **Cambiar contraseña del admin**
   ```python
   # Desde consola Python
   from backend.models.user import User
   from backend.app import db
   
   admin = User.query.filter_by(username='admin').first()
   admin.set_password('nueva_contraseña_segura')
   db.session.commit()
   ```

2. **Configurar tipos de elección** para tu jornada específica

3. **Configurar candidatos** por cada tipo de elección

4. **Crear coordinadores** departamentales y municipales

5. **Crear testigos** y asignarlos a puestos

---

## FLUJO COMPLETO DEL SISTEMA

### Cronología de Uso

#### FASE 1: CONFIGURACIÓN (Semanas antes)

**Super Administrador:**
1. Instalar y configurar sistema
2. Cambiar contraseña por defecto
3. Configurar tipos de elección
4. Registrar partidos políticos
5. Registrar candidatos

**Admin Departamental:**
1. Crear coordinadores departamentales
2. Crear coordinadores municipales
3. Configurar zonas electorales

**Admin Municipal:**
1. Configurar puestos de votación
2. Configurar mesas por puesto
3. Asignar votantes registrados

#### FASE 2: PREPARACIÓN (Días antes)

**Admin Departamental/Municipal:**
1. Crear coordinadores de puesto
2. Crear testigos electorales
3. Asignar testigos a puestos específicos
4. Generar credenciales

**Coordinadores:**
1. Recibir credenciales
2. Contactar testigos asignados
3. Entregar credenciales a testigos
4. Capacitar testigos en uso del sistema

**Testigos:**
1. Recibir credenciales
2. Probar acceso al sistema
3. Familiarizarse con la interfaz
4. Conocer ubicación del puesto

#### FASE 3: DÍA DE ELECCIONES

**8:00 AM - Apertura**

**Testigos:**
1. Llegar al puesto asignado
2. Login al sistema
3. **Registrar presencia** ← CRÍTICO
4. Observar proceso de votación

**Coordinadores de Puesto:**
1. Login al sistema
2. Verificar presencia de testigos
3. Contactar testigos ausentes

**Coordinadores Municipal/Departamental:**
1. Monitorear cobertura general
2. Identificar puestos sin testigos
3. Coordinar soluciones

**8:00 AM - 4:00 PM - Votación**

**Testigos:**
- Permanecer en el puesto
- Mantener celular cargado
- Observar el proceso

**Coordinadores:**
- Monitorear en tiempo real
- Estar disponibles para soporte
- Resolver problemas

**4:00 PM - Cierre y Escrutinio**

**Testigos:**
1. Observar cierre de mesas
2. Observar escrutinio (conteo)
3. Tomar fotos del E-14 físico
4. Esperar a que termine el conteo

**4:30 PM en adelante - Envío de Resultados**

**Testigos:**
1. Login al sistema
2. Clic en "Nuevo Formulario E-14"
3. Seleccionar mesa
4. Seleccionar tipo de elección
5. Ingresar votos por candidato
6. Ingresar votos en blanco, nulos, no marcados
7. Verificar totales
8. Enviar formulario
9. Repetir para cada tipo de elección
10. Repetir para cada mesa (si tiene varias)

**Coordinadores de Puesto:**
1. Ver formularios que llegan
2. Revisar cada formulario
3. Validar datos
4. Aprobar o rechazar
5. Contactar testigos si hay errores

**Coordinadores Municipal/Departamental:**
1. Monitorear llegada de formularios
2. Ver consolidados en tiempo real
3. Identificar puestos sin reporte
4. Coordinar con coordinadores de puesto

**Auditores:**
1. Revisar formularios aprobados
2. Validar contra E-14 físicos
3. Aprobar definitivamente
4. Marcar inconsistencias

#### FASE 4: POST-ELECCIONES

**Super Administrador:**
1. Verificar que todos los formularios estén completos
2. Generar reportes finales
3. Exportar datos
4. Hacer backup de base de datos

**Coordinadores:**
1. Generar reportes de su área
2. Identificar lecciones aprendidas
3. Documentar problemas

---

## CASOS DE USO DETALLADOS

### Caso 1: Testigo Reporta Mesa Completa

**Escenario:**
- Testigo: Juan Pérez
- Puesto: Colegio San José
- Mesa: 001
- Tipos de elección: Gobernación, Asamblea, Alcaldía

**Proceso:**

1. **Registrar Presencia (8:00 AM)**
   ```
   Login → Dashboard → "Registrar Presencia" → Confirmar
   ✅ Presencia registrada
   ```

2. **Esperar Cierre (4:00 PM)**
   - Observar escrutinio
   - Tomar fotos del E-14

3. **Reportar Gobernación (4:30 PM)**
   ```
   "Nuevo Formulario E-14"
   Mesa: 001
   Tipo: Gobernación
   
   Candidato A (PL): 150 votos
   Candidato B (PC): 100 votos
   Candidato C (PV): 30 votos
   Votos en blanco: 10
   Votos nulos: 5
   Tarjetas no marcadas: 5
   
   Total: 300 ✓
   
   "Enviar" → ✅ Confirmación #12345
   ```

4. **Reportar Asamblea (4:35 PM)**
   ```
   "Nuevo Formulario E-14"
   Mesa: 001
   Tipo: Asamblea Departamental
   
   Lista 1 (PL): 120 votos
   Lista 2 (PC): 90 votos
   Lista 3 (PV): 60 votos
   Votos en blanco: 15
   Votos nulos: 10
   Tarjetas no marcadas: 5
   
   Total: 300 ✓
   
   "Enviar" → ✅ Confirmación #12346
   ```

5. **Reportar Alcaldía (4:40 PM)**
   ```
   Similar al proceso anterior...
   ```

### Caso 2: Coordinador de Puesto Valida Formularios

**Escenario:**
- Coordinador: María García
- Puesto: Colegio San José
- Formularios recibidos: 15

**Proceso:**

1. **Ver Formularios Pendientes**
   ```
   Dashboard → "Formularios Pendientes"
   
   Lista:
   - Mesa 001 - Gobernación (Juan Pérez)
   - Mesa 001 - Asamblea (Juan Pérez)
   - Mesa 002 - Gobernación (Pedro López)
   ...
   ```

2. **Revisar Formulario**
   ```
   Clic en "Mesa 001 - Gobernación"
   
   Ver:
   - Votantes registrados: 300
   - Total votos: 300 ✓
   - Votos por candidato
   - Votos en blanco: 10
   - Votos nulos: 5
   - Tarjetas no marcadas: 5
   
   Verificación:
   150 + 100 + 30 + 10 + 5 + 5 = 300 ✓
   ```

3. **Aprobar Formulario**
   ```
   Todo correcto → "Aprobar"
   ✅ Formulario aprobado
   ```

4. **Rechazar Formulario (si hay error)**
   ```
   Total no coincide → "Rechazar"
   Motivo: "Los totales no coinciden. 
            Verificar votos en blanco."
   
   ❌ Formulario rechazado
   → Notificación enviada al testigo
   ```

### Caso 3: Testigo Corrige Formulario Rechazado

**Escenario:**
- Formulario rechazado por error en totales

**Proceso:**

1. **Ver Notificación**
   ```
   Dashboard → "Formularios Rechazados"
   
   Mesa 001 - Gobernación
   Motivo: "Los totales no coinciden"
   ```

2. **Revisar E-14 Físico**
   - Comparar con foto tomada
   - Identificar error

3. **Crear Nuevo Formulario**
   ```
   "Nuevo Formulario E-14"
   Mesa: 001
   Tipo: Gobernación
   
   Ingresar datos correctos
   Verificar totales
   
   "Enviar" → ✅ Nueva confirmación
   ```

### Caso 4: Coordinador Municipal Identifica Problema

**Escenario:**
- Puesto sin reportes después de 2 horas del cierre

**Proceso:**

1. **Identificar Problema**
   ```
   Dashboard → Mapa de Cobertura
   
   ❌ Puesto "Escuela Rural" - 0 formularios
   ```

2. **Contactar Coordinador de Puesto**
   ```
   Ver contacto del coordinador
   Llamar por teléfono
   ```

3. **Diagnóstico**
   - Testigo sin señal de internet
   - Testigo olvidó contraseña
   - Testigo no llegó al puesto

4. **Solución**
   - Resetear contraseña
   - Enviar testigo de respaldo
   - Coordinar envío de datos

---

## PREGUNTAS FRECUENTES

### Para Testigos

**P: ¿Qué hago si olvido mi contraseña?**
R: Contacta inmediatamente a tu coordinador de puesto. Él puede resetear tu contraseña.

**P: ¿Puedo enviar formularios sin registrar presencia?**
R: No. Debes registrar presencia primero. El botón "Nuevo Formulario" estará deshabilitado hasta que lo hagas.

**P: ¿Qué hago si no tengo señal de internet?**
R: Busca un lugar con mejor señal. Si no es posible, contacta a tu coordinador para enviar los datos por otro medio.

**P: ¿Puedo modificar un formulario después de enviarlo?**
R: No. Una vez enviado, no se puede modificar. Si hay un error, el coordinador lo rechazará y deberás enviar uno nuevo.

**P: ¿Qué hago si los totales no coinciden?**
R: Revisa cada número ingresado. La suma de todos los votos debe ser igual a los votantes registrados.

### Para Coordinadores

**P: ¿Qué hago si un testigo no llega?**
R: Contacta al testigo. Si no responde, informa al coordinador municipal para enviar un testigo de respaldo.

**P: ¿Puedo aprobar un formulario con pequeños errores?**
R: No. Si hay errores, debes rechazarlo con el motivo específico para que el testigo lo corrija.

**P: ¿Cómo sé si un formulario es sospechoso?**
R: Verifica: totales que no coinciden, votos mayores a registrados, números imposibles, patrones extraños.

### Para Administradores

**P: ¿Cómo reseteo la contraseña de un usuario?**
R: Dashboard → Gestión de Usuarios → Buscar usuario → "Resetear Contraseña"

**P: ¿Puedo eliminar un usuario?**
R: Sí, pero mejor desactívalo. Así mantienes el historial.

**P: ¿Cómo creo múltiples testigos rápidamente?**
R: Usa la función de carga masiva desde CSV (si está habilitada) o crea un script.

---

## SOLUCIÓN DE PROBLEMAS

### Problema: No puedo iniciar sesión

**Síntomas:**
- Error "Usuario o contraseña incorrectos"
- Cuenta bloqueada

**Soluciones:**
1. Verificar usuario y contraseña (distingue mayúsculas)
2. Esperar 30 minutos si la cuenta está bloqueada
3. Contactar coordinador para resetear contraseña

### Problema: Botón "Nuevo Formulario" deshabilitado

**Causa:** No has registrado presencia

**Solución:**
1. Clic en "Registrar Presencia"
2. Confirmar ubicación
3. Esperar confirmación
4. El botón se habilitará automáticamente

### Problema: No aparecen candidatos

**Causas posibles:**
- Tipo de elección sin candidatos configurados
- Candidatos desactivados
- Error de configuración

**Solución:**
1. Verificar tipo de elección seleccionado
2. Contactar coordinador
3. Verificar con admin que los candidatos estén activos

### Problema: Error al enviar formulario

**Causas posibles:**
- Sin conexión a internet
- Datos incompletos
- Totales no coinciden
- Error del servidor

**Solución:**
1. Verificar conexión a internet
2. Verificar que todos los campos estén llenos
3. Verificar que los totales coincidan
4. Intentar nuevamente
5. Si persiste, contactar coordinador

### Problema: Base de datos no inicializa

**Síntomas:**
- Error al acceder a `/init-db`
- Tablas no se crean

**Solución:**
```bash
# Eliminar BD corrupta
rm instance/electoral.db

# Crear carpeta instance
mkdir instance

# Ejecutar script
python backend/scripts/load_basic_data_simple.py
```

---

## GLOSARIO

**DIVIPOLA**: División Político-Administrativa de Colombia. Sistema oficial de códigos para departamentos y municipios.

**E-14**: Formulario oficial de escrutinio de mesa. Documento donde se registran los votos de cada mesa.

**Escrutinio**: Proceso de conteo de votos al cierre de la votación.

**Mesa**: Unidad básica de votación. Cada mesa tiene aproximadamente 300-400 votantes registrados.

**Puesto de Votación**: Lugar físico donde se ubican varias mesas (ej: un colegio).

**Testigo Electoral**: Persona autorizada para observar el proceso electoral y reportar resultados.

**Uninominal**: Elección donde se vota por un solo candidato (ej: Presidente, Gobernador, Alcalde).

**Por Listas**: Elección donde se vota por una lista de candidatos de un partido (ej: Senado, Asamblea, Concejo).

**Votos en Blanco**: Tarjetas depositadas sin marcar ningún candidato.

**Votos Nulos**: Tarjetas marcadas incorrectamente (ej: marcaron 2 candidatos cuando solo se puede marcar 1).

**Tarjetas no Marcadas**: Tarjetas que no se usaron (sobrantes).

---

## CONTACTO Y SOPORTE

### Durante las Elecciones

**Testigos:**
- Contactar a tu Coordinador de Puesto

**Coordinadores de Puesto:**
- Contactar a tu Coordinador Municipal

**Coordinadores Municipales:**
- Contactar a tu Coordinador Departamental

**Coordinadores Departamentales:**
- Contactar al Super Administrador

### Soporte Técnico

Para problemas técnicos del sistema:
- Email: soporte@sistema-electoral.com
- Teléfono: [Número de soporte]
- WhatsApp: [Número de WhatsApp]

---

## CONCLUSIÓN

Este sistema está diseñado para ser **simple y eficiente**. Cada rol tiene funciones específicas y claras:

- **Super Admin**: Configura todo
- **Admins**: Crean usuarios y configuran ubicaciones
- **Coordinadores**: Monitorean y supervisan
- **Testigos**: Reportan resultados
- **Auditores**: Validan datos

La clave del éxito es:
1. ✅ Configurar bien antes de las elecciones
2. ✅ Capacitar a todos los usuarios
3. ✅ Registrar presencia temprano
4. ✅ Reportar resultados rápidamente
5. ✅ Validar datos cuidadosamente

**¡Éxito en tu jornada electoral!** 🗳️

