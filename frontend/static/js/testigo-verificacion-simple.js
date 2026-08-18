/**
 * Verificación de presencia SIMPLE y ROBUSTA
 * Fail-closed: la presencia SOLO se marca si el API confirma el registro
 */

window.verificarPresenciaSimple = async function() {
    try {
        console.log('🔵 [SIMPLE] Iniciando verificación de presencia...');
        
        // 1. Verificar que haya una mesa seleccionada
        const selectorMesa = document.getElementById('mesa');
        if (!selectorMesa || !selectorMesa.value) {
            alert('Debe seleccionar una mesa primero');
            return;
        }
        
        const selectedOption = selectorMesa.options[selectorMesa.selectedIndex];
        if (!selectedOption || !selectedOption.dataset.mesa) {
            alert('Error al obtener datos de la mesa');
            return;
        }
        
        const mesaData = JSON.parse(selectedOption.dataset.mesa);
        console.log('📋 [SIMPLE] Mesa seleccionada:', mesaData);
        
        // 2. Llamar al API para registrar presencia (obligatorio)
        let response;
        try {
            response = await APIClient.post('/testigo/registrar-presencia', {
                mesa_id: mesaData.id
            });
            console.log('📡 [SIMPLE] Respuesta del API:', response);
        } catch (apiError) {
            console.error('❌ [SIMPLE] Error del API, presencia NO verificada:', apiError);
            if (window.Utils && window.Utils.showError) {
                Utils.showError('⚠️ Error al verificar presencia en el servidor. No se marcó la presencia.');
            } else {
                alert('⚠️ Error al verificar presencia en el servidor. No se marcó la presencia.');
            }
            return;
        }
        
        // Fail-closed: si el API no confirmó éxito, no continuar
        if (!response || !response.success) {
            const errorMsg = (response && response.error) || 'Error al verificar presencia';
            console.error('❌ [SIMPLE] API no confirmó, presencia NO verificada:', errorMsg);
            if (window.Utils && window.Utils.showError) {
                Utils.showError('⚠️ ' + errorMsg + '. No se marcó la presencia.');
            } else {
                alert('⚠️ ' + errorMsg + '. No se marcó la presencia.');
            }
            return;
        }
        
        // 3. Guardar en localStorage (solo después de confirmación del servidor)
        localStorage.setItem('presenciaVerificada', 'true');
        localStorage.setItem('mesaVerificadaId', mesaData.id.toString());
        localStorage.setItem('mesaVerificadaData', JSON.stringify(mesaData));
        
        console.log('💾 [SIMPLE] Datos guardados en localStorage');
        
        // 4. Actualizar variables globales
        window.presenciaVerificada = true;
        window.mesaSeleccionadaDashboard = mesaData;
        
        // 5. Actualizar UI
        const btnVerificar = document.getElementById('btnVerificarPresencia');
        const alertaVerificada = document.getElementById('alertaPresenciaVerificada');
        
        if (btnVerificar) btnVerificar.classList.add('d-none');
        if (alertaVerificada) {
            alertaVerificada.classList.remove('d-none');
            const fechaElement = document.getElementById('presenciaFecha');
            if (fechaElement) {
                const ahora = new Date();
                fechaElement.textContent = `Verificada el ${ahora.toLocaleDateString('es-CO')} a las ${ahora.toLocaleTimeString('es-CO')}`;
            }
        }
        
        // 6. Actualizar estado
        const statEstado = document.getElementById('statEstado');
        const statEstadoTexto = document.getElementById('statEstadoTexto');
        if (statEstado) {
            statEstado.innerHTML = '<i class="bi bi-check-circle-fill"></i>';
            statEstado.style.color = '#28a745';
        }
        if (statEstadoTexto) {
            statEstadoTexto.textContent = 'Verificado';
        }
        
        console.log('✅ [SIMPLE] Verificación completada exitosamente');
        
        if (window.Utils && window.Utils.showSuccess) {
            Utils.showSuccess('✅ Presencia verificada exitosamente');
        } else {
            alert('✅ Presencia verificada exitosamente');
        }
        
    } catch (error) {
        console.error('❌ [SIMPLE] Error en verificación:', error);
        if (window.Utils && window.Utils.showError) {
            Utils.showError('Error al verificar presencia: ' + error.message);
        } else {
            alert('Error al verificar presencia: ' + error.message);
        }
    }
};

console.log('✅ [SIMPLE] Script de verificación simple cargado');
console.log('💡 [SIMPLE] El botón "Verificar Mi Presencia" usa esta función (fail-closed)');