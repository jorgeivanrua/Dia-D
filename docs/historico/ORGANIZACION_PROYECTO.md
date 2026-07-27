# 📁 Organización del Proyecto - Sistema de Testigos Electorales

## 🎯 Estructura Limpia y Organizada

```
Sistema de Testigos Electorales/
│
├── 📂 backend/                      # Lógica del servidor
│   ├── app.py                       # Aplicación Flask principal
│   ├── database.py                  # Configuración de base de datos
│   │
│   ├── 📂 models/                   # Modelos de datos (ORM)
│   │   ├── user.py                  # Usuarios y autenticación
│   │   ├── location.py              # Ubicaciones (DIVIPOLA)
│   │   ├── formulario_e14.py        # Formularios E-14
│   │   └── configuracion_electoral.py # Partidos, candidatos, etc.
│   │
│   ├── 📂 routes/                   # Endpoints de API
│   │   ├── auth.py                  # Autenticación (login/logout)
│   │   ├── testigo.py               # Rutas de testigo
│   │   ├── coordinador_*.py         # Rutas de coordinadores
│   │   ├── super_admin.py           # Rutas de super admin
│   │   ├── auditor.py               # Rutas de auditor
│   │   ├── formularios_e14.py       # Gestión de formularios
│   │   └── locations_geo.py         # Geolocalización
│   │
│   ├── 📂 migrations/               # Migraciones de BD
│   │   └── apply_user_geolocation.py
│   │
│   └── 📂 utils/                    # Utilidades
│       └── decorators.py            # Decoradores de seguridad
│
├── 📂 frontend/                     # Interfaz de usuario
│   ├── 📂 templates/                # Templates HTML (Jinja2)
│   │   ├── base.html                # Template base
│   │   ├── auth/login.html          # Página de login
│   │   ├── testigo/dashboard.html   # Dashboard de testigo
│   │   ├── coordinador/*.html       # Dashboards de coordinadores
│   │   └── admin/*.html             # Dashboards de admin
│   │
│   └── 📂 static/                   # Archivos estáticos
│       ├── 📂 js/                   # JavaScript
│       │   ├── utils.js             # Utilidades comunes
│       │   ├── api-client.js        # Cliente API
│       │   ├── session-manager.js   # Gestión de sesión
│       │   ├── testigo-dashboard-v2.js
│       │   ├── testigo-dashboard-final-fix.js ✨ NUEVO
│       │   └── [otros dashboards].js
│       │
│       ├── 📂 css/                  # Estilos CSS
│       │   └── *.css
│       │
│       └── 📂 images/               # Imágenes
│
├── 📂 scripts/                      # Scripts de utilidad ✨ ORGANIZADO
│   ├── init_db.py                   # Inicializar BD
│   ├── load_divipola.py             # Cargar ubicaciones
│   ├── create_fixed_users.py        # Crear usuarios
│   ├── init_configuracion_electoral.py
│   ├── create_formularios_e14_tables.py
│   ├── verificacion_completa_sistema.py ✨ MOVIDO
│   ├── diagnostico_inicializacion.py ✨ MOVIDO
│   ├── diagnostico_sistema.py ✨ MOVIDO
│   ├── test_testigo_fix.py ✨ MOVIDO
│   ├── test_all_roles.py ✨ MOVIDO
│   ├── apply_migration_now.py ✨ MOVIDO
│   ├── verificar_roles_jwt.py ✨ MOVIDO
│   ├── actualizar_passwords_*.py ✨ MOVIDO
│   ├── reset_passwords_*.py ✨ MOVIDO
│   ├── upload_db_to_render.py ✨ MOVIDO
│   └── verificar_passwords.py ✨ MOVIDO
│
├── 📂 instance/                     # Base de datos
│   └── testigos.db                  # SQLite database
│
├── 📂 uploads/                      # Archivos subidos
│   └── [imágenes de formularios]
│
├── 📂 md_funciones/                 # Documentación
│   └── [documentos .md]
│
├── 📄 setup.py                      # Inicialización completa
├── 📄 setup.bat / setup.sh          # Wrappers de setup
├── 📄 start.bat / start.sh          # Scripts de inicio
├── 📄 run.py                        # Servidor de desarrollo
├── 📄 render_setup.py               # Setup para Render
├── 📄 render.yaml                   # Configuración de Render
├── 📄 requirements.txt              # Dependencias Python
├── 📄 README.md                     # Documentación principal
└── 📄 .env                          # Variables de entorno (local)
```

