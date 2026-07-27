# 🏗️ Arquitectura del Sistema Electoral

## 📋 Visión General

Sistema web completo para gestión electoral con múltiples roles, registro de formularios E-14, consolidación en E-24, monitoreo en tiempo real, y gestión de incidentes y delitos electorales.

**Arquitectura:** Monolítica con patrón MVC  
**Backend:** Flask (Python 3.9+)  
**Frontend:** HTML5/CSS3/JavaScript (ES6+)  
**Base de Datos:** SQLite (desarrollo) / PostgreSQL (producción)  
**Autenticación:** JWT (JSON Web Tokens)  
**Geolocalización:** HTML5 Geolocation API

---

## 🎯 Principios de Diseño

### SOLID
- **S**ingle Responsibility: Cada clase tiene una responsabilidad única
- **O**pen/Closed: Abierto para extensión, cerrado para modificación
- **L**iskov Substitution: Subtipos deben ser sustituibles
- **I**nterface Segregation: Interfaces específicas mejor que generales
- **D**ependency Inversion: Depender de abstracciones, no de concreciones

### Otros Principios
- **DRY:** Don't Repeat Yourself
- **KISS:** Keep It Simple, Stupid
- **YAGNI:** You Aren't Gonna Need It
- **Separation of Concerns:** Separación clara de responsabilidades

---

## 📁 Estructura del Proyecto

```
sistema-electoral/
│
├── backend/                           # Backend Flask
│   ├── models/                        # Modelos de datos (ORM)
│   │   ├── user.py                   # Usuarios (7 roles)
│   │   ├── location.py               # Ubicaciones (DIVIPOLA)
│   │   ├── formulario_e14.py         # Formularios E-14
│   │   ├── configuracion_electoral.py # Partidos, Candidatos, Tipos
│   │   ├── incidentes_delitos.py     # Incidentes y Delitos
│   │   └── coordinador_municipal.py  # E-24 Municipal
│   │
│   ├── routes/                        # Endpoints de API
│   │   ├── auth.py                   # Autenticación
│   │   ├── super_admin.py            # Super Admin
│   │   ├── coordinador_departamental.py
│   │   ├── coordinador_municipal.py
│   │   ├── coordinador_puesto.py
│   │   ├── testigo.py                # Testigos
│   │   ├── auditor.py                # Auditores
│   │   ├── monitoreo.py              # Monitoreo en tiempo real
│   │   ├── formularios_e14.py        # E-14 y E-24
│   │   ├── incidentes_delitos.py     # Incidentes y Delitos
│   │   ├── verificacion_presencia.py # Geolocalización
│   │   ├── cargar_logos.py           # Logos de partidos
│   │   └── locations.py              # DIVIPOLA
│   │
│   ├── services/                      # Lógica de negocio
│   │   ├── auth_service.py
│   │   ├── formulario_service.py
│   │   ├── e24_service.py            # Generación E-24
│   │   ├── consolidado_service.py    # Consolidación
│   │   ├── municipal_service.py
│   │   ├── incidentes_delitos_service.py
│   │   └── discrepancia_service.py
│   │
│   ├── utils/                         # Utilidades
│   │   ├── decorators.py             # @role_required, @jwt_required
│   │   ├── exceptions.py
│   │   ├── jwt_utils.py
│   │   ├── logging_config.py
│   │   └── cache.py                  # Caché para monitoreo
│   │
│   ├── migrations/                    # Migraciones de BD
│   ├── tests/                         # Tests
│   ├── app.py                         # Factory de aplicación
│   ├── config.py                      # Configuración
│   ├── database.py                    # Configuración de BD
│   └── init_app.py                    # Inicialización
│
├── frontend/                          # Frontend
│   ├── static/                        # Archivos estáticos
│   │   ├── css/
│   │   │   ├── styles.css
│   │   │   ├── dashboard.css
│   │   │   └── monitoreo.css
│   │   ├── js/
│   │   │   ├── api-client.js         # Cliente API
│   │   │   ├── super-admin-dashboard.js
│   │   │   ├── super-admin-init-fix.js  # Fix de dashboard
│   │   │   ├── coordinador-puesto.js
│   │   │   ├── coordinador-municipal.js
│   │   │   ├── testigo-dashboard.js
│   │   │   └── monitoreo-dashboard.js
│   │   └── uploads/                   # Archivos subidos
│   │       └── logos/                 # Logos de partidos
│   │
│   └── templates/                     # Templates HTML
│       ├── base.html                  # Template base
│       ├── index.html
│       ├── auth/
│       │   └── login.html
│       ├── admin/
│       │   └── super-admin-dashboard.html
│       ├── coordinador/
│       │   ├── departamental.html
│       │   ├── municipal.html
│       │   └── puesto.html
│       ├── testigo/
│       │   └── dashboard.html
│       ├── monitoreo/
│       │   └── dashboard.html
│       └── dashboard/
│
├── scripts/                           # Scripts de utilidad
│   ├── init_system.py                # Inicialización completa
│   ├── check_system.py               # Verificación
│   ├── clean_system.py               # Limpieza
│   └── deprecated/                   # Scripts antiguos
│
├── docs/                              # Documentación (10 docs)
│   ├── ARQUITECTURA.md               # Este archivo
│   ├── ROLES_Y_FLUJOS.md             # 7 roles documentados
│   ├── VERIFICACION_FLUJO_COMPLETO.md
│   ├── FLUJO_DATOS_ELECTORALES.md
│   ├── TIPOS_ELECCIONES_COLOMBIA.md
│   ├── GUIA_LOGOS_PARTIDOS.md
│   ├── CHECKLIST_SUPER_ADMIN.md
│   ├── INDICE_DOCUMENTACION.md
│   ├── SEGURIDAD.md
│   └── TROUBLESHOOTING.md
│
├── instance/                          # Base de datos SQLite
│   └── sistema_electoral.db
│
├── logs/                              # Logs de aplicación
├── pdfs/                              # PDFs generados (E-24)
│
├── .env                               # Variables de entorno
├── .env.example                       # Ejemplo
├── .gitignore
├── requirements.txt                   # Dependencias Python
├── requirements-dev.txt               # Dependencias desarrollo
├── run.py                             # Punto de entrada
├── Procfile                           # Para Render
├── render.yaml                        # Configuración Render
└── README.md
```

