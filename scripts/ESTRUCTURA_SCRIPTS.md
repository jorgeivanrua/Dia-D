# Estructura de Scripts - Organización Final

## Fecha: 2025-12-07

## Estructura Organizada

```
scripts/
├── init/          # Inicialización y carga de datos (~30 archivos)
│   ├── README.md
│   ├── init_*.py
│   ├── load_*.py
│   ├── cargar_*.py
│   ├── crear_*.py
│   └── ...
├── test/          # Pruebas y verificación (~50 archivos)
│   ├── README.md
│   ├── test_*.py
│   ├── verificar_*.py
│   ├── check_*.py
│   ├── diagnostico_*.py
│   └── ...
├── fix/           # Corrección y reparación (~15 archivos)
│   ├── README.md
│   ├── fix_*.py
│   ├── corregir_*.py
│   ├── desbloquear_*.py
│   └── ...
├── utils/         # Utilidades y herramientas (~17 archivos)
│   ├── README.md
│   ├── actualizar_*.py
│   ├── listar_*.py
│   ├── *.sql
│   ├── *.bat
│   └── ...
├── README_PRINCIPAL.md
├── ESTRUCTURA_SCRIPTS.md (este archivo)
├── README.md (antiguo)
├── README_CARGA_DATOS_2023.md
└── README_NUEVO.md
```

## Reorganización Realizada

### 1. Consolidación de Carpetas
**Antes**: 2 carpetas
- `/scripts` (raíz) - 119 archivos
- `/backend/scripts` - 15 archivos

**Después**: 1 carpeta con 4 subcarpetas
- `/scripts/init` - 30 archivos
- `/scripts/test` - 50 archivos
- `/scripts/fix` - 15 archivos
- `/scripts/utils` - 17 archivos

### 2. Reubicación de Archivos
- ✅ Scripts de test movidos de `/init` a `/test`
- ✅ Scripts de verificación movidos a `/test`
- ✅ Archivos .bat movidos a carpetas apropiadas
- ✅ Scripts de backend/scripts consolidados en `/init`

### 3. Eliminación de Duplicados
Archivos eliminados:
- `load_basic_data_simple.py` (mantener load_complete_test_data.py)
- `init_db_simple.py` (mantener init_db.py)
- `test_all_roles_api.py` (mantener test_all_roles.py)
- `verificar_y_cargar_datos_completo.py` (duplicado)
- `clean_and_reload.py` (obsoleto)
- `test_init_data.py` (obsoleto)
- `test_testigo_fix.py` (obsoleto)

Total eliminados: ~7 archivos

### 4. Documentación Creada
- ✅ `README.md` en cada subcarpeta
- ✅ `ESTRUCTURA_SCRIPTS.md` (este archivo)
- ✅ `README_PRINCIPAL.md` actualizado

## Guía de Uso por Carpeta

### `/init` - Inicialización
**Cuándo usar**: Al configurar el sistema por primera vez o cargar datos

**Scripts principales**:
```bash
# Setup completo
python scripts/init/init_system.py
python scripts/init/load_complete_test_data.py

# Solo Caquetá
python scripts/init/init_caqueta_electoral_data.py
python scripts/init/load_only_caqueta.py

# Usuarios
python scripts/init/crear_usuarios_florencia.py
```

### `/test` - Pruebas
**Cuándo usar**: Para verificar que todo funciona correctamente

**Scripts principales**:
```bash
# Verificación completa
python scripts/test/verificacion_completa_sistema.py
python scripts/test/check_system.py

# Pruebas de roles
python scripts/test/test_all_roles.py

# Pruebas de endpoints
python scripts/test/test_coordinador_municipal_endpoints.py
```

### `/fix` - Correcciones
**Cuándo usar**: Cuando hay problemas que necesitan corrección

**⚠️ IMPORTANTE**: Hacer backup antes
```bash
copy instance\electoral.db instance\electoral_backup.db
```

**Scripts principales**:
```bash
# Corrección de usuarios
python scripts/fix/fix_usuarios_ubicacion.py
python scripts/fix/corregir_roles_universal.py

# Corrección de BD
python scripts/fix/fix_database_columns.py
```

### `/utils` - Utilidades
**Cuándo usar**: Para tareas de mantenimiento y actualización

**Scripts principales**:
```bash
# Actualizar datos
python scripts/utils/actualizar_votantes_mesas.py
python scripts/utils/actualizar_logos_partidos.py

# Listar datos
python scripts/utils/listar_municipios_caqueta.py
python scripts/utils/listar_testigos.py
```

## Convenciones de Nombres

### Prefijos por Tipo
- `init_*.py` → Inicialización
- `load_*.py` → Carga de datos
- `cargar_*.py` → Carga de datos (español)
- `crear_*.py` → Creación de registros
- `test_*.py` → Pruebas
- `verificar_*.py` → Verificación
- `check_*.py` → Checks
- `diagnostico_*.py` → Diagnóstico
- `fix_*.py` → Correcciones
- `corregir_*.py` → Correcciones (español)
- `actualizar_*.py` → Actualización
- `listar_*.py` → Listado

### Sufijos Especiales
- `*_v2.py` → Versión 2 (mejorada)
- `*_simple.py` → Versión simplificada
- `*_completo.py` → Versión completa
- `*.bat` → Scripts de Windows
- `*.sql` → Scripts SQL

## Flujos de Trabajo Comunes

### Setup Inicial
```bash
# 1. Inicializar
python scripts/init/init_system.py

# 2. Cargar datos
python scripts/init/load_complete_test_data.py

# 3. Verificar
python scripts/test/verificacion_completa_sistema.py
```

### Desarrollo Diario
```bash
# 1. Verificar estado
python scripts/test/check_system.py

# 2. Probar cambios
python scripts/test/test_endpoints.py

# 3. Si hay problemas
python scripts/fix/[script_apropiado].py
```

### Mantenimiento
```bash
# 1. Actualizar datos
python scripts/utils/actualizar_votantes_mesas.py

# 2. Verificar
python scripts/test/verificar_votantes_mesas.py

# 3. Listar para confirmar
python scripts/utils/listar_testigos.py
```

## Mejores Prácticas

### Antes de Ejecutar
✅ Leer el README de la subcarpeta
✅ Entender qué hace el script
✅ Hacer backup si es script de corrección
✅ Activar entorno virtual

### Durante la Ejecución
✅ Ejecutar desde raíz del proyecto
✅ Revisar output del script
✅ Anotar cualquier error

### Después de Ejecutar
✅ Verificar que funcionó
✅ Probar la funcionalidad afectada
✅ Documentar si es necesario

## Mantenimiento de Scripts

### Mensual
- Revisar scripts nuevos y ubicarlos correctamente
- Actualizar READMEs si hay cambios

### Trimestral
- Identificar scripts obsoletos
- Consolidar duplicados
- Actualizar documentación

### Anual
- Revisar toda la estructura
- Eliminar scripts muy antiguos
- Reorganizar si es necesario

## Resultado Final

✅ **Estructura clara**: 4 carpetas bien definidas
✅ **Sin duplicados**: Eliminados 7 archivos duplicados
✅ **Bien documentado**: README en cada carpeta
✅ **Fácil de usar**: Scripts organizados por función
✅ **Mantenible**: Convenciones claras establecidas

**Total de scripts**: ~112 archivos organizados
**Eliminados**: ~7 duplicados/obsoletos
**Documentación**: 5 READMEs creados
