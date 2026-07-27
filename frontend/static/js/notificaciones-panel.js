/**
 * NotificacionesPanel - Panel de notificaciones con lista y filtros
 */

class NotificacionesPanel {
    constructor() {
        this.notificaciones = [];
        this.filtro = 'todas'; // 'todas', 'no_leidas'
        this.loading = false;
        this.offset = 0;
        this.limit = 20;
        this.hasMore = true;
    }

    /**
     * Inicializar panel
     */
    async init() {
        // Crear elementos del DOM
        this.crearDropdown();
        this.crearModal();

        // Cargar notificaciones
        await this.cargarNotificaciones();

        // Escuchar nuevas notificaciones
        if (window.notificacionesManager) {
            window.notificacionesManager.onNuevaNotificacion((notif) => {
                this.agregarNotificacion(notif);
            });
        }

        // Event listeners
        this.setupEventListeners();
    }

    /**
     * Crear dropdown en navbar
     */
    crearDropdown() {
        // Buscar navbar
        const navbar = document.querySelector('.navbar') || document.querySelector('nav');
        if (!navbar) {
            console.warn('No se encontró navbar para agregar notificaciones');
            return;
        }

        // Crear contenedor de notificaciones
        const container = document.createElement('div');
        container.className = 'notificaciones-container';
        container.innerHTML = `
            <div class="notificaciones-dropdown">
                <button class="notificaciones-btn" id="notificaciones-btn" title="Notificaciones">
                    <i class="fas fa-bell"></i>
                    <span class="notificaciones-badge" id="notificaciones-badge" style="display: none;">0</span>
                </button>
                <div class="notificaciones-dropdown-menu" id="notificaciones-dropdown">
                    <div class="notificaciones-header">
                        <h3>Notificaciones</h3>
                        <button class="btn-marcar-todas" id="btn-marcar-todas" title="Marcar todas como leídas">
                            <i class="fas fa-check-double"></i>
                        </button>
                    </div>
                    <div class="notificaciones-filtros">
                        <button class="filtro-btn active" data-filtro="todas">Todas</button>
                        <button class="filtro-btn" data-filtro="no_leidas">No leídas</button>
                    </div>
                    <div class="notificaciones-lista" id="notificaciones-lista">
                        <div class="notificaciones-loading">
                            <i class="fas fa-spinner fa-spin"></i> Cargando...
                        </div>
                    </div>
                    <div class="notificaciones-footer">
                        <button class="btn-ver-todas" id="btn-ver-todas">Ver todas</button>
                    </div>
                </div>
            </div>
        `;

        // Insertar en navbar (al final)
        const navbarNav = navbar.querySelector('.navbar-nav') || navbar;
        navbarNav.appendChild(container);
    }