## 📋 Archivos Movidos a `scripts/`

### Scripts de Verificación:
- ✅ `verificacion_completa_sistema.py` - Verificación exhaustiva
- ✅ `diagnostico_inicializacion.py` - Diagnóstico de inicialización
- ✅ `diagnostico_sistema.py` - Diagnóstico general
- ✅ `test_testigo_fix.py` - Test de correcciones del testigo
- ✅ `test_all_roles.py` - Test de todos los roles

### Scripts de Migraciones:
- ✅ `apply_migration_now.py` - Aplicar migraciones

### Scripts de Usuarios:
- ✅ `verificar_roles_jwt.py` - Verificar roles en JWT
- ✅ `actualizar_passwords_render.py` - Actualizar passwords en Render
- ✅ `actualizar_passwords_texto_plano.py` - Actualizar passwords
- ✅ `reset_passwords_render_simple.py` - Reset passwords en Render
- ✅ `reset_passwords_via_api.py` - Reset passwords vía API
- ✅ `verificar_passwords.py` - Verificar passwords

### Scripts de Utilidad:
- ✅ `upload_db_to_render.py` - Subir BD a Render

## 🎯 Archivos en Raíz (Propósito Claro)

### Scripts de Inicio:
- `setup.py` - Inicialización completa del sistema
- `setup.bat` / `setup.sh` - Wrappers para crear entorno e inicializar
- `start.bat` / `start.sh` - Inicio rápido del servidor
- `run.py` - Servidor de desarrollo Flask

### Configuración:
- `render_setup.py` - Inicialización específica para Render
- `render.yaml` - Configuración de Render
- `requirements.txt` - Dependencias Python
- `.env` - Variables de entorno (local)
- `.gitignore` - Archivos ignorados por Git

### Documentación:
- `README.md` - Documentación principal
- Otros `.md` en `md_funciones/`

### Utilidades:
- `check_system.bat` - Verificación rápida (Windows)
- `Procfile` - Para Heroku
- `runtime.txt` - Versión de Python
- `Makefile` - Comandos make

## 📝 Cómo Usar los Scripts

### Scripts de Inicialización:
```bash
python setup.py                                    # Inicialización completa
python scripts/init_db.py                          # Solo crear BD
python scripts/load_divipola.py                    # Solo cargar ubicaciones
python scripts/create_fixed_users.py               # Solo crear usuarios
```

### Scripts de Verificación:
```bash
python scripts/verificacion_completa_sistema.py    # Verificación exhaustiva
python scripts/diagnostico_inicializacion.py       # Diagnóstico de setup
python scripts/diagnostico_sistema.py              # Diagnóstico general
python scripts/test_all_roles.py                   # Test de todos los roles
```

### Scripts de Mantenimiento:
```bash
python scripts/verificar_passwords.py              # Verificar passwords
python scripts/verificar_roles_jwt.py              # Verificar roles
python scripts/apply_migration_now.py              # Aplicar migraciones
```

## ✅ Beneficios de la Organización

1. **Claridad:** Fácil encontrar scripts por categoría
2. **Mantenibilidad:** Código organizado es más fácil de mantener
3. **Escalabilidad:** Fácil agregar nuevos scripts
4. **Profesionalismo:** Estructura clara y profesional
5. **Documentación:** Cada carpeta tiene un propósito claro

## 🔄 Próximos Pasos

1. ✅ Scripts organizados en `scripts/`
2. ✅ Documentación actualizada
3. ⏳ Commit de cambios
4. ⏳ Push a GitHub
5. ⏳ Deploy en Render

---

**Fecha:** Noviembre 23, 2025
**Estado:** ✅ Proyecto Organizado
