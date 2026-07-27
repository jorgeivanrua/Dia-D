/**
 * Módulo para gestión de incidentes y delitos electorales
 */

// Variables globales
let incidentes = [];
let delitos = [];
let tiposIncidentes = {};
let tiposDelitos = {};
let fotoCaptureIncidente = null;
let fotoCaptureDelito = null;

/**
 * Inicializar módulo de incidentes y delitos
 */
async function initIncidentesDelitos() {
    try {
        // Cargar tipos de incidentes y delitos
        await cargarTiposIncidentesDelitos();
        
        // Cargar incidentes y delitos del usuario
        await cargarIncidentes();
        await cargarDelitos();
    } catch (error) {
        console.error('Error inicializando incidentes y delitos:', error);
    }
}

/**
 * Cargar tipos de incidentes y delitos desde el servidor
 */
async function cargarTiposIncidentesDelitos() {
    try {
        const [responseTiposInc, responseTiposDel] = await Promise.all([
            APIClient.obtenerTiposIncidentes(),
            APIClient.obtenerTiposDelitos()
        ]);
        
        if (responseTiposInc.tipos) {
            tiposIncidentes = responseTiposInc.tipos;
            poblarSelectTiposIncidentes();
        }
        
        if (responseTiposDel.tipos) {
            tiposDelitos = responseTiposDel.tipos;
            poblarSelectTiposDelitos();
        }
    } catch (error) {
        console.error('Error cargando tipos:', error);
    }
}

/**
 * Poblar select de tipos de incidentes
 */
function poblarSelectTiposIncidentes() {
    const select = document.getElementById('tipoIncidente');
    if (!select) return;
    
    select.innerHTML = '<option value="">Seleccione tipo de incidente...</option>';
    
    Object.entries(tiposIncidentes).forEach(([key, label]) => {
        const option = document.createElement('option');
        option.value = key;
        option.textContent = label;
        select.appendChild(option);
    });
}

/**
 * Poblar select de tipos de delitos
 */
function poblarSelectTiposDelitos() {
    const select = document.getElementById('tipoDelito');
    if (!select) return;
    
    select.innerHTML = '<option value="">Seleccione tipo de delito...</option>';
    
    Object.entries(tiposDelitos).forEach(([key, label]) => {
        const option = document.createElement('option');
        option.value = key;
        option.textContent = label;
        select.appendChild(option);
    });
}

/**
 * Cargar incidentes del usuario
 */
async function cargarIncidentes() {
    try {
        const response = await APIClient.obtenerIncidentes();
        
        if (response.incidentes) {
            incidentes = response.incidentes;
            renderizarIncidentes();
        }
    } catch (error) {
        console.error('Error cargando incidentes:', error);
        Utils.showError('Error al cargar incidentes');
    }
}

/**
 * Cargar delitos del usuario
 */
async function cargarDelitos() {
    try {
        const response = await APIClient.obtenerDelitos();
        
        if (response.delitos) {
            delitos = response.delitos;
            renderizarDelitos();
        }
    } catch (error) {
        console.error('Error cargando delitos:', error);
        Utils.showError('Error al cargar delitos');
    }
}

/**
 * Renderizar lista de incidentes
 */
function renderizarIncidentes() {
    const container = document.getElementById('incidentesLista');
    if (!container) return;
    
    if (incidentes.length === 0) {
        container.innerHTML = '<p class="text-muted text-center py-4">No hay incidentes reportados</p>';
        return;
    }
    
    container.innerHTML = incidentes.map(incidente => `
        <div class="card mb-3">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <h6 class="card-title mb-2">
                            ${incidente.titulo}
                            <span class="badge bg-${getSeveridadColor(incidente.severidad)} ms-2">
                                ${incidente.severidad_label}
                            </span>
                        </h6>
                        <p class="card-text text-muted small mb-2">
                            <i class="bi bi-tag"></i> ${incidente.tipo_incidente_label}
                        </p>
                        <p class="card-text">${incidente.descripcion}</p>
                        ${incidente.mesa_codigo ? `
                            <p class="card-text small text-muted mb-1">
                                <i class="bi bi-geo-alt"></i> Mesa: ${incidente.mesa_codigo}
                            </p>
                        ` : ''}
                        <p class="card-text small text-muted">
                            <i class="bi bi-clock"></i> ${Utils.formatDate(incidente.fecha_reporte)}
                        </p>
                    </div>
                    <div>
                        <span class="badge bg-${getEstadoIncidenteColor(incidente.estado)}">
                            ${incidente.estado_label}
                        </span>
                    </div>
                </div>
                ${incidente.notas_resolucion ? `
                    <div class="alert alert-info mt-2 mb-0">
                        <strong>Resolución:</strong> ${incidente.notas_resolucion}
                    </div>
                ` : ''}
            </div>
        </div>
    `).join('');
}

