/**
 * EstadoDelitoModal - Modal para cambiar estado de delitos
 */

class EstadoDelitoModal {
    constructor() {
        this.delito = null;
        this.callback = null;
        this.init();
    }

    /**
     * Inicializar modal
     */
    init() {
        this.crearModal();
        this.setupEventListeners();
    }

    /**
     * Crear estructura del modal
     */
    crearModal() {
        const modal = document.createElement('div');
        modal.className = 'estado-modal';
        modal.id = 'estado-delito-modal';
        modal.innerHTML = `
            <div class="estado-modal-overlay"></div>
            <div class="estado-modal-content">
                <div class="estado-modal-header">
                    <h3>Cambiar Estado del Delito Electoral</h3>
                    <button class="estado-modal-close" id="estado-delito-modal-close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="estado-modal-body">
                    <div class="form-group">
                        <label for="estado-delito-select">Nuevo Estado *</label>
                        <select id="estado-delito-select" class="form-control" required>
                            <option value="">Seleccione un estado...</option>
                            <option value="reportado">Reportado</option>
                            <option value="en_investigacion">En Investigación</option>
                            <option value="denunciado">Denunciado Formalmente</option>
                            <option value="archivado">Archivado</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="comentario-delito-textarea">Comentario *</label>
                        <textarea 
                            id="comentario-delito-textarea" 
                            class="form-control" 
                            rows="4" 
                            placeholder="Describa el motivo del cambio de estado..."
                            required
                        ></textarea>
                        <small class="form-text text-muted">
                            El comentario es obligatorio y quedará registrado en el seguimiento.
                        </small>
                    </div>
                    
                    <div id="campos-denuncia" class="campos-adicionales" style="display: none;">
                        <div class="alert alert-warning">
                            <i class="fas fa-exclamation-triangle"></i>
                            <strong>Denuncia Formal:</strong> Complete los siguientes campos obligatorios.
                        </div>
                        
                        <div class="form-group">
                            <label for="numero-denuncia">Número de Denuncia *</label>
                            <input 
                                type="text" 
                                id="numero-denuncia" 
                                class="form-control"
                                placeholder="Ej: DEN-2024-001234"
                            />
                        </div>
                        
                        <div class="form-group">
                            <label for="autoridad-competente">Autoridad Competente *</label>
                            <select id="autoridad-competente" class="form-control">
                                <option value="">Seleccione...</option>
                                <option value="fiscalia">Fiscalía General de la Nación</option>
                                <option value="policia">Policía Nacional</option>
                                <option value="cne">Consejo Nacional Electoral</option>
                                <option value="procuraduria">Procuraduría General</option>
                                <option value="otra">Otra</option>
                            </select>
                        </div>
                        
                        <div class="form-group" id="otra-autoridad-group" style="display: none;">
                            <label for="otra-autoridad">Especifique la Autoridad</label>
                            <input 
                                type="text" 
                                id="otra-autoridad" 
                                class="form-control"
                                placeholder="Nombre de la autoridad"
                            />
                        </div>
                        
                        <div class="form-group">
                            <label for="fecha-denuncia">Fecha de Denuncia *</label>
                            <input 
                                type="date" 
                                id="fecha-denuncia" 
                                class="form-control"
                            />
                        </div>
                        
                        <div class="form-group">
                            <label for="observaciones-denuncia">Observaciones</label>
                            <textarea 
                                id="observaciones-denuncia" 
                                class="form-control" 
                                rows="3"
                                placeholder="Detalles adicionales sobre la denuncia..."
                            ></textarea>
                        </div>
                    </div>
                    
                    <div id="campos-archivado" class="campos-adicionales" style="display: none;">
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle"></i>
                            Al archivar, el delito no se eliminará pero no aparecerá en reportes activos.
                        </div>
                        <div class="form-group">
                            <label for="motivo-archivo">Motivo de Archivo *</label>
                            <select id="motivo-archivo" class="form-control">
                                <option value="">Seleccione...</option>
                                <option value="falta_pruebas">Falta de Pruebas</option>
                                <option value="duplicado">Reporte Duplicado</option>
                                <option value="no_procede">No Procede</option>
                                <option value="resuelto_otra_via">Resuelto por Otra Vía</option>
                                <option value="otro">Otro</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="error-message" id="error-delito-message" style="display: none;"></div>
                </div>
                <div class="estado-modal-footer">
                    <button type="button" class="btn btn-secondary" id="btn-delito-cancelar">
                        Cancelar
                    </button>
                    <button type="button" class="btn btn-primary" id="btn-delito-guardar">
                        <i class="fas fa-save"></i> Guardar Cambios
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Cerrar modal
        document.getElementById('estado-delito-modal-close').addEventListener('click', () => {
            this.cerrar();
        });

        document.getElementById('btn-delito-cancelar').addEventListener('click', () => {
            this.cerrar();
        });

        // Cerrar al hacer click en overlay
        document.querySelector('#estado-delito-modal .estado-modal-overlay').addEventListener('click', () => {
            this.cerrar();
        });

        // Cambio de estado
        document.getElementById('estado-delito-select').addEventListener('change', (e) => {
            this.handleEstadoChange(e.target.value);
        });

        // Cambio de autoridad competente
        document.getElementById('autoridad-competente').addEventListener('change', (e) => {
            const otraGroup = document.getElementById('otra-autoridad-group');
            otraGroup.style.display = e.target.value === 'otra' ? 'block' : 'none';
        });

        // Guardar
        document.getElementById('btn-delito-guardar').addEventListener('click', () => {
            this.guardar();
        });
    }

    /**
     * Manejar cambio de estado
     */
    handleEstadoChange(estado) {
        // Ocultar todos los campos adicionales
        document.getElementById('campos-denuncia').style.display = 'none';
        document.getElementById('campos-archivado').style.display = 'none';

        // Mostrar campos según estado
        if (estado === 'denunciado') {
            document.getElementById('campos-denuncia').style.display = 'block';
            // Establecer fecha actual por defecto
            document.getElementById('fecha-denuncia').valueAsDate = new Date();
        } else if (estado === 'archivado') {
            document.getElementById('campos-archivado').style.display = 'block';
        }
    }

    /**
     * Abrir modal
     */
    abrir(delito, callback) {
        this.delito = delito;
        this.callback = callback;

        // Limpiar formulario
        document.getElementById('estado-delito-select').value = '';
        document.getElementById('comentario-delito-textarea').value = '';
        document.getElementById('numero-denuncia').value = '';
        document.getElementById('autoridad-competente').value = '';
        document.getElementById('otra-autoridad').value = '';
        document.getElementById('fecha-denuncia').value = '';
        document.getElementById('observaciones-denuncia').value = '';
        document.getElementById('motivo-archivo').value = '';
        document.getElementById('error-delito-message').style.display = 'none';

        // Ocultar campos adicionales
        document.getElementById('campos-denuncia').style.display = 'none';
        document.getElementById('campos-archivado').style.display = 'none';
        document.getElementById('otra-autoridad-group').style.display = 'none';

        // Mostrar modal
        const modal = document.getElementById('estado-delito-modal');
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';

        // Focus en select
        setTimeout(() => {
            document.getElementById('estado-delito-select').focus();
        }, 100);
    }

    /**
     * Cerrar modal
     */
    cerrar() {
        const modal = document.getElementById('estado-delito-modal');
        modal.classList.remove('show');
        document.body.style.overflow = '';
        this.delito = null;
        this.callback = null;
    }

    /**
     * Validar formulario
     */
    validar() {
        const estado = document.getElementById('estado-delito-select').value;
        const comentario = document.getElementById('comentario-delito-textarea').value.trim();

        if (!estado) {
            this.mostrarError('Debe seleccionar un estado');
            return false;
        }

        if (!comentario) {
            this.mostrarError('El comentario es obligatorio');
            return false;
        }

        if (comentario.length < 10) {
            this.mostrarError('El comentario debe tener al menos 10 caracteres');
            return false;
        }

        // Validaciones específicas para denuncia
        if (estado === 'denunciado') {
            const numeroDenuncia = document.getElementById('numero-denuncia').value.trim();
            const autoridadCompetente = document.getElementById('autoridad-competente').value;
            const fechaDenuncia = document.getElementById('fecha-denuncia').value;

            if (!numeroDenuncia) {
                this.mostrarError('El número de denuncia es obligatorio');
                return false;
            }

            if (!autoridadCompetente) {
                this.mostrarError('Debe seleccionar la autoridad competente');
                return false;
            }

            if (autoridadCompetente === 'otra') {
                const otraAutoridad = document.getElementById('otra-autoridad').value.trim();
                if (!otraAutoridad) {
                    this.mostrarError('Debe especificar la autoridad');
                    return false;
                }
            }

            if (!fechaDenuncia) {
                this.mostrarError('La fecha de denuncia es obligatoria');
                return false;
            }
        }

        // Validaciones para archivado
        if (estado === 'archivado') {
            const motivoArchivo = document.getElementById('motivo-archivo').value;
            if (!motivoArchivo) {
                this.mostrarError('Debe seleccionar el motivo de archivo');
                return false;
            }
        }

        return true;
    }

    /**
     * Mostrar error
     */
    mostrarError(mensaje) {
        const errorDiv = document.getElementById('error-delito-message');
        errorDiv.textContent = mensaje;
        errorDiv.style.display = 'block';

        // Ocultar después de 5 segundos
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    }

    /**
     * Guardar cambios
     */
    async guardar() {
        // Validar
        if (!this.validar()) {
            return;
        }

        // Obtener datos
        const estado = document.getElementById('estado-delito-select').value;
        const comentario = document.getElementById('comentario-delito-textarea').value.trim();

        const data = {
            estado: estado,
            comentario: comentario
        };

        // Datos de denuncia
        if (estado === 'denunciado') {
            const autoridadCompetente = document.getElementById('autoridad-competente').value;
            
            data.numero_denuncia = document.getElementById('numero-denuncia').value.trim();
            data.autoridad_competente = autoridadCompetente === 'otra' 
                ? document.getElementById('otra-autoridad').value.trim()
                : autoridadCompetente;
            data.fecha_denuncia = document.getElementById('fecha-denuncia').value;
            data.observaciones_denuncia = document.getElementById('observaciones-denuncia').value.trim();
        }

        // Datos de archivo
        if (estado === 'archivado') {
            data.motivo_archivo = document.getElementById('motivo-archivo').value;
        }

        // Deshabilitar botón
        const btnGuardar = document.getElementById('btn-delito-guardar');
        btnGuardar.disabled = true;
        btnGuardar.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Guardando...';

        try {
            // Llamar API
            const token = localStorage.getItem('token') || sessionStorage.getItem('token');
            const response = await fetch(`/api/delitos/${this.delito.id}/estado`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok && result.success) {
                // Éxito
                this.cerrar();

                // Llamar callback
                if (this.callback) {
                    this.callback(result.data);
                }

                // Mostrar mensaje de éxito
                this.mostrarMensajeExito('Estado del delito actualizado exitosamente');
            } else {
                // Error
                this.mostrarError(result.error || 'Error al actualizar estado');
            }
        } catch (error) {
            console.error('Error:', error);
            this.mostrarError('Error de conexión. Intente nuevamente.');
        } finally {
            // Rehabilitar botón
            btnGuardar.disabled = false;
            btnGuardar.innerHTML = '<i class="fas fa-save"></i> Guardar Cambios';
        }
    }

    /**
     * Mostrar mensaje de éxito
     */
    mostrarMensajeExito(mensaje) {
        // Usar Toastify si está disponible
        if (typeof Toastify !== 'undefined') {
            Toastify({
                text: mensaje,
                duration: 3000,
                gravity: 'top',
                position: 'right',
                backgroundColor: '#4CAF50'
            }).showToast();
        } else {
            alert(mensaje);
        }
    }
}

// Crear instancia global
window.estadoDelitoModal = new EstadoDelitoModal();

// Los estilos CSS se comparten con EstadoIncidenteModal
// Si no están cargados, agregarlos
if (!document.querySelector('style[data-estado-modal-styles]')) {
    const style = document.createElement('style');
    style.setAttribute('data-estado-modal-styles', 'true');
    style.textContent = `
        .alert-warning {
            background-color: #fff3cd;
            border: 1px solid #ff9800;
            color: #856404;
        }
    `;
    document.head.appendChild(style);
}
