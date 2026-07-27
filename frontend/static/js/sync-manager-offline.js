/**
 * SyncManager - Gestión de sincronización offline con retry logic
 */

class SyncManager {
    constructor() {
        this.isOnline = navigator.onLine;
        this.syncInProgress = false;
        this.syncQueue = [];
        this.retryAttempts = 3;
        this.retryDelay = 5000; // 5 segundos
        this.maxRetryDelay = 60000; // 1 minuto
        this.syncInterval = null;
        this.callbacks = {
            onSyncStart: [],
            onSyncComplete: [],
            onSyncError: [],
            onConnectionChange: []
        };
        
        this.init();
    }

    /**
     * Inicializar SyncManager
     */
    init() {
        // Verificar si el rol actual necesita sincronización
        const rolesConSincronizacion = ['testigo', 'coordinador_puesto'];
        const currentUserRol = this.getCurrentUserRole();
        
        if (!rolesConSincronizacion.includes(currentUserRol)) {
            console.log(`SyncManager: Sincronización deshabilitada para rol ${currentUserRol}`);
            return;
        }
        
        // Escuchar cambios de conectividad
        window.addEventListener('online', () => this.handleConnectionChange(true));
        window.addEventListener('offline', () => this.handleConnectionChange(false));
        
        // Iniciar sincronización periódica
        this.startPeriodicSync();
        
        // Sincronizar al cargar la página si hay conexión
        if (this.isOnline) {
            setTimeout(() => this.syncPendingData(), 2000);
        }
        
        console.log('SyncManager inicializado');
    }
    
    /**
     * Obtener rol del usuario actual desde el token
     */
    getCurrentUserRole() {
        try {
            const token = localStorage.getItem('token');
            if (!token) return null;
            
            // Decodificar JWT (simple, sin validación)
            const payload = JSON.parse(atob(token.split('.')[1]));
            return payload.rol || null;
        } catch (error) {
            console.error('Error obteniendo rol del usuario:', error);
            return null;
        }
    }

    /**
     * Manejar cambio de conectividad
     */
    handleConnectionChange(online) {
        const wasOnline = this.isOnline;
        this.isOnline = online;
        
        console.log(`Estado de conexión: ${online ? 'ONLINE' : 'OFFLINE'}`);
        
        // Notificar callbacks
        this.callbacks.onConnectionChange.forEach(callback => {
            try {
                callback(online, wasOnline);
            } catch (error) {
                console.error('Error en callback de conexión:', error);
            }
        });
        
        // Mostrar indicador visual
        this.showConnectionStatus(online);
        
        // Si volvemos online, sincronizar
        if (online && !wasOnline) {
            setTimeout(() => this.syncPendingData(), 1000);
        }
    }

    /**
     * Mostrar estado de conexión
     */
    showConnectionStatus(online) {
        // Remover indicador anterior
        const existingIndicator = document.getElementById('connection-status');
        if (existingIndicator) {
            existingIndicator.remove();
        }
        
        // Crear nuevo indicador
        const indicator = document.createElement('div');
        indicator.id = 'connection-status';
        indicator.className = `connection-indicator ${online ? 'online' : 'offline'}`;
        indicator.innerHTML = `
            <i class="fas ${online ? 'fa-wifi' : 'fa-wifi-slash'}"></i>
            <span>${online ? 'Conectado' : 'Sin conexión'}</span>
        `;
        
        document.body.appendChild(indicator);
        
        // Auto-ocultar después de 3 segundos si está online
        if (online) {
            setTimeout(() => {
                if (indicator.parentNode) {
                    indicator.remove();
                }
            }, 3000);
        }
    }

    /**
     * Guardar reporte offline
     */
    async guardarReporteOffline(reporte) {
        try {
            if (!window.indexedDBService || !window.indexedDBService.db) {
                throw new Error('IndexedDB no disponible');
            }
            
            const id = await window.indexedDBService.guardarReportePendiente(reporte);
            
            // Agregar a cola de sincronización
            this.addToSyncQueue({
                type: 'reporte',
                action: 'create',
                data: reporte,
                localId: id
            });
            
            // Intentar sincronizar inmediatamente si hay conexión
            if (this.isOnline) {
                this.syncPendingData();
            }
            
            return id;
        } catch (error) {
            console.error('Error guardando reporte offline:', error);
            throw error;
        }
    }

