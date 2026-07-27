# Guía de Logos de Partidos Políticos

## Descripción
Los logos de los partidos políticos se almacenan como URLs en la base de datos y se muestran en todo el sistema (dashboard, formularios, reportes).

---

## 1. Almacenamiento en Base de Datos

### Campo en la Tabla `partidos`
```sql
CREATE TABLE partidos (
    id INTEGER PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    nombre_corto VARCHAR(50),
    color VARCHAR(7),  -- Color hexadecimal
    logo_url VARCHAR(500),  -- ← URL del logo
    activo BOOLEAN DEFAULT TRUE,
    orden INTEGER DEFAULT 0
);
```

### Tipos de URLs Soportadas

1. **URLs Externas** (Recomendado):
   ```
   https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Colombian_Liberal_Party_logo.svg/200px-Colombian_Liberal_Party_logo.svg.png
   ```
   - ✅ No requiere almacenamiento local
   - ✅ URLs estables de Wikipedia
   - ✅ Imágenes optimizadas

2. **URLs Locales**:
   ```
   /static/uploads/logos/partido_liberal.png
   ```
   - ✅ Control total sobre las imágenes
   - ❌ Requiere almacenamiento en el servidor
   - ❌ Requiere gestión de archivos

---

## 2. Carga Automática desde Wikipedia

### Paso a Paso

1. **Acceder al Dashboard del Super Admin**:
   ```
   http://localhost:5000/super-admin-dashboard
   ```

2. **Ir a la sección "Partidos Políticos"**

3. **Hacer clic en el botón "Cargar Logos"** (icono de imagen)

4. **Confirmar la acción**:
   ```
   ¿Desea cargar los logos de los partidos políticos colombianos desde Wikipedia?
   
   Esto actualizará los logos de los partidos que coincidan con los nombres estándar.
   ```

5. **Ver el resultado**:
   ```
   ✅ Logos cargados exitosamente:
   
   📊 Total de partidos: 9
   ✅ Logos actualizados: 7
   ℹ️  Sin cambios: 0
   ⚠️  Sin logo encontrado: 2
   
   Partidos actualizados:
     • Partido Liberal
     • Partido Conservador
     • Centro Democrático
     • Pacto Histórico
     • Cambio Radical
     • Partido de la U
     • Alianza Verde
   
   Partidos sin logo:
     • Partido Nuevo
     • Movimiento Local
   ```

### Partidos Soportados

El sistema tiene URLs predefinidas para estos partidos colombianos:

| Partido | Nombre Corto | URL Wikipedia |
|---------|--------------|---------------|
| Partido Liberal | PL | ✅ Disponible |
| Partido Conservador | PC | ✅ Disponible |
| Centro Democrático | CD | ✅ Disponible |
| Pacto Histórico | PH | ✅ Disponible |
| Cambio Radical | CR | ✅ Disponible |
| Partido de la U | La U | ✅ Disponible |
| Alianza Verde | Verde | ✅ Disponible |
| Polo Democrático | Polo | ✅ Disponible |
| MIRA | MIRA | ✅ Disponible |
| Comunes | Comunes | ✅ Disponible |

### Algoritmo de Búsqueda

```python
def buscar_logo(partido):
    nombre_upper = partido.nombre.upper()
    nombre_corto_upper = partido.nombre_corto.upper()
    
    # 1. Buscar por nombre exacto
    if nombre_upper in LOGOS_PARTIDOS:
        return LOGOS_PARTIDOS[nombre_upper]
    
    # 2. Buscar por nombre_corto exacto
    if nombre_corto_upper in LOGOS_PARTIDOS:
        return LOGOS_PARTIDOS[nombre_corto_upper]
    
    # 3. Buscar por coincidencia parcial
    for key, url in LOGOS_PARTIDOS.items():
        if key in nombre_upper or nombre_upper in key:
            return url
    
    # 4. No encontrado
    return None
```

---

## 3. Carga Manual de Logos

### Opción 1: Actualizar en la Base de Datos

```sql
-- Actualizar logo de un partido específico
UPDATE partidos 
SET logo_url = 'https://ejemplo.com/logo.png'
WHERE id = 1;

-- O por nombre
UPDATE partidos 
SET logo_url = 'https://ejemplo.com/logo.png'
WHERE nombre = 'Partido Liberal';
```

### Opción 2: Cargar desde Excel

