/**
 * Script para forzar renderizado de usuarios
 */

console.log('🔧 [Force Render] Script cargado');

// Esperar a que el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 [Force Render] DOM listo');
    
    // Esperar 3 segundos para que todo se cargue
    setTimeout(() => {
        console.log('🔧 [Force Render] Intentando forzar renderizado...');
        
        // Verificar si hay usuarios cargados
        if (window.allUsers && window.allUsers.length > 0) {
            console.log(`🔧 [Force Render] Encontrados ${window.allUsers.length} usuarios`);
            
            // Buscar el tbody
            const tbody = document.getElementById('usuarios-lista');
            if (tbody) {
                console.log('🔧 [Force Render] Elemento usuarios-lista encontrado');
                console.log('🔧 [Force Render] Contenido actual:', tbody.innerHTML.substring(0, 100));
                
                // Si está vacío o solo tiene el spinner, forzar renderizado
                if (tbody.children.length <= 1 || tbody.innerHTML.includes('spinner-border')) {
                    console.log('🔧 [Force Render] Forzando renderizado manual...');
                    
                    // Renderizar manualmente con estilos inline
                    const html = window.allUsers.map(user => {
                        return `
                            <tr style="background: white !important; color: #212529 !important;">
                                <td style="color: #212529 !important;">${user.id}</td>
                                <td style="color: #212529 !important;"><strong>${user.nombre}</strong></td>
                                <td style="color: #212529 !important;"><span class="badge bg-primary">${user.rol}</span></td>
                                <td style="color: #212529 !important;">${user.ubicacion_nombre || '<span class="text-muted" style="color: #6c757d !important;">Sin asignar</span>'}</td>
                                <td style="color: #212529 !important;"><span class="badge bg-${user.activo ? 'success' : 'secondary'}">${user.activo ? 'Activo' : 'Inactivo'}</span></td>
                                <td style="color: #212529 !important;"><small>${user.ultimo_acceso || '<span class="text-muted" style="color: #6c757d !important;">Nunca</span>'}</small></td>
                                <td class="text-center" style="color: #212529 !important;">
                                    <button class="btn btn-sm btn-outline-primary">
                                        <i class="bi bi-pencil"></i>
                                    </button>
                                </td>
                            </tr>
                        `;
                    }).join('');
                    
                    tbody.innerHTML = html;
                    console.log('🔧 [Force Render] ✅ Renderizado forzado completado');
                    
                    // Actualizar contador
                    const counter = document.getElementById('usuarios-count');
                    if (counter) {
                        counter.textContent = window.allUsers.length;
                        console.log('🔧 [Force Render] ✅ Contador actualizado');
                    }
                    
                    // Forzar visibilidad solo de elementos internos (NO del tab)
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
                    }, 500);
                } else {
                    console.log('🔧 [Force Render] ℹ️ Ya hay contenido en la tabla');
                    
                    // Forzar visibilidad solo de elementos internos (NO del tab)
                    const table = tbody.closest('table');
                    const chartCard = tbody.closest('.chart-card');
                    
                    if (chartCard) {
                        chartCard.style.cssText = 'opacity: 1 !important; visibility: visible !important; background: white !important;';
                    }
                    if (table) {
                        table.style.cssText = 'opacity: 1 !important; visibility: visible !important;';
                    }
                    tbody.style.cssText = 'opacity: 1 !important; visibility: visible !important;';
                    
                    // Hacer scroll incluso si ya hay contenido
                    setTimeout(() => {
                        if (chartCard) {
                            chartCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }
                    }, 500);
                }
            } else {
                console.error('🔧 [Force Render] ❌ Elemento usuarios-lista NO encontrado');
            }
        } else {
            console.warn('🔧 [Force Render] ⚠️ No hay usuarios cargados en window.allUsers');
        }
    }, 3000);
});

// También intentar cuando se active la pestaña de usuarios
document.addEventListener('shown.bs.tab', function(e) {
    if (e.target.id === 'users-tab') {
        console.log('🔧 [Force Render] Pestaña de usuarios activada');
        
        setTimeout(() => {
            const tbody = document.getElementById('usuarios-lista');
            if (tbody && window.allUsers && window.allUsers.length > 0) {
                if (tbody.children.length <= 1 || tbody.innerHTML.includes('spinner-border')) {
                    console.log('🔧 [Force Render] Forzando renderizado al activar pestaña...');
                    
                    const html = window.allUsers.map(user => {
                        return `
                            <tr style="background: white !important; color: #212529 !important;">
                                <td style="color: #212529 !important;">${user.id}</td>
                                <td style="color: #212529 !important;"><strong>${user.nombre}</strong></td>
                                <td style="color: #212529 !important;"><span class="badge bg-primary">${user.rol}</span></td>
                                <td style="color: #212529 !important;">${user.ubicacion_nombre || '<span class="text-muted" style="color: #6c757d !important;">Sin asignar</span>'}</td>
                                <td style="color: #212529 !important;"><span class="badge bg-${user.activo ? 'success' : 'secondary'}">${user.activo ? 'Activo' : 'Inactivo'}</span></td>
                                <td style="color: #212529 !important;"><small>${user.ultimo_acceso || '<span class="text-muted" style="color: #6c757d !important;">Nunca</span>'}</small></td>
                                <td class="text-center" style="color: #212529 !important;">
                                    <button class="btn btn-sm btn-outline-primary">
                                        <i class="bi bi-pencil"></i>
                                    </button>
                                </td>
                            </tr>
                        `;
                    }).join('');
                    
                    tbody.innerHTML = html;
                    
                    const counter = document.getElementById('usuarios-count');
                    if (counter) counter.textContent = window.allUsers.length;
                    
                    console.log('🔧 [Force Render] ✅ Renderizado forzado en activación de pestaña');
                }
                
                // Forzar visibilidad solo de elementos internos (NO del tab)
                const table = tbody.closest('table');
                const chartCard = tbody.closest('.chart-card');
                
                if (chartCard) {
                    chartCard.style.cssText = 'opacity: 1 !important; visibility: visible !important; background: white !important;';
                }
                if (table) {
                    table.style.cssText = 'opacity: 1 !important; visibility: visible !important;';
                }
                tbody.style.cssText = 'opacity: 1 !important; visibility: visible !important;';
                
                // Hacer scroll a la tabla
                setTimeout(() => {
                    if (chartCard) {
                        chartCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }, 300);
            }
        }, 500);
    }
});
