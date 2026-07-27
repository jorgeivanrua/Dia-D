/**
 * SeguimientoTimeline - Componente para mostrar línea de tiempo de seguimiento
 */

class SeguimientoTimeline {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`Container ${containerId} not found`);
            return;
        }
        
        this.seguimientos = [];
        this.loading = false;
        this.init();
    }

    /**
     * Inicializar componente
     */
    init() {
        this.render();
    }

    /**
     * Cargar seguimiento de un reporte
     */
    async cargar(tipoReporte, reporteId) {
        this.loading = true;
        this.render();

        try {
            const token = localStorage.getItem('token') || sessionStorage.getItem('token');
            const response = await fetch(`/api/seguimiento/${tipoReporte}/${reporteId}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    this.seguimientos = data.seguimientos || [];
                    this.render();
                }
            } else {
                this.mostrarError('Error cargando seguimiento');
            }
        } catch (error) {
            console.error('Error:', error);
            this.mostrarError('Error de conexión');
        } finally {
            this.loading = false;
        }
    }

    /**
     * Renderizar timeline
     */
    render() {
        if (this.loading) {
            this.container.innerHTML = `
                <div class="seguimiento-loading">
                    <i class="fas fa-spinner fa-spin"></i>
                    <p>Cargando seguimiento...</p>
                </div>
            `;
            return;
        }

        if (this.seguimientos.length === 0) {
            this.container.innerHTML = `
                <div class="seguimiento-vacio">
                    <i class="fas fa-history"></i>
                    <p>No hay registros de seguimiento</p>
                </div>
            `;
            return;
        }

        // Renderizar timeline
        const timelineHTML = this.seguimientos.map((seg, index) => {
            return this.renderSeguimientoItem(seg, index === this.seguimientos.length - 1);
        }).join('');

        this.container.innerHTML = `
            <div class="seguimiento-timeline">
                ${timelineHTML}
            </div>
        `;
    }

    /**
     * Renderizar item de seguimiento
     */
    renderSeguimientoItem(seguimiento, isLast) {
        const icono = this.getIconoAccion(seguimiento.accion);
        const color = this.getColorAccion(seguimiento.accion);
        const tiempoRelativo = this.getTiempoRelativo(seguimiento.fecha_accion);
        const fechaCompleta = this.formatFechaCompleta(seguimiento.fecha_accion);

        return `
            <div class="seguimiento-item ${isLast ? 'is-last' : ''}">
                <div class="seguimiento-marker" style="background-color: ${color}">
                    <i class="${icono}"></i>
                </div>
                <div class="seguimiento-content">
                    <div class="seguimiento-header">
                        <div class="seguimiento-accion">
                            ${this.getTextoAccion(seguimiento)}
                        </div>
                        <div class="seguimiento-tiempo" title="${fechaCompleta}">
                            ${tiempoRelativo}
                        </div>
                    </div>
                    <div class="seguimiento-usuario">
                        <i class="fas fa-user"></i>
                        ${seguimiento.usuario_nombre || 'Usuario desconocido'}
                        <span class="seguimiento-rol">(${this.formatRol(seguimiento.usuario_rol)})</span>
                    </div>
                    ${seguimiento.comentario ? `
                        <div class="seguimiento-comentario">
                            <i class="fas fa-comment"></i>
                            ${this.escapeHtml(seguimiento.comentario)}
                        </div>
                    ` : ''}
                    ${this.renderMetadatos(seguimiento)}
                </div>
            </div>
        `;
    }

    /**
     * Renderizar metadatos adicionales
     */
    renderMetadatos(seguimiento) {
        if (!seguimiento.metadatos) return '';

        const metadatos = seguimiento.metadatos;
        let html = '<div class="seguimiento-metadatos">';

        // Número de denuncia
        if (metadatos.numero_denuncia) {
            html += `
                <div class="metadato-item">
                    <strong>Número de Denuncia:</strong> ${metadatos.numero_denuncia}
                </div>
            `;
        }

        // Autoridad competente
        if (metadatos.autoridad_competente) {
            html += `
                <div class="metadato-item">
                    <strong>Autoridad:</strong> ${metadatos.autoridad_competente}
                </div>
            `;
        }

        // Escalado a
        if (metadatos.escalado_a) {
            html += `
                <div class="metadato-item">
                    <strong>Escalado a:</strong> ${this.formatRol(metadatos.escalado_a)}
                </div>
            `;
        }

        html += '</div>';
        return html;
    }

    /**
     * Obtener icono según acción
     */
    getIconoAccion(accion) {
        const iconos = {
            'crear': 'fas fa-plus-circle',
            'cambiar_estado': 'fas fa-exchange-alt',
            'agregar_comentario': 'fas fa-comment',
            'denunciar': 'fas fa-gavel',
            'resolver': 'fas fa-check-circle',
            'escalar': 'fas fa-arrow-up',
            'exportar': 'fas fa-download'
        };
        return iconos[accion] || 'fas fa-circle';
    }

    /**
     * Obtener color según acción
     */
    getColorAccion(accion) {
        const colores = {
            'crear': '#4CAF50',
            'cambiar_estado': '#2196F3',
            'agregar_comentario': '#9E9E9E',
            'denunciar': '#f44336',
            'resolver': '#4CAF50',
            'escalar': '#ff9800',
            'exportar': '#9c27b0'
        };
        return colores[accion] || '#757575';
    }

    /**
     * Obtener texto de acción
     */
    getTextoAccion(seguimiento) {
        const { accion, estado_anterior, estado_nuevo } = seguimiento;

        switch (accion) {
            case 'crear':
                return '<strong>Reporte creado</strong>';
            case 'cambiar_estado':
                return `<strong>Estado cambiado:</strong> ${estado_anterior} → ${estado_nuevo}`;
            case 'agregar_comentario':
                return '<strong>Comentario agregado</strong>';
            case 'denunciar':
                return '<strong>Denuncia formal presentada</strong>';
            case 'resolver':
                return '<strong>Reporte resuelto</strong>';
            case 'escalar':
                return '<strong>Reporte escalado</strong>';
            case 'exportar':
                return '<strong>Evidencia exportada</strong>';
            default:
                return `<strong>${accion}</strong>`;
        }
    }

    /**
     * Formatear rol
     */
    formatRol(rol) {
        const roles = {
            'testigo': 'Testigo',
            'coordinador_puesto': 'Coordinador de Puesto',
            'coordinador_municipal': 'Coordinador Municipal',
            'coordinador_departamental': 'Coordinador Departamental',
            'auditor': 'Auditor',
            'super_admin': 'Super Admin'
        };
        return roles[rol] || rol;
    }

    /**
     * Obtener tiempo relativo
     */
    getTiempoRelativo(fechaStr) {
        const fecha = new Date(fechaStr);
        const ahora = new Date();
        const diff = ahora - fecha;

        const segundos = Math.floor(diff / 1000);
        const minutos = Math.floor(diff / 60000);
        const horas = Math.floor(diff / 3600000);
        const dias = Math.floor(diff / 86400000);

        if (segundos < 60) return 'Hace unos segundos';
        if (minutos < 60) return `Hace ${minutos} min`;
        if (horas < 24) return `Hace ${horas} h`;
        if (dias < 7) return `Hace ${dias} d`;
        if (dias < 30) return `Hace ${Math.floor(dias / 7)} sem`;
        if (dias < 365) return `Hace ${Math.floor(dias / 30)} mes`;
        return `Hace ${Math.floor(dias / 365)} año`;
    }

    /**
     * Formatear fecha completa
     */
    formatFechaCompleta(fechaStr) {
        const fecha = new Date(fechaStr);
        return fecha.toLocaleString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    /**
     * Escape HTML
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Mostrar error
     */
    mostrarError(mensaje) {
        this.container.innerHTML = `
            <div class="seguimiento-error">
                <i class="fas fa-exclamation-circle"></i>
                <p>${mensaje}</p>
            </div>
        `;
    }

    /**
     * Agregar nuevo seguimiento (para actualización en tiempo real)
     */
    agregarSeguimiento(seguimiento) {
        this.seguimientos.unshift(seguimiento);
        this.render();
    }
}

// Agregar estilos CSS
const style = document.createElement('style');
style.textContent = `
    .seguimiento-timeline {
        position: relative;
        padding: 20px 0;
    }

    .seguimiento-item {
        position: relative;
        padding-left: 50px;
        padding-bottom: 30px;
    }

    .seguimiento-item:not(.is-last)::before {
        content: '';
        position: absolute;
        left: 19px;
        top: 40px;
        bottom: 0;
        width: 2px;
        background-color: #e0e0e0;
    }

    .seguimiento-marker {
        position: absolute;
        left: 0;
        top: 0;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }

    .seguimiento-content {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .seguimiento-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 10px;
    }

    .seguimiento-accion {
        flex: 1;
        font-size: 15px;
        color: #333;
    }

    .seguimiento-tiempo {
        font-size: 13px;
        color: #999;
        white-space: nowrap;
        margin-left: 10px;
    }

    .seguimiento-usuario {
        font-size: 14px;
        color: #666;
        margin-bottom: 8px;
    }

    .seguimiento-usuario i {
        margin-right: 5px;
        color: #999;
    }

    .seguimiento-rol {
        font-size: 12px;
        color: #999;
    }

    .seguimiento-comentario {
        background-color: #f9f9f9;
        border-left: 3px solid #2196F3;
        padding: 10px 12px;
        margin-top: 10px;
        font-size: 14px;
        color: #555;
        border-radius: 4px;
    }

    .seguimiento-comentario i {
        margin-right: 8px;
        color: #2196F3;
    }

    .seguimiento-metadatos {
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid #f0f0f0;
    }

    .metadato-item {
        font-size: 13px;
        color: #666;
        margin-bottom: 5px;
    }

    .metadato-item strong {
        color: #333;
    }

    .seguimiento-loading,
    .seguimiento-vacio,
    .seguimiento-error {
        text-align: center;
        padding: 40px 20px;
        color: #999;
    }

    .seguimiento-loading i,
    .seguimiento-vacio i,
    .seguimiento-error i {
        font-size: 48px;
        margin-bottom: 15px;
        display: block;
    }

    .seguimiento-loading i {
        color: #2196F3;
    }

    .seguimiento-error i {
        color: #f44336;
    }

    .seguimiento-loading p,
    .seguimiento-vacio p,
    .seguimiento-error p {
        margin: 0;
        font-size: 14px;
    }

    @media (max-width: 768px) {
        .seguimiento-item {
            padding-left: 40px;
        }

        .seguimiento-marker {
            width: 32px;
            height: 32px;
            font-size: 14px;
        }

        .seguimiento-item:not(.is-last)::before {
            left: 15px;
        }

        .seguimiento-header {
            flex-direction: column;
        }

        .seguimiento-tiempo {
            margin-left: 0;
            margin-top: 5px;
        }
    }
`;
document.head.appendChild(style);

// Exportar para uso global
window.SeguimientoTimeline = SeguimientoTimeline;
