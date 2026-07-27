/**
 * GESTOR DE SINCRONIZACIÓN MEJORADO
 * Sincronización inmediata con soporte offline completo
 * 
 * Características:
 * - Sincronización inmediata al crear/modificar
 * - Cola de sincronización con reintentos
 * - Detección automática de conexión
 * - Sincronización al reconectar
 * - Persistencia en IndexedDB
 */

class SyncManagerMejorado {
    constructor() {
        this.db = null;
        this.syncQueue = [];
        this.syncing = false;
        this.online = navigator.onLine;
        this.maxRetries = 3;
        this.retryDelay = 5000; // 5 segundos
        this.listeners = new Set();
        
        this.init();
    }
    
    // ========================================================================
    // INICIALIZACIÓN
    // ========================================================================
    
    async init() {
        console.log('🔄 SyncManager Mejorado: Inicializando...');
        
        // Inicializar IndexedDB
        await this.initDB();
        
        // Cargar cola pendiente
        await this.loadQueue();
        
        // Setup listeners de conexión
        this.setupConnectionListeners();
        
        // Sincronizar cola si hay conexión
        if (this.online) {
            this.processQueue();
        }
        
        console.log('✅ SyncManager Mejorado: Inicializado');
    }
    
    /**
     * Inicializar IndexedDB para persistencia
     */
    async initDB() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open('SyncDB', 1);
            
