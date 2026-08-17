/**
 * Dashboard del Coordinador Municipal
 */

// Estado global
let currentUser = null;
let userLocation = null;
let puestos = [];
let puestosOriginales = [];
let puestoSeleccionado = null;
let filtroEstado = '';
let autoRefreshInterval = null;
let chartConsolidado = null;

// Inicialización
document.addEventListener('DOMContentLoaded', async function() {
    try {
        console.log('[Coordinador Municipal] Inicializando dashboard...');
        
        await loadUserProfile();
        await loadPuestos();
        await loadEstadisticas();
        await loadConsolidadoMunicipal();
        await loadDiscrepancias();
        
        console.log('[Coordinador Municipal] Dashboard inicializado correctamente');
        
        // Auto-refresh cada 60 segundos
        autoRefreshInterval = setInterval(() => {
            loadPuestos();
            loadEstadisticas();
            loadConsolidadoMunicipal();
            loadDiscrepancias();
        }, 60000);
    } catch (error) {
        console.error('[Coordinador Municipal] Error inicializando dashboard:', error);
        Utils.showError('Error al inicializar el dashboard. Por favor, recarga la página.');
    }
});

// Limpiar interval al salir
window.addEventListener('beforeunload', function() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
});

/**
 * Cargar perfil del coordinador
 */
async function loadUserProfile() {
    try {
        console.log('[Coordinador Municipal] Cargando perfil...');
        const response = await APIClient.get('/auth/profile');
        
        if (response && response.success) {
            currentUser = response.data.user;
            userLocation = response.data.ubicacion;
            
            console.log('[Coordinador Municipal] Perfil cargado:', currentUser);
            console.log('[Coordinador Municipal] Ubicación:', userLocation);
            
            // Mostrar información del municipio
            const municipioInfo = document.getElementById('municipioInfo');
            if (municipioInfo && userLocation) {
                municipioInfo.textContent = 
                    `${userLocation.municipio_nombre || userLocation.nombre_completo} - Código: ${userLocation.municipio_codigo || 'N/A'}`;
            }
        } else {
            throw new Error(response?.error || 'Error al cargar perfil');
        }
    } catch (error) {
        console.error('[Coordinador Municipal] Error loading profile:', error);
        const municipioInfo = document.getElementById('municipioInfo');
        if (municipioInfo) {
            municipioInfo.textContent = 'Error al cargar información del municipio';
        }
        // No mostrar error al usuario en este caso, solo log
    }
}

/**
 * Cargar estadísticas detalladas del municipio
 */
async function loadEstadisticas() {
    try {
        const response = await APIClient.get('/coordinador-municipal/estadisticas');
        
        if (response.success) {
            const stats = response.data;
            renderEstadisticasDetalladas(stats);
        } else {
            throw new Error(response.error || 'Error al cargar estadísticas');
        }
    } catch (error) {
        console.error('Error loading estadisticas:', error);
        Utils.showError('Error al cargar estadísticas detalladas');
    }
}

/**
 * Renderizar estadísticas detalladas
 */
