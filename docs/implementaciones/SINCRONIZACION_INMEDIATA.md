# 🔄 Sincronización Inmediata - Sistema Electoral

**Fecha:** 29 de Noviembre de 2025  
**Versión:** 2.0

---

## 📋 CARACTERÍSTICAS

### **Sincronización Inmediata**
✅ Los formularios se sincronizan inmediatamente al crearlos  
✅ Los incidentes se sincronizan inmediatamente al reportarlos  
✅ Los delitos se sincronizan inmediatamente al reportarlos  

### **Soporte Offline Completo**
✅ Funciona sin conexión a internet  
✅ Guarda datos localmente en IndexedDB  
✅ Sincroniza automáticamente al reconectar  
✅ Cola persistente con reintentos automáticos  

### **Gestión Inteligente**
✅ Detección automática de conexión/desconexión  
✅ Reintentos automáticos (máximo 3 intentos)  
✅ Notificaciones al usuario  
✅ Estado de sincronización visible  

---

## 🚀 IMPLEMENTACIÓN

### **1. Incluir el Script**

En `frontend/templates/testigo/dashboard.html`:

```html
{% block extra_js %}
<!-- Scripts base -->
<script src="{{ url_for('static', filename='js/api-client.js') }}"></script>
<script src="{{ url_for('static', filename='js/utils.js') }}"></script>

<!-- NUEVO: Sync Manager Mejorado -->
<script src="{{ url_for('static', filename='js/sync-manager-mejorado.js') }}"></script>

<!-- Scripts del dashboard -->
<script src="{{ url_for('static', filename='js/testigo-dashboard-v2.js') }}"></script>
{% endblock %}
```

### **2. Usar en Formularios**

```javascript
// Al crear un formulario E-14
async function crearFormulario() {
    const formulario = {
        mesa_id: mesaId,
        tipo_eleccion_id: tipoEleccionId,
        votos_partidos: votosPartidos,
        foto_acta: fotoActa,
        // ... más datos
    };
    
    try {
        // Sincronizar inmediatamente
        const result = await syncManagerMejorado.syncFormulario(formulario);
        
        if (result.success) {
            Utils.showSuccess('Formulario enviado exitosamente');
            // Actualizar UI
        } else if (result.offline) {
            Utils.showWarning('Sin conexión. Formulario guardado para sincronizar después.');
            // Actualizar UI mostrando estado "pendiente"
        } else {
            Utils.showError('Error enviando formulario: ' + result.error);
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error inesperado');
    }
}
```

### **3. Usar en Incidentes**

```javascript
// Al reportar un incidente
async function reportarIncidente() {
    const incidente = {
        tipo: tipoIncidente,
        descripcion: descripcion,
        severidad: severidad,
        evidencias: fotos,
        // ... más datos
    };
    
    try {
        const result = await syncManagerMejorado.syncIncidente(incidente);
        
        if (result.success) {
            Utils.showSuccess('Incidente reportado exitosamente');
        } else if (result.offline) {
            Utils.showWarning('Sin conexión. Incidente guardado para sincronizar después.');
        } else {
            Utils.showError('Error reportando incidente');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
```

### **4. Usar en Delitos**

```javascript
// Al reportar un delito
async function reportarDelito() {
    const delito = {
        tipo: tipoDelito,
        descripcion: descripcion,
        gravedad: gravedad,
        evidencias: fotos,
        // ... más datos
    };
    
    try {
        const result = await syncManagerMejorado.syncDelito(delito);
        
        if (result.success) {
            Utils.showSuccess('Delito reportado exitosamente');
        } else if (result.offline) {
            Utils.showWarning('Sin conexión. Delito guardado para sincronizar después.');
        } else {
            Utils.showError('Error reportando delito');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
```

---

## 📊 MONITOREO DE ESTADO

### **Obtener Estado de Sincronización**

```javascript
const status = syncManagerMejorado.getStatus();
console.log(status);
/*
{
    online: true,
    syncing: false,
    queueSize: 3,
    pendingItems: 2,
    failedItems: 1
}
*/
```

### **Mostrar Indicador en UI**

