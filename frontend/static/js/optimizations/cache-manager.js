/**
 * Cache Manager - Sistema de caché para datos frecuentes
 * Optimización #2: Agregar caché de datos frecuentes
 */

class CacheManager {
    constructor() {
        this.cache = new Map();
        this.cacheExpiry = new Map();
        this.defaultTTL = 5 * 60 * 1000; // 5 minutos por defecto
    }

    /**
     * Guardar datos en caché
     * @param {string} key - Clave del caché
     * @param {any} data - Datos a guardar
     * @param {number} ttl - Tiempo de vida en milisegundos (opcional)
     */
    set(key, data, ttl = this.defaultTTL) {
        this.cache.set(key, data);
        this.cacheExpiry.set(key, Date.now() + ttl);
        console.log(`✅ Cache guardado: ${key} (TTL: ${ttl}ms)`);
    }

    /**
     * Obtener datos del caché
     * @param {string} key - Clave del caché
     * @returns {any|null} - Datos o null si no existe o expiró
     */
    get(key) {
        if (!this.cache.has(key)) {
            return null;
        }

        const expiry = this.cacheExpiry.get(key);
        if (Date.now() > expiry) {
            // Cache expirado
            this.delete(key);
            console.log(`⏰ Cache expirado: ${key}`);
            return null;
        }

        console.log(`✅ Cache hit: ${key}`);
        return this.cache.get(key);
    }

    /**
     * Verificar si existe en caché y no ha expirado
     */
    has(key) {
        return this.get(key) !== null;
    }

    /**
     * Eliminar entrada del caché
     */
    delete(key) {
        this.cache.delete(key);
        this.cacheExpiry.delete(key);
    }

    /**
     * Limpiar todo el caché
     */
    clear() {
        this.cache.clear();
        this.cacheExpiry.clear();
        console.log('🗑️ Cache limpiado completamente');
    }

    /**
     * Limpiar caché expirado
     */
    clearExpired() {
        const now = Date.now();
        let cleared = 0;

        for (const [key, expiry] of this.cacheExpiry.entries()) {
            if (now > expiry) {
                this.delete(key);
                cleared++;
            }
        }

        if (cleared > 0) {
            console.log(`🗑️ ${cleared} entradas de cache expiradas eliminadas`);
        }
    }

    /**
     * Obtener estadísticas del caché
     */
    getStats() {
        return {
            size: this.cache.size,
            keys: Array.from(this.cache.keys())
        };
    }
}

// Instancia global
window.cacheManager = new CacheManager();

// Limpiar cache expirado cada 2 minutos
setInterval(() => {
    window.cacheManager.clearExpired();
}, 2 * 60 * 1000);
