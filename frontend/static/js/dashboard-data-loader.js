/**
 * Cargador de datos para dashboards con manejo de errores mejorado
 */

// Función auxiliar para cargar datos con reintentos
async function loadDataWithRetry(apiCall, maxRetries = 3, delay = 1000) {
    let lastError = null;
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            console.log(`[Data Loader] Intento ${attempt}/${maxRetries}...`);
            const response = await apiCall();
            
            if (response && response.success) {
                console.log('[Data Loader] ✓ Datos cargados exitosamente');
                return response;
            } else {
                lastError = new Error(response?.error || 'Respuesta no exitosa');
                console.warn(`[Data Loader] Intento ${attempt} falló:`, lastError.message);
            }
        } catch (error) {
            lastError = error;
            console.warn(`[Data Loader] Intento ${attempt} falló:`, error.message);
            
            // Si es error 401 o 403, no reintentar
            if (error.message && (error.message.includes('401') || error.message.includes('403') || error.message.includes('Sesión'))) {
                console.error('[Data Loader] Error de autenticación, no se reintentará');
                throw error;
            }
        }
        
        // Esperar antes del siguiente intento (excepto en el último)
        if (attempt < maxRetries) {
            await new Promise(resolve => setTimeout(resolve, delay * attempt));
        }
    }
    
    // Si llegamos aquí, todos los intentos fallaron
    console.error('[Data Loader] ✗ Todos los intentos fallaron');
    throw lastError || new Error('Error desconocido al cargar datos');
}

// Sobrescribir loadMainStats para Super Admin
window.loadMainStats = async function() {
    try {
        console.log('[Data Loader] Cargando estadísticas principales...');
        
        const response = await loadDataWithRetry(
            () => APIClient.get('/super-admin/stats'),
            3,
            1000
        );
            
        if (response && response.success && response.data) {
            const stats = response.data;
            console.log('[Data Loader] Estadísticas recibidas:', stats);
            
            // Actualizar UI de forma segura
            const updateElement = (id, value) => {
                const element = document.getElementById(id);
                if (element) {
                    element.textContent = value;
                } else {
                    console.warn(`[Data Loader] Elemento ${id} no encontrado`);
                }
            };
            
            updateElement('totalUsuarios', stats.totalUsuarios || 0);
            updateElement('usuariosChange', stats.usuariosChange >= 0 ? `+${stats.usuariosChange}` : stats.usuariosChange);
            updateElement('totalPuestos', stats.totalPuestos || 0);
            updateElement('totalMesas', stats.totalMesas || 0);
            updateElement('totalFormularios', stats.totalFormularios || 0);
            updateElement('formulariosPendientes', stats.formulariosPendientes || 0);
            updateElement('totalValidados', stats.totalValidados || 0);
            updateElement('porcentajeValidados', (stats.porcentajeValidados || 0).toFixed(1));
            
            console.log('[Data Loader] ✓ UI actualizada correctamente');
        } else {
            console.error('[Data Loader] Respuesta no válida:', response);
        }
    } catch (error) {
        console.error('[Data Loader] Error cargando estadísticas:', error);
        
        // Mostrar error al usuario
        if (typeof Utils !== 'undefined' && typeof Utils.showError === 'function') {
            Utils.showError('Error al cargar estadísticas del sistema');
        }
        
        // Si es error de autenticación, redirigir
        if (error.message && (error.message.includes('401') || error.message.includes('403') || error.message.includes('Sesión'))) {
            console.log('[Data Loader] Redirigiendo al login...');
            setTimeout(() => {
                window.location.href = '/auth/login';
            }, 2000);
        }
    }
};

// Forzar ejecución inmediata si ya existe initSuperAdminDashboard
if (typeof window.initSuperAdminDashboard === 'function') {
    console.log('[Data Loader] initSuperAdminDashboard ya existe, reemplazando...');
    const originalInit = window.initSuperAdminDashboard;
    window.initSuperAdminDashboard = async function() {
        console.log('[Data Loader] Ejecutando initSuperAdminDashboard mejorado...');
        await originalInit();
    };
}

// Función para cargar usuarios activos (Monitoreo)
window.loadUsuariosActivos = async function() {
    try {
        console.log('[Data Loader] Cargando usuarios activos...');
        
        const response = await loadDataWithRetry(
            () => APIClient.get('/monitoreo/usuarios-activos'),
            3,
            1000
        );
        
        if (response && response.success && response.data) {
            console.log('[Data Loader] ✓ Usuarios activos cargados:', response.data.length);
            return response.data;
        }
        
        return [];
    } catch (error) {
        console.error('[Data Loader] Error cargando usuarios activos:', error);
        
        if (typeof Utils !== 'undefined' && typeof Utils.showError === 'function') {
            Utils.showError('Error al cargar usuarios activos');
        }
        
        return [];
    }
};

// Función para cargar estadísticas (Monitoreo)
window.loadEstadisticasMonitoreo = async function() {
    try {
        console.log('[Data Loader] Cargando estadísticas de monitoreo...');
        
        const response = await loadDataWithRetry(
            () => APIClient.get('/monitoreo/estadisticas'),
            3,
            1000
        );
        
        if (response && response.success && response.data) {
            console.log('[Data Loader] ✓ Estadísticas de monitoreo cargadas');
            return response.data;
        }
        
        return null;
    } catch (error) {
        console.error('[Data Loader] Error cargando estadísticas de monitoreo:', error);
        
        if (typeof Utils !== 'undefined' && typeof Utils.showError === 'function') {
            Utils.showError('Error al cargar estadísticas de monitoreo');
        }
        
        return null;
    }
};

// Función para verificar conectividad con el backend
window.checkBackendConnection = async function() {
    try {
        console.log('[Data Loader] Verificando conexión con backend...');
        
        const response = await fetch('/api/auth/profile', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });
        
        if (response.ok) {
            console.log('[Data Loader] ✓ Backend conectado');
            return true;
        } else {
            console.warn('[Data Loader] Backend respondió con error:', response.status);
            return false;
        }
    } catch (error) {
        console.error('[Data Loader] ✗ No se pudo conectar con el backend:', error);
        return false;
    }
};

// Verificar conexión al cargar
setTimeout(async () => {
    const connected = await window.checkBackendConnection();
    if (!connected) {
        console.error('[Data Loader] ⚠️ Problemas de conectividad detectados');
        if (typeof Utils !== 'undefined' && typeof Utils.showWarning === 'function') {
            Utils.showWarning('Problemas de conexión con el servidor. Algunos datos pueden no cargarse correctamente.');
        }
    }
}, 2000);

console.log('[Data Loader] ✓ Cargador de datos inicializado');
