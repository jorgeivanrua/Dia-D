/**
 * Gestión de Personalización del Sistema
 * Permite al Super Admin cambiar fondos y apariencia
 */

class PersonalizacionSistema {
    constructor() {
        this.fondosActuales = [];
        this.fondoPredefinidos = [];
        this.fondoActivo = null;
    }

    /**
     * Inicializar módulo de personalización
     */
    async init() {
        console.log('[Personalización] Inicializando...');
        await this.cargarFondos();
        await this.cargarFondosPredefinidos();
        this.setupEventListeners();
    }

    /**
     * Cargar fondos existentes
     */
    async cargarFondos() {
        try {
            const response = await APIClient.get('/config-sistema/fondos');
            
            if (response.success) {
                this.fondosActuales = response.data;
                this.renderizarFondos();
                
                // Identificar fondo activo
                this.fondoActivo = this.fondosActuales.find(f => f.activo);
            }
        } catch (error) {
            console.error('Error cargando fondos:', error);
            Utils.showError('Error al cargar fondos');
        }
    }

    /**
     * Cargar fondos predefinidos
     */
    async cargarFondosPredefinidos() {
        try {
            const response = await APIClient.get('/config-sistema/fondos/predefinidos');
            
            if (response.success) {
                this.fondoPredefinidos = response.data;
                this.renderizarFondosPredefinidos();
            }
        } catch (error) {
            console.error('Error cargando fondos predefinidos:', error);
        }
    }