---

## 🗄️ Arquitectura de Base de Datos

### Tablas Principales

#### 1. Usuarios y Autenticación
```sql
users
├── id (PK)
├── nombre
├── password_hash
├── rol (7 roles)
├── ubicacion_id (FK → locations)
├── activo
├── presencia_verificada
├── ultima_latitud
├── ultima_longitud
├── ultima_geolocalizacion_at
└── ultimo_acceso
```

#### 2. Ubicaciones (DIVIPOLA)
```sql
locations
├── id (PK)
├── departamento_codigo
├── municipio_codigo
├── zona_codigo
├── puesto_codigo
├── mesa_codigo
├── tipo (departamento/municipio/zona/puesto/mesa)
├── nombre_completo
├── total_votantes_registrados
├── latitud
├── longitud
└── parent_id (FK → locations)
```

#### 3. Configuración Electoral
```sql
tipos_eleccion
├── id (PK)
├── codigo
├── nombre
├── es_uninominal
├── permite_lista_cerrada
├── permite_lista_abierta
└── activo

partidos
├── id (PK)
├── codigo
├── nombre
├── nombre_corto
├── color
├── logo_url
├── activo
└── orden

candidatos
├── id (PK)
├── codigo
├── nombre_completo
├── partido_id (FK → partidos)
├── tipo_eleccion_id (FK → tipos_eleccion)
├── numero_lista
├── es_independiente
├── activo
└── orden
```

#### 4. Formularios E-14
```sql
formularios_e14
├── id (PK)
├── mesa_id (FK → locations)
├── testigo_id (FK → users)
├── tipo_eleccion_id (FK → tipos_eleccion)
├── total_votos
├── votos_validos
├── votos_nulos
├── votos_blancos
├── estado (pendiente/validado/rechazado)
├── validado_por_id (FK → users)
└── validado_at

votos_partidos
├── id (PK)
├── formulario_id (FK → formularios_e14)
├── partido_id (FK → partidos)
└── votos

votos_candidatos
├── id (PK)
├── formulario_id (FK → formularios_e14)
├── candidato_id (FK → candidatos)
└── votos
```

