/**
 * Mejoras para Dashboard del Coordinador de Puesto
 * Mobile-First & Responsive
 */

// Variables globales para las mejoras
let allFormularios = [];
let filteredFormularios = [];

/**
 * Renderizar cards de formularios para móvil
 */
function renderFormulariosCards(formularios) {
    const container = document.getElementById('formulariosCards');
    
    if (!container) return;
    
    if (formularios.length === 0) {
        container.innerHTML = `
            <div class="text-center py-5">
                <i class="bi bi-inbox" style="font-size: 3rem; color: var(--text-tertiary);"></i>
                <p class="text-muted mt-3">No hay formularios ${estadoFiltro ? 'en estado ' + estadoFiltro : ''}</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = formularios.map(form => {
        const estadoBadge = getEstadoBadgeV2(form.estado);
        const fecha = Utils.formatDate(form.created_at);
        const puedeValidar = form.estado === 'pendiente';
        
        return `
            <div class="formulario-card" onclick="${puedeValidar ? `abrirModalValidacion(${form.id})` : `verDetalles(${form.id})`}">
                <div class="formulario-card-header">
                    <div class="formulario-card-title">
                        <h6><i class="bi bi-table"></i> Mesa ${form.mesa_codigo || 'N/A'}</h6>
                        <p><i class="bi bi-person"></i> ${form.testigo_nombre || 'N/A'}</p>
                        <p>
                            <span class="badge bg-primary" style="font-size: 0.75rem;">
                                ${form.tipo_eleccion_nombre || 'N/A'}
                            </span>
                        </p>
                    </div>
                    <div class="formulario-card-badge">
                        ${estadoBadge}
                    </div>
                </div>
                <div class="formulario-card-body">
                    <div class="formulario-card-info">
                        <div class="formulario-card-info-item">
                            <label>Total Votos</label>
                            <span>${Utils.formatNumber(form.total_votos)}</span>
                        </div>
                        <div class="formulario-card-info-item">
                            <label>Fecha</label>
                            <span>${fecha}</span>
                        </div>
                    </div>
                    <div>
                        ${puedeValidar ? 
                            `<button class="btn btn-primary btn-sm" onclick="event.stopPropagation(); abrirModalValidacion(${form.id})">
                                <i class="bi bi-eye"></i>
                            </button>` :
                            `<button class="btn btn-outline-secondary btn-sm" onclick="event.stopPropagation(); verDetalles(${form.id})">
                                <i class="bi bi-info-circle"></i>
                            </button>`
                        }
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Obtener badge de estado v2 (mejorado)
 */
function getEstadoBadgeV2(estado) {
    const badges = {
        'borrador': '<span class="badge-status badge-borrador">Borrador</span>',
        'pendiente': '<span class="badge-status badge-pendiente">Pendiente</span>',
        'validado': '<span class="badge-status badge-validado">Validado</span>',
        'rechazado': '<span class="badge-status badge-rechazado">Rechazado</span>'
    };
    return badges[estado] || `<span class="badge-status badge-borrador">${estado}</span>`;
}

/**
 * Actualizar badges de los filtros
 */
function updateFilterBadges(stats) {
    const total = stats.total || 0;
    const pendientes = stats.pendientes || 0;
    const validados = stats.validados || 0;
    const rechazados = stats.rechazados || 0;
    
    // Actualizar badges de chips
    const badgeTodos = document.getElementById('badgeTodos');
    const badgePendientes = document.getElementById('badgePendientes');
    const badgeValidados = document.getElementById('badgeValidados');
    const badgeRechazados = document.getElementById('badgeRechazados');
    
    if (badgeTodos) badgeTodos.textContent = total;
    if (badgePendientes) badgePendientes.textContent = pendientes;
    if (badgeValidados) badgeValidados.textContent = validados;
    if (badgeRechazados) badgeRechazados.textContent = rechazados;
    
    // Actualizar badges de bottom nav
    const navBadgeFormularios = document.getElementById('navBadgeFormularios');
    if (navBadgeFormularios) {
        if (pendientes > 0) {
            navBadgeFormularios.textContent = pendientes;
            navBadgeFormularios.style.display = 'flex';
        } else {
            navBadgeFormularios.style.display = 'none';
        }
    }
    
    // Actualizar badge de alertas (incidentes + delitos)
    const navBadgeAlertas = document.getElementById('navBadgeAlertas');
    const badgeIncidentes = document.getElementById('badge-incidentes');
    const badgeDelitos = document.getElementById('badge-delitos');
    
    if (navBadgeAlertas && badgeIncidentes && badgeDelitos) {
        const totalAlertas = parseInt(badgeIncidentes.textContent || 0) + parseInt(badgeDelitos.textContent || 0);
        if (totalAlertas > 0) {
            navBadgeAlertas.textContent = totalAlertas;
            navBadgeAlertas.style.display = 'flex';
        } else {
            navBadgeAlertas.style.display = 'none';
        }
    }
}

/**
 * Buscar formularios
 */
function buscarFormularios(query) {
    query = query.toLowerCase().trim();
    
    if (!query) {
        // Mostrar todos
        filteredFormularios = allFormularios;
    } else {
        // Filtrar
        filteredFormularios = allFormularios.filter(form => {
            const mesa = (form.mesa_codigo || '').toLowerCase();
            const testigo = (form.testigo_nombre || '').toLowerCase();
            return mesa.includes(query) || testigo.includes(query);
        });
    }
    
    // Aplicar filtro de estado si existe
    let formulariosParaMostrar = filteredFormularios;
    if (estadoFiltro) {
        formulariosParaMostrar = filteredFormularios.filter(f => f.estado === estadoFiltro);
    }
    
    renderFormulariosTable(formulariosParaMostrar);
    renderFormulariosCards(formulariosParaMostrar);
}

/**
 * Cambiar tab desde bottom navigation
 */
function cambiarTab(tabName) {
    // Actualizar active en bottom nav
    document.querySelectorAll('.bottom-nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    const clickedItem = event.target.closest('.bottom-nav-item');
    if (clickedItem) {
        clickedItem.classList.add('active');
    }
    
    // Activar tab correspondiente
    const tabMap = {
        'formularios': 'formularios-tab',
        'alertas': 'incidentes-tab',
        'equipo': 'equipo-tab',
        'mapa': 'mapa-tab'
    };
    
    const tabId = tabMap[tabName];
    if (tabId) {
        const tab = document.getElementById(tabId);
        if (tab) {
            const bsTab = new bootstrap.Tab(tab);
            bsTab.show();
        }
    }
    
    // Vibración háptica
    vibrate(50);
}

/**
 * Mostrar toast notification
 */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    // Vibración en móvil
    if (type === 'success') {
        vibrate([50, 100, 50]);
    } else if (type === 'error') {
        vibrate([100, 50, 100, 50, 100]);
    } else {
        vibrate(50);
    }
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

/**
 * Vibración háptica (móvil)
 */
function vibrate(pattern = [100]) {
    if ('vibrate' in navigator) {
        navigator.vibrate(pattern);
    }
}

/**
 * Pull to refresh
 */
let touchStartY = 0;
let touchEndY = 0;
let isPulling = false;

document.addEventListener('touchstart', e => {
    touchStartY = e.changedTouches[0].screenY;
}, { passive: true });

document.addEventListener('touchmove', e => {
    touchEndY = e.changedTouches[0].screenY;
    const diff = touchEndY - touchStartY;
    
    if (diff > 0 && window.scrollY === 0 && !isPulling) {
        isPulling = true;
    }
}, { passive: true });

document.addEventListener('touchend', e => {
    if (isPulling) {
        isPulling = false;
        const diff = touchEndY - touchStartY;
        
        if (diff > 100) {
            // Refresh
            showToast('Actualizando...', 'info');
            if (typeof loadFormularios === 'function') loadFormularios();
            if (typeof loadConsolidado === 'function') loadConsolidado();
            if (typeof loadMesas === 'function') loadMesas();
            if (typeof loadTestigos === 'function') loadTestigos();
        }
    }
}, { passive: true });

/**
 * Actualizar filtro de estado con chips
 */
const originalFiltrarPorEstado = window.filtrarPorEstado;
window.filtrarPorEstado = function(estado) {
    // Actualizar chips activos
    document.querySelectorAll('.chip').forEach(chip => {
        chip.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Llamar a la función original
    if (originalFiltrarPorEstado) {
        originalFiltrarPorEstado(estado);
    }
    
    // Vibración
    vibrate(50);
};

/**
 * Override de loadFormularios para incluir renderizado de cards
 */
const originalLoadFormularios = window.loadFormularios;
if (originalLoadFormularios) {
    window.loadFormularios = async function() {
        try {
            const params = {};
            if (estadoFiltro) {
                params.estado = estadoFiltro;
            }
            
            const response = await APIClient.get('/formularios/puesto', params);
            
            if (response.success) {
                formularios = response.data.formularios || [];
                allFormularios = formularios;
                filteredFormularios = formularios;
                
                const stats = response.data.estadisticas || {
                    total: 0,
                    pendientes: 0,
                    validados: 0,
                    rechazados: 0,
                    mesas_reportadas: 0,
                    total_mesas: 0
                };
                
                // Actualizar estadísticas
                if (typeof updateEstadisticas === 'function') {
                    updateEstadisticas(stats);
                }
                
                // Actualizar badges de filtros
                updateFilterBadges(stats);
                
                // Renderizar tabla (desktop)
                if (typeof renderFormulariosTable === 'function') {
                    renderFormulariosTable(formularios);
                }
                
                // Renderizar cards (móvil)
                renderFormulariosCards(formularios);
            } else {
                throw new Error(response.error || 'Error desconocido');
            }
        } catch (error) {
            console.error('Error loading formularios:', error);
            showToast('Error al cargar formularios', 'error');
        }
    };
}

/**
 * Mejorar validación con feedback
 */
const originalValidarFormulario = window.validarFormulario;
if (originalValidarFormulario) {
    window.validarFormulario = async function() {
        try {
            await originalValidarFormulario();
            showToast('Formulario validado exitosamente', 'success');
        } catch (error) {
            showToast('Error al validar formulario', 'error');
        }
    };
}

/**
 * Mejorar rechazo con feedback
 */
const originalConfirmarRechazo = window.confirmarRechazo;
if (originalConfirmarRechazo) {
    window.confirmarRechazo = async function() {
        try {
            await originalConfirmarRechazo();
            showToast('Formulario rechazado', 'warning');
        } catch (error) {
            showToast('Error al rechazar formulario', 'error');
        }
    };
}

/**
 * Sincronizar tabs con bottom nav
 */
document.addEventListener('shown.bs.tab', function (event) {
    const tabId = event.target.id;
    const tabMap = {
        'formularios-tab': 'formularios',
        'incidentes-tab': 'alertas',
        'delitos-tab': 'alertas',
        'equipo-tab': 'equipo',
        'mapa-tab': 'mapa'
    };
    
    const bottomNavTab = tabMap[tabId];
    if (bottomNavTab) {
        document.querySelectorAll('.bottom-nav-item').forEach(item => {
            item.classList.remove('active');
            if (item.dataset.tab === bottomNavTab) {
                item.classList.add('active');
            }
        });
    }
});

/**
 * Inicialización de mejoras
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Mejoras del coordinador de puesto cargadas');
    
    // Detectar si es móvil
    const isMobile = window.innerWidth < 768;
    if (isMobile) {
        console.log('📱 Modo móvil detectado');
    }
    
    // Agregar clase al body para estilos específicos de móvil
    if (isMobile) {
        document.body.classList.add('mobile-view');
    }
});

// Detectar cambios de orientación
window.addEventListener('orientationchange', function() {
    setTimeout(() => {
        const isMobile = window.innerWidth < 768;
        if (isMobile) {
            document.body.classList.add('mobile-view');
        } else {
            document.body.classList.remove('mobile-view');
        }
    }, 100);
});

console.log('✅ Módulo de mejoras del coordinador de puesto cargado');
