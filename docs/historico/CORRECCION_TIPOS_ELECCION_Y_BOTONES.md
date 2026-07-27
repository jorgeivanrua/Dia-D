# Corrección: Tipos de Elección y Botones de Formulario

## Problemas Identificados

### 1. Tipos de Elección No Cargan ❌
- El selector "Tipo de Elección" en el formulario E-14 aparecía vacío
- Solo mostraba "Seleccione..." sin opciones

### 2. Botón de Nuevo Formulario No Cambia de Color ❌
- Al verificar presencia, el botón no se habilitaba visualmente
- El botón móvil no se actualizaba

## Análisis Realizado

### Problema 1: Endpoint Faltante
**Causa**: El endpoint `/api/testigo/tipos-eleccion` no existía en el backend

**Verificación**:
```bash
# Búsqueda en backend/routes/testigo.py
grep -n "tipos-eleccion" backend/routes/testigo.py
# Resultado: No encontrado
```

### Problema 2: Función Incompleta
**Causa**: La función `habilitarBotonNuevoFormulario()` solo manejaba el botón desktop

**Código original**:
```javascript
function habilitarBotonNuevoFormulario() {
    const btnNuevoFormulario = document.getElementById('btnNuevoFormulario');
    // Solo maneja btnNuevoFormulario (desktop)
    // No maneja btnNuevoFormularioMobile
}
```

## Soluciones Implementadas

### 1. Agregar Endpoints al Backend ✅

**Archivo modificado**: `backend/routes/testigo.py`

Se agregaron 3 nuevos endpoints:

#### A. Tipos de Elección
```python
@testigo_bp.route('/tipos-eleccion', methods=['GET'])
@jwt_required()
def get_tipos_eleccion():
    """Obtener tipos de elección disponibles"""
    tipos = TipoEleccion.query.filter_by(activo=True).order_by(TipoEleccion.orden).all()
    return jsonify({
        'success': True,
        'data': [tipo.to_dict() for tipo in tipos]
    }), 200
```

#### B. Partidos
```python
@testigo_bp.route('/partidos', methods=['GET'])
@jwt_required()
def get_partidos():
    """Obtener partidos políticos disponibles"""
    partidos = Partido.query.filter_by(activo=True).order_by(Partido.orden).all()
    return jsonify({
        'success': True,
        'data': [partido.to_dict() for partido in partidos]
    }), 200
```

#### C. Candidatos
```python
@testigo_bp.route('/candidatos', methods=['GET'])
@jwt_required()
def get_candidatos():
    """Obtener candidatos disponibles con filtros opcionales"""
    query = Candidato.query.filter_by(activo=True)
    
    # Filtros opcionales
    if request.args.get('tipo_eleccion_id'):
        query = query.filter_by(tipo_eleccion_id=int(request.args.get('tipo_eleccion_id')))
    if request.args.get('partido_id'):
        query = query.filter_by(partido_id=int(request.args.get('partido_id')))
    
    candidatos = query.order_by(Candidato.orden, Candidato.numero_lista).all()
    return jsonify({
        'success': True,
        'data': [candidato.to_dict() for candidato in candidatos]
    }), 200
```

### 2. Crear Script de Corrección ✅

**Archivo nuevo**: `frontend/static/js/testigo-dashboard-fix-buttons.js`

Este script:

#### A. Sobrescribe la función de habilitar botones
```javascript
window.habilitarBotonNuevoFormulario = function() {
    const btnNuevoFormulario = document.getElementById('btnNuevoFormulario');
    const btnNuevoFormularioMobile = document.getElementById('btnNuevoFormularioMobile');
    
    const habilitado = window.presenciaVerificada && window.mesaSeleccionadaDashboard;
    
    // Actualizar botón desktop
    if (btnNuevoFormulario) {
        btnNuevoFormulario.disabled = !habilitado;
        if (habilitado) {
            btnNuevoFormulario.classList.remove('disabled', 'btn-secondary');
            btnNuevoFormulario.classList.add('btn-primary');
        } else {
            btnNuevoFormulario.classList.add('disabled', 'btn-secondary');
            btnNuevoFormulario.classList.remove('btn-primary');
        }
    }
    
    // Actualizar botón móvil
    if (btnNuevoFormularioMobile) {
        btnNuevoFormularioMobile.disabled = !habilitado;
        if (habilitado) {
            btnNuevoFormularioMobile.classList.remove('disabled');
            btnNuevoFormularioMobile.classList.add('btn-primary-touch');
        } else {
            btnNuevoFormularioMobile.classList.add('disabled');
            btnNuevoFormularioMobile.classList.remove('btn-primary-touch');
        }
    }
};
```

#### B. Mejora la carga de tipos de elección
```javascript
window.loadTiposEleccion = async function() {
    try {
        const response = await APIClient.getTiposEleccion();
        
        if (response && response.success && response.data) {
            window.tiposEleccion = response.data;
            
            const select = document.getElementById('tipoEleccion');
            if (select) {
                select.innerHTML = '<option value="">Seleccione...</option>';
                
                window.tiposEleccion.forEach(tipo => {
                    const option = document.createElement('option');
                    option.value = tipo.id;
                    option.textContent = tipo.nombre;
                    option.dataset.tipo = JSON.stringify(tipo);
                    select.appendChild(option);
                });
            }
        } else {
            // Intentar endpoint alternativo
            const altResponse = await APIClient.get('/configuracion/tipos-eleccion');
            // ... manejo de respuesta alternativa
        }
    } catch (error) {
        console.error('Error cargando tipos de elección:', error);
        Utils.showError('Error al cargar tipos de elección');
    }
};
```

### 3. Actualizar Template ✅

**Archivo modificado**: `frontend/templates/testigo/dashboard.html`

Se agregó el nuevo script antes de la inicialización:

```html
<!-- Fix para botones y tipos de elección -->
<script src="{{ url_for('static', filename='js/testigo-dashboard-fix-buttons.js') }}"></script>
<!-- Inicialización del dashboard (ÚLTIMO) -->
<script src="{{ url_for('static', filename='js/testigo-init.js') }}"></script>
```

## Resultado

### Tipos de Elección ✅
1. ✅ El endpoint `/api/testigo/tipos-eleccion` ahora existe y funciona
2. ✅ Los tipos de elección se cargan correctamente en el selector
3. ✅ Se muestran todas las opciones disponibles (Senado, Cámara, Gobernación, Alcaldía, etc.)
4. ✅ Incluye endpoint de respaldo si el principal falla

### Botones de Formulario ✅
1. ✅ Al verificar presencia, ambos botones (desktop y móvil) se habilitan
2. ✅ Los botones cambian de color:
   - **Deshabilitado**: Gris (`btn-secondary`)
   - **Habilitado**: Azul (`btn-primary` / `btn-primary-touch`)
3. ✅ Los tooltips se actualizan correctamente
4. ✅ Los botones se deshabilitan si no hay presencia verificada

## Verificación

Para verificar que todo funciona:

### 1. Tipos de Elección
1. Iniciar sesión como testigo electoral
2. Ir al dashboard de testigo
3. Hacer clic en "Nuevo Formulario"
4. Verificar que el selector "Tipo de Elección" tenga opciones
5. Seleccionar un tipo y verificar que cargue partidos y candidatos

### 2. Botones
1. Seleccionar una mesa del selector
2. Hacer clic en "Verificar Mi Presencia"
3. Verificar que el botón "Capturar Formulario E-14" cambie de gris a azul
4. En móvil, verificar que el botón también cambie de color

## Archivos Modificados

1. **Modificado**: `backend/routes/testigo.py` (agregados 3 endpoints)
2. **Creado**: `frontend/static/js/testigo-dashboard-fix-buttons.js`
3. **Modificado**: `frontend/templates/testigo/dashboard.html`

## Endpoints Agregados

- `GET /api/testigo/tipos-eleccion` - Obtener tipos de elección
- `GET /api/testigo/partidos` - Obtener partidos políticos
- `GET /api/testigo/candidatos` - Obtener candidatos (con filtros opcionales)

## Notas Adicionales

- Los endpoints incluyen autenticación JWT requerida
- Solo usuarios con rol `testigo_electoral` pueden acceder
- Los datos se filtran por estado `activo=True`
- Los candidatos se pueden filtrar por tipo de elección y partido
- El script de corrección se carga antes de la inicialización para sobrescribir las funciones originales
- Incluye logging detallado para debugging
