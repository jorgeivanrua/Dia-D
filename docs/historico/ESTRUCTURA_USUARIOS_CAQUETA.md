# 👥 Estructura de Usuarios para el Caquetá

## 🎯 Estructura Prevista

### Jerarquía de Usuarios

```
CAQUETÁ (Departamento)
│
├── 1 Super Admin (Nacional)
│   └── Gestión completa del sistema
│
├── 1 Coordinador Departamental (Caquetá)
│   └── Supervisión de todo el departamento
│
├── 16 Coordinadores Municipales (1 por municipio)
│   ├── Albania
│   ├── Belén de los Andaquíes
│   ├── Cartagena del Chairá
│   ├── Curillo
│   ├── El Doncello
│   ├── El Paujil
│   ├── Florencia (Capital)
│   ├── La Montañita
│   ├── Milán
│   ├── Morelia
│   ├── Puerto Rico
│   ├── San José del Fragua
│   ├── San Vicente del Caguán
│   ├── Solano
│   ├── Solita
│   └── Valparaíso
│
├── N Coordinadores de Puesto (1 por puesto de votación)
│   └── Depende del número de puestos en cada municipio
│
└── M Testigos Electorales (1 por mesa de votación)
    └── Depende del número de mesas en cada puesto
```

## 📊 Cálculo de Usuarios Necesarios

### Datos del Caquetá (Estimados)

| Nivel | Cantidad | Descripción |
|-------|----------|-------------|
| Super Admin | 1 | Administrador nacional |
| Coordinador Departamental | 1 | Para todo el Caquetá |
| Coordinadores Municipales | 16 | Uno por cada municipio |
| Coordinadores de Puesto | ~50-100 | Depende de puestos por municipio |
| Testigos Electorales | ~500-1000 | Depende de mesas por puesto |

### Ejemplo de Distribución

**Florencia (Capital)**:
- 1 Coordinador Municipal
- ~15-20 Coordinadores de Puesto
- ~150-200 Testigos Electorales

**Municipio Pequeño (ej. Curillo)**:
- 1 Coordinador Municipal
- ~2-3 Coordinadores de Puesto
- ~20-30 Testigos Electorales

## 🔐 Sistema de Autenticación por Ubicación

### Principio Fundamental
**Los usuarios se identifican por su ubicación geográfica, NO por nombre de usuario único.**

### Formato de Credenciales

#### 1. Super Admin
```
Usuario: super_admin
Contraseña: [contraseña segura]
Ubicación: Sin asignar (nacional)
```

#### 2. Coordinador Departamental
```
Usuario: CAQUETA
Contraseña: [contraseña del departamento]
Ubicación: Departamento Caquetá (código: 18)
```

#### 3. Coordinador Municipal
```
Usuario: FLORENCIA (o código del municipio)
Contraseña: [contraseña del municipio]
Ubicación: Municipio Florencia, Caquetá (código: 18001)
```

#### 4. Coordinador de Puesto
```
Usuario: PUESTO_001 (o código del puesto)
Contraseña: [contraseña del puesto]
Ubicación: Puesto de votación específico
```

#### 5. Testigo Electoral
```
Usuario: TESTIGO_001 (o código único)
Contraseña: [contraseña del testigo]
Ubicación Inicial: Puesto de votación
Ubicación Final: Mesa específica (se asigna al verificar presencia)
```

## 🔄 Flujo de Asignación de Testigos

### Fase 1: Creación del Testigo
```
1. Super Admin o Coordinador crea testigo
2. Asigna al PUESTO de votación
3. Genera credenciales:
   - Usuario: Basado en ubicación del puesto
   - Contraseña: Generada o asignada
```

### Fase 2: Llegada al Puesto (Día de Elecciones)
```
1. Testigo llega al puesto de votación
2. Inicia sesión con sus credenciales
3. Sistema detecta que está en el puesto correcto (GPS)
4. Testigo selecciona su MESA específica
5. Sistema verifica y asigna la mesa
```

