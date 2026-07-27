# Verificación Completa del Flujo del Sistema

## Fecha de Verificación
30 de Noviembre de 2025

---

## 1. Estructura de Usuarios y Ubicaciones

### Modelo de Usuario

#### Campos Principales
```python
id                          # ID único
nombre                      # Nombre del usuario
password_hash               # Contraseña hasheada
rol                         # Rol del usuario
ubicacion_id                # FK a locations (puede ser NULL)
activo                      # Estado activo/inactivo
```

#### Campos de Geolocalización
```python
ultima_latitud              # Última latitud GPS
ultima_longitud             # Última longitud GPS
ultima_geolocalizacion_at   # Timestamp de última geolocalización
precision_geolocalizacion   # Precisión en metros
```

#### Campos de Presencia
```python
presencia_verificada        # Boolean: ¿Verificó presencia?
presencia_verificada_at     # Timestamp de verificación
ultimo_acceso               # Último acceso al sistema
```

#### Roles Válidos
```python
'super_admin'                    # Sin ubicación
'admin_departamental'            # ubicacion_id → departamento
'admin_municipal'                # ubicacion_id → municipio
'coordinador_departamental'      # ubicacion_id → departamento
'coordinador_municipal'          # ubicacion_id → municipio
'coordinador_puesto'             # ubicacion_id → puesto
'testigo_electoral'              # ubicacion_id → mesa
'auditor_electoral'              # ubicacion_id → variable
'monitoreo'                      # Sin ubicación
```

### Modelo de Location (DIVIPOLA)

#### Jerarquía
```
Departamento
    ├── Municipio
    │   ├── Zona (opcional)
    │   │   ├── Puesto
    │   │   │   ├── Mesa 1
    │   │   │   ├── Mesa 2
    │   │   │   └── Mesa N
```

#### Campos de Jerarquía
```python
departamento_codigo         # Código del departamento (siempre presente)
municipio_codigo            # Código del municipio (NULL si es departamento)
zona_codigo                 # Código de zona (opcional)
puesto_codigo               # Código del puesto (NULL si no es puesto/mesa)
mesa_codigo                 # Código de mesa (NULL si no es mesa)
```

#### Campos de Ubicación
```python
tipo                        # 'departamento', 'municipio', 'zona', 'puesto', 'mesa'
nombre_completo             # Nombre completo jerárquico
latitud                     # Coordenada GPS del lugar
longitud                    # Coordenada GPS del lugar
direccion                   # Dirección física
```

#### Campos de Votantes
```python
total_votantes_registrados  # Total de votantes (solo para mesas)
mujeres                     # Cantidad de mujeres
hombres                     # Cantidad de hombres
```

---

## 2. Flujo de Creación de Usuarios por Rol

### 2.1 Super Admin

**Ubicación**: `ubicacion_id = NULL`

**Creado por**: Sistema (usuario inicial)

**Puede crear**:
- Coordinadores Departamentales
- Usuarios de cualquier rol

**Proceso de creación**:
```python
# Super Admin NO tiene ubicación
user = User(
    nombre='Super Admin',
    rol='super_admin',
    ubicacion_id=None,  # Sin ubicación
    activo=True
)
```

**Verificación**:
```sql
SELECT * FROM users WHERE rol = 'super_admin';
-- Debe tener ubicacion_id = NULL
```

---

### 2.2 Coordinador Departamental

**Ubicación**: `ubicacion_id` → Location con `tipo='departamento'`

**Creado por**: Super Admin

**Puede crear**:
- Coordinadores Municipales de su departamento
- Coordinadores de Puesto de su departamento

**Proceso de creación**:
```python
# 1. Buscar departamento
departamento = Location.query.filter_by(
    tipo='departamento',
    departamento_codigo='05'  # Ejemplo: Antioquia
).first()

# 2. Crear coordinador
coordinador = User(
    nombre='Coordinador Antioquia',
    rol='coordinador_departamental',
    ubicacion_id=departamento.id,  # ID del departamento
    activo=True
)
```

**Verificación**:
```sql
SELECT u.*, l.nombre_completo, l.tipo
FROM users u
JOIN locations l ON u.ubicacion_id = l.id
WHERE u.rol = 'coordinador_departamental'
  AND l.tipo = 'departamento';
-- Todos deben tener ubicación de tipo 'departamento'
```

**Alcance**:
- Ve todos los municipios de su departamento
- Ve todos los puestos de su departamento
- Ve todos los formularios de su departamento

---

### 2.3 Coordinador Municipal

**Ubicación**: `ubicacion_id` → Location con `tipo='municipio'`

**Creado por**: 
- Super Admin
- Coordinador Departamental (del mismo departamento)

**Puede crear**:
- Coordinadores de Puesto de su municipio

**Proceso de creación**:
```python
# 1. Buscar municipio
municipio = Location.query.filter_by(
    tipo='municipio',
    departamento_codigo='05',
    municipio_codigo='001'  # Ejemplo: Medellín
).first()

# 2. Crear coordinador
coordinador = User(
    nombre='Coordinador Medellín',
    rol='coordinador_municipal',
    ubicacion_id=municipio.id,  # ID del municipio
    activo=True
)
```

**Verificación**:
```sql
SELECT u.*, l.nombre_completo, l.tipo
FROM users u
JOIN locations l ON u.ubicacion_id = l.id
WHERE u.rol = 'coordinador_municipal'
  AND l.tipo = 'municipio';
-- Todos deben tener ubicación de tipo 'municipio'
```

