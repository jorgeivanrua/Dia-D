/**
 * Tour de Bienvenida para Nuevos Usuarios
 * Usa Intro.js para guiar a los usuarios por primera vez
 */

class WelcomeTour {
    constructor() {
        this.tourKey = 'electoral_tour_completed';
        this.userRole = null;
    }

    /**
     * Verificar si el usuario ya completó el tour
     */
    hasCompletedTour() {
        return localStorage.getItem(this.tourKey) === 'true';
    }

    /**
     * Marcar el tour como completado
     */
    markTourCompleted() {
        localStorage.setItem(this.tourKey, 'true');
    }

    /**
     * Resetear el tour (para testing)
     */
    resetTour() {
        localStorage.removeItem(this.tourKey);
    }

    /**
     * Iniciar tour según el rol del usuario
     */
    async startTour(role) {
        this.userRole = role;

        // Si ya completó el tour, no mostrar
        if (this.hasCompletedTour()) {
            return;
        }

        // Esperar a que la página cargue completamente
        await this.waitForPageLoad();

        // Iniciar tour según rol
        switch (role) {
            case 'testigo_electoral':
                this.startTestigoTour();
                break;
            case 'coordinador_puesto':
            case 'coordinador_municipal':
            case 'coordinador_departamental':
                this.startCoordinadorTour();
                break;
            case 'monitoreo':
                this.startMonitoreoTour();
                break;
            case 'auditor_electoral':
                this.startAuditorTour();
                break;
            default:
                this.startGeneralTour();
        }
    }

    /**
     * Esperar a que la página cargue
     */
    waitForPageLoad() {
        return new Promise((resolve) => {
            if (document.readyState === 'complete') {
                setTimeout(resolve, 500);
            } else {
                window.addEventListener('load', () => {
                    setTimeout(resolve, 500);
                });
            }
        });
    }

    /**
     * Tour para Testigos Electorales
     */
    startTestigoTour() {
        const steps = [
            {
                element: document.querySelector('.dashboard-header') || document.body,
                intro: `
                    <div class="tour-welcome">
                        <h3>¡Bienvenido, Testigo Electoral! 👋</h3>
                        <p>Te guiaremos por las funciones principales del sistema.</p>
                    </div>
                `,
                position: 'bottom'
            },
            {
                element: document.querySelector('#puesto') || document.querySelector('.location-selector'),
                intro: `
                    <h4>1. Selecciona tu Puesto de Votación</h4>
                    <p>Primero, selecciona el puesto donde estás asignado.</p>
                    <p><strong>Importante:</strong> Debes estar físicamente en el puesto para verificar tu presencia.</p>
                `,
                position: 'bottom'
            },
            {
                element: document.querySelector('#mesa') || document.querySelector('.mesa-selector'),
                intro: `
                    <h4>2. Selecciona la Mesa</h4>
                    <p>Después de seleccionar el puesto, elige la mesa específica que vas a monitorear.</p>
                `,
                position: 'bottom'
            },
            {
                element: document.querySelector('.verificar-presencia-btn') || document.querySelector('[onclick*="verificarPresencia"]'),
                intro: `
                    <h4>3. Verifica tu Presencia</h4>
                    <p>Haz clic aquí para verificar que estás en el puesto de votación.</p>
                    <p><i class="bi bi-geo-alt"></i> El sistema usará tu ubicación GPS para confirmar.</p>
                `,
                position: 'top'
            },
            {
                element: document.querySelector('.formulario-e14') || document.querySelector('[data-bs-target*="formularioModal"]'),
                intro: `
                    <h4>4. Registra Formularios E-14</h4>
                    <p>Una vez verificada tu presencia, podrás registrar los formularios E-14.</p>
                    <p><strong>Recuerda:</strong> Ingresa los datos exactamente como aparecen en el acta física.</p>
                `,
                position: 'left'
            },
            {
                element: document.querySelector('.mis-formularios') || document.querySelector('.table'),
                intro: `
                    <h4>5. Revisa tus Formularios</h4>
                    <p>Aquí verás todos los formularios que has registrado.</p>
                    <p>Estados posibles:</p>
                    <ul>
                        <li><span class="badge bg-warning">Pendiente</span> - En revisión</li>
                        <li><span class="badge bg-success">Validado</span> - Aprobado</li>
                        <li><span class="badge bg-danger">Rechazado</span> - Requiere corrección</li>
                    </ul>
                `,
                position: 'top'
            },
            {
                element: document.querySelector('.navbar') || document.querySelector('nav'),
                intro: `
                    <h4>6. Menú de Navegación</h4>
                    <p>Usa el menú para acceder a:</p>
                    <ul>
                        <li><i class="bi bi-house"></i> Dashboard</li>
                        <li><i class="bi bi-file-earmark"></i> Mis Formularios</li>
                        <li><i class="bi bi-bell"></i> Notificaciones</li>
                        <li><i class="bi bi-person"></i> Mi Perfil</li>
                    </ul>
                `,
                position: 'bottom'
            },
            {
                intro: `
                    <div class="tour-complete">
                        <h3>¡Tour Completado! 🎉</h3>
                        <p>Ya estás listo para usar el sistema.</p>
                        <p><strong>Consejos finales:</strong></p>
                        <ul>
                            <li>Mantén tu teléfono cargado</li>
                            <li>Verifica tu conexión a internet</li>
                            <li>Toma fotos claras de los formularios</li>
                            <li>Contacta a tu coordinador si tienes dudas</li>
                        </ul>
                        <p class="text-muted">Puedes volver a ver este tour desde el menú de ayuda.</p>
                    </div>
                `
            }
        ];

        this.showTour(steps);
    }

