/**
 * ReportesPendientesPanel - Panel para visualizar reportes pendientes de sincronización
 */

class ReportesPendientesPanel {
    constructor() {
        this.reportesPendientes = [];
        this.init();
    }

    /**
     * Inicializar panel
     */
    async init() {
        this.createPanel();
        await this.cargarReportesPendientes();
        this.setupEventListeners();
        
        // Actualizar cada 30 segundos
        setInterval(() => {
            this.cargarReportesPendientes();
        }, 30000);
    }

    /**
     * Crear panel HTML
     */
    createPanel() {
        const panel = document.createElement('div');
        panel.id = 'reportes-pendientes-panel';
        panel.className = 'reportes-pendientes-panel';
        panel.innerHTML = `
            <div class="panel-header">
                <div class="panel-title">
                    <i class="fas fa-clock"></i>
                    <span>Reportes Pendientes</span>
                    <span class="badge bg-warning" id="pendientes-count">0</span>
                </div>
                <button class="panel-toggle" id="panel-toggle-btn">
                    <i class="fas fa-chevron-down"></i>
                </button>
            </div>
            <div class="panel-content" id="panel-content">
                <div class="panel-info">
                    <p class="text-muted small mb-2">
                        <i class="fas fa-info-circle"></i>
                        Estos reportes se sincronizarán automáticamente cuando haya conexión.
                    </p>
                </div>
                <div class="reportes-list" id="reportes-pendientes-list">
                    <!-- Los reportes se cargarán aquí -->
                </div>
                <div class="panel-actions">
                    <button class="btn btn-sm btn-primary w-100" id="btn-sync-now">
                        <i class="fas fa-sync-alt"></i> Sincronizar Ahora
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(panel);
    }

    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        // Toggle panel
        const toggleBtn = document.getElementById('panel-toggle-btn');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                this.togglePanel();
            });
        }
        
        // Sincronizar ahora
        const syncBtn = document.getElementById('btn-sync-now');
        if (syncBtn) {
            syncBtn.addEventListener('click', () => {
                this.sincronizarAhora();
            });
        }
        
        // Escuchar eventos del SyncManager
        if (window.syncManager) {
            window.syncManager.on('onSyncComplete', () => {
                this.cargarReportesPendientes();
            });
            
            window.syncManager.on('onConnectionChange', (online) => {
                this.updateConnectionStatus(online);
            });
        }
    }

    /**
     * Cargar reportes pendientes
     */
    async cargarReportesPendientes() {
        try {
            if (!window.indexedDBService || !window.indexedDBService.db) {
                return;
            }
            
            this.reportesPendientes = await window.indexedDBService.obtenerReportesPendientes();
            
            // Actualizar contador
            const countBadge = document.getElementById('pendientes-count');
            if (countBadge) {
                countBadge.textContent = this.reportesPendientes.length;
                
                // Mostrar/ocultar panel según haya reportes
                const panel = document.getElementById('reportes-pendientes-panel');
                if (panel) {
                    if (this.reportesPendientes.length > 0) {
                        panel.classList.add('visible');
                    } else {
                        panel.classList.remove('visible');
                    }
                }
            }
            
            // Renderizar lista
            this.renderizarReportes();
            
        } catch (error) {
            console.error('Error cargando reportes pendientes:', error);
        }
    }

    /**
     * Renderizar lista de reportes
     */
    renderizarReportes() {
        const lista = document.getElementById('reportes-pendientes-list');
        if (!lista) return;
        
        if (this.reportesPendientes.length === 0) {
            lista.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-check-circle"></i>
                    <p>No hay reportes pendientes</p>
                </div>
            `;
            return;
        }
        