**Alcance**:
- Ve todos los puestos de su municipio
- Ve todos los formularios de su municipio
- Genera E-24 Municipal

**Requisito para E-24 Municipal**:
- Mínimo 80% de puestos con datos completos

---

### 2.4 Coordinador de Puesto

**Ubicación**: `ubicacion_id` → Location con `tipo='puesto'`

**Creado por**:
- Super Admin
- Coordinador Departamental (del mismo departamento)
- Coordinador Municipal (del mismo municipio)

**Puede crear**:
- Testigos de las mesas de su puesto

**Proceso de creación**:
```python
# 1. Buscar puesto
puesto = Location.query.filter_by(
    tipo='puesto',
    departamento_codigo='05',
    municipio_codigo='001',
    zona_codigo='01',
    puesto_codigo='001'  # Ejemplo: Puesto Central
).first()

# 2. Crear coordinador
coordinador = User(
    nombre='Coordinador Puesto Central',
    rol='coordinador_puesto',
    ubicacion_id=puesto.id,  # ID del puesto
    activo=True
)
```

**Verificación**:
```sql
SELECT u.*, l.nombre_completo, l.tipo
FROM users u
JOIN locations l ON u.ubicacion_id = l.id
WHERE u.rol = 'coordinador_puesto'
  AND l.tipo = 'puesto';
-- Todos deben tener ubicación de tipo 'puesto'
```

**Alcance**:
- Ve todas las mesas de su puesto
- Ve todos los formularios de su puesto
- **VALIDA** formularios E-14 (rol crítico)
- Genera E-24 de Puesto

**Responsabilidad Crítica**:
- Es el ÚNICO que puede validar E-14
- Solo E-14 validados se incluyen en E-24

---

### 2.5 Testigo Electoral

**Ubicación**: `ubicacion_id` → Location con `tipo='mesa'`

**Creado por**:
- Super Admin
- Coordinador Departamental (del mismo departamento)
- Coordinador Municipal (del mismo municipio)
- Coordinador de Puesto (del mismo puesto)

**Proceso de creación**:
```python
# 1. Buscar mesa
mesa = Location.query.filter_by(
    tipo='mesa',
    departamento_codigo='05',
    municipio_codigo='001',
    zona_codigo='01',
    puesto_codigo='001',
    mesa_codigo='001'  # Ejemplo: Mesa 001
).first()

# 2. Crear testigo
testigo = User(
    nombre='Juan Pérez',
    rol='testigo_electoral',
    ubicacion_id=mesa.id,  # ID de la mesa
    activo=True
)
```

**Verificación**:
```sql
SELECT u.*, l.nombre_completo, l.tipo, l.mesa_codigo
FROM users u
JOIN locations l ON u.ubicacion_id = l.id
WHERE u.rol = 'testigo_electoral'
  AND l.tipo = 'mesa';
-- Todos deben tener ubicación de tipo 'mesa'
```

**Alcance**:
- Ve solo su mesa
- Crea formularios E-14 para su mesa
- Reporta incidentes y delitos
- Registra presencia con GPS

**Responsabilidades**:
1. **Verificar presencia**:
   ```python
   POST /api/verificacion/presencia
   {
     "latitud": 4.6097,
     "longitud": -74.0817
   }
   ```

2. **Crear E-14**:
   ```python
   POST /api/formularios
   {
     "mesa_id": mesa.id,
     "tipo_eleccion_id": 1,
     "total_votos": 500,
     "votos_partidos": [...],
     "votos_candidatos": [...]
   }
   ```

3. **Reportar incidentes**:
   ```python
   POST /api/incidentes
   {
     "tipo_incidente": "falta_material",
     "titulo": "Falta de bolígrafos",
     "descripcion": "...",
     "ubicacion_gps": "4.6097,-74.0817"
   }
   ```

---

### 2.6 Auditor Electoral

**Ubicación**: `ubicacion_id` → Variable (puede ser departamento, municipio, o NULL)

**Creado por**: Super Admin

**Proceso de creación**:
```python
# Auditor puede tener ubicación o no
auditor = User(
    nombre='Auditor Nacional',
    rol='auditor_electoral',
    ubicacion_id=None,  # O ID de departamento/municipio
    activo=True
)
```

**Alcance**:
- Si `ubicacion_id = NULL`: Ve todo el sistema
- Si `ubicacion_id = departamento`: Ve solo ese departamento
- Si `ubicacion_id = municipio`: Ve solo ese municipio

**Permisos**:
- Solo lectura
- No puede modificar datos
- Puede ver todos los formularios
- Puede ver todos los incidentes y delitos
- Puede exportar reportes

---

### 2.7 Monitoreo

**Ubicación**: `ubicacion_id = NULL`

**Creado por**: Super Admin

**Proceso de creación**:
```python
# Monitoreo NO tiene ubicación
monitoreo = User(
    nombre='Monitoreo',
    rol='monitoreo',
    ubicacion_id=None,  # Sin ubicación
    activo=True
)
```

**Verificación**:
```sql
SELECT * FROM users WHERE rol = 'monitoreo';
-- Debe tener ubicacion_id = NULL
```

**Alcance**:
- Ve todo el sistema en tiempo real
- Dashboard con mapa de geolocalización
- Estadísticas globales
- Alertas del sistema

**Permisos**:
- Solo lectura
- No puede modificar datos
- No puede crear usuarios
- No puede validar formularios

---

## 3. Flujo de Geolocalización

### 3.1 Registro de Presencia

