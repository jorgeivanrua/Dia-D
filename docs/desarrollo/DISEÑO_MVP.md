# Diseño Técnico - MVP

## 1. Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (Browser)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Dashboard  │  │   Forms E14  │  │    Admin     │      │
│  │   Testigo    │  │   Capture    │  │    Panel     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │ HTTP/JSON
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Flask API)                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    API Routes                         │   │
│  │  /auth  /e14  /coordination  /admin  /locations     │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  Services Layer                       │   │
│  │  AuthService  E14Service  ValidationService          │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   Models (ORM)                        │   │
│  │  User  Location  FormE14  FormE14History            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   DATABASE (SQLite/PostgreSQL)               │
│  users  locations  forms_e14  forms_e14_history             │
└─────────────────────────────────────────────────────────────┘
```

## 2. Modelo de Datos

### 2.1 Diagrama ER Simplificado

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│    User      │         │   Location   │         │   FormE14    │
├──────────────┤         ├──────────────┤         ├──────────────┤
│ id (PK)      │────┐    │ id (PK)      │    ┌────│ id (PK)      │
│ nombre       │    │    │ depto_codigo │    │    │ mesa_id (FK) │
│ email (UQ)   │    └───▶│ ubicacion_id │◀───┘    │ testigo_id   │
│ password_hash│         │ tipo         │         │ total_votos  │
│ rol          │         │ nombre       │         │ estado       │
│ ubicacion_id │         │ votantes     │         │ foto_url     │
│ activo       │         └──────────────┘         │ created_at   │
└──────────────┘                                  └──────────────┘
                                                         │
                                                         │
                                                         ▼
                                                  ┌──────────────┐
                                                  │ FormE14      │
                                                  │ History      │
                                                  ├──────────────┤
                                                  │ id (PK)      │
                                                  │ form_id (FK) │
                                                  │ usuario_id   │
                                                  │ accion       │
                                                  │ estado_ant   │
                                                  │ estado_nuevo │
                                                  │ justificacion│
                                                  │ timestamp    │
                                                  └──────────────┘
```

### 2.2 Esquemas de Tablas

#### users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    ubicacion_id INTEGER,
    activo BOOLEAN DEFAULT TRUE,
    ultimo_acceso DATETIME,
    intentos_fallidos INTEGER DEFAULT 0,
    bloqueado_hasta DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ubicacion_id) REFERENCES locations(id)
);
```

#### locations
```sql
CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    departamento_codigo VARCHAR(10) NOT NULL,
    municipio_codigo VARCHAR(10),
    puesto_codigo VARCHAR(10),
    mesa_codigo VARCHAR(10),
    nombre_completo VARCHAR(200) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    total_votantes_registrados INTEGER DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    latitud FLOAT,
    longitud FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### forms_e14
```sql
CREATE TABLE forms_e14 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mesa_id INTEGER NOT NULL,
    testigo_id INTEGER NOT NULL,
    total_votos INTEGER NOT NULL,
    votos_partido_1 INTEGER DEFAULT 0,
    votos_partido_2 INTEGER DEFAULT 0,
    votos_partido_3 INTEGER DEFAULT 0,
    votos_nulos INTEGER DEFAULT 0,
    votos_no_marcados INTEGER DEFAULT 0,
    foto_url VARCHAR(500),
    estado VARCHAR(50) NOT NULL DEFAULT 'borrador',
    observaciones TEXT,
    aprobado_por INTEGER,
    aprobado_en DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mesa_id) REFERENCES locations(id),
    FOREIGN KEY (testigo_id) REFERENCES users(id),
    FOREIGN KEY (aprobado_por) REFERENCES users(id)
);
```

#### forms_e14_history
```sql
CREATE TABLE forms_e14_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    form_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    accion VARCHAR(50) NOT NULL,
    estado_anterior VARCHAR(50),
    estado_nuevo VARCHAR(50),
    justificacion TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (form_id) REFERENCES forms_e14(id),
    FOREIGN KEY (usuario_id) REFERENCES users(id)
);
```

## 3. API Endpoints

### 3.1 Autenticación

```
POST   /api/auth/login
Body:  { "email": "user@example.com", "password": "pass123" }
Response: { "access_token": "...", "refresh_token": "...", "user": {...} }

POST   /api/auth/logout
Headers: Authorization: Bearer <token>
Response: { "message": "Sesión cerrada" }

GET    /api/auth/profile
Headers: Authorization: Bearer <token>
Response: { "user": {...}, "accessible_locations": [...] }

POST   /api/auth/change-password
Headers: Authorization: Bearer <token>
Body:  { "current_password": "old", "new_password": "new" }
Response: { "message": "Contraseña actualizada" }
```

