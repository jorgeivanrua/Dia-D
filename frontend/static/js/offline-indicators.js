/**
 * OfflineIndicators - Indicadores visuales para estado offline
 */

class OfflineIndicators {
    constructor() {
        this.init();
    }

    /**
     * Inicializar indicadores
     */
    init() {
        this.createOfflineModal();
        this.setupSyncStatusPanel();
        this.setupEventListeners();
        
        // Mostrar estado inicial
        this.updateConnectionStatus(navigator.onLine);
    }

    /**
     * Crear modal de estado offline
     */
    createOfflineModal() {
        const modal = document.createElement('div');
        modal.id = 'offline-modal';
        modal.className = 'offline-modal';
        modal.innerHTML = `
            <div class="offline-modal-content">
                <div class="offline-modal-header">
                    <i class="fas fa-wifi-slash"></i>
                    <h3>Modo Offline</h3>
                </div>
                <div class="offline-modal-body">
                    <p>No hay conexión a internet. Los datos se guardarán localmente y se sincronizarán cuando se restablezca la conexión.</p>
                    <div class="offline-features">
                        <div class="feature-item">
                            <i class="fas fa-save"></i>
                            <span>Reportes guardados localmente</span>
                        </div>
                        <div class="feature-item">
                            <i class="fas fa-camera"></i>
                            <span>Fotos almacenadas offline</span>
                        </div>
                        <div class="feature-item">
                            <i class="fas fa-sync-alt"></i>
                            <span>Sincronización automática al reconectar</span>
                        </div>
                    </div>
                </div>
                <div class="offline-modal-footer">
                    <button class="btn btn-primary" id="offline-modal-close">
                        Entendido
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Event listener para cerrar
        document.getElementById('offline-modal-close').addEventListener('click', () => {
            this.hideOfflineModal();
        });
    }

    /**
     * Configurar panel de estado de sincronización
     */
    setupSyncStatusPanel() {
        const panel = document.createElement('div');
        panel.id = 'sync-status-panel';
        panel.className = 'sync-status-panel';
        panel.innerHTML = `
            <div class="sync-status-header">
                <i class="fas fa-sync-alt"></i>
                <span>Estado de Sincronización</span>
                <button class="sync-status-toggle" id="sync-status-toggle">
                    <i class="fas fa-chevron-up"></i>
                </button>
            </div>
            <div class="sync-status-content" id="sync-status-content">
                <div class="sync-stats">
                    <div class="stat-item">
                        <span class="stat-label">Pendientes:</span>
                        <span class="stat-value" id="stat-pendientes">0</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Sincronizados:</span>
                        <span class="stat-value" id="stat-sincronizados">0</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Evidencia:</span>
                        <span class="stat-value" id="stat-evidencia">0</span>
                    </div>
                </div>
                <div class="sync-actions">
                    <button class="btn btn-sm btn-primary" id="btn-force-sync">
                        <i class="fas fa-sync-alt"></i> Sincronizar Ahora
                    </button>
                    <button class="btn btn-sm btn-secondary" id="btn-clear-synced">
                        <i class="fas fa-trash"></i> Limpiar Sincronizados
                    </button>
                </div>
                <div class="sync-log" id="sync-log">
                    <div class="log-header">Registro de Sincronización</div>
                    <div class="log-content" id="log-content">
                        <!-- Los logs se agregarán aquí -->
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(panel);
        
        // Event listeners
        document.getElementById('sync-status-toggle').addEventListener('click', () => {
            this.toggleSyncPanel();
        });
        
        document.getElementById('btn-force-sync').addEventListener('click', () => {
            this.forceSync();
        });
        
        document.getElementById('btn-clear-synced').addEventListener('click', () => {
            this.clearSyncedData();
        });
    }

    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        // Escuchar cambios de conexión
        window.addEventListener('online', () => {
            this.updateConnectionStatus(true);
        });
        
        window.addEventListener('offline', () => {
            this.updateConnectionStatus(false);
        });
        
        // Escuchar eventos del SyncManager
        if (window.syncManager) {
            window.syncManager.on('onConnectionChange', (online) => {
                this.updateConnectionStatus(online);
            });
            
            window.syncManager.on('onSyncStart', () => {
                this.onSyncStart();
            });
            
            window.syncManager.on('onSyncComplete', (result) => {
                this.onSyncComplete(result);
            });
            
            window.syncManager.on('onSyncError', (error) => {
                this.onSyncError(error);
            });
        }
        