**Quién puede registrar**:
- Todos los roles (excepto Super Admin y Monitoreo)

**Proceso**:
```javascript
// 1. Usuario abre la aplicación
// 2. Sistema solicita permiso de GPS
// 3. Usuario acepta
// 4. Sistema envía coordenadas

POST /api/verificacion/presencia
{
  "latitud": 4.6097,
  "longitud": -74.0817
}

// 5. Backend actualiza usuario
UPDATE users SET
  presencia_verificada = TRUE,
  presencia_verificada_at = NOW(),
  ultima_latitud = 4.6097,
  ultima_longitud = -74.0817,
  ultima_geolocalizacion_at = NOW(),
  ultimo_acceso = NOW()
WHERE id = :user_id;
```

### 3.2 Monitoreo de Presencia

**Coordinador de Puesto ve sus testigos**:
```javascript
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
      "estado": "activo",
      "latitud": 4.6097,
      "longitud": -74.0817
    }
  ]
}
```

**Monitoreo ve todos los usuarios**:
```javascript
GET /monitoreo/usuarios-activos

// Respuesta con TODOS los usuarios con GPS
{
  "success": true,
  "data": [
    {
      "id": 123,
      "nombre": "Juan Pérez",
      "rol": "testigo_electoral",
      "latitud": 4.6097,
      "longitud": -74.0817,
      "ultima_actualizacion": "2024-11-30T08:30:00",
      "ubicacion": {
        "nombre_completo": "Mesa 001 - Puesto Central - Medellín",
        "tipo": "mesa"
      }
    },
    // ... más usuarios
  ],
  "total": 1500
}
```

### 3.3 Alertas de Geolocalización

**Alertas automáticas**:
1. **Testigo sin presencia**: 30 min antes del inicio
2. **Testigo inactivo**: > 30 minutos sin actividad
3. **Testigo fuera de rango**: > 500m del puesto
4. **Coordinador inactivo**: > 60 minutos sin actividad

**Cálculo de distancia**:
```python
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """Calcular distancia entre dos puntos GPS en metros"""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371000  # Radio de la Tierra en metros
    return c * r

# Verificar si testigo está en el puesto
distancia = haversine(
    testigo.ultima_longitud,
    testigo.ultima_latitud,
    puesto.longitud,
    puesto.latitud
)

if distancia > 500:  # Más de 500 metros
    generar_alerta("Testigo fuera de rango")
```

---

## 4. Flujo de Formularios E-14

### 4.1 Creación por Testigo

**Restricción**: Un testigo solo puede crear E-14 para su mesa

```python
# Verificación en backend
testigo = User.query.get(user_id)
mesa = Location.query.get(testigo.ubicacion_id)

if mesa.tipo != 'mesa':
    return error("Usuario no es testigo de mesa")

# Verificar que no exista E-14 para esta mesa y tipo de elección
e14_existente = FormularioE14.query.filter_by(
    mesa_id=mesa.id,
    tipo_eleccion_id=tipo_eleccion_id
).first()

if e14_existente:
    return error("Ya existe un formulario para esta mesa y tipo de elección")

# Crear E-14
e14 = FormularioE14(
    mesa_id=mesa.id,
    testigo_id=testigo.id,
    tipo_eleccion_id=tipo_eleccion_id,
    estado='pendiente',  # Estado inicial
    ...
)
```

### 4.2 Validación por Coordinador de Puesto

**Restricción**: Solo puede validar E-14 de su puesto

```python
# Verificación en backend
coordinador = User.query.get(user_id)
puesto = Location.query.get(coordinador.ubicacion_id)

if puesto.tipo != 'puesto':
    return error("Usuario no es coordinador de puesto")

# Obtener E-14
e14 = FormularioE14.query.get(formulario_id)
mesa = Location.query.get(e14.mesa_id)

# Verificar que la mesa pertenece al puesto del coordinador
if mesa.puesto_codigo != puesto.puesto_codigo:
    return error("Este formulario no pertenece a su puesto")

# Validar
e14.estado = 'validado'
e14.validado_por_id = coordinador.id
e14.validado_at = datetime.now()
```

### 4.3 Consolidación en E-24

**E-24 de Puesto**:
```python
# Solo incluye E-14 validados del puesto
e14_validados = FormularioE14.query.join(Location).filter(
    Location.puesto_codigo == puesto.puesto_codigo,
    FormularioE14.estado == 'validado',
    FormularioE14.tipo_eleccion_id == tipo_eleccion_id
).all()

# Sumar votos
consolidado = {}
for e14 in e14_validados:
    for voto_partido in e14.votos_partidos:
        consolidado[voto_partido.partido_id] += voto_partido.votos
```

**E-24 Municipal**:
```python
# Verificar requisito del 80%
total_puestos = Location.query.filter_by(
    municipio_codigo=municipio.municipio_codigo,
    tipo='puesto'
).count()

puestos_con_datos = # Contar puestos con E-14 validados

if puestos_con_datos / total_puestos < 0.80:
    return error("Se requiere mínimo 80% de puestos completos")

# Consolidar todos los E-14 del municipio
e14_validados = FormularioE14.query.join(Location).filter(
    Location.municipio_codigo == municipio.municipio_codigo,
    FormularioE14.estado == 'validado',
    FormularioE14.tipo_eleccion_id == tipo_eleccion_id
).all()
```

---

## 5. Verificaciones SQL

### 5.1 Verificar Jerarquía de Usuarios