    /**
     * Tour para Coordinadores
     */
    startCoordinadorTour() {
        const steps = [
            {
                intro: `
                    <div class="tour-welcome">
                        <h3>¡Bienvenido, Coordinador! 👋</h3>
                        <p>Te mostraremos las funciones principales de coordinación.</p>
                    </div>
                `
            },
            {
                element: document.querySelector('.dashboard-stats') || document.querySelector('.card'),
                intro: `
                    <h4>1. Panel de Métricas</h4>
                    <p>Aquí verás las estadísticas en tiempo real de tu área:</p>
                    <ul>
                        <li>Formularios registrados</li>
                        <li>Testigos activos</li>
                        <li>Cobertura de puestos</li>
                    </ul>
                `
            },
            {
                element: document.querySelector('.formularios-pendientes') || document.querySelector('.table'),
                intro: `
                    <h4>2. Validación de Formularios</h4>
                    <p>Tu función principal es validar los formularios E-14 enviados por los testigos.</p>
                    <p><strong>Acciones disponibles:</strong></p>
                    <ul>
                        <li><i class="bi bi-check-circle text-success"></i> Validar</li>
                        <li><i class="bi bi-x-circle text-danger"></i> Rechazar</li>
                        <li><i class="bi bi-eye text-info"></i> Ver detalles</li>
                    </ul>
                `
            },
            {
                element: document.querySelector('.testigos-activos'),
                intro: `
                    <h4>3. Monitoreo de Testigos</h4>
                    <p>Visualiza la ubicación y estado de todos tus testigos en tiempo real.</p>
                    <p><i class="bi bi-geo-alt"></i> Usa el mapa para ver su distribución geográfica.</p>
                `
            },
            {
                intro: `
                    <div class="tour-complete">
                        <h3>¡Listo para Coordinar! 🎯</h3>
                        <p>Recuerda:</p>
                        <ul>
                            <li>Valida los formularios rápidamente</li>
                            <li>Mantén comunicación con tus testigos</li>
                            <li>Reporta cualquier irregularidad</li>
                        </ul>
                    </div>
                `
            }
        ];

        this.showTour(steps);
    }

