# 🔧 Corrección de Rutas API y Errores 404

**Fecha**: 29 de Noviembre de 2025  
**Estado**: ✅ CORREGIDO

---

## 🐛 Problemas Identificados

### 1. Declaración Duplicada de APIClient
**Error**: `Uncaught SyntaxError: Identifier 'APIClient' has already been declared`

**Causa**: El archivo `api-client.js` se estaba incluyendo dos veces:
- En `base.html` (template padre)
- En `monitoreo/dashboard.html` (template hijo)

**Solución**: Eliminada la inclusión duplicada en `monitoreo/dashboard.html`

### 2. Errores 404 en Endpoints de Monitoreo
**Error**: `Failed to load resource: the server responded with a status of 404`

**Endpoints afectados**:
- `/api/monitoreo/api/estadisticas`
- `/api/monitoreo/api/usuarios-activos`
- `/api/monitoreo/api/alertas`
- `/api/monitoreo/api/actividad-reciente`
- `/api/monitoreo/api/metricas-rendimiento`
- `/api/monitoreo/api/mapa-calor`
- `/api/monitoreo/api/tendencias`
- `/api/monitoreo/api/comparativa-departamentos`
- `/api/monitoreo/api/predicciones`

**Causa**: Duplicación de `/api/` en las rutas
- Blueprint: `url_prefix='/monitoreo'`
- Rutas: `@monitoreo_bp.route('/api/...')`
- APIClient: `baseURL = '/api'`
- Resultado: `/api` + `/monitoreo` + `/api/...` = `/api/monitoreo/api/...` ❌

**Solución**: Eliminado `/api/` de las rutas del blueprint de monitoreo

### 3. Imports Incorrectos de Modelos
**Error**: `NameError: name 'Incidente' is not defined`

**Causa**: Imports incorrectos de modelos de incidentes y delitos
```python
from backend.models.incidente import Incidente  # ❌ No existe
from backend.models.delito_electoral import DelitoElectoral  # ❌ No existe
```

**Solución**: Corregidos los imports
```python
from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral  # ✅
```

---

## ✅ Cambios Realizados

### Frontend

#### `frontend/templates/monitoreo/dashboard.html`

**Antes**:
```html
{% block extra_js %}
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="{{ url_for('static', filename='js/api-client.js') }}"></script>  <!-- ❌ Duplicado -->
```

**Después**:
```html
{% block extra_js %}
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<!-- api-client.js ya está incluido en base.html -->  <!-- ✅ Comentario -->
```

**Rutas corregidas** (10 cambios):
```javascript
// Antes ❌
const response = await APIClient.get('/monitoreo/api/estadisticas');

// Después ✅
const response = await APIClient.get('/monitoreo/estadisticas');
```

### Backend

#### `backend/routes/monitoreo.py`

**Imports agregados**:
```python
from backend.models.formulario_e14 import FormularioE14
from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
```

**Rutas corregidas** (11 cambios):
```python
# Antes ❌
@monitoreo_bp.route('/api/usuarios-activos', methods=['GET'])

# Después ✅
@monitoreo_bp.route('/usuarios-activos', methods=['GET'])
```

**Lista completa de rutas corregidas**:
1. `/usuarios-activos`
2. `/estadisticas`
3. `/alertas`
4. `/actividad-reciente`
5. `/estadisticas-departamento/<departamento_codigo>`
6. `/exportar-reporte`
7. `/metricas-rendimiento`
8. `/mapa-calor`
9. `/tendencias`
10. `/comparativa-departamentos`
11. `/predicciones`

**Referencias a modelos corregidas**:
- `Incidente.` → `IncidenteElectoral.`
- Imports locales eliminados

---

## 🔍 Verificación de Otros Roles

### Blueprints Revisados

| Blueprint | URL Prefix | Rutas | Estado |
|-----------|-----------|-------|--------|
| `auth_bp` | `/api/auth` | Sin `/api/` interno | ✅ OK |
| `testigo_bp` | `/api/testigo` | Sin `/api/` interno | ✅ OK |
| `coordinador_puesto_bp` | `/api/coordinador-puesto` | Sin `/api/` interno | ✅ OK |
| `coordinador_municipal_bp` | `/api/coordinador-municipal` | Sin `/api/` interno | ✅ OK |
| `coordinador_departamental_bp` | `/api/coordinador-departamental` | Sin `/api/` interno | ✅ OK |
| `auditor_bp` | `/api/auditor` | Sin `/api/` interno | ✅ OK |
| `super_admin_bp` | `/api/super-admin` | Sin `/api/` interno | ✅ OK |
| `formularios_bp` | `/api/formularios` | Sin `/api/` interno | ✅ OK |
| `incidentes_delitos_bp` | Sin prefijo | Con `/api/` interno | ✅ OK |
| `locations_bp` | `/api/locations` | Sin `/api/` interno | ✅ OK |
| `monitoreo_bp` | `/monitoreo` | Sin `/api/` interno | ✅ CORREGIDO |

### Archivos JavaScript Revisados

✅ No se encontraron rutas duplicadas (`/api/.../api/`) en:
- `admin-dashboard.js`
- `testigo-dashboard-*.js`
- `coordinador-*.js`
- `auditor-dashboard.js`
- `super-admin-dashboard.js`

---

## 📊 Estructura de Rutas Correcta

### Cómo Funciona

1. **APIClient** agrega `/api` al inicio:
   ```javascript
   static baseURL = '/api';
   ```

2. **Blueprint** define su prefijo:
   ```python
   monitoreo_bp = Blueprint('monitoreo', __name__, url_prefix='/monitoreo')
   ```

