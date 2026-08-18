# 🗳️ Sistema de Testigos Electorales - MVP

Sistema web para la gestión y registro de formularios E-14 (Actas de Escrutinio) por parte de testigos electorales en Colombia.

## 🚀 Características Principales

### ✅ Sistema Completo de Configuración Electoral
- Gestión de tipos de elección (Senado, Cámara, Concejo, etc.)
- Administración de partidos políticos con colores y logos
- Registro de candidatos por tipo de elección
- Gestión de coaliciones políticas

### ✅ Formularios E-14 Dinámicos
- Registro de actas de escrutinio con datos en tiempo real
- Carga dinámica de partidos y candidatos según tipo de elección
- Cálculos automáticos de totales y validaciones
- Sistema de estados (pendiente, validado, rechazado)
- Validación por coordinadores y administradores

### ✅ Dashboards por Rol
- **Admin**: Configuración electoral completa
- **Coordinador**: Validación de formularios (en desarrollo)
- **Testigo**: Registro de formularios E-14

### ✅ Seguridad
- Autenticación JWT
- Permisos por rol
- Validación de datos en backend y frontend

## 📋 Requisitos

- Python 3.8+
- SQLite (incluido)
- Navegador web moderno

## 🔧 Instalación y Configuración

### Opción Docker (rápida) 🐳

Si quieres levantar la app con PostgreSQL y MinIO en contenedores:

```bash
docker compose up --build -d
```

Después de unos segundos, la aplicación estará disponible en:
- http://localhost:5000
- MinIO Console: http://localhost:9001

Para ver los logs:
```bash
docker compose logs -f app
```

Para detenerlos:
```bash
docker compose down
```

### Opción 1: Instalación Automática (Recomendada) ⚡

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

Este script automáticamente:
- ✅ Crea el entorno virtual
- ✅ Instala todas las dependencias
- ✅ Crea archivo .env desde .env.example
- ✅ Inicializa la base de datos
- ✅ **Carga automáticamente todos los datos:**
  - 📍 DIVIPOLA (22 departamentos, 1122 municipios, 13405 puestos)
  - 🎨 Partidos políticos (9 partidos con colores)
  - 👤 Candidatos (7 candidatos de ejemplo)
  - 🗳️ Tipos de elección (6 tipos)
  - 👥 Usuarios del sistema (6 usuarios con contraseñas hasheadas)
- ✅ Configura el sistema electoral

### Verificar Sistema

Antes de iniciar, verifica que todo esté correcto:

```bash
python scripts/check_system.py
```

Este script verifica:
- ✅ Versión de Python
- ✅ Dependencias instaladas
- ✅ Base de datos existe y tiene datos
- ✅ Contraseñas hasheadas correctamente
- ✅ Puerto 5000 disponible

### Opción 2: Instalación Manual 🔧

#### 1. Clonar el repositorio
```bash
git clone https://github.com/jorgeivanrua/testigos.git
cd testigos/mvp
```

#### 2. Crear y activar entorno virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 4. Inicializar el sistema
```bash
python setup.py
```

## 🚀 Ejecutar la Aplicación

### Desarrollo Local

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**O directamente con Python:**
```bash
python run.py
```

La aplicación estará disponible en: `http://localhost:5000`

### Despliegue en Render.com 🌐

