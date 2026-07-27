/**
 * SISTEMA DE CARGA MASIVA CSV - ELECTORAL
 * Maneja el wizard de carga masiva de datos electorales
 */

let currentUploadStep = 1;
let uploadConfig = {};
let uploadFile = null;
let validationResults = null;

/**
 * Inicializar sistema de carga masiva
 */
function initBulkUpload() {
    console.log('[BulkUpload] Inicializando sistema de carga masiva');
    handleUploadTypeSelection();
}

/**
 * Selección rápida de tipo de carga
 */
function quickSelectUploadType(type) {
    console.log('[BulkUpload] Acceso rápido a:', type);
    
    // Resetear wizard si está en otro paso
    if (currentUploadStep !== 1) {
        resetUploadWizard();
    }
    
    // Seleccionar el radio button correspondiente
    const radio = document.querySelector(`input[name="uploadType"][value="${type}"]`);
    if (radio) {
        radio.checked = true;
        uploadConfig.type = type;
        
        // Habilitar botón de continuar
        const btnNext = document.getElementById('btnNextStep1');
        if (btnNext) {
            btnNext.disabled = false;
        }
        
        // Scroll al wizard
        document.getElementById('bulkUploadWizard').scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Resaltar la selección
        const label = radio.closest('label');
        if (label) {
            label.classList.add('active');
            setTimeout(() => label.classList.remove('active'), 1000);
        }
    }
}

/**
 * Manejar selección de tipo de carga
 */
function handleUploadTypeSelection() {
    const radios = document.querySelectorAll('input[name="uploadType"]');
    const btnNext = document.getElementById('btnNextStep1');
    
    if (!radios.length || !btnNext) {
        console.log('[BulkUpload] Elementos no encontrados, reintentando...');
        setTimeout(handleUploadTypeSelection, 500);
        return;
    }
    
    radios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.checked) {
                uploadConfig.type = this.value;
                btnNext.disabled = false;
                console.log('[Upload] Tipo seleccionado:', this.value);
            }
        });
    });
}

/**
 * Avanzar al siguiente paso del wizard
 */
function nextUploadStep() {
    const currentStepEl = document.getElementById(`step${currentUploadStep}`);
    if (!currentStepEl) return;
    
    currentStepEl.classList.add('d-none');
    
    currentUploadStep++;
    
    const nextStepEl = document.getElementById(`step${currentUploadStep}`);
    if (nextStepEl) {
        nextStepEl.classList.remove('d-none');
    }
    
    if (currentUploadStep === 2) {
        loadUploadConfiguration();
    } else if (currentUploadStep === 3) {
        updateCurrentConfig();
    }
    
    console.log('[Upload] Paso actual:', currentUploadStep);
}

/**
 * Retroceder al paso anterior del wizard
 */
function prevUploadStep() {
    const currentStepEl = document.getElementById(`step${currentUploadStep}`);
    if (!currentStepEl) return;
    
    currentStepEl.classList.add('d-none');
    
    currentUploadStep--;
    
    const prevStepEl = document.getElementById(`step${currentUploadStep}`);
    if (prevStepEl) {
        prevStepEl.classList.remove('d-none');
    }
    
    console.log('[Upload] Paso actual:', currentUploadStep);
}

/**
 * Cargar configuración para el paso 2
 */
async function loadUploadConfiguration() {
    try {
        // Cargar configuración desde el backend
        const response = await fetch('/api/super-admin/bulk-upload/config', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Cargar tipos de elección
            const tipoSelect = document.getElementById('uploadTipoEleccion');
            if (tipoSelect) {
                tipoSelect.innerHTML = '<option value="">Seleccionar...</option>' +
                    result.data.tipos_eleccion.map(tipo => 
                        `<option value="${tipo.id}">${tipo.nombre}</option>`
                    ).join('');
            }
            
            // Cargar departamentos
            const deptSelect = document.getElementById('uploadDepartamento');
            if (deptSelect) {
                deptSelect.innerHTML = '<option value="">Seleccionar...</option>' +
                    result.data.departamentos.map(dept => 
                        `<option value="${dept.codigo}">${dept.nombre}</option>`
                    ).join('');
            }
            
            // Configurar eventos
            if (deptSelect) {
                deptSelect.addEventListener('change', loadMunicipios);
            }
        }
        
    } catch (error) {
        console.error('[Upload] Error cargando configuración:', error);
        showError('Error cargando configuración: ' + error.message);
    }
}

