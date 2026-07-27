/**
 * Dashboard Mejorado del Coordinador Municipal
 * Versión optimizada con todas las funcionalidades
 */

// Estado global
let currentUser = null;
let userLocation = null;
let puestos = [];
let puestosOriginales = [];
let filtroEstadoActual = '';
let autoRefreshInterval = null;
let mapaGeolocalizacion = null;

// Inicialización
document.addEventListener('DOMContentLoaded', async function() {
    try {
        console.log('[Coordinador Municipal Mejorado] Inicializando...');
        
        await loadUserProfile();
        await loadEstadisticas();
        await loadPuestos();
        await loadConsolidado();
        await loadDiscrepancias();
        
        // Inicializar sincronización de pestañas con bottom nav
        initBottomNavSync();
        
        // Inicializar pestañas cuando se activen
        const mapaTab = document.getElementById('mapa-tab');
        if (mapaTab) {
            mapaTab.addEventListener('shown.bs.tab', function() {
                if (!mapaGeolocalizacion) {
                    initMapa();
                }
            });
        }
        
        const incidentesTab = document.getElementById('incidentes-tab');
        if (incidentesTab) {
            incidentesTab.addEventListener('shown.bs.tab', function() {
                cargarIncidentes();
            });
        }
        
        const delitosTab = document.getElementById('delitos-tab');
        if (delitosTab) {
            delitosTab.addEventListener('shown.bs.tab', function() {
                cargarDelitos();
            });
        }
        
        const equipoTab = document.getElementById('equipo-tab');
        if (equipoTab) {
            equipoTab.addEventListener('shown.bs.tab', function() {
                actualizarEstadoCoordinadores();
            });
        }
        
        const e24Tab = document.getElementById('e24-tab');
        if (e24Tab) {
            e24Tab.addEventListener('shown.bs.tab', function() {
                cargarDatosE24();
            });
        }
        
        console.log('[Coordinador Municipal Mejorado] Inicializado correctamente');
        
        // Auto-refresh cada 60 segundos
        autoRefreshInterval = setInterval(() => {
            loadEstadisticas();
            loadPuestos();
            loadConsolidado();
            loadDiscrepancias();
        }, 60000);
        
    } catch (error) {
        console.error('[Coordinador Municipal Mejorado] Error:', error);
        Utils.showError('Error al inicializar el dashboard');
    }
});

// Limpiar al salir
window.addEventListener('beforeunload', function() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
});

/**
 * Inicializar sincronización entre bottom nav y pestañas principales
 */
