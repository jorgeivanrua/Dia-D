/**
 * Fix para renderizar candidatos
 */

console.log('🔧 [Fix Candidatos] Script cargado');

setTimeout(() => {
    console.log('🔧 [Fix Candidatos] Ejecutando...');
    
    const tbody = document.getElementById('candidatos-lista');
    if (!tbody) {
        console.error('❌ [Fix Candidatos] Elemento no encontrado');
        return;
    }
    
    // Verificar si candidatosManager existe y tiene datos
    if (window.candidatosManager && window.candidatosManager.candidatos && window.candidatosManager.candidatos.length > 0) {
        console.log(`🔧 [Fix Candidatos] Encontrados ${window.candidatosManager.candidatos.length} candidatos`);
        
        // Forzar renderizado
        const candidatos = window.candidatosManager.candidatos;
        
        tbody.innerHTML = candidatos.map(candidato => `
            <tr style="background: white !important; color: #212529 !important;">
                <td style="color: #212529 !important;">
                    ${candidato.foto_url ? 
                        `<img src="${candidato.foto_url}" alt="${candidato.nombre_completo}" class="rounded-circle" style="width: 40px; height: 40px; object-fit: cover;">` :
                        `<div class="rounded-circle bg-secondary d-flex align-items-center justify-content-center" style="width: 40px; height: 40px; color: white;">
                            <i class="bi bi-person"></i>
                        </div>`
                    }
                </td>
                <td style="color: #212529 !important;"><strong>${candidato.nombre_completo}</strong></td>
                <td style="color: #212529 !important;">
                    ${candidato.partido ? 
                        `<span class="badge" style="background-color: ${candidato.partido.color}; color: white;">
                            ${candidato.partido.sigla}
                        </span>` :
                        '<span class="text-muted" style="color: #6c757d !important;">N/A</span>'
                    }
                </td>
                <td style="color: #212529 !important;">${candidato.cargo || 'N/A'}</td>
                <td style="color: #212529 !important;">
                    ${candidato.tipo_eleccion ? 
                        `<small>${candidato.tipo_eleccion.nombre}</small>` :
                        '<span class="text-muted" style="color: #6c757d !important;">N/A</span>'
                    }
                </td>
                <td style="color: #212529 !important;">
                    <span class="badge bg-${candidato.activo ? 'success' : 'secondary'}">
                        ${candidato.activo ? 'Activo' : 'Inactivo'}
                    </span>
                </td>
                <td style="color: #212529 !important;">
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" title="Editar">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-outline-danger" title="Eliminar">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
        
        // Actualizar contador
        const contador = document.getElementById('candidatos-count');
        if (contador) {
            contador.textContent = candidatos.length;
        }
        
        console.log('✅ [Fix Candidatos] Renderizados correctamente');
        
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
        
        // Hacer scroll automático a la tabla
        setTimeout(() => {
            if (chartCard) {
                chartCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
            console.log('✅ [Fix Candidatos] Scroll automático realizado');
        }, 500);
    } else {
        console.log('⚠️ [Fix Candidatos] No hay datos disponibles aún');
    }
}, 4000); // Esperar 4 segundos para que candidatosManager se inicialice

// También hacer scroll cuando se active la pestaña de candidatos
document.addEventListener('shown.bs.tab', function(e) {
    if (e.target.id === 'candidatos-tab') {
        console.log('🔧 [Fix Candidatos] Pestaña activada, haciendo scroll...');
        setTimeout(() => {
            const tbody = document.getElementById('candidatos-lista');
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
