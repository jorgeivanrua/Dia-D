/**
 * CandidatosManager - Gestión de Candidatos
 */

class CandidatosManager {
    constructor() {
        this.candidatos = [];
        this.partidos = [];
        this.tiposEleccion = [];
        this.candidatoEditando = null;
        this.init();
    }

    /**
     * Inicializar gestor
     */
    async init() {
        await Promise.all([
            this.cargarCandidatos(),
            this.cargarPartidos(),
            this.cargarTiposEleccion()
        ]);
        this.setupEventListeners();
    }

    /**
     * Cargar candidatos
     */
    async cargarCandidatos() {
        try {
            const response = await fetch('/api/candidatos', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            const data = await response.json();

            if (data.success) {
                this.candidatos = data.data;
                this.renderizarCandidatos();
            }
        } catch (error) {
            console.error('Error cargando candidatos:', error);
        }
    }

    /**
     * Cargar partidos para selector
     */
    async cargarPartidos() {
        try {
            const response = await fetch('/api/partidos?activo=true', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            const data = await response.json();

            if (data.success) {
                this.partidos = data.data;
                this.poblarSelectorPartidos();
            }
        } catch (error) {
            console.error('Error cargando partidos:', error);
        }
    }

    /**
     * Cargar tipos de elección
     */
    async cargarTiposEleccion() {
        try {
            const response = await fetch('/api/configuracion/tipos-eleccion', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            const data = await response.json();

            if (data.success) {
                this.tiposEleccion = data.data;
                this.poblarSelectorTiposEleccion();
            }
        } catch (error) {
            console.error('Error cargando tipos de elección:', error);
        }
    }

    /**
     * Poblar selector de partidos
     */
    poblarSelectorPartidos() {
        const select = document.getElementById('candidato-partido');
        if (!select) return;

        select.innerHTML = '<option value="">Seleccione un partido...</option>';
        
        this.partidos.forEach(partido => {
            const option = document.createElement('option');
            option.value = partido.id;
            option.textContent = `${partido.nombre} (${partido.sigla})`;
            option.style.color = partido.color;
            select.appendChild(option);
        });
    }

    /**
     * Poblar selector de tipos de elección
     */
    poblarSelectorTiposEleccion() {
        const select = document.getElementById('candidato-tipo-eleccion');
        if (!select) return;

        select.innerHTML = '<option value="">Seleccione tipo de elección...</option>';
        
        this.tiposEleccion.forEach(tipo => {
            const option = document.createElement('option');
            option.value = tipo.id;
            option.textContent = tipo.nombre;
            select.appendChild(option);
        });
    }

    /**
     * Renderizar lista de candidatos
     */
    renderizarCandidatos() {
        const container = document.getElementById('candidatos-lista');
        if (!container) return;

        if (this.candidatos.length === 0) {
            container.innerHTML = `
                <tr style="background: white !important;">
                    <td colspan="7" class="text-center text-muted py-4" style="color: #6c757d !important;">
                        No hay candidatos registrados
                    </td>
                </tr>
            `;
            return;
        }

        container.innerHTML = this.candidatos.map(candidato => `
            <tr style="background: white !important; color: #212529 !important;">
                <td style="color: #212529 !important;">
                    ${candidato.foto_url ? 
                        `<img src="${candidato.foto_url}" alt="${candidato.nombre_completo}" class="rounded-circle" style="width: 40px; height: 40px; object-fit: cover;">` :
                        `<div class="rounded-circle bg-secondary d-flex align-items-center justify-content-center" style="width: 40px; height: 40px; color: white;">
                            <i class="bi bi-person"></i>
                        </div>`
                    }
                </td>
                <td style="color: #212529 !important;"><strong>${candidato.nombre_completo}</strong></td>
                <td style="color: #212529 !important;">
                    ${candidato.partido ? 
                        `<span class="badge" style="background-color: ${candidato.partido.color}; color: white;">
                            ${candidato.partido.sigla}
                        </span>` :
                        '<span class="text-muted" style="color: #6c757d !important;">N/A</span>'
                    }
                </td>
                <td style="color: #212529 !important;">${candidato.cargo}</td>
                <td style="color: #212529 !important;">
                    ${candidato.tipo_eleccion ? 
                        `<small>${candidato.tipo_eleccion.nombre}</small>` :
                        '<span class="text-muted" style="color: #6c757d !important;">N/A</span>'
                    }
                </td>
                <td style="color: #212529 !important;">
                    <span class="badge bg-${candidato.activo ? 'success' : 'secondary'}">
                        ${candidato.activo ? 'Activo' : 'Inactivo'}
                    </span>
                </td>
                <td style="color: #212529 !important;">
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="candidatosManager.editarCandidato(${candidato.id})" title="Editar">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-outline-danger" onclick="candidatosManager.eliminarCandidato(${candidato.id})" title="Eliminar">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');

        // Actualizar contador
        const contador = document.getElementById('candidatos-count');
        if (contador) {
            contador.textContent = this.candidatos.length;
        }
    }

    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        // Botón nuevo candidato
        const btnNuevo = document.getElementById('btn-nuevo-candidato');
        if (btnNuevo) {
            btnNuevo.addEventListener('click', () => this.mostrarModalCandidato());
        }

        // Formulario de candidato
        const form = document.getElementById('form-candidato');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.guardarCandidato();
            });
        }

        // Búsqueda
        const searchInput = document.getElementById('search-candidatos');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.buscarCandidatos(e.target.value));
        }

        // Filtros
        const filtroPartido = document.getElementById('filtro-partido-candidatos');
        const filtroTipoEleccion = document.getElementById('filtro-tipo-eleccion-candidatos');
        
        if (filtroPartido) {
            filtroPartido.addEventListener('change', () => this.aplicarFiltros());
        }
        
        if (filtroTipoEleccion) {
            filtroTipoEleccion.addEventListener('change', () => this.aplicarFiltros());
        }
    }

    /**
     * Mostrar modal de candidato
     */
    mostrarModalCandidato(candidato = null) {
        this.candidatoEditando = candidato;

        const modal = new bootstrap.Modal(document.getElementById('modalCandidato'));
        const form = document.getElementById('form-candidato');
        const title = document.getElementById('modal-candidato-title');

        if (candidato) {
            // Editar
            title.textContent = 'Editar Candidato';
            form.elements['nombre_completo'].value = candidato.nombre_completo;
            form.elements['partido_id'].value = candidato.partido_id;
            form.elements['tipo_eleccion_id'].value = candidato.tipo_eleccion_id;
            form.elements['cargo'].value = candidato.cargo;
            form.elements['numero_lista'].value = candidato.numero_lista || '';
            form.elements['biografia'].value = candidato.biografia || '';
            form.elements['activo'].checked = candidato.activo;
        } else {
            // Nuevo
            title.textContent = 'Nuevo Candidato';
            form.reset();
            form.elements['activo'].checked = true;
        }

        modal.show();
    }

    /**
     * Guardar candidato
     */
    async guardarCandidato() {
        const form = document.getElementById('form-candidato');
        const formData = new FormData(form);

        const data = {
            nombre_completo: formData.get('nombre_completo'),
            partido_id: parseInt(formData.get('partido_id')),
            tipo_eleccion_id: parseInt(formData.get('tipo_eleccion_id')),
            cargo: formData.get('cargo'),
            numero_lista: formData.get('numero_lista') ? parseInt(formData.get('numero_lista')) : null,
            biografia: formData.get('biografia'),
            activo: formData.get('activo') === 'on'
        };

        try {
            const url = this.candidatoEditando 
                ? `/api/candidatos/${this.candidatoEditando.id}`
                : '/api/candidatos';

            const method = this.candidatoEditando ? 'PUT' : 'POST';

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
                bootstrap.Modal.getInstance(document.getElementById('modalCandidato')).hide();
                await this.cargarCandidatos();
            } else {
                this.mostrarError(result.error);
            }
        } catch (error) {
            console.error('Error guardando candidato:', error);
            this.mostrarError('Error al guardar candidato');
        }
    }

    /**
     * Editar candidato
     */
    async editarCandidato(id) {
        const candidato = this.candidatos.find(c => c.id === id);
        if (candidato) {
            this.mostrarModalCandidato(candidato);
        }
    }

    /**
     * Eliminar candidato
     */
    async eliminarCandidato(id) {
        const candidato = this.candidatos.find(c => c.id === id);
        if (!candidato) return;

        if (!confirm(`¿Está seguro de eliminar al candidato "${candidato.nombre_completo}"?`)) {
            return;
        }

        try {
            const response = await fetch(`/api/candidatos/${id}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            const result = await response.json();

            if (result.success) {
                this.mostrarExito(result.message);
                await this.cargarCandidatos();
            } else {
                this.mostrarError(result.error);
            }
        } catch (error) {
            console.error('Error eliminando candidato:', error);
            this.mostrarError('Error al eliminar candidato');
        }
    }

    /**
     * Buscar candidatos
     */
    buscarCandidatos(query) {
        const rows = document.querySelectorAll('#candidatos-lista tr');
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
        // Implementar lógica de filtros combinados
        const rows = document.querySelectorAll('#candidatos-lista tr');
        
        rows.forEach(row => {
            // Lógica de filtrado
            row.style.display = '';
        });
    }

    /**
     * Exportar candidatos
     */
    async exportarCandidatos() {
        try {
            const response = await fetch('/api/candidatos/export', {
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
                link.download = `candidatos_${new Date().toISOString().split('T')[0]}.json`;
                link.click();
                URL.revokeObjectURL(url);

                this.mostrarExito('Candidatos exportados exitosamente');
            }
        } catch (error) {
            console.error('Error exportando candidatos:', error);
            this.mostrarError('Error al exportar candidatos');
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
window.candidatosManager = null;

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        if (document.getElementById('candidatos-lista')) {
            window.candidatosManager = new CandidatosManager();
        }
    });
} else {
    if (document.getElementById('candidatos-lista')) {
        window.candidatosManager = new CandidatosManager();
    }
}
