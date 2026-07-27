/**
 * EstadoIncidenteModal - Modal para cambiar estado de incidentes
 */

class EstadoIncidenteModal {
    constructor() {
        this.incidente = null;
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
        modal.id = 'estado-incidente-modal';
        modal.innerHTML = `
            <div class="estado-modal-overlay"></div>
            <div class="estado-modal-content">
                <div class="estado-modal-header">
                    <h3>Cambiar Estado del Incidente</h3>
                    <button class="estado-modal-close" id="estado-modal-close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="estado-modal-body">
                    <div class="form-group">
                        <label for="estado-select">Nuevo Estado *</label>
                        <select id="estado-select" class="form-control" required>
                            <option value="">Seleccione un estado...</option>
                            <option value="reportado">Reportado</option>
                            <option value="en_revision">En Revisión</option>
                            <option value="resuelto">Resuelto</option>
                            <option value="escalado">Escalado</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="comentario-textarea">Comentario *</label>
                        <textarea 
                            id="comentario-textarea" 
                            class="form-control" 
                            rows="4" 
                            placeholder="Describa el motivo del cambio de estado..."
                            required
                        ></textarea>
                        <small class="form-text text-muted">
                            El comentario es obligatorio y quedará registrado en el seguimiento.
                        </small>
                    </div>
                    
                    <div id="campos-resolucion" class="campos-adicionales" style="display: none;">
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle"></i>
                            Al marcar como resuelto, se registrará la fecha y usuario de resolución.
                        </div>
                        <div class="form-group">
                            <label for="notas-resolucion">Notas de Resolución</label>
                            <textarea 
                                id="notas-resolucion" 
                                class="form-control" 
                                rows="3"
                                placeholder="Detalles adicionales sobre la resolución..."
                            ></textarea>
                        </div>
                    </div>
                    
                    <div id="campos-escalado" class="campos-adicionales" style="display: none;">
                        <div class="form-group">
                            <label for="escalar-a">Escalar a *</label>
                            <select id="escalar-a" class="form-control">
                                <option value="">Seleccione...</option>
                                <option value="coordinador_municipal">Coordinador Municipal</option>
                                <option value="coordinador_departamental">Coordinador Departamental</option>
                                <option value="auditor">Auditor</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="error-message" id="error-message" style="display: none;"></div>
                </div>
                <div class="estado-modal-footer">
                    <button type="button" class="btn btn-secondary" id="btn-cancelar">
                        Cancelar
                    </button>
                    <button type="button" class="btn btn-primary" id="btn-guardar">
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
        document.getElementById('estado-modal-close').addEventListener('click', () => {
            this.cerrar();
        });

        document.getElementById('btn-cancelar').addEventListener('click', () => {
            this.cerrar();
        });

        // Cerrar al hacer click en overlay
        document.querySelector('.estado-modal-overlay').addEventListener('click', () => {
            this.cerrar();
        });

        // Cambio de estado
        document.getElementById('estado-select').addEventListener('change', (e) => {
            this.handleEstadoChange(e.target.value);
        });

        // Guardar
        document.getElementById('btn-guardar').addEventListener('click', () => {
            this.guardar();
        });

        // Cerrar con ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                const modal = document.getElementById('estado-incidente-modal');
                if (modal.classList.contains('show')) {
                    this.cerrar();
                }
            }
        });
    }

    /**
     * Manejar cambio de estado
     */
    handleEstadoChange(estado) {
        // Ocultar todos los campos adicionales
        document.getElementById('campos-resolucion').style.display = 'none';
        document.getElementById('campos-escalado').style.display = 'none';

        // Mostrar campos según estado
        if (estado === 'resuelto') {
            document.getElementById('campos-resolucion').style.display = 'block';
        } else if (estado === 'escalado') {
            document.getElementById('campos-escalado').style.display = 'block';
        }
    }

    /**
     * Abrir modal
     */
    abrir(incidente, callback) {
        this.incidente = incidente;
        this.callback = callback;

        // Limpiar formulario
        document.getElementById('estado-select').value = '';
        document.getElementById('comentario-textarea').value = '';
        document.getElementById('notas-resolucion').value = '';
        document.getElementById('escalar-a').value = '';
        document.getElementById('error-message').style.display = 'none';

        // Ocultar campos adicionales
        document.getElementById('campos-resolucion').style.display = 'none';
        document.getElementById('campos-escalado').style.display = 'none';

        // Mostrar modal
        const modal = document.getElementById('estado-incidente-modal');
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';

        // Focus en select
        setTimeout(() => {
            document.getElementById('estado-select').focus();
        }, 100);
    }

    /**
     * Cerrar modal
     */
    cerrar() {
        const modal = document.getElementById('estado-incidente-modal');
        modal.classList.remove('show');
        document.body.style.overflow = '';
        this.incidente = null;
        this.callback = null;
    }

    /**
     * Validar formulario
     */
    validar() {
        const estado = document.getElementById('estado-select').value;
        const comentario = document.getElementById('comentario-textarea').value.trim();

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

        if (estado === 'escalado') {
            const escalarA = document.getElementById('escalar-a').value;
            if (!escalarA) {
                this.mostrarError('Debe seleccionar a quién escalar');
                return false;
            }
        }

        return true;
    }

    /**
     * Mostrar error
     */
    mostrarError(mensaje) {
        const errorDiv = document.getElementById('error-message');
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
        const estado = document.getElementById('estado-select').value;
        const comentario = document.getElementById('comentario-textarea').value.trim();
        const notasResolucion = document.getElementById('notas-resolucion').value.trim();
        const escalarA = document.getElementById('escalar-a').value;

        const data = {
            estado: estado,
            comentario: comentario
        };

        if (estado === 'resuelto' && notasResolucion) {
            data.notas_resolucion = notasResolucion;
        }

        if (estado === 'escalado' && escalarA) {
            data.escalado_a = escalarA;
        }

        // Deshabilitar botón
        const btnGuardar = document.getElementById('btn-guardar');
        btnGuardar.disabled = true;
        btnGuardar.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Guardando...';

        try {
            // Llamar API
            const token = localStorage.getItem('token') || sessionStorage.getItem('token');
            const response = await fetch(`/api/incidentes/${this.incidente.id}/estado`, {
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
                this.mostrarMensajeExito('Estado actualizado exitosamente');
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
window.estadoIncidenteModal = new EstadoIncidenteModal();

// Agregar estilos CSS
const style = document.createElement('style');
style.textContent = `
    .estado-modal {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 2000;
    }

    .estado-modal.show {
        display: block;
    }

    .estado-modal-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
    }

