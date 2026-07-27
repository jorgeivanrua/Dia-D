# 🔧 Solución: Problema de Sesión al Tomar Foto

## 🐛 Problema Identificado

Cuando el testigo toma una foto del formulario E-14, la aplicación se cierra o pierde la sesión, obligando al usuario a volver a hacer login.

### Causas Identificadas:

1. **Atributo `capture="environment"`** - Puede causar que algunos navegadores móviles pierdan el contexto de la aplicación
2. **Falta de persistencia de sesión** - El token JWT no se está guardando correctamente
3. **Timeout de sesión** - La sesión expira mientras el usuario toma la foto
4. **Navegador cierra la pestaña** - Al abrir la cámara nativa, algunos navegadores cierran la pestaña web

---

## ✅ Soluciones Implementadas

### Solución 1: Mejorar el Input de Cámara

**Archivo:** `frontend/templates/testigo/dashboard.html`

**Cambio en línea 410:**

```html
<!-- ANTES (Problemático) -->
<input type="file" class="form-control d-none" id="imagen" name="imagen" accept="image/*" capture="environment">

<!-- DESPUÉS (Mejorado) -->
<input type="file" class="form-control d-none" id="imagen" name="imagen" accept="image/*">
```

**Razón:** Eliminar `capture="environment"` permite que el usuario elija entre cámara o galería, reduciendo problemas de contexto.

### Solución 2: Guardar Estado Antes de Abrir Cámara

**Archivo:** `frontend/static/js/testigo-dashboard-[version].js`

**Agregar antes de abrir la cámara:**

```javascript
// Guardar estado del formulario antes de abrir cámara
function guardarEstadoFormulario() {
    const formData = {
        mesa_id: document.getElementById('mesa_id')?.value,
        tipo_eleccion_id: document.getElementById('tipo_eleccion_id')?.value,
        votantes_registrados: document.getElementById('votantes_registrados')?.value,
        total_votos: document.getElementById('total_votos')?.value,
        votos_validos: document.getElementById('votos_validos')?.value,
        votos_nulos: document.getElementById('votos_nulos')?.value,
        votos_blanco: document.getElementById('votos_blanco')?.value,
        tarjetas_no_marcadas: document.getElementById('tarjetas_no_marcadas')?.value,
        observaciones: document.getElementById('observaciones')?.value,
        votosData: votosData,
        timestamp: Date.now()
    };
    
    localStorage.setItem('formulario_e14_temp', JSON.stringify(formData));
    console.log('Estado del formulario guardado');
}

// Restaurar estado del formulario
function restaurarEstadoFormulario() {
    const savedData = localStorage.getItem('formulario_e14_temp');
    if (savedData) {
        try {
            const formData = JSON.parse(savedData);
            
            // Verificar que no sea muy antiguo (más de 1 hora)
            if (Date.now() - formData.timestamp < 3600000) {
                // Restaurar campos
                if (formData.mesa_id) document.getElementById('mesa_id').value = formData.mesa_id;
                if (formData.tipo_eleccion_id) document.getElementById('tipo_eleccion_id').value = formData.tipo_eleccion_id;
                if (formData.votantes_registrados) document.getElementById('votantes_registrados').value = formData.votantes_registrados;
                if (formData.total_votos) document.getElementById('total_votos').value = formData.total_votos;
                if (formData.votos_validos) document.getElementById('votos_validos').value = formData.votos_validos;
                if (formData.votos_nulos) document.getElementById('votos_nulos').value = formData.votos_nulos;
                if (formData.votos_blanco) document.getElementById('votos_blanco').value = formData.votos_blanco;
                if (formData.tarjetas_no_marcadas) document.getElementById('tarjetas_no_marcadas').value = formData.tarjetas_no_marcadas;
                if (formData.observaciones) document.getElementById('observaciones').value = formData.observaciones;
                if (formData.votosData) votosData = formData.votosData;
                
                console.log('Estado del formulario restaurado');
            }
            
            // Limpiar después de restaurar
            localStorage.removeItem('formulario_e14_temp');
        } catch (error) {
            console.error('Error al restaurar formulario:', error);
        }
    }
}

// Modificar setupImagePreview para guardar estado
function setupImagePreview() {
    const input = document.getElementById('imagen');
    const preview = document.getElementById('imagePreview');
    
    if (!input || !preview) return;
    
    input.addEventListener('change', function() {
        // Guardar estado antes de procesar imagen
        guardarEstadoFormulario();
        
        const file = this.files[0];
        if (file) {
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.innerHTML = `<img src="${e.target.result}" alt="Preview" style="max-width: 100%; max-height: 250px;">`;
                };
                reader.onerror = function() {
                    preview.innerHTML = '<p class="text-danger">Error al cargar la imagen</p>';
                };
                reader.readAsDataURL(file);
            } else {
                preview.innerHTML = '<p class="text-danger">Por favor seleccione una imagen válida</p>';
            }
        } else {
            preview.innerHTML = '<p class="text-muted">Toque el botón para tomar una foto</p>';
        }
    });
}
```