    /**
     * Renderizar fondos existentes
     */
    renderizarFondos() {
        const container = document.getElementById('fondos-actuales');
        if (!container) return;

        if (this.fondosActuales.length === 0) {
            container.innerHTML = `
                <div class="text-center text-muted py-4">
                    <i class="bi bi-image" style="font-size: 3rem;"></i>
                    <p class="mt-2">No hay fondos personalizados aún</p>
                    <p class="small">Crea uno nuevo o selecciona uno predefinido</p>
                </div>
            `;
            return;
        }

        const html = this.fondosActuales.map(fondo => {
            const isActivo = fondo.activo;
            const preview = this.generarPreview(fondo);
            
            return `
                <div class="col-md-4 mb-3">
                    <div class="card fondo-card ${isActivo ? 'border-success' : ''}">
                        <div class="fondo-preview" style="${preview}">
                            ${isActivo ? '<span class="badge bg-success position-absolute top-0 end-0 m-2">Activo</span>' : ''}
                        </div>
                        <div class="card-body">
                            <h6 class="card-title">${fondo.nombre}</h6>
                            <p class="card-text small text-muted">
                                <i class="bi bi-palette"></i> ${this.getTipoLabel(fondo.tipo)}
                            </p>
                            <div class="btn-group w-100" role="group">
                                ${!isActivo ? `
                                    <button class="btn btn-sm btn-primary" onclick="personalizacion.activarFondo(${fondo.id})">
                                        <i class="bi bi-check-circle"></i> Activar
                                    </button>
                                ` : ''}
                                <button class="btn btn-sm btn-outline-secondary" onclick="personalizacion.previsualizarFondo(${fondo.id})">
                                    <i class="bi bi-eye"></i> Vista Previa
                                </button>
                                ${!isActivo && !fondo.predeterminado ? `
                                    <button class="btn btn-sm btn-outline-danger" onclick="personalizacion.eliminarFondo(${fondo.id})">
                                        <i class="bi bi-trash"></i>
                                    </button>
                                ` : ''}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        container.innerHTML = html;
    }

    /**
     * Renderizar fondos predefinidos
     */
    renderizarFondosPredefinidos() {
        const container = document.getElementById('fondos-predefinidos');
        if (!container) return;

        const html = this.fondoPredefinidos.map((fondo, index) => {
            return `
                <div class="col-md-3 mb-3">
                    <div class="card fondo-card-small">
                        <div class="fondo-preview-small" style="background: ${fondo.preview}"></div>
                        <div class="card-body p-2">
                            <p class="card-text small mb-2">${fondo.nombre}</p>
                            <button class="btn btn-sm btn-primary w-100" onclick="personalizacion.aplicarPredefinido(${index})">
                                <i class="bi bi-plus-circle"></i> Usar
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        container.innerHTML = html;
    }

    /**
     * Generar CSS preview para un fondo
     */
    generarPreview(fondo) {
        if (fondo.tipo === 'gradient') {
            const colors = [];
            if (fondo.color1) {
                colors.push(`${fondo.color1} 0%`);
                colors.push(`${fondo.color1} 50%`);
            }
            if (fondo.color2) {
                colors.push(`${fondo.color2} 50%`);
                colors.push(`${fondo.color2} 75%`);
            }
            if (fondo.color3) {
                colors.push(`${fondo.color3} 75%`);
                colors.push(`${fondo.color3} 100%`);
            }
            return `background: linear-gradient(${fondo.direccion}, ${colors.join(', ')})`;
            
        } else if (fondo.tipo === 'image') {
            return `
                background-image: url('${fondo.imagen_url}');
                background-size: ${fondo.imagen_tamano};
                background-position: ${fondo.imagen_posicion};
                background-repeat: no-repeat;
            `;
            
        } else if (fondo.tipo === 'solid') {
            return `background: ${fondo.color_solido}`;
        }
        
        return '';
    }

    /**
     * Obtener label del tipo de fondo
     */
    getTipoLabel(tipo) {
        const labels = {
            'gradient': 'Gradiente',
            'image': 'Imagen',
            'solid': 'Color Sólido'
        };
        return labels[tipo] || tipo;
    }

    /**
     * Activar un fondo
     */
    async activarFondo(fondoId) {
        try {
            const response = await APIClient.put(`/config-sistema/fondos/${fondoId}/activar`, {});
            
            if (response.success) {
                Utils.showSuccess('Fondo activado exitosamente');
                await this.cargarFondos();
            }
        } catch (error) {
            console.error('Error activando fondo:', error);
            Utils.showError(error.message || 'Error al activar fondo');
        }
    }

    /**
     * Eliminar un fondo
     */
    async eliminarFondo(fondoId) {
        if (!confirm('¿Estás seguro de eliminar este fondo?')) {
            return;
        }

        try {
            const response = await APIClient.delete(`/config-sistema/fondos/${fondoId}`);
            
            if (response.success) {
                Utils.showSuccess('Fondo eliminado exitosamente');
                await this.cargarFondos();
            }
        } catch (error) {
            console.error('Error eliminando fondo:', error);
            Utils.showError(error.message || 'Error al eliminar fondo');
        }
    }

    /**
     * Previsualizar un fondo
     */
    previsualizarFondo(fondoId) {
        const fondo = this.fondosActuales.find(f => f.id === fondoId);
        if (!fondo) return;

        const preview = this.generarPreview(fondo);
        
        // Crear modal de previsualización
        const modal = `
            <div class="modal fade" id="previewModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Vista Previa: ${fondo.nombre}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="preview-container" style="${preview}; height: 400px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                                <div class="card" style="max-width: 400px;">
                                    <div class="card-body text-center">
                                        <h3>DÍA D</h3>
                                        <p class="text-muted">Sistema Electoral</p>
                                        <p class="small">Así se verá el fondo en la página de login</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Eliminar modal anterior si existe
        const oldModal = document.getElementById('previewModal');
        if (oldModal) oldModal.remove();

        // Agregar nuevo modal
        document.body.insertAdjacentHTML('beforeend', modal);
        
        // Mostrar modal
        const modalElement = new bootstrap.Modal(document.getElementById('previewModal'));
        modalElement.show();
    }

    /**
     * Aplicar fondo predefinido
     */
    async aplicarPredefinido(index) {
        const fondo = this.fondoPredefinidos[index];
        if (!fondo) return;

        try {
            const response = await APIClient.post('/config-sistema/fondos', fondo);
            
            if (response.success) {
                Utils.showSuccess('Fondo predefinido agregado');
                await this.cargarFondos();
            }
        } catch (error) {
            console.error('Error aplicando fondo predefinido:', error);
            Utils.showError(error.message || 'Error al aplicar fondo');
        }
    }

    /**
     * Mostrar formulario de crear fondo personalizado
     */
    mostrarFormularioCrear() {
        const modal = document.getElementById('crearFondoModal');
        if (modal) {
            const modalInstance = new bootstrap.Modal(modal);
            modalInstance.show();
        }
    }

    /**
     * Crear fondo con gradiente personalizado
     */
    async crearFondoGradiente() {
        const nombre = document.getElementById('gradiente-nombre').value;
        const color1 = document.getElementById('gradiente-color1').value;
        const color2 = document.getElementById('gradiente-color2').value;
        const color3 = document.getElementById('gradiente-color3').value;
        const direccion = document.getElementById('gradiente-direccion').value;

        if (!nombre || !color1) {
            Utils.showError('Completa al menos el nombre y el primer color');
            return;
        }

        try {
            const response = await APIClient.post('/config-sistema/fondos', {
                nombre,
                tipo: 'gradient',
                color1,
                color2: color2 || null,
                color3: color3 || null,
                direccion
            });

            if (response.success) {
                Utils.showSuccess('Fondo creado exitosamente');
                await this.cargarFondos();
                
                // Cerrar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('crearFondoModal'));
                if (modal) modal.hide();
                
                // Limpiar formulario
                document.getElementById('form-gradiente').reset();
            }
        } catch (error) {
            console.error('Error creando fondo:', error);
            Utils.showError(error.message || 'Error al crear fondo');
        }
    }

    /**
     * Subir imagen de fondo
     */
    async subirImagenFondo() {
        const fileInput = document.getElementById('imagen-file');
        const nombre = document.getElementById('imagen-nombre').value;
        const posicion = document.getElementById('imagen-posicion').value;
        const tamano = document.getElementById('imagen-tamano').value;

        if (!fileInput.files[0]) {
            Utils.showError('Selecciona una imagen');
            return;
        }

        if (!nombre) {
            Utils.showError('Ingresa un nombre para el fondo');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('nombre', nombre);
        formData.append('imagen_posicion', posicion);
        formData.append('imagen_tamano', tamano);

        try {
            const response = await fetch('/api/config-sistema/fondos/upload', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                Utils.showSuccess('Imagen subida exitosamente');
                await this.cargarFondos();
                
                // Cerrar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('crearFondoModal'));
                if (modal) modal.hide();
                
                // Limpiar formulario
                document.getElementById('form-imagen').reset();
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error('Error subiendo imagen:', error);
            Utils.showError(error.message || 'Error al subir imagen');
        }
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Preview de imagen antes de subir
        const fileInput = document.getElementById('imagen-file');
        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        const preview = document.getElementById('imagen-preview');
                        if (preview) {
                            preview.style.backgroundImage = `url('${e.target.result}')`;
                            preview.style.display = 'block';
                        }
                    };
                    reader.readAsDataURL(file);
                }
            });
        }

        // Preview de gradiente en tiempo real
        const gradienteInputs = ['gradiente-color1', 'gradiente-color2', 'gradiente-color3', 'gradiente-direccion'];
        gradienteInputs.forEach(id => {
            const input = document.getElementById(id);
            if (input) {
                input.addEventListener('input', () => this.actualizarPreviewGradiente());
            }
        });
    }

    /**
     * Actualizar preview de gradiente en tiempo real
     */
    actualizarPreviewGradiente() {
        const color1 = document.getElementById('gradiente-color1').value;
        const color2 = document.getElementById('gradiente-color2').value;
        const color3 = document.getElementById('gradiente-color3').value;
        const direccion = document.getElementById('gradiente-direccion').value;

        const preview = document.getElementById('gradiente-preview');
        if (!preview) return;

        const colors = [];
        if (color1) {
            colors.push(`${color1} 0%`);
            if (color2) colors.push(`${color1} 50%`);
        }
        if (color2) {
            colors.push(`${color2} 50%`);
            if (color3) colors.push(`${color2} 75%`);
        }
        if (color3) {
            colors.push(`${color3} 75%`);
            colors.push(`${color3} 100%`);
        }

        if (colors.length > 0) {
            preview.style.background = `linear-gradient(${direccion}, ${colors.join(', ')})`;
            preview.style.display = 'block';
        }
    }

    /**
     * Crear fondo con color sólido
     */
    async crearFondoSolido() {
        const nombre = document.getElementById('solido-nombre').value;
        const color = document.getElementById('solido-color').value;

        if (!nombre || !color) {
            Utils.showError('Completa todos los campos');
            return;
        }

        try {
            const response = await APIClient.post('/config-sistema/fondos', {
                nombre,
                tipo: 'solid',
                color_solido: color
            });

            if (response.success) {
                Utils.showSuccess('Fondo creado exitosamente');
                await this.cargarFondos();
                
                // Cerrar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('crearFondoModal'));
                if (modal) modal.hide();
                
                // Limpiar formulario
                document.getElementById('form-solido').reset();
            }
        } catch (error) {
            console.error('Error creando fondo:', error);
            Utils.showError(error.message || 'Error al crear fondo');
        }
    }
}

// Crear instancia global
window.personalizacion = new PersonalizacionSistema();
