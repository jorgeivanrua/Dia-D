/**
 * Script simple para habilitar botones de formulario E-14
 * Este script se ejecuta después de verificar presencia
 */

// Función global para habilitar botones
window.habilitarBotonesFormulario = function() {
    console.log('🔧 [ENABLE] Habilitando botones de formulario...');
    
    // Buscar botones por ID
    const btnDesktop = document.getElementById('btnNuevoFormulario');
    const btnMobile = document.getElementById('btnNuevoFormularioMobile');
    
    let habilitados = 0;
    
    if (btnDesktop) {
        btnDesktop.disabled = false;
        btnDesktop.classList.remove('disabled');
        btnDesktop.title = 'Crear nuevo formulario E-14';
        habilitados++;
        console.log('  ✅ Botón desktop habilitado');
    } else {
        console.error('  ❌ Botón desktop NO encontrado');
    }
    
    if (btnMobile) {
        btnMobile.disabled = false;
        btnMobile.classList.remove('disabled');
        btnMobile.title = 'Crear nuevo formulario E-14';
        habilitados++;
        console.log('  ✅ Botón móvil habilitado');
    }
    
    console.log(`✅ [ENABLE] ${habilitados} botón(es) habilitado(s)`);
    return habilitados;
};

// Verificar periódicamente si se verificó presencia y habilitar botones
setInterval(function() {
    const presenciaVerificada = localStorage.getItem('presenciaVerificada') === 'true';
    
    if (presenciaVerificada) {
        const btnDesktop = document.getElementById('btnNuevoFormulario');
        const btnMobile = document.getElementById('btnNuevoFormularioMobile');
        
        // Si algún botón está deshabilitado, habilitarlo
        if ((btnDesktop && btnDesktop.disabled) || (btnMobile && btnMobile.disabled)) {
            console.log('🔔 [ENABLE] Detectado presencia verificada, habilitando botones...');
            window.habilitarBotonesFormulario();
        }
    }
}, 500); // Verificar cada 500ms

console.log('✅ [ENABLE] Script de habilitación de botones cargado');
console.log('💡 [ENABLE] Puedes ejecutar window.habilitarBotonesFormulario() manualmente');
