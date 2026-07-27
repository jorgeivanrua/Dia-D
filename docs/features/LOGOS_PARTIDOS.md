# 🎨 Logos de Partidos Políticos Colombianos

**Fecha:** 2025-11-26  
**Estado:** 📋 Documentado

---

## 📊 Logos Disponibles

Todos los logos provienen de **Wikimedia Commons** (dominio público o licencia libre):

### Partidos Principales:

1. **Partido Liberal Colombiano**
   - URL: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Colombian_Liberal_Party_logo.svg/200px-Colombian_Liberal_Party_logo.svg.png`
   - Sigla: LIBERAL, PL

2. **Partido Conservador Colombiano**
   - URL: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Colombian_Conservative_Party_logo.svg/200px-Colombian_Conservative_Party_logo.svg.png`
   - Sigla: CONSERVADOR, PC

3. **Centro Democrático**
   - URL: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Democratic_Center_%28Colombia%29_logo.svg/200px-Democratic_Center_%28Colombia%29_logo.svg.png`
   - Sigla: CD

4. **Pacto Histórico**
   - URL: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Logo_Pacto_Hist%C3%B3rico.svg/200px-Logo_Pacto_Hist%C3%B3rico.svg.png`
   - Sigla: PH

5. **Cambio Radical**
   - URL: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Radical_Change_logo.svg/200px-Radical_Change_logo.svg.png`
   - Sigla: CR

6. **Partido de la U (Partido Social de Unidad Nacional)**
   - URL: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Social_Party_of_National_Unity_logo.svg/200px-Social_Party_of_National_Unity_logo.svg.png`
   - Sigla: LA U, PSUN

7. **Alianza Verde**
   - URL: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Green_Alliance_%28Colombia%29_logo.svg/200px-Green_Alliance_%28Colombia%29_logo.svg.png`
   - Sigla: VERDE, AV

8. **Polo Democrático Alternativo**
   - URL: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Alternative_Democratic_Pole_logo.svg/200px-Alternative_Democratic_Pole_logo.svg.png`
   - Sigla: POLO, PDA

9. **MIRA (Movimiento Independiente de Renovación Absoluta)**
   - URL: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/MIRA_logo.svg/200px-MIRA_logo.svg.png`
   - Sigla: MIRA

10. **Comunes (antes FARC)**
    - URL: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Comunes_logo.svg/200px-Comunes_logo.svg.png`
    - Sigla: COMUNES

---

## 🔧 Cómo Actualizar los Logos en la BD

### Opción 1: Usando el Dashboard Super Admin

1. Ir a **Dashboard Super Admin** → **Configuración** → **Partidos**
2. Click en **Editar** (ícono lápiz) en cada partido
3. Pegar la URL del logo en el campo **Logo URL**
4. Guardar cambios

### Opción 2: Usando SQL Directo

Ejecutar el archivo `logos_update.sql` generado:

```bash
# En PostgreSQL
psql -U usuario -d nombre_bd -f logos_update.sql
```

O copiar y pegar los comandos SQL directamente en tu cliente de PostgreSQL.

### Opción 3: Usando el Script Python

```bash
# Activar entorno virtual
.venv\Scripts\activate

# Ejecutar script
python actualizar_logos_partidos.py
```

---

## 📝 Estructura del Campo en la BD

```python
class Partido(db.Model):
    # ...
    logo_url = db.Column(db.String(500))  # URL del logo
    # ...
```

**Formato esperado:**
- URL completa (http:// o https://)
- Preferiblemente PNG o SVG
- Tamaño recomendado: 200x200px o similar
- Debe ser accesible públicamente

---

## 🎨 Visualización en el Frontend

Los logos se muestran en:

1. **Dashboard Super Admin:**
   - Lista de partidos (30x30px)
   - Modal de edición (preview)

2. **Formulario E-14 (Testigos):**
   - Selector de partidos
   - Tabla de resultados

3. **Dashboards de Coordinadores:**
   - Gráficos de resultados
   - Tablas comparativas

---

## 📋 Ejemplo de Actualización Manual

```sql
-- Actualizar Partido Liberal
UPDATE partidos 
SET logo_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Colombian_Liberal_Party_logo.svg/200px-Colombian_Liberal_Party_logo.svg.png'
WHERE UPPER(nombre) LIKE '%LIBERAL%';

-- Actualizar Centro Democrático
UPDATE partidos 
SET logo_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Democratic_Center_%28Colombia%29_logo.svg/200px-Democratic_Center_%28Colombia%29_logo.svg.png'
WHERE UPPER(nombre) LIKE '%CENTRO%DEMOCR%';

-- Actualizar Cambio Radical
UPDATE partidos 
SET logo_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Radical_Change_logo.svg/200px-Radical_Change_logo.svg.png'
WHERE UPPER(nombre) LIKE '%CAMBIO%RADICAL%';
```

---

## ✅ Verificación

Para verificar que los logos se cargaron correctamente:

1. **En el Dashboard:**
   ```
   Dashboard Super Admin → Configuración → Partidos
   Verificar que aparezcan los logos junto a cada partido
   ```

2. **En la BD:**
   ```sql
   SELECT nombre, nombre_corto, logo_url 
   FROM partidos 
   WHERE logo_url IS NOT NULL;
   ```

3. **En el Frontend:**
   ```
   Abrir formulario E-14 como testigo
   Verificar que los logos aparezcan en el selector de partidos
   ```

---

## 📚 Recursos Adicionales

- **Wikimedia Commons:** https://commons.wikimedia.org/
- **Logos de partidos colombianos:** https://commons.wikimedia.org/wiki/Category:Political_party_logos_of_Colombia
- **Documentación del modelo:** `backend/models/configuracion_electoral.py`

---

## 🔄 Actualización Futura

Si se agregan nuevos partidos:

1. Buscar el logo en Wikimedia Commons
2. Copiar la URL de la imagen (preferir tamaño 200px)
3. Actualizar usando cualquiera de las 3 opciones mencionadas

---

**Archivos Relacionados:**
- `actualizar_logos_partidos.py` - Script Python completo
- `backend/scripts/actualizar_logos_partidos_simple.py` - Generador de SQL
- `logos_update.sql` - SQL generado para actualización
- `actualizar_logos.bat` - Script batch para Windows

---

**Desarrollado por:** Kiro AI  
**Última actualización:** 2025-11-26
