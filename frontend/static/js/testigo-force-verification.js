/**
 * Script para forzar la verificación de presencia manualmente
 */

window.forzarVerificacionPresencia = function() {
    console.log('🔧 [FORCE] Forzando verificación de presencia...');
    
    // Obtener mesa seleccionada
    const selectorMesa = document.getElementById('mesa');
    if (!selectorMesa || !selectorMesa.value) {
        console.error('❌ No hay mesa seleccionada');
        alert('Primero selecciona una mesa');
        return;
    }
    
    const selectedOption = selectorMesa.options[selectorMesa.selectedIndex];
    if (!selectedOption || !selectedOption.dataset.mesa) {
        console.error('❌ No se pudo obtener datos de la mesa');
        return;
    }
    
    const mesaData = JSON.parse(selectedOption.dataset.mesa);
    console.log('📋 Mesa seleccionada:', mesaData);
    
    // Guardar en localStorage DIRECTAMENTE
    localStorage.setItem('presenciaVerificada', 'true');
    localStorage.setItem('mesaVerificadaId', mesaData.id);
    localStorage.setItem('mesaVerificadaData', JSON.stringify(mesaData));
    
    // Actualizar variables globales
    window.presenciaVerificada = true;
    window.mesaSeleccionadaDashboard = mesaData;
    
    console.log('✅ [FORCE] Datos guardados en localStorage:');
    console.log('  - presenciaVerificada:', localStorage.getItem('presenciaVerificada'));
    console.log('  - mesaVerificadaId:', localStorage.getItem('mesaVerificadaId'));
    console.log('  - mesaVerificadaData:', localStorage.getItem('mesaVerificadaData'));
    
    // Actualizar UI
    const btnVerificar = document.getElementById('btnVerificarPresencia');
    const alertaVerificada = document.getElementById('alertaPresenciaVerificada');
    
    if (btnVerificar) btnVerificar.classList.add('d-none');
    if (alertaVerificada) alertaVerificada.classList.remove('d-none');
    
    // Actualizar estado
    const statEstado = document.getElementById('statEstado');
    const statEstadoTexto = document.getElementById('statEstadoTexto');
    if (statEstado) {
        statEstado.innerHTML = '<i class="bi bi-check-circle-fill"></i>';
        statEstado.style.color = '#28a745';
    }
    if (statEstadoTexto) {
        statEstadoTexto.textContent = 'Verificado';
    }
    
    // Habilitar botones
    if (window.habilitarBotonesFormulario) {
        window.habilitarBotonesFormulario();
    }
    
    alert('✅ Presencia verificada manualmente');
    console.log('✅ [FORCE] Verificación completada');
};

console.log('✅ [FORCE] Script de verificación forzada cargado');
console.log('💡 [FORCE] Ejecuta: window.forzarVerificacionPresencia()');