            request.onerror = () => reject(request.error);
            request.onsuccess = () => {
                this.db = request.result;
                resolve();
            };
            
            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                
                // Store para cola de sincronización
                if (!db.objectStoreNames.contains('syncQueue')) {
                    const store = db.createObjectStore('syncQueue', { 
                        keyPath: 'id', 
                        autoIncrement: true 
                    });
                    store.createIndex('timestamp', 'timestamp', { unique: false });
                    store.createIndex('type', 'type', { unique: false });
                    store.createIndex('status', 'status', { unique: false });
                }
            };
        });
    }
    
    /**
     * Cargar cola pendiente desde IndexedDB
     */
    async loadQueue() {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['syncQueue'], 'readonly');
            const store = transaction.objectStore('syncQueue');
            const request = store.getAll();
            
            request.onsuccess = () => {
                this.syncQueue = request.result.filter(item => item.status === 'pending');
                console.log(`📋 Cola cargada: ${this.syncQueue.length} items pendientes`);
                resolve();
            };
            
            request.onerror = () => reject(request.error);
        });
    }
    
    /**
     * Setup listeners de conexión
     */
    setupConnectionListeners() {
        window.addEventListener('online', () => {
            console.log('✅ Conexión restaurada');
            this.online = true;
            this.notifyListeners('online');
            
            // Sincronizar cola automáticamente
            this.processQueue();
            
            // Notificar al usuario
            if (window.Utils) {
                Utils.showSuccess('Conexión restaurada. Sincronizando datos...');
            }
        });
        
        window.addEventListener('offline', () => {
            console.log('❌ Sin conexión');
            this.online = false;
            this.notifyListeners('offline');
            
            // Notificar al usuario
            if (window.Utils) {
                Utils.showWarning('Sin conexión. Los datos se guardarán localmente.');
            }
        });
    }
    
    // ========================================================================
    // SINCRONIZACIÓN INMEDIATA
    // ========================================================================
    
    /**
     * Sincronizar formulario inmediatamente
     */
    async syncFormulario(formulario) {
        console.log('📝 Sincronizando formulario inmediatamente...');
        
        const item = {
            type: 'formulario',
            action: 'create',
            data: formulario,
            timestamp: Date.now(),
            status: 'pending',
            retries: 0
        };
        
        // Agregar a cola
        await this.addToQueue(item);
        
        // Intentar sincronizar inmediatamente si hay conexión
        if (this.online) {
            return await this.syncItem(item);
        } else {
            console.log('⏳ Sin conexión. Formulario guardado para sincronizar después.');
            return { success: false, offline: true };
        }
    }
    
    /**
     * Sincronizar incidente inmediatamente
     */
    async syncIncidente(incidente) {
        console.log('⚠️ Sincronizando incidente inmediatamente...');
        
        const item = {
            type: 'incidente',
            action: 'create',
            data: incidente,
            timestamp: Date.now(),
            status: 'pending',
            retries: 0
        };
        
        await this.addToQueue(item);
        
        if (this.online) {
            return await this.syncItem(item);
        } else {
            console.log('⏳ Sin conexión. Incidente guardado para sincronizar después.');
            return { success: false, offline: true };
        }
    }
    
    /**
     * Sincronizar delito inmediatamente
     */
    async syncDelito(delito) {
        console.log('🚨 Sincronizando delito inmediatamente...');
        
        const item = {
            type: 'delito',
            action: 'create',
            data: delito,
            timestamp: Date.now(),
            status: 'pending',
            retries: 0
        };
        
        await this.addToQueue(item);
        
        if (this.online) {
            return await this.syncItem(item);
        } else {
            console.log('⏳ Sin conexión. Delito guardado para sincronizar después.');
            return { success: false, offline: true };
        }
    }
    
    // ========================================================================
    // GESTIÓN DE COLA
    // ========================================================================
    
    /**
     * Agregar item a la cola
     */
    async addToQueue(item) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['syncQueue'], 'readwrite');
            const store = transaction.objectStore('syncQueue');
            const request = store.add(item);
            
            request.onsuccess = () => {
                item.id = request.result;
                this.syncQueue.push(item);
                this.notifyListeners('queueUpdated', { size: this.syncQueue.length });
                console.log(`✅ Item agregado a cola (ID: ${item.id})`);
                resolve(item.id);
            };
            
            request.onerror = () => reject(request.error);
        });
    }
    
    /**
     * Actualizar item en la cola
     */
    async updateQueueItem(item) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['syncQueue'], 'readwrite');
            const store = transaction.objectStore('syncQueue');
            const request = store.put(item);
            
            request.onsuccess = () => {
                // Actualizar en memoria
                const index = this.syncQueue.findIndex(i => i.id === item.id);
                if (index !== -1) {
                    this.syncQueue[index] = item;
                }
                resolve();
            };
            
            request.onerror = () => reject(request.error);
        });
    }
    
    /**
     * Eliminar item de la cola
     */
    async removeFromQueue(itemId) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['syncQueue'], 'readwrite');
            const store = transaction.objectStore('syncQueue');
            const request = store.delete(itemId);
            
            request.onsuccess = () => {
                // Eliminar de memoria
                this.syncQueue = this.syncQueue.filter(i => i.id !== itemId);
                this.notifyListeners('queueUpdated', { size: this.syncQueue.length });
                console.log(`🗑️ Item eliminado de cola (ID: ${itemId})`);
                resolve();
            };
            
            request.onerror = () => reject(request.error);
        });
    }
    
    // ========================================================================
    // PROCESAMIENTO DE COLA
    // ========================================================================
    
    /**
     * Procesar toda la cola
     */
    async processQueue() {
        if (this.syncing || !this.online || this.syncQueue.length === 0) {
            return;
        }
        
        this.syncing = true;
        console.log(`🔄 Procesando cola: ${this.syncQueue.length} items`);
        
        const results = {
            success: 0,
            failed: 0,
            errors: []
        };
        
        // Procesar items uno por uno
        for (const item of [...this.syncQueue]) {
            try {
                const result = await this.syncItem(item);
                
                if (result.success) {
                    results.success++;
                    await this.removeFromQueue(item.id);
                } else {
                    results.failed++;
                    results.errors.push({
                        item: item.type,
                        error: result.error
                    });
                    
                    // Incrementar reintentos
                    item.retries++;
                    
                    if (item.retries >= this.maxRetries) {
                        item.status = 'failed';
                        console.error(`❌ Item falló después de ${this.maxRetries} intentos:`, item);
                    }
                    
                    await this.updateQueueItem(item);
                }
            } catch (error) {
                console.error('Error procesando item:', error);
                results.failed++;
                results.errors.push({
                    item: item.type,
                    error: error.message
                });
            }
        }
        
        this.syncing = false;
        
        // Notificar resultados
        this.notifyListeners('syncCompleted', results);
        
        if (results.success > 0) {
            console.log(`✅ Sincronizados: ${results.success} items`);
            if (window.Utils) {
                Utils.showSuccess(`${results.success} registro(s) sincronizado(s)`);
            }
        }
        
        if (results.failed > 0) {
            console.warn(`⚠️ Fallidos: ${results.failed} items`);
        }
        
        return results;
    }
    
    /**
     * Sincronizar un item específico
     */
    async syncItem(item) {
        try {
            let response;
            
            switch (item.type) {
                case 'formulario':
                    response = await this.syncFormularioToServer(item.data);
                    break;
                    
                case 'incidente':
                    response = await this.syncIncidenteToServer(item.data);
                    break;
                    
                case 'delito':
                    response = await this.syncDelitoToServer(item.data);
                    break;
                    
                default:
                    throw new Error(`Tipo desconocido: ${item.type}`);
            }
            
            return response;
            
        } catch (error) {
            console.error(`Error sincronizando ${item.type}:`, error);
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    // ========================================================================
    // SINCRONIZACIÓN CON SERVIDOR
    // ========================================================================
    
    /**
     * Sincronizar formulario con servidor
     */
    async syncFormularioToServer(formulario) {
        try {
            const response = await APIClient.post('/api/testigo/formularios', formulario);
            
            if (response.success) {
                console.log('✅ Formulario sincronizado con servidor');
                return { success: true, data: response.data };
            } else {
                return { success: false, error: response.error };
            }
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
    
    /**
     * Sincronizar incidente con servidor
     */
    async syncIncidenteToServer(incidente) {
        try {
            const response = await APIClient.post('/api/incidentes', incidente);
            
            if (response.success) {
                console.log('✅ Incidente sincronizado con servidor');
                return { success: true, data: response.data };
            } else {
                return { success: false, error: response.error };
            }
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
    
    /**
     * Sincronizar delito con servidor
     */
    async syncDelitoToServer(delito) {
        try {
            const response = await APIClient.post('/api/delitos', delito);
            
            if (response.success) {
                console.log('✅ Delito sincronizado con servidor');
                return { success: true, data: response.data };
            } else {
                return { success: false, error: response.error };
            }
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
    
    // ========================================================================
    // LISTENERS Y NOTIFICACIONES
    // ========================================================================
    
    /**
     * Agregar listener
     */
    addListener(callback) {
        this.listeners.add(callback);
    }
    
    /**
     * Remover listener
     */
    removeListener(callback) {
        this.listeners.delete(callback);
    }
    
    /**
     * Notificar a listeners
     */
    notifyListeners(event, data = null) {
        this.listeners.forEach(callback => {
            try {
                callback(event, data);
            } catch (error) {
                console.error('Error en listener:', error);
            }
        });
    }
    
    // ========================================================================
    // UTILIDADES
    // ========================================================================
    
    /**
     * Obtener estado de sincronización
     */
    getStatus() {
        return {
            online: this.online,
            syncing: this.syncing,
            queueSize: this.syncQueue.length,
            pendingItems: this.syncQueue.filter(i => i.status === 'pending').length,
            failedItems: this.syncQueue.filter(i => i.status === 'failed').length
        };
    }
    
    /**
     * Limpiar items fallidos
     */
    async clearFailedItems() {
        const failedItems = this.syncQueue.filter(i => i.status === 'failed');
        
        for (const item of failedItems) {
            await this.removeFromQueue(item.id);
        }
        
        console.log(`🗑️ ${failedItems.length} items fallidos eliminados`);
    }
    
    /**
     * Reintentar items fallidos
     */
    async retryFailedItems() {
        const failedItems = this.syncQueue.filter(i => i.status === 'failed');
        
        for (const item of failedItems) {
            item.status = 'pending';
            item.retries = 0;
            await this.updateQueueItem(item);
        }
        
        console.log(`🔄 ${failedItems.length} items marcados para reintentar`);
        
        if (this.online) {
            await this.processQueue();
        }
    }
    
    /**
     * Obtener items de la cola
     */
    getQueueItems() {
        return [...this.syncQueue];
    }
}

// ============================================================================
// INSTANCIA GLOBAL
// ============================================================================

// Crear instancia global
const syncManagerMejorado = new SyncManagerMejorado();

// Exportar para uso global
window.syncManagerMejorado = syncManagerMejorado;

console.log('✅ SyncManager Mejorado cargado');