    /**
     * Tour para Monitoreo
     */
    startMonitoreoTour() {
        const steps = [
            {
                intro: `
                    <div class="tour-welcome">
                        <h3>¡Bienvenido al Dashboard de Monitoreo! 📊</h3>
                        <p>Aquí podrás supervisar toda la operación electoral en tiempo real.</p>
                    </div>
                `
            },
            {
                element: document.querySelector('.metricas-principales'),
                intro: `
                    <h4>1. Métricas Principales</h4>
                    <p>Vista general de toda la operación:</p>
                    <ul>
                        <li>Total de formularios</li>
                        <li>Testigos activos</li>
                        <li>Cobertura territorial</li>
                        <li>Alertas y notificaciones</li>
                    </ul>
                `
            },
            {
                element: document.querySelector('#map') || document.querySelector('.leaflet-container'),
                intro: `
                    <h4>2. Mapa Interactivo</h4>
                    <p>Visualiza la ubicación de todos los testigos y coordinadores.</p>
                    <p><strong>Funciones:</strong></p>
                    <ul>
                        <li>Zoom y navegación</li>
                        <li>Filtros por departamento</li>
                        <li>Información detallada al hacer clic</li>
                    </ul>
                `
            },
            {
                element: document.querySelector('.graficos-dashboard'),
                intro: `
                    <h4>3. Gráficos y Análisis</h4>
                    <p>Analiza tendencias y patrones:</p>
                    <ul>
                        <li>Formularios por hora</li>
                        <li>Distribución por departamento</li>
                        <li>Estados de validación</li>
                    </ul>
                `
            },
            {
                element: document.querySelector('.actualizacion-automatica'),
                intro: `
                    <h4>4. Actualización Automática</h4>
                    <p>El dashboard se actualiza cada 30 segundos automáticamente.</p>
                    <p><i class="bi bi-arrow-clockwise"></i> También puedes actualizar manualmente.</p>
                `
            },
            {
                intro: `
                    <div class="tour-complete">
                        <h3>¡Dashboard Listo! 🚀</h3>
                        <p>Ahora puedes monitorear toda la operación electoral en tiempo real.</p>
                    </div>
                `
            }
        ];

        this.showTour(steps);
    }

    /**
     * Tour para Auditores
     */
    startAuditorTour() {
        const steps = [
            {
                intro: `
                    <div class="tour-welcome">
                        <h3>¡Bienvenido, Auditor Electoral! 🔍</h3>
                        <p>Tu rol es supervisar y auditar todo el proceso.</p>
                    </div>
                `
            },
            {
                element: document.querySelector('.audit-logs'),
                intro: `
                    <h4>1. Registro de Auditoría</h4>
                    <p>Accede al historial completo de todas las acciones del sistema.</p>
                    <p>Puedes filtrar por:</p>
                    <ul>
                        <li>Usuario</li>
                        <li>Fecha y hora</li>
                        <li>Tipo de acción</li>
                        <li>Resultado</li>
                    </ul>
                `
            },
            {
                element: document.querySelector('.reportes'),
                intro: `
                    <h4>2. Reportes y Análisis</h4>
                    <p>Genera reportes detallados para auditoría:</p>
                    <ul>
                        <li>Formularios por período</li>
                        <li>Actividad de usuarios</li>
                        <li>Inconsistencias detectadas</li>
                    </ul>
                `
            },
            {
                intro: `
                    <div class="tour-complete">
                        <h3>¡Listo para Auditar! ✅</h3>
                        <p>Mantén la transparencia y confiabilidad del proceso electoral.</p>
                    </div>
                `
            }
        ];

        this.showTour(steps);
    }

    /**
     * Tour general para otros roles
     */
    startGeneralTour() {
        const steps = [
            {
                intro: `
                    <div class="tour-welcome">
                        <h3>¡Bienvenido al Sistema Electoral! 👋</h3>
                        <p>Te mostraremos las funciones básicas.</p>
                    </div>
                `
            },
            {
                element: document.querySelector('.navbar'),
                intro: `
                    <h4>Navegación</h4>
                    <p>Usa el menú superior para navegar por el sistema.</p>
                `
            },
            {
                element: document.querySelector('.user-profile'),
                intro: `
                    <h4>Tu Perfil</h4>
                    <p>Accede a tu perfil para ver tu información y configuración.</p>
                `
            },
            {
                intro: `
                    <div class="tour-complete">
                        <h3>¡Tour Completado! 🎉</h3>
                        <p>Explora el sistema y contacta al soporte si necesitas ayuda.</p>
                    </div>
                `
            }
        ];

        this.showTour(steps);
    }

    /**
     * Mostrar el tour con Intro.js
     */
    showTour(steps) {
        // Verificar si Intro.js está disponible
        if (typeof introJs === 'undefined') {
            console.warn('Intro.js no está cargado. Cargando desde CDN...');
            this.loadIntroJs().then(() => {
                this.initializeTour(steps);
            });
        } else {
            this.initializeTour(steps);
        }
    }

