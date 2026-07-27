/**
 * Script de debugging para Super Admin Dashboard
 */

console.log('[Super Admin Debug] Script cargado');

// Verificar que APIClient existe
if (typeof APIClient === 'undefined') {
    console.error('[Super Admin Debug] ❌ APIClient no está definido');
} else {
    console.log('[Super Admin Debug] ✓ APIClient disponible');
}

// Verificar token
const token = localStorage.getItem('access_token');
if (!token) {
    console.error('[Super Admin Debug] ❌ No hay token de acceso');
} else {
    console.log('[Super Admin Debug] ✓ Token encontrado:', token.substring(0, 20) + '...');
}

// Función de prueba para cargar stats
window.testLoadStats = async function() {
    console.log('[Super Admin Debug] === INICIANDO PRUEBA DE CARGA ===');
    
    try {
        console.log('[Super Admin Debug] 1. Verificando perfil...');
        const profileResponse = await APIClient.getProfile();
        console.log('[Super Admin Debug] Perfil:', profileResponse);
        
        if (!profileResponse.success) {
            console.error('[Super Admin Debug] ❌ Error en perfil:', profileResponse.error);
            return;
        }
        
        const user = profileResponse.data.user;
        console.log('[Super Admin Debug] Usuario:', user.nombre, '- Rol:', user.rol);
        
        if (user.rol !== 'super_admin') {
            console.error('[Super Admin Debug] ❌ Usuario no es super_admin');
            return;
        }
        
        console.log('[Super Admin Debug] 2. Cargando estadísticas...');
        const statsResponse = await APIClient.get('/super-admin/stats');
        console.log('[Super Admin Debug] Respuesta stats:', statsResponse);
        
        if (!statsResponse.success) {
            console.error('[Super Admin Debug] ❌ Error en stats:', statsResponse.error);
            return;
        }
        
        const stats = statsResponse.data;
        console.log('[Super Admin Debug] ✓ Estadísticas recibidas:');
        console.log('  - Total Usuarios:', stats.totalUsuarios);
        console.log('  - Total Puestos:', stats.totalPuestos);
        console.log('  - Total Mesas:', stats.totalMesas);
        console.log('  - Total Formularios:', stats.totalFormularios);
        console.log('  - Formularios Pendientes:', stats.formulariosPendientes);
        console.log('  - Total Validados:', stats.totalValidados);
        console.log('  - Porcentaje Validados:', stats.porcentajeValidados);
        
        console.log('[Super Admin Debug] 3. Actualizando UI...');
        
        // Actualizar elementos
        const elementos = {
            'totalUsuarios': stats.totalUsuarios,
            'totalPuestos': stats.totalPuestos,
            'totalMesas': stats.totalMesas,
            'totalFormularios': stats.totalFormularios,
            'formulariosPendientes': stats.formulariosPendientes,
            'totalValidados': stats.totalValidados,
            'porcentajeValidados': stats.porcentajeValidados
        };
        
        for (const [id, valor] of Object.entries(elementos)) {
            const elemento = document.getElementById(id);
            if (elemento) {
                elemento.textContent = valor;
                console.log(`[Super Admin Debug]   ✓ ${id} = ${valor}`);
            } else {
                console.warn(`[Super Admin Debug]   ⚠️ Elemento ${id} no encontrado`);
            }
        }
        
        console.log('[Super Admin Debug] === PRUEBA COMPLETADA EXITOSAMENTE ===');
        
    } catch (error) {
        console.error('[Super Admin Debug] ❌ Error en prueba:', error);
        console.error('[Super Admin Debug] Stack:', error.stack);
    }
};

// Ejecutar prueba automáticamente después de 2 segundos
setTimeout(() => {
    console.log('[Super Admin Debug] Ejecutando prueba automática...');
    window.testLoadStats();
}, 2000);

// También exponer función para ejecución manual
console.log('[Super Admin Debug] Para ejecutar manualmente: testLoadStats()');
