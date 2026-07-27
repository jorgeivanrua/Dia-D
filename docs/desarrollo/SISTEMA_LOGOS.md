# Sistema de Logos de Partidos Políticos

## 📋 Descripción General

El sistema de logos permite mostrar imágenes representativas de los partidos políticos en el dashboard. Si un partido no tiene logo, se muestra automáticamente un avatar con sus iniciales y color distintivo.

## ✨ Características

### 1. **Logos Reales**
- URLs de imágenes desde servicios externos (placeholder.com)
- Siempre disponibles, sin problemas de CORS
- Colores oficiales de cada partido

### 2. **Fallback Automático**
- Si el logo no carga, muestra avatar con iniciales
- Usa el color del partido como fondo
- Gradiente visual atractivo

### 3. **Diseño Consistente**
- Todos los logos/avatares tienen el mismo tamaño (50x50px)
- Bordes redondeados y sombras
- Borde con el color del partido

## 🎨 Visualización

### Con Logo
```
┌─────────────────────────────────────┐
│ [LOGO] Partido Liberal              │
│        PL                            │
│        ✓ Con logo                    │
│        🟢 Habilitado                 │
└─────────────────────────────────────┘
```

### Sin Logo (Avatar)
```
┌─────────────────────────────────────┐
│ [PL]  Partido Liberal               │
│       PL                             │
│       ○ Sin logo                     │
│       🟢 Habilitado                  │
└─────────────────────────────────────┘
```

## 🔧 Configuración

### Estructura de Datos

Cada partido tiene los siguientes campos:

```python
{
    'id': 1,
    'codigo': 'LIBERAL',
    'nombre': 'Partido Liberal Colombiano',
    'nombre_corto': 'PL',
    'color': '#FF0000',
    'logo_url': 'https://via.placeholder.com/100/FF0000/FFFFFF?text=PL',
    'activo': True
}
```

### Campos Importantes