        lista.innerHTML = this.reportesPendientes.map(reporte => {
            const tipo = reporte.tipo || 'incidente';
            let icono, color, titulo, subtitulo;
            
            // Determinar icono y color según tipo
            switch(tipo) {
                case 'formulario_e14':
                    icono = 'fa-file-alt';
                    color = 'primary';
                    titulo = `E-14: ${reporte.mesa_display || 'Mesa ' + reporte.mesa_id}`;
                    subtitulo = reporte.tipo_eleccion_display || 'Tipo de elección';
                    break;
                case 'formulario_e24':
                    icono = 'fa-file-invoice';
                    color = 'info';
                    titulo = `E-24: ${reporte.puesto_nombre || 'Puesto'}`;
                    subtitulo = reporte.tipo_eleccion_display || 'Consolidado';
                    break;
                case 'delito':
                    icono = 'fa-shield-exclamation';
                    color = 'danger';
                    titulo = reporte.titulo || 'Delito electoral';
                    subtitulo = reporte.tipo_delito || '';
                    break;
                case 'incidente':
                default:
                    icono = 'fa-exclamation-triangle';
                    color = 'warning';
                    titulo = reporte.titulo || 'Incidente electoral';
                    subtitulo = reporte.tipo_incidente || '';
                    break;
            }
            
            const fechaCreacion = new Date(reporte.fecha_creacion_offline || reporte.fecha_creacion);
            const tiempoTranscurrido = this.calcularTiempoTranscurrido(fechaCreacion);
            
            return `
                <div class="reporte-item">
                    <div class="reporte-icon">
                        <i class="fas ${icono} text-${color}"></i>
                    </div>
                    <div class="reporte-info">
                        <div class="reporte-titulo">${titulo}</div>
                        ${subtitulo ? `<div class="reporte-subtitulo text-muted small">${subtitulo}</div>` : ''}
                        <div class="reporte-meta">
                            <span class="badge bg-${color}">${this.getTipoLabel(tipo)}</span>
                            <span class="text-muted small">
                                <i class="fas fa-clock"></i> ${tiempoTranscurrido}
                            </span>
                        </div>
                        ${reporte.intentos_sync > 0 ? `
                            <div class="reporte-intentos">
                                <i class="fas fa-redo"></i> ${reporte.intentos_sync} intento(s)
                            </div>
                        ` : ''}
                    </div>
                    <div class="reporte-status">
                        <i class="fas fa-spinner fa-pulse text-warning"></i>
                    </div>
                </div>
            `;
        }).join('');
    }

    /**
     * Obtener etiqueta del tipo de reporte
     */
    getTipoLabel(tipo) {
        const labels = {
            'formulario_e14': 'E-14',
            'formulario_e24': 'E-24',
            'incidente': 'Incidente',
            'delito': 'Delito'
        };
        return labels[tipo] || tipo;
    }

    /**
     * Calcular tiempo transcurrido
     */
    calcularTiempoTranscurrido(fecha) {
        const ahora = new Date();
        const diff = ahora - fecha;
        
        const minutos = Math.floor(diff / 60000);
        const horas = Math.floor(minutos / 60);
        const dias = Math.floor(horas / 24);
        
        if (dias > 0) {
            return `hace ${dias} día${dias > 1 ? 's' : ''}`;
        } else if (horas > 0) {
            return `hace ${horas} hora${horas > 1 ? 's' : ''}`;
        } else if (minutos > 0) {
            return `hace ${minutos} minuto${minutos > 1 ? 's' : ''}`;
        } else {
            return 'hace un momento';
        }
    }

    /**
     * Toggle panel
     */
    togglePanel() {
        const content = document.getElementById('panel-content');
        const toggleBtn = document.getElementById('panel-toggle-btn');
        
        if (!content || !toggleBtn) return;
        
        if (content.classList.contains('expanded')) {
            content.classList.remove('expanded');
            toggleBtn.innerHTML = '<i class="fas fa-chevron-down"></i>';
        } else {
            content.classList.add('expanded');
            toggleBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
        }
    }

    /**
     * Sincronizar ahora
     */
    async sincronizarAhora() {
        if (!navigator.onLine) {
            if (typeof Toastify !== 'undefined') {
                Toastify({
                    text: '❌ No hay conexión a internet',
                    duration: 3000,
                    gravity: 'top',
                    position: 'right',
                    backgroundColor: '#f44336'
                }).showToast();
            }
            return;
        }
        
        try {
            const btn = document.getElementById('btn-sync-now');
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sincronizando...';
            }
            
            if (window.syncManager) {
                await window.syncManager.forcSync();
            }
            
            if (typeof Toastify !== 'undefined') {
                Toastify({
                    text: '✅ Sincronización completada',
                    duration: 3000,
                    gravity: 'top',
                    position: 'right',
                    backgroundColor: '#4CAF50'
                }).showToast();
            }
            
        } catch (error) {
            console.error('Error sincronizando:', error);
            
            if (typeof Toastify !== 'undefined') {
                Toastify({
                    text: '❌ Error en sincronización',
                    duration: 3000,
                    gravity: 'top',
                    position: 'right',
                    backgroundColor: '#f44336'
                }).showToast();
            }
        } finally {
            const btn = document.getElementById('btn-sync-now');
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-sync-alt"></i> Sincronizar Ahora';
            }
        }
    }

    /**
     * Actualizar estado de conexión
     */
    updateConnectionStatus(online) {
        const panel = document.getElementById('reportes-pendientes-panel');
        if (!panel) return;
        
        if (online) {
            panel.classList.remove('offline');
        } else {
            panel.classList.add('offline');
        }
    }
}