### Fase 3: Verificación de Presencia
```
1. Testigo confirma presencia en la mesa
2. Sistema registra:
   - Geolocalización GPS
   - Hora de llegada
   - Mesa asignada
3. Testigo queda habilitado para registrar votos
```

### Fase 4: Registro de Votos
```
1. Testigo registra votos en formulario E-14
2. Sistema valida que está en la mesa correcta
3. Coordinador de puesto supervisa
4. Al finalizar, envía formulario
```

## 📋 Ejemplo Práctico: Florencia

### Estructura de Usuarios

```
CAQUETÁ (18)
└── FLORENCIA (18001)
    ├── Coordinador Municipal: "FLORENCIA"
    │   └── Contraseña: "Florencia2025!"
    │
    ├── PUESTO 001 - Colegio San José
    │   ├── Coordinador: "FLORENCIA_P001"
    │   │   └── Contraseña: "Puesto001!"
    │   │
    │   ├── Mesa 001
    │   │   └── Testigo: "FLORENCIA_P001_M001"
    │   │       └── Contraseña: "Mesa001!"
    │   │
    │   ├── Mesa 002
    │   │   └── Testigo: "FLORENCIA_P001_M002"
    │   │       └── Contraseña: "Mesa002!"
    │   │
    │   └── Mesa 003
    │       └── Testigo: "FLORENCIA_P001_M003"
    │           └── Contraseña: "Mesa003!"
    │
    └── PUESTO 002 - Escuela Normal
        ├── Coordinador: "FLORENCIA_P002"
        │   └── Contraseña: "Puesto002!"
        │
        ├── Mesa 001
        │   └── Testigo: "FLORENCIA_P002_M001"
        │       └── Contraseña: "Mesa001!"
        │
        └── Mesa 002
            └── Testigo: "FLORENCIA_P002_M002"
                └── Contraseña: "Mesa002!"
```

## 🗄️ Estructura en Base de Datos

### Tabla: users

| id | nombre | rol | ubicacion_id | password_hash |
|----|--------|-----|--------------|---------------|
| 1 | Super Admin | super_admin | NULL | [hash] |
| 2 | CAQUETA | coordinador_departamental | 1 (Depto) | [hash] |
| 3 | FLORENCIA | coordinador_municipal | 10 (Muni) | [hash] |
| 4 | FLORENCIA_P001 | coordinador_puesto | 50 (Puesto) | [hash] |
| 5 | FLORENCIA_P001_M001 | testigo_electoral | 100 (Mesa) | [hash] |

### Tabla: locations

| id | tipo | departamento_codigo | municipio_codigo | puesto_codigo | mesa_codigo | nombre_completo |
|----|------|---------------------|------------------|---------------|-------------|-----------------|
| 1 | departamento | 18 | NULL | NULL | NULL | Caquetá |
| 10 | municipio | 18 | 18001 | NULL | NULL | Florencia, Caquetá |
| 50 | puesto | 18 | 18001 | P001 | NULL | Puesto 001 - Colegio San José |
| 100 | mesa | 18 | 18001 | P001 | M001 | Mesa 001 - Puesto 001 |

## 🔧 Scripts de Creación de Usuarios

### Script para Crear Estructura Completa

```python
# backend/scripts/crear_usuarios_caqueta.py

def crear_estructura_caqueta():
    """
    Crear estructura completa de usuarios para el Caquetá
    """
    
    # 1. Coordinador Departamental
    crear_coordinador_departamental(
        departamento_codigo='18',
        password='Caqueta2025!'
    )
    
    # 2. Coordinadores Municipales (16)
    municipios = [
        '18001',  # Florencia
        '18029',  # Albania
        '18094',  # Belén de los Andaquíes
        # ... resto de municipios
    ]
    
    for municipio_codigo in municipios:
        crear_coordinador_municipal(
            departamento_codigo='18',
            municipio_codigo=municipio_codigo,
            password=f'Municipio{municipio_codigo}!'
        )
    
    # 3. Coordinadores de Puesto (por cada puesto)
    puestos = Location.query.filter_by(
        tipo='puesto',
        departamento_codigo='18'
    ).all()
    
    for puesto in puestos:
        crear_coordinador_puesto(
            puesto_id=puesto.id,
            password=f'Puesto{puesto.puesto_codigo}!'
        )
    
    # 4. Testigos (por cada mesa)
    mesas = Location.query.filter_by(
        tipo='mesa',
        departamento_codigo='18'
    ).all()
    
    for mesa in mesas:
        crear_testigo(
            mesa_id=mesa.id,
            password=f'Mesa{mesa.mesa_codigo}!'
        )
```