    /**
     * Guardar evidencia offline
     */
    async guardarEvidenciaOffline(evidencia, reporteTempId) {
        try {
            if (!window.indexedDBService || !window.indexedDBService.db) {
                throw new Error('IndexedDB no disponible');
            }
            
            const evidenciaConReporte = {
                ...evidencia,
                reporte_temp_id: reporteTempId
            };
            
            const id = await window.indexedDBService.guardarEvidenciaOffline(evidenciaConReporte);
            
            // Agregar a cola de sincronización
            this.addToSyncQueue({
                type: 'evidencia',
                action: 'create',
                data: evidenciaConReporte,
                localId: id
            });
            
            return id;
        } catch (error) {
            console.error('Error guardando evidencia offline:', error);
            throw error;
        }
    }

    /**
     * Agregar item a cola de sincronización
     */
    addToSyncQueue(item) {
        item.id = this.generateQueueId();
        item.attempts = 0;
        item.createdAt = new Date().toISOString();
        
        this.syncQueue.push(item);
        
        // Actualizar indicador de elementos pendientes
        this.updatePendingIndicator();
    }

    /**
     * Sincronizar datos pendientes
     */
    async syncPendingData() {
        if (!this.isOnline || this.syncInProgress) {
            return;
        }
        
        this.syncInProgress = true;
        
        try {
            // Notificar inicio de sincronización
            this.callbacks.onSyncStart.forEach(callback => {
                try {
                    callback();
                } catch (error) {
                    console.error('Error en callback de inicio de sync:', error);
                }
            });
            
            // Obtener reportes pendientes de IndexedDB
            const reportesPendientes = await window.indexedDBService.obtenerReportesPendientes();
            
            console.log(`Sincronizando ${reportesPendientes.length} reportes pendientes`);
            
            let sincronizados = 0;
            let errores = 0;
            
            // Sincronizar cada reporte
            for (const reporte of reportesPendientes) {
                try {
                    await this.syncReporte(reporte);
                    sincronizados++;
                } catch (error) {
                    console.error('Error sincronizando reporte:', error);
                    errores++;
                    
                    // Incrementar intentos
                    await this.incrementarIntentos(reporte.id);
                }
            }
            
            // Procesar cola de sincronización
            await this.processSyncQueue();
            
            // Notificar finalización
            this.callbacks.onSyncComplete.forEach(callback => {
                try {
                    callback({ sincronizados, errores });
                } catch (error) {
                    console.error('Error en callback de finalización de sync:', error);
                }
            });
            
            // Actualizar indicador
            this.updatePendingIndicator();
            
            console.log(`Sincronización completada: ${sincronizados} exitosos, ${errores} errores`);
            
        } catch (error) {
            console.error('Error en sincronización:', error);
            
            this.callbacks.onSyncError.forEach(callback => {
                try {
                    callback(error);
                } catch (err) {
                    console.error('Error en callback de error de sync:', err);
                }
            });
        } finally {
            this.syncInProgress = false;
        }
    }

    /**
     * Sincronizar un reporte específico
     */
    async syncReporte(reporte) {
        const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
        
        if (!token) {
            throw new Error('No hay token de autenticación');
        }
        
        // Preparar datos para envío
        const datosReporte = {
            ...reporte
        };
        
        // Remover campos de sincronización
        delete datosReporte.id;
        delete datosReporte.fecha_creacion_offline;
        delete datosReporte.estado_sync;
        delete datosReporte.intentos_sync;
        delete datosReporte.temp_id;
        
        // Determinar endpoint según tipo
        let endpoint;
        let method = 'POST';
        
        switch (reporte.tipo) {
            case 'incidente':
                endpoint = '/api/incidentes';
                break;
            case 'delito':
                endpoint = '/api/delitos';
                break;
            case 'formulario_e14':
                endpoint = '/api/formularios';
                break;
            case 'formulario_e24':
                endpoint = '/api/formularios/e24';
                break;
            default:
                throw new Error(`Tipo de reporte desconocido: ${reporte.tipo}`);
        }
        
        const response = await fetch(endpoint, {
            method: method,
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datosReporte)
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `HTTP ${response.status}`);
        }
        