function initBottomNavSync() {
    // Sincronizar bottom nav con pestañas principales
    const bottomNavItems = document.querySelectorAll('.bottom-nav-item');
    
    bottomNavItems.forEach(item => {
        item.addEventListener('shown.bs.tab', function(e) {
            // Actualizar estado activo en bottom nav
            bottomNavItems.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Sincronizar pestañas principales con bottom nav
    const mainTabs = document.querySelectorAll('#dashboardTabs button[data-bs-toggle="tab"]');
    
    mainTabs.forEach(tab => {
        tab.addEventListener('shown.bs.tab', function(e) {
            const target = this.getAttribute('data-bs-target');
            
            // Actualizar bottom nav correspondiente
            bottomNavItems.forEach(btn => {
                if (btn.getAttribute('data-bs-target') === target) {
                    bottomNavItems.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                }
            });
        });
    });
}

/**
 * Actualizar badges de incidentes y delitos en móvil
 */
function actualizarBadgesMobile(incidentes, delitos) {
    const badgeIncidentesMobile = document.getElementById('badge-incidentes-mobile');
    const badgeDelitosMobile = document.getElementById('badge-delitos-mobile');
    
    if (badgeIncidentesMobile) {
        badgeIncidentesMobile.textContent = incidentes || 0;
    }
    
    if (badgeDelitosMobile) {
        badgeDelitosMobile.textContent = delitos || 0;
    }
}

/**
 * Cargar perfil del usuario
 */
async function loadUserProfile() {
    try {
        const response = await APIClient.get('/auth/profile');
        
        if (response && response.success) {
            currentUser = response.data.user;
            userLocation = response.data.ubicacion;
            
            // Mostrar información del municipio
            const municipioInfo = document.getElementById('municipioInfo');
            if (municipioInfo && userLocation) {
                municipioInfo.textContent = 
                    `${userLocation.municipio_nombre || userLocation.nombre_completo} - ${userLocation.departamento_nombre || ''}`;
            }
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

/**
 * Cargar estadísticas generales
 */
async function loadEstadisticas() {
    try {
        const response = await APIClient.get('/coordinador-municipal/estadisticas');
        
        if (response.success) {
            const stats = response.data;
            updateEstadisticasCards(stats.resumen_general);
        }
    } catch (error) {
        console.error('Error loading estadisticas:', error);
    }
}

/**
 * Actualizar cards de estadísticas
 */
function updateEstadisticasCards(resumen) {
    const pendientes = resumen.puestos_incompletos || 0;
    const completos = resumen.puestos_completos || 0;
    const discrepancias = resumen.puestos_con_discrepancias || 0;
    const total = resumen.total_puestos || 0;
    const progreso = resumen.porcentaje_avance || 0;
    
    // Actualizar valores
    document.getElementById('statPendientes').textContent = pendientes;
    document.getElementById('statValidados').textContent = completos;
    document.getElementById('statRechazados').textContent = discrepancias;
    document.getElementById('statProgreso').textContent = `${progreso.toFixed(0)}%`;
    document.getElementById('statPuestos').textContent = `${completos} de ${total} puestos`;
    
    // Actualizar badges de filtros
    document.getElementById('badgeTodos').textContent = total;
    document.getElementById('badgeCompletos').textContent = completos;
    document.getElementById('badgeIncompletos').textContent = pendientes;
    document.getElementById('badgeDiscrepancias').textContent = discrepancias;
}

/**
 * Cargar lista de puestos
 */
async function loadPuestos() {
    try {
        const params = {};
        if (filtroEstadoActual) {
            params.estado = filtroEstadoActual;
        }
        
        const response = await APIClient.get('/coordinador-municipal/puestos', params);
        
        if (response.success) {
            puestosOriginales = response.data.puestos || [];
            puestos = [...puestosOriginales];
            
            renderPuestosTable(puestos);
            renderPuestosCards(puestos);
        }
    } catch (error) {
        console.error('Error loading puestos:', error);
        showErrorInTable('Error al cargar puestos');
    }
}

/**
 * Renderizar tabla de puestos (desktop) - Agrupados por zona
 */
function renderPuestosTable(puestos) {
    const tbody = document.querySelector('#puestosTable tbody');
    
    if (!tbody) return;
    
    if (puestos.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center py-4">
                    <p class="text-muted">No hay puestos para mostrar</p>
                </td>
            </tr>
        `;
        return;
    }
    
    // Agrupar puestos por zona
    const puestosPorZona = {};
    puestos.forEach(puesto => {
        const zona = puesto.zona_codigo || 'Sin Zona';
        if (!puestosPorZona[zona]) {
            puestosPorZona[zona] = [];
        }
        puestosPorZona[zona].push(puesto);
    });
    
    // Ordenar zonas
    const zonasOrdenadas = Object.keys(puestosPorZona).sort();
    
    // Renderizar tabla agrupada por zona
    let html = '';
    
    zonasOrdenadas.forEach(zona => {
        const puestosZona = puestosPorZona[zona];
        const totalPuestos = puestosZona.length;
        const completados = puestosZona.filter(p => p.estado === 'completo').length;
        const porcentajeZona = (completados / totalPuestos * 100).toFixed(0);
        
        // Fila de encabezado de zona con color
        const zonaColor = getZonaColor(zona);
        html += `
            <tr style="background-color: ${zonaColor.bg}; border-left: 4px solid ${zonaColor.border};">
                <td colspan="6">
                    <strong style="color: ${zonaColor.text};">
                        <i class="bi bi-geo-alt-fill"></i> ZONA ${zona}
                    </strong>
                    <span class="ms-2 badge bg-primary">${totalPuestos} puestos</span>
                    <span class="ms-1 badge bg-success">${completados} completos</span>
                    <span class="ms-1 badge bg-info">${porcentajeZona}% avance</span>
                </td>
            </tr>
        `;
        
        // Filas de puestos de la zona
        puestosZona.forEach(puesto => {
            const estadoBadge = getEstadoBadge(puesto.estado);
            const porcentaje = puesto.porcentaje_avance || 0;
            const coordinador = puesto.coordinador?.nombre || 'Sin asignar';
            const discrepancia = puesto.tiene_discrepancias ? 
                '<i class="bi bi-exclamation-triangle text-danger ms-1"></i>' : '';
            
            html += `
                <tr class="puesto-row" onclick="verDetallePuesto(${puesto.id})">
                    <td>
                        <strong>${puesto.codigo}</strong>${discrepancia}<br>
                        <small class="text-muted">${puesto.nombre}</small>
                    </td>
                    <td><small>${coordinador}</small></td>
                    <td class="text-center"><span class="badge bg-secondary">${puesto.zona_codigo || 'N/A'}</span></td>
                    <td class="text-center">
                        <div class="progress" style="height: 20px; min-width: 80px;">
                            <div class="progress-bar ${porcentaje >= 100 ? 'bg-success' : 'bg-primary'}" 
                                 style="width: ${porcentaje}%">
                                ${porcentaje.toFixed(0)}%
                            </div>
                        </div>
                        <small class="text-muted">${puesto.mesas_reportadas}/${puesto.total_mesas}</small>
                    </td>
                    <td class="text-center">${estadoBadge}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary" onclick="event.stopPropagation(); verDetallePuesto(${puesto.id})">
                            <i class="bi bi-eye"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
    });
    
    tbody.innerHTML = html;
}

/**
 * Renderizar cards de puestos (móvil) - Agrupados por zona
 */
function renderPuestosCards(puestos) {
    const container = document.getElementById('puestosCards');
    
    if (!container) return;
    
    if (puestos.length === 0) {
        container.innerHTML = '<p class="text-muted text-center py-4">No hay puestos para mostrar</p>';
        return;
    }
    
    // Agrupar puestos por zona
    const puestosPorZona = {};
    puestos.forEach(puesto => {
        const zona = puesto.zona_codigo || 'Sin Zona';
        if (!puestosPorZona[zona]) {
            puestosPorZona[zona] = [];
        }
        puestosPorZona[zona].push(puesto);
    });
    
    // Ordenar zonas
    const zonasOrdenadas = Object.keys(puestosPorZona).sort();
    
    // Renderizar cards agrupados por zona
    let html = '';
    
    zonasOrdenadas.forEach(zona => {
        const puestosZona = puestosPorZona[zona];
        const totalPuestos = puestosZona.length;
        const completados = puestosZona.filter(p => p.estado === 'completo').length;
        const porcentajeZona = (completados / totalPuestos * 100).toFixed(0);
        
        // Encabezado de zona con color
        const zonaColor = getZonaColor(zona);
        html += `
            <div class="card mb-2" style="background-color: ${zonaColor.bg}; border-left: 4px solid ${zonaColor.border};">
                <div class="card-body py-2">
                    <div class="d-flex justify-content-between align-items-center">
                        <strong style="color: ${zonaColor.text};">
                            <i class="bi bi-geo-alt-fill"></i> ZONA ${zona}
                        </strong>
                        <div>
                            <span class="badge bg-primary">${totalPuestos}</span>
                            <span class="badge bg-success ms-1">${completados}</span>
                            <span class="badge bg-info ms-1">${porcentajeZona}%</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Cards de puestos de la zona
        puestosZona.forEach(puesto => {
            const estadoBadge = getEstadoBadge(puesto.estado);
            const porcentaje = puesto.porcentaje_avance || 0;
            const coordinador = puesto.coordinador?.nombre || 'Sin asignar';
            
            html += `
                <div class="card mb-2" onclick="verDetallePuesto(${puesto.id})">
                    <div class="card-body py-2">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <div>
                                <h6 class="mb-0">${puesto.codigo}</h6>
                                <small class="text-muted">${puesto.nombre}</small>
                            </div>
                            ${estadoBadge}
                        </div>
                        <div class="mb-2">
                            <small class="text-muted">Coordinador:</small>
                            <div><small>${coordinador}</small></div>
                        </div>
                        <div class="mb-1">
                            <small class="text-muted">Avance:</small>
                            <div class="progress mt-1" style="height: 16px;">
                                <div class="progress-bar ${porcentaje >= 100 ? 'bg-success' : 'bg-primary'}" 
                                     style="width: ${porcentaje}%">
                                    ${porcentaje.toFixed(0)}%
                                </div>
                            </div>
                            <small class="text-muted">${puesto.mesas_reportadas}/${puesto.total_mesas} mesas</small>
                        </div>
                    </div>
                </div>
            `;
        });
    });
    
    container.innerHTML = html;
}

/**
 * Obtener badge de estado
 */
function getEstadoBadge(estado) {
    const badges = {
        'completo': '<span class="badge bg-success">Completo</span>',
        'incompleto': '<span class="badge bg-warning text-dark">Incompleto</span>',
        'con_discrepancias': '<span class="badge bg-danger">Con Discrepancias</span>'
    };
    return badges[estado] || `<span class="badge bg-secondary">${estado}</span>`;
}

/**
 * Obtener color para una zona
 */
function getZonaColor(zona) {
    const colores = {
        '01': { bg: '#e3f2fd', border: '#2196f3', text: '#1565c0' },
        '02': { bg: '#f3e5f5', border: '#9c27b0', text: '#6a1b9a' },
        '03': { bg: '#e8f5e9', border: '#4caf50', text: '#2e7d32' },
        '04': { bg: '#fff3e0', border: '#ff9800', text: '#e65100' },
        '05': { bg: '#fce4ec', border: '#e91e63', text: '#c2185b' },
        '06': { bg: '#e0f2f1', border: '#009688', text: '#00695c' },
        '07': { bg: '#fff9c4', border: '#fbc02d', text: '#f57f17' },
        '08': { bg: '#f1f8e9', border: '#8bc34a', text: '#558b2f' },
        '09': { bg: '#ede7f6', border: '#673ab7', text: '#4527a0' },
        '10': { bg: '#e1f5fe', border: '#03a9f4', text: '#0277bd' }
    };
    
    return colores[zona] || { bg: '#f5f5f5', border: '#9e9e9e', text: '#424242' };
}

/**
 * Filtrar puestos por estado
 */
function filtrarPorEstado(estado) {
    filtroEstadoActual = estado;
    
    // Actualizar chips activos
    document.querySelectorAll('.filter-chips .chip').forEach(chip => {
        chip.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Recargar puestos
    loadPuestos();
}

/**
 * Buscar puestos
 */
function buscarPuestos(query) {
    query = query.toLowerCase().trim();
    
    if (!query) {
        puestos = [...puestosOriginales];
    } else {
        puestos = puestosOriginales.filter(p => 
            p.codigo.toLowerCase().includes(query) || 
            p.nombre.toLowerCase().includes(query)
        );
    }
    
    renderPuestosTable(puestos);
    renderPuestosCards(puestos);
}

/**
 * Ver detalle de puesto
 */
async function verDetallePuesto(puestoId) {
    try {
        const response = await APIClient.get(`/coordinador-municipal/puesto/${puestoId}`);
        
        if (response.success) {
            mostrarModalDetallePuesto(response.data);
        }
    } catch (error) {
        console.error('Error loading puesto details:', error);
        Utils.showError('Error al cargar detalles del puesto');
    }
}

/**
 * Mostrar modal con detalle del puesto
 */
function mostrarModalDetallePuesto(data) {
    const modal = new bootstrap.Modal(document.getElementById('detallePuestoModal'));
    const content = document.getElementById('detallePuestoContent');
    
    const puesto = data.puesto || {};
    const coordinador = data.coordinador || {};
    const estadisticas = data.estadisticas || {};
    const mesas = data.mesas || [];
    const zonaColor = getZonaColor(puesto.zona_codigo);
    
    content.innerHTML = `
        <!-- Encabezado con color de zona -->
        <div class="alert mb-3" style="background-color: ${zonaColor.bg}; border-left: 4px solid ${zonaColor.border};">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h5 class="mb-0" style="color: ${zonaColor.text};">
                        <i class="bi bi-geo-alt-fill"></i> ZONA ${puesto.zona_codigo || 'N/A'}
                    </h5>
                    <strong>${puesto.nombre}</strong>
                    <br><small class="text-muted">Código: ${puesto.codigo}</small>
                </div>
                <div class="text-end">
                    <div class="progress" style="width: 100px; height: 24px;">
                        <div class="progress-bar ${estadisticas.porcentaje_avance >= 100 ? 'bg-success' : 'bg-primary'}" 
                             style="width: ${estadisticas.porcentaje_avance}%">
                            ${estadisticas.porcentaje_avance.toFixed(0)}%
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Estadísticas principales -->
        <div class="row mb-3">
            <div class="col-6 col-md-3 mb-2">
                <div class="card bg-success bg-opacity-10 border-success">
                    <div class="card-body text-center py-2">
                        <small class="text-muted d-block">Validados</small>
                        <h4 class="text-success mb-0">${estadisticas.formularios_validados || 0}</h4>
                    </div>
                </div>
            </div>
            <div class="col-6 col-md-3 mb-2">
                <div class="card bg-warning bg-opacity-10 border-warning">
                    <div class="card-body text-center py-2">
                        <small class="text-muted d-block">Pendientes</small>
                        <h4 class="text-warning mb-0">${estadisticas.formularios_pendientes || 0}</h4>
                    </div>
                </div>
            </div>
            <div class="col-6 col-md-3 mb-2">
                <div class="card bg-danger bg-opacity-10 border-danger">
                    <div class="card-body text-center py-2">
                        <small class="text-muted d-block">Rechazados</small>
                        <h4 class="text-danger mb-0">${estadisticas.formularios_rechazados || 0}</h4>
                    </div>
                </div>
            </div>
            <div class="col-6 col-md-3 mb-2">
                <div class="card bg-info bg-opacity-10 border-info">
                    <div class="card-body text-center py-2">
                        <small class="text-muted d-block">Total Mesas</small>
                        <h4 class="text-info mb-0">${puesto.total_mesas || 0}</h4>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Alertas -->
        ${estadisticas.incidentes > 0 || estadisticas.delitos > 0 ? `
        <div class="alert alert-warning py-2 mb-3">
            <strong><i class="bi bi-exclamation-triangle"></i> Alertas:</strong>
            ${estadisticas.incidentes > 0 ? `<span class="badge bg-warning text-dark ms-2">${estadisticas.incidentes} Incidentes</span>` : ''}
            ${estadisticas.delitos > 0 ? `<span class="badge bg-danger ms-2">${estadisticas.delitos} Delitos</span>` : ''}
        </div>
        ` : ''}
        
        <!-- Tabs de información -->
        <ul class="nav nav-tabs mb-3" role="tablist">
            <li class="nav-item">
                <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#tab-info">
                    <i class="bi bi-info-circle"></i> Info
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-mesas">
                    <i class="bi bi-table"></i> Mesas (${mesas.length})
                </button>
            </li>
            ${estadisticas.incidentes > 0 ? `
            <li class="nav-item">
                <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-incidentes">
                    <i class="bi bi-exclamation-triangle"></i> Incidentes (${estadisticas.incidentes})
                </button>
            </li>
            ` : ''}
            ${estadisticas.delitos > 0 ? `
            <li class="nav-item">
                <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-delitos">
                    <i class="bi bi-shield-exclamation"></i> Delitos (${estadisticas.delitos})
                </button>
            </li>
            ` : ''}
            <li class="nav-item">
                <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-coordinador">
                    <i class="bi bi-person"></i> Coordinador
                </button>
            </li>
        </ul>
        
        <div class="tab-content">
            <!-- Tab Info -->
            <div class="tab-pane fade show active" id="tab-info">
                <table class="table table-sm">
                    <tr>
                        <td width="40%"><strong>Código:</strong></td>
                        <td>${puesto.codigo}</td>
                    </tr>
                    <tr>
                        <td><strong>Nombre:</strong></td>
                        <td>${puesto.nombre}</td>
                    </tr>
                    <tr>
                        <td><strong>Zona:</strong></td>
                        <td><span class="badge" style="background-color: ${zonaColor.border};">${puesto.zona_codigo || 'N/A'}</span></td>
                    </tr>
                    ${puesto.direccion ? `
                    <tr>
                        <td><strong>Dirección:</strong></td>
                        <td>${puesto.direccion}</td>
                    </tr>
                    ` : ''}
                    <tr>
                        <td><strong>Total Mesas:</strong></td>
                        <td>${puesto.total_mesas}</td>
                    </tr>
                </table>
            </div>
            
            <!-- Tab Mesas -->
            <div class="tab-pane fade" id="tab-mesas">
                ${mesas.length > 0 ? `
                <div class="table-responsive">
                    <table class="table table-sm table-hover">
                        <thead>
                            <tr>
                                <th>Mesa</th>
                                <th>Votantes</th>
                                <th>Estado</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${mesas.map(mesa => `
                                <tr>
                                    <td><strong>${mesa.codigo}</strong></td>
                                    <td>${mesa.votantes || 0}</td>
                                    <td>${getEstadoBadge(mesa.estado)}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
                ${mesas.length >= 10 ? '<small class="text-muted">Mostrando primeras 10 mesas</small>' : ''}
                ` : '<p class="text-muted">No hay información de mesas</p>'}
            </div>
            
            <!-- Tab Incidentes -->
            ${estadisticas.incidentes > 0 ? `
            <div class="tab-pane fade" id="tab-incidentes">
                ${renderIncidentesList(data.incidentes || [])}
            </div>
            ` : ''}
            
            <!-- Tab Delitos -->
            ${estadisticas.delitos > 0 ? `
            <div class="tab-pane fade" id="tab-delitos">
                ${renderDelitosList(data.delitos || [])}
            </div>
            ` : ''}
            
            <!-- Tab Coordinador -->
            <div class="tab-pane fade" id="tab-coordinador">
                ${coordinador ? `
                <table class="table table-sm">
                    <tr>
                        <td width="40%"><strong>Nombre:</strong></td>
                        <td>${coordinador.nombre}</td>
                    </tr>
                    ${coordinador.ultimo_acceso ? `
                    <tr>
                        <td><strong>Último acceso:</strong></td>
                        <td>${Utils.formatDate(coordinador.ultimo_acceso)}</td>
                    </tr>
                    ` : ''}
                </table>
                ` : '<p class="text-muted">No hay coordinador asignado</p>'}
            </div>
        </div>
    `;
    
    modal.show();
}

/**
 * Renderizar lista de incidentes con evidencias
 */
function renderIncidentesList(incidentes) {
    if (!incidentes || incidentes.length === 0) {
        return '<p class="text-muted">No hay incidentes reportados</p>';
    }
    
    let html = '';
    
    incidentes.forEach(inc => {
        const severidadClass = {
            'baja': 'info',
            'media': 'warning',
            'alta': 'danger',
            'critica': 'danger'
        }[inc.severidad] || 'secondary';
        
        const estadoClass = {
            'reportado': 'warning',
            'en_revision': 'info',
            'resuelto': 'success',
            'escalado': 'danger'
        }[inc.estado] || 'secondary';
        
        html += `
            <div class="card mb-3">
                <div class="card-header d-flex justify-content-between align-items-center py-2">
                    <strong>${inc.titulo}</strong>
                    <div>
                        <span class="badge bg-${severidadClass}">${inc.severidad_label}</span>
                        <span class="badge bg-${estadoClass} ms-1">${inc.estado_label}</span>
                    </div>
                </div>
                <div class="card-body">
                    <p class="mb-2"><strong>Tipo:</strong> ${inc.tipo_incidente_label}</p>
                    <p class="mb-2"><strong>Descripción:</strong> ${inc.descripcion}</p>
                    <p class="mb-2"><small class="text-muted">
                        <i class="bi bi-person"></i> ${inc.reportado_por} | 
                        <i class="bi bi-calendar"></i> ${Utils.formatDate(inc.fecha_reporte)}
                    </small></p>
                    
                    ${inc.ubicacion_gps ? `
                    <p class="mb-2"><small><i class="bi bi-geo-alt"></i> ${inc.ubicacion_gps}</small></p>
                    ` : ''}
                    
                    ${inc.notas_resolucion ? `
                    <div class="alert alert-info py-2 mb-2">
                        <strong>Notas de resolución:</strong><br>
                        ${inc.notas_resolucion}
                    </div>
                    ` : ''}
                    
                    ${inc.evidencias && inc.evidencias.length > 0 ? `
                    <div class="mt-3">
                        <strong class="d-block mb-2">
                            <i class="bi bi-camera"></i> Evidencias (${inc.evidencias.length})
                        </strong>
                        <div class="row g-2">
                            ${inc.evidencias.map(ev => `
                                <div class="col-6 col-md-4">
                                    <a href="${ev.url}" target="_blank" class="d-block">
                                        <img src="${ev.url}" 
                                             class="img-fluid rounded border" 
                                             alt="${ev.filename}"
                                             style="max-height: 150px; width: 100%; object-fit: cover;">
                                    </a>
                                    <small class="text-muted d-block mt-1">${ev.filename}</small>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    ` : ''}
                </div>
            </div>
        `;
    });
    
    return html;
}

/**
 * Renderizar lista de delitos con evidencias
 */
function renderDelitosList(delitos) {
    if (!delitos || delitos.length === 0) {
        return '<p class="text-muted">No hay delitos reportados</p>';
    }
    
    let html = '';
    
    delitos.forEach(delito => {
        const gravedadClass = {
            'leve': 'info',
            'media': 'warning',
            'grave': 'danger',
            'muy_grave': 'danger'
        }[delito.gravedad] || 'secondary';
        
        const estadoClass = {
            'reportado': 'warning',
            'en_investigacion': 'info',
            'investigado': 'primary',
            'denunciado': 'success',
            'archivado': 'secondary'
        }[delito.estado] || 'secondary';
        
        html += `
            <div class="card mb-3 border-danger">
                <div class="card-header bg-danger bg-opacity-10 d-flex justify-content-between align-items-center py-2">
                    <strong>${delito.titulo}</strong>
                    <div>
                        <span class="badge bg-${gravedadClass}">${delito.gravedad_label}</span>
                        <span class="badge bg-${estadoClass} ms-1">${delito.estado_label}</span>
                    </div>
                </div>
                <div class="card-body">
                    <p class="mb-2"><strong>Tipo:</strong> ${delito.tipo_delito_label}</p>
                    <p class="mb-2"><strong>Descripción:</strong> ${delito.descripcion}</p>
                    <p class="mb-2"><small class="text-muted">
                        <i class="bi bi-person"></i> ${delito.reportado_por} | 
                        <i class="bi bi-calendar"></i> ${Utils.formatDate(delito.fecha_reporte)}
                    </small></p>
                    
                    ${delito.ubicacion_gps ? `
                    <p class="mb-2"><small><i class="bi bi-geo-alt"></i> ${delito.ubicacion_gps}</small></p>
                    ` : ''}
                    
                    ${delito.denunciado_formalmente ? `
                    <div class="alert alert-success py-2 mb-2">
                        <strong><i class="bi bi-check-circle"></i> Denunciado formalmente</strong><br>
                        ${delito.numero_denuncia ? `Número de denuncia: ${delito.numero_denuncia}` : ''}
                    </div>
                    ` : ''}
                    
                    ${delito.resultado_investigacion ? `
                    <div class="alert alert-info py-2 mb-2">
                        <strong>Resultado de investigación:</strong><br>
                        ${delito.resultado_investigacion}
                    </div>
                    ` : ''}
                    
                    ${delito.evidencias && delito.evidencias.length > 0 ? `
                    <div class="mt-3">
                        <strong class="d-block mb-2">
                            <i class="bi bi-camera"></i> Evidencias (${delito.evidencias.length})
                        </strong>
                        <div class="row g-2">
                            ${delito.evidencias.map(ev => `
                                <div class="col-6 col-md-4">
                                    <a href="${ev.url}" target="_blank" class="d-block">
                                        <img src="${ev.url}" 
                                             class="img-fluid rounded border" 
                                             alt="${ev.filename}"
                                             style="max-height: 150px; width: 100%; object-fit: cover;">
                                    </a>
                                    <small class="text-muted d-block mt-1">${ev.filename}</small>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    ` : ''}
                </div>
            </div>
        `;
    });
    
    return html;
}

/**
 * Cargar consolidado municipal
 */
async function loadConsolidado() {
    try {
        const response = await APIClient.get('/coordinador-municipal/consolidado');
        
        if (response.success) {
            renderConsolidadoPanel(response.data);
        }
    } catch (error) {
        console.error('Error loading consolidado:', error);
        document.getElementById('consolidadoPanel').innerHTML = 
            '<p class="text-danger">Error al cargar consolidado</p>';
    }
}

/**
 * Renderizar panel de consolidado
 */
function renderConsolidadoPanel(data) {
    const container = document.getElementById('consolidadoPanel');
    
    if (!data || !data.votos_por_partido || data.votos_por_partido.length === 0) {
        container.innerHTML = '<p class="text-muted">No hay datos consolidados</p>';
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
    
    data.votos_por_partido.slice(0, 5).forEach(partido => {
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
                    <div class="progress-bar" 
                         style="width: ${partido.porcentaje}%; background-color: ${partido.partido_color};">
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
            renderDiscrepanciasPanel(response.data);
        }
    } catch (error) {
        console.error('Error loading discrepancias:', error);
        document.getElementById('discrepanciasPanel').innerHTML = 
            '<p class="text-danger">Error al cargar alertas</p>';
    }
}

/**
 * Renderizar panel de discrepancias
 */
function renderDiscrepanciasPanel(discrepancias) {
    const container = document.getElementById('discrepanciasPanel');
    
    if (!discrepancias || discrepancias.length === 0) {
        container.innerHTML = `
            <div class="text-center py-3">
                <i class="bi bi-check-circle text-success" style="font-size: 2rem;"></i>
                <p class="text-muted mb-0 mt-2">No hay discrepancias</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    
    discrepancias.slice(0, 5).forEach(d => {
        const severidadClass = d.severidad === 'alta' ? 'danger' : 'warning';
        html += `
            <div class="alert alert-${severidadClass} py-2 px-2 mb-2" role="alert" 
                 style="cursor: pointer;" onclick="verDetallePuesto(${d.puesto_id})">
                <small>
                    <strong>${d.puesto_nombre}</strong><br>
                    ${d.descripcion}
                </small>
            </div>
        `;
    });
    
    if (discrepancias.length > 5) {
        html += `<small class="text-muted">Y ${discrepancias.length - 5} más...</small>`;
    }
    
    container.innerHTML = html;
}

/**
 * Exportar datos municipales
 */
async function exportarDatosMunicipal() {
    try {
        Utils.showInfo('Generando archivo CSV...');
        
        const url = '/api/coordinador-municipal/exportar?formato=csv';
        const token = localStorage.getItem('token');
        
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
            a.download = `consolidado_municipal_${fecha}.csv`;
            
            document.body.appendChild(a);
            a.click();
            a.remove();
            
            Utils.showSuccess('Archivo descargado exitosamente');
        } else {
            throw new Error('Error al exportar datos');
        }
    } catch (error) {
        console.error('Error exporting data:', error);
        Utils.showError('Error al exportar datos');
    }
}

/**
 * Generar PDF E-24 Municipal
 */
function generarPDFE24Municipal() {
    Utils.showInfo('Funcionalidad de generación de E-24 en desarrollo');
}

/**
 * Inicializar mapa de geolocalización
 */
function initMapa() {
    try {
        const container = document.getElementById('mapaGeolocalizacion');
        
        if (!container) return;
        
        // Inicializar mapa con Leaflet
        mapaGeolocalizacion = L.map('mapaGeolocalizacion').setView([1.6, -75.6], 10);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(mapaGeolocalizacion);
        
        // Cargar datos del mapa
        cargarDatosMapa();
        
    } catch (error) {
        console.error('Error initializing map:', error);
    }
}

/**
 * Cargar datos del mapa
 */
async function cargarDatosMapa() {
    try {
        const response = await APIClient.get('/coordinador-municipal/geolocalizacion');
        
        if (response.success) {
            const data = response.data;
            
            // Centrar mapa en el municipio
            if (data.centro) {
                mapaGeolocalizacion.setView([data.centro.latitud, data.centro.longitud], 12);
            }
            
            // Agregar markers de puestos con colores por zona
            if (data.puestos) {
                data.puestos.forEach(puesto => {
                    const zonaColor = getZonaColor(puesto.zona_codigo || '01');
                    
                    const icon = L.divIcon({
                        className: 'custom-marker',
                        html: `<div class="marker-pin" style="background-color: ${zonaColor.border};"><i class="bi bi-building"></i></div>`,
                        iconSize: [30, 42],
                        iconAnchor: [15, 42]
                    });
                    
                    const marker = L.marker([puesto.latitud, puesto.longitud], { icon: icon })
                        .addTo(mapaGeolocalizacion);
                    
                    const popupContent = `
                        <div class="p-2">
                            <div style="background-color: ${zonaColor.bg}; padding: 0.5rem; margin: -0.5rem -0.5rem 0.5rem -0.5rem; border-left: 4px solid ${zonaColor.border};">
                                <strong style="color: ${zonaColor.text};">
                                    <i class="bi bi-geo-alt-fill"></i> ZONA ${puesto.zona_codigo || 'N/A'}
                                </strong>
                            </div>
                            <h6 class="mt-2">${puesto.nombre}</h6>
                            <p class="mb-1"><strong>Código:</strong> ${puesto.codigo}</p>
                            <p class="mb-1"><strong>Mesas:</strong> ${puesto.total_mesas}</p>
                            <p class="mb-1"><strong>Validados:</strong> ${puesto.formularios_validados}</p>
                            <div class="progress mt-2" style="height: 20px;">
                                <div class="progress-bar ${puesto.porcentaje_avance >= 100 ? 'bg-success' : 'bg-primary'}" 
                                     style="width: ${puesto.porcentaje_avance}%">
                                    ${puesto.porcentaje_avance.toFixed(0)}%
                                </div>
                            </div>
                            ${puesto.direccion ? `<p class="mb-0 mt-2"><small>${puesto.direccion}</small></p>` : ''}
                        </div>
                    `;
                    
                    marker.bindPopup(popupContent);
                });
            }
            
            // Agregar markers de coordinadores
            if (data.coordinadores) {
                data.coordinadores.forEach(coord => {
                    const estadoClass = {
                        'activo': 'marker-activo',
                        'inactivo': 'marker-inactivo',
                        'ausente': 'marker-ausente'
                    }[coord.estado_conexion] || 'marker-ausente';
                    
                    const icon = L.divIcon({
                        className: 'custom-marker',
                        html: `<div class="marker-pin marker-usuario ${estadoClass}"><i class="bi bi-person"></i></div>`,
                        iconSize: [30, 42],
                        iconAnchor: [15, 42]
                    });
                    
                    const marker = L.marker([coord.latitud, coord.longitud], { icon: icon })
                        .addTo(mapaGeolocalizacion);
                    
                    const estadoBadge = {
                        'activo': '<span class="badge bg-success">Activo</span>',
                        'inactivo': '<span class="badge bg-warning">Inactivo</span>',
                        'ausente': '<span class="badge bg-secondary">Ausente</span>'
                    }[coord.estado_conexion] || '';
                    
                    const popupContent = `
                        <div class="p-2">
                            <h6>${coord.nombre}</h6>
                            <p class="mb-1">${estadoBadge}</p>
                            ${coord.puesto ? `<p class="mb-1"><strong>Puesto:</strong> ${coord.puesto.nombre}</p>` : ''}
                            ${coord.ultimo_acceso ? `<p class="mb-0"><small>Último acceso: ${Utils.formatDate(coord.ultimo_acceso)}</small></p>` : ''}
                        </div>
                    `;
                    
                    marker.bindPopup(popupContent);
                });
            }
            
            Utils.showSuccess('Mapa actualizado');
        }
    } catch (error) {
        console.error('Error loading map data:', error);
        Utils.showError('Error al cargar datos del mapa');
    }
}

/**
 * Actualizar mapa
 */
function actualizarMapa() {
    if (mapaGeolocalizacion) {
        cargarDatosMapa();
    }
}

/**
 * Centrar mapa en municipio
 */
function centrarMapaEnMunicipio() {
    if (mapaGeolocalizacion && userLocation) {
        // Placeholder - usar coordenadas del municipio
        Utils.showInfo('Centrando mapa en municipio...');
    }
}

/**
 * Ajustar vista del mapa
 */
function ajustarVistaMapa() {
    if (mapaGeolocalizacion) {
        mapaGeolocalizacion.fitBounds(mapaGeolocalizacion.getBounds());
    }
}

/**
 * Cargar y actualizar estado de coordinadores
 */
async function actualizarEstadoCoordinadores() {
    try {
        const response = await APIClient.get('/coordinador-municipal/coordinadores');
        
        if (response.success) {
            renderCoordinadores(response.data);
        }
    } catch (error) {
        console.error('Error loading coordinadores:', error);
        Utils.showError('Error al cargar coordinadores');
    }
}

/**
 * Renderizar lista de coordinadores
 */
function renderCoordinadores(coordinadores) {
    const container = document.getElementById('estadoCoordinadoresContainer');
    
    if (!coordinadores || coordinadores.length === 0) {
        container.innerHTML = '<p class="text-muted text-center py-4">No hay coordinadores asignados</p>';
        return;
    }
    
    // Agrupar por estado
    const activos = coordinadores.filter(c => c.estado_conexion === 'activo');
    const inactivos = coordinadores.filter(c => c.estado_conexion === 'inactivo');
    const ausentes = coordinadores.filter(c => c.estado_conexion === 'ausente');
    
    let html = `
        <div class="row mb-3">
            <div class="col-md-4">
                <div class="card bg-success bg-opacity-10">
                    <div class="card-body text-center">
                        <h3 class="text-success">${activos.length}</h3>
                        <small>Activos</small>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card bg-warning bg-opacity-10">
                    <div class="card-body text-center">
                        <h3 class="text-warning">${inactivos.length}</h3>
                        <small>Inactivos</small>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card bg-secondary bg-opacity-10">
                    <div class="card-body text-center">
                        <h3 class="text-secondary">${ausentes.length}</h3>
                        <small>Ausentes</small>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Coordinador</th>
                        <th>Puesto</th>
                        <th>Estado</th>
                        <th>Avance</th>
                        <th>Último Acceso</th>
                        <th>Contacto</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    coordinadores.forEach(coord => {
        const estadoBadge = {
            'activo': '<span class="badge bg-success">Activo</span>',
            'inactivo': '<span class="badge bg-warning">Inactivo</span>',
            'ausente': '<span class="badge bg-secondary">Ausente</span>'
        }[coord.estado_conexion] || '<span class="badge bg-secondary">Desconocido</span>';
        
        const avance = coord.estadisticas?.porcentaje_avance || 0;
        const ultimoAcceso = coord.ultimo_acceso ? 
            Utils.formatDate(coord.ultimo_acceso) : 'Nunca';
        
        html += `
            <tr>
                <td><strong>${coord.nombre}</strong></td>
                <td>
                    <small>${coord.puesto?.nombre || 'N/A'}</small><br>
                    <small class="text-muted">${coord.puesto?.codigo || ''}</small>
                </td>
                <td>${estadoBadge}</td>
                <td>
                    <div class="progress" style="height: 20px; min-width: 80px;">
                        <div class="progress-bar ${avance >= 100 ? 'bg-success' : 'bg-primary'}" 
                             style="width: ${avance}%">
                            ${avance.toFixed(0)}%
                        </div>
                    </div>
                    <small class="text-muted">${coord.estadisticas?.formularios_validados || 0}/${coord.estadisticas?.total_mesas || 0}</small>
                </td>
                <td><small>${ultimoAcceso}</small></td>
                <td>
                    ${coord.telefono ? `<small><i class="bi bi-telephone"></i> ${coord.telefono}</small>` : ''}
                </td>
            </tr>
        `;
    });
    
    html += `
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = html;
}

/**
 * Cargar y filtrar incidentes
 */
let incidentesData = [];
let filtroIncidenteActual = '';

async function cargarIncidentes() {
    try {
        const params = {};
        if (filtroIncidenteActual) {
            params.estado = filtroIncidenteActual;
        }
        
        const response = await APIClient.get('/coordinador-municipal/incidentes', params);
        
        if (response.success) {
            incidentesData = response.data;
            renderIncidentes(incidentesData);
            
            // Actualizar badges (desktop y móvil)
            const total = response.total || 0;
            document.getElementById('badge-incidentes').textContent = total;
            const badgeMobile = document.getElementById('badge-incidentes-mobile');
            if (badgeMobile) {
                badgeMobile.textContent = total;
            }
        }
    } catch (error) {
        console.error('Error loading incidentes:', error);
        document.getElementById('incidentesLista').innerHTML = 
            '<p class="text-danger text-center py-4">Error al cargar incidentes</p>';
    }
}

function filtrarIncidentes(estado) {
    filtroIncidenteActual = estado;
    
    // Actualizar botones activos
    document.querySelectorAll('#incidentes .btn-group button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    cargarIncidentes();
}

/**
 * Renderizar lista de incidentes
 */
function renderIncidentes(incidentes) {
    const container = document.getElementById('incidentesLista');
    
    if (!incidentes || incidentes.length === 0) {
        container.innerHTML = '<p class="text-muted text-center py-4">No hay incidentes reportados</p>';
        return;
    }
    
    let html = '';
    
    incidentes.forEach(incidente => {
        const severidadClass = {
            'baja': 'info',
            'media': 'warning',
            'alta': 'danger',
            'critica': 'danger'
        }[incidente.severidad] || 'secondary';
        
        const estadoBadge = {
            'reportado': '<span class="badge bg-primary">Reportado</span>',
            'en_revision': '<span class="badge bg-warning">En Revisión</span>',
            'resuelto': '<span class="badge bg-success">Resuelto</span>',
            'escalado': '<span class="badge bg-danger">Escalado</span>'
        }[incidente.estado] || '<span class="badge bg-secondary">Desconocido</span>';
        
        html += `
            <div class="card mb-3 border-${severidadClass}">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <div>
                            <h6 class="mb-1">${incidente.tipo}</h6>
                            <small class="text-muted">
                                <i class="bi bi-geo-alt"></i> ${incidente.mesa?.puesto_nombre || 'N/A'} - 
                                Mesa ${incidente.mesa?.codigo || 'N/A'}
                            </small>
                        </div>
                        <div class="text-end">
                            ${estadoBadge}
                            <br>
                            <span class="badge bg-${severidadClass} mt-1">${incidente.severidad}</span>
                        </div>
                    </div>
                    <p class="mb-2">${incidente.descripcion}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                            <i class="bi bi-person"></i> ${incidente.reportante?.nombre || 'Anónimo'} - 
                            ${Utils.formatDate(incidente.fecha_reporte)}
                        </small>
                        ${incidente.tiene_evidencia ? '<span class="badge bg-info"><i class="bi bi-paperclip"></i> Evidencia</span>' : ''}
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

/**
 * Cargar y filtrar delitos
 */
let delitosData = [];
let filtroDelitoActual = '';

async function cargarDelitos() {
    try {
        const params = {};
        if (filtroDelitoActual) {
            params.estado = filtroDelitoActual;
        }
        
        const response = await APIClient.get('/coordinador-municipal/delitos', params);
        
        if (response.success) {
            delitosData = response.data;
            renderDelitos(delitosData);
            
            // Actualizar badges (desktop y móvil)
            const total = response.total || 0;
            document.getElementById('badge-delitos').textContent = total;
            const badgeMobile = document.getElementById('badge-delitos-mobile');
            if (badgeMobile) {
                badgeMobile.textContent = total;
            }
        }
    } catch (error) {
        console.error('Error loading delitos:', error);
        document.getElementById('delitosLista').innerHTML = 
            '<p class="text-danger text-center py-4">Error al cargar delitos</p>';
    }
}

function filtrarDelitos(estado) {
    filtroDelitoActual = estado;
    
    // Actualizar botones activos
    document.querySelectorAll('#delitos .btn-group button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    cargarDelitos();
}

/**
 * Renderizar lista de delitos
 */
function renderDelitos(delitos) {
    const container = document.getElementById('delitosLista');
    
    if (!delitos || delitos.length === 0) {
        container.innerHTML = '<p class="text-muted text-center py-4">No hay delitos reportados</p>';
        return;
    }
    
    let html = '';
    
    delitos.forEach(delito => {
        const gravedadClass = {
            'leve': 'warning',
            'grave': 'danger',
            'muy_grave': 'danger'
        }[delito.gravedad] || 'secondary';
        
        const estadoBadge = {
            'reportado': '<span class="badge bg-primary">Reportado</span>',
            'en_investigacion': '<span class="badge bg-warning">En Investigación</span>',
            'investigado': '<span class="badge bg-success">Investigado</span>',
            'archivado': '<span class="badge bg-secondary">Archivado</span>'
        }[delito.estado] || '<span class="badge bg-secondary">Desconocido</span>';
        
        html += `
            <div class="card mb-3 border-${gravedadClass}">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <div>
                            <h6 class="mb-1 text-${gravedadClass}">
                                <i class="bi bi-shield-exclamation"></i> ${delito.tipo}
                            </h6>
                            <small class="text-muted">
                                <i class="bi bi-geo-alt"></i> ${delito.mesa?.puesto_nombre || 'N/A'} - 
                                Mesa ${delito.mesa?.codigo || 'N/A'}
                            </small>
                        </div>
                        <div class="text-end">
                            ${estadoBadge}
                            <br>
                            <span class="badge bg-${gravedadClass} mt-1">${delito.gravedad}</span>
                        </div>
                    </div>
                    <p class="mb-2">${delito.descripcion}</p>
                    ${delito.autoridad_notificada ? 
                        '<div class="alert alert-info py-1 px-2 mb-2"><small><i class="bi bi-check-circle"></i> Autoridad notificada</small></div>' 
                        : ''}
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                            <i class="bi bi-person"></i> ${delito.reportante?.nombre || 'Anónimo'} - 
                            ${Utils.formatDate(delito.fecha_reporte)}
                        </small>
                        ${delito.tiene_evidencia ? '<span class="badge bg-info"><i class="bi bi-paperclip"></i> Evidencia</span>' : ''}
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

/**
 * Mostrar error en tabla
 */
function showErrorInTable(message) {
    const tbody = document.querySelector('#puestosTable tbody');
    if (tbody) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center py-4">
                    <p class="text-danger">${message}</p>
                    <button class="btn btn-sm btn-outline-primary" onclick="loadPuestos()">
                        <i class="bi bi-arrow-clockwise"></i> Reintentar
                    </button>
                </td>
            </tr>
        `;
    }
}

/**
 * Cargar datos del tab E-24
 */
async function cargarDatosE24() {
    try {
        // Cargar datos de puestos con sus estadísticas
        const response = await APIClient.get('/coordinador-municipal/puestos');
        
        if (response.success) {
            const puestos = response.data.puestos || [];
            const stats = response.data.estadisticas || {};
            
            // Actualizar resumen
            document.getElementById('e24TotalPuestos').textContent = stats.total_puestos || 0;
            document.getElementById('e24PuestosValidados').textContent = stats.puestos_completos || 0;
            
            // Calcular totales
            let totalVotos = 0;
            let totalVotantes = 0;
            
            // Renderizar tabla
            const tbody = document.querySelector('#e24Table tbody');
            if (tbody) {
                if (puestos.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="10" class="text-center py-4">No hay datos disponibles</td></tr>';
                } else {
                    tbody.innerHTML = puestos.map(puesto => {
                        const estadoBadge = getEstadoBadge(puesto.estado);
                        const coordinador = puesto.coordinador?.nombre || 'Sin asignar';
                        const porcentaje = puesto.porcentaje_avance || 0;
                        
                        return `
                            <tr>
                                <td>${puesto.nombre}</td>
                                <td><small>${coordinador}</small></td>
                                <td class="text-center">${estadoBadge}</td>
                                <td class="text-end">${puesto.total_mesas}</td>
                                <td class="text-end">-</td>
                                <td class="text-end">-</td>
                                <td class="text-end">-</td>
                                <td class="text-end">-</td>
                                <td class="text-end">-</td>
                                <td class="text-end">${porcentaje.toFixed(0)}%</td>
                            </tr>
                        `;
                    }).join('');
                }
            }
            
            // Actualizar totales
            document.getElementById('e24TotalVotos').textContent = totalVotos;
            document.getElementById('e24Participacion').textContent = '0%';
            
            // Cargar consolidado de votos por partido
            const consolidadoResponse = await APIClient.get('/coordinador-municipal/consolidado');
            if (consolidadoResponse.success) {
                const consolidado = consolidadoResponse.data;
                const resumen = consolidado.resumen || {};
                
                document.getElementById('e24TotalVotos').textContent = Utils.formatNumber(resumen.total_votos || 0);
                document.getElementById('e24Participacion').textContent = `${(resumen.participacion_porcentaje || 0).toFixed(2)}%`;
                
                // Actualizar footer
                document.getElementById('e24FooterVotantes').textContent = Utils.formatNumber(resumen.total_votantes_registrados || 0);
                document.getElementById('e24FooterVotos').textContent = Utils.formatNumber(resumen.total_votos || 0);
                document.getElementById('e24FooterValidos').textContent = Utils.formatNumber(resumen.votos_validos || 0);
                document.getElementById('e24FooterNulos').textContent = Utils.formatNumber(resumen.votos_nulos || 0);
                document.getElementById('e24FooterBlanco').textContent = Utils.formatNumber(resumen.votos_blanco || 0);
                document.getElementById('e24FooterParticipacion').textContent = `${(resumen.participacion_porcentaje || 0).toFixed(2)}%`;
                
                // Renderizar votos por partido
                renderVotosPartidosE24(consolidado.votos_por_partido || []);
            }
        }
    } catch (error) {
        console.error('Error loading E-24 data:', error);
        const tbody = document.querySelector('#e24Table tbody');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="10" class="text-center py-4 text-danger">Error al cargar datos</td></tr>';
        }
    }
}

/**
 * Renderizar votos por partido en E-24
 */
function renderVotosPartidosE24(votosPartidos) {
    const container = document.getElementById('e24VotosPartidos');
    
    if (!container) return;
    
    if (!votosPartidos || votosPartidos.length === 0) {
        container.innerHTML = '<p class="text-muted">No hay datos de votos por partido</p>';
        return;
    }
    
    let html = '<div class="row">';
    
    votosPartidos.forEach(partido => {
        html += `
            <div class="col-md-6 mb-3">
                <div class="card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <div>
                                <span style="display: inline-block; width: 12px; height: 12px; background-color: ${partido.partido_color}; border-radius: 2px; margin-right: 8px;"></span>
                                <strong>${partido.partido_nombre_corto}</strong>
                            </div>
                            <h4 class="mb-0">${Utils.formatNumber(partido.total_votos)}</h4>
                        </div>
                        <div class="progress" style="height: 8px;">
                            <div class="progress-bar" 
                                 style="width: ${partido.porcentaje}%; background-color: ${partido.partido_color};">
                            </div>
                        </div>
                        <small class="text-muted">${partido.porcentaje.toFixed(2)}% del total</small>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

/**
 * Logout
 */
function logout() {
    localStorage.removeItem('token');
    window.location.href = '/auth/login';
}