## 📱 Flujo de Usuario en Aplicación Móvil

### Coordinador de Puesto

```
1. Abrir app
2. Ingresar:
   - Usuario: FLORENCIA_P001
   - Contraseña: Puesto001!
3. App detecta ubicación GPS
4. Valida que está en el puesto correcto
5. Muestra dashboard con:
   - Lista de mesas del puesto
   - Testigos asignados
   - Estado de cada mesa
   - Formularios recibidos
```

### Testigo Electoral

```
1. Abrir app
2. Ingresar:
   - Usuario: FLORENCIA_P001_M001
   - Contraseña: Mesa001!
3. App detecta ubicación GPS
4. Valida que está en el puesto correcto
5. Muestra lista de mesas del puesto
6. Testigo selecciona su mesa (Mesa 001)
7. Sistema verifica y asigna
8. Testigo confirma presencia
9. Queda habilitado para registrar votos
```

## 🎯 Ventajas de Este Sistema

### 1. Seguridad por Ubicación
- Usuario vinculado a ubicación geográfica específica
- Validación GPS automática
- Difícil de suplantar

### 2. Simplicidad
- Credenciales basadas en ubicación
- Fácil de recordar
- Fácil de distribuir

### 3. Escalabilidad
- Fácil crear usuarios masivamente
- Patrón consistente
- Automatizable

### 4. Trazabilidad
- Cada acción vinculada a ubicación
- Auditoría completa
- Geolocalización en tiempo real

## 📊 Resumen de Usuarios para Caquetá

| Rol | Cantidad | Ubicación | Ejemplo de Usuario |
|-----|----------|-----------|-------------------|
| Super Admin | 1 | Nacional | super_admin |
| Coordinador Departamental | 1 | Caquetá | CAQUETA |
| Coordinador Municipal | 16 | Cada municipio | FLORENCIA |
| Coordinador de Puesto | ~80 | Cada puesto | FLORENCIA_P001 |
| Testigo Electoral | ~800 | Cada mesa | FLORENCIA_P001_M001 |
| **TOTAL** | **~898** | | |

## 🚀 Próximos Pasos

### 1. Cargar Datos del Caquetá
```bash
python backend/scripts/init_caqueta_electoral_data.py
```

### 2. Crear Usuarios Masivamente
```bash
python backend/scripts/crear_usuarios_caqueta.py
```

### 3. Generar Credenciales
```bash
python backend/scripts/generar_credenciales_caqueta.py
```

### 4. Exportar Lista de Usuarios
```bash
python backend/scripts/exportar_usuarios_excel.py
```

## 📝 Notas Importantes

### Contraseñas
- En desarrollo: Contraseñas simples basadas en ubicación
- En producción: Contraseñas seguras generadas aleatoriamente
- Cambio obligatorio en primer acceso

### Ubicaciones
- Todos los usuarios (excepto super_admin) DEBEN tener ubicación
- La ubicación determina qué datos puede ver/modificar
- La geolocalización GPS valida la presencia física

### Testigos
- Inicialmente asignados a PUESTO
- Al llegar, seleccionan su MESA específica
- Sistema verifica y actualiza ubicación
- Quedan vinculados a esa mesa todo el día

---

**Fecha**: 30 de Noviembre de 2025  
**Versión**: 1.0.0  
**Estado**: ✅ DOCUMENTADO