### Solución 3: Extender Tiempo de Sesión

**Archivo:** `backend/config.py`

**Agregar/Modificar:**

```python
# JWT Configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)  # Aumentar de 1 hora a 8 horas
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
```

### Solución 4: Renovar Token Automáticamente

**Archivo:** `frontend/static/js/api-client.js`

**Agregar:**

```javascript
// Renovar token automáticamente cada 30 minutos
setInterval(async () => {
    try {
        const token = localStorage.getItem('token');
        if (token) {
            // Hacer una petición simple para mantener la sesión activa
            await APIClient.getProfile();
            console.log('Sesión renovada automáticamente');
        }
    } catch (error) {
        console.error('Error al renovar sesión:', error);
    }
}, 30 * 60 * 1000); // Cada 30 minutos
```

### Solución 5: Detectar Pérdida de Sesión y Restaurar

**Archivo:** `frontend/static/js/testigo-dashboard-[version].js`

**Agregar al inicio:**

```javascript
// Detectar cuando la página vuelve a estar visible
document.addEventListener('visibilitychange', function() {
    if (!document.hidden) {
        console.log('Página visible nuevamente');
        
        // Verificar si hay sesión activa
        const token = localStorage.getItem('token');
        if (!token) {
            console.warn('Sesión perdida, redirigiendo a login');
            window.location.href = '/login';
            return;
        }
        
        // Restaurar estado del formulario si existe
        restaurarEstadoFormulario();
        
        // Recargar datos
        if (typeof loadFormularios === 'function') {
            loadFormularios();
        }
    }
});

// Guardar estado antes de que la página se oculte
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        console.log('Página oculta, guardando estado');
        guardarEstadoFormulario();
    }
});
```

### Solución 6: Botón Alternativo con Mejor UX

**Archivo:** `frontend/templates/testigo/dashboard.html`

**Mejorar el botón de captura:**

```html
<div class="mb-3">
    <label class="form-label">Foto del Formulario E-14 *</label>
    <input type="file" class="form-control d-none" id="imagen" name="imagen" accept="image/*">
    
    <div class="d-grid gap-2">
        <button type="button" class="btn btn-primary btn-lg" onclick="abrirCamara()">
            <i class="bi bi-camera-fill"></i> Tomar Foto del Formulario
        </button>
        <button type="button" class="btn btn-outline-secondary" onclick="document.getElementById('imagen').click()">
            <i class="bi bi-image"></i> Seleccionar desde Galería
        </button>
    </div>
    
    <div id="imagePreview" class="image-preview mt-3">
        <p class="text-muted">Toque un botón para agregar la foto</p>
    </div>
    
    <small class="text-muted">
        <i class="bi bi-info-circle"></i> 
        Asegúrese de que la foto sea clara y legible
    </small>
</div>
```

**JavaScript para el botón:**

```javascript
function abrirCamara() {
    // Guardar estado antes de abrir cámara
    guardarEstadoFormulario();
    
    // Abrir input de archivo
    const input = document.getElementById('imagen');
    if (input) {
        // En móviles, esto abrirá la cámara
        input.click();
    }
}
```

---

## 🚀 Implementación Rápida

### Paso 1: Actualizar el Input de Imagen

En `frontend/templates/testigo/dashboard.html`, buscar la línea 410 y cambiar:

