/**
 * Dashboard del Coordinador Departamental
 */

let currentUser = null;
let departamento = null;
let municipiosData = [];
let consolidadoData = null;

document.addEventListener('DOMContentLoaded', function() {
    loadUserProfile();
    loadMunicipios();
    loadEstadisticas();
    
    // Auto-refresh cada 60 segundos
    setInterval(() => {
        loadMunicipios();
        loadEstadisticas();
    }, 60000);
});

/**
 * Cargar perfil del coordinador
 */
async function loadUserProfile() {
    try {
        const response = await APIClient.getProfile();
        if (response.success) {
            currentUser = response.data.user;
            departamento = response.data.ubicacion;
            
            if (departamento) {
                document.getElementById('departamentoNombre').textContent = 
                    departamento.departamento_nombre || departamento.nombre_completo;
            }
        }
    } catch (error) {
        console.error('Error loading profile:', error);
        Utils.showError('Error al cargar perfil');
    }
}

/**
 * Cargar lista de municipios
 */
async function loadMunicipios() {
    try {
        const response = await APIClient.get('/coordinador-departamental/municipios');
        
        if (response.success) {
            municipiosData = response.data || [];
            renderMunicipiosTable(municipiosData);
            actualizarBadgesMunicipios();
        } else {
            throw new Error(response.error || 'Error al cargar municipios');
        }
    } catch (error) {
        console.error('Error loading municipios:', error);
        const tbody = document.querySelector('#municipiosTable tbody');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center py-4">
                        <p class="text-danger mb-2">❌ Error al cargar municipios</p>
                        <button class="btn btn-sm btn-outline-primary" onclick="loadMunicipios()">
                            <i class="bi bi-arrow-clockwise"></i> Reintentar
                        </button>
                    </td>
                </tr>
            `;
        }
    }
}

/**
 * Determinar estado de un municipio según su porcentaje de avance
 */
function getMunicipioEstado(porcentaje) {
    if (porcentaje >= 90) return 'completo';
    if (porcentaje > 0) return 'incompleto';
    return 'sin_datos';
}

/**
 * Actualizar badges de filtros con conteos reales
 */
function actualizarBadgesMunicipios() {
    if (!municipiosData || municipiosData.length === 0) return;
    
    const completos = municipiosData.filter(m => getMunicipioEstado(m.porcentaje_avance || 0) === 'completo').length;
    const incompletos = municipiosData.filter(m => getMunicipioEstado(m.porcentaje_avance || 0) === 'incompleto').length;
    
    const updateBadge = (id, value) => {
        const element = document.getElementById(id);
        if (element) element.textContent = value;
    };
    
    updateBadge('badgeTodos', municipiosData.length);
    updateBadge('badgeCompletos', completos);
    updateBadge('badgeIncompletos', incompletos);
}

/**
 * Filtrar municipios según estado
 */
function filtrarMunicipios(filtro) {
    let filtrados = municipiosData;
    
    if (filtro) {
        filtrados = municipiosData.filter(m => {
            const estado = getMunicipioEstado(m.porcentaje_avance || 0);
            if (filtro === 'completo') return estado === 'completo';
            if (filtro === 'incompleto') return estado === 'incompleto';
            if (filtro === 'con_discrepancias') return false; // Sin datos de discrepancias por ahora
            return true;
        });
    }
    
    renderMunicipiosTable(filtrados);
    
    // Sincronizar tarjetas móviles
    if (window.departamentalMejoras && window.departamentalMejoras.renderMunicipiosMobile) {
        window.departamentalMejoras.renderMunicipiosMobile(filtrados);
    }
}

/**
 * Buscar municipios por texto
 */
function buscarMunicipio() {
    const input = document.getElementById('searchMunicipio');
    const termino = (input ? input.value : '').toLowerCase().trim();
    
    const filtrados = municipiosData.filter(m => {
        const nombre = (m.nombre || m.nombre_completo || '').toLowerCase();
        const codigo = (m.municipio_codigo || '').toLowerCase();
        return !termino || nombre.includes(termino) || codigo.includes(termino);
    });
    
    renderMunicipiosTable(filtrados);
    
    if (window.departamentalMejoras && window.departamentalMejoras.renderMunicipiosMobile) {
        window.departamentalMejoras.renderMunicipiosMobile(filtrados);
    }
}

/**
 * Renderizar tabla de municipios
 */
function renderMunicipiosTable(municipios) {
    const tbody = document.querySelector('#municipiosTable tbody');
    
    if (municipios.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center py-4">
                    <p class="text-muted">No hay municipios en este departamento</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = municipios.map(municipio => {
        const porcentaje = municipio.porcentaje_avance || 0;
        const progressColor = porcentaje >= 90 ? 'success' : porcentaje >= 50 ? 'warning' : 'danger';
        const estadoBadge = getEstadoBadge(porcentaje);
        
        return `
            <tr>
                <td>
                    <strong>${municipio.nombre}</strong><br>
                    <small class="text-muted">Código: ${municipio.municipio_codigo}</small>
                </td>
                <td class="text-center">
                    <span class="badge bg-primary">${municipio.total_puestos}</span>
                </td>
                <td class="text-center">
                    <span class="badge bg-info">${municipio.total_mesas}</span>
                </td>
                <td class="text-center">
                    <strong>${municipio.formularios_completados}</strong> / ${municipio.total_formularios}
                </td>
                <td>
                    <div class="progress" style="height: 25px;">
                        <div class="progress-bar bg-${progressColor}" role="progressbar" 
                             style="width: ${porcentaje}%;" 
                             aria-valuenow="${porcentaje}" aria-valuemin="0" aria-valuemax="100">
                            ${porcentaje.toFixed(1)}%
                        </div>
                    </div>
                </td>
                <td>${estadoBadge}</td>
            </tr>
        `;
    }).join('');
}

/**
 * Obtener badge de estado según porcentaje
 */
function getEstadoBadge(porcentaje) {
    if (porcentaje >= 90) {
        return '<span class="badge bg-success">Completo</span>';
    } else if (porcentaje >= 50) {
        return '<span class="badge bg-warning">En Progreso</span>';
    } else if (porcentaje > 0) {
        return '<span class="badge bg-danger">Incompleto</span>';
    } else {
        return '<span class="badge bg-secondary">Sin Reportes</span>';
    }
}

/**
 * Cargar estadísticas departamentales
 * Actualiza las tarjetas de resumen y el panel de análisis
 */
async function loadEstadisticas() {
    try {
        // 1. Estadísticas generales para las tarjetas (statMunicipios, statPuestos, statFormularios, statParticipacion)
        const statsResponse = await APIClient.get('/coordinador-departamental/stats');
        if (statsResponse.success) {
            const stats = statsResponse.data;
            const updateElement = (id, value) => {
                const element = document.getElementById(id);
                if (element) element.textContent = value;
            };
            
            updateElement('statMunicipios', Utils.formatNumber(stats.total_municipios || 0));
            updateElement('statPuestos', Utils.formatNumber(stats.total_puestos || 0));
            updateElement('statFormularios', Utils.formatNumber(stats.total_formularios || 0));
            updateElement('statParticipacion', (stats.porcentaje_avance || 0).toFixed(1) + '%');
        }
        
        // 2. Estadísticas detalladas para el panel de Análisis
        const detalleResponse = await APIClient.get('/coordinador-departamental/estadisticas');
        if (detalleResponse.success) {
            renderEstadisticasGenerales(detalleResponse.data);
        }
    } catch (error) {
        console.error('Error loading estadisticas:', error);
        Utils.showError('Error al cargar estadísticas');
    }
}

/**
 * Renderizar panel de estadísticas detalladas en el tab de Análisis
 */
function renderEstadisticasGenerales(estadisticas) {
    const container = document.getElementById('estadisticasGenerales');
    if (!container) return;
    
    const estados = estadisticas.estados || {};
    let html = `
        <div class="mb-3">
            <p class="mb-1"><strong>Mesas totales:</strong> ${estadisticas.total_mesas || 0}</p>
            <p class="mb-1"><strong>Formularios recibidos:</strong> ${estadisticas.total_formularios || 0}</p>
            <p class="mb-1"><strong>Completado:</strong> ${(estadisticas.porcentaje_completado || 0).toFixed(1)}%</p>
            <p class="mb-0"><strong>Validado:</strong> ${(estadisticas.porcentaje_validado || 0).toFixed(1)}%</p>
        </div>
        <hr>
        <h6 class="mb-2">Estado de formularios</h6>
        <div class="d-flex justify-content-between mb-1">
            <span><span class="badge bg-warning">Pendientes</span></span>
            <strong>${estados.pendiente || 0}</strong>
        </div>
        <div class="d-flex justify-content-between mb-1">
            <span><span class="badge bg-success">Validados</span></span>
            <strong>${estados.validado || 0}</strong>
        </div>
        <div class="d-flex justify-content-between mb-1">
            <span><span class="badge bg-danger">Rechazados</span></span>
            <strong>${estados.rechazado || 0}</strong>
        </div>
        <div class="d-flex justify-content-between">
            <span><span class="badge bg-secondary">Sin reporte</span></span>
            <strong>${estados.sin_reporte || 0}</strong>
        </div>
    `;
    
    // Tabla de avance por municipio
    const porMunicipio = estadisticas.estadisticas_por_municipio || [];
    if (porMunicipio.length > 0) {
        html += '<hr><h6 class="mb-2">Avance por municipio</h6>';
        html += '<div class="table-responsive"><table class="table table-sm">';
        html += '<thead class="table-light"><tr><th>Municipio</th><th>Mesas</th><th>Recibidos</th><th>Validados</th><th>Avance</th></tr></thead>';
        html += '<tbody>';
        
        porMunicipio.forEach(stat => {
            const progressColor = stat.porcentaje_avance >= 90 ? 'success' : stat.porcentaje_avance >= 50 ? 'warning' : 'danger';
            html += `
                <tr>
                    <td><strong>${stat.municipio}</strong></td>
                    <td>${stat.total_mesas}</td>
                    <td>${stat.formularios_recibidos}</td>
                    <td>${stat.formularios_validados}</td>
                    <td>
                        <div class="progress" style="height: 20px;">
                            <div class="progress-bar bg-${progressColor}" style="width: ${stat.porcentaje_avance}%;">
                                ${stat.porcentaje_avance.toFixed(1)}%
                            </div>
                        </div>
                    </td>
                </tr>
            `;
        });
        
        html += '</tbody></table></div>';
    }
    
    container.innerHTML = html;
}

/**
 * Cargar consolidado departamental
 */
async function loadConsolidado() {
    try {
        const response = await APIClient.get('/coordinador-departamental/consolidado');
        
        if (response.success) {
            consolidadoData = response.data;
            renderConsolidado(consolidadoData);
        } else {
            throw new Error(response.error || 'Error al cargar consolidado');
        }
    } catch (error) {
        console.error('Error loading consolidado:', error);
        document.getElementById('resumenDepartamental').innerHTML = `
            <div class="text-center py-3">
                <p class="text-danger mb-2">❌ Error al cargar consolidado</p>
                <button class="btn btn-sm btn-outline-primary" onclick="loadConsolidado()">
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
    const container = document.getElementById('resumenDepartamental');
    
    if (!data || !data.votos_por_partido || data.votos_por_partido.length === 0) {
        container.innerHTML = '<p class="text-muted">No hay datos consolidados aún</p>';
        return;
    }
    
    let html = `
        <div class="mb-3">
            <h5>Resumen Departamental</h5>
            <p><strong>Total Formularios Validados:</strong> ${Utils.formatNumber(data.total_formularios)}</p>
            <p><strong>Total Votos:</strong> ${Utils.formatNumber(data.total_votos)}</p>
            <p><strong>Votantes Registrados:</strong> ${Utils.formatNumber(data.total_votantes_registrados)}</p>
            <p><strong>Participación:</strong> ${data.porcentaje_participacion.toFixed(2)}%</p>
        </div>
        <hr>
        <h6 class="mb-3">Votos por Partido</h6>
    `;
    
    data.votos_por_partido.forEach(partido => {
        html += `
            <div class="mb-3">
                <div class="d-flex justify-content-between align-items-center mb-1">
                    <div>
                        <span style="display: inline-block; width: 12px; height: 12px; background-color: ${partido.partido_color}; border-radius: 2px; margin-right: 8px;"></span>
                        <strong>${partido.partido_nombre}</strong>
                    </div>
                    <strong>${Utils.formatNumber(partido.total_votos)} votos</strong>
                </div>
                <div class="progress" style="height: 25px;">
                    <div class="progress-bar" role="progressbar" 
                         style="width: ${partido.porcentaje}%; background-color: ${partido.partido_color};"
                         aria-valuenow="${partido.porcentaje}" aria-valuemin="0" aria-valuemax="100">
                        ${partido.porcentaje.toFixed(2)}%
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

/**
 * Actualizar datos
 */
function actualizarDatos() {
    loadMunicipios();
    loadEstadisticas();
    Utils.showSuccess('Datos actualizados');
}

/**
 * ⭐ IMPLEMENTADO: Exportar datos departamentales
 */
async function exportarDatos() {
    try {
        // Mostrar modal de opciones de exportación
        const modalHtml = `
            <div class="modal fade" id="exportarModalDepartamental" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="bi bi-download"></i> Exportar Datos Departamentales
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p>Seleccione el formato de exportación:</p>
                            <div class="d-grid gap-2">
                                <button class="btn btn-outline-success" onclick="exportarFormatoDepartamental('csv')">
                                    <i class="bi bi-filetype-csv"></i> Exportar como CSV
                                </button>
                                <button class="btn btn-outline-primary" onclick="exportarFormatoDepartamental('excel')">
                                    <i class="bi bi-file-earmark-excel"></i> Exportar como Excel
                                </button>
                                <button class="btn btn-outline-danger" onclick="exportarFormatoDepartamental('pdf')">
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
        const modal = new bootstrap.Modal(document.getElementById('exportarModalDepartamental'));
        modal.show();
        
        // Limpiar modal al cerrar
        document.getElementById('exportarModalDepartamental').addEventListener('hidden.bs.modal', function() {
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
async function exportarFormatoDepartamental(formato) {
    try {
        Utils.showInfo(`Generando archivo ${formato.toUpperCase()}...`);
        
        // Cerrar modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('exportarModalDepartamental'));
        if (modal) modal.hide();
        
        const url = `/api/coordinador-departamental/exportar?formato=${formato}`;
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
            a.download = `consolidado_departamental_${fecha}.${extension}`;
            
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
 * ⭐ IMPLEMENTADO: Generar reporte departamental E-24
 */
async function generarReporte() {
    try {
        Utils.showInfo('Generando reporte E-24 departamental...');
        
        const url = '/api/coordinador-departamental/generar-e24';
        const token = localStorage.getItem('access_token');
        
        // Llamar al endpoint
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            
            const fecha = new Date().toISOString().split('T')[0];
            a.download = `E24_Departamental_${fecha}.pdf`;
            
            document.body.appendChild(a);
            a.click();
            a.remove();
            
            Utils.showSuccess('✅ Reporte E-24 generado y descargado exitosamente');
        } else {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Error al generar reporte');
        }
    } catch (error) {
        console.error('Error generando reporte:', error);
        Utils.showError('Error al generar reporte: ' + error.message);
    }
}

/**
 * Función global para logout
 */
async function logout() {
    try {
        await APIClient.logout();
    } catch (error) {
        console.error('Error during logout:', error);
    } finally {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_data');
        window.location.href = '/auth/login';
    }
}

// Event listener para cargar consolidado al cambiar de pestaña
document.addEventListener('DOMContentLoaded', function() {
    const consolidadoTab = document.getElementById('consolidado-tab');
    if (consolidadoTab) {
        consolidadoTab.addEventListener('shown.bs.tab', function() {
            loadConsolidado();
        });
    }
});