```sql
-- Verificar que cada rol tiene la ubicación correcta
SELECT 
    u.rol,
    l.tipo as tipo_ubicacion,
    COUNT(*) as cantidad
FROM users u
LEFT JOIN locations l ON u.ubicacion_id = l.id
GROUP BY u.rol, l.tipo
ORDER BY u.rol;

-- Resultado esperado:
-- super_admin          | NULL         | 1
-- coordinador_depto    | departamento | N
-- coordinador_muni     | municipio    | N
-- coordinador_puesto   | puesto       | N
-- testigo_electoral    | mesa         | N
-- auditor_electoral    | variable     | N
-- monitoreo            | NULL         | 1
```

### 5.2 Verificar Testigos con Presencia

```sql
-- Testigos que han verificado presencia
SELECT 
    u.nombre,
    l.nombre_completo as mesa,
    u.presencia_verificada,
    u.presencia_verificada_at,
    u.ultima_latitud,
    u.ultima_longitud,
    u.ultimo_acceso
FROM users u
JOIN locations l ON u.ubicacion_id = l.id
WHERE u.rol = 'testigo_electoral'
  AND l.tipo = 'mesa'
ORDER BY u.presencia_verificada DESC, u.ultimo_acceso DESC;
```

### 5.3 Verificar E-14 por Estado

```sql
-- Formularios por estado y puesto
SELECT 
    p.nombre_completo as puesto,
    f.estado,
    COUNT(*) as cantidad
FROM formularios_e14 f
JOIN locations m ON f.mesa_id = m.id
JOIN locations p ON m.puesto_codigo = p.puesto_codigo 
    AND p.tipo = 'puesto'
GROUP BY p.nombre_completo, f.estado
ORDER BY p.nombre_completo, f.estado;
```

### 5.4 Verificar Incidentes por Ubicación

```sql
-- Incidentes por puesto
SELECT 
    p.nombre_completo as puesto,
    i.tipo_incidente,
    i.severidad,
    i.estado,
    COUNT(*) as cantidad
FROM incidentes_electorales i
JOIN locations p ON i.puesto_id = p.id
WHERE p.tipo = 'puesto'
GROUP BY p.nombre_completo, i.tipo_incidente, i.severidad, i.estado
ORDER BY p.nombre_completo, i.severidad DESC;
```

---

## 6. Casos de Prueba

### Caso 1: Crear Jerarquía Completa

```python
# 1. Crear departamento
depto = Location(
    tipo='departamento',
    departamento_codigo='05',
    departamento_nombre='Antioquia',
    nombre_completo='Antioquia'
)

# 2. Crear municipio
muni = Location(
    tipo='municipio',
    departamento_codigo='05',
    municipio_codigo='001',
    departamento_nombre='Antioquia',
    municipio_nombre='Medellín',
    nombre_completo='Medellín - Antioquia'
)

# 3. Crear puesto
puesto = Location(
    tipo='puesto',
    departamento_codigo='05',
    municipio_codigo='001',
    zona_codigo='01',
    puesto_codigo='001',
    departamento_nombre='Antioquia',
    municipio_nombre='Medellín',
    puesto_nombre='Puesto Central',
    nombre_completo='Puesto Central - Medellín - Antioquia',
    latitud=6.2442,
    longitud=-75.5812
)

# 4. Crear mesa
mesa = Location(
    tipo='mesa',
    departamento_codigo='05',
    municipio_codigo='001',
    zona_codigo='01',
    puesto_codigo='001',
    mesa_codigo='001',
    departamento_nombre='Antioquia',
    municipio_nombre='Medellín',
    puesto_nombre='Puesto Central',
    mesa_nombre='Mesa 001',
    nombre_completo='Mesa 001 - Puesto Central - Medellín - Antioquia',
    total_votantes_registrados=500,
    mujeres=250,
    hombres=250
)
```

### Caso 2: Crear Usuarios de la Jerarquía

```python
# 1. Coordinador Departamental
coord_depto = User(
    nombre='Coordinador Antioquia',
    rol='coordinador_departamental',
    ubicacion_id=depto.id
)

# 2. Coordinador Municipal
coord_muni = User(
    nombre='Coordinador Medellín',
    rol='coordinador_municipal',
    ubicacion_id=muni.id
)

# 3. Coordinador de Puesto
coord_puesto = User(
    nombre='Coordinador Puesto Central',
    rol='coordinador_puesto',
    ubicacion_id=puesto.id
)

# 4. Testigo
testigo = User(
    nombre='Juan Pérez',
    rol='testigo_electoral',
    ubicacion_id=mesa.id
)
```

### Caso 3: Flujo Completo de E-14

```python
# 1. Testigo registra presencia
testigo.verificar_presencia()
testigo.ultima_latitud = 6.2442
testigo.ultima_longitud = -75.5812

# 2. Testigo crea E-14
e14 = FormularioE14(
    mesa_id=mesa.id,
    testigo_id=testigo.id,
    tipo_eleccion_id=1,
    estado='pendiente'
)

# 3. Coordinador valida
e14.estado = 'validado'
e14.validado_por_id = coord_puesto.id

# 4. Se incluye en E-24
# (automático al generar E-24)
```

---

## 7. Problemas Comunes y Soluciones

### Problema 1: Usuario sin ubicación

**Síntoma**: Usuario no puede acceder a sus datos

**Causa**: `ubicacion_id = NULL` cuando debería tener ubicación