```javascript
// Actualizar indicador cada 5 segundos
setInterval(() => {
    const status = syncManagerMejorado.getStatus();
    
    // Actualizar badge
    const badge = document.getElementById('sync-badge');
    if (badge) {
        if (status.queueSize > 0) {
            badge.textContent = status.queueSize;
            badge.classList.remove('d-none');
        } else {
            badge.classList.add('d-none');
        }
    }
    
    // Actualizar icono de conexión
    const icon = document.getElementById('connection-icon');
    if (icon) {
        if (status.online) {
            icon.className = 'bi bi-wifi text-success';
        } else {
            icon.className = 'bi bi-wifi-off text-danger';
        }
    }
}, 5000);
```

### **HTML para Indicador**

```html
<!-- En el header del dashboard -->
<div class="d-flex align-items-center gap-2">
    <!-- Indicador de conexión -->
    <i id="connection-icon" class="bi bi-wifi text-success"></i>
    
    <!-- Badge de items pendientes -->
    <span class="position-relative">
        <i class="bi bi-cloud-upload"></i>
        <span id="sync-badge" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-warning d-none">
            0
        </span>
    </span>
</div>
```

---

## 🔔 LISTENERS DE EVENTOS

### **Escuchar Eventos de Sincronización**

```javascript
// Agregar listener
syncManagerMejorado.addListener((event, data) => {
    switch (event) {
        case 'online':
            console.log('✅ Conexión restaurada');
            // Actualizar UI
            break;
            
        case 'offline':
            console.log('❌ Sin conexión');
            // Actualizar UI
            break;
            
        case 'queueUpdated':
            console.log(`📋 Cola actualizada: ${data.size} items`);
            // Actualizar contador
            break;
            
        case 'syncCompleted':
            console.log(`✅ Sincronización completada:`, data);
            // Mostrar notificación
            if (data.success > 0) {
                Utils.showSuccess(`${data.success} registro(s) sincronizado(s)`);
            }
            break;
    }
});
```

---

## 🛠️ GESTIÓN DE COLA

### **Ver Items en Cola**

```javascript
const items = syncManagerMejorado.getQueueItems();
console.log('Items en cola:', items);

// Mostrar en UI
items.forEach(item => {
    console.log(`- ${item.type}: ${item.status} (${item.retries} reintentos)`);
});
```

### **Reintentar Items Fallidos**

```javascript
// Reintentar todos los items fallidos
await syncManagerMejorado.retryFailedItems();
```

### **Limpiar Items Fallidos**

```javascript
// Eliminar items que fallaron después de 3 intentos
await syncManagerMejorado.clearFailedItems();
```

### **Forzar Sincronización**

```javascript
// Procesar toda la cola manualmente
await syncManagerMejorado.processQueue();
```

---

## 🎨 EJEMPLO COMPLETO

### **Dashboard con Sincronización Inmediata**

```javascript
// Inicializar al cargar
document.addEventListener('DOMContentLoaded', async () => {
    // El sync manager se inicializa automáticamente
    
    // Agregar listener para actualizar UI
    syncManagerMejorado.addListener((event, data) => {
        actualizarIndicadorSync(event, data);
    });
    
    // Actualizar indicador inicial
    actualizarIndicadorSync();
    
    // Actualizar cada 5 segundos
    setInterval(actualizarIndicadorSync, 5000);
});

// Función para actualizar indicador
function actualizarIndicadorSync(event = null, data = null) {
    const status = syncManagerMejorado.getStatus();
    
    // Actualizar icono de conexión
    const connectionIcon = document.getElementById('connection-icon');
    if (connectionIcon) {
        if (status.online) {
            connectionIcon.className = 'bi bi-wifi text-success';
            connectionIcon.title = 'Conectado';
        } else {
            connectionIcon.className = 'bi bi-wifi-off text-danger';
            connectionIcon.title = 'Sin conexión';
        }
    }
    
    // Actualizar badge de pendientes
    const syncBadge = document.getElementById('sync-badge');
    if (syncBadge) {
        if (status.queueSize > 0) {
            syncBadge.textContent = status.queueSize;
            syncBadge.classList.remove('d-none');
            syncBadge.title = `${status.pendingItems} pendientes, ${status.failedItems} fallidos`;
        } else {
            syncBadge.classList.add('d-none');
        }
    }
    
    // Actualizar texto de estado
    const statusText = document.getElementById('sync-status-text');
    if (statusText) {
        if (status.syncing) {
            statusText.textContent = 'Sincronizando...';
        } else if (status.queueSize > 0) {
            statusText.textContent = `${status.queueSize} pendiente(s)`;
        } else {
            statusText.textContent = 'Todo sincronizado';
        }
    }
}

// Crear formulario con sincronización inmediata
async function crearFormularioE14() {
    const formulario = obtenerDatosFormulario();
    
    // Validar
    const validacion = ValidadorFormulario.validarE14(formulario);
    if (!validacion.valido) {
        Utils.showError(validacion.errores.join('<br>'));
        return;
    }
    
    // Mostrar loading
    Utils.showLoading('Enviando formulario...');
    
    try {
        // Sincronizar inmediatamente
        const result = await syncManagerMejorado.syncFormulario(formulario);
        
        Utils.hideLoading();
        
        if (result.success) {
            Utils.showSuccess('✅ Formulario enviado exitosamente');
            cerrarModal();
            recargarFormularios();
        } else if (result.offline) {
            Utils.showWarning('⏳ Sin conexión. Formulario guardado para sincronizar después.');
            cerrarModal();
            recargarFormularios();
        } else {
            Utils.showError('❌ Error: ' + result.error);
        }
    } catch (error) {
        Utils.hideLoading();
        console.error('Error:', error);
        Utils.showError('Error inesperado');
    }
}
```