        // Actualizar estadísticas periódicamente
        setInterval(() => {
            this.updateSyncStats();
        }, 10000); // Cada 10 segundos
    }

    /**
     * Actualizar estado de conexión
     */
    updateConnectionStatus(online) {
        // Actualizar indicador en navbar
        this.updateNavbarIndicator(online);
        
        // Mostrar/ocultar modal offline
        if (!online) {
            this.showOfflineModal();
        } else {
            this.hideOfflineModal();
            this.showReconnectedMessage();
        }
        
        // Actualizar panel de sincronización
        this.updateSyncPanel(online);
    }

    /**
     * Actualizar indicador en navbar
     */
    updateNavbarIndicator(online) {
        // Buscar navbar
        const navbar = document.querySelector('.navbar') || document.querySelector('nav');
        if (!navbar) return;
        
        // Remover indicador anterior
        const existingIndicator = navbar.querySelector('.connection-status-navbar');
        if (existingIndicator) {
            existingIndicator.remove();
        }
        
        // Crear nuevo indicador solo si está offline
        if (!online) {
            const indicator = document.createElement('div');
            indicator.className = 'connection-status-navbar offline';
            indicator.innerHTML = `
                <i class="fas fa-wifi-slash"></i>
                <span>Sin conexión</span>
            `;
            
            navbar.appendChild(indicator);
        }
    }

    /**
     * Mostrar modal offline
     */
    showOfflineModal() {
        const modal = document.getElementById('offline-modal');
        if (modal) {
            modal.classList.add('show');
        }
    }

    /**
     * Ocultar modal offline
     */
    hideOfflineModal() {
        const modal = document.getElementById('offline-modal');
        if (modal) {
            modal.classList.remove('show');
        }
    }

    /**
     * Mostrar mensaje de reconexión
     */
    showReconnectedMessage() {
        // Usar Toastify si está disponible
        if (typeof Toastify !== 'undefined') {
            Toastify({
                text: '✅ Conexión restablecida. Sincronizando datos...',
                duration: 3000,
                gravity: 'top',
                position: 'right',
                backgroundColor: '#4CAF50'
            }).showToast();
        }
    }

    /**
     * Actualizar panel de sincronización
     */
    updateSyncPanel(online) {
        const panel = document.getElementById('sync-status-panel');
        if (!panel) return;
        
        if (online) {
            panel.classList.remove('offline');
        } else {
            panel.classList.add('offline');
        }
    }

    /**
     * Toggle panel de sincronización
     */
    toggleSyncPanel() {
        const content = document.getElementById('sync-status-content');
        const toggle = document.getElementById('sync-status-toggle');
        
        if (content.classList.contains('expanded')) {
            content.classList.remove('expanded');
            toggle.innerHTML = '<i class="fas fa-chevron-up"></i>';
        } else {
            content.classList.add('expanded');
            toggle.innerHTML = '<i class="fas fa-chevron-down"></i>';
            this.updateSyncStats();
        }
    }

    /**
     * Actualizar estadísticas de sincronización
     */
    async updateSyncStats() {
        try {
            if (!window.syncManager) return;
            
            const status = await window.syncManager.getStatus();
            
            // Actualizar valores
            const pendientesEl = document.getElementById('stat-pendientes');
            const sincronizadosEl = document.getElementById('stat-sincronizados');
            const evidenciaEl = document.getElementById('stat-evidencia');
            
            if (pendientesEl) pendientesEl.textContent = status.reportes_pendientes || 0;
            if (sincronizadosEl) sincronizadosEl.textContent = status.reportes_sincronizados || 0;
            if (evidenciaEl) evidenciaEl.textContent = status.evidencia_offline || 0;
            
        } catch (error) {
            console.error('Error actualizando estadísticas:', error);
        }
    }

    /**
     * Forzar sincronización
     */
    async forceSync() {
        try {
            if (!window.syncManager) {
                throw new Error('SyncManager no disponible');
            }
            
            const btn = document.getElementById('btn-force-sync');
            const originalText = btn.innerHTML;
            
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sincronizando...';
            
            await window.syncManager.forcSync();
            
            // Mostrar mensaje de éxito
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
            console.error('Error en sincronización forzada:', error);
            
            if (typeof Toastify !== 'undefined') {
                Toastify({
                    text: '❌ Error en sincronización: ' + error.message,
                    duration: 5000,
                    gravity: 'top',
                    position: 'right',
                    backgroundColor: '#f44336'
                }).showToast();
            }
        } finally {
            const btn = document.getElementById('btn-force-sync');
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-sync-alt"></i> Sincronizar Ahora';
        }
    }

    /**
     * Limpiar datos sincronizados
     */
    async clearSyncedData() {
        if (!confirm('¿Está seguro de que desea limpiar los datos ya sincronizados?')) {
            return;
        }
        
        try {
            if (window.indexedDBService) {
                const eliminados = await window.indexedDBService.limpiarDatosSincronizados();
                
                if (typeof Toastify !== 'undefined') {
                    Toastify({
                        text: `✅ ${eliminados} registros eliminados`,
                        duration: 3000,
                        gravity: 'top',
                        position: 'right',
                        backgroundColor: '#4CAF50'
                    }).showToast();
                }
                
                this.updateSyncStats();
            }
        } catch (error) {
            console.error('Error limpiando datos:', error);
        }
    }

    /**
     * Eventos de sincronización
     */
    onSyncStart() {
        this.addLogEntry('Iniciando sincronización...', 'info');
        
        // Actualizar botón
        const btn = document.getElementById('btn-force-sync');
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sincronizando...';
        }
    }

    onSyncComplete(result) {
        this.addLogEntry(
            `Sincronización completada: ${result.sincronizados} exitosos, ${result.errores} errores`,
            result.errores > 0 ? 'warning' : 'success'
        );
        
        // Restaurar botón
        const btn = document.getElementById('btn-force-sync');
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-sync-alt"></i> Sincronizar Ahora';
        }
        
        // Actualizar estadísticas
        this.updateSyncStats();
    }

    onSyncError(error) {
        this.addLogEntry(`Error en sincronización: ${error.message}`, 'error');
        
        // Restaurar botón
        const btn = document.getElementById('btn-force-sync');
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-sync-alt"></i> Sincronizar Ahora';
        }
    }

    /**
     * Agregar entrada al log
     */
    addLogEntry(message, type = 'info') {
        const logContent = document.getElementById('log-content');
        if (!logContent) return;
        
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        entry.innerHTML = `
            <span class="log-time">${new Date().toLocaleTimeString()}</span>
            <span class="log-message">${message}</span>
        `;
        
        logContent.insertBefore(entry, logContent.firstChild);
        
        // Mantener solo las últimas 20 entradas
        while (logContent.children.length > 20) {
            logContent.removeChild(logContent.lastChild);
        }
    }
}

