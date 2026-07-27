/**
 * PartidosManager - Gestión de Partidos Políticos
 */

class PartidosManager {
    constructor() {
        this.partidos = [];
        this.partidoEditando = null;
        this.init();
    }

    /**
     * Inicializar gestor
     */
    async init() {
        await this.cargarPartidos();
        this.setupEventListeners();
    }

    /**
     * Cargar partidos desde el servidor
     */
    async cargarPartidos() {
        try {
            const response = await fetch('/api/partidos', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            const data = await response.json();

            if (data.success) {
                this.partidos = data.data;
                this.renderizarPartidos();
            }
        } catch (error) {
            console.error('Error cargando partidos:', error);
            this.mostrarError('Error al cargar partidos');
        }
    }

    /**
     * Renderizar lista de partidos
     */
    renderizarPartidos() {
        const container = document.getElementById('partidos-lista');
        if (!container) return;

        if (this.partidos.length === 0) {
            container.innerHTML = `
                <tr style="background: white !important;">
                    <td colspan="6" class="text-center text-muted py-4" style="color: #6c757d !important;">
                        No hay partidos registrados
                    </td>
                </tr>
            `;
            return;
        }

        container.innerHTML = this.partidos.map(partido => `
            <tr style="display: table-row !important; background: white !important; color: #212529 !important;">
                <td style="display: table-cell !important; color: #212529 !important;">
                    <div class="d-flex align-items-center gap-2">
                        ${partido.logo_url ? 
                            `<img src="${partido.logo_url}" alt="${partido.sigla}" style="width: 30px; height: 30px; object-fit: contain;">` :
                            `<div style="width: 30px; height: 30px; background-color: ${partido.color}; border-radius: 4px;"></div>`
                        }
                    </div>
                </td>
                <td style="display: table-cell !important; color: #212529 !important;"><strong>${partido.nombre}</strong></td>
                <td style="display: table-cell !important; color: #212529 !important;"><span class="badge" style="background-color: ${partido.color}; color: white;">${partido.sigla}</span></td>
                <td style="display: table-cell !important; color: #212529 !important;">
                    <div class="d-flex align-items-center gap-2">
                        <div style="width: 20px; height: 20px; background-color: ${partido.color}; border: 1px solid #ddd; border-radius: 3px;"></div>
                        <code style="color: #212529 !important;">${partido.color}</code>
                    </div>
                </td>
                <td style="display: table-cell !important; color: #212529 !important;">
                    <span class="badge bg-${partido.activo ? 'success' : 'secondary'}">
                        ${partido.activo ? 'Activo' : 'Inactivo'}
                    </span>
                </td>
                <td style="display: table-cell !important; color: #212529 !important;">
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="partidosManager.editarPartido(${partido.id})" title="Editar">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-outline-danger" onclick="partidosManager.eliminarPartido(${partido.id})" title="Eliminar">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');

        // Actualizar contador
        const contador = document.getElementById('partidos-count');
        if (contador) {
            contador.textContent = this.partidos.length;
        }

        // Forzar visibilidad de elementos internos (NO del tab contenedor)
        const table = container.closest('table');
        const chartCard = container.closest('.chart-card');
        
        if (chartCard) {
            chartCard.style.cssText = 'opacity: 1 !important; visibility: visible !important; background: white !important;';
        }
        if (table) {
            table.style.cssText = 'opacity: 1 !important; visibility: visible !important;';
        }
        container.style.cssText = 'opacity: 1 !important; visibility: visible !important;';
    }

    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        // Botón nuevo partido
        const btnNuevo = document.getElementById('btn-nuevo-partido');
        if (btnNuevo) {
            btnNuevo.addEventListener('click', () => this.mostrarModalPartido());
        }

        // Formulario de partido
        const form = document.getElementById('form-partido');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.guardarPartido();
            });
        }

        // Búsqueda
        const searchInput = document.getElementById('search-partidos');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.buscarPartidos(e.target.value));
        }

        // Filtro activo
        const filtroActivo = document.getElementById('filtro-activo-partidos');
        if (filtroActivo) {
            filtroActivo.addEventListener('change', () => this.aplicarFiltros());
        }

        // Selector de color
        const colorInput = document.getElementById('partido-color');
        const colorPreview = document.getElementById('color-preview');
        if (colorInput && colorPreview) {
            colorInput.addEventListener('input', (e) => {
                colorPreview.style.backgroundColor = e.target.value;
            });
        }
    }

    /**
     * Mostrar modal de partido
     */
    mostrarModalPartido(partido = null) {
        this.partidoEditando = partido;

        const modal = new bootstrap.Modal(document.getElementById('modalPartido'));
        const form = document.getElementById('form-partido');
        const title = document.getElementById('modal-partido-title');

        if (partido) {
            // Editar
            title.textContent = 'Editar Partido';
            form.elements['nombre'].value = partido.nombre;
            form.elements['sigla'].value = partido.sigla;
            form.elements['color'].value = partido.color;
            form.elements['descripcion'].value = partido.descripcion || '';
            form.elements['activo'].checked = partido.activo;

            const colorPreview = document.getElementById('color-preview');
            if (colorPreview) {
                colorPreview.style.backgroundColor = partido.color;
            }
        } else {
            // Nuevo
            title.textContent = 'Nuevo Partido';
            form.reset();
            form.elements['activo'].checked = true;

            const colorPreview = document.getElementById('color-preview');
            if (colorPreview) {
                colorPreview.style.backgroundColor = '#000000';
            }
        }

        modal.show();
    }

    /**
     * Guardar partido
     */
    async guardarPartido() {
        const form = document.getElementById('form-partido');
        const formData = new FormData(form);

        const data = {
            nombre: formData.get('nombre'),
            sigla: formData.get('sigla'),
            color: formData.get('color'),
            descripcion: formData.get('descripcion'),
            activo: formData.get('activo') === 'on'
        };

        try {
            const url = this.partidoEditando 
                ? `/api/partidos/${this.partidoEditando.id}`
                : '/api/partidos';

            const method = this.partidoEditando ? 'PUT' : 'POST';

            const response = await fetch(url, {
                method: method,
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                this.mostrarExito(result.message);
                bootstrap.Modal.getInstance(document.getElementById('modalPartido')).hide();
                await this.cargarPartidos();
            } else {
                this.mostrarError(result.error);
            }
        } catch (error) {
            console.error('Error guardando partido:', error);
            this.mostrarError('Error al guardar partido');
        }
    }

    /**
     * Editar partido
     */
    async editarPartido(id) {
        const partido = this.partidos.find(p => p.id === id);
        if (partido) {
            this.mostrarModalPartido(partido);
        }
    }

    /**
     * Eliminar partido
     */
    async eliminarPartido(id) {
        const partido = this.partidos.find(p => p.id === id);
        if (!partido) return;

        if (!confirm(`¿Está seguro de eliminar el partido "${partido.nombre}"?`)) {
            return;
        }

        try {
            const response = await fetch(`/api/partidos/${id}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            const result = await response.json();

            if (result.success) {
                this.mostrarExito(result.message);
                await this.cargarPartidos();
            } else {
                this.mostrarError(result.error);
            }
        } catch (error) {
            console.error('Error eliminando partido:', error);
            this.mostrarError('Error al eliminar partido');
        }
    }

    /**
     * Buscar partidos
     */
    buscarPartidos(query) {
        const rows = document.querySelectorAll('#partidos-lista tr');
        const searchLower = query.toLowerCase();

        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchLower) ? '' : 'none';
        });
    }

    /**
     * Aplicar filtros
     */
    aplicarFiltros() {
        const filtroActivo = document.getElementById('filtro-activo-partidos');
        if (!filtroActivo) return;

        const valor = filtroActivo.value;
        const rows = document.querySelectorAll('#partidos-lista tr');

        rows.forEach(row => {
            if (valor === 'todos') {
                row.style.display = '';
            } else {
                const esActivo = row.querySelector('.badge.bg-success') !== null;
                const mostrar = (valor === 'activos' && esActivo) || (valor === 'inactivos' && !esActivo);
                row.style.display = mostrar ? '' : 'none';
            }
        });
    }

    /**
     * Exportar partidos
     */
    async exportarPartidos() {
        try {
            const response = await fetch('/api/partidos/export', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            const result = await response.json();

            if (result.success) {
                const dataStr = JSON.stringify(result.data, null, 2);
                const dataBlob = new Blob([dataStr], { type: 'application/json' });
                const url = URL.createObjectURL(dataBlob);
                const link = document.createElement('a');
                link.href = url;
                link.download = `partidos_${new Date().toISOString().split('T')[0]}.json`;
                link.click();
                URL.revokeObjectURL(url);

                this.mostrarExito('Partidos exportados exitosamente');
            }
        } catch (error) {
            console.error('Error exportando partidos:', error);
            this.mostrarError('Error al exportar partidos');
        }
    }

    /**
     * Mostrar mensaje de éxito
     */
    mostrarExito(mensaje) {
        if (typeof Toastify !== 'undefined') {
            Toastify({
                text: mensaje,
                duration: 3000,
                gravity: 'top',
                position: 'right',
                backgroundColor: '#28a745'
            }).showToast();
        } else {
            alert(mensaje);
        }
    }

    /**
     * Mostrar mensaje de error
     */
    mostrarError(mensaje) {
        if (typeof Toastify !== 'undefined') {
            Toastify({
                text: mensaje,
                duration: 5000,
                gravity: 'top',
                position: 'right',
                backgroundColor: '#dc3545'
            }).showToast();
        } else {
            alert(mensaje);
        }
    }
}

// Crear instancia global
window.partidosManager = null;

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        if (document.getElementById('partidos-lista')) {
            window.partidosManager = new PartidosManager();
        }
    });
} else {
    if (document.getElementById('partidos-lista')) {
        window.partidosManager = new PartidosManager();
    }
}
