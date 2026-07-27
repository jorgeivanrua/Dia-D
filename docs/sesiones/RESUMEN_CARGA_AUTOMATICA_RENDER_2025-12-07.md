# Resumen: Carga Automática de Datos en Render

**Fecha**: 2025-12-07  
**Sesión**: Continuación - Carga automática de datos  
**Estado**: ✅ Completado

## Problema

Render no cargaba automáticamente las ubicaciones ni los usuarios. Solo creaba la estructura de la BD y los usuarios básicos (Super Admin y Monitoreo), pero el resto de datos había que importarlos manualmente desde el dashboard.

## Solución Implementada

### Sistema de Carga Automática

Render ahora busca y carga automáticamente un archivo JSON con todos los datos en el primer despliegue.

### Archivos Buscados (en orden)

1. `data/render_initial_data.json` ⭐ RECOMENDADO
2. `render_initial_data.json` (raíz)
3. `initial_data.json` (raíz)

### Script TODO-EN-UNO

Creado `scripts/utils/preparar_datos_render.py` que ejecuta automáticamente:

1. Marca usuarios definitivos como básicos
2. Verifica usuarios básicos
3. Limpia usuarios de prueba (opcional)
4. Exporta BD a JSON
5. Copia archivo a `data/render_initial_data.json`

**Uso**:
```bash
python scripts/utils/preparar_datos_render.py
```

### Modificaciones en Scripts

#### `scripts/init/render_setup.py`
- Agregado PASO 6: Importación automática de datos
- Busca archivos JSON en ubicaciones predefinidas
- Ejecuta `import_data_from_json.py` automáticamente
- Muestra instrucciones si no encuentra archivo

#### `scripts/utils/import_data_from_json.py`
- Acepta archivo como argumento: `python import_data_from_json.py [archivo.json]`
- Modo automático sin confirmación cuando se ejecuta en Render
- Detecta entorno Render con `os.getenv('RENDER')`
- Usa `sys.stdin.isatty()` para detectar modo interactivo

### Documentación

#### `data/README.md` (NUEVO)
Documentación completa sobre:
- Cómo preparar datos para Render
- Formato del archivo JSON
- Flujo de trabajo
- Troubleshooting

#### `scripts/utils/README.md` (ACTUALIZADO)
- Agregada sección "Preparar Datos para Render"
- Documentado script `preparar_datos_render.py`
- Actualizado flujo de trabajo

## Flujo de Trabajo Completo

### 1. Preparar Datos en Local

**Opción A: Script TODO-EN-UNO (Recomendado)**
```bash
python scripts/utils/preparar_datos_render.py
```

**Opción B: Paso a paso**
```bash
# 1. Marcar usuarios definitivos
python scripts/utils/marcar_usuarios_definitivos_basicos.py

# 2. Verificar
python scripts/utils/verificar_usuarios_basicos.py

# 3. Limpiar usuarios de prueba (opcional)
python scripts/utils/limpiar_usuarios_prueba.py

# 4. Exportar
python scripts/utils/export_data_to_json.py

# 5. Copiar
cp data_export_*.json data/render_initial_data.json
```

### 2. Commit y Push

```bash
git add data/render_initial_data.json
git commit -m "feat: Agregar datos iniciales para Render"
git push
```

### 3. Despliegue Automático en Render

Render ejecuta `scripts/init/render_setup.py` que:
1. ✅ Crea estructura de BD (PostgreSQL)
2. ✅ Crea usuarios básicos (Super Admin, Monitoreo)
3. ✅ **Busca y carga automáticamente** `data/render_initial_data.json`
4. ✅ Importa ubicaciones, usuarios, formularios, etc.

**Sin intervención manual necesaria**

## Datos Importados Automáticamente

- ✅ Ubicaciones (departamentos, municipios, puestos, mesas)
- ✅ Usuarios (coordinadores, testigos, auditores)
- ✅ Formularios E-14
- ✅ Votos por partido
- ✅ Incidentes electorales
- ✅ Delitos electorales
- ✅ Evidencias fotográficas

## Protecciones

1. **Usuarios básicos**: NO se sobrescriben si ya existen
2. **Contraseñas**: Usuarios importados reciben `test123`
3. **Modo automático**: Sin confirmación en Render
4. **Manejo de errores**: Continúa aunque fallen registros individuales

## Archivos Creados/Modificados

### Nuevos
- `scripts/utils/preparar_datos_render.py` - Script TODO-EN-UNO
- `data/README.md` - Documentación completa
- `docs/sesiones/RESUMEN_CARGA_AUTOMATICA_RENDER_2025-12-07.md` - Este archivo

### Modificados
- `scripts/init/render_setup.py` - Agregado PASO 6 de importación automática
- `scripts/utils/import_data_from_json.py` - Acepta argumento, modo automático
- `scripts/utils/README.md` - Documentación actualizada

## Ventajas

1. **Cero intervención manual**: Todo se carga automáticamente
2. **Reproducible**: Mismo proceso cada vez
3. **Documentado**: README completo con instrucciones
4. **Flexible**: Puede usarse archivo en diferentes ubicaciones
5. **Seguro**: Protege usuarios básicos existentes

## Próximos Pasos

1. ✅ Sistema de carga automática implementado
2. ✅ Script TODO-EN-UNO creado
3. ✅ Documentación completa
4. ⏳ **Ejecutar en local**: `python scripts/utils/preparar_datos_render.py`
5. ⏳ **Commit y push**: Subir `data/render_initial_data.json`
6. ⏳ **Verificar en Render**: Revisar logs de despliegue

## Notas Importantes

- **Tamaño del archivo**: GitHub tiene límite de 100MB. Si el archivo es muy grande, considerar Git LFS
- **Actualizaciones**: Para actualizar datos, modificar el archivo y redesplegar, o usar el dashboard
- **Logs**: Revisar logs de Render para ver el proceso de importación
- **Credenciales**: Super Admin (admin123), usuarios importados (test123)

## Commits

```
feat: Carga automática de datos en Render desde archivo JSON

- Render busca y carga automáticamente data/render_initial_data.json
- Script preparar_datos_render.py: TODO-EN-UNO
- import_data_from_json.py acepta archivo como argumento
- Modo automático sin confirmación en Render
- Documentación completa
```

**Commit hash**: ef08e04  
**Pusheado**: ✅ Sí

## Testing

Para probar localmente:

```bash
# 1. Preparar datos
python scripts/utils/preparar_datos_render.py

# 2. Simular importación
python scripts/utils/import_data_from_json.py data/render_initial_data.json

# 3. Verificar
python scripts/utils/verificar_usuarios_basicos.py
```

## Troubleshooting

### El archivo no se carga en Render
- Verificar que existe en `data/render_initial_data.json`
- Verificar que es JSON válido
- Revisar logs de Render

### Archivo muy grande
- Usar Git LFS
- O importar manualmente desde dashboard
- O dividir en archivos más pequeños

### Errores de importación
- Revisar formato del JSON
- Verificar relaciones (IDs)
- Ver logs de Render para detalles
