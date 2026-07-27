/**
 * Script de debugging para Coordinador Dashboard (Puesto, Municipal, Departamental)
 */

console.log('[Coordinador Debug] Script cargado');

// Verificar dependencias
if (typeof APIClient === 'undefined') {
    console.error('[Coordinador Debug] ❌ APIClient no está definido');
} else {
    console.log('[Coordinador Debug] ✓ APIClient disponible');
}

const token = localStorage.getItem('access_token');
if (!token) {
    console.error('[Coordinador Debug] ❌ No hay token de acceso');
} else {
    console.log('[Coordinador Debug] ✓ Token encontrado');
}

// Función de prueba completa
window.testCoordinadorDashboard = async function() {
    console.log('[Coordinador Debug] === INICIANDO PRUEBA COMPLETA ===');
    
    try {
        // 1. Verificar perfil
        console.log('[Coordinador Debug] 1. Verificando perfil...');
        const profileResponse = await APIClient.getProfile();
        console.log('[Coordinador Debug] Perfil:', profileResponse);
        
        if (!profileResponse.success) {
            console.error('[Coordinador Debug] ❌ Error en perfil:', profileResponse.error);
            return;
        }
        
        const user = profileResponse.data.user;
        const ubicacion = profileResponse.data.ubicacion;
        console.log('[Coordinador Debug] Usuario:', user.nombre, '- Rol:', user.rol);
        console.log('[Coordinador Debug] Ubicación:', ubicacion);
        
        const rolesCoordinador = ['coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental'];
        if (!rolesCoordinador.includes(user.rol)) {
            console.error('[Coordinador Debug] ❌ Usuario no es coordinador');
            return;
        }
        
        // 2. Determinar tipo de coordinador
        let tipoCoordinador = 'desconocido';
        if (user.rol === 'coordinador_puesto') tipoCoordinador = 'puesto';
        else if (user.rol === 'coordinador_municipal') tipoCoordinador = 'municipal';
        else if (user.rol === 'coordinador_departamental') tipoCoordinador = 'departamental';
        
        console.log('[Coordinador Debug] Tipo de coordinador:', tipoCoordinador);
        
        // 3. Cargar formularios según el tipo
        console.log('[Coordinador Debug] 2. Cargando formularios...');
        try {
            let formsResponse;
            
            if (tipoCoordinador === 'puesto') {
                formsResponse = await APIClient.getFormulariosPuesto();
            } else if (tipoCoordinador === 'municipal') {
                formsResponse = await APIClient.get('/coordinador-municipal/formularios');
            } else if (tipoCoordinador === 'departamental') {
                formsResponse = await APIClient.get('/coordinador-departamental/formularios');
            }
            
            console.log('[Coordinador Debug] Formularios:', formsResponse);
            
            if (formsResponse && formsResponse.success) {
                const formularios = formsResponse.data || [];
                console.log('[Coordinador Debug] ✓ Formularios:', formularios.length);
                
                // Contar por estado
                const porEstado = {};
                formularios.forEach(f => {
                    porEstado[f.estado] = (porEstado[f.estado] || 0) + 1;
                });
                
                console.log('[Coordinador Debug] Distribución por estado:');
                Object.entries(porEstado).forEach(([estado, count]) => {
                    console.log(`[Coordinador Debug]   - ${estado}: ${count}`);
                });
            } else {
                console.warn('[Coordinador Debug] ⚠️ No se pudieron cargar formularios');
            }
        } catch (error) {
            console.error('[Coordinador Debug] ❌ Error cargando formularios:', error.message);
        }
        
        // 4. Verificar estadísticas
        console.log('[Coordinador Debug] 3. Verificando estadísticas en UI...');
        const statsElements = {
            'totalFormularios': document.getElementById('totalFormularios'),
            'formulariosPendientes': document.getElementById('formulariosPendientes'),
            'formulariosValidados': document.getElementById('formulariosValidados'),
            'totalTestigos': document.getElementById('totalTestigos')
        };
        
        Object.entries(statsElements).forEach(([id, element]) => {
            if (element) {
                console.log(`[Coordinador Debug]   ✓ ${id}: ${element.textContent}`);
            } else {
                console.warn(`[Coordinador Debug]   ⚠️ ${id} no encontrado`);
            }
        });
        
        // 5. Verificar tabla de formularios
        console.log('[Coordinador Debug] 4. Verificando tabla de formularios...');
        const tablaFormularios = document.getElementById('formsTable') || document.querySelector('table');
        if (tablaFormularios) {
            const filas = tablaFormularios.querySelectorAll('tbody tr');
            console.log('[Coordinador Debug] ✓ Tabla encontrada con', filas.length, 'filas');
        } else {
            console.warn('[Coordinador Debug] ⚠️ Tabla de formularios no encontrada');
        }
        
        // 6. Verificar funciones de validación
        console.log('[Coordinador Debug] 5. Verificando funciones...');
        console.log('[Coordinador Debug]   validarFormulario:', typeof window.validarFormulario);
        console.log('[Coordinador Debug]   rechazarFormulario:', typeof window.rechazarFormulario);
        console.log('[Coordinador Debug]   verDetalleFormulario:', typeof window.verDetalleFormulario);
        
        // 7. Verificar mesas (para coordinador de puesto)
        if (tipoCoordinador === 'puesto') {
            console.log('[Coordinador Debug] 6. Verificando mesas del puesto...');
            const panelMesas = document.getElementById('panelMesas');
            if (panelMesas) {
                console.log('[Coordinador Debug] ✓ Panel de mesas encontrado');
            } else {
                console.warn('[Coordinador Debug] ⚠️ Panel de mesas no encontrado');
            }
        }
        
        console.log('[Coordinador Debug] === PRUEBA COMPLETADA ===');
        
    } catch (error) {
        console.error('[Coordinador Debug] ❌ Error en prueba:', error);
        console.error('[Coordinador Debug] Stack:', error.stack);
    }
};

// Ejecutar automáticamente
setTimeout(() => {
    console.log('[Coordinador Debug] Ejecutando prueba automática...');
    window.testCoordinadorDashboard();
}, 2000);

console.log('[Coordinador Debug] Para ejecutar manualmente: testCoordinadorDashboard()');