```html
<!-- Cambiar esto -->
<input type="file" class="form-control d-none" id="imagen" name="imagen" accept="image/*" capture="environment">

<!-- Por esto -->
<input type="file" class="form-control d-none" id="imagen" name="imagen" accept="image/*">
```

### Paso 2: Agregar Funciones de Guardado

En el archivo JavaScript del testigo (el que esté activo), agregar las funciones `guardarEstadoFormulario()` y `restaurarEstadoFormulario()` al inicio del archivo.

### Paso 3: Modificar setupImagePreview

Buscar la función `setupImagePreview()` y agregar `guardarEstadoFormulario()` al inicio del event listener de 'change'.

### Paso 4: Agregar Event Listeners de Visibilidad

Agregar los event listeners de `visibilitychange` al final del archivo JavaScript.

### Paso 5: Aumentar Tiempo de Sesión

En `backend/config.py`, cambiar:

```python
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)  # Era 1 hora
```

---

## 🧪 Testing

### Probar en Móvil:

1. **Login como testigo**
2. **Abrir formulario E-14**
3. **Llenar algunos campos**
4. **Hacer clic en "Tomar Foto"**
5. **Tomar la foto**
6. **Verificar que:**
   - La sesión sigue activa
   - Los campos llenados se mantienen
   - La foto se carga correctamente

### Escenarios a Probar:

- ✅ Tomar foto con cámara
- ✅ Seleccionar foto de galería
- ✅ Cancelar la captura
- ✅ Tomar múltiples fotos
- ✅ Cambiar de app y volver
- ✅ Esperar 5 minutos y volver

---

## 📊 Mejoras Adicionales

### Opción 1: Usar PWA (Progressive Web App)

Convertir la aplicación en PWA para mejor manejo de la cámara:

```html
<!-- En base.html, agregar en <head> -->
<link rel="manifest" href="/static/manifest.json">
<meta name="theme-color" content="#2563eb">
```

### Opción 2: Comprimir Imágenes Antes de Enviar

```javascript
function comprimirImagen(file, maxWidth = 1920, quality = 0.8) {
    return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                let width = img.width;
                let height = img.height;
                
                if (width > maxWidth) {
                    height = (height * maxWidth) / width;
                    width = maxWidth;
                }
                
                canvas.width = width;
                canvas.height = height;
                
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);
                
                canvas.toBlob((blob) => {
                    resolve(new File([blob], file.name, {
                        type: 'image/jpeg',
                        lastModified: Date.now()
                    }));
                }, 'image/jpeg', quality);
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    });
}
```

### Opción 3: Mostrar Indicador de Guardado

```javascript
function mostrarIndicadorGuardado() {
    const indicator = document.createElement('div');
    indicator.className = 'toast toast-success show';
    indicator.textContent = '💾 Formulario guardado temporalmente';
    document.body.appendChild(indicator);
    
    setTimeout(() => {
        indicator.classList.remove('show');
        setTimeout(() => indicator.remove(), 300);
    }, 2000);
}
```

---

## ✅ Checklist de Implementación

- [ ] Eliminar `capture="environment"` del input
- [ ] Agregar función `guardarEstadoFormulario()`
- [ ] Agregar función `restaurarEstadoFormulario()`
- [ ] Modificar `setupImagePreview()` para guardar estado
- [ ] Agregar event listeners de `visibilitychange`
- [ ] Aumentar tiempo de sesión JWT a 8 horas
- [ ] Agregar renovación automática de token
- [ ] Probar en dispositivo móvil real
- [ ] Probar en diferentes navegadores
- [ ] Documentar para usuarios

---

## 🎯 Resultado Esperado

Después de implementar estas soluciones:

✅ **La sesión NO se pierde** al tomar fotos
✅ **Los datos del formulario se preservan** automáticamente
✅ **Mejor experiencia de usuario** con opciones claras
✅ **Funciona en todos los navegadores** móviles
✅ **Sesión dura 8 horas** en lugar de 1 hora

---

**Prioridad:** 🔴 ALTA - Afecta funcionalidad crítica en campo
**Tiempo de implementación:** 30-45 minutos
**Impacto:** Soluciona problema bloqueante para testigos