**Archivo Excel** (`partidos.xlsx`):
```
nombre                  | nombre_corto | color    | logo_url
Partido Liberal         | PL           | #FF0000  | https://ejemplo.com/liberal.png
Partido Conservador     | PC           | #0000FF  | https://ejemplo.com/conservador.png
```

**Cargar en el sistema**:
1. Ir al dashboard del Super Admin
2. Sección "Importar Datos"
3. Seleccionar archivo Excel
4. Hacer clic en "Cargar Partidos"

### Opción 3: Subir Archivos al Servidor

**Crear carpeta de logos**:
```bash
mkdir -p frontend/static/uploads/logos
```

**Subir archivo**:
```bash
# Copiar logo al servidor
cp partido_liberal.png frontend/static/uploads/logos/
```

**Actualizar en BD**:
```sql
UPDATE partidos 
SET logo_url = '/static/uploads/logos/partido_liberal.png'
WHERE nombre = 'Partido Liberal';
```

---

## 4. Uso de Logos en el Sistema

### 4.1 Dashboard del Super Admin

Los logos se muestran en la lista de partidos:

```html
<div class="partido-item">
  <img src="https://upload.wikimedia.org/..." 
       alt="Partido Liberal" 
       class="partido-logo"
       style="width: 40px; height: 40px;">
  <span>Partido Liberal</span>
</div>
```

### 4.2 Formulario E-14 (Testigos)

Los testigos ven los logos al registrar votos:

```javascript
// Endpoint
GET /api/testigo/partidos

// Respuesta
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nombre": "Partido Liberal",
      "nombre_corto": "PL",
      "color": "#FF0000",
      "logo_url": "https://upload.wikimedia.org/..."
    }
  ]
}

// Renderizado
partidos.forEach(partido => {
  const html = `
    <div class="partido-voto">
      <img src="${partido.logo_url}" alt="${partido.nombre}">
      <span>${partido.nombre}</span>
      <input type="number" name="votos_${partido.id}">
    </div>
  `;
});
```

### 4.3 Reportes E-24 (PDFs)

Los logos se incluyen en los PDFs generados:

```python
from reportlab.lib.utils import ImageReader
import requests
from io import BytesIO

def agregar_logo_pdf(partido, pdf):
    if partido.logo_url:
        try:
            # Descargar imagen
            response = requests.get(partido.logo_url, timeout=5)
            img_data = BytesIO(response.content)
            
            # Agregar al PDF
            img = Image(img_data, width=30, height=30)
            pdf.drawImage(img, x=50, y=700)
        except:
            # Si falla, usar texto
            pdf.drawString(50, 700, partido.nombre_corto)
```

### 4.4 Dashboard de Monitoreo

Los logos se muestran en tiempo real:

```javascript
// Mapa con marcadores de partidos
partidos.forEach(partido => {
  const marker = L.marker([lat, lng], {
    icon: L.icon({
      iconUrl: partido.logo_url,
      iconSize: [30, 30]
    })
  });
});
```

---

## 5. Verificación de Logos

### 5.1 Consulta SQL

```sql
-- Ver estado de logos
SELECT 
    id,
    nombre,
    nombre_corto,
    CASE 
        WHEN logo_url IS NOT NULL THEN '✅ Con logo'
        ELSE '❌ Sin logo'
    END as estado_logo,
    logo_url
FROM partidos
WHERE activo = 1
ORDER BY nombre;
```

### 5.2 Script de Verificación

```python
import requests

def verificar_logos_partidos():
    """Verificar que todas las URLs de logos funcionan"""
    partidos = Partido.query.filter_by(activo=True).all()
    
    resultados = {
        'validos': [],
        'invalidos': [],
        'sin_logo': []
    }
    
    for partido in partidos:
        if partido.logo_url:
            try:
                response = requests.head(partido.logo_url, timeout=5)
                if response.status_code == 200:
                    resultados['validos'].append(partido.nombre)
                    print(f"✅ {partido.nombre}: Logo válido")
                else:
                    resultados['invalidos'].append({
                        'nombre': partido.nombre,
                        'url': partido.logo_url,
                        'status': response.status_code
                    })
                    print(f"❌ {partido.nombre}: Logo no accesible ({response.status_code})")
            except Exception as e:
                resultados['invalidos'].append({
                    'nombre': partido.nombre,
                    'url': partido.logo_url,
                    'error': str(e)
                })
                print(f"❌ {partido.nombre}: Error - {str(e)}")
        else:
            resultados['sin_logo'].append(partido.nombre)
            print(f"⚠️  {partido.nombre}: Sin logo")
    
    return resultados

# Ejecutar verificación
resultados = verificar_logos_partidos()
print(f"\n📊 Resumen:")
print(f"✅ Logos válidos: {len(resultados['validos'])}")
print(f"❌ Logos inválidos: {len(resultados['invalidos'])}")
print(f"⚠️  Sin logo: {len(resultados['sin_logo'])}")
```

