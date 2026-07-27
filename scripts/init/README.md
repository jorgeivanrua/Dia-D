# Scripts de Inicialización

Scripts para inicializar y cargar datos en el sistema.

## Uso Común

### Inicialización Completa del Sistema
```bash
# 1. Inicializar base de datos
python scripts/init/init_db.py

# 2. Cargar datos completos de prueba
python scripts/init/load_complete_test_data.py

# 3. Crear usuarios de prueba
python scripts/init/crear_usuarios_florencia.py
```

### Inicialización para Caquetá
```bash
# Cargar datos electorales de Caquetá
python scripts/init/init_caqueta_electoral_data.py

# Cargar solo Caquetá (DIVIPOLA)
python scripts/init/load_only_caqueta.py
```

## Categorías

### Inicialización de Base de Datos
- `init_db.py` - Inicializar BD
- `init_system.py` - Sistema completo
- `init_configuracion_electoral.py` - Configuración electoral
- `init_super_admin_data.py` - Datos de super admin

### Carga de Datos Geográficos
- `load_divipola.py` - DIVIPOLA completo
- `cargar_divipola_v2.py` - DIVIPOLA v2
- `load_only_caqueta.py` - Solo Caquetá

### Carga de Datos Electorales
- `cargar_partidos_2023.py` - Partidos 2023
- `cargar_candidatos_2023.py` - Candidatos 2023
- `cargar_partidos_candidatos.py` - Partidos y candidatos
- `cargar_logos_bd.py` - Logos de partidos

### Creación de Usuarios
- `crear_testigos_iniciales.py` - Testigos iniciales
- `crear_testigos_prueba.py` - Testigos de prueba
- `crear_usuarios_caqueta.py` - Usuarios de Caquetá
- `crear_usuarios_florencia.py` - Usuarios de Florencia
- `crear_usuario_monitoreo.py` - Usuario de monitoreo

### Migraciones
- `migrate_to_alembic.py` - Migrar a Alembic
- `apply_migration_now.py` - Aplicar migración
- `aplicar_migracion_monitoreo.py` - Migración monitoreo
- `aplicar_optimizaciones.py` - Optimizaciones
- `aplicar_indices.py` - Índices

### Deploy
- `render_setup.py` - Setup para Render

## Notas

- Ejecutar desde la raíz del proyecto
- Activar entorno virtual antes: `.venv\Scripts\activate`
- Algunos scripts requieren BD inicializada
- Hacer backup antes de ejecutar migraciones