/**
 * Renderizar lista de delitos
 */
function renderizarDelitos() {
    const container = document.getElementById('delitosLista');
    if (!container) return;
    
    if (delitos.length === 0) {
        container.innerHTML = '<p class="text-muted text-center py-4">No hay delitos reportados</p>';
        return;
    }
    
    container.innerHTML = delitos.map(delito => `
        <div class="card mb-3 border-danger">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <h6 class="card-title mb-2">
                            ${delito.titulo}
                            <span class="badge bg-${getGravedadColor(delito.gravedad)} ms-2">
                                ${delito.gravedad_label}
                            </span>
                        </h6>
                        <p class="card-text text-muted small mb-2">
                            <i class="bi bi-shield-exclamation"></i> ${delito.tipo_delito_label}
                        </p>
                        <p class="card-text">${delito.descripcion}</p>
                        ${delito.testigos_adicionales ? `
                            <p class="card-text small mb-1">
                                <strong>Testigos:</strong> ${delito.testigos_adicionales}
                            </p>
                        ` : ''}
                        ${delito.mesa_codigo ? `
                            <p class="card-text small text-muted mb-1">
                                <i class="bi bi-geo-alt"></i> Mesa: ${delito.mesa_codigo}
                            </p>
                        ` : ''}
                        <p class="card-text small text-muted">
                            <i class="bi bi-clock"></i> ${Utils.formatDate(delito.fecha_reporte)}
                        </p>
                    </div>
                    <div>
                        <span class="badge bg-${getEstadoDelitoColor(delito.estado)}">
                            ${delito.estado_label}
                        </span>
                        ${delito.denunciado_formalmente ? `
                            <br><span class="badge bg-success mt-1">Denunciado</span>
                        ` : ''}
                    </div>
                </div>
                ${delito.resultado_investigacion ? `
                    <div class="alert alert-info mt-2 mb-0">
                        <strong>Investigación:</strong> ${delito.resultado_investigacion}
                    </div>
                ` : ''}
                ${delito.numero_denuncia ? `
                    <div class="alert alert-success mt-2 mb-0">
                        <strong>Denuncia Formal:</strong> ${delito.numero_denuncia}<br>
                        <strong>Autoridad:</strong> ${delito.autoridad_competente}
                    </div>
                ` : ''}
            </div>
        </div>
    `).join('');
}

/**
 * Abrir modal para reportar incidente
 */
function reportarIncidente() {
    // Verificar que haya una mesa verificada
    if (!window.mesaSeleccionadaDashboard || !window.presenciaVerificada) {
        Utils.showError('Debe seleccionar una mesa y verificar su presencia antes de reportar incidentes');
        return;
    }
    
    // Mostrar información de la mesa en el modal
    const mesaInfoElement = document.getElementById('mesaInfoIncidente');
    if (mesaInfoElement && window.mesaSeleccionadaDashboard) {
        mesaInfoElement.textContent = `Mesa ${window.mesaSeleccionadaDashboard.mesa_codigo} - ${window.mesaSeleccionadaDashboard.puesto_nombre || ''}`;
    }
    
    // Limpiar formulario
    document.getElementById('formIncidente').reset();
    
    // Inicializar componente de fotos si no existe
    if (!fotoCaptureIncidente) {
        fotoCaptureIncidente = new FotoCaptureComponent('foto-capture-incidente', {
            maxFiles: 5,
            onFilesChange: (files) => {
                console.log('Fotos de incidente actualizadas:', files.length);
            }
        });
    } else {
        fotoCaptureIncidente.clear();
    }
    
    // Abrir modal
    const modal = new bootstrap.Modal(document.getElementById('incidenteModal'));
    modal.show();
}

