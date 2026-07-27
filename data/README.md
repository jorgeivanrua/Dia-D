# Datos Iniciales para Render

Este directorio contiene los datos iniciales que se cargarán automáticamente en Render.

## Archivo de Datos Inicial

Para que Render cargue automáticamente todos los datos (ubicaciones, usuarios, formularios, etc.) en el primer despliegue:

### 1. Preparar los Datos en Local

```bash
# 1. Marcar usuarios definitivos como básicos
python scripts/utils/marcar_usuarios_definitivos_basicos.py

# 2. Verificar que todo esté correcto
python scripts/utils/verificar_usuarios_basicos.py

# 3. Limpiar usuarios de prueba (opcional)
python scripts/utils/limpiar_usuarios_prueba.py

# 4. Exportar BD completa a JSON
python scripts/utils/export_data_to_json.py
```

Esto generará un archivo `data_export_YYYYMMDD_HHMMSS.json` en el directorio raíz.

### 2. Preparar para Render

```bash
# Copiar el archivo exportado a este directorio con el nombre correcto
cp data_export_YYYYMMDD_HHMMSS.json data/render_initial_data.json

# O renombrar directamente
mv data_export_YYYYMMDD_HHMMSS.json data/render_initial_data.json
```

### 3. Commit y Push

```bash
git add data/render_initial_data.json
git commit -m "feat: Agregar datos iniciales para Render"
git push
```

### 4. Despliegue en Render

Render ejecutará automáticamente `scripts/init/render_setup.py` que:
1. Creará la estructura de la BD (PostgreSQL)
2. Creará usuarios básicos (Super Admin, Monitoreo)
3. **Buscará y cargará automáticamente** `data/render_initial_data.json`
4. Importará todas las ubicaciones, usuarios, formularios, etc.

## Archivos Buscados

El script de inicialización busca archivos en este orden:
1. `data/render_initial_data.json` ⭐ RECOMENDADO
2. `render_initial_data.json` (raíz del proyecto)
3. `initial_data.json` (raíz del proyecto)

## Contenido del Archivo JSON

El archivo debe contener:
- `users` - Usuarios del sistema
- `locations` - Ubicaciones (departamentos, municipios, puestos, mesas)
- `formularios` - Formularios E-14
- `votos_partidos` - Votos por partido
- `incidentes` - Incidentes electorales
- `delitos` - Delitos electorales
- `evidencias` - Evidencias fotográficas

## Notas Importantes

- **Usuarios básicos**: Los usuarios con `es_usuario_basico=True` NO se sobrescriben si ya existen
- **Contraseñas**: Los usuarios importados reciben contraseña temporal `test123`
- **Tamaño**: GitHub tiene límite de 100MB por archivo. Si tu archivo es muy grande, considera:
  - Usar Git LFS (Large File Storage)
  - Comprimir el archivo (gzip)
  - Importar manualmente desde el dashboard después del despliegue

## Actualizar Datos

Para actualizar los datos en Render después del primer despliegue:

### Opción 1: Desde el Dashboard (Recomendado)
1. Acceder a Super Admin Dashboard
2. Exportar BD actual (backup)
3. Importar nuevo archivo JSON

### Opción 2: Actualizar el archivo y redesplegar
1. Actualizar `data/render_initial_data.json`
2. Commit y push
3. Render redesplegar automáticamente
4. **NOTA**: Solo importará datos nuevos, no sobrescribirá existentes

## Troubleshooting

### El archivo no se carga automáticamente
- Verificar que el archivo existe en `data/render_initial_data.json`
- Verificar que el archivo es JSON válido
- Revisar logs de Render para ver errores

### Errores de importación
- Verificar que el formato del JSON es correcto
- Verificar que las relaciones (IDs) son válidas
- Revisar logs de Render para detalles del error

### Archivo muy grande
- Considerar usar Git LFS
- O importar manualmente desde el dashboard
- O dividir en múltiples archivos más pequeños