        const result = await response.json();
        
        // Marcar como sincronizado
        await window.indexedDBService.marcarReporteSincronizado(
            reporte.id, 
            result.data ? result.data.id : null
        );
        
        // Sincronizar evidencia asociada
        await this.syncEvidenciaReporte(reporte.temp_id, result.data.id);
        
        return result;
    }

    /**
     * Sincronizar evidencia de un reporte
     */
    async syncEvidenciaReporte(reporteTempId, reporteServidorId) {
        try {
            const evidencias = await window.indexedDBService.obtenerEvidenciaOffline(reporteTempId);
            
            for (const evidencia of evidencias) {
                await this.syncEvidencia(evidencia, reporteServidorId);
            }
        } catch (error) {
            console.error('Error sincronizando evidencia:', error);
        }
    }

    /**
     * Sincronizar evidencia específica
     */
    async syncEvidencia(evidencia, reporteServidorId) {
        const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
        
        if (!token) {
            throw new Error('No hay token de autenticación');
        }
        
        // Crear FormData para upload
        const formData = new FormData();
        
        // Convertir base64 a blob si es necesario
        if (evidencia.file_data) {
            const blob = this.base64ToBlob(evidencia.file_data, evidencia.mime_type);
            formData.append('file', blob, evidencia.filename);
        }
        
        formData.append('tipo_reporte', evidencia.tipo_reporte);
        formData.append('reporte_id', reporteServidorId);
        
        const response = await fetch('/api/evidencia/upload', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Error uploading evidencia: ${response.status}`);
        }
        
        return await response.json();
    }

    /**
     * Procesar cola de sincronización
     */
    async processSyncQueue() {
        const itemsToProcess = [...this.syncQueue];
        
        for (let i = itemsToProcess.length - 1; i >= 0; i--) {
            const item = itemsToProcess[i];
            
            try {
                await this.processSyncItem(item);
                
                // Remover de la cola si fue exitoso
                const index = this.syncQueue.findIndex(q => q.id === item.id);
                if (index !== -1) {
                    this.syncQueue.splice(index, 1);
                }
            } catch (error) {
                console.error('Error procesando item de sync:', error);
                
                // Incrementar intentos
                item.attempts++;
                
                // Remover si excede intentos máximos
                if (item.attempts >= this.retryAttempts) {
                    const index = this.syncQueue.findIndex(q => q.id === item.id);
                    if (index !== -1) {
                        this.syncQueue.splice(index, 1);
                    }
                    console.warn('Item removido de cola por exceder intentos:', item);
                }
            }
        }
    }

    /**
     * Procesar item individual de sincronización
     */
    async processSyncItem(item) {
        // Implementar según tipo de item
        switch (item.type) {
            case 'reporte':
                // Ya manejado en syncReporte
                break;
            case 'evidencia':
                // Ya manejado en syncEvidencia
                break;
            default:
                console.warn('Tipo de item desconocido:', item.type);
        }
    }

    /**
     * Incrementar intentos de sincronización
     */
    async incrementarIntentos(reporteId) {
        // Implementar lógica para incrementar intentos en IndexedDB
        // Por ahora solo log
        console.log(`Incrementando intentos para reporte ${reporteId}`);
    }

    /**
     * Iniciar sincronización periódica
     */
    startPeriodicSync() {
        // Sincronizar cada 5 minutos si hay conexión
        this.syncInterval = setInterval(() => {
            if (this.isOnline && !this.syncInProgress) {
                this.syncPendingData();
            }
        }, 5 * 60 * 1000);
    }

    /**
     * Detener sincronización periódica
     */
    stopPeriodicSync() {
        if (this.syncInterval) {
            clearInterval(this.syncInterval);
            this.syncInterval = null;
        }
    }

    /**
     * Actualizar indicador de elementos pendientes
     */
    async updatePendingIndicator() {
        try {
            const stats = await window.indexedDBService.obtenerEstadisticas();
            const pendientes = stats ? stats.reportes_pendientes : 0;
            
            // Buscar o crear indicador
            let indicator = document.getElementById('sync-pending-indicator');
            
            if (pendientes > 0) {
                if (!indicator) {
                    indicator = document.createElement('div');
                    indicator.id = 'sync-pending-indicator';
                    indicator.className = 'sync-pending-badge';
                    document.body.appendChild(indicator);
                }
                
                indicator.innerHTML = `
                    <i class="fas fa-sync-alt ${this.syncInProgress ? 'fa-spin' : ''}"></i>
                    <span>${pendientes}</span>
                `;
                indicator.title = `${pendientes} elemento(s) pendiente(s) de sincronización`;
            } else if (indicator) {
                indicator.remove();
            }
        } catch (error) {
            console.error('Error actualizando indicador:', error);
        }
    }

    /**
     * Registrar callback
     */
    on(event, callback) {
        if (this.callbacks[event]) {
            this.callbacks[event].push(callback);
        }
    }

    /**
     * Obtener estado de sincronización
     */
    async getStatus() {
        const stats = await window.indexedDBService.obtenerEstadisticas();
        
        return {
            isOnline: this.isOnline,
            syncInProgress: this.syncInProgress,
            queueLength: this.syncQueue.length,
            ...stats
        };
    }

    /**
     * Forzar sincronización
     */
    async forcSync() {
        if (this.isOnline) {
            return await this.syncPendingData();
        } else {
            throw new Error('No hay conexión a internet');
        }
    }

    /**
     * Utilidades
     */
    generateQueueId() {
        return 'queue_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    base64ToBlob(base64, mimeType) {
        const byteCharacters = atob(base64.split(',')[1]);
        const byteNumbers = new Array(byteCharacters.length);
        
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        
        const byteArray = new Uint8Array(byteNumbers);
        return new Blob([byteArray], { type: mimeType });
    }
    
    /**
     * Obtener incidentes locales (stub para compatibilidad)
     */
    async getLocalIncidents() {
        try {
            // Intentar obtener de IndexedDB si está disponible
            if (window.indexedDBService) {
                return await window.indexedDBService.getAll('incidentes');
            }
            return [];
        } catch (error) {
            console.warn('Error obteniendo incidentes locales:', error);
            return [];
        }
    }

    /**
     * Obtener delitos locales (stub para compatibilidad)
     */
    async getLocalCrimes() {
        try {
            // Intentar obtener de IndexedDB si está disponible
            if (window.indexedDBService) {
                return await window.indexedDBService.getAll('delitos');
            }
            return [];
        } catch (error) {
            console.warn('Error obteniendo delitos locales:', error);
            return [];
        }
    }
}

// Crear instancia global
window.syncManager = new SyncManager();

// Agregar estilos CSS
const style = document.createElement('style');
style.textContent = `
    .connection-indicator {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 10px 15px;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .connection-indicator.online {
        background-color: #4CAF50;
    }
    
    .connection-indicator.offline {
        background-color: #f44336;
    }
    
    .sync-pending-badge {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #ff9800;
        color: white;
        padding: 10px 12px;
        border-radius: 50px;
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
        font-size: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        cursor: pointer;
        z-index: 9999;
        transition: all 0.3s ease;
    }
    
    .sync-pending-badge:hover {
        background-color: #f57c00;
        transform: scale(1.05);
    }
    
    @media (max-width: 768px) {
        .connection-indicator {
            top: 10px;
            right: 10px;
            font-size: 14px;
        }
        
        .sync-pending-badge {
            bottom: 10px;
            right: 10px;
        }
    }
`;
document.head.appendChild(style);
