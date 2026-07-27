/**
 * Mejoras UI/UX para Coordinador Municipal
 * Mobile-first responsive design
 */

(function() {
    'use strict';

    // ============================================
    // BOTTOM NAVIGATION
    // ============================================
    
    function initBottomNavigation() {
        const bottomNavItems = document.querySelectorAll('.bottom-nav-item');
        
        bottomNavItems.forEach(item => {
            item.addEventListener('click', function(e) {
                const tabTarget = this.getAttribute('data-tab');
                
                if (tabTarget) {
                    e.preventDefault();
                    
                    // Remover active de todos
                    bottomNavItems.forEach(nav => nav.classList.remove('active'));
                    
                    // Agregar active al clickeado
                    this.classList.add('active');
                    
                    // Activar el tab correspondiente
                    const tabButton = document.getElementById(`${tabTarget}-tab`);
                    if (tabButton) {
                        const tab = new bootstrap.Tab(tabButton);
                        tab.show();
                    }
                }
            });
        });
        
        // Sincronizar tabs con bottom nav
        const tabButtons = document.querySelectorAll('[data-bs-toggle="tab"]');
        tabButtons.forEach(button => {
            button.addEventListener('shown.bs.tab', function(e) {
                const targetId = e.target.getAttribute('data-bs-target');
                if (targetId) {
                    const tabName = targetId.replace('#', '');
                    const bottomNavItem = document.querySelector(`.bottom-nav-item[data-tab="${tabName}"]`);
                    if (bottomNavItem) {
                        bottomNavItems.forEach(nav => nav.classList.remove('active'));
                        bottomNavItem.classList.add('active');
                    }
                }
            });
        });
    }

    // ============================================
    // STATS CARDS
    // ============================================
    
    function updateStatsCards(data) {
        if (!data) return;
        
        // Actualizar puestos
        if (data.total_puestos !== undefined) {
            document.getElementById('statPuestos').textContent = data.total_puestos;
        }
        
        // Actualizar validados
        if (data.formularios_validados !== undefined) {
            document.getElementById('statValidados').textContent = data.formularios_validados;
        }
        
        // Actualizar pendientes
        if (data.formularios_pendientes !== undefined) {
            document.getElementById('statPendientes').textContent = data.formularios_pendientes;
        }
        
        // Actualizar progreso
        if (data.progreso !== undefined) {
            document.getElementById('statProgreso').textContent = data.progreso + '%';
        }
        
        // Actualizar badges de filtros
        if (data.completos !== undefined) {
            document.getElementById('badgeCompletos').textContent = data.completos;
        }
        if (data.incompletos !== undefined) {
            document.getElementById('badgeIncompletos').textContent = data.incompletos;
        }
        if (data.con_discrepancias !== undefined) {
            document.getElementById('badgeDiscrepancias').textContent = data.con_discrepancias;
        }
        if (data.total_puestos !== undefined) {
            document.getElementById('badgeTodos').textContent = data.total_puestos;
        }
    }

    // ============================================
    // MOBILE CARDS PARA PUESTOS
    // ============================================
    
    function renderPuestosMobile(puestos) {
        const container = document.getElementById('puestosCardsMobile');
        if (!container) return;
        
        if (!puestos || puestos.length === 0) {
            container.innerHTML = `
                <div class="text-center py-4 text-muted">
                    <i class="bi bi-geo-alt" style="font-size: 3rem;"></i>
                    <p class="mt-2">No hay puestos registrados</p>
                </div>
            `;
            return;
        }
        
        let html = '';
        puestos.forEach(puesto => {
            const estadoClass = {
                'completo': 'success',
                'incompleto': 'warning',
                'con_discrepancias': 'danger',
                'sin_datos': 'secondary'
            }[puesto.estado] || 'secondary';
            
            const estadoIcon = {
                'completo': 'check-circle',
                'incompleto': 'hourglass-split',
                'con_discrepancias': 'exclamation-triangle',
                'sin_datos': 'dash-circle'
            }[puesto.estado] || 'dash-circle';
            
            const avance = puesto.avance || 0;
            const progressClass = avance >= 80 ? 'success' : avance >= 50 ? 'warning' : 'danger';
            
            html += `
                <div class="puesto-card" onclick="seleccionarPuesto(${puesto.id})" data-puesto-id="${puesto.id}">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <div>
                            <h6 class="mb-1">
                                <i class="bi bi-geo-alt"></i> ${puesto.nombre || 'Puesto ' + puesto.codigo}
                            </h6>
                            <small class="text-muted">${puesto.codigo}</small>
                        </div>
                        <span class="badge bg-${estadoClass}">
                            <i class="bi bi-${estadoIcon}"></i> ${puesto.estado}
                        </span>
                    </div>
                    
                    <div class="mb-2">
                        <small class="text-muted d-block mb-1">Coordinador</small>
                        <strong>${puesto.coordinador_nombre || 'Sin asignar'}</strong>
                    </div>
                    
                    <div class="mb-2">
                        <div class="d-flex justify-content-between align-items-center mb-1">
                            <small class="text-muted">Avance</small>
                            <small><strong>${avance}%</strong></small>
                        </div>
                        <div class="progress" style="height: 6px;">
                            <div class="progress-bar bg-${progressClass}" role="progressbar" 
                                 style="width: ${avance}%" aria-valuenow="${avance}" 
                                 aria-valuemin="0" aria-valuemax="100"></div>
                        </div>
                    </div>
                    
                    <div class="row g-2">
                        <div class="col-4">
                            <small class="text-muted d-block">Mesas</small>
                            <strong>${puesto.total_mesas || 0}</strong>
                        </div>
                        <div class="col-4">
                            <small class="text-muted d-block">Formularios</small>
                            <strong>${puesto.formularios_enviados || 0}</strong>
                        </div>
                        <div class="col-4">
                            <small class="text-muted d-block">Validados</small>
                            <strong class="text-success">${puesto.formularios_validados || 0}</strong>
                        </div>
                    </div>
                    
                    ${puesto.tiene_discrepancias ? `
                        <div class="alert alert-danger mt-2 mb-0 py-1 px-2">
                            <small><i class="bi bi-exclamation-triangle"></i> Tiene discrepancias</small>
                        </div>
                    ` : ''}
                </div>
            `;
        });
        
        container.innerHTML = html;
    }

    // ============================================
    // FILTROS
    // ============================================
    
    function initFiltros() {
        const filterChips = document.querySelectorAll('.filter-chip');
        
        filterChips.forEach(chip => {
            chip.addEventListener('click', function() {
                // Remover active de todos
                filterChips.forEach(c => c.classList.remove('active'));
                
                // Agregar active al clickeado
                this.classList.add('active');
                
                // Vibración háptica
                if (navigator.vibrate) {
                    navigator.vibrate(10);
                }
            });
        });
    }

    // ============================================
    // SELECCIÓN DE PUESTO
    // ============================================
    
    window.seleccionarPuesto = function(puestoId) {
        // Remover selección anterior
        document.querySelectorAll('.puesto-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        // Agregar selección al nuevo
        const card = document.querySelector(`.puesto-card[data-puesto-id="${puestoId}"]`);
        if (card) {
            card.classList.add('selected');
        }
        
        // Vibración háptica
        if (navigator.vibrate) {
            navigator.vibrate(10);
        }
        
        // Cargar detalle del puesto
        cargarDetallePuesto(puestoId);
    };

    // ============================================
    // DETALLE DE PUESTO
    // ============================================
    
    function cargarDetallePuesto(puestoId) {
        const container = document.getElementById('detallePuesto');
        if (!container) return;
        
        // Mostrar loading
        container.innerHTML = `
            <div class="text-center py-3">
                <div class="spinner-border spinner-border-sm text-info" role="status">
                    <span class="visually-hidden">Cargando...</span>
                </div>
            </div>
        `;
        
        // Aquí iría la llamada al backend
        // Por ahora solo mostramos un placeholder
        setTimeout(() => {
            container.innerHTML = `
                <p class="text-muted text-center">
                    <i class="bi bi-info-circle"></i><br>
                    Detalle del puesto ${puestoId}
                </p>
            `;
        }, 500);
    }

    // ============================================
    // HAPTIC FEEDBACK
    // ============================================
    
    function addHapticFeedback() {
        const touchButtons = document.querySelectorAll('.btn-touch, .bottom-nav-item, .filter-chip');
        
        touchButtons.forEach(button => {
            button.addEventListener('click', function() {
                if (navigator.vibrate) {
                    navigator.vibrate(10);
                }
            });
        });
    }

    // ============================================
    // TOAST NOTIFICATIONS
    // ============================================
    
    function showToast(message, type = 'info') {
        // Buscar o crear contenedor de toasts
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }
        
        const toastId = 'toast-' + Date.now();
        const iconMap = {
            'success': 'check-circle-fill',
            'error': 'x-circle-fill',
            'warning': 'exclamation-triangle-fill',
            'info': 'info-circle-fill'
        };
        
        const toast = document.createElement('div');
        toast.id = toastId;
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi bi-${iconMap[type]}"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast, { delay: 5000 });
        bsToast.show();
        
        // Remover después de ocultar
        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    }

    // ============================================
    // PULL TO REFRESH
    // ============================================
    
    function initPullToRefresh() {
        let startY = 0;
        let currentY = 0;
        let pulling = false;
        
        const container = document.querySelector('.container-fluid');
        if (!container) return;
        
        container.addEventListener('touchstart', function(e) {
            if (window.scrollY === 0) {
                startY = e.touches[0].pageY;
                pulling = true;
            }
        });
        
        container.addEventListener('touchmove', function(e) {
            if (!pulling) return;
            
            currentY = e.touches[0].pageY;
            const diff = currentY - startY;
            
            if (diff > 100) {
                pulling = false;
                if (typeof loadPuestos === 'function') {
                    showToast('Actualizando datos...', 'info');
                    loadPuestos();
                }
            }
        });
        
        container.addEventListener('touchend', function() {
            pulling = false;
        });
    }

    // ============================================
    // HELPER FUNCTIONS
    // ============================================
    
    function formatDate(dateString) {
        if (!dateString) return '-';
        const date = new Date(dateString);
        return date.toLocaleDateString('es-CO', { 
            day: '2-digit', 
            month: '2-digit',
            year: '2-digit'
        });
    }

    // ============================================
    // INICIALIZACIÓN
    // ============================================
    
    function init() {
        console.log('🎨 Inicializando mejoras UI/UX para Coordinador Municipal');
        
        // Esperar a que el DOM esté listo
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }
        
        // Inicializar componentes
        initBottomNavigation();
        initFiltros();
        addHapticFeedback();
        initPullToRefresh();
        
        // Exponer funciones globales
        window.municipalMejoras = {
            updateStatsCards,
            renderPuestosMobile,
            showToast,
            seleccionarPuesto
        };
        
        console.log('✅ Mejoras UI/UX inicializadas correctamente');
    }

    // Iniciar
    init();
})();