#### 5. Formularios E-24 (Consolidados)
```sql
formularios_e24_municipal
├── id (PK)
├── municipio_id (FK → locations)
├── coordinador_id (FK → users)
├── tipo_eleccion_id (FK → tipos_eleccion)
├── total_puestos
├── puestos_incluidos
├── total_votos
├── pdf_url
├── pdf_hash (SHA-256)
└── version

votos_partidos_e24_municipal
├── id (PK)
├── e24_municipal_id (FK → formularios_e24_municipal)
├── partido_id (FK → partidos)
└── votos
```

#### 6. Incidentes y Delitos
```sql
incidentes_electorales
├── id (PK)
├── reportado_por_id (FK → users)
├── mesa_id (FK → locations)
├── tipo_incidente (8 tipos)
├── titulo
├── descripcion
├── severidad (baja/media/alta/critica)
├── estado (reportado/en_revision/resuelto/escalado)
├── evidencia_url
├── ubicacion_gps
└── fecha_incidente

delitos_electorales
├── id (PK)
├── reportado_por_id (FK → users)
├── mesa_id (FK → locations)
├── tipo_delito (9 tipos)
├── titulo
├── descripcion
├── gravedad (leve/media/grave/muy_grave)
├── estado (reportado/en_investigacion/investigado/denunciado)
├── evidencia_url
├── testigos_adicionales
├── ubicacion_gps
├── denunciado_formalmente
└── numero_denuncia
```

---

## 🔄 Flujo de Datos

### 1. Flujo de Autenticación

```
Usuario → POST /api/auth/login
    ↓
Backend valida credenciales
    ↓
Genera JWT token
    ↓
Frontend guarda token
    ↓
Todas las peticiones incluyen: Authorization: Bearer <token>
```

### 2. Flujo de Registro de Votos (E-14)

```
Testigo → Verifica presencia (GPS)
    ↓
Testigo → Crea E-14 para su mesa
    ↓
Registra votos por partido (si aplica)
    ↓
Registra votos por candidato
    ↓
Guarda E-14 (estado: pendiente)
    ↓
Coordinador Puesto → Valida E-14
    ↓
E-14 cambia a estado: validado
    ↓
E-14 validado se incluye en consolidados
```

### 3. Flujo de Consolidación (E-24)

```
E-14 validados del puesto
    ↓
Coordinador Puesto → Genera E-24 Puesto
    ↓
Sistema suma votos automáticamente
    ↓
Genera PDF con hash SHA-256
    ↓
E-24 Puesto disponible
    ↓
Coordinador Municipal → Genera E-24 Municipal
    ↓
Requiere 80% de puestos completos
    ↓
Sistema suma todos los E-14 del municipio
    ↓
Genera PDF E-24 Municipal
    ↓
Coordinador Departamental → Genera E-24 Departamental
    ↓
Sistema suma todos los E-14 del departamento
    ↓
Genera PDF E-24 Departamental
```

### 4. Flujo de Incidentes

```
Testigo/Coordinador → Detecta incidente
    ↓
Reporta en sistema con GPS y evidencia
    ↓
Coordinador → Recibe notificación
    ↓
Revisa y evalúa severidad
    ↓
Resuelve o Escala a nivel superior
    ↓
Sistema registra seguimiento
```

### 5. Flujo de Monitoreo

```
Usuarios registran presencia (GPS)
    ↓
Sistema actualiza ubicaciones cada 30s
    ↓
Monitoreo → Dashboard en tiempo real
    ↓
Mapa con todos los usuarios
    ↓
Estadísticas y alertas automáticas
    ↓
Exportación de reportes
```

---

## 🔐 Seguridad

### Autenticación y Autorización

**JWT (JSON Web Tokens)**:
- Token expira en 24 horas
- Incluye: user_id, rol, ubicacion_id
- Firmado con SECRET_KEY

**Decoradores de Seguridad**:
```python
@jwt_required()  # Requiere token válido
@role_required(['super_admin', 'coordinador_puesto'])  # Requiere rol específico
```

**Validación de Permisos**:
- Cada endpoint valida rol del usuario
- Usuarios solo acceden a datos de su jurisdicción
- Coordinadores solo ven su nivel y niveles inferiores

### Protección de Datos

**Contraseñas**:
- Hasheadas con Werkzeug (PBKDF2)
- Nunca se almacenan en texto plano
- Política de intentos fallidos (5 intentos → bloqueo 1 min)

