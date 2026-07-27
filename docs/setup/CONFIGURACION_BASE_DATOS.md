# Configuración de Base de Datos

## Fecha: 2025-12-07

## Ubicación de la Base de Datos

### Base de Datos Activa
```
instance/electoral.db
```

Esta es la **única** base de datos que usa la aplicación.

## Configuración

### Backend Config (`backend/config.py`)
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/electoral.db'
```

La ruta es relativa a la raíz del proyecto, por lo que apunta a:
```
mvp/instance/electoral.db
```

## Problema Resuelto

### Antes
Había **3 bases de datos** en el proyecto:
1. `electoral.db` (raíz) - 0 bytes, vacía
2. `backend/instance/electoral.db` - 196KB, antigua
3. `instance/electoral.db` - 15MB, **activa**

Esto causaba:
- ❌ Confusión sobre cuál usar
- ❌ Posibles errores al ejecutar scripts
- ❌ Datos duplicados o desincronizados
- ❌ Desperdicio de espacio

### Después
Solo hay **1 base de datos**:
- ✅ `instance/electoral.db` - 15MB, activa
- ✅ Configuración clara
- ✅ Sin confusión
- ✅ Scripts usan la BD correcta

## Carpeta Instance

La carpeta `instance/` es especial en Flask:
- Contiene archivos específicos de la instancia
- No se versiona en Git (está en .gitignore)
- Ideal para bases de datos de desarrollo
- Cada desarrollador tiene su propia instancia

## Gitignore

El `.gitignore` está configurado para ignorar:
```gitignore
# Flask instance folder
instance/

# Database files
*.db
*.sqlite
*.sqlite3
```

Esto previene que las bases de datos se suban a Git.

## Desarrollo vs Producción

### Desarrollo (Local)
```python
DATABASE_URL = 'sqlite:///instance/electoral.db'
```
- Base de datos SQLite local
- Archivo en `instance/electoral.db`
- Rápida y fácil de usar

### Producción (Render/Heroku)
```python
DATABASE_URL = 'postgresql://...'  # De variable de entorno
```
- Base de datos PostgreSQL
- Configurada en el servicio de hosting
- Escalable y robusta

## Scripts y Base de Datos

Todos los scripts deben usar la configuración de Flask para acceder a la BD:

```python
from backend.app import create_app
from backend.database import db

app = create_app()
with app.app_context():
    # Aquí el código que accede a la BD
    # Automáticamente usa instance/electoral.db
```

## Backup

Para hacer backup de la base de datos:

```bash
# Windows
copy instance\electoral.db instance\electoral_backup_YYYYMMDD.db

# Linux/Mac
cp instance/electoral.db instance/electoral_backup_YYYYMMDD.db
```

## Resetear Base de Datos

Si necesitas resetear la base de datos:

```bash
# 1. Eliminar BD actual
rm instance/electoral.db

# 2. Recrear con migraciones
flask db upgrade

# 3. Cargar datos iniciales (si hay script)
python scripts/init_data.py
```

## Verificación

Para verificar que solo hay una BD:

```bash
# Windows PowerShell
Get-ChildItem -Path . -Recurse -Filter "electoral.db"

# Linux/Mac
find . -name "electoral.db"
```

Debe mostrar solo: `./instance/electoral.db`

## Migraciones

Las migraciones se guardan en:
```
migrations/
├── versions/
│   ├── xxxx_initial.py
│   ├── xxxx_add_feature.py
│   └── ...
└── alembic.ini
```

Para crear una nueva migración:
```bash
flask db migrate -m "Descripción del cambio"
flask db upgrade
```

## Troubleshooting

### Error: "No such table"
- La BD no tiene las tablas creadas
- Solución: `flask db upgrade`

### Error: "Database is locked"
- Otro proceso está usando la BD
- Solución: Cerrar otros procesos o reiniciar

### Error: "Unable to open database file"
- La carpeta `instance/` no existe
- Solución: `mkdir instance`

## Buenas Prácticas

✅ **Usar siempre** `instance/electoral.db`
✅ **No versionar** la base de datos en Git
✅ **Hacer backups** antes de cambios importantes
✅ **Usar migraciones** para cambios de esquema
✅ **Probar scripts** en copia de la BD primero

❌ **No crear** bases de datos en otras ubicaciones
❌ **No editar** la BD directamente (usar migraciones)
❌ **No compartir** la BD de desarrollo (usar migraciones)

## Resumen

- **Ubicación única**: `instance/electoral.db`
- **Configuración**: `backend/config.py`
- **Gitignore**: Configurado correctamente
- **Scripts**: Usan Flask app context
- **Producción**: PostgreSQL (variable de entorno)