    /**
     * Cargar Intro.js desde CDN
     */
    loadIntroJs() {
        return new Promise((resolve, reject) => {
            // Cargar CSS
            const css = document.createElement('link');
            css.rel = 'stylesheet';
            css.href = 'https://cdn.jsdelivr.net/npm/intro.js@7.2.0/minified/introjs.min.css';
            document.head.appendChild(css);

            // Cargar JS
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/intro.js@7.2.0/intro.min.js';
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    /**
     * Inicializar el tour
     */
    initializeTour(steps) {
        const intro = introJs();

        intro.setOptions({
            steps: steps,
            showProgress: true,
            showBullets: true,
            exitOnOverlayClick: false,
            exitOnEsc: true,
            nextLabel: 'Siguiente →',
            prevLabel: '← Anterior',
            doneLabel: '¡Entendido!',
            skipLabel: 'Saltar tour',
            hidePrev: false,
            hideNext: false,
            tooltipClass: 'electoral-tour-tooltip',
            highlightClass: 'electoral-tour-highlight'
        });

        intro.oncomplete(() => {
            this.markTourCompleted();
            this.showCompletionMessage();
        });

        intro.onexit(() => {
            if (confirm('¿Deseas marcar el tour como completado? No se volverá a mostrar automáticamente.')) {
                this.markTourCompleted();
            }
        });

        intro.start();
    }

    /**
     * Mostrar mensaje de completación
     */
    showCompletionMessage() {
        if (typeof Utils !== 'undefined' && Utils.showSuccess) {
            Utils.showSuccess('¡Tour completado! Ya puedes usar el sistema con confianza.');
        }
    }

    /**
     * Mostrar tour manualmente (desde menú de ayuda)
     */
    showManualTour() {
        // Resetear para mostrar de nuevo
        const currentValue = localStorage.getItem(this.tourKey);
        localStorage.removeItem(this.tourKey);

        // Obtener rol del usuario
        const userRole = this.getUserRole();
        this.startTour(userRole);

        // Restaurar valor después del tour
        setTimeout(() => {
            if (currentValue) {
                localStorage.setItem(this.tourKey, currentValue);
            }
        }, 1000);
    }

    /**
     * Obtener rol del usuario actual
     */
    getUserRole() {
        // Intentar obtener del localStorage o de la página
        const userInfo = localStorage.getItem('user_info');
        if (userInfo) {
            try {
                const user = JSON.parse(userInfo);
                return user.rol;
            } catch (e) {
                console.error('Error parsing user info:', e);
            }
        }

        // Intentar obtener del DOM
        const roleElement = document.querySelector('[data-user-role]');
        if (roleElement) {
            return roleElement.dataset.userRole;
        }

        return 'general';
    }
}

// Crear instancia global
window.WelcomeTour = new WelcomeTour();

// CSS personalizado para el tour
const tourStyles = `
<style>
.electoral-tour-tooltip {
    max-width: 400px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.electoral-tour-tooltip .introjs-tooltip-header {
    padding: 15px;
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
}

.electoral-tour-tooltip .introjs-tooltip-title {
    color: white;
    font-weight: bold;
}

.electoral-tour-tooltip .introjs-tooltiptext {
    padding: 20px;
    line-height: 1.6;
}

.electoral-tour-tooltip .introjs-tooltiptext h3 {
    color: #1e3c72;
    margin-bottom: 15px;
}

.electoral-tour-tooltip .introjs-tooltiptext h4 {
    color: #2a5298;
    margin-bottom: 10px;
}

.electoral-tour-tooltip .introjs-tooltiptext ul {
    margin-left: 20px;
    margin-top: 10px;
}

.electoral-tour-tooltip .introjs-tooltiptext ul li {
    margin-bottom: 5px;
}

.electoral-tour-tooltip .introjs-button {
    border-radius: 5px;
    padding: 8px 20px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.electoral-tour-tooltip .introjs-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.electoral-tour-tooltip .introjs-nextbutton {
    background: #1e3c72;
    border: none;
}

.electoral-tour-tooltip .introjs-nextbutton:hover {
    background: #2a5298;
}

.electoral-tour-highlight {
    box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.7);
    border-radius: 8px;
}

.tour-welcome,
.tour-complete {
    text-align: center;
    padding: 10px;
}

.tour-welcome h3,
.tour-complete h3 {
    font-size: 1.5rem;
    margin-bottom: 15px;
}

.tour-complete ul {
    text-align: left;
    display: inline-block;
}
</style>
`;

// Inyectar estilos
if (document.head) {
    document.head.insertAdjacentHTML('beforeend', tourStyles);
}