/**
 * Guardar incidente
 */
async function guardarIncidente() {
    const form = document.getElementById('formIncidente');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const formData = new FormData(form);
    
    // Usar la mesa verificada (mesaSeleccionadaDashboard)
    const mesaId = window.mesaSeleccionadaDashboard ? window.mesaSeleccionadaDashboard.id : null;
    
    if (!mesaId) {
        Utils.showError('No hay una mesa verificada. Por favor, seleccione y verifique una mesa primero.');
        return;
    }
    
    const data = {
        tipo_incidente: formData.get('tipo_incidente'),
        titulo: formData.get('titulo'),
        descripcion: formData.get('descripcion'),
        severidad: formData.get('severidad'),
        mesa_id: mesaId,
        tipo: 'incidente'
    };
    
    // Obtener fotos antes de intentar guardar
    const fotos = fotoCaptureIncidente ? fotoCaptureIncidente.getFiles() : [];
    
    try {
        // Verificar si hay conexión
        if (!navigator.onLine) {
            // Guardar offline directamente
            await guardarIncidenteOffline(data, fotos);
            return;
        }
        
        Utils.showInfo('Reportando incidente...');
        
        const response = await APIClient.crearIncidente(data);
        
        if (response.success && response.data) {
            const incidenteId = response.data.id;
            
            // Subir fotos si hay
            if (fotos.length > 0) {
                Utils.showInfo('Subiendo evidencia fotográfica...');
                
                try {
                    await window.uploadManager.uploadWithProgressModal(
                        fotos,
                        'incidente',
                        incidenteId
                    );
                } catch (uploadError) {
                    console.error('Error subiendo fotos:', uploadError);
                    Utils.showWarning('Incidente creado pero hubo errores al subir algunas fotos');
                }
            }
            
            Utils.showSuccess('✓ Incidente reportado exitosamente');
            
            // Cerrar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('incidenteModal'));
            if (modal) modal.hide();
            
            // Recargar incidentes
            await cargarIncidentes();
        }
    } catch (error) {
        console.error('Error guardando incidente:', error);
        
        // Si falla, intentar guardar offline
        if (window.syncManager && window.indexedDBService) {
            try {
                await guardarIncidenteOffline(data, fotos);
            } catch (offlineError) {
                console.error('Error guardando offline:', offlineError);
                Utils.showError('Error al reportar incidente: ' + error.message);
            }
        } else {
            Utils.showError('Error al reportar incidente: ' + error.message);
        }
    }
}

/**
 * Guardar incidente offline
 */
async function guardarIncidenteOffline(data, fotos) {
    try {
        // Guardar reporte en IndexedDB
        const tempId = await window.syncManager.guardarReporteOffline(data);
        
        // Guardar fotos offline si hay
        if (fotos && fotos.length > 0) {
            for (const foto of fotos) {
                // Convertir foto a base64
                const base64 = await convertirFotoABase64(foto);
                
                const evidencia = {
                    file_data: base64,
                    filename: foto.name,
                    mime_type: foto.type,
                    tipo_reporte: 'incidente',
                    fecha_captura: new Date().toISOString()
                };
                
                await window.syncManager.guardarEvidenciaOffline(evidencia, tempId);
            }
        }
        
        Utils.showWarning('⚠️ Sin conexión. Incidente guardado localmente y se sincronizará automáticamente.');
        
        // Cerrar modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('incidenteModal'));
        if (modal) modal.hide();
        
        // Limpiar formulario
        document.getElementById('formIncidente').reset();
        if (fotoCaptureIncidente) fotoCaptureIncidente.clear();
        
    } catch (error) {
        console.error('Error guardando offline:', error);
        throw error;
    }
}

/**
 * Abrir modal para reportar delito
 */