    /**
     * Crear modal para ver todas las notificaciones
     */
    crearModal() {
        const modal = document.createElement('div');
        modal.className = 'notificaciones-modal';
        modal.id = 'notificaciones-modal';
        modal.innerHTML = `
            <div class="notificaciones-modal-content">
                <div class="notificaciones-modal-header">
                    <h2>Todas las Notificaciones</h2>
                    <button class="notificaciones-modal-close" id="modal-close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="notificaciones-modal-body">
                    <div class="notificaciones-lista-completa" id="notificaciones-lista-completa">
                        <!-- Notificaciones se cargarán aquí -->
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Toggle dropdown
        const btn = document.getElementById('notificaciones-btn');
        if (btn) {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleDropdown();
            });
        }

        // Cerrar dropdown al hacer click fuera
        document.addEventListener('click', (e) => {
            const dropdown = document.getElementById('notificaciones-dropdown');
            if (dropdown && !dropdown.contains(e.target)) {
                dropdown.classList.remove('show');
            }
        });

        // Filtros
        document.querySelectorAll('.filtro-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.cambiarFiltro(e.target.dataset.filtro);
            });
        });

        // Marcar todas como leídas
        const btnMarcarTodas = document.getElementById('btn-marcar-todas');
        if (btnMarcarTodas) {
            btnMarcarTodas.addEventListener('click', () => {
                this.marcarTodasLeidas();
            });
        }

        // Ver todas
        const btnVerTodas = document.getElementById('btn-ver-todas');
        if (btnVerTodas) {
            btnVerTodas.addEventListener('click', () => {
                this.abrirModal();
            });
        }

        // Cerrar modal
        const modalClose = document.getElementById('modal-close');
        if (modalClose) {
            modalClose.addEventListener('click', () => {
                this.cerrarModal();
            });
        }

        // Cerrar modal al hacer click fuera
        const modal = document.getElementById('notificaciones-modal');
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.cerrarModal();
                }
            });
        }
    }

    /**
     * Toggle dropdown
     */
    toggleDropdown() {
        const dropdown = document.getElementById('notificaciones-dropdown');
        if (dropdown) {
            dropdown.classList.toggle('show');
        }
    }

    /**
     * Cargar notificaciones desde el servidor
     */
    async cargarNotificaciones() {
        if (this.loading) return;

        this.loading = true;
        this.mostrarLoading();

        try {
            const token = localStorage.getItem('token') || sessionStorage.getItem('token');
            const soloNoLeidas = this.filtro === 'no_leidas';

            const response = await fetch(
                `/api/notificaciones?solo_no_leidas=${soloNoLeidas}&limit=${this.limit}&offset=${this.offset}`,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                }
            );

            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    this.notificaciones = data.notificaciones || [];
                    this.renderizarNotificaciones();
                }
            }
        } catch (error) {
            console.error('Error cargando notificaciones:', error);
            this.mostrarError();
        } finally {
            this.loading = false;
        }
    }

    /**
     * Renderizar notificaciones en el dropdown
     */
    renderizarNotificaciones() {
        const lista = document.getElementById('notificaciones-lista');
        if (!lista) return;

        if (this.notificaciones.length === 0) {
            lista.innerHTML = `
                <div class="notificaciones-vacio">
                    <i class="fas fa-bell-slash"></i>
                    <p>No hay notificaciones</p>
                </div>
            `;
            return;
        }

        // Mostrar solo las primeras 5 en el dropdown
        const notificacionesDropdown = this.notificaciones.slice(0, 5);

        lista.innerHTML = notificacionesDropdown.map(notif => this.renderizarNotificacion(notif)).join('');

        // Event listeners para cada notificación
        lista.querySelectorAll('.notificacion-item').forEach(item => {
            item.addEventListener('click', () => {
                const id = parseInt(item.dataset.id);
                this.clickNotificacion(id);
            });
        });
    }

    /**
     * Renderizar una notificación
     */
    renderizarNotificacion(notif) {
        const iconoTipo = this.getIconoTipo(notif.tipo);
        const colorSeveridad = this.getColorSeveridad(notif);
        const leidaClass = notif.leida ? 'leida' : 'no-leida';
        const tiempoRelativo = this.getTiempoRelativo(notif.fecha_creacion);

        return `
            <div class="notificacion-item ${leidaClass}" data-id="${notif.id}">
                <div class="notificacion-icono" style="background-color: ${colorSeveridad}">
                    <i class="${iconoTipo}"></i>
                </div>
                <div class="notificacion-contenido">
                    <div class="notificacion-titulo">${notif.titulo}</div>
                    <div class="notificacion-mensaje">${notif.mensaje.substring(0, 80)}...</div>
                    <div class="notificacion-tiempo">${tiempoRelativo}</div>
                </div>
                ${!notif.leida ? '<div class="notificacion-punto"></div>' : ''}
            </div>
        `;
    }

    /**
     * Obtener icono según tipo de notificación
     */
    getIconoTipo(tipo) {
        const iconos = {
            'nuevo_incidente': 'fas fa-exclamation-triangle',
            'nuevo_delito': 'fas fa-gavel',
            'cambio_estado': 'fas fa-sync-alt'
        };
        return iconos[tipo] || 'fas fa-bell';
    }

    /**
     * Obtener color según severidad/gravedad
     */
    getColorSeveridad(notif) {
        if (notif.tipo === 'nuevo_incidente') {
            const colores = {
                'baja': '#4CAF50',
                'media': '#2196F3',
                'alta': '#ff9800',
                'crítica': '#f44336',
                'critica': '#f44336'
            };
            return colores[notif.severidad] || '#757575';
        } else if (notif.tipo === 'nuevo_delito') {
            return '#9c27b0';
        }
        return '#757575';
    }

    /**
     * Obtener tiempo relativo
     */
    getTiempoRelativo(fechaStr) {
        const fecha = new Date(fechaStr);
        const ahora = new Date();
        const diff = ahora - fecha;

        const minutos = Math.floor(diff / 60000);
        const horas = Math.floor(diff / 3600000);
        const dias = Math.floor(diff / 86400000);

        if (minutos < 1) return 'Ahora';
        if (minutos < 60) return `Hace ${minutos} min`;
        if (horas < 24) return `Hace ${horas} h`;
        if (dias < 7) return `Hace ${dias} d`;
        return fecha.toLocaleDateString();
    }

    /**
     * Click en notificación
     */
    async clickNotificacion(id) {
        const notif = this.notificaciones.find(n => n.id === id);
        if (!notif) return;

        // Marcar como leída
        await this.marcarLeida(id);

        // Navegar
        if (notif.incidente_id) {
            window.location.href = `/incidentes/${notif.incidente_id}`;
        } else if (notif.delito_id) {
            window.location.href = `/delitos/${notif.delito_id}`;
        }
    }

    /**
     * Marcar notificación como leída
     */
    async marcarLeida(id) {
        try {
            const token = localStorage.getItem('token') || sessionStorage.getItem('token');
            const response = await fetch(`/api/notificaciones/${id}/leer`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                // Actualizar en lista local
                const notif = this.notificaciones.find(n => n.id === id);
                if (notif) {
                    notif.leida = true;
                    this.renderizarNotificaciones();
                }
            }
        } catch (error) {
            console.error('Error marcando como leída:', error);
        }
    }

    /**
     * Marcar todas como leídas
     */
    async marcarTodasLeidas() {
        try {
            const token = localStorage.getItem('token') || sessionStorage.getItem('token');
            const response = await fetch('/api/notificaciones/marcar-todas-leidas', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                // Actualizar todas en lista local
                this.notificaciones.forEach(n => n.leida = true);
                this.renderizarNotificaciones();

                // Actualizar badge
                if (window.notificacionesManager) {
                    window.notificacionesManager.actualizarBadge();
                }
            }
        } catch (error) {
            console.error('Error marcando todas como leídas:', error);
        }
    }

    /**
     * Cambiar filtro
     */
    cambiarFiltro(filtro) {
        this.filtro = filtro;
        this.offset = 0;

        // Actualizar botones
        document.querySelectorAll('.filtro-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.filtro === filtro);
        });

        // Recargar
        this.cargarNotificaciones();
    }

    /**
     * Agregar nueva notificación
     */
    agregarNotificacion(notif) {
        this.notificaciones.unshift(notif);
        this.renderizarNotificaciones();
    }

    /**
     * Abrir modal
     */
    abrirModal() {
        const modal = document.getElementById('notificaciones-modal');
        if (modal) {
            modal.classList.add('show');
            this.renderizarModalCompleto();
        }
    }

    /**
     * Cerrar modal
     */
    cerrarModal() {
        const modal = document.getElementById('notificaciones-modal');
        if (modal) {
            modal.classList.remove('show');
        }
    }

    /**
     * Renderizar modal completo
     */
    renderizarModalCompleto() {
        const lista = document.getElementById('notificaciones-lista-completa');
        if (!lista) return;

        if (this.notificaciones.length === 0) {
            lista.innerHTML = `
                <div class="notificaciones-vacio">
                    <i class="fas fa-bell-slash"></i>
                    <p>No hay notificaciones</p>
                </div>
            `;
            return;
        }

        lista.innerHTML = this.notificaciones.map(notif => this.renderizarNotificacion(notif)).join('');

        // Event listeners
        lista.querySelectorAll('.notificacion-item').forEach(item => {
            item.addEventListener('click', () => {
                const id = parseInt(item.dataset.id);
                this.clickNotificacion(id);
            });
        });
    }

    /**
     * Mostrar loading
     */
    mostrarLoading() {
        const lista = document.getElementById('notificaciones-lista');
        if (lista) {
            lista.innerHTML = `
                <div class="notificaciones-loading">
                    <i class="fas fa-spinner fa-spin"></i> Cargando...
                </div>
            `;
        }
    }

    /**
     * Mostrar error
     */
    mostrarError() {
        const lista = document.getElementById('notificaciones-lista');
        if (lista) {
            lista.innerHTML = `
                <div class="notificaciones-error">
                    <i class="fas fa-exclamation-circle"></i>
                    <p>Error cargando notificaciones</p>
                </div>
            `;
        }
    }
}

// Crear instancia global
window.notificacionesPanel = new NotificacionesPanel();

// Auto-inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.notificacionesPanel.init();
    });
} else {
    window.notificacionesPanel.init();
}