**Integridad de PDFs**:
- Hash SHA-256 de cada PDF E-24
- Verificación de integridad
- Previene alteración de documentos

**Geolocalización**:
- Solo se almacenan coordenadas
- No se almacena historial completo
- Última ubicación + timestamp

---

## 🚀 Despliegue

### Desarrollo Local

```bash
# 1. Clonar repositorio
git clone <repo>

# 2. Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env

# 5. Inicializar base de datos
python scripts/init_system.py

# 6. Ejecutar aplicación
python run.py
```

### Producción (Render)

**Archivos de configuración**:
- `Procfile`: Define comando de inicio
- `render.yaml`: Configuración de servicios
- `build.sh`: Script de construcción

**Variables de entorno requeridas**:
```
DATABASE_URL=postgresql://...
SECRET_KEY=...
FLASK_ENV=production
```

**Proceso de despliegue**:
1. Push a repositorio Git
2. Render detecta cambios
3. Ejecuta build.sh
4. Inicia aplicación con Procfile
5. Aplicación disponible en URL

---

## 📊 Monitoreo y Logs

### Logs de Aplicación

**Ubicación**: `logs/`

**Niveles**:
- DEBUG: Información detallada
- INFO: Eventos normales
- WARNING: Advertencias
- ERROR: Errores
- CRITICAL: Errores críticos

**Rotación**:
- Máximo 10 MB por archivo
- Mantiene últimos 5 archivos

### Métricas

**Endpoint de Health**:
```
GET /api/health
```

**Respuesta**:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-11-30T22:00:00"
}
```

---

## 🧪 Testing

### Estructura de Tests

```
backend/tests/
├── test_auth.py
├── test_formularios.py
├── test_consolidado.py
├── test_incidentes.py
└── test_api.py
```

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=backend

# Test específico
pytest backend/tests/test_auth.py
```

---

## 📈 Escalabilidad

### Optimizaciones Implementadas

**Caché**:
- Datos de monitoreo cacheados 20-30 segundos
- Reduce carga en BD
- Mejora tiempo de respuesta

**Consultas Optimizadas**:
- Índices en campos frecuentes
- Agregaciones en BD (no en Python)
- Paginación para grandes volúmenes

**Lazy Loading**:
- Carga de datos bajo demanda
- Reduce memoria inicial
- Mejora experiencia de usuario

### Límites Actuales

**SQLite (Desarrollo)**:
- Máximo ~1,000 usuarios concurrentes
- Adecuado para pruebas

**PostgreSQL (Producción)**:
- Soporta 10,000+ usuarios concurrentes
- Escalable horizontalmente
- Recomendado para producción

---

## 🔧 Mantenimiento

### Tareas Periódicas

**Diarias**:
- Backup de base de datos
- Revisión de logs de errores
- Verificación de espacio en disco

**Semanales**:
- Limpieza de logs antiguos
- Verificación de URLs de logos
- Actualización de dependencias

**Mensuales**:
- Auditoría de seguridad
- Optimización de BD
- Revisión de rendimiento

### Scripts de Mantenimiento

```bash
# Verificar sistema
python scripts/check_system.py

# Limpiar datos antiguos
python scripts/clean_system.py

# Backup de BD
python scripts/backup_db.py
```

---

## 📚 Documentación Relacionada

- [ROLES_Y_FLUJOS.md](./ROLES_Y_FLUJOS.md) - Roles y flujos completos
- [VERIFICACION_FLUJO_COMPLETO.md](./VERIFICACION_FLUJO_COMPLETO.md) - Verificación exhaustiva
- [TIPOS_ELECCIONES_COLOMBIA.md](./TIPOS_ELECCIONES_COLOMBIA.md) - Tipos de elecciones
- [GUIA_LOGOS_PARTIDOS.md](./GUIA_LOGOS_PARTIDOS.md) - Gestión de logos
- [CHECKLIST_SUPER_ADMIN.md](./CHECKLIST_SUPER_ADMIN.md) - Lista de verificación
- [SEGURIDAD.md](./SEGURIDAD.md) - Seguridad del sistema
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) - Solución de problemas

---

**Última actualización**: 30 de Noviembre de 2025  
**Versión**: 2.0  
**Estado**: ✅ Completo y Verificado