**Solución**:
```sql
-- Verificar usuarios sin ubicación (excepto super_admin y monitoreo)
SELECT * FROM users 
WHERE ubicacion_id IS NULL 
  AND rol NOT IN ('super_admin', 'monitoreo');

-- Asignar ubicación
UPDATE users 
SET ubicacion_id = :location_id 
WHERE id = :user_id;
```

### Problema 2: Testigo en ubicación incorrecta

**Síntoma**: Testigo no puede crear E-14

**Causa**: `ubicacion_id` apunta a puesto en lugar de mesa

**Solución**:
```sql
-- Verificar testigos con ubicación incorrecta
SELECT u.*, l.tipo
FROM users u
JOIN locations l ON u.ubicacion_id = l.id
WHERE u.rol = 'testigo_electoral'
  AND l.tipo != 'mesa';

-- Corregir
UPDATE users 
SET ubicacion_id = :mesa_id 
WHERE id = :testigo_id;
```

### Problema 3: E-14 no se incluye en E-24

**Síntoma**: E-24 no suma todos los votos

**Causa**: E-14 no está en estado 'validado'

**Solución**:
```sql
-- Verificar E-14 pendientes
SELECT f.*, m.nombre_completo
FROM formularios_e14 f
JOIN locations m ON f.mesa_id = m.id
WHERE f.estado != 'validado';

-- Validar (solo coordinador de puesto puede hacer esto)
UPDATE formularios_e14 
SET estado = 'validado',
    validado_por_id = :coordinador_id,
    validado_at = NOW()
WHERE id = :formulario_id;
```

---

## 7. Tablas E-24 en Dashboards de Coordinadores

### 7.1 Estructura de Pestañas

Cada coordinador tiene pestañas en su dashboard para ver consolidados en tiempo real:

#### Coordinador de Puesto
```
Dashboard
├── Formularios (pestaña principal)
├── E-24 Consolidado (pestaña)  ← Tabla automática
│   ├── Estadísticas del puesto
│   ├── Tabla de votos por partido
│   ├── Tabla de votos por candidato
│   └── Botón "Generar PDF E-24"
└── Reportes
```

#### Coordinador Municipal
```
Dashboard
├── Puestos (pestaña principal)
├── Consolidado (pestaña)  ← Tabla automática
│   ├── Estadísticas del municipio
│   ├── Tabla por zonas
│   ├── Tabla de votos por partido
│   ├── Tabla de votos por candidato
│   └── Botón "Generar E-24 Municipal"
└── Reportes
```

#### Coordinador Departamental
```
Dashboard
├── Municipios (pestaña principal)
├── Consolidado (pestaña)  ← Tabla automática
│   ├── Estadísticas del departamento
│   ├── Tabla por municipios
│   ├── Tabla de votos por partido
│   ├── Tabla de votos por candidato
│   └── Botón "Generar E-24 Departamental"
└── Análisis
```

### 7.2 Llenado Automático de Tablas

Las tablas se llenan automáticamente con datos de E-14 validados:

#### Coordinador de Puesto

**Consulta automática**:
```sql
-- Se ejecuta cada vez que se abre la pestaña E-24
SELECT 
    m.mesa_codigo,
    m.nombre_completo as mesa,
    f.estado,
    f.total_votos,
    f.votos_validos,
    f.votos_nulos,
    f.votos_blancos
FROM formularios_e14 f
JOIN locations m ON f.mesa_id = m.id
WHERE m.puesto_codigo = :puesto_codigo
  AND f.estado = 'validado'
  AND f.tipo_eleccion_id = :tipo_eleccion_id
ORDER BY m.mesa_codigo;
```

**Tabla de votos por partido**:
```sql
SELECT 
    p.nombre as partido,
    p.nombre_corto,
    p.color,
    p.logo_url,
    SUM(vp.votos) as total_votos
FROM votos_partidos vp
JOIN partidos p ON vp.partido_id = p.id
JOIN formularios_e14 f ON vp.formulario_id = f.id
JOIN locations m ON f.mesa_id = m.id
WHERE m.puesto_codigo = :puesto_codigo
  AND f.estado = 'validado'
  AND f.tipo_eleccion_id = :tipo_eleccion_id
GROUP BY p.id, p.nombre, p.nombre_corto, p.color, p.logo_url
ORDER BY total_votos DESC;
```

**Renderizado en HTML**:
```html
<table class="table table-hover">
  <thead>
    <tr>
      <th>Mesa</th>
      <th>Total Votos</th>
      <th>Válidos</th>
      <th>Nulos</th>
      <th>Blancos</th>
      <th>Estado</th>
    </tr>
  </thead>
  <tbody id="e24TableBody">
    <!-- Se llena automáticamente con JavaScript -->
  </tbody>
</table>

<h5>Votos por Partido</h5>
<table class="table">
  <thead>
    <tr>
      <th>Partido</th>
      <th>Logo</th>
      <th>Votos</th>
      <th>%</th>
    </tr>
  </thead>
  <tbody id="votosPartidosTable">
    <!-- Se llena automáticamente -->
  </tbody>
</table>
```

#### Coordinador Municipal

**Consulta por zonas**:
```sql
-- Consolidado por zonas
SELECT 
    l.zona_codigo,
    COUNT(DISTINCT l.puesto_codigo) as total_puestos,
    COUNT(DISTINCT f.id) as total_formularios,
    SUM(f.total_votos) as total_votos
FROM locations l
LEFT JOIN locations m ON m.puesto_codigo = l.puesto_codigo 
    AND m.tipo = 'mesa'
LEFT JOIN formularios_e14 f ON f.mesa_id = m.id 
    AND f.estado = 'validado'
WHERE l.municipio_codigo = :municipio_codigo
  AND l.tipo = 'puesto'
GROUP BY l.zona_codigo
ORDER BY l.zona_codigo;
```

