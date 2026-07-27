/**
 * Fix para renderizar partidos
 */

console.log('🔧 [Fix Partidos] Script cargado');

setTimeout(() => {
    console.log('🔧 [Fix Partidos] Ejecutando...');
    
    const tbody = document.getElementById('partidos-lista');
    if (!tbody) {
        console.error('❌ [Fix Partidos] Elemento no encontrado');
        return;
    }
    
    // Verificar si partidosManager existe y tiene datos
    if (window.partidosManager && window.partidosManager.partidos && window.partidosManager.partidos.length > 0) {
        console.log(`🔧 [Fix Partidos] Encontrados ${window.partidosManager.partidos.length} partidos`);
        
        // Forzar visibilidad de elementos internos
        const table = tbody.closest('table');
        const chartCard = tbody.closest('.chart-card');
        
        if (chartCard) {
            chartCard.style.cssText = 'opacity: 1 !important; visibility: visible !important; background: white !important;';
        }
        if (table) {
            table.style.cssText = 'opacity: 1 !important; visibility: visible !important;';
        }
        tbody.style.cssText = 'opacity: 1 !important; visibility: visible !important;';
        
        console.log('✅ [Fix Partidos] Visibilidad forzada');
        
        // Hacer scroll automático
        setTimeout(() => {
            if (chartCard) {
                chartCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
            console.log('✅ [Fix Partidos] Scroll automático realizado');
        }, 500);
    } else {
        console.log('⚠️ [Fix Partidos] No hay datos disponibles aún');
    }
}, 4000); // Esperar 4 segundos

// También hacer scroll cuando se active la pestaña de partidos
document.addEventListener('shown.bs.tab', function(e) {
    if (e.target.id === 'partidos-tab') {
        console.log('🔧 [Fix Partidos] Pestaña activada');
        setTimeout(() => {
            const tbody = document.getElementById('partidos-lista');
            if (tbody) {
                // Forzar visibilidad
                const table = tbody.closest('table');
                const chartCard = tbody.closest('.chart-card');
                
                if (chartCard) {
                    chartCard.style.cssText = 'opacity: 1 !important; visibility: visible !important; background: white !important;';
                }
                if (table) {
                    table.style.cssText = 'opacity: 1 !important; visibility: visible !important;';
                }
                tbody.style.cssText = 'opacity: 1 !important; visibility: visible !important;';
                
                // Hacer scroll
                if (chartCard) {
                    chartCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        }, 300);
    }
});
