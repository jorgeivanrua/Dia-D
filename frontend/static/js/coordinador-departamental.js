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
        } else {
            throw new Error(response.error || 'Error al cargar municipios');
        }
    } catch (error) {
        console.error('Error loading municipios:', error);
        const tbody = document.querySelector('#municipiosTable tbody');
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
 */
async function loadEstadisticas() {
    try {
        const response = await APIClient.get('/coordinador-departamental/estadisticas');
        
        if (response.success) {
            const stats = response.data;
            
            // Actualizar estadísticas generales
            document.getElementById('statTotalMesas').textContent = Utils.formatNumber(stats.total_mesas);
            document.getElementById('statFormulariosRecibidos').textContent = Utils.formatNumber(stats.total_formularios);
            document.getElementById('statFormulariosValidados').textContent = Utils.formatNumber(stats.estados.validado);
            document.getElementById('statPorcentajeCompletado').textContent = stats.porcentaje_completado.toFixed(1) + '%';
            
            // Actualizar estadísticas por estado
            document.getElementById('statPendientes').textContent = stats.estados.pendiente || 0;
            document.getElementById('statValidados').textContent = stats.estados.validado || 0;
            document.getElementById('statRechazados').textContent = stats.estados.rechazado || 0;
            document.getElementById('statSinReporte').textContent = stats.estados.sin_reporte || 0;
            
            // Renderizar tabla de municipios con estadísticas
            if (stats.estadisticas_por_municipio) {
                renderEstadisticasMunicipios(stats.estadisticas_por_municipio);
            }
        } else {
            throw new Error(response.error || 'Error al cargar estadísticas');
        }
    } catch (error) {
        console.error('Error loading estadisticas:', error);
        Utils.showError('Error al cargar estadísticas');
    }
}

/**
 * Renderizar estadísticas por municipio
 */
function renderEstadisticasMunicipios(estadisticas) {
    const container = document.getElementById('estadisticasMunicipios');
    
    if (!container) return;
    
    let html = '<div class="table-responsive"><table class="table table-sm">';
    html += '<thead class="table-light"><tr><th>Municipio</th><th>Mesas</th><th>Recibidos</th><th>Validados</th><th>Avance</th></tr></thead>';
    html += '<tbody>';
    
    estadisticas.forEach(stat => {
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
        document.getElementById('consolidadoPanel').innerHTML = `
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
    const container = document.getElementById('consolidadoPanel');
    
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