**Tabla de votos por partido (municipal)**:
```sql
SELECT 
    p.nombre as partido,
    p.nombre_corto,
    p.color,
    p.logo_url,
    SUM(vp.votos) as total_votos,
    ROUND(SUM(vp.votos) * 100.0 / SUM(SUM(vp.votos)) OVER(), 2) as porcentaje
FROM votos_partidos vp
JOIN partidos p ON vp.partido_id = p.id
JOIN formularios_e14 f ON vp.formulario_id = f.id
JOIN locations m ON f.mesa_id = m.id
WHERE m.municipio_codigo = :municipio_codigo
  AND f.estado = 'validado'
  AND f.tipo_eleccion_id = :tipo_eleccion_id
GROUP BY p.id, p.nombre, p.nombre_corto, p.color, p.logo_url
ORDER BY total_votos DESC;
```

**Renderizado**:
```html
<h5>Consolidado por Zonas</h5>
<table class="table">
  <thead>
    <tr>
      <th>Zona</th>
      <th>Puestos</th>
      <th>Formularios</th>
      <th>Total Votos</th>
      <th>% Avance</th>
    </tr>
  </thead>
  <tbody id="zonasTable">
    <!-- Se llena automáticamente -->
  </tbody>
</table>

<h5>Votos por Partido (Municipal)</h5>
<table class="table">
  <thead>
    <tr>
      <th>Partido</th>
      <th>Logo</th>
      <th>Votos</th>
      <th>%</th>
    </tr>
  </thead>
  <tbody id="votosPartidosMunicipalTable">
    <!-- Se llena automáticamente -->
  </tbody>
</table>
```

#### Coordinador Departamental

**Consulta por municipios**:
```sql
-- Consolidado por municipios
SELECT 
    l.municipio_codigo,
    l.municipio_nombre,
    COUNT(DISTINCT CASE WHEN l.tipo = 'puesto' THEN l.id END) as total_puestos,
    COUNT(DISTINCT f.id) as total_formularios,
    SUM(f.total_votos) as total_votos
FROM locations l
LEFT JOIN locations m ON m.municipio_codigo = l.municipio_codigo 
    AND m.tipo = 'mesa'
LEFT JOIN formularios_e14 f ON f.mesa_id = m.id 
    AND f.estado = 'validado'
WHERE l.departamento_codigo = :departamento_codigo
  AND l.tipo IN ('municipio', 'puesto')
GROUP BY l.municipio_codigo, l.municipio_nombre
ORDER BY l.municipio_nombre;
```

**Tabla de votos por partido (departamental)**:
```sql
SELECT 
    p.nombre as partido,
    p.nombre_corto,
    p.color,
    p.logo_url,
    SUM(vp.votos) as total_votos,
    ROUND(SUM(vp.votos) * 100.0 / SUM(SUM(vp.votos)) OVER(), 2) as porcentaje
FROM votos_partidos vp
JOIN partidos p ON vp.partido_id = p.id
JOIN formularios_e14 f ON vp.formulario_id = f.id
JOIN locations m ON f.mesa_id = m.id
WHERE m.departamento_codigo = :departamento_codigo
  AND f.estado = 'validado'
  AND f.tipo_eleccion_id = :tipo_eleccion_id
GROUP BY p.id, p.nombre, p.nombre_corto, p.color, p.logo_url
ORDER BY total_votos DESC;
```

### 7.3 Actualización en Tiempo Real

**JavaScript para actualización automática**:
```javascript
// Coordinador de Puesto
async function cargarConsolidadoE24() {
    try {
        const response = await APIClient.get('/formularios/consolidado');
        
        if (response.success) {
            const data = response.data;
            
            // Actualizar estadísticas
            document.getElementById('e24TotalMesas').textContent = data.total_mesas;
            document.getElementById('e24MesasValidadas').textContent = data.mesas_validadas;
            document.getElementById('e24TotalVotos').textContent = data.total_votos;
            
            // Llenar tabla de mesas
            const tbody = document.getElementById('e24TableBody');
            tbody.innerHTML = data.mesas.map(mesa => `
                <tr>
                    <td>${mesa.mesa_codigo}</td>
                    <td>${mesa.total_votos}</td>
                    <td>${mesa.votos_validos}</td>
                    <td>${mesa.votos_nulos}</td>
                    <td>${mesa.votos_blancos}</td>
                    <td><span class="badge bg-success">Validado</span></td>
                </tr>
            `).join('');
            
            // Llenar tabla de partidos
            const partidosBody = document.getElementById('votosPartidosTable');
            partidosBody.innerHTML = data.votos_partidos.map(vp => `
                <tr>
                    <td>${vp.partido_nombre}</td>
                    <td>
                        ${vp.logo_url ? 
                          `<img src="${vp.logo_url}" width="30" height="30">` :
                          vp.partido_nombre_corto
                        }
                    </td>
                    <td>${vp.total_votos}</td>
                    <td>${vp.porcentaje}%</td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error cargando consolidado:', error);
    }
}

// Actualizar cada 30 segundos
setInterval(cargarConsolidadoE24, 30000);

// Cargar al abrir la pestaña
document.getElementById('e24-tab').addEventListener('shown.bs.tab', function() {
    cargarConsolidadoE24();
});
```

### 7.4 Generación de PDF E-24

**Botón en cada pestaña**:
```html
<button class="btn btn-primary" onclick="generarPDFE24()">
    <i class="bi bi-file-pdf"></i> Generar E-24
