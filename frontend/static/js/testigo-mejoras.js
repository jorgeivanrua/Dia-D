/**
 * Mejoras UI/UX para Testigo Electoral
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
                
                // Si tiene data-tab, es una navegación de tab
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
    
    function updateStatsCards() {
        // Actualizar estado de presencia
        const presenciaVerificada = document.getElementById('alertaPresenciaVerificada');
        const statEstado = document.getElementById('statEstado');
        const statEstadoTexto = document.getElementById('statEstadoTexto');
        
        if (presenciaVerificada && !presenciaVerificada.classList.contains('d-none')) {
            statEstado.textContent = '✓';
            statEstadoTexto.textContent = 'Verificado';
        } else {
            statEstado.textContent = '✗';
            statEstadoTexto.textContent = 'Sin verificar';
        }
        
        // Actualizar formularios
        const formsTable = document.getElementById('formsTable');
        if (formsTable) {
            const rows = formsTable.querySelectorAll('tbody tr:not(.empty-row)');
            document.getElementById('statFormularios').textContent = rows.length;
        }
        
        // Actualizar votantes registrados
        const mesaSelect = document.getElementById('mesa');
        if (mesaSelect && mesaSelect.value) {
            const selectedOption = mesaSelect.options[mesaSelect.selectedIndex];
            const votantes = selectedOption.getAttribute('data-votantes') || '0';
            document.getElementById('statVotantes').textContent = votantes;
        }
    }

    // ============================================
    // MOBILE CARDS PARA FORMULARIOS
    // ============================================
    
    function renderFormulariosMobile(formularios) {
        const container = document.getElementById('formsCardsMobile');
        if (!container) return;
        
        if (!formularios || formularios.length === 0) {
            container.innerHTML = `
                <div class="text-center py-4 text-muted">
                    <i class="bi bi-file-earmark-text" style="font-size: 3rem;"></i>
                    <p class="mt-2">No hay formularios registrados</p>
                </div>
            `;
            return;
        }
        
        let html = '';
        formularios.forEach(form => {
            const estadoClass = {
                'pendiente': 'warning',
                'validado': 'success',
                'rechazado': 'danger',
                'borrador': 'secondary'
            }[form.estado] || 'secondary';
            
            const estadoIcon = {
                'pendiente': 'hourglass-split',
                'validado': 'check-circle',
                'rechazado': 'x-circle',
                'borrador': 'pencil'
            }[form.estado] || 'file-earmark';
            
            html += `
                <div class="card mb-3 shadow-sm">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <div>
                                <h6 class="mb-1">
                                    <i class="bi bi-table"></i> ${form.mesa_nombre || 'Mesa ' + form.mesa_codigo}
                                </h6>
                                <small class="text-muted">${form.tipo_eleccion || 'Sin tipo'}</small>
                            </div>
                            <span class="badge bg-${estadoClass}">
                                <i class="bi bi-${estadoIcon}"></i> ${form.estado}
                            </span>
                        </div>
                        <div class="row g-2 mb-2">
                            <div class="col-6">
                                <small class="text-muted d-block">Total Votos</small>
                                <strong>${form.total_votos || 0}</strong>
                            </div>
                            <div class="col-6">
                                <small class="text-muted d-block">Fecha</small>
                                <strong>${formatDate(form.fecha_creacion)}</strong>
                            </div>
                        </div>
                        <div class="d-flex gap-2">
                            <button class="btn btn-sm btn-outline-primary flex-fill" onclick="viewForm(${form.id})">
                                <i class="bi bi-eye"></i> Ver
                            </button>
                            ${form.estado === 'borrador' ? `
                                <button class="btn btn-sm btn-outline-warning flex-fill" onclick="editForm(${form.id})">
                                    <i class="bi bi-pencil"></i> Editar
                                </button>
                            ` : ''}
                        </div>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    }

    // ============================================
    // SINCRONIZACIÓN DE BOTONES
    // ============================================
    
    function syncFormButtons() {
        const btnDesktop = document.getElementById('btnNuevoFormulario');
        const btnMobile = document.getElementById('btnNuevoFormularioMobile');
        
        if (btnDesktop && btnMobile) {
            // Sincronizar estado inicial
            btnMobile.disabled = btnDesktop.disabled;
            
            // Sincronizar cambios
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.attributeName === 'disabled') {
                        const isDisabled = btnDesktop.disabled;
                        btnMobile.disabled = isDisabled;
                        
                        if (isDisabled) {
                            btnMobile.title = 'Debe seleccionar una mesa y verificar presencia primero';
                            btnMobile.classList.add('disabled');
                        } else {
                            btnMobile.title = '';
                            btnMobile.classList.remove('disabled');
                        }
                    }
                });
            });
            
            observer.observe(btnDesktop, { attributes: true });
            console.log('✅ Botones sincronizados correctamente');
        }
    }

    // ============================================
    // HAPTIC FEEDBACK
    // ============================================
    
    function addHapticFeedback() {
        const touchButtons = document.querySelectorAll('.btn-touch, .bottom-nav-item');
        
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
        const toastContainer = document.getElementById('alert-container');
        if (!toastContainer) return;
        
        const toastId = 'toast-' + Date.now();
        const iconMap = {
            'success': 'check-circle-fill',
            'error': 'x-circle-fill',
            'warning': 'exclamation-triangle-fill',
            'info': 'info-circle-fill'
        };
        
        const toast = document.createElement('div');
        toast.id = toastId;
        toast.className = `alert alert-${type} alert-dismissible fade show`;
        toast.innerHTML = `
            <i class="bi bi-${iconMap[type]}"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        toastContainer.appendChild(toast);
        
        // Auto-dismiss después de 5 segundos
        setTimeout(() => {
            const toastElement = document.getElementById(toastId);
            if (toastElement) {
                toastElement.classList.remove('show');
                setTimeout(() => toastElement.remove(), 150);
            }
        }, 5000);
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
                // Trigger refresh
                pulling = false;
                if (window.syncManager && window.syncManager.syncAll) {
                    showToast('Sincronizando datos...', 'info');
                    window.syncManager.syncAll();
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
        console.log('🎨 Inicializando mejoras UI/UX para Testigo Electoral');
        
        // Esperar a que el DOM esté listo
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }
        
        // Inicializar componentes
        initBottomNavigation();
        syncFormButtons();
        addHapticFeedback();
        initPullToRefresh();
        
        // Actualizar stats cada 5 segundos
        setInterval(updateStatsCards, 5000);
        updateStatsCards();
        
        // Exponer funciones globales
        window.testigoMejoras = {
            updateStatsCards,
            renderFormulariosMobile,
            showToast
        };
        
        console.log('✅ Mejoras UI/UX inicializadas correctamente');
    }

    // Iniciar
    init();
})();
