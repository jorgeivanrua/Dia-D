/**
 * Script de debugging para Monitoreo Dashboard
 */

console.log('[Monitoreo Debug] Script cargado');

// Verificar dependencias
if (typeof APIClient === 'undefined') {
    console.error('[Monitoreo Debug] ❌ APIClient no está definido');
} else {
    console.log('[Monitoreo Debug] ✓ APIClient disponible');
}

const token = localStorage.getItem('access_token');
if (!token) {
    console.error('[Monitoreo Debug] ❌ No hay token de acceso');
} else {
    console.log('[Monitoreo Debug] ✓ Token encontrado');
}

// Función de prueba completa
window.testMonitoreoDashboard = async function() {
    console.log('[Monitoreo Debug] === INICIANDO PRUEBA COMPLETA ===');
    
    try {
        // 1. Verificar perfil
        console.log('[Monitoreo Debug] 1. Verificando perfil...');
        const profileResponse = await APIClient.getProfile();
        console.log('[Monitoreo Debug] Perfil:', profileResponse);
        
        if (!profileResponse.success) {
            console.error('[Monitoreo Debug] ❌ Error en perfil:', profileResponse.error);
            return;
        }
        
        const user = profileResponse.data.user;
        console.log('[Monitoreo Debug] Usuario:', user.nombre, '- Rol:', user.rol);
        
        if (user.rol !== 'monitoreo') {
            console.error('[Monitoreo Debug] ❌ Usuario no es monitoreo');
            return;
        }
        
        // 2. Cargar usuarios activos
        console.log('[Monitoreo Debug] 2. Cargando usuarios activos...');
        try {
            const usuariosResponse = await APIClient.get('/monitoreo/usuarios-activos');
            console.log('[Monitoreo Debug] Usuarios activos:', usuariosResponse);
            
            if (usuariosResponse && usuariosResponse.success) {
                const usuarios = usuariosResponse.data || [];
                console.log('[Monitoreo Debug] ✓ Usuarios activos:', usuarios.length);
                
                // Contar por rol
                const porRol = {};
                usuarios.forEach(u => {
                    porRol[u.rol] = (porRol[u.rol] || 0) + 1;
                });
                
                console.log('[Monitoreo Debug] Distribución por rol:');
                Object.entries(porRol).forEach(([rol, count]) => {
                    console.log(`[Monitoreo Debug]   - ${rol}: ${count}`);
                });
                
                // Usuarios con geolocalización
                const conGeo = usuarios.filter(u => u.latitud && u.longitud).length;
                console.log('[Monitoreo Debug] Con geolocalización:', conGeo);
            } else {
                console.warn('[Monitoreo Debug] ⚠️ No se pudieron cargar usuarios activos');
            }
        } catch (error) {
            console.error('[Monitoreo Debug] ❌ Error cargando usuarios:', error.message);
        }
        
        // 3. Cargar estadísticas
        console.log('[Monitoreo Debug] 3. Cargando estadísticas...');
        try {
            const statsResponse = await APIClient.get('/monitoreo/estadisticas');
            console.log('[Monitoreo Debug] Estadísticas:', statsResponse);
            
            if (statsResponse && statsResponse.success && statsResponse.data) {
                const stats = statsResponse.data;
                console.log('[Monitoreo Debug] ✓ Estadísticas recibidas:');
                console.log('[Monitoreo Debug]   Testigos:');
                console.log('[Monitoreo Debug]     - Total:', stats.testigos?.total);
                console.log('[Monitoreo Debug]     - Con geo:', stats.testigos?.con_geolocalizacion);
                console.log('[Monitoreo Debug]     - Con presencia:', stats.testigos?.con_presencia);
                console.log('[Monitoreo Debug]   Coordinadores:');
                console.log('[Monitoreo Debug]     - Total:', stats.coordinadores?.total);
                console.log('[Monitoreo Debug]   Formularios:');
                console.log('[Monitoreo Debug]     - Total:', stats.formularios?.total);
                console.log('[Monitoreo Debug]     - Validados:', stats.formularios?.validados);
                console.log('[Monitoreo Debug]     - Pendientes:', stats.formularios?.pendientes);
            } else {
                console.warn('[Monitoreo Debug] ⚠️ No se pudieron cargar estadísticas');
            }
        } catch (error) {
            console.error('[Monitoreo Debug] ❌ Error cargando estadísticas:', error.message);
        }
        
        // 4. Verificar mapa
        console.log('[Monitoreo Debug] 4. Verificando mapa...');
        const mapaElement = document.getElementById('mapa-monitoreo');
        if (mapaElement) {
            console.log('[Monitoreo Debug] ✓ Elemento de mapa encontrado');
        } else {
            console.warn('[Monitoreo Debug] ⚠️ Elemento de mapa no encontrado');
        }
        
        if (typeof window.mapa !== 'undefined') {
            console.log('[Monitoreo Debug] ✓ Mapa Leaflet inicializado');
        } else {
            console.warn('[Monitoreo Debug] ⚠️ Mapa Leaflet no inicializado');
        }
        
        // 5. Verificar métricas de rendimiento
        console.log('[Monitoreo Debug] 5. Cargando métricas de rendimiento...');
        try {
            const metricasResponse = await APIClient.get('/monitoreo/metricas-rendimiento');
            console.log('[Monitoreo Debug] Métricas:', metricasResponse);
            
            if (metricasResponse && metricasResponse.success) {
                console.log('[Monitoreo Debug] ✓ Métricas cargadas');
            }
        } catch (error) {
            console.warn('[Monitoreo Debug] ⚠️ Error cargando métricas:', error.message);
        }
        
        // 6. Verificar filtros
        console.log('[Monitoreo Debug] 6. Verificando filtros...');
        const filtrosElement = document.querySelector('.filtros');
        if (filtrosElement) {
            console.log('[Monitoreo Debug] ✓ Sección de filtros encontrada');
        } else {
            console.warn('[Monitoreo Debug] ⚠️ Sección de filtros no encontrada');
        }
        
        console.log('[Monitoreo Debug] === PRUEBA COMPLETADA ===');
        
    } catch (error) {
        console.error('[Monitoreo Debug] ❌ Error en prueba:', error);
        console.error('[Monitoreo Debug] Stack:', error.stack);
    }
};

// Ejecutar automáticamente
setTimeout(() => {
    console.log('[Monitoreo Debug] Ejecutando prueba automática...');
    window.testMonitoreoDashboard();
}, 2000);

console.log('[Monitoreo Debug] Para ejecutar manualmente: testMonitoreoDashboard()');
