# 🔧 Corrección de Errores del Dashboard de Testigo

## Errores Identificados

Basándome en la imagen proporcionada, los errores son:

1. **Error en "Resumen de Candidatos"** - Elemento no encontrado
2. **Problemas al cargar el dashboard** - Variables undefined
3. **Botón "Nuevo Formulario" no se habilita** - Lógica de verificación de presencia

## Soluciones Aplicadas

### 1. Eliminar Referencia a "Resumen de Candidatos"

El HTML no tiene un elemento con ID `resumenCandidatos`, pero el JavaScript intenta acceder a él.

**Archivo:** `frontend/static/js/testigo-dashboard-v2.js`

Buscar y eliminar o comentar cualquier referencia a:
```javascript
document.getElementById('resumenCandidatos')
```

### 2. Verificar Variables Globales

Asegurarse de que todas las variables estén inicializadas:

```javascript
let currentUser = null;
let userLocation = null;
let selectedMesa = null;
let mesaSeleccionadaDashboard = null;
let presenciaVerificada = false;
let tiposEleccion = [];
let partidosData = [];
let candidatosData = [];
let votosData = {};
let formularios = []; // ← AGREGAR ESTA
```

### 3. Corregir Función `showCreateForm()`

La función intenta acceder a `formularios` que no está definida globalmente.

**Cambio necesario:**

```javascript
async function showCreateForm() {
    try {
        // ... código existente ...
        
        // Obtener formularios para verificar mesas disponibles
        let formulariosExistentes = [];
        try {
            const response = await APIClient.getFormulariosE14({});
            formulariosExistentes = response.success ? (response.data.formularios || response.data || []) : [];
        } catch (error) {
            console.warn('No se pudieron cargar formularios:', error);
        }
        
        // Obtener mesas que ya tienen formularios
        const mesasConFormularios = new Set();
        formulariosExistentes.forEach(form => {
            if (form.estado !== 'rechazado') {
                mesasConFormularios.add(form.mesa_id);
            }
        });
        
        // ... resto del código ...
    } catch (error) {
        console.error('Error al abrir formulario:', error);
        Utils.showError('Error al abrir formulario: ' + error.message);
    }
}
```

### 4. Simplificar Habilitación del Botón

**Archivo:** `frontend/static/js/testigo-dashboard-v2.js`

```javascript
function habilitarBotonNuevoFormulario() {
    const btnNuevoFormulario = document.getElementById('btnNuevoFormulario');
    
    if (!btnNuevoFormulario) {
        console.error('Botón btnNuevoFormulario no encontrado');
        return;
    }
    
    console.log('Verificando condiciones para habilitar botón:');
    console.log('- presenciaVerificada:', presenciaVerificada);
    console.log('- mesaSeleccionadaDashboard:', mesaSeleccionadaDashboard);
    
    if (presenciaVerificada && mesaSeleccionadaDashboard) {
        btnNuevoFormulario.disabled = false;
        btnNuevoFormulario.classList.remove('disabled');
        btnNuevoFormulario.title = 'Crear nuevo formulario E-14';
        console.log('✅ Botón habilitado');
    } else {
        btnNuevoFormulario.disabled = true;
        btnNuevoFormulario.classList.add('disabled');
        btnNuevoFormulario.title = 'Debe seleccionar una mesa y verificar presencia primero';
        console.log('❌ Botón deshabilitado');
    }
}
```

## Archivo de Parche Completo

Crear archivo: `frontend/static/js/testigo-dashboard-fix.js`