function reportarDelito() {
    // Verificar que haya una mesa verificada
    if (!window.mesaSeleccionadaDashboard || !window.presenciaVerificada) {
        Utils.showError('Debe seleccionar una mesa y verificar su presencia antes de reportar delitos');
        return;
    }
    
    // Mostrar información de la mesa en el modal
    const mesaInfoElement = document.getElementById('mesaInfoDelito');
    if (mesaInfoElement && window.mesaSeleccionadaDashboard) {
        mesaInfoElement.textContent = `Mesa ${window.mesaSeleccionadaDashboard.mesa_codigo} - ${window.mesaSeleccionadaDashboard.puesto_nombre || ''}`;
    }
    
    // Limpiar formulario
    document.getElementById('formDelito').reset();
    
    // Inicializar componente de fotos si no existe
    if (!fotoCaptureDelito) {
        fotoCaptureDelito = new FotoCaptureComponent('foto-capture-delito', {
            maxFiles: 5,
            onFilesChange: (files) => {
                console.log('Fotos de delito actualizadas:', files.length);
            }
        });
    } else {
        fotoCaptureDelito.clear();
    }
    
    // Abrir modal
    const modal = new bootstrap.Modal(document.getElementById('delitoModal'));
    modal.show();
}

/**
 * Guardar delito
 */
async function guardarDelito() {
    const form = document.getElementById('formDelito');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const formData = new FormData(form);
    
    // Usar la mesa verificada (mesaSeleccionadaDashboard)
    const mesaId = window.mesaSeleccionadaDashboard ? window.mesaSeleccionadaDashboard.id : null;
    
    if (!mesaId) {
        Utils.showError('No hay una mesa verificada. Por favor, seleccione y verifique una mesa primero.');
        return;
    }
    
    const data = {
        tipo_delito: formData.get('tipo_delito'),
        titulo: formData.get('titulo'),
        descripcion: formData.get('descripcion'),
        gravedad: formData.get('gravedad'),
        testigos_adicionales: formData.get('testigos_adicionales') || '',
        mesa_id: mesaId,
        tipo: 'delito'
    };
    
    // Obtener fotos antes de intentar guardar
    const fotos = fotoCaptureDelito ? fotoCaptureDelito.getFiles() : [];
    
    try {
        // Verificar si hay conexión
        if (!navigator.onLine) {
            // Guardar offline directamente
            await guardarDelitoOffline(data, fotos);
            return;
        }
        
        Utils.showInfo('Reportando delito...');
        
        const response = await APIClient.crearDelito(data);
        
        if (response.success && response.data) {
            const delitoId = response.data.id;
            
            // Subir fotos si hay
            if (fotos.length > 0) {
                Utils.showInfo('Subiendo evidencia fotográfica...');
                
                try {
                    await window.uploadManager.uploadWithProgressModal(
                        fotos,
                        'delito',
                        delitoId
                    );
                } catch (uploadError) {
                    console.error('Error subiendo fotos:', uploadError);
                    Utils.showWarning('Delito creado pero hubo errores al subir algunas fotos');
                }
            }
            
            Utils.showSuccess('✓ Delito reportado exitosamente');
            
            // Cerrar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('delitoModal'));
            if (modal) modal.hide();
            
            // Recargar delitos
            await cargarDelitos();
        }
    } catch (error) {
        console.error('Error guardando delito:', error);
        
        // Si falla, intentar guardar offline
        if (window.syncManager && window.indexedDBService) {
            try {
                await guardarDelitoOffline(data, fotos);
            } catch (offlineError) {
                console.error('Error guardando offline:', offlineError);
                Utils.showError('Error al reportar delito: ' + error.message);
            }
        } else {
            Utils.showError('Error al reportar delito: ' + error.message);
        }
    }
}

/**
 * Guardar delito offline
 */