### 3.2 Usuarios (Admin)

```
GET    /api/auth/users?page=1&per_page=20&rol=testigo
Headers: Authorization: Bearer <admin_token>
Response: { "data": [...], "total": 50, "page": 1, "per_page": 20 }

POST   /api/auth/users
Headers: Authorization: Bearer <admin_token>
Body:  { "nombre": "Juan", "email": "juan@test.com", "rol": "testigo", "ubicacion_id": 5 }
Response: { "user": {...}, "temporary_password": "Temp123!" }

PUT    /api/auth/users/:id
Headers: Authorization: Bearer <admin_token>
Body:  { "nombre": "Juan Pérez", "activo": true }
Response: { "user": {...} }

POST   /api/auth/users/:id/deactivate
Headers: Authorization: Bearer <admin_token>
Body:  { "justificacion": "Usuario duplicado" }
Response: { "message": "Usuario desactivado" }
```

### 3.3 Ubicaciones

```
GET    /api/auth/locations?tipo=mesa&departamento=05
Headers: Authorization: Bearer <token>
Response: { "data": [...] }

GET    /api/locations/departamentos
Response: { "data": [...] }

GET    /api/locations/municipios?departamento=05
Response: { "data": [...] }

GET    /api/locations/puestos?departamento=05&municipio=001
Response: { "data": [...] }

GET    /api/locations/mesas?departamento=05&municipio=001&puesto=001
Response: { "data": [...] }
```

### 3.4 Formularios E-14

```
GET    /api/e14/forms?estado=enviado&page=1
Headers: Authorization: Bearer <token>
Response: { "data": [...], "total": 10, "page": 1 }

POST   /api/e14/forms
Headers: Authorization: Bearer <token>
Body:  { "mesa_id": 5, "total_votos": 100, "votos_partido_1": 50, ... }
Response: { "form": {...} }

GET    /api/e14/forms/:id
Headers: Authorization: Bearer <token>
Response: { "form": {...}, "history": [...] }

PUT    /api/e14/forms/:id
Headers: Authorization: Bearer <token>
Body:  { "total_votos": 105, "observaciones": "Corrección" }
Response: { "form": {...} }

POST   /api/e14/forms/:id/submit
Headers: Authorization: Bearer <token>
Response: { "form": {...}, "message": "Formulario enviado" }

POST   /api/e14/forms/:id/approve
Headers: Authorization: Bearer <coord_token>
Body:  { "observaciones": "Datos correctos" }
Response: { "form": {...} }

POST   /api/e14/forms/:id/reject
Headers: Authorization: Bearer <coord_token>
Body:  { "justificacion": "Suma de votos incorrecta" }
Response: { "form": {...} }

POST   /api/e14/forms/:id/upload-photo
Headers: Authorization: Bearer <token>
Body:  FormData with file
Response: { "foto_url": "/uploads/e14/..." }
```

### 3.5 Dashboards

```
GET    /api/coordination/dashboard
Headers: Authorization: Bearer <coord_token>
Response: {
  "pendientes": 5,
  "aprobados_hoy": 10,
  "rechazados_hoy": 2,
  "forms_pendientes": [...]
}

GET    /api/admin/stats
Headers: Authorization: Bearer <admin_token>
Response: {
  "total_usuarios": 50,
  "total_formularios": 100,
  "formularios_por_estado": {...},
  "actividad_reciente": [...]
}
```

## 4. Flujos de Datos

### 4.1 Flujo de Autenticación

```
1. Usuario → POST /api/auth/login
2. AuthService.authenticate_user()
3. User.authenticate(email, password)
4. Verificar password_hash con bcrypt
5. Generar JWT tokens
6. Actualizar ultimo_acceso
7. Retornar tokens + user data
```

### 4.2 Flujo de Captura E-14

```
1. Testigo → POST /api/e14/forms
2. Verificar permisos (token_required)
3. Validar que mesa pertenece al testigo
4. E14Service.create_form(data, testigo_id)
5. Validar datos (ValidationService)
   - Total votos ≤ Votantes registrados
   - Suma de votos = Total votos
6. Crear FormE14 con estado='borrador'
7. Crear entrada en FormE14History
8. Retornar formulario creado
```

### 4.3 Flujo de Aprobación E-14