---

## 6. Mejores Prácticas

### 6.1 Especificaciones de Imágenes

**Tamaño recomendado**:
- Ancho: 200px
- Alto: 200px
- Relación de aspecto: 1:1 (cuadrado)

**Formato**:
- PNG con fondo transparente (preferido)
- SVG (ideal para escalabilidad)
- JPG (solo si no hay transparencia)

**Peso**:
- Máximo: 100 KB
- Recomendado: 20-50 KB

### 6.2 URLs de Wikipedia

**Ventajas**:
- ✅ Estables y confiables
- ✅ No requieren almacenamiento local
- ✅ Imágenes optimizadas
- ✅ Actualizaciones automáticas

**Formato de URL**:
```
https://upload.wikimedia.org/wikipedia/commons/thumb/
[hash]/[nombre_archivo]/[tamaño]px-[nombre_archivo]
```

**Ejemplo**:
```
https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Colombian_Liberal_Party_logo.svg/200px-Colombian_Liberal_Party_logo.svg.png
```

### 6.3 Fallback (Sin Logo)

Si un partido no tiene logo, mostrar:

1. **Iniciales del partido**:
   ```html
   <div class="partido-sin-logo" style="background-color: ${partido.color}">
     ${partido.nombre_corto}
   </div>
   ```

2. **Icono genérico**:
   ```html
   <i class="bi bi-flag-fill" style="color: ${partido.color}"></i>
   ```

### 6.4 Cache

**En el navegador**:
```html
<img src="${partido.logo_url}" 
     alt="${partido.nombre}"
     loading="lazy"
     style="cache-control: max-age=86400">
```

**En el servidor** (si se usan logos locales):
```python
@app.route('/static/uploads/logos/<filename>')
def serve_logo(filename):
    response = send_file(f'static/uploads/logos/{filename}')
    response.cache_control.max_age = 86400  # 24 horas
    return response
```

---

## 7. Solución de Problemas

### Problema 1: Logo no se muestra

**Síntomas**:
- Imagen rota en el dashboard
- Alt text visible

**Causas posibles**:
1. URL incorrecta o rota
2. Problema de CORS
3. Imagen eliminada de Wikipedia

**Solución**:
```sql
-- Verificar URL
SELECT nombre, logo_url FROM partidos WHERE id = 1;

-- Probar URL en el navegador
-- Si no funciona, actualizar:
UPDATE partidos 
SET logo_url = 'nueva_url_valida'
WHERE id = 1;

-- O volver a cargar logos automáticamente
-- Hacer clic en "Cargar Logos" en el dashboard
```

### Problema 2: Logos no se cargan automáticamente

**Síntomas**:
- Botón "Cargar Logos" no hace nada
- Error en consola

**Solución**:
```javascript
// Verificar en consola del navegador
console.log('Verificando endpoint...');

// Probar manualmente
fetch('/api/admin/cargar-logos-partidos', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
  }
})
.then(r => r.json())
.then(data => console.log(data));
```

### Problema 3: Logo muy grande o muy pequeño

**Solución CSS**:
```css
.partido-logo {
  width: 40px;
  height: 40px;
  object-fit: contain;  /* Mantener proporción */
  border-radius: 4px;
}
```

---

## 8. Checklist

### Antes de Iniciar Elecciones

- [ ] Todos los partidos activos tienen logo
- [ ] Todas las URLs de logos funcionan
- [ ] Los logos se muestran correctamente en el dashboard
- [ ] Los logos se muestran en el formulario E-14
- [ ] Los logos tienen el tamaño correcto

### Verificación

```sql
-- Partidos sin logo
SELECT nombre FROM partidos 
WHERE activo = 1 AND logo_url IS NULL;

-- Debe retornar 0 filas
```

---

**Última actualización**: 30 de Noviembre de 2025  
**Versión**: 1.0