async function guardarDelitoOffline(data, fotos) {
    try {
        // Guardar reporte en IndexedDB
        const tempId = await window.syncManager.guardarReporteOffline(data);
        
        // Guardar fotos offline si hay
        if (fotos && fotos.length > 0) {
            for (const foto of fotos) {
                // Convertir foto a base64
                const base64 = await convertirFotoABase64(foto);
                
                const evidencia = {
                    file_data: base64,
                    filename: foto.name,
                    mime_type: foto.type,
                    tipo_reporte: 'delito',
                    fecha_captura: new Date().toISOString()
                };
                
                await window.syncManager.guardarEvidenciaOffline(evidencia, tempId);
            }
        }
        
        Utils.showWarning('⚠️ Sin conexión. Delito guardado localmente y se sincronizará automáticamente.');
        
        // Cerrar modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('delitoModal'));
        if (modal) modal.hide();
        
        // Limpiar formulario
        document.getElementById('formDelito').reset();
        if (fotoCaptureDelito) fotoCaptureDelito.clear();
        
    } catch (error) {
        console.error('Error guardando offline:', error);
        throw error;
    }
}

/**
 * Convertir foto a base64
 */
function convertirFotoABase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

/**
 * Obtener color según severidad
 */
function getSeveridadColor(severidad) {
    const colors = {
        'baja': 'info',
        'media': 'warning',
        'alta': 'danger',
        'critica': 'dark'
    };
    return colors[severidad] || 'secondary';
}

/**
 * Obtener color según gravedad
 */
function getGravedadColor(gravedad) {
    const colors = {
        'leve': 'info',
        'media': 'warning',
        'grave': 'danger',
        'muy_grave': 'dark'
    };
    return colors[gravedad] || 'secondary';
}

/**
 * Obtener color según estado de incidente
 */
function getEstadoIncidenteColor(estado) {
    const colors = {
        'reportado': 'primary',
        'en_revision': 'warning',
        'resuelto': 'success',
        'escalado': 'danger'
    };
    return colors[estado] || 'secondary';
}

/**
 * Obtener color según estado de delito
 */
function getEstadoDelitoColor(estado) {
    const colors = {
        'reportado': 'primary',
        'en_investigacion': 'warning',
        'investigado': 'info',
        'denunciado': 'success',
        'archivado': 'secondary'
    };
    return colors[estado] || 'secondary';
}

// Exponer funciones globalmente
window.initIncidentesDelitos = initIncidentesDelitos;
window.reportarIncidente = reportarIncidente;
window.guardarIncidente = guardarIncidente;
window.reportarDelito = reportarDelito;
window.guardarDelito = guardarDelito;
window.cargarIncidentes = cargarIncidentes;
window.cargarDelitos = cargarDelitos;
window.guardarIncidenteOffline = guardarIncidenteOffline;
window.guardarDelitoOffline = guardarDelitoOffline;


// ============================================
// INTEGRACIÓN CON SYNC MANAGER (LEGACY)
// ============================================

/**
 * Reportar incidente con sincronización automática
 */
async function reportarIncidenteConSync(data) {
    try {
        // Intentar guardar en el servidor primero
        const response = await APIClient.reportarIncidente(data);
        
        if (response.success) {
            Utils.showSuccess('✓ Incidente reportado exitosamente');
            return response;
        } else {
            throw new Error(response.error || 'Error al reportar incidente');
        }
    } catch (error) {
        console.error('Error reportando incidente, guardando localmente:', error);
        
        // Guardar localmente si falla
        if (window.syncManager) {
            window.syncManager.saveIncidentLocally(data);
            Utils.showWarning('⚠️ Incidente guardado localmente. Se sincronizará automáticamente.');
        } else {
            throw error;
        }
    }
}

/**
 * Reportar delito con sincronización automática
 */
async function reportarDelitoConSync(data) {
    try {
        // Intentar guardar en el servidor primero
        const response = await APIClient.reportarDelito(data);
        
        if (response.success) {
            Utils.showSuccess('✓ Delito reportado exitosamente');
            return response;
        } else {
            throw new Error(response.error || 'Error al reportar delito');
        }
    } catch (error) {
        console.error('Error reportando delito, guardando localmente:', error);
        
        // Guardar localmente si falla
        if (window.syncManager) {
            window.syncManager.saveCrimeLocally(data);
            Utils.showWarning('⚠️ Delito guardado localmente. Se sincronizará automáticamente.');
        } else {
            throw error;
        }
    }
}

// Exponer funciones globalmente
window.reportarIncidenteConSync = reportarIncidenteConSync;
window.reportarDelitoConSync = reportarDelitoConSync;