```
1. Coordinador → POST /api/e14/forms/:id/approve
2. Verificar permisos (role_required: coordinador)
3. Verificar que form pertenece a su puesto
4. E14Service.approve_form(form_id, coord_id, observaciones)
5. Actualizar estado='aprobado'
6. Registrar aprobado_por y aprobado_en
7. Crear entrada en FormE14History
8. Retornar formulario actualizado
```

## 5. Seguridad

### 5.1 Autenticación JWT

```python
# Configuración JWT
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
```

### 5.2 Control de Acceso

```python
# Decoradores de autorización
@token_required  # Requiere token válido
@admin_required  # Requiere rol admin/sistemas
@role_required(UserRole.COORDINADOR_PUESTO)  # Requiere rol específico
```

### 5.3 Validación de Entrada

```python
# Sanitización de datos
DataSanitizer.sanitize_user_data(data)
DataSanitizer.sanitize_form_data(data)

# Validación de negocio
ElectoralValidators.validate_e14_data(form_data)
ElectoralValidators.validate_email(email)
ElectoralValidators.validate_password_strength(password)
```

## 6. Manejo de Errores

### 6.1 Códigos de Estado HTTP

```
200 OK - Operación exitosa
201 Created - Recurso creado
400 Bad Request - Datos inválidos
401 Unauthorized - No autenticado
403 Forbidden - Sin permisos
404 Not Found - Recurso no encontrado
500 Internal Server Error - Error del servidor
```

### 6.2 Formato de Respuestas

```json
// Éxito
{
  "success": true,
  "data": {...},
  "message": "Operación exitosa"
}

// Error
{
  "success": false,
  "error": "Mensaje de error",
  "errors": {
    "campo": ["Error específico"]
  }
}

// Paginación
{
  "success": true,
  "data": [...],
  "page": 1,
  "per_page": 20,
  "total": 100
}
```

## 7. Frontend

### 7.1 Estructura de Páginas

```
/                          → Landing page / Redirect to login
/login                     → Página de login
/dashboard/testigo         → Dashboard testigo
/dashboard/coordinador     → Dashboard coordinador
/dashboard/admin           → Dashboard admin
/e14/new                   → Crear E-14
/e14/:id                   → Ver/Editar E-14
/admin/users               → Gestión de usuarios
```

### 7.2 Componentes Reutilizables

```javascript
// components/FormE14.js
- Formulario de captura E-14
- Validación en tiempo real
- Upload de foto

// components/FormE14Card.js
- Tarjeta de resumen de E-14
- Acciones rápidas (aprobar/rechazar)

// components/UserForm.js
- Formulario de usuario
- Selector de rol y ubicación

// components/LocationSelector.js
- Selector jerárquico de ubicaciones
- Departamento → Municipio → Puesto → Mesa
```

### 7.3 Estado Global (localStorage)

```javascript
// Almacenar tokens
localStorage.setItem('access_token', token);
localStorage.setItem('refresh_token', refresh_token);
localStorage.setItem('user', JSON.stringify(user));

// Interceptor para agregar token a requests
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

## 8. Despliegue

### 8.1 Desarrollo

```bash
# Variables de entorno
FLASK_ENV=development
SECRET_KEY=dev-secret-key
JWT_SECRET_KEY=dev-jwt-secret
DATABASE_URL=sqlite:///electoral.db

# Ejecutar
python run.py
```

### 8.2 Producción

```bash
# Variables de entorno
FLASK_ENV=production
SECRET_KEY=<strong-secret-key>
JWT_SECRET_KEY=<strong-jwt-secret>
DATABASE_URL=postgresql://user:pass@host:5432/electoral

# Ejecutar con Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

## 9. Testing

### 9.1 Tests Unitarios

```python
# tests/test_auth.py
def test_login_success()
def test_login_invalid_credentials()
def test_token_generation()

# tests/test_e14.py
def test_create_e14_valid()
def test_create_e14_invalid_sum()
def test_approve_e14()
def test_reject_e14()
```

### 9.2 Tests de Integración

```python
# tests/test_integration.py
def test_full_e14_workflow()
def test_user_creation_and_login()
def test_location_hierarchy()
```

## 10. Monitoreo

### 10.1 Logs

```python
# Configuración de logging
logging.basicConfig(
    filename='logs/sistema_electoral.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Eventos a registrar
- Login exitoso/fallido
- Creación de formularios
- Aprobación/Rechazo de formularios
- Errores de validación
- Errores del servidor
```

### 10.2 Métricas

```python
# Métricas a monitorear
- Usuarios activos
- Formularios creados por hora
- Tiempo promedio de aprobación
- Tasa de rechazo
- Errores por endpoint
```
