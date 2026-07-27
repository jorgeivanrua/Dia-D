/**
 * Componente para captura y gestión de fotos de evidencia
 */

class FotoCaptureComponent {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            maxFiles: options.maxFiles || 5,
            maxFileSize: options.maxFileSize || 10 * 1024 * 1024, // 10MB
            allowedTypes: options.allowedTypes || ['image/jpeg', 'image/png', 'image/heic', 'image/heif'],
            compressionQuality: options.compressionQuality || 0.8,
            maxWidth: options.maxWidth || 1920,
            maxHeight: options.maxHeight || 1080,
            onFilesChange: options.onFilesChange || (() => {})
        };
        
        this.files = [];
        this.previews = [];
        
        this.init();
    }
    
    init() {
        if (!this.container) {
            console.error('Container not found');
            return;
        }
        
        this.render();
        this.attachEventListeners();
    }
    
    render() {
        this.container.innerHTML = `
            <div class="foto-capture-component">
                <div class="foto-capture-buttons">
                    <button type="button" class="btn btn-primary btn-capture-camera">
                        <i class="bi bi-camera"></i> Capturar Foto
                    </button>
                    <button type="button" class="btn btn-secondary btn-select-gallery">
                        <i class="bi bi-images"></i> Seleccionar de Galería
                    </button>
                    <input type="file" 
                           class="d-none foto-file-input" 
                           accept="image/*" 
                           multiple 
                           capture="environment">
                    <input type="file" 
                           class="d-none foto-gallery-input" 
                           accept="image/*" 
                           multiple>
                </div>
                
                <div class="foto-previews mt-3">
                    <!-- Previews will be inserted here -->
                </div>
                
                <div class="foto-info mt-2">
                    <small class="text-muted">
                        <i class="bi bi-info-circle"></i> 
                        Máximo ${this.options.maxFiles} fotos. 
                        Tamaño máximo por foto: ${(this.options.maxFileSize / (1024 * 1024)).toFixed(0)}MB
                    </small>
                </div>
            </div>
        `;
    }
    
    attachEventListeners() {
        const btnCamera = this.container.querySelector('.btn-capture-camera');
        const btnGallery = this.container.querySelector('.btn-select-gallery');
        const fileInput = this.container.querySelector('.foto-file-input');
        const galleryInput = this.container.querySelector('.foto-gallery-input');
        
        btnCamera.addEventListener('click', () => {
            fileInput.click();
        });
        
        btnGallery.addEventListener('click', () => {
            galleryInput.click();
        });
        
        fileInput.addEventListener('change', (e) => {
            this.handleFileSelect(e.target.files);
            e.target.value = ''; // Reset input
        });
        
        galleryInput.addEventListener('change', (e) => {
            this.handleFileSelect(e.target.files);
            e.target.value = ''; // Reset input
        });
    }
    
    async handleFileSelect(fileList) {
        const files = Array.from(fileList);
        
        // Validar número de archivos
        if (this.files.length + files.length > this.options.maxFiles) {
            alert(`Solo puedes subir un máximo de ${this.options.maxFiles} fotos`);
            return;
        }
        
        for (const file of files) {
            // Validar tipo
            if (!this.options.allowedTypes.includes(file.type)) {
                alert(`Tipo de archivo no permitido: ${file.name}`);
                continue;
            }
            
            // Validar tamaño
            if (file.size > this.options.maxFileSize) {
                alert(`Archivo demasiado grande: ${file.name}. Máximo ${(this.options.maxFileSize / (1024 * 1024)).toFixed(0)}MB`);
                continue;
            }
            
            // Comprimir y agregar
            try {
                const compressedFile = await this.compressImage(file);
                const gpsData = await this.extractGPS();
                
                this.files.push({
                    file: compressedFile,
                    originalFile: file,
                    gps: gpsData,
                    id: Date.now() + Math.random()
                });
                
                await this.createPreview(compressedFile, this.files.length - 1);
                
            } catch (error) {
                console.error('Error procesando imagen:', error);
                alert(`Error procesando ${file.name}`);
            }
        }
        
        this.options.onFilesChange(this.files);
    }
    
    async compressImage(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            
            reader.onload = (e) => {
                const img = new Image();
                
                img.onload = () => {
                    const canvas = document.createElement('canvas');
                    let width = img.width;
                    let height = img.height;
                    
                    // Calcular nuevas dimensiones manteniendo aspect ratio
                    if (width > this.options.maxWidth) {
                        height = (height * this.options.maxWidth) / width;
                        width = this.options.maxWidth;
                    }
                    
                    if (height > this.options.maxHeight) {
                        width = (width * this.options.maxHeight) / height;
                        height = this.options.maxHeight;
                    }
                    
                    canvas.width = width;
                    canvas.height = height;
                    
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, width, height);
                    
                    canvas.toBlob((blob) => {
                        if (blob) {
                            const compressedFile = new File([blob], file.name, {
                                type: 'image/jpeg',
                                lastModified: Date.now()
                            });
                            resolve(compressedFile);
                        } else {
                            reject(new Error('Error comprimiendo imagen'));
                        }
                    }, 'image/jpeg', this.options.compressionQuality);
                };
                
                img.onerror = () => reject(new Error('Error cargando imagen'));
                img.src = e.target.result;
            };
            
            reader.onerror = () => reject(new Error('Error leyendo archivo'));
            reader.readAsDataURL(file);
        });
    }
    
    async extractGPS() {
        return new Promise((resolve) => {
            if (!navigator.geolocation) {
                resolve({ latitud: null, longitud: null, precision: null });
                return;
            }
            
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    resolve({
                        latitud: position.coords.latitude,
                        longitud: position.coords.longitude,
                        precision: position.coords.accuracy
                    });
                },
                (error) => {
                    console.warn('No se pudo obtener geolocalización:', error);
                    resolve({ latitud: null, longitud: null, precision: null });
                },
                {
                    enableHighAccuracy: true,
                    timeout: 5000,
                    maximumAge: 0
                }
            );
        });
    }
    
    async createPreview(file, index) {
        const previewsContainer = this.container.querySelector('.foto-previews');
        
        const reader = new FileReader();
        reader.onload = (e) => {
            const previewDiv = document.createElement('div');
            previewDiv.className = 'foto-preview-item';
            previewDiv.dataset.index = index;
            
            const sizeKB = (file.size / 1024).toFixed(1);
            const gpsIcon = this.files[index].gps.latitud ? 
                '<i class="bi bi-geo-alt-fill text-success" title="Con GPS"></i>' : 
                '<i class="bi bi-geo-alt text-muted" title="Sin GPS"></i>';
            
            previewDiv.innerHTML = `
                <div class="card">
                    <img src="${e.target.result}" class="card-img-top" alt="Preview">
                    <div class="card-body p-2">
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">
                                ${gpsIcon}
                                ${sizeKB} KB
                            </small>
                            <button type="button" class="btn btn-sm btn-danger btn-remove-foto" data-index="${index}">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            `;
            
            previewsContainer.appendChild(previewDiv);
            
            // Attach remove listener
            const btnRemove = previewDiv.querySelector('.btn-remove-foto');
            btnRemove.addEventListener('click', () => {
                this.removeFile(index);
            });
        };
        
        reader.readAsDataURL(file);
    }
    
    removeFile(index) {
        // Remove from arrays
        this.files.splice(index, 1);
        
        // Remove preview
        const previewItem = this.container.querySelector(`.foto-preview-item[data-index="${index}"]`);
        if (previewItem) {
            previewItem.remove();
        }
        
        // Update indices
        const remainingPreviews = this.container.querySelectorAll('.foto-preview-item');
        remainingPreviews.forEach((preview, newIndex) => {
            preview.dataset.index = newIndex;
            const btnRemove = preview.querySelector('.btn-remove-foto');
            btnRemove.dataset.index = newIndex;
        });
        
        this.options.onFilesChange(this.files);
    }
    
    getFiles() {
        return this.files;
    }
    
    clear() {
        this.files = [];
        const previewsContainer = this.container.querySelector('.foto-previews');
        if (previewsContainer) {
            previewsContainer.innerHTML = '';
        }
        this.options.onFilesChange(this.files);
    }
}

// Exponer globalmente
window.FotoCaptureComponent = FotoCaptureComponent;