</button>
```

**Proceso**:
```javascript
async function generarPDFE24() {
    if (!confirm('¿Generar PDF E-24 del puesto?')) return;
    
    try {
        const response = await APIClient.post('/formularios/puesto/generar-e24', {
            tipo_eleccion_id: tipoEleccionSeleccionado
        });
        
        if (response.success) {
            // Descargar PDF
            window.open(response.data.pdf_url, '_blank');
            alert('E-24 generado exitosamente');
        }
    } catch (error) {
        alert('Error generando E-24: ' + error.message);
    }
}
```

### 7.5 Requisitos para Generar E-24

#### Coordinador de Puesto
- ✅ Al menos 1 E-14 validado
- ✅ Todas las mesas deben tener E-14 (recomendado)

#### Coordinador Municipal
- ✅ Mínimo 80% de puestos con E-14 validados
- ✅ Al menos 1 E-14 validado por puesto

#### Coordinador Departamental
- ✅ Mínimo 80% de municipios con E-24 generados
- ✅ Cada municipio debe cumplir su requisito del 80%

### 7.6 Verificación de Tablas

**Consulta para verificar datos en tablas**:
```sql
-- Verificar que las tablas se llenan correctamente
-- Para Coordinador de Puesto
SELECT 
    'Puesto' as nivel,
    p.puesto_codigo,
    p.puesto_nombre,
    COUNT(DISTINCT m.id) as total_mesas,
    COUNT(DISTINCT CASE WHEN f.estado = 'validado' THEN f.id END) as mesas_validadas,
    SUM(CASE WHEN f.estado = 'validado' THEN f.total_votos ELSE 0 END) as total_votos
FROM locations p
LEFT JOIN locations m ON m.puesto_codigo = p.puesto_codigo AND m.tipo = 'mesa'
LEFT JOIN formularios_e14 f ON f.mesa_id = m.id
WHERE p.tipo = 'puesto'
  AND p.puesto_codigo = :puesto_codigo
GROUP BY p.puesto_codigo, p.puesto_nombre;

-- Para Coordinador Municipal
SELECT 
    'Municipal' as nivel,
    z.zona_codigo,
    COUNT(DISTINCT p.id) as total_puestos,
    COUNT(DISTINCT CASE WHEN f.estado = 'validado' THEN f.id END) as formularios_validados,
    SUM(CASE WHEN f.estado = 'validado' THEN f.total_votos ELSE 0 END) as total_votos
FROM locations z
LEFT JOIN locations p ON p.zona_codigo = z.zona_codigo AND p.tipo = 'puesto'
LEFT JOIN locations m ON m.puesto_codigo = p.puesto_codigo AND m.tipo = 'mesa'
LEFT JOIN formularios_e14 f ON f.mesa_id = m.id
WHERE z.municipio_codigo = :municipio_codigo
  AND z.tipo = 'zona'
GROUP BY z.zona_codigo;

-- Para Coordinador Departamental
SELECT 
    'Departamental' as nivel,
    mun.municipio_codigo,
    mun.municipio_nombre,
    COUNT(DISTINCT p.id) as total_puestos,
    COUNT(DISTINCT CASE WHEN f.estado = 'validado' THEN f.id END) as formularios_validados,
    SUM(CASE WHEN f.estado = 'validado' THEN f.total_votos ELSE 0 END) as total_votos
FROM locations mun
LEFT JOIN locations p ON p.municipio_codigo = mun.municipio_codigo AND p.tipo = 'puesto'
LEFT JOIN locations m ON m.puesto_codigo = p.puesto_codigo AND m.tipo = 'mesa'
LEFT JOIN formularios_e14 f ON f.mesa_id = m.id
WHERE mun.departamento_codigo = :departamento_codigo
  AND mun.tipo = 'municipio'
GROUP BY mun.municipio_codigo, mun.municipio_nombre;
```

---

## 8. Sistema de Logos de Partidos

### 7.1 Almacenamiento de Logos

**Campo en la base de datos**:
```sql
-- Tabla: partidos
logo_url VARCHAR(500)  -- URL del logo (puede ser externa o local)
```

**Tipos de URLs soportadas**:
1. **URLs externas** (Wikipedia, CDN):
   ```
   https://upload.wikimedia.org/wikipedia/commons/...
   ```

2. **URLs locales** (subidas al servidor):
   ```
   /static/uploads/logos/partido_liberal.png
   ```

### 7.2 Carga Automática desde Wikipedia

**Endpoint**: `POST /api/admin/cargar-logos-partidos`

**Proceso**:
```javascript
// 1. Usuario hace clic en "Cargar Logos"
// 2. Sistema busca coincidencias por nombre
// 3. Actualiza campo logo_url