1. **Conectar repositorio a Render**
   - Ve a [render.com](https://render.com)
   - Crea una nueva Web Service
   - Conecta tu repositorio de GitHub

2. **Configuración automática**
   - Render detectará automáticamente el archivo `render.yaml`
   - La inicialización se ejecutará automáticamente con `render_setup.py`

3. **Variables de entorno** (opcional)
   - `SECRET_KEY`: Se genera automáticamente
   - `JWT_SECRET_KEY`: Se genera automáticamente
   - `DATABASE_URL`: Para usar PostgreSQL (recomendado en producción)

4. **Archivo DIVIPOLA**
   - Coloca el archivo `divipola.csv` en la carpeta `todos los datos/`
   - O súbelo manualmente después del despliegue

## 👥 Usuarios del Sistema

### 🎉 Inicialización Automática de Datos

El sistema ahora carga automáticamente todos los datos necesarios en cada instalación o deploy:

```bash
# Inicialización completa del sistema (RECOMENDADO)
python scripts/init_system.py

# Con reseteo de contraseñas
python scripts/init_system.py --reset-passwords
```

### Usuarios Creados Automáticamente

| Usuario | Contraseña | Rol | Descripción |
|---------|-----------|-----|-------------|
| **Super Admin** | **admin123** | super_admin | Administrador principal |
| Monitoreo | test123 | monitoreo | Dashboard de monitoreo en tiempo real |
| Coordinador Departamental | test123 | coordinador_departamental | Coordinación departamental |
| Coordinador Municipal | test123 | coordinador_municipal | Coordinación municipal |
| Coordinador Puesto | test123 | coordinador_puesto | Coordinación de puesto |
| Auditor Electoral | test123 | auditor_electoral | Auditoría del sistema |

### Datos Cargados Automáticamente

- ✅ **DIVIPOLA**: 22 departamentos, 1122 municipios, 13405 puestos
- ✅ **Partidos Políticos**: 9 partidos (Pacto Histórico, Liberal, Conservador, Verde, Centro Democrático, Cambio Radical, La U, MIRA, Otros)
- ✅ **Candidatos**: 7 candidatos de ejemplo (Gustavo Bolívar, María José Pizarro, Iván Cepeda, Juan Fernando Cristo, Efraín Cepeda, Angélica Lozano, María Fernanda Cabal)
- ✅ **Tipos de Elección**: 6 tipos (Senado, Cámara, Gobernación, Asamblea, Alcaldía, Concejo)

### 🔒 Seguridad

⚠️ **CRÍTICO**: 
- Las contraseñas ahora se almacenan con **hashing seguro** (Werkzeug)
- **DEBES cambiar todas las contraseñas** después del primer acceso en producción
- Ver `docs/SEGURIDAD.md` para más información

⚠️ **IMPORTANTE**: Si actualizas desde una versión anterior, lee `CAMBIOS_SEGURIDAD_2024.md`

## 📁 Estructura del Proyecto

```
mvp/
├── backend/
│   ├── models/          # Modelos de datos
│   ├── routes/          # Endpoints API
│   ├── services/        # Lógica de negocio
│   └── utils/           # Utilidades
├── frontend/
│   ├── static/
│   │   ├── css/        # Estilos
│   │   └── js/         # JavaScript
│   └── templates/       # HTML templates
├── scripts/             # Scripts de inicialización
├── instance/            # Base de datos SQLite
└── requirements.txt     # Dependencias Python
```

## 🔑 Funcionalidades por Rol

### Administrador
- ✅ Gestión completa de configuración electoral
- ✅ Crear/editar tipos de elección
- ✅ Crear/editar partidos políticos
- ✅ Crear/editar candidatos
- ✅ Gestionar coaliciones
- ✅ Eliminar formularios

### Coordinador
- ✅ Validar formularios E-14
- ✅ Rechazar formularios con observaciones
- 🔄 Dashboard de validación (en desarrollo)

### Testigo Electoral
- ✅ Registrar formularios E-14
- ✅ Ver sus propios formularios
- ✅ Editar formularios pendientes
- ✅ Carga dinámica de configuración electoral

## 📊 API Endpoints

> La API tiene **254 endpoints** en **33 blueprints**. La documentación interactiva completa se genera automáticamente con **Swagger/OpenAPI 3**.

### 🧪 Documentación Interactiva
- **Swagger UI**: `GET /api/docs/` — Explora y prueba todos los endpoints
- **Spec JSON**: `GET /apispec.json` — Spec OpenAPI 3 en formato JSON

### Autenticación
- `POST /api/auth/login` - Iniciar sesión (retorna `access_token` y `refresh_token`)
- `POST /api/auth/logout` - Cerrar sesión
- `GET /api/auth/profile` - Obtener perfil del usuario autenticado

### Ubicaciones (DIVIPOLA)
- `GET /api/locations/departamentos` - Listar departamentos
- `GET /api/locations/municipios/{departamento_codigo}` - Listar municipios
- `GET /api/locations/zonas/{municipio_codigo}` - Listar zonas
- `GET /api/locations/puestos/{zona_codigo}` - Listar puestos
- `GET /api/locations/mesas/{puesto_codigo}` - Listar mesas

### Formularios E-14
- `GET /api/formularios/mis-formularios` - Listar mis formularios (testigo)
- `GET /api/formularios/puesto` - Listar formularios del puesto (coordinador)
- `POST /api/formularios` - Crear formulario E-14
- `GET /api/formularios/{id}` - Ver formulario
- `PUT /api/formularios/{id}` - Actualizar formulario
- `PUT /api/formularios/{id}/validar` - Validar formulario
- `PUT /api/formularios/{id}/rechazar` - Rechazar formulario
- `POST /api/formularios/puesto/generar-e24` - Generar E-24 de puesto
- `POST /api/formularios/municipal/generar-e24` - Generar E-24 municipal

### Incidentes y Delitos
- `POST /api/incidentes` - Reportar incidente
- `GET /api/incidentes` - Listar incidentes
- `PUT /api/incidentes/{id}/estado` - Cambiar estado de incidente
- `POST /api/delitos` - Reportar delito
- `GET /api/delitos` - Listar delitos
- `PUT /api/delitos/{id}/estado` - Cambiar estado de delito
- `POST /api/delitos/{id}/denunciar` - Denunciar formalmente un delito
- `GET /api/reportes/estadisticas` - Estadísticas de reportes

### Seguimiento
- `GET /api/seguimiento/{tipo}/{reporte_id}` - Obtener seguimiento de un reporte
- `POST /api/seguimiento` - Registrar seguimiento

### Notificaciones
- `GET /api/notificaciones` - Listar notificaciones
- `POST /api/notificaciones/{id}/leer` - Marcar como leída
- `POST /api/notificaciones/marcar-todas-leidas` - Marcar todas como leídas
- `GET /api/notificaciones/contador` - Contador de no leídas

### Monitoreo (Super Admin)
- `GET /api/monitoreo/usuarios-activos` - Usuarios activos
- `GET /api/monitoreo/estadisticas` - Estadísticas generales
- `GET /api/monitoreo/alertas` - Alertas del sistema
- `GET /api/monitoreo/actividad-reciente` - Actividad reciente
- `GET /api/monitoreo/metricas-rendimiento` - Métricas de rendimiento
- `GET /api/monitoreo/mapa-calor` - Mapa de calor
- `GET /api/monitoreo/exportar-reporte` - Exportar reporte

### Gestión de Usuarios
- `GET /api/gestion-usuarios/puestos` - Listar puestos
- `GET /api/gestion-usuarios/municipios` - Listar municipios
- `GET /api/gestion-usuarios/departamentos` - Listar departamentos
- `POST /api/gestion-usuarios/crear-testigos-puesto` - Crear testigos de un puesto
- `POST /api/gestion-usuarios/crear-coordinador-puesto` - Crear coordinador de puesto
- `POST /api/gestion-usuarios/crear-usuarios-municipio` - Crear usuarios de municipio
- `POST /api/gestion-usuarios/crear-usuarios-departamento` - Crear usuarios de departamento

### Otros
- `GET /api/evidencia/{filename}` - Obtener evidencia
- `POST /api/evidencia/upload` - Subir evidencia
- `GET /api/partidos` - Listar partidos
- `GET /api/candidatos` - Listar candidatos
- `GET /api/database/exportar` - Backup completo de BD (JSON)
- `GET /health` - Health check

## 📖 Documentación

### Guías de Inicio
- **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - ⚡ Empieza en 2 minutos
- **[GUIA_DESPLIEGUE.md](GUIA_DESPLIEGUE.md)** - 🚀 Despliegue completo (Local, Render, Heroku, VPS)
- **[GUIA_PRUEBAS_MANUALES.md](GUIA_PRUEBAS_MANUALES.md)** - 🧪 Cómo probar el sistema

### Documentación Técnica
- [FORMULARIOS_E14_IMPLEMENTADOS.md](FORMULARIOS_E14_IMPLEMENTADOS.md) - Sistema de formularios
- [DASHBOARDS_IMPLEMENTADOS.md](DASHBOARDS_IMPLEMENTADOS.md) - Dashboards por rol
- [ESTADO_FINAL_SISTEMA.md](ESTADO_FINAL_SISTEMA.md) - Estado actual del proyecto

## 🛠️ Tecnologías Utilizadas

### Backend
- Flask 3.0.0
- Flask-SQLAlchemy
- Flask-JWT-Extended
- SQLite

### Frontend
- Bootstrap 5.3
- JavaScript ES6+
- Bootstrap Icons

## 🔄 Estado del Proyecto

### ✅ Completado (v1.0.0 - Nov 22, 2025)
- ✅ Sistema de autenticación JWT
- ✅ Gestión de usuarios por rol
- ✅ Configuración electoral dinámica
- ✅ Formularios E-14 completos con todas las funcionalidades
- ✅ API REST completa
- ✅ Dashboards funcionales para todos los roles
- ✅ Verificación de presencia con geolocalización
- ✅ Sistema de sincronización offline
- ✅ Carga de imágenes de formularios
- ✅ Validación de formularios por coordinadores
- ✅ Reportes y estadísticas por rol
- ✅ Sistema de inicialización automatizado
- ✅ Scripts de despliegue para Render
- ✅ Documentación completa
- ✅ Correcciones de errores aplicadas

### 🎯 Estado Actual
**LISTO PARA PRODUCCIÓN** ✅

El sistema está completamente funcional y listo para:
- ✓ Desarrollo local
- ✓ Despliegue en Render
- ✓ Uso en producción

### 📋 Próximas Versiones
- v1.1: Formularios E-24, notificaciones, exportación
- v1.2: Modo completamente offline, PWA
- v2.0: App móvil nativa, ML para detección de anomalías

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📚 Documentación

### Sistema de Monitoreo
Para documentación completa del sistema de monitoreo electoral:
- **[README_MONITOREO.md](README_MONITOREO.md)** - Índice principal del sistema de monitoreo
- **[docs/INICIO_RAPIDO_MONITOREO.md](docs/INICIO_RAPIDO_MONITOREO.md)** - Guía de inicio rápido
- **[docs/GUIA_COMPLETA_MONITOREO.md](docs/GUIA_COMPLETA_MONITOREO.md)** - Guía completa

### Documentación Técnica
- **[docs/ESTRUCTURA_PROYECTO_MONITOREO.md](docs/ESTRUCTURA_PROYECTO_MONITOREO.md)** - Estructura del proyecto
- **[docs/VERIFICACION_MONITOREO_BD.md](docs/VERIFICACION_MONITOREO_BD.md)** - Verificación de BD
- **[docs/optimizaciones/](docs/optimizaciones/)** - Optimizaciones implementadas

### Documentación Histórica
- **[docs/historico/](docs/historico/)** - Correcciones y mejoras históricas
- **[docs/features/](docs/features/)** - Documentación de features específicas

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 👨‍💻 Autor

Jorge Iván Rúa

## 📧 Contacto

Para preguntas o soporte, contactar a través de GitHub Issues.

---

**Nota**: Este es un MVP (Producto Mínimo Viable) en desarrollo activo. Algunas funcionalidades están en proceso de implementación.