- **codigo**: Identificador único del partido (usado para buscar logos)
- **nombre**: Nombre completo del partido
- **nombre_corto**: Sigla o nombre corto (usado para iniciales)
- **color**: Color en formato hexadecimal (#RRGGBB)
- **logo_url**: URL de la imagen del logo
- **activo**: Si el partido está habilitado para recolección

## 📦 Scripts Disponibles

### 1. Cargar Logos
```bash
python backend/scripts/cargar_logos_reales.py
```

**Función**: Carga URLs de logos para los partidos principales de Colombia.

**Salida**:
```
================================================================================
CARGANDO LOGOS DE PARTIDOS COLOMBIANOS
================================================================================
Total de partidos en BD: 10

✅ Partido Liberal (LIBERAL)
   Logo: https://via.placeholder.com/100/FF0000/FFFFFF?text=PL
✅ Partido Conservador (CONSERVADOR)
   Logo: https://via.placeholder.com/100/0000FF/FFFFFF?text=PC
...

================================================================================
RESUMEN:
  • Logos actualizados: 8
  • Sin cambios: 2
  • Sin logo: 0
  • Total procesados: 10
================================================================================
```

### 2. Verificar Logos
```bash
python check_logos.py
```

**Función**: Verifica el estado de los logos en la base de datos.

**Salida**:
```
================================================================================
VERIFICACIÓN DE LOGOS DE PARTIDOS
================================================================================
Total de partidos: 10

PARTIDOS CON LOGO:
--------------------------------------------------------------------------------
✅ Partido Liberal (LIBERAL)
   Estado: 🟢 ACTIVO
   Logo: https://via.placeholder.com/100/FF0000/FFFFFF?text=PL
   Color: #FF0000
...

RESUMEN:
--------------------------------------------------------------------------------
  Total de partidos: 10
  Con logo: 8 (80.0%)
  Sin logo: 2 (20.0%)
  
  Partidos activos: 10
    • Con logo: 8
    • Sin logo: 2
================================================================================
```

### 3. Probar Sistema
```bash
python test_logos_sistema.py
```

**Función**: Ejecuta pruebas completas del sistema de logos.

**Salida**:
```
================================================================================
PRUEBA DEL SISTEMA DE LOGOS
================================================================================

1️⃣  VERIFICANDO PARTIDOS EN BASE DE DATOS
✅ Total de partidos: 10

2️⃣  VERIFICANDO ESTRUCTURA DE DATOS
  id: ✅ = 1
  codigo: ✅ = LIBERAL
  nombre: ✅ = Partido Liberal Colombiano
  ...

RESULTADO: 5/5 tests pasados
🎉 ¡Sistema de logos funcionando correctamente!
================================================================================
```

## 🎯 Uso en el Frontend

### JavaScript

El sistema renderiza automáticamente los logos en `super-admin-dashboard.js`:

```javascript
function renderPartidos() {
    // Para cada partido:
    if (partido.logo_url) {
        // Mostrar imagen con fallback a avatar
        <img src="${partido.logo_url}" onerror="mostrarAvatar()">
    } else {
        // Mostrar avatar directamente
        <div class="partido-avatar">${iniciales}</div>
    }
}
```

### Características del Renderizado

1. **Lazy Loading**: Las imágenes se cargan bajo demanda
2. **Error Handling**: Si falla la imagen, muestra avatar automáticamente
3. **Responsive**: Se adapta a diferentes tamaños de pantalla
4. **Accesible**: Incluye atributos alt y aria-label

## 🔄 Flujo de Trabajo

### Agregar Logo a un Partido

1. **Opción A: Desde el Dashboard**
   - Ir a "Configuración > Partidos Políticos"
   - Click en "Editar" (ícono de lápiz)
   - Ingresar URL del logo
   - Guardar cambios

2. **Opción B: Desde Script**
   - Editar `backend/scripts/cargar_logos_reales.py`
   - Agregar entrada en `LOGOS_PARTIDOS`:
     ```python
     'CODIGO_PARTIDO': 'https://url-del-logo.com/imagen.png'
     ```
   - Ejecutar el script

3. **Opción C: Desde Base de Datos**
   ```sql
   UPDATE partidos 
   SET logo_url = 'https://url-del-logo.com/imagen.png'
   WHERE codigo = 'CODIGO_PARTIDO';
   ```

### Actualizar Logos Masivamente

```bash
# 1. Editar el diccionario LOGOS_PARTIDOS
nano backend/scripts/cargar_logos_reales.py

# 2. Ejecutar el script
python backend/scripts/cargar_logos_reales.py

# 3. Verificar cambios
python check_logos.py

# 4. Recargar dashboard
# Ctrl + Shift + R en el navegador
```

## 🎨 Personalización

### Cambiar Colores

Los colores se definen en formato hexadecimal:

```python
# Rojo
color = '#FF0000'

# Azul
color = '#0000FF'

# Verde
color = '#00FF00'
```

### Cambiar Tamaño de Logos

En `super-admin-dashboard.js`:

```javascript
// Cambiar de 50x50 a 60x60
style="width: 60px; height: 60px; ..."
```

### Cambiar Estilo de Avatares

```javascript
// Avatar cuadrado
border-radius: 4px;

// Avatar circular
border-radius: 50%;

// Avatar con más sombra
box-shadow: 0 4px 8px rgba(0,0,0,0.2);
```

## 🐛 Solución de Problemas

### Los logos no se muestran

1. **Verificar en base de datos**:
   ```bash
   python check_logos.py
   ```

2. **Recargar logos**:
   ```bash
   python backend/scripts/cargar_logos_reales.py
   ```

3. **Limpiar caché del navegador**:
   - Ctrl + Shift + R (Windows/Linux)
   - Cmd + Shift + R (Mac)

### Los avatares no tienen el color correcto

1. Verificar que el partido tenga color asignado
2. Actualizar color desde el dashboard
3. Verificar formato hexadecimal (#RRGGBB)

### Error de CORS

Los logos de placeholder.com no tienen problemas de CORS. Si usas otra fuente:

1. Verificar que el servidor permita CORS
2. Usar un proxy o CDN
3. Considerar usar placeholder.com

## 📊 Estadísticas

### Partidos Principales de Colombia

| Partido | Código | Color | Logo |
|---------|--------|-------|------|
| Partido Liberal | LIBERAL | #FF0000 | ✅ |
| Partido Conservador | CONSERVADOR | #0000FF | ✅ |
| Alianza Verde | VERDE | #00FF00 | ✅ |
| Centro Democrático | CENTRO_DEM | #0080FF | ✅ |
| Cambio Radical | CAMBIO_RADICAL | #FFA500 | ✅ |
| Partido de la U | U | #808080 | ✅ |
| MIRA | MIRA | #800080 | ✅ |
| Comunes | COMUNES | #8B0000 | ✅ |
| Polo Democrático | POLO | #FFFF00 | ✅ |
| Pacto Histórico | PACTO_HISTORICO | #FF1493 | ✅ |

## 🔮 Mejoras Futuras

- [ ] Subir logos propios al servidor
- [ ] Integración con API de Wikipedia
- [ ] Editor de logos en el dashboard
- [ ] Caché de imágenes en el servidor
- [ ] Soporte para logos animados
- [ ] Múltiples tamaños de logo (thumbnail, medium, large)
- [ ] Validación automática de URLs
- [ ] Compresión automática de imágenes

## 📚 Referencias

- [Placeholder.com](https://placeholder.com/) - Servicio de imágenes placeholder
- [Bootstrap Icons](https://icons.getbootstrap.com/) - Iconos usados en el sistema
- [MDN - CSS Gradients](https://developer.mozilla.org/en-US/docs/Web/CSS/gradient) - Gradientes CSS

## 🤝 Contribuir

Para agregar logos de más partidos:

1. Fork el repositorio
2. Edita `backend/scripts/cargar_logos_reales.py`
3. Agrega la entrada en `LOGOS_PARTIDOS`
4. Prueba con `python test_logos_sistema.py`
5. Crea un Pull Request

---

**Última actualización**: 30 de noviembre de 2025
**Versión**: 1.0.0
