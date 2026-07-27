# Scripts de Utilidades

Scripts de utilidades generales y herramientas.

## Uso Común

### Preparar Datos para Render ⭐ NUEVO
```bash
# Script TODO-EN-UNO para preparar datos para Render
python scripts/utils/preparar_datos_render.py
```
Este script ejecuta automáticamente:
1. Marca usuarios definitivos como básicos
2. Verifica usuarios básicos
3. Limpia usuarios de prueba (opcional)
4. Exporta BD a JSON
5. Copia archivo a data/render_initial_data.json

### Gestión de Usuarios Básicos del Sistema
```bash
# Verificar usuarios básicos del sistema
python scripts/utils/verificar_usuarios_basicos.py

# Marcar usuarios definitivos como básicos (RECOMENDADO - hace todo de una vez)
python scripts/utils/marcar_usuarios_definitivos_basicos.py

# Limpiar usuarios de prueba (mantener solo usuarios básicos)
python scripts/utils/limpiar_usuarios_prueba.py
```

### Backup y Restauración de Base de Datos
```bash
# Exportar base de datos a JSON
python scripts/utils/export_data_to_json.py

# Importar base de datos desde JSON
python scripts/utils/import_data_from_json.py [archivo.json]
```

### Actualización de Datos
```bash
# Actualizar votantes por mesa
python scripts/utils/actualizar_votantes_mesas.py

# Actualizar coordenadas de puestos
python scripts/utils/actualizar_coordenadas_puestos_v2.py

# Actualizar logos de partidos
python scripts/utils/actualizar_logos_partidos.py
```

### Listar Datos
```bash
# Listar municipios de Caquetá
python scripts/utils/listar_municipios_caqueta.py

# Listar testigos
python scripts/utils/listar_testigos.py
```

## Categorías

### Preparación para Render ⭐ NUEVO
- `preparar_datos_render.py` - Script TODO-EN-UNO para preparar datos (RECOMENDADO)

### Gestión de Usuarios Básicos ⭐ NUEVO
- `verificar_usuarios_basicos.py` - Verificar usuarios básicos del sistema
- `limpiar_usuarios_prueba.py` - Eliminar usuarios de prueba
- `marcar_usuarios_definitivos_basicos.py` - Marcar usuarios definitivos como básicos
- `marcar_testigos_basicos.py` - Marcar solo testigos como usuarios básicos

### Backup y Restauración ⭐ NUEVO
- `export_data_to_json.py` - Exportar BD completa a JSON
- `import_data_from_json.py` - Importar BD desde JSON (acepta archivo como argumento)

### Actualización de Datos
- `actualizar_candidatos_completos.py` - Candidatos
- `actualizar_coordenadas_puestos.py` - Coordenadas de puestos
- `actualizar_coordenadas_puestos_v2.py` - Coordenadas v2
- `actualizar_logos_partidos.py` - Logos de partidos
- `actualizar_votantes_mesas.py` - Votantes por mesa

### Agregar Datos
- `add_citrep_tipo_eleccion.py` - Tipo de elección CITREP

### Listar Datos
- `listar_municipios_caqueta.py` - Municipios de Caquetá
- `listar_testigos.py` - Testigos

### Asignación
- `asignar_ubicacion_testigos.py` - Ubicación a testigos

### Upload/Download
- `upload_db_to_render.py` - Subir BD a Render

### Archivos SQL
- `crear_indices_monitoreo.sql` - Índices de monitoreo
- `optimizar_bd_monitoreo.sql` - Optimizar BD monitoreo
- `verificar_y_corregir_roles.sql` - Verificar y corregir roles

### Batch Scripts (Windows)
- `actualizar_logos.bat` - Actualizar logos
- `crear_usuario_monitoreo.bat` - Crear usuario monitoreo
- `inicializar_datos.bat` - Inicializar datos
- `instalar_monitoreo_completo.bat` - Instalar monitoreo

## Uso de Archivos SQL

```bash
# Ejecutar SQL en SQLite
sqlite3 instance/electoral.db < scripts/utils/crear_indices_monitoreo.sql
```

## Uso de Batch Scripts

```cmd
# Windows
scripts\utils\actualizar_logos.bat
```

## Usuarios Básicos del Sistema

Los **usuarios básicos** son usuarios DEFINITIVOS que NO deben eliminarse:

### 1. Usuarios Globales (sin ubicación)
- **Super Admin** (1) - Acceso completo al sistema
- **Monitoreo** (1) - Acceso de solo lectura para monitoreo en tiempo real

### 2. Usuarios con Ubicación Específica (1 por ubicación)
- **Coordinador Departamental** - 1 por departamento
- **Coordinador Municipal** - 1 por municipio
- **Coordinador de Puesto** - 1 por puesto
- **Testigo Electoral** - 1 por puesto

**IMPORTANTE**: Estos son los usuarios DEFINITIVOS del sistema. Cada ubicación debe tener exactamente 1 coordinador y 1 testigo marcados como básicos.

Estos usuarios tienen `es_usuario_basico=True` y están protegidos en:
- Importación de base de datos (no se sobrescriben)
- Limpieza de usuarios de prueba (no se eliminan)
- Inicialización automática al arrancar la app (solo Super Admin y Monitoreo)

## Flujo de Trabajo Recomendado

### 1. Desarrollo Local - Preparar para Render

**Opción A: Script TODO-EN-UNO (Recomendado)**
```bash
python scripts/utils/preparar_datos_render.py
```
Este script hace todo automáticamente y genera `data/render_initial_data.json`

**Opción B: Paso a paso**
```bash
# 1. Marcar usuarios definitivos como básicos
python scripts/utils/marcar_usuarios_definitivos_basicos.py

# 2. Verificar que todos estén marcados correctamente
python scripts/utils/verificar_usuarios_basicos.py

# 3. Limpiar usuarios de prueba antes de exportar
python scripts/utils/limpiar_usuarios_prueba.py

# 4. Exportar BD limpia
python scripts/utils/export_data_to_json.py

# 5. Copiar a data/render_initial_data.json
cp data_export_*.json data/render_initial_data.json
```

### 2. Despliegue en Render
- Los usuarios básicos se crean automáticamente al iniciar la app
- Usar el botón "Importar Base de Datos" en Super Admin Dashboard
- Los usuarios básicos existentes NO se sobrescriben

### 3. Mantenimiento
```bash
# Marcar usuarios definitivos como básicos (después de agregar ubicaciones/usuarios)
python scripts/utils/marcar_usuarios_definitivos_basicos.py

# Verificar estado del sistema
python scripts/utils/verificar_usuarios_basicos.py

# Backup periódico
python scripts/utils/export_data_to_json.py
```

## Notas

- Scripts de actualización modifican datos existentes
- Hacer backup antes de actualizar datos importantes
- Scripts de listado son solo lectura (seguros)
- Archivos .bat solo funcionan en Windows
- **IMPORTANTE**: Los usuarios básicos están protegidos contra eliminación accidental