// Crear instancia global
window.offlineIndicators = new OfflineIndicators();

// Agregar estilos CSS
const offlineIndicatorsStyle = document.createElement('style');
offlineIndicatorsStyle.textContent = `
    .offline-modal {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.7);
        z-index: 10000;
        align-items: center;
        justify-content: center;
    }
    
    .offline-modal.show {
        display: flex;
    }
    
    .offline-modal-content {
        background: white;
        border-radius: 12px;
        width: 90%;
        max-width: 500px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .offline-modal-header {
        text-align: center;
        padding: 30px 20px 20px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .offline-modal-header i {
        font-size: 48px;
        color: #f44336;
        margin-bottom: 15px;
        display: block;
    }
    
    .offline-modal-header h3 {
        margin: 0;
        font-size: 24px;
        color: #333;
    }
    
    .offline-modal-body {
        padding: 25px;
    }
    
    .offline-modal-body p {
        text-align: center;
        color: #666;
        margin-bottom: 25px;
        line-height: 1.5;
    }
    
    .offline-features {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    
    .feature-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px;
        background-color: #f9f9f9;
        border-radius: 8px;
    }
    
    .feature-item i {
        color: #4CAF50;
        font-size: 18px;
        width: 20px;
    }
    
    .offline-modal-footer {
        padding: 20px 25px;
        text-align: center;
        border-top: 1px solid #e0e0e0;
    }
    
    .connection-status-navbar {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        background-color: #f44336;
        color: white;
        border-radius: 4px;
        font-size: 14px;
        margin-left: 15px;
    }
    
    .sync-status-panel {
        position: fixed;
        bottom: 80px;
        right: 20px;
        width: 300px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        z-index: 9998;
        border: 1px solid #e0e0e0;
    }
    
    .sync-status-panel.offline {
        border-color: #f44336;
    }
    
    .sync-status-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 15px;
        background-color: #f5f5f5;
        border-radius: 8px 8px 0 0;
        cursor: pointer;
        font-weight: 600;
        font-size: 14px;
    }
    
    .sync-status-panel.offline .sync-status-header {
        background-color: #ffebee;
        color: #c62828;
    }
    
    .sync-status-toggle {
        background: none;
        border: none;
        cursor: pointer;
        color: inherit;
    }
    
    .sync-status-content {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.3s ease;
    }
    
    .sync-status-content.expanded {
        max-height: 400px;
        overflow-y: auto;
    }
    
    .sync-stats {
        padding: 15px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .stat-item {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-size: 14px;
    }
    
    .stat-label {
        color: #666;
    }
    
    .stat-value {
        font-weight: 600;
        color: #333;
    }
    
    .sync-actions {
        padding: 15px;
        display: flex;
        gap: 10px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .sync-actions .btn {
        flex: 1;
        font-size: 12px;
        padding: 8px 10px;
    }
    
    .sync-log {
        padding: 15px;
    }
    
    .log-header {
        font-weight: 600;
        font-size: 13px;
        margin-bottom: 10px;
        color: #333;
    }
    
    .log-content {
        max-height: 150px;
        overflow-y: auto;
    }
    
    .log-entry {
        padding: 6px 8px;
        margin-bottom: 5px;
        border-radius: 4px;
        font-size: 12px;
        display: flex;
        gap: 8px;
    }
    
    .log-entry.info {
        background-color: #e3f2fd;
        color: #1976d2;
    }
    
    .log-entry.success {
        background-color: #e8f5e9;
        color: #388e3c;
    }
    
    .log-entry.warning {
        background-color: #fff3e0;
        color: #f57c00;
    }
    
    .log-entry.error {
        background-color: #ffebee;
        color: #d32f2f;
    }
    
    .log-time {
        font-weight: 600;
        white-space: nowrap;
    }
    
    .log-message {
        flex: 1;
    }
    
    @media (max-width: 768px) {
        .sync-status-panel {
            width: calc(100% - 40px);
            right: 20px;
            left: 20px;
        }
        
        .offline-modal-content {
            width: 95%;
        }
    }
`;
document.head.appendChild(offlineIndicatorsStyle);