    .estado-modal-content {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        border-radius: 8px;
        width: 90%;
        max-width: 600px;
        max-height: 90vh;
        display: flex;
        flex-direction: column;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }

    .estado-modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 25px;
        border-bottom: 1px solid #e0e0e0;
    }

    .estado-modal-header h3 {
        margin: 0;
        font-size: 20px;
        font-weight: 600;
        color: #333;
    }

    .estado-modal-close {
        background: transparent;
        border: none;
        font-size: 24px;
        color: #666;
        cursor: pointer;
        padding: 5px 10px;
        border-radius: 4px;
        transition: all 0.2s;
    }

    .estado-modal-close:hover {
        background-color: #f5f5f5;
        color: #333;
    }

    .estado-modal-body {
        flex: 1;
        overflow-y: auto;
        padding: 25px;
    }

    .estado-modal-footer {
        display: flex;
        justify-content: flex-end;
        gap: 10px;
        padding: 20px 25px;
        border-top: 1px solid #e0e0e0;
    }

    .form-group {
        margin-bottom: 20px;
    }

    .form-group label {
        display: block;
        margin-bottom: 8px;
        font-weight: 600;
        color: #333;
    }

    .form-control {
        width: 100%;
        padding: 10px 12px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 14px;
        transition: border-color 0.2s;
    }

    .form-control:focus {
        outline: none;
        border-color: #2196F3;
        box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.1);
    }

    .form-text {
        display: block;
        margin-top: 5px;
        font-size: 12px;
        color: #666;
    }

    .campos-adicionales {
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid #e0e0e0;
    }

    .alert {
        padding: 12px 15px;
        border-radius: 4px;
        margin-bottom: 15px;
    }

    .alert-info {
        background-color: #e3f2fd;
        border: 1px solid #2196F3;
        color: #1976D2;
    }

    .error-message {
        padding: 12px 15px;
        background-color: #ffebee;
        border: 1px solid #f44336;
        border-radius: 4px;
        color: #c62828;
        margin-top: 15px;
    }

    .btn {
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }

    .btn-secondary {
        background-color: #f5f5f5;
        color: #333;
    }

    .btn-secondary:hover {
        background-color: #e0e0e0;
    }

    .btn-primary {
        background-color: #2196F3;
        color: white;
    }

    .btn-primary:hover {
        background-color: #1976D2;
    }

    .btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    @media (max-width: 768px) {
        .estado-modal-content {
            width: 95%;
            max-height: 95vh;
        }
    }
`;
document.head.appendChild(style);