function renderEstadisticasDetalladas(stats) {
    const container = document.getElementById('estadisticasDetalladas');
    
    if (!container) return;
    
    const resumen = stats.resumen_general || {};
    const consolidado = stats.consolidado || {};
    
    let html = `
        <div class="row g-3">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h6 class="card-title">Resumen General</h6>
                        <p><strong>Total Puestos:</strong> ${resumen.total_puestos || 0}</p>
                        <p><strong>Puestos Completos:</strong> ${resumen.puestos_completos || 0}</p>
                        <p><strong>Formularios Validados:</strong> ${resumen.formularios_validados || 0}</p>
                        <p><strong>Avance:</strong> ${(resumen.porcentaje_avance || 0).toFixed(1)}%</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h6 class="card-title">Participación</h6>
                        <p><strong>Total Votos:</strong> ${Utils.formatNumber(consolidado.total_votos || 0)}</p>
                        <p><strong>Votantes Registrados:</strong> ${Utils.formatNumber(consolidado.total_votantes_registrados || 0)}</p>
                        <p><strong>Participación:</strong> ${(consolidado.participacion_porcentaje || 0).toFixed(2)}%</p>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Agregar tasa de rechazo si existe
    if (stats.tasa_rechazo_por_puesto && stats.tasa_rechazo_por_puesto.length > 0) {
        html += `
            <div class="card mt-3">
                <div class="card-body">
                    <h6 class="card-title">Puestos con Mayor Tasa de Rechazo</h6>
                    <div class="table-responsive">
                        <table class="table table-sm">
                            <thead>
                                <tr>
                                    <th>Puesto</th>
                                    <th>Rechazados</th>
                                    <th>Total</th>
                                    <th>Tasa</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${stats.tasa_rechazo_por_puesto.slice(0, 5).map(p => `
                                    <tr>
                                        <td>${p.puesto_nombre}</td>
                                        <td>${p.rechazados}</td>
                                        <td>${p.total}</td>
                                        <td><span class="badge bg-${p.tasa_rechazo > 20 ? 'danger' : 'warning'}">${p.tasa_rechazo.toFixed(1)}%</span></td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;
    }
    
    container.innerHTML = html;
}

/**
 * Cargar lista de puestos
 */
async function loadPuestos() {
    try {
        const params = {};
        if (filtroEstado) {
            params.estado = filtroEstado;
        }
        
        const response = await APIClient.get('/coordinador-municipal/puestos', params);
        
        if (response.success) {
            puestosOriginales = response.data.puestos || [];
            puestos = [...puestosOriginales];
            const stats = response.data.estadisticas || {};
            
            // Actualizar estadísticas
            updateEstadisticas(stats);
            
            // Renderizar tabla
            renderPuestosTable(puestos);
        } else {
            throw new Error(response.error || 'Error desconocido');
        }
    } catch (error) {
        console.error('Error loading puestos:', error);
        const tbody = document.querySelector('#puestosTable tbody');
        const errorMsg = error.message || 'Error al cargar puestos';
        tbody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center py-4">
                    <p class="text-danger">❌ ${errorMsg}</p>
                    <button class="btn btn-sm btn-outline-primary mt-2" onclick="loadPuestos()">
                        <i class="bi bi-arrow-clockwise"></i> Reintentar
                    </button>
                </td>
            </tr>
        `;
    }
}

/**
 * Actualizar estadísticas generales
 */
function updateEstadisticas(stats) {
    const container = document.getElementById('estadisticasGenerales');
    
    const totalPuestos = stats.total_puestos || 0;
    const puestosCompletos = stats.puestos_completos || 0;
    const puestosIncompletos = stats.puestos_incompletos || 0;
    const puestosConDiscrepancias = stats.puestos_con_discrepancias || 0;
    const cobertura = stats.cobertura_porcentaje || 0;
    
    container.innerHTML = `
        <div class="stat-card card p-2 success">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <small class="text-muted">Completos</small>
                    <h4 class="mb-0">${puestosCompletos}</h4>
                </div>
                <i class="bi bi-check-circle text-success" style="font-size: 2rem;"></i>
            </div>
        </div>
        
        <div class="stat-card card p-2 warning">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <small class="text-muted">Incompletos</small>
                    <h4 class="mb-0">${puestosIncompletos}</h4>
                </div>
                <i class="bi bi-hourglass-split text-warning" style="font-size: 2rem;"></i>
            </div>
        </div>
        
        <div class="stat-card card p-2 danger">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <small class="text-muted">Con Discrepancias</small>
                    <h4 class="mb-0">${puestosConDiscrepancias}</h4>
                </div>
                <i class="bi bi-exclamation-triangle text-danger" style="font-size: 2rem;"></i>
            </div>
        </div>
        
        <div class="card p-2 bg-light">
            <div class="text-center">
                <small class="text-muted">Cobertura</small>
                <h3 class="mb-0">${cobertura.toFixed(1)}%</h3>
                <div class="progress mt-2" style="height: 8px;">
                    <div class="progress-bar ${cobertura >= 80 ? 'bg-success' : 'bg-warning'}" 
                         style="width: ${cobertura}%"></div>
                </div>
                <small class="text-muted">${puestosCompletos} de ${totalPuestos} puestos</small>
            </div>
        </div>
    `;
}

/**
 * Renderizar tabla de puestos
 */
function renderPuestosTable(puestos) {
    const tbody = document.querySelector('#puestosTable tbody');
    
    if (puestos.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center py-4">
                    <p class="text-muted">No hay puestos ${filtroEstado ? 'en estado ' + filtroEstado : ''}</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = puestos.map(puesto => {
        const estadoBadge = getEstadoBadge(puesto.estado);
        const discrepanciaBadge = puesto.tiene_discrepancias ? 
            '<span class="badge bg-danger discrepancia-badge ms-1">!</span>' : '';
        const porcentaje = puesto.porcentaje_avance || 0;
        const coordinadorNombre = puesto.coordinador?.nombre || 'Sin asignar';
        
        return `
            <tr class="puesto-row ${puestoSeleccionado?.id === puesto.id ? 'selected' : ''}" 
                onclick="seleccionarPuesto(${puesto.id})">
                <td>
                    <strong>${puesto.codigo}</strong>${discrepanciaBadge}<br>
                    <small class="text-muted">${puesto.nombre}</small>
                </td>
                <td>
                    <small>${coordinadorNombre}</small>
                </td>
                <td class="text-center">
                    <div class="progress" style="height: 20px;">
                        <div class="progress-bar ${porcentaje >= 100 ? 'bg-success' : 'bg-primary'}" 
                             style="width: ${porcentaje}%">
                            ${porcentaje.toFixed(0)}%
                        </div>
                    </div>
                    <small class="text-muted">${puesto.mesas_reportadas}/${puesto.total_mesas}</small>
                </td>
                <td class="text-center">${estadoBadge}</td>
            </tr>
        `;
    }).join('');
}

/**
 * Obtener badge de estado
 */
function getEstadoBadge(estado) {
    const badges = {
        'completo': '<span class="badge badge-status bg-success">Completo</span>',
        'incompleto': '<span class="badge badge-status bg-warning text-dark">Incompleto</span>',
        'con_discrepancias': '<span class="badge badge-status bg-danger">Con Discrepancias</span>'
    };
    return badges[estado] || `<span class="badge badge-status bg-secondary">${estado}</span>`;
}

/**
 * Filtrar puestos por estado
 */
function filtrarPuestos(estado) {
    filtroEstado = estado;
    
    // Actualizar botones activos
    document.querySelectorAll('#filterButtons button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Recargar puestos
    loadPuestos();
}

/**
 * Buscar puesto
 */
function buscarPuesto() {
    const query = document.getElementById('searchPuesto').value.toLowerCase().trim();
    
    if (!query) {
        puestos = [...puestosOriginales];
    } else {
        puestos = puestosOriginales.filter(p => 
            p.codigo.toLowerCase().includes(query) || 
            p.nombre.toLowerCase().includes(query)
        );
    }
    
    renderPuestosTable(puestos);
}

/**
 * Seleccionar puesto para ver detalles
 */
async function seleccionarPuesto(puestoId) {
    try {
        puestoSeleccionado = puestos.find(p => p.id === puestoId);
        
        // Actualizar tabla para resaltar selección
        renderPuestosTable(puestos);
        
        // Cargar detalles del puesto
        const response = await APIClient.get(`/coordinador-municipal/puesto/${puestoId}`);
        
        if (response.success) {
            renderDetallePuesto(response.data);
        }
    } catch (error) {
        console.error('Error loading puesto details:', error);
        Utils.showError('Error al cargar detalles del puesto: ' + error.message);
    }
}

/**
 * Renderizar detalles del puesto
 */
function renderDetallePuesto(data) {
    const container = document.getElementById('detallePuesto');
    
    const puesto = data.puesto || {};
    const coordinador = data.coordinador || {};
    const estadisticas = data.estadisticas || {};
    
    container.innerHTML = `
        <h6 class="border-bottom pb-2">${puesto.nombre}</h6>
        
        <div class="mb-3">
            <small class="text-muted">Código:</small>
            <div><strong>${puesto.codigo}</strong></div>
        </div>
        
        <div class="mb-3">
            <small class="text-muted">Total Mesas:</small>
            <div><strong>${puesto.total_mesas}</strong></div>
        </div>
        
        <div class="mb-3">
            <small class="text-muted">Coordinador:</small>
            <div>${coordinador.nombre}</div>
            ${coordinador.telefono ? `<small class="text-muted">${coordinador.telefono}</small>` : ''}
        </div>
        
        ${coordinador.ultimo_acceso ? `
            <div class="mb-3">
                <small class="text-muted">Último acceso:</small>
                <div><small>${Utils.formatDate(coordinador.ultimo_acceso)}</small></div>
            </div>
        ` : ''}
        
        <div class="mb-3">
            <small class="text-muted">Avance:</small>
            <div class="progress mt-1">
                <div class="progress-bar" style="width: ${estadisticas.porcentaje_avance || 0}%">
                    ${(estadisticas.porcentaje_avance || 0).toFixed(0)}%
                </div>
            </div>
        </div>
        
        <button class="btn btn-sm btn-outline-primary w-100" onclick="verPuestoCompleto(${puesto.id})">
            <i class="bi bi-eye"></i> Ver Detalles Completos
        </button>
    `;
}

/**
 * Ver puesto completo (placeholder)
 */
function verPuestoCompleto(puestoId) {
    Utils.showInfo('Funcionalidad de vista completa en desarrollo');
}


/**
 * Cargar consolidado municipal
 */
async function loadConsolidadoMunicipal() {
    try {
        const response = await APIClient.get('/coordinador-municipal/consolidado');
        
        if (response.success) {
            renderConsolidado(response.data);
        } else {
            throw new Error(response.error || 'Error al cargar consolidado');
        }
    } catch (error) {
        console.error('Error loading consolidado:', error);
        const errorMsg = error.message || 'Error al cargar consolidado';
        document.getElementById('consolidadoMunicipal').innerHTML = `
            <div class="text-center py-3">
                <p class="text-danger mb-2">❌ ${errorMsg}</p>
                <button class="btn btn-sm btn-outline-primary" onclick="loadConsolidadoMunicipal()">
                    <i class="bi bi-arrow-clockwise"></i> Reintentar
                </button>
            </div>
        `;
    }
}

/**
 * Renderizar consolidado
 */
function renderConsolidado(data) {
    const container = document.getElementById('consolidadoMunicipal');
    
    if (!data || !data.votos_por_partido || data.votos_por_partido.length === 0) {
        container.innerHTML = '<p class="text-muted">No hay datos consolidados aún</p>';
        return;
    }
    
    const resumen = data.resumen;
    const participacion = resumen.participacion_porcentaje || 0;
    
    let html = `
        <div class="mb-3">
            <small class="text-muted">Total Votos</small>
            <h4>${Utils.formatNumber(resumen.total_votos)}</h4>
            <small class="text-muted">Participación: ${participacion.toFixed(2)}%</small>
        </div>
        <hr>
        <h6 class="mb-2">Votos por Partido</h6>
    `;
    
    data.votos_por_partido.forEach(partido => {
        html += `
            <div class="mb-2">
                <div class="d-flex justify-content-between align-items-center mb-1">
                    <small>
                        <span style="display: inline-block; width: 10px; height: 10px; background-color: ${partido.partido_color}; border-radius: 2px; margin-right: 4px;"></span>
                        ${partido.partido_nombre_corto}
                    </small>
                    <strong>${Utils.formatNumber(partido.total_votos)}</strong>
                </div>
                <div class="progress" style="height: 8px;">
                    <div class="progress-bar" role="progressbar" 
                         style="width: ${partido.porcentaje}%; background-color: ${partido.partido_color};"
                         aria-valuenow="${partido.porcentaje}" aria-valuemin="0" aria-valuemax="100">
                    </div>
                </div>
                <small class="text-muted">${partido.porcentaje.toFixed(2)}%</small>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

/**
 * Cargar discrepancias
 */
async function loadDiscrepancias() {
    try {
        const response = await APIClient.get('/coordinador-municipal/discrepancias');
        
        if (response.success) {
            renderDiscrepancias(response.data);
        } else {
            throw new Error(response.error || 'Error al cargar discrepancias');
        }
    } catch (error) {
        console.error('Error loading discrepancias:', error);
        document.getElementById('discrepanciasPanel').innerHTML = `
            <div class="text-center py-3">
                <p class="text-danger mb-2">❌ Error al cargar alertas</p>
                <button class="btn btn-sm btn-outline-primary" onclick="loadDiscrepancias()">
                    <i class="bi bi-arrow-clockwise"></i> Reintentar
                </button>
            </div>
        `;
    }
}

/**
 * Renderizar discrepancias
 */
function renderDiscrepancias(discrepancias) {
    const container = document.getElementById('discrepanciasPanel');
    
    if (!discrepancias || discrepancias.length === 0) {
        container.innerHTML = `
            <div class="text-center py-3">
                <i class="bi bi-check-circle text-success" style="font-size: 2rem;"></i>
                <p class="text-muted mb-0">No hay discrepancias detectadas</p>
            </div>
        `;
        return;
    }
    
    // Agrupar por severidad
    const criticas = discrepancias.filter(d => d.severidad === 'critica');
    const altas = discrepancias.filter(d => d.severidad === 'alta');
    const medias = discrepancias.filter(d => d.severidad === 'media');
    const bajas = discrepancias.filter(d => d.severidad === 'baja');
    
    let html = '';
    
    // Mostrar críticas primero
    if (criticas.length > 0) {
        html += '<h6 class="text-danger mb-2"><i class="bi bi-exclamation-octagon"></i> Críticas</h6>';
        criticas.slice(0, 3).forEach(d => {
            html += renderDiscrepanciaItem(d);
        });
    }
    
    // Mostrar altas
    if (altas.length > 0) {
        html += '<h6 class="text-warning mb-2 mt-3"><i class="bi bi-exclamation-triangle"></i> Altas</h6>';
        altas.slice(0, 2).forEach(d => {
            html += renderDiscrepanciaItem(d);
        });
    }
    
    // Mostrar total
    html += `
        <div class="mt-3 text-center">
            <small class="text-muted">
                Total: ${discrepancias.length} discrepancia(s) detectada(s)
            </small>
        </div>
    `;
    
    container.innerHTML = html;
}

/**
 * Renderizar item de discrepancia
 */
function renderDiscrepanciaItem(discrepancia) {
    const severidadClass = {
        'critica': 'danger',
        'alta': 'warning',
        'media': 'info',
        'baja': 'secondary'
    };
    
    const badgeClass = severidadClass[discrepancia.severidad] || 'secondary';
    
    return `
        <div class="alert alert-${badgeClass} py-2 px-2 mb-2" role="alert" 
             style="cursor: pointer;" onclick="irAPuesto(${discrepancia.puesto_id})">
            <small>
                <strong>${discrepancia.puesto_nombre}</strong><br>
                ${discrepancia.descripcion}
            </small>
        </div>
    `;
}

/**
 * Ir a puesto desde discrepancia
 */
function irAPuesto(puestoId) {
    seleccionarPuesto(puestoId);
    
    // Scroll a la tabla de puestos
    document.querySelector('#puestosTable').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Generar E-24 Municipal
 */
async function generarE24Municipal() {
    try {
        // Mostrar modal de confirmación
        const modal = new bootstrap.Modal(document.getElementById('e24Modal'));
        
        // Validar requisitos primero
        const response = await APIClient.get('/coordinador-municipal/puestos');
        
        if (response.success) {
            const stats = response.data.estadisticas || {};
            const cobertura = stats.cobertura_porcentaje || 0;
            
            let validacionesHtml = '';
            
            if (cobertura >= 80) {
                validacionesHtml = `
                    <div class="alert alert-success">
                        <i class="bi bi-check-circle"></i> Se cumplen los requisitos mínimos
                        <ul class="mb-0 mt-2">
                            <li>Cobertura: ${cobertura.toFixed(1)}% (mínimo 80%)</li>
                            <li>Puestos completos: ${stats.puestos_completos} de ${stats.total_puestos}</li>
                        </ul>
                    </div>
                `;
            } else {
                validacionesHtml = `
                    <div class="alert alert-danger">
                        <i class="bi bi-x-circle"></i> No se cumplen los requisitos mínimos
                        <ul class="mb-0 mt-2">
                            <li>Cobertura: ${cobertura.toFixed(1)}% (se requiere mínimo 80%)</li>
                            <li>Puestos completos: ${stats.puestos_completos} de ${stats.total_puestos}</li>
                        </ul>
                    </div>
                `;
                
                // Deshabilitar botón de generar
                document.querySelector('#e24Modal .btn-primary').disabled = true;
            }
            
            document.getElementById('e24Validaciones').innerHTML = validacionesHtml;
        }
        
        modal.show();
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al validar requisitos: ' + error.message);
    }
}

/**
 * Confirmar generación de E-24
 */
async function confirmarGenerarE24() {
    try {
        // Tipo de elección por defecto (debería venir de configuración)
        const tipo_eleccion_id = 1;
        
        const response = await APIClient.post('/coordinador-municipal/e24-municipal', {
            tipo_eleccion_id: tipo_eleccion_id
        });
        
        if (response.success) {
            Utils.showSuccess('Formulario E-24 Municipal generado exitosamente');
            
            // Cerrar modal
            bootstrap.Modal.getInstance(document.getElementById('e24Modal')).hide();
            
            // Descargar PDF
            if (response.data.pdf_url) {
                window.open(response.data.pdf_url, '_blank');
            }
        } else {
            throw new Error(response.error || 'Error al generar E-24');
        }
    } catch (error) {
        console.error('Error generating E-24:', error);
        Utils.showError('Error al generar E-24: ' + error.message);
    }
}

/**
 * ⭐ MEJORADO: Exportar datos con opciones de formato
 */
async function exportarDatos() {
    try {
        // Mostrar modal de opciones de exportación
        const modalHtml = `
            <div class="modal fade" id="exportarModalMunicipal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="bi bi-download"></i> Exportar Datos Municipales
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p>Seleccione el formato de exportación:</p>
                            <div class="d-grid gap-2">
                                <button class="btn btn-outline-success" onclick="exportarFormatoMunicipal('csv')">
                                    <i class="bi bi-filetype-csv"></i> Exportar como CSV
                                </button>
                                <button class="btn btn-outline-primary" onclick="exportarFormatoMunicipal('excel')">
                                    <i class="bi bi-file-earmark-excel"></i> Exportar como Excel
                                </button>
                                <button class="btn btn-outline-danger" onclick="exportarFormatoMunicipal('pdf')">
                                    <i class="bi bi-filetype-pdf"></i> Exportar como PDF
                                </button>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Agregar modal al DOM
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        // Mostrar modal
        const modal = new bootstrap.Modal(document.getElementById('exportarModalMunicipal'));
        modal.show();
        
        // Limpiar modal al cerrar
        document.getElementById('exportarModalMunicipal').addEventListener('hidden.bs.modal', function() {
            this.remove();
        });
        
    } catch (error) {
        console.error('Error mostrando opciones de exportación:', error);
        Utils.showError('Error al mostrar opciones de exportación');
    }
}

/**
 * ⭐ NUEVA FUNCIÓN: Exportar en formato específico
 */
async function exportarFormatoMunicipal(formato) {
    try {
        Utils.showInfo(`Generando archivo ${formato.toUpperCase()}...`);
        
        // Cerrar modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('exportarModalMunicipal'));
        if (modal) modal.hide();
        
        const url = `/api/coordinador-municipal/exportar?formato=${formato}`;
        const token = localStorage.getItem('access_token');
        
        // Descargar archivo
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            
            const fecha = new Date().toISOString().split('T')[0];
            const extension = formato === 'excel' ? 'xlsx' : formato;
            a.download = `consolidado_municipal_${fecha}.${extension}`;
            
            document.body.appendChild(a);
            a.click();
            a.remove();
            
            Utils.showSuccess(`✅ Archivo ${formato.toUpperCase()} descargado exitosamente`);
        } else {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Error al exportar datos');
        }
    } catch (error) {
        console.error('Error exporting data:', error);
        Utils.showError('Error al exportar datos: ' + error.message);
    }
}

/**
 * Abrir modal de comparación
 */
function abrirComparacion() {
    Utils.showInfo('Funcionalidad de comparación en desarrollo');
}

/**
 * Logout
 */
function logout() {
    localStorage.removeItem('token');
    window.location.href = '/auth/login';
}