// Crear instancia global
window.reportesPendientesPanel = null;

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        // Esperar a que IndexedDB esté listo
        setTimeout(() => {
            window.reportesPendientesPanel = new ReportesPendientesPanel();
        }, 1000);
    });
} else {
    setTimeout(() => {
        window.reportesPendientesPanel = new ReportesPendientesPanel();
    }, 1000);
}

// Agregar estilos CSS
const reportesPendientesStyle = document.createElement('style');
reportesPendientesStyle.textContent = `
    .reportes-pendientes-panel {
        position: fixed;
        bottom: 20px;
        left: 20px;
        width: 350px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        z-index: 9997;
        border: 2px solid #ff9800;
        opacity: 0;
        transform: translateY(20px);
        pointer-events: none;
        transition: all 0.3s ease;
    }
    
    .reportes-pendientes-panel.visible {
        opacity: 1;
        transform: translateY(0);
        pointer-events: all;
    }
    
    .reportes-pendientes-panel.offline {
        border-color: #f44336;
    }
    
    .panel-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 15px;
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        color: white;
        border-radius: 10px 10px 0 0;
        cursor: pointer;
    }
    
    .reportes-pendientes-panel.offline .panel-header {
        background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
    }
    
    .panel-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 600;
        font-size: 15px;
    }
    
    .panel-title .badge {
        font-size: 12px;
        padding: 4px 8px;
    }
    
    .panel-toggle {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        font-size: 16px;
        padding: 5px;
        transition: transform 0.3s ease;
    }
    
    .panel-toggle:hover {
        transform: scale(1.1);
    }
    
    .panel-content {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.3s ease;
    }
    
    .panel-content.expanded {
        max-height: 500px;
        overflow-y: auto;
    }
    
    .panel-info {
        padding: 12px 15px;
        background-color: #fff3e0;
        border-bottom: 1px solid #ffe0b2;
    }
    
    .panel-info p {
        margin: 0;
        font-size: 13px;
    }
    
    .reportes-list {
        padding: 10px;
        max-height: 300px;
        overflow-y: auto;
    }
    
    .reporte-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px;
        background-color: #f9f9f9;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 3px solid #ff9800;
    }
    
    .reporte-icon {
        font-size: 20px;
        width: 30px;
        text-align: center;
    }
    
    .reporte-info {
        flex: 1;
    }
    
    .reporte-titulo {
        font-weight: 600;
        font-size: 14px;
        color: #333;
        margin-bottom: 2px;
    }
    
    .reporte-subtitulo {
        font-size: 12px;
        margin-bottom: 4px;
        font-style: italic;
    }
    
    .reporte-meta {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 12px;
        margin-top: 4px;
    }
    
    .reporte-meta .badge {
        font-size: 11px;
        padding: 2px 6px;
    }
    
    .reporte-intentos {
        margin-top: 4px;
        font-size: 11px;
        color: #f57c00;
    }
    
    .reporte-status {
        font-size: 18px;
    }
    
    .empty-state {
        text-align: center;
        padding: 30px 20px;
        color: #999;
    }
    
    .empty-state i {
        font-size: 48px;
        margin-bottom: 10px;
        color: #4CAF50;
    }
    
    .empty-state p {
        margin: 0;
        font-size: 14px;
    }
    
    .panel-actions {
        padding: 12px 15px;
        border-top: 1px solid #e0e0e0;
    }
    
    .panel-actions .btn {
        font-size: 13px;
        padding: 8px 12px;
    }
    
    @media (max-width: 768px) {
        .reportes-pendientes-panel {
            width: calc(100% - 40px);
            left: 20px;
            right: 20px;
        }
    }
`;
document.head.appendChild(reportesPendientesStyle);