// Partidos soportados:
const LOGOS_PARTIDOS = {
  'PARTIDO LIBERAL': 'https://upload.wikimedia.org/...',
  'PARTIDO CONSERVADOR': 'https://upload.wikimedia.org/...',
  'CENTRO DEMOCRÁTICO': 'https://upload.wikimedia.org/...',
  'PACTO HISTÓRICO': 'https://upload.wikimedia.org/...',
  'CAMBIO RADICAL': 'https://upload.wikimedia.org/...',
  'PARTIDO DE LA U': 'https://upload.wikimedia.org/...',
  'ALIANZA VERDE': 'https://upload.wikimedia.org/...',
  'POLO DEMOCRÁTICO': 'https://upload.wikimedia.org/...',
  'MIRA': 'https://upload.wikimedia.org/...',
  'COMUNES': 'https://upload.wikimedia.org/...'
};
```

**Algoritmo de búsqueda**:
1. Buscar por nombre exacto (mayúsculas)
2. Buscar por nombre_corto exacto
3. Buscar por coincidencia parcial
4. Si no encuentra, dejar logo_url = NULL

### 7.3 Uso de Logos en el Sistema

**En el Dashboard del Super Admin**:
```javascript
// Los logos se muestran en la lista de partidos
partidos.map(partido => `
  <div class="partido-item">
    ${partido.logo_url ? 
      `<img src="${partido.logo_url}" alt="${partido.nombre}" class="partido-logo">` :
      `<div class="partido-sin-logo">${partido.nombre_corto}</div>`
    }
    <span>${partido.nombre}</span>
  </div>
`)
```

**En el Formulario E-14 (Testigos)**:
```javascript
// Los testigos ven los logos al registrar votos
GET /api/testigo/partidos

// Respuesta:
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nombre": "Partido Liberal",
      "nombre_corto": "PL",
      "color": "#FF0000",
      "logo_url": "https://upload.wikimedia.org/..."
    }
  ]
}
```

**En los E-24 (PDFs)**:
```python
# Los logos se incluyen en los PDFs generados
if partido.logo_url:
    # Descargar imagen
    response = requests.get(partido.logo_url)
    img = Image(BytesIO(response.content), width=30, height=30)
    # Agregar al PDF
```

### 7.4 Verificación de Logos

**Consulta SQL**:
```sql
-- Verificar partidos con logo
SELECT 
    nombre,
    nombre_corto,
    CASE 
        WHEN logo_url IS NOT NULL THEN '✅ Con logo'
        ELSE '❌ Sin logo'
    END as estado_logo,
    logo_url
FROM partidos
WHERE activo = 1
ORDER BY nombre;
```

**Verificar URLs válidas**:
```python
import requests

def verificar_logos():
    partidos = Partido.query.filter_by(activo=True).all()
    
    for partido in partidos:
        if partido.logo_url:
            try:
                response = requests.head(partido.logo_url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ {partido.nombre}: Logo válido")
                else:
                    print(f"❌ {partido.nombre}: Logo no accesible ({response.status_code})")
            except Exception as e:
                print(f"❌ {partido.nombre}: Error - {str(e)}")
        else:
            print(f"⚠️  {partido.nombre}: Sin logo")
```

### 7.5 Carga Manual de Logos

**Opción 1: Actualizar directamente en BD**:
```sql
UPDATE partidos 
SET logo_url = 'https://ejemplo.com/logo.png'
WHERE id = 1;
```

**Opción 2: Subir archivo al servidor**:
```python
# Endpoint para subir logo
@app.route('/api/admin/upload-logo-partido/<int:partido_id>', methods=['POST'])
def upload_logo_partido(partido_id):
    file = request.files['logo']
    filename = secure_filename(file.filename)
    filepath = os.path.join('static/uploads/logos', filename)
    file.save(filepath)
    
    partido = Partido.query.get(partido_id)
    partido.logo_url = f'/static/uploads/logos/{filename}'
    db.session.commit()
```

**Opción 3: Usar Excel**:
```csv
nombre,nombre_corto,color,logo_url
Partido Liberal,PL,#FF0000,https://ejemplo.com/liberal.png
Partido Conservador,PC,#0000FF,https://ejemplo.com/conservador.png
```

### 7.6 Mejores Prácticas

1. **Usar URLs de Wikipedia**:
   - Son estables y confiables
   - No requieren almacenamiento local
   - Se actualizan automáticamente

2. **Tamaño de imágenes**:
   - Recomendado: 200x200 px
   - Formato: PNG con fondo transparente
   - Peso máximo: 100 KB

3. **Fallback**:
   - Si no hay logo, mostrar iniciales del partido
   - Usar color del partido como fondo

4. **Cache**:
   - Cachear logos en el navegador
   - Usar CDN si es posible

5. **Verificación periódica**:
   - Verificar que las URLs siguen funcionando
   - Actualizar URLs rotas

---

## 8. Checklist de Verificación

### Antes de Iniciar Elecciones

- [ ] Todos los departamentos tienen coordinador
- [ ] Todos los municipios tienen coordinador
- [ ] Todos los puestos tienen coordinador
- [ ] Todas las mesas tienen testigo
- [ ] Todos los testigos tienen `ubicacion_id` de tipo 'mesa'
- [ ] Todos los coordinadores tienen ubicación correcta
- [ ] Partidos políticos están activos
- [ ] Candidatos están activos
- [ ] Tipos de elección están activos

### Durante las Elecciones

- [ ] Testigos registran presencia
- [ ] Testigos están dentro del rango GPS (< 500m)
- [ ] E-14 se están creando
- [ ] Coordinadores están validando E-14
- [ ] No hay alertas críticas
- [ ] Incidentes se están resolviendo

### Después de las Elecciones

- [ ] Todos los E-14 están validados
- [ ] E-24 de puestos generados
- [ ] E-24 municipales generados (80% mínimo)
- [ ] E-24 departamentales generados
- [ ] Reportes exportados
- [ ] Auditoría completada

---

**Última actualización**: 30 de Noviembre de 2025  
**Versión**: 1.0  
**Estado**: ✅ Verificación Completa
