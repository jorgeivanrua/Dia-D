/**
 * IndexedDBService - Servicio para almacenamiento offline
 */

class IndexedDBService {
    constructor() {
        this.dbName = 'ElectoralSystemDB';
        this.dbVersion = 1;
        this.db = null;
        this.isSupported = this.checkSupport();
    }

    /**
     * Verificar soporte de IndexedDB
     */
    checkSupport() {
        return 'indexedDB' in window;
    }

    /**
     * Inicializar base de datos
     */
    async init() {
        if (!this.isSupported) {
            console.warn('IndexedDB no está soportado en este navegador');
            return false;
        }

        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, this.dbVersion);

            request.onerror = () => {
                console.error('Error abriendo IndexedDB:', request.error);
                reject(request.error);
            };

            request.onsuccess = () => {
                this.db = request.result;
                console.log('IndexedDB inicializado correctamente');
                resolve(true);
            };

            request.onupgradeneeded = (event) => {
                this.db = event.target.result;
                this.createStores();
            };
        });
    }

    /**
     * Crear object stores
     */
    createStores() {
        // Store para reportes pendientes de sincronización
        if (!this.db.objectStoreNames.contains('reportes_pendientes')) {
            const reportesStore = this.db.createObjectStore('reportes_pendientes', {
                keyPath: 'id',
                autoIncrement: true
            });
            reportesStore.createIndex('tipo', 'tipo', { unique: false });
            reportesStore.createIndex('fecha_creacion', 'fecha_creacion', { unique: false });
            reportesStore.createIndex('estado_sync', 'estado_sync', { unique: false });
        }

        // Store para evidencia fotográfica offline
        if (!this.db.objectStoreNames.contains('evidencia_offline')) {
            const evidenciaStore = this.db.createObjectStore('evidencia_offline', {
                keyPath: 'id',
                autoIncrement: true
            });
            evidenciaStore.createIndex('reporte_temp_id', 'reporte_temp_id', { unique: false });
            evidenciaStore.createIndex('fecha_captura', 'fecha_captura', { unique: false });
        }

        // Store para configuración offline
        if (!this.db.objectStoreNames.contains('configuracion_offline')) {
            this.db.createObjectStore('configuracion_offline', {
                keyPath: 'key'
            });
        }

        // Store para datos de referencia (puestos, mesas, etc.)
        if (!this.db.objectStoreNames.contains('datos_referencia')) {
            const refStore = this.db.createObjectStore('datos_referencia', {
                keyPath: 'id'
            });
            refStore.createIndex('tipo', 'tipo', { unique: false });
            refStore.createIndex('fecha_actualizacion', 'fecha_actualizacion', { unique: false });
        }

        console.log('Object stores creados correctamente');
    }

    /**
     * Guardar reporte pendiente de sincronización
     */
    async guardarReportePendiente(reporte) {
        if (!this.db) {
            throw new Error('Base de datos no inicializada');
        }

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['reportes_pendientes'], 'readwrite');
            const store = transaction.objectStore('reportes_pendientes');

            // Agregar metadatos de sincronización
            const reporteConSync = {
                ...reporte,
                fecha_creacion_offline: new Date().toISOString(),
                estado_sync: 'pendiente',
                intentos_sync: 0,
                temp_id: this.generateTempId()
            };

            const request = store.add(reporteConSync);

            request.onsuccess = () => {
                console.log('Reporte guardado offline:', request.result);
                resolve(request.result);
            };

            request.onerror = () => {
                console.error('Error guardando reporte offline:', request.error);
                reject(request.error);
            };
        });
    }

    /**
     * Obtener reportes pendientes de sincronización
     */
    async obtenerReportesPendientes() {
        if (!this.db) {
            return [];
        }

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['reportes_pendientes'], 'readonly');
            const store = transaction.objectStore('reportes_pendientes');
            const index = store.index('estado_sync');
            const request = index.getAll('pendiente');

            request.onsuccess = () => {
                resolve(request.result || []);
            };

            request.onerror = () => {
                reject(request.error);
            };
        });
    }

    /**
     * Marcar reporte como sincronizado
     */
    async marcarReporteSincronizado(id, servidorId = null) {
        if (!this.db) {
            return false;
        }

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['reportes_pendientes'], 'readwrite');
            const store = transaction.objectStore('reportes_pendientes');
            const request = store.get(id);

            request.onsuccess = () => {
                const reporte = request.result;
                if (reporte) {
                    reporte.estado_sync = 'sincronizado';
                    reporte.fecha_sincronizacion = new Date().toISOString();
                    if (servidorId) {
                        reporte.servidor_id = servidorId;
                    }

                    const updateRequest = store.put(reporte);
                    updateRequest.onsuccess = () => resolve(true);
                    updateRequest.onerror = () => reject(updateRequest.error);
                } else {
                    resolve(false);
                }
            };

            request.onerror = () => {
                reject(request.error);
            };
        });
    }

    /**
     * Guardar evidencia offline
     */
    async guardarEvidenciaOffline(evidencia) {
        if (!this.db) {
            throw new Error('Base de datos no inicializada');
        }

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['evidencia_offline'], 'readwrite');
            const store = transaction.objectStore('evidencia_offline');

            const evidenciaConMetadata = {
                ...evidencia,
                fecha_guardado_offline: new Date().toISOString(),
                estado_sync: 'pendiente'
            };

            const request = store.add(evidenciaConMetadata);

            request.onsuccess = () => {
                resolve(request.result);
            };

            request.onerror = () => {
                reject(request.error);
            };
        });
    }

    /**
     * Obtener evidencia offline por reporte
     */
    async obtenerEvidenciaOffline(reporteTempId) {
        if (!this.db) {
            return [];
        }

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['evidencia_offline'], 'readonly');
            const store = transaction.objectStore('evidencia_offline');
            const index = store.index('reporte_temp_id');
            const request = index.getAll(reporteTempId);

            request.onsuccess = () => {
                resolve(request.result || []);
            };

            request.onerror = () => {
                reject(request.error);
            };
        });
    }

    /**
     * Guardar configuración offline
     */
    async guardarConfiguracion(key, value) {
        if (!this.db) {
            return false;
        }

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['configuracion_offline'], 'readwrite');
            const store = transaction.objectStore('configuracion_offline');

            const config = {
                key: key,
                value: value,
                fecha_actualizacion: new Date().toISOString()
            };

            const request = store.put(config);

            request.onsuccess = () => {
                resolve(true);
            };

            request.onerror = () => {
                reject(request.error);
            };
        });
    }

    /**
     * Obtener configuración offline
     */
    async obtenerConfiguracion(key) {
        if (!this.db) {
            return null;
        }

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['configuracion_offline'], 'readonly');
            const store = transaction.objectStore('configuracion_offline');
            const request = store.get(key);

            request.onsuccess = () => {
                const result = request.result;
                resolve(result ? result.value : null);
            };

            request.onerror = () => {
                reject(request.error);
            };
        });
    }

    /**
     * Guardar datos de referencia
     */
    async guardarDatosReferencia(tipo, datos) {
        if (!this.db) {
            return false;
        }

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['datos_referencia'], 'readwrite');
            const store = transaction.objectStore('datos_referencia');

            const registro = {
                id: tipo,
                tipo: tipo,
                datos: datos,
                fecha_actualizacion: new Date().toISOString()
            };

            const request = store.put(registro);

            request.onsuccess = () => {
                resolve(true);
            };

            request.onerror = () => {
                reject(request.error);
            };
        });
    }

    /**
     * Obtener datos de referencia
     */
    async obtenerDatosReferencia(tipo) {
        if (!this.db) {
            return null;
        }

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['datos_referencia'], 'readonly');
            const store = transaction.objectStore('datos_referencia');
            const request = store.get(tipo);

            request.onsuccess = () => {
                const result = request.result;
                resolve(result ? result.datos : null);
            };

            request.onerror = () => {
                reject(request.error);
            };
        });
    }

    /**
     * Limpiar datos sincronizados antiguos
     */
    async limpiarDatosSincronizados(diasAntiguedad = 7) {
        if (!this.db) {
            return 0;
        }

        const fechaLimite = new Date();
        fechaLimite.setDate(fechaLimite.getDate() - diasAntiguedad);

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['reportes_pendientes'], 'readwrite');
            const store = transaction.objectStore('reportes_pendientes');
            const index = store.index('estado_sync');
            const request = index.openCursor('sincronizado');
            let eliminados = 0;

            request.onsuccess = (event) => {
                const cursor = event.target.result;
                if (cursor) {
                    const reporte = cursor.value;
                    const fechaSincronizacion = new Date(reporte.fecha_sincronizacion);
                    
                    if (fechaSincronizacion < fechaLimite) {
                        cursor.delete();
                        eliminados++;
                    }
                    cursor.continue();
                } else {
                    resolve(eliminados);
                }
            };

            request.onerror = () => {
                reject(request.error);
            };
        });
    }

    /**
     * Obtener estadísticas de almacenamiento
     */
    async obtenerEstadisticas() {
        if (!this.db) {
            return null;
        }

        const stats = {
            reportes_pendientes: 0,
            reportes_sincronizados: 0,
            evidencia_offline: 0,
            datos_referencia: 0
        };

        // Contar reportes pendientes
        const reportesPendientes = await this.obtenerReportesPendientes();
        stats.reportes_pendientes = reportesPendientes.length;

        // Contar reportes sincronizados
        const reportesSincronizados = await new Promise((resolve) => {
            const transaction = this.db.transaction(['reportes_pendientes'], 'readonly');
            const store = transaction.objectStore('reportes_pendientes');
            const index = store.index('estado_sync');
            const request = index.count('sincronizado');
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => resolve(0);
        });
        stats.reportes_sincronizados = reportesSincronizados;

        // Contar evidencia offline
        const evidenciaCount = await new Promise((resolve) => {
            const transaction = this.db.transaction(['evidencia_offline'], 'readonly');
            const store = transaction.objectStore('evidencia_offline');
            const request = store.count();
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => resolve(0);
        });
        stats.evidencia_offline = evidenciaCount;

        // Contar datos de referencia
        const datosRefCount = await new Promise((resolve) => {
            const transaction = this.db.transaction(['datos_referencia'], 'readonly');
            const store = transaction.objectStore('datos_referencia');
            const request = store.count();
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => resolve(0);
        });
        stats.datos_referencia = datosRefCount;

        return stats;
    }

    /**
     * Generar ID temporal
     */
    generateTempId() {
        return 'temp_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    /**
     * Cerrar conexión
     */
    close() {
        if (this.db) {
            this.db.close();
            this.db = null;
        }
    }
}

// Crear instancia global
window.indexedDBService = new IndexedDBService();

// Auto-inicializar
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', async () => {
        try {
            await window.indexedDBService.init();
        } catch (error) {
            console.error('Error inicializando IndexedDB:', error);
        }
    });
} else {
    window.indexedDBService.init().catch(error => {
        console.error('Error inicializando IndexedDB:', error);
    });
}
