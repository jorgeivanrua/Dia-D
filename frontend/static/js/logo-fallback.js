/**
 * Sistema de fallback para logos de partidos
 * Genera SVG localmente cuando las imágenes no cargan
 */

(function() {
    'use strict';

    // Colores de partidos políticos
    const COLORES_PARTIDOS = {
        'PL': { bg: '#FF0000', text: '#FFFFFF', nombre: 'PL' },
        'LIBERAL': { bg: '#FF0000', text: '#FFFFFF', nombre: 'PL' },
        'PC': { bg: '#0000FF', text: '#FFFFFF', nombre: 'PC' },
        'CONSERVADOR': { bg: '#0000FF', text: '#FFFFFF', nombre: 'PC' },
        'VERDE': { bg: '#00FF00', text: '#000000', nombre: 'AV' },
        'ALIANZA_VERDE': { bg: '#00FF00', text: '#000000', nombre: 'AV' },
        'AV': { bg: '#00FF00', text: '#000000', nombre: 'AV' },
        'CD': { bg: '#0080FF', text: '#FFFFFF', nombre: 'CD' },
        'CENTRO_DEM': { bg: '#0080FF', text: '#FFFFFF', nombre: 'CD' },
        'CENTRO_DEMOCRATICO': { bg: '#0080FF', text: '#FFFFFF', nombre: 'CD' },
        'CR': { bg: '#FFA500', text: '#FFFFFF', nombre: 'CR' },
        'CAMBIO_RADICAL': { bg: '#FFA500', text: '#FFFFFF', nombre: 'CR' },
        'U': { bg: '#808080', text: '#FFFFFF', nombre: 'U' },
        'PARTIDO_U': { bg: '#808080', text: '#FFFFFF', nombre: 'U' },
        'LA_U': { bg: '#808080', text: '#FFFFFF', nombre: 'U' },
        'MIRA': { bg: '#800080', text: '#FFFFFF', nombre: 'MIRA' },
        'COMUNES': { bg: '#8B0000', text: '#FFFFFF', nombre: 'COM' },
        'FARC': { bg: '#8B0000', text: '#FFFFFF', nombre: 'COM' },
        'POLO': { bg: '#FFFF00', text: '#000000', nombre: 'POLO' },
        'POLO_DEMOCRATICO': { bg: '#FFFF00', text: '#000000', nombre: 'POLO' },
        'PDA': { bg: '#FFFF00', text: '#000000', nombre: 'POLO' },
        'PACTO_HISTORICO': { bg: '#FF1493', text: '#FFFFFF', nombre: 'PH' },
        'PH': { bg: '#FF1493', text: '#FFFFFF', nombre: 'PH' }
    };

    /**
     * Generar SVG para logo de partido
     */
    function generarLogoSVG(partidoCodigo, width = 100, height = 100) {
        const partido = COLORES_PARTIDOS[partidoCodigo.toUpperCase()] || {
            bg: '#CCCCCC',
            text: '#000000',
            nombre: partidoCodigo.substring(0, 4).toUpperCase()
        };

        const svg = `
            <svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
                <rect width="100%" height="100%" fill="${partido.bg}"/>
                <text 
                    x="50%" 
                    y="50%" 
                    dominant-baseline="middle" 
                    text-anchor="middle" 
                    font-family="Arial, sans-serif" 
                    font-size="24" 
                    font-weight="bold" 
                    fill="${partido.text}">
                    ${partido.nombre}
                </text>
            </svg>
        `;

        return 'data:image/svg+xml;base64,' + btoa(svg);
    }

    /**
     * Reemplazar imágenes fallidas con SVG
     */
    function aplicarFallback() {
        // Buscar todas las imágenes de logos
        const imagenes = document.querySelectorAll('img[src*="placeholder"], img[src*="logo"]');
        
        imagenes.forEach(img => {
            // Agregar listener para errores ANTES de que ocurran
            // Esto evita que el error aparezca en la consola
            if (!img.dataset.fallbackConfigured) {
                img.dataset.fallbackConfigured = 'true';
                
                img.addEventListener('error', function(e) {
                    // Prevenir que el error se propague a la consola
                    e.preventDefault();
                    e.stopPropagation();
                    
                    const partidoCodigo = this.alt || this.dataset.partido || 'PARTIDO';
                    this.src = generarLogoSVG(partidoCodigo);
                    this.onerror = null; // Evitar loop infinito
                }, true); // useCapture = true para capturar antes
            }
            
            // Si la imagen ya tiene error o no ha cargado
            if (!img.complete || img.naturalHeight === 0) {
                const partidoCodigo = img.alt || img.dataset.partido || 'PARTIDO';
                img.src = generarLogoSVG(partidoCodigo);
            }
        });
    }

    /**
     * Obtener URL de logo (SVG local)
     */
    function getLogoURL(partidoCodigo, width = 100, height = 100) {
        return generarLogoSVG(partidoCodigo, width, height);
    }

    // Aplicar fallback cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', aplicarFallback);
    } else {
        aplicarFallback();
    }

    // Aplicar fallback también después de actualizaciones dinámicas
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                aplicarFallback();
            }
        });
    });

    // Observar cambios en el body
    if (document.body) {
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // Exportar función para uso global
    window.LogoFallback = {
        generarLogoSVG,
        getLogoURL,
        aplicarFallback
    };

})();
