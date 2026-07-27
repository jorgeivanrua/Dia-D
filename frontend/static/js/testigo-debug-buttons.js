/**
 * Script de depuración para botones de testigo
 */

console.log('🔍 DEBUG: Script de depuración cargado');

// Esperar a que el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔍 DEBUG: DOM listo');
    
    setTimeout(() => {
        console.log('🔍 DEBUG: Verificando botones después de 1 segundo...');
        
        // Buscar todos los botones
        const todosLosBotones = document.querySelectorAll('button');
        console.log('🔍 DEBUG: Total de botones en la página:', todosLosBotones.length);
        
        // Buscar botón por ID
        const btnDesktop = document.getElementById('btnNuevoFormulario');
        const btnMobile = document.getElementById('btnNuevoFormularioMobile');
        
        console.log('🔍 DEBUG: btnNuevoFormulario:', btnDesktop);
        console.log('🔍 DEBUG: btnNuevoFormularioMobile:', btnMobile);
        
        // Buscar botones con onclick
        const botonesConOnclick = document.querySelectorAll('button[onclick*="showCreateForm"]');
        console.log('🔍 DEBUG: Botones con onclick showCreateForm:', botonesConOnclick.length);
        
        botonesConOnclick.forEach((btn, i) => {
            console.log(`🔍 DEBUG: Botón ${i}:`, {
                id: btn.id,
                className: btn.className,
                disabled: btn.disabled,
                textContent: btn.textContent.trim().substring(0, 50)
            });
        });
        
        // Verificar variables globales
        console.log('🔍 DEBUG: Variables globales:');
        console.log('  - window.presenciaVerificada:', window.presenciaVerificada);
        console.log('  - window.mesaSeleccionadaDashboard:', window.mesaSeleccionadaDashboard);
        console.log('  - localStorage presenciaVerificada:', localStorage.getItem('presenciaVerificada'));
        
    }, 1000);
});

// Función para habilitar botones manualmente desde consola
window.debugHabilitarBotones = function() {
    console.log('🔧 DEBUG: Habilitando botones manualmente...');
    
    const botones = document.querySelectorAll('button[onclick*="showCreateForm"]');
    console.log('🔧 DEBUG: Encontrados', botones.length, 'botones');
    
    botones.forEach((btn, i) => {
        btn.disabled = false;
        btn.classList.remove('disabled');
        btn.title = 'Crear nuevo formulario E-14';
        console.log(`🔧 DEBUG: Botón ${i} habilitado`);
    });
    
    console.log('✅ DEBUG: Botones habilitados');
};

console.log('💡 DEBUG: Puedes ejecutar window.debugHabilitarBotones() en la consola para habilitar los botones manualmente');
