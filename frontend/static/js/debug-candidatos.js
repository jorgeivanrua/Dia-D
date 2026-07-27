/**
 * Script de debug para verificar el estado de candidatos
 */

setTimeout(() => {
    console.log('=== DEBUG CANDIDATOS ===');

    // Verificar que el elemento existe
    const candidatosLista = document.getElementById('candidatos-lista');
    console.log('1. Elemento candidatos-lista:', candidatosLista ? 'ENCONTRADO' : 'NO ENCONTRADO');

    if (candidatosLista) {
        console.log('2. Contenido HTML:', candidatosLista.innerHTML.substring(0, 200));
        console.log('3. Número de filas:', candidatosLista.children.length);
    }

    // Verificar que el manager está inicializado
    console.log('4. candidatosManager:', window.candidatosManager ? 'INICIALIZADO' : 'NO INICIALIZADO');

    // Si el manager existe, verificar sus datos
    if (window.candidatosManager) {
        console.log('5. Candidatos cargados:', window.candidatosManager.candidatos.length);
        console.log('6. Partidos cargados:', window.candidatosManager.partidos.length);
        console.log('7. Tipos de elección cargados:', window.candidatosManager.tiposEleccion.length);
        
        // Mostrar primeros 3 candidatos
        if (window.candidatosManager.candidatos.length > 0) {
            console.log('8. Primeros 3 candidatos:');
            window.candidatosManager.candidatos.slice(0, 3).forEach(c => {
                console.log(`  - ${c.nombre_completo} (${c.cargo})`);
            });
        } else {
            console.log('8. ⚠️ Array de candidatos está vacío');
        }
        
        // Intentar forzar re-render
        console.log('9. Intentando forzar re-render...');
        window.candidatosManager.renderizarCandidatos();
    }

    // Verificar estilos del contenedor
    if (candidatosLista) {
        const styles = window.getComputedStyle(candidatosLista);
        console.log('10. Estilos del tbody:');
        console.log('  background:', styles.backgroundColor);
        console.log('  color:', styles.color);
        console.log('  display:', styles.display);
        console.log('  visibility:', styles.visibility);
    }

    console.log('=== FIN DEBUG ===');
}, 3000);