```javascript
/**
 * Parche para corregir errores del dashboard de testigo
 * Incluir DESPUÉS de testigo-dashboard-v2.js
 */

// Sobrescribir función problemática
const originalShowCreateForm = window.showCreateForm;
window.showCreateForm = async function() {
    try {
        console.log('=== ABRIENDO FORMULARIO E-14 (VERSIÓN CORREGIDA) ===');
        
        // Verificar presencia
        if (!window.presenciaVerificada && !presenciaVerificada) {
            Utils.showError('Debe verificar su presencia primero');
            return;
        }
        
        // Limpiar formulario
        const form = document.getElementById('e14Form');
        if (form) form.reset();
        
        window.votosData = {};
        
        // Limpiar preview
        const imagePreview = document.getElementById('imagePreview');
        if (imagePreview) {
            imagePreview.innerHTML = '<p class="text-muted">Toque el botón para tomar una foto</p>';
        }
        
        // Habilitar selectores
        const tipoEleccionSelect = document.getElementById('tipoEleccion');
        if (tipoEleccionSelect) tipoEleccionSelect.disabled = false;
        
        // Cargar mesas
        const mesaSelect = document.getElementById('mesaFormulario');
        if (mesaSelect && (window.userLocation || userLocation)) {
            const location = window.userLocation || userLocation;
            
            const params = {
                puesto_codigo: location.puesto_codigo,
                zona_codigo: location.zona_codigo,
                municipio_codigo: location.municipio_codigo,
                departamento_codigo: location.departamento_codigo
            };
            
            const response = await APIClient.get('/locations/mesas', params);
            const mesas = response.data || [];
            
            mesaSelect.innerHTML = '<option value="">Seleccione una mesa...</option>';
            
            mesas.forEach(mesa => {
                const option = document.createElement('option');
                option.value = mesa.id;
                option.textContent = `Mesa ${mesa.mesa_codigo} - ${mesa.puesto_nombre || ''} (${mesa.total_votantes_registrados || 0} votantes)`;
                option.dataset.mesa = JSON.stringify(mesa);
                
                // Pre-seleccionar mesa actual
                const mesaActual = window.mesaSeleccionadaDashboard || mesaSeleccionadaDashboard;
                if (mesaActual && mesa.id === mesaActual.id) {
                    option.selected = true;
                }
                
                mesaSelect.appendChild(option);
            });
            
            mesaSelect.disabled = false;
            
            // Cargar votantes si hay mesa seleccionada
            if (mesaSelect.value) {
                await cambiarMesaFormulario();
            }
        }
        
        // Mostrar modal
        const modalElement = document.getElementById('formModal');
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
            
            modalElement.addEventListener('shown.bs.modal', function() {
                if (typeof setupImagePreview === 'function') {
                    setupImagePreview();
                }
            }, { once: true });
        }
        
    } catch (error) {
        console.error('Error al abrir formulario:', error);
        Utils.showError('Error al abrir formulario: ' + error.message);
    }
};

// Asegurar que las variables globales existan
if (typeof formularios === 'undefined') {
    window.formularios = [];
}

console.log('✅ Parche de testigo aplicado');
```

## Cómo Aplicar el Parche

### Opción 1: Incluir el archivo de parche

En `frontend/templates/testigo/dashboard.html`, agregar al final de `{% block extra_js %}`:

```html
{% block extra_js %}
<script src="{{ url_for('static', filename='js/incidentes-delitos.js') }}"></script>
<script src="{{ url_for('static', filename='js/testigo-dashboard-v2.js') }}"></script>
<script src="{{ url_for('static', filename='js/testigo-presencia-simple.js') }}"></script>
<script src="{{ url_for('static', filename='js/testigo-dashboard-fix.js') }}"></script>
{% endblock %}
```

### Opción 2: Corregir directamente el archivo principal

Editar `frontend/static/js/testigo-dashboard-v2.js` y aplicar los cambios mencionados arriba.

## Verificación

Después de aplicar los cambios:

1. Recargar la página del testigo
2. Abrir consola del navegador (F12)
3. Verificar que no haya errores rojos
4. Probar:
   - Seleccionar mesa
   - Verificar presencia
   - Botón "Nuevo Formulario" debe habilitarse
   - Abrir formulario sin errores

## Errores Comunes Resueltos

✅ `Cannot read property 'textContent' of null` - Elemento resumenCandidatos eliminado
✅ `formularios is not defined` - Variable inicializada globalmente  
✅ `Cannot read property 'id' of undefined` - Validaciones agregadas
✅ Botón no se habilita - Lógica simplificada y corregida

---

**Fecha:** Noviembre 2025
**Estado:** Pendiente de aplicar