/**
 * Cargar municipios según departamento seleccionado
 */
async function loadMunicipios() {
    const deptCodigo = document.getElementById('uploadDepartamento').value;
    const munSelect = document.getElementById('uploadMunicipio');
    
    if (!munSelect) return;
    
    if (!deptCodigo) {
        munSelect.innerHTML = '<option value="">Seleccionar...</option>';
        return;
    }
    
    try {
        const response = await fetch(`/api/super-admin/bulk-upload/municipios/${deptCodigo}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            munSelect.innerHTML = '<option value="">Seleccionar...</option>' +
                result.data.map(mun => 
                    `<option value="${mun.codigo}">${mun.nombre}</option>`
                ).join('');
        }
    } catch (error) {
        console.error('[Upload] Error cargando municipios:', error);
    }
}

/**
 * Actualizar configuración actual en el paso 3
 */
function updateCurrentConfig() {
    uploadConfig.tipoEleccion = document.getElementById('uploadTipoEleccion')?.value;
    uploadConfig.departamento = document.getElementById('uploadDepartamento')?.value;
    uploadConfig.municipio = document.getElementById('uploadMunicipio')?.value;
    uploadConfig.validateBefore = document.getElementById('validateBeforeUpload')?.checked;
    uploadConfig.createParties = document.getElementById('createPartiesIfNotExist')?.checked;
    uploadConfig.overwrite = document.getElementById('overwriteExisting')?.checked;
    
    const configEl = document.getElementById('currentConfig');
    if (!configEl) return;
    
    const tipoText = document.getElementById('uploadTipoEleccion')?.selectedOptions[0]?.text || 'No especificado';
    const deptText = document.getElementById('uploadDepartamento')?.selectedOptions[0]?.text || 'No especificado';
    const munText = document.getElementById('uploadMunicipio')?.selectedOptions[0]?.text || 'No especificado';
    
    configEl.innerHTML = `
        <li><strong>Tipo:</strong> ${getUploadTypeText(uploadConfig.type)}</li>
        <li><strong>Elección:</strong> ${tipoText}</li>
        <li><strong>Departamento:</strong> ${deptText}</li>
        <li><strong>Municipio:</strong> ${munText}</li>
        <li><strong>Validar:</strong> ${uploadConfig.validateBefore ? 'Sí' : 'No'}</li>
    `;
    
    // Configurar drag & drop
    setupFileUpload();
}

/**
 * Obtener texto descriptivo del tipo de carga
 */
function getUploadTypeText(type) {
    const types = {
        'partidos': 'Partidos Políticos',
        'candidatos_uninominal': 'Candidatos - Elección Uninominal',
        'candidatos_lista_cerrada': 'Candidatos - Lista Cerrada',
        'candidatos_lista_abierta': 'Candidatos - Lista Abierta',
        'coaliciones': 'Coaliciones de Partidos',
        'ubicaciones': 'Ubicaciones Geográficas'
    };
    return types[type] || type;
}

/**
 * Configurar drag & drop para archivos
 */
function setupFileUpload() {
    const dropZone = document.getElementById('csvDropZone');
    const fileInput = document.getElementById('csvFileInput');
    const btnValidate = document.getElementById('btnValidate');
    
    if (!dropZone || !fileInput || !btnValidate) return;
    
    // Click en zona de drop
    dropZone.addEventListener('click', () => fileInput.click());
    
    // Drag & drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('border-primary');
    });
    
    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('border-primary');
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('border-primary');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelection(files[0]);
        }
    });
    
    // Selección de archivo
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });
}

/**
 * Manejar selección de archivo
 */
function handleFileSelection(file) {
    console.log('[Upload] Archivo seleccionado:', file.name);
    
    // Validar tipo de archivo
    if (!file.name.toLowerCase().endsWith('.csv')) {
        showError('Solo se permiten archivos CSV');
        return;
    }
    
    // Validar tamaño (10 MB)
    if (file.size > 10 * 1024 * 1024) {
        showError('El archivo es demasiado grande (máximo 10 MB)');
        return;
    }
    
    uploadFile = file;
    
    // Mostrar información del archivo
    const fileNameEl = document.getElementById('fileName');
    const fileSizeEl = document.getElementById('fileSize');
    const fileRecordsEl = document.getElementById('fileRecords');
    const fileInfoEl = document.getElementById('fileInfo');
    const btnValidate = document.getElementById('btnValidate');
    
    if (fileNameEl) fileNameEl.textContent = file.name;
    if (fileSizeEl) fileSizeEl.textContent = formatFileSize(file.size);
    if (fileRecordsEl) fileRecordsEl.textContent = 'Calculando...';
    if (fileInfoEl) fileInfoEl.classList.remove('d-none');
    if (btnValidate) btnValidate.disabled = false;
    
    // Contar registros
    countCSVRecords(file);
}

/**
 * Formatear tamaño de archivo
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Contar registros en CSV
 */
function countCSVRecords(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const text = e.target.result;
        const lines = text.split('\n').filter(line => line.trim());
        const records = Math.max(0, lines.length - 1); // -1 para el header
        const fileRecordsEl = document.getElementById('fileRecords');
        if (fileRecordsEl) {
            fileRecordsEl.textContent = records + ' registros';
        }
    };
    reader.readAsText(file);
}

/**
 * Descargar plantilla CSV
 */
function downloadTemplate() {
    const type = uploadConfig.type;
    console.log('[Upload] Descargando plantilla para:', type);
    
    // Generar plantilla según tipo
    const templates = {
        'partidos': 'codigo,nombre,nombre_corto,color,logo_url,activo\nLIBERAL,Partido Liberal Colombiano,Partido Liberal,#FF0000,,TRUE',
        'candidatos_uninominal': 'partido_codigo,candidato_nombre,candidato_cedula,es_independiente,foto_url\nLIBERAL,Juan Pérez García,12345678,FALSE,',
        'candidatos_lista_cerrada': 'partido_codigo,numero_lista,candidato_nombre,candidato_cedula,es_cabeza_lista,foto_url\nLIBERAL,1,Ana García Rodríguez,12345678,TRUE,',
        'candidatos_lista_abierta': 'partido_codigo,numero_lista,candidato_nombre,candidato_cedula,es_cabeza_lista,permite_voto_preferente,foto_url\nVERDE,1,Roberto Silva Mora,12345678,TRUE,TRUE,',
        'coaliciones': 'coalicion_nombre,partido_codigo,partido_nombre\nCoalición Centro Esperanza,VERDE,Alianza Verde',
        'ubicaciones': 'departamento_codigo,departamento_nombre,municipio_codigo,municipio_nombre,zona_codigo,puesto_codigo,puesto_nombre,direccion,latitud,longitud\n18,CAQUETÁ,001,FLORENCIA,00,01,Puesto Centro,Calle 11 # 5-42,1.6143,-75.6062'
    };
    
    const template = templates[type];
    if (template) {
        const blob = new Blob([template], { type: 'text/csv;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `plantilla_${type}.csv`;
        a.click();
        URL.revokeObjectURL(url);
    }
}

/**
 * Validar archivo antes de cargar
 */
async function validateUpload() {
    if (!uploadFile) {
        showError('Seleccione un archivo CSV');
        return;
    }
    
    console.log('[Upload] Validando archivo...');
    
    try {
        const formData = new FormData();
        formData.append('file', uploadFile);
        formData.append('type', uploadConfig.type);
        formData.append('config', JSON.stringify(uploadConfig));
        
        // Llamar al endpoint de validación
        const response = await fetch('/api/super-admin/bulk-upload/validate-csv', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            validationResults = {
                success: result.data.valid,
                records: result.data.records,
                warnings: result.data.warnings || [],
                errors: result.data.errors || []
            };
            
            showValidationResults();
            nextUploadStep();
        } else {
            showError('Error validando: ' + result.error);
        }
        
    } catch (error) {
        console.error('[Upload] Error validando:', error);
        showError('Error validando archivo: ' + error.message);
    }
}

/**
 * Mostrar resultados de validación
 */
function showValidationResults() {
    const resultsEl = document.getElementById('validationResults');
    const btnConfirm = document.getElementById('btnConfirm');
    
    if (!resultsEl || !btnConfirm) return;
    
    let html = `
        <div class="alert alert-info">
            <strong>Archivo:</strong> ${uploadFile.name}<br>
            <strong>Registros encontrados:</strong> ${validationResults.records}
        </div>
    `;
    
    if (validationResults.success) {
        html += '<div class="alert alert-success"><h6>✅ Validaciones exitosas:</h6><ul>';
        html += '<li>Formato de archivo correcto</li>';
        html += '<li>Todas las columnas requeridas presentes</li>';
        html += `<li>${validationResults.records} registros válidos</li>`;
        html += '</ul></div>';
    }
    
    if (validationResults.warnings.length > 0) {
        html += '<div class="alert alert-warning"><h6>⚠️ Advertencias:</h6><ul>';
        validationResults.warnings.forEach(warning => {
            html += `<li>${warning}</li>`;
        });
        html += '</ul></div>';
    }
    
    if (validationResults.errors.length > 0) {
        html += '<div class="alert alert-danger"><h6>❌ Errores (deben corregirse):</h6><ul>';
        validationResults.errors.forEach(error => {
            html += `<li>${error}</li>`;
        });
        html += '</ul></div>';
        btnConfirm.disabled = true;
    } else {
        btnConfirm.disabled = false;
    }
    
    resultsEl.innerHTML = html;
}

/**
 * Confirmar carga de datos
 */
async function confirmUpload() {
    console.log('[Upload] Confirmando carga...');
    
    try {
        const formData = new FormData();
        formData.append('file', uploadFile);
        formData.append('type', uploadConfig.type);
        formData.append('config', JSON.stringify(uploadConfig));
        
        // Llamar al endpoint de carga
        const response = await fetch('/api/super-admin/bulk-upload/upload-csv', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showSuccess(`Datos cargados exitosamente: ${result.data.total_created} creados, ${result.data.total_updated} actualizados`);
            
            // Resetear wizard
            resetUploadWizard();
            
            // Recargar datos según tipo
            if (uploadConfig.type.includes('candidatos')) {
                if (typeof loadCandidatos === 'function') loadCandidatos();
            } else if (uploadConfig.type === 'partidos') {
                if (typeof loadPartidos === 'function') loadPartidos();
            }
        } else {
            showError('Error cargando datos: ' + result.error);
        }
        
    } catch (error) {
        console.error('[Upload] Error cargando:', error);
        showError('Error cargando datos: ' + error.message);
    }
}

/**
 * Resetear wizard de carga
 */
function resetUploadWizard() {
    // Ocultar todos los pasos
    for (let i = 1; i <= 4; i++) {
        const stepEl = document.getElementById(`step${i}`);
        if (stepEl) stepEl.classList.add('d-none');
    }
    
    // Mostrar paso 1
    const step1 = document.getElementById('step1');
    if (step1) step1.classList.remove('d-none');
    currentUploadStep = 1;
    
    // Limpiar configuración
    uploadConfig = {};
    uploadFile = null;
    validationResults = null;
    
    // Limpiar formularios
    document.querySelectorAll('input[name="uploadType"]').forEach(radio => radio.checked = false);
    const btnNext = document.getElementById('btnNextStep1');
    if (btnNext) btnNext.disabled = true;
    
    const fileInfo = document.getElementById('fileInfo');
    if (fileInfo) fileInfo.classList.add('d-none');
    
    const csvFileInput = document.getElementById('csvFileInput');
    if (csvFileInput) csvFileInput.value = '';
}

/**
 * Mostrar mensaje de error
 */
function showError(message) {
    if (typeof Utils !== 'undefined' && Utils.showError) {
        Utils.showError(message);
    } else {
        alert('Error: ' + message);
    }
}

/**
 * Mostrar mensaje de éxito
 */
function showSuccess(message) {
    if (typeof Utils !== 'undefined' && Utils.showSuccess) {
        Utils.showSuccess(message);
    } else {
        alert(message);
    }
}

// Inicializar cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    initBulkUpload();
});
