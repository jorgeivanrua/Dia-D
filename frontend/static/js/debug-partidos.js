/**
 * Script de debug para partidos
 */

console.log('=== DEBUG PARTIDOS ===');

// 1. Verificar elemento
const partidosTbody = document.getElementById('partidos-lista');
console.log('1. Elemento partidos-lista:', partidosTbody ? 'ENCONTRADO' : 'NO ENCONTRADO');

if (partidosTbody) {
    console.log('2. Contenido HTML:', partidosTbody.innerHTML.substring(0, 150));
    console.log('3. Número de filas:', partidosTbody.querySelectorAll('tr').length);
    
    // 2. Verificar partidosManager
    console.log('4. partidosManager:', window.partidosManager ? 'INICIALIZADO' : 'NO INICIALIZADO');
    
    if (window.partidosManager) {
        console.log('5. Partidos cargados:', window.partidosManager.partidos.length);
        
        // 3. Mostrar primeros partidos
        console.log('6. Primeros 3 partidos:');
        window.partidosManager.partidos.slice(0, 3).forEach(p => {
            console.log(`  - ${p.nombre} (${p.sigla})`);
        });
        
        // 4. Forzar re-render
        console.log('7. Intentando forzar re-render...');
        window.partidosManager.renderizarPartidos();
    }
    
    // 5. Verificar estilos
    const computedStyle = window.getComputedStyle(partidosTbody);
    console.log('8. Estilos del tbody:');
    console.log('  background:', computedStyle.background);
    console.log('  color:', computedStyle.color);
    console.log('  display:', computedStyle.display);
    console.log('  visibility:', computedStyle.visibility);
    
    // 6. Verificar tabla
    const table = partidosTbody.closest('table');
    if (table) {
        const tableStyle = window.getComputedStyle(table);
        console.log('9. Estilos de la tabla:');
        console.log('  display:', tableStyle.display);
        console.log('  table-layout:', tableStyle.tableLayout);
        console.log('  width:', tableStyle.width);
    }
    
    // 7. Verificar filas
    const rows = partidosTbody.querySelectorAll('tr');
    if (rows.length > 0) {
        const firstRow = rows[0];
        const rowStyle = window.getComputedStyle(firstRow);
        console.log('10. Estilos de la primera fila:');
        console.log('  display:', rowStyle.display);
        console.log('  background:', rowStyle.background);
        
        // Verificar celdas
        const cells = firstRow.querySelectorAll('td');
        if (cells.length > 0) {
            const cellStyle = window.getComputedStyle(cells[0]);
            console.log('11. Estilos de la primera celda:');
            console.log('  display:', cellStyle.display);
            console.log('  color:', cellStyle.color);
        }
    }
}

console.log('=== FIN DEBUG ===');
