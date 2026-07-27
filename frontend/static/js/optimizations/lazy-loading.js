/**
 * Lazy Loading Manager - Carga diferida de imágenes
 * Optimización #3: Optimizar carga de imágenes (lazy loading)
 */

class LazyLoadManager {
    constructor(options = {}) {
        this.options = {
            rootMargin: options.rootMargin || '50px',
            threshold: options.threshold || 0.01,
            loadingClass: options.loadingClass || 'lazy-loading',
            loadedClass: options.loadedClass || 'lazy-loaded',
            errorClass: options.errorClass || 'lazy-error',
            placeholder: options.placeholder || 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"%3E%3Crect fill="%23f0f0f0" width="100" height="100"/%3E%3Ctext x="50" y="50" text-anchor="middle" dy=".3em" fill="%23999"%3ECargando...%3C/text%3E%3C/svg%3E'
        };

        this.observer = null;
        this.init();
    }

    /**
     * Inicializar Intersection Observer
     */
    init() {
        if (!('IntersectionObserver' in window)) {
            console.warn('IntersectionObserver no soportado, cargando todas las imágenes');
            this.loadAllImages();
            return;
        }

        this.observer = new IntersectionObserver(
            (entries) => this.handleIntersection(entries),
            {
                rootMargin: this.options.rootMargin,
                threshold: this.options.threshold
            }
        );

        this.observeImages();
    }

    /**
     * Observar todas las imágenes lazy
     */
    observeImages() {
        const images = document.querySelectorAll('img[data-src], img[data-lazy]');
        images.forEach(img => {
            this.observer.observe(img);
            img.classList.add(this.options.loadingClass);
        });
    }

    /**
     * Manejar intersección
     */
    handleIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                this.loadImage(entry.target);
                this.observer.unobserve(entry.target);
            }
        });
    }

    /**
     * Cargar imagen
     */
    loadImage(img) {
        const src = img.dataset.src || img.dataset.lazy;
        if (!src) return;

        // Crear nueva imagen para precargar
        const tempImg = new Image();

        tempImg.onload = () => {
            img.src = src;
            img.classList.remove(this.options.loadingClass);
            img.classList.add(this.options.loadedClass);
            
            // Remover data attributes
            delete img.dataset.src;
            delete img.dataset.lazy;
        };

        tempImg.onerror = () => {
            img.classList.remove(this.options.loadingClass);
            img.classList.add(this.options.errorClass);
            img.alt = 'Error al cargar imagen';
        };

        tempImg.src = src;
    }

    /**
     * Cargar todas las imágenes (fallback)
     */
    loadAllImages() {
        const images = document.querySelectorAll('img[data-src], img[data-lazy]');
        images.forEach(img => this.loadImage(img));
    }

    /**
     * Actualizar observador (para imágenes dinámicas)
     */
    update() {
        if (this.observer) {
            this.observeImages();
        }
    }

    /**
     * Destruir observador
     */
    destroy() {
        if (this.observer) {
            this.observer.disconnect();
        }
    }
}

// Instancia global
window.lazyLoadManager = new LazyLoadManager();

// Actualizar cuando se agreguen nuevas imágenes dinámicamente
const originalAppendChild = Element.prototype.appendChild;
Element.prototype.appendChild = function(child) {
    const result = originalAppendChild.call(this, child);
    if (child.tagName === 'IMG' && (child.dataset.src || child.dataset.lazy)) {
        window.lazyLoadManager.update();
    }
    return result;
};
