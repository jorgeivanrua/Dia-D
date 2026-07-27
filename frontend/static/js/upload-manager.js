/**
 * Manager para upload de evidencia fotográfica
 */

class UploadManager {
    constructor() {
        this.uploadQueue = [];
        this.uploading = false;
        this.maxRetries = 3;
    }
    
    /**
     * Subir foto al servidor
     * @param {File} file - Archivo a subir
     * @param {string} tipoReporte - 'incidente' o 'delito'
     * @param {number} reporteId - ID del reporte
     * @param {Object} metadata - Metadatos adicionales (GPS, etc.)
     * @returns {Promise<Object>} Resultado del upload
     */
    async uploadFoto(file, tipoReporte, reporteId, metadata = {}) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('tipo_reporte', tipoReporte);
        formData.append('reporte_id', reporteId);
        
        // Agregar metadatos GPS si existen
        if (metadata.gps) {
            if (metadata.gps.latitud) {
                formData.append('latitud', metadata.gps.latitud);
            }
            if (metadata.gps.longitud) {
                formData.append('longitud', metadata.gps.longitud);
            }
            if (metadata.gps.precision) {
                formData.append('precision_gps', metadata.gps.precision);
            }
        }
        
        try {
            const response = await fetch('/api/evidencia/upload', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: formData
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Error al subir evidencia');
            }
            
            return data;
            
        } catch (error) {
            console.error('Error en upload:', error);
            throw error;
        }
    }
    
    /**
     * Subir múltiples fotos con progress tracking
     * @param {Array} files - Array de objetos {file, gps}
     * @param {string} tipoReporte - 'incidente' o 'delito'
     * @param {number} reporteId - ID del reporte
     * @param {Function} onProgress - Callback para progreso
     * @returns {Promise<Array>} Resultados de uploads
     */
    async uploadMultiple(files, tipoReporte, reporteId, onProgress = null) {
        const results = [];
        const total = files.length;
        
        for (let i = 0; i < files.length; i++) {
            const fileData = files[i];
            
            try {
                // Notificar progreso
                if (onProgress) {
                    onProgress({
                        current: i + 1,
                        total: total,
                        percentage: Math.round(((i + 1) / total) * 100),
                        fileName: fileData.file.name,
                        status: 'uploading'
                    });
                }
                
                // Subir archivo
                const result = await this.uploadFoto(
                    fileData.file,
                    tipoReporte,
                    reporteId,
                    { gps: fileData.gps }
                );
                
                results.push({
                    success: true,
                    fileName: fileData.file.name,
                    data: result.data
                });
                
                // Notificar éxito
                if (onProgress) {
                    onProgress({
                        current: i + 1,
                        total: total,
                        percentage: Math.round(((i + 1) / total) * 100),
                        fileName: fileData.file.name,
                        status: 'success'
                    });
                }
                
            } catch (error) {
                console.error(`Error subiendo ${fileData.file.name}:`, error);
                
                results.push({
                    success: false,
                    fileName: fileData.file.name,
                    error: error.message
                });
                
                // Notificar error
                if (onProgress) {
                    onProgress({
                        current: i + 1,
                        total: total,
                        percentage: Math.round(((i + 1) / total) * 100),
                        fileName: fileData.file.name,
                        status: 'error',
                        error: error.message
                    });
                }
            }
        }
        
        return results;
    }
    
    /**
     * Subir foto con reintentos automáticos
     * @param {File} file - Archivo a subir
     * @param {string} tipoReporte - 'incidente' o 'delito'
     * @param {number} reporteId - ID del reporte
     * @param {Object} metadata - Metadatos adicionales
     * @param {number} attempts - Número de intentos realizados
     * @returns {Promise<Object>} Resultado del upload
     */
    async uploadWithRetry(file, tipoReporte, reporteId, metadata = {}, attempts = 0) {
        try {
            return await this.uploadFoto(file, tipoReporte, reporteId, metadata);
        } catch (error) {
            if (attempts < this.maxRetries) {
                console.log(`Reintentando upload (${attempts + 1}/${this.maxRetries})...`);
                
                // Esperar antes de reintentar (exponential backoff)
                await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempts) * 1000));
                
                return this.uploadWithRetry(file, tipoReporte, reporteId, metadata, attempts + 1);
            } else {
                throw new Error(`Error después de ${this.maxRetries} intentos: ${error.message}`);
            }
        }
    }
    
    /**
     * Obtener URL de evidencia
     * @param {string} filename - Nombre del archivo
     * @returns {string} URL completa
     */
    getEvidenciaUrl(filename) {
        return `/api/evidencia/${filename}`;
    }
    
    /**
     * Eliminar evidencia
     * @param {number} evidenciaId - ID de la evidencia
     * @returns {Promise<Object>} Resultado de la eliminación
     */
    async deleteEvidencia(evidenciaId) {
        try {
            const response = await fetch(`/api/evidencia/${evidenciaId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Error al eliminar evidencia');
            }
            
            return data;
            
        } catch (error) {
            console.error('Error eliminando evidencia:', error);
            throw error;
        }
    }
    
    /**
     * Mostrar modal de progreso de upload
     * @param {Array} files - Archivos a subir
     * @param {string} tipoReporte - Tipo de reporte
     * @param {number} reporteId - ID del reporte
     * @returns {Promise<Array>} Resultados
     */
    async uploadWithProgressModal(files, tipoReporte, reporteId) {
        // Crear modal de progreso
        const modalHtml = `
            <div class="modal fade" id="uploadProgressModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="bi bi-cloud-upload"></i> Subiendo Evidencia
                            </h5>
                        </div>
                        <div class="modal-body">
                            <div class="upload-progress-info mb-3">
                                <div class="d-flex justify-content-between mb-2">
                                    <span id="upload-current-file">Preparando...</span>
                                    <span id="upload-counter">0/${files.length}</span>
                                </div>
                                <div class="progress" style="height: 25px;">
                                    <div class="progress-bar progress-bar-striped progress-bar-animated" 
                                         id="upload-progress-bar"
                                         role="progressbar" 
                                         style="width: 0%">
                                        0%
                                    </div>
                                </div>
                            </div>
                            <div id="upload-results" class="mt-3">
                                <!-- Results will be shown here -->
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" id="upload-close-btn" disabled>
                                Cerrar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Agregar modal al DOM
        const modalContainer = document.createElement('div');
        modalContainer.innerHTML = modalHtml;
        document.body.appendChild(modalContainer);
        
        // Mostrar modal
        const modal = new bootstrap.Modal(document.getElementById('uploadProgressModal'));
        modal.show();
        
        // Elementos del modal
        const currentFileEl = document.getElementById('upload-current-file');
        const counterEl = document.getElementById('upload-counter');
        const progressBar = document.getElementById('upload-progress-bar');
        const resultsEl = document.getElementById('upload-results');
        const closeBtn = document.getElementById('upload-close-btn');
        
        // Subir archivos con progreso
        const results = await this.uploadMultiple(files, tipoReporte, reporteId, (progress) => {
            currentFileEl.textContent = progress.fileName;
            counterEl.textContent = `${progress.current}/${progress.total}`;
            progressBar.style.width = `${progress.percentage}%`;
            progressBar.textContent = `${progress.percentage}%`;
            
            // Agregar resultado
            if (progress.status === 'success') {
                resultsEl.innerHTML += `
                    <div class="alert alert-success alert-sm py-1 px-2 mb-1">
                        <i class="bi bi-check-circle"></i> ${progress.fileName}
                    </div>
                `;
            } else if (progress.status === 'error') {
                resultsEl.innerHTML += `
                    <div class="alert alert-danger alert-sm py-1 px-2 mb-1">
                        <i class="bi bi-x-circle"></i> ${progress.fileName}: ${progress.error}
                    </div>
                `;
            }
        });
        
        // Habilitar botón de cerrar
        closeBtn.disabled = false;
        progressBar.classList.remove('progress-bar-animated');
        
        // Cerrar modal al hacer clic
        closeBtn.addEventListener('click', () => {
            modal.hide();
            modalContainer.remove();
        });
        
        return results;
    }
}

// Crear instancia global
window.uploadManager = new UploadManager();

// Exponer clase
window.UploadManager = UploadManager;