---

## 📱 INDICADORES VISUALES

### **HTML Completo**

```html
<!-- Header con indicadores -->
<div class="dashboard-header">
    <div class="d-flex justify-content-between align-items-center">
        <div>
            <h2>Dashboard Testigo</h2>
        </div>
        <div class="d-flex align-items-center gap-3">
            <!-- Indicador de conexión -->
            <div class="d-flex align-items-center gap-2">
                <i id="connection-icon" class="bi bi-wifi text-success"></i>
                <small id="sync-status-text" class="text-muted">Todo sincronizado</small>
            </div>
            
            <!-- Botón de sincronización manual -->
            <button class="btn btn-sm btn-outline-primary" onclick="sincronizarManual()">
                <i class="bi bi-arrow-repeat"></i>
                <span class="position-relative">
                    Sincronizar
                    <span id="sync-badge" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-warning d-none">
                        0
                    </span>
                </span>
            </button>
            
            <!-- Botón de cerrar sesión -->
            <button class="btn btn-sm btn-outline-danger" onclick="logout()">
                <i class="bi bi-box-arrow-right"></i> Salir
            </button>
        </div>
    </div>
</div>
```

### **CSS para Indicadores**

```css
/* Animación para icono de sincronización */
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.syncing .bi-arrow-repeat {
    animation: spin 1s linear infinite;
}

/* Badge pulsante */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

#sync-badge {
    animation: pulse 2s ease-in-out infinite;
}

/* Indicador de conexión */
#connection-icon {
    font-size: 1.2rem;
}

#connection-icon.text-danger {
    animation: pulse 2s ease-in-out infinite;
}
```

---

## ✅ VENTAJAS

### **Para el Usuario:**
- ✅ Respuesta inmediata al crear formularios
- ✅ Funciona sin conexión
- ✅ No pierde datos
- ✅ Sabe cuándo está sincronizado
- ✅ Notificaciones claras

### **Para el Sistema:**
- ✅ Menor carga en el servidor
- ✅ Datos más actualizados
- ✅ Menos errores de sincronización
- ✅ Mejor experiencia offline
- ✅ Cola persistente

---

## 🔧 CONFIGURACIÓN

### **Ajustar Parámetros**

En `sync-manager-mejorado.js`:

```javascript
constructor() {
    // ...
    this.maxRetries = 3;        // Máximo de reintentos
    this.retryDelay = 5000;     // Delay entre reintentos (ms)
    // ...
}
```

---

## 📝 CONCLUSIÓN

El nuevo sistema de sincronización inmediata proporciona:

✅ **Sincronización instantánea** al crear formularios  
✅ **Soporte offline completo** con IndexedDB  
✅ **Sincronización automática** al reconectar  
✅ **Cola persistente** con reintentos  
✅ **Indicadores visuales** claros  
✅ **Notificaciones** al usuario  

El sistema ahora es **robusto, confiable y user-friendly** para todos los testigos. 🎯

---

**Documento creado por:** Sistema de Sincronización  
**Última actualización:** 29/11/2025  
**Versión:** 2.0  
**Estado:** ✅ COMPLETADO