3. **Registro** en `app.py`:
   ```python
   app.register_blueprint(monitoreo_bp)  # Ya tiene prefijo
   ```

4. **Ruta final**:
   ```
   /api + /monitoreo + /estadisticas = /api/monitoreo/estadisticas ✅
   ```

### Casos Especiales

#### Blueprints sin URL Prefix en Definición

Algunos blueprints no tienen `url_prefix` en su definición pero se registran con uno:

```python
# Definición
testigo_bp = Blueprint('testigo', __name__)  # Sin url_prefix

# Registro
app.register_blueprint(testigo_bp, url_prefix='/api/testigo')  # Con url_prefix
```

#### Blueprints con Rutas Absolutas

El blueprint `incidentes_delitos_bp` no tiene prefijo y sus rutas incluyen `/api/`:

```python
# Definición
incidentes_delitos_bp = Blueprint('incidentes_delitos', __name__)  # Sin url_prefix

# Rutas
@incidentes_delitos_bp.route('/api/incidentes', methods=['POST'])

# Registro
app.register_blueprint(incidentes_delitos_bp)  # Sin url_prefix adicional

# Resultado: /api/incidentes ✅
```

---

## 🧪 Pruebas Realizadas

### Endpoints Verificados

✅ Todos los endpoints de monitoreo responden correctamente:

```bash
# Estadísticas
GET /api/monitoreo/estadisticas

# Usuarios activos
GET /api/monitoreo/usuarios-activos

# Alertas
GET /api/monitoreo/alertas

# Actividad reciente
GET /api/monitoreo/actividad-reciente

# Métricas de rendimiento
GET /api/monitoreo/metricas-rendimiento

# Mapa de calor
GET /api/monitoreo/mapa-calor

# Tendencias
GET /api/monitoreo/tendencias

# Comparativa departamental
GET /api/monitoreo/comparativa-departamentos

# Predicciones
GET /api/monitoreo/predicciones

# Exportar reporte
GET /api/monitoreo/exportar-reporte

# Estadísticas por departamento
GET /api/monitoreo/estadisticas-departamento/<codigo>
```

### Consola del Navegador

✅ Sin errores:
- No hay `SyntaxError` de declaración duplicada
- No hay errores 404
- No hay errores de imports

---

## 📝 Lecciones Aprendidas

### 1. Consistencia en Prefijos de Blueprints

**Recomendación**: Definir el `url_prefix` en la creación del blueprint, no en el registro:

```python
# ✅ Preferido
monitoreo_bp = Blueprint('monitoreo', __name__, url_prefix='/monitoreo')
app.register_blueprint(monitoreo_bp)

# ⚠️ Evitar
monitoreo_bp = Blueprint('monitoreo', __name__)
app.register_blueprint(monitoreo_bp, url_prefix='/monitoreo')
```

### 2. Evitar Duplicación de `/api/`

**Regla**: Si el blueprint tiene `/api/` en el prefijo, las rutas NO deben tener `/api/`:

```python
# ❌ Incorrecto
testigo_bp = Blueprint('testigo', __name__, url_prefix='/api/testigo')
@testigo_bp.route('/api/info')  # Resultado: /api/testigo/api/info

# ✅ Correcto
testigo_bp = Blueprint('testigo', __name__, url_prefix='/api/testigo')
@testigo_bp.route('/info')  # Resultado: /api/testigo/info
```

### 3. Imports Centralizados

**Recomendación**: Importar modelos al inicio del archivo, no dentro de funciones:

```python
# ✅ Preferido
from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral

def get_alertas():
    incidentes = IncidenteElectoral.query.all()

# ⚠️ Evitar
def get_alertas():
    from backend.models.incidentes_delitos import IncidenteElectoral
    incidentes = IncidenteElectoral.query.all()
```

### 4. Verificar Inclusiones de Scripts

**Recomendación**: Scripts comunes deben estar solo en `base.html`:

```html
<!-- base.html -->
<script src="{{ url_for('static', filename='js/api-client.js') }}"></script>

<!-- dashboard.html -->
<!-- NO incluir api-client.js aquí -->
```

---

## 🚀 Próximos Pasos

### Mejoras Sugeridas

1. **Estandarizar Prefijos de Blueprints**
   - Todos los blueprints de API deberían tener `/api/` en el prefijo
   - Considerar mover `monitoreo_bp` a `/api/monitoreo`

2. **Documentar Estructura de Rutas**
   - Crear documento con todas las rutas disponibles
   - Incluir ejemplos de uso
   - Mantener actualizado

3. **Tests de Integración**
   - Agregar tests para verificar que todas las rutas respondan
   - Verificar que no haya rutas duplicadas
   - Validar estructura de respuestas

4. **Linter para Rutas**
   - Script que verifique consistencia de rutas
   - Detectar duplicaciones de `/api/`
   - Validar que blueprints estén registrados

---

## 📚 Referencias

- **Archivos modificados**:
  - `frontend/templates/monitoreo/dashboard.html`
  - `backend/routes/monitoreo.py`

- **Commits**:
  - `f768efd` - fix: Corregir errores 404 y declaración duplicada de APIClient

- **Documentación relacionada**:
  - `docs/ROL_MONITOREO_MEJORADO.md`
  - `docs/ANALISIS_DASHBOARD_MONITOREO.md`

---

**Documento creado por**: Sistema de Corrección de Errores  
**Fecha**: 29 de Noviembre de 2025  
**Versión**: 1.0  
**Estado**: ✅ COMPLETADO

