/**
 * Dashboard del Auditor Electoral - Actualizado para nuevo template
 */

const auditorDashboard = {
    currentUser: null,
    departamento: null,
    formularios: [],
    discrepancias: [],
    incidentes: [],
    filtroEstado: '',
    autoRefreshInterval: null,
    charts: {},

    /**
     * Inicializar dashboard
     */
    init: function() {
        console.log('Inicializando dashboard de auditor...');
        this.loadUserProfile();
        this.loadStats();
        this.loadFormularios();
        this.loadAnomalias();
        this.loadIncidentes();
        this.setupEventListeners();
        this.startAutoRefresh();
    },

    /**
     * Configurar event listeners
     */
    setupEventListeners: function() {
        // Tab de consolidado
        const consolidadoTab = document.getElementById('resumen-tab');
        if (consolidadoTab) {
            consolidadoTab.addEventListener('shown.bs.tab', () => {
                this.loadResumen();
            });
        }

        // Tab de mapa
        const mapaTab = document.getElementById('mapa-tab');
        if (mapaTab) {
            mapaTab.addEventListener('shown.bs.tab', () => {
                this.initMapa();
            });
        }

        // Búsqueda de formularios
        const searchInput = document.getElementById('buscar-formulario');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.buscarFormularios(e.target.value);
            });
        }
    },

    /**
     * Iniciar auto-refresh
     */
    startAutoRefresh: function() {
        this.autoRefreshInterval = setInterval(() => {
            this.loadStats();
            this.loadFormularios();
            this.loadAnomalias();
        }, 60000); // 60 segundos
    },

    /**
     * Detener auto-refresh
     */
    stopAutoRefresh: function() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
        }
    }
};

// Limpiar interval al salir
window.addEventListener('beforeunload', function() {
    if (auditorDashboard.autoRefreshInterval) {
        clearInterval(auditorDashboard.autoRefreshInterval);
    }
});

/**
 * Cargar perfil del auditor
 */
auditorDashboard.loadUserProfile = async function() {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            window.location.href = '/login';
            return;
        }

        const response = await fetch('/api/auth/profile', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            this.currentUser = data.user;
            this.departamento = data.ubicacion;
            
            console.log('Perfil cargado:', this.currentUser);
        } else {
            throw new Error('Error al cargar perfil');
        }
    } catch (error) {
        console.error('Error loading profile:', error);
        this.showError('Error al cargar perfil');
    }
};

/**
 * Cargar estadísticas de auditoría
 */
auditorDashboard.loadStats = async function() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('/api/auditor/stats', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            const stats = data.data;
            
            // Actualizar estadísticas en las cards
            document.getElementById('stat-formularios-validados').textContent = stats.formularios_completados || 0;
            document.getElementById('stat-formularios-info').textContent = `${stats.total_formularios || 0} formularios totales`;
            
            document.getElementById('stat-anomalias').textContent = stats.inconsistencias_detectadas || 0;
            document.getElementById('stat-anomalias-info').textContent = 'Requieren atención';
            
            document.getElementById('stat-incidentes').textContent = stats.formularios_pendientes || 0;
            document.getElementById('stat-incidentes-info').textContent = 'Pendientes de revisión';
            
            document.getElementById('stat-progreso').textContent = `${stats.porcentaje_auditado.toFixed(1)}%`;
            document.getElementById('stat-progreso-info').textContent = 'Completado';
        } else {
            throw new Error('Error al cargar estadísticas');
        }
    } catch (error) {
        console.error('Error loading stats:', error);
        this.showError('Error al cargar estadísticas');
    }
};

/**
 * Cargar lista de formularios
 */
auditorDashboard.loadFormularios = async function() {
    try {
        const token = localStorage.getItem('access_token');
        let url = '/api/auditor/formularios';
        
        if (this.filtroEstado) {
            url += `?estado=${this.filtroEstado}`;
        }
        
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            this.formularios = data.data || [];
            this.renderFormulariosTable(this.formularios);
        } else {
            throw new Error('Error al cargar formularios');
        }
    } catch (error) {
        console.error('Error loading formularios:', error);
        const tbody = document.querySelector('#tabla-formularios tbody');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="9" class="text-center py-4">
                        <p class="text-danger mb-2">Error al cargar formularios</p>
                        <button class="btn btn-sm btn-outline-primary" onclick="auditorDashboard.loadFormularios()">
                            <i class="bi bi-arrow-clockwise"></i> Reintentar
                        </button>
                    </td>
                </tr>
            `;
        }
    }
};

/**
 * Renderizar tabla de formularios
 */
auditorDashboard.renderFormulariosTable = function(formularios) {
    const tbody = document.querySelector('#tabla-formularios tbody');
    
    if (!tbody) return;
    
    if (formularios.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="9" class="text-center py-4">
                    <p class="text-muted">No hay formularios ${this.filtroEstado ? 'en estado ' + this.filtroEstado : ''}</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = formularios.map(form => {
        const estadoBadge = this.getEstadoBadge(form.estado);
        const fecha = this.formatDate(form.updated_at || form.created_at);
        
        // Obtener información de ubicación
        const puesto = form.mesa_nombre ? form.mesa_nombre.split(' - ')[0] : 'N/A';
        const municipio = form.mesa_nombre ? form.mesa_nombre.split(' - ')[1] || 'N/A' : 'N/A';
        const departamento = form.mesa_nombre ? form.mesa_nombre.split(' - ')[2] || 'N/A' : 'N/A';
        
        return `
            <tr onclick="auditorDashboard.verDetalleFormulario(${form.id})" style="cursor: pointer;">
                <td><strong>#${form.id}</strong></td>
                <td>${form.mesa_nombre || 'N/A'}</td>
                <td>${puesto}</td>
                <td>${municipio}</td>
                <td>${departamento}</td>
                <td>${form.testigo_nombre || 'N/A'}</td>
                <td><small>${fecha}</small></td>
                <td class="text-center">${estadoBadge}</td>
                <td class="text-center">
                    <button class="btn btn-sm btn-outline-primary" onclick="event.stopPropagation(); auditorDashboard.verDetalleFormulario(${form.id})">
                        <i class="bi bi-eye"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');
};

/**
 * Obtener badge de estado
 */
auditorDashboard.getEstadoBadge = function(estado) {
    const badges = {
        'borrador': '<span class="badge bg-secondary">Borrador</span>',
        'pendiente': '<span class="badge bg-warning text-dark">Pendiente</span>',
        'validado': '<span class="badge bg-success">Validado</span>',
        'rechazado': '<span class="badge bg-danger">Rechazado</span>',
        'en_revision': '<span class="badge bg-info">En Revisión</span>',
        'completado': '<span class="badge bg-success">Completado</span>'
    };
    return badges[estado] || `<span class="badge bg-secondary">${estado}</span>`;
};

/**
 * Formatear fecha
 */
auditorDashboard.formatDate = function(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
};

/**
 * Mostrar error
 */
auditorDashboard.showError = function(message) {
    console.error(message);
    // TODO: Implementar notificación visual
    alert(message);
};

/**
 * Mostrar éxito
 */
auditorDashboard.showSuccess = function(message) {
    console.log(message);
    // TODO: Implementar notificación visual
    alert(message);
};



/**
 * Cargar anomalías detectadas
 */
auditorDashboard.loadAnomalias = async function() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('/api/auditor/discrepancias', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            this.discrepancias = data.data || [];
            this.renderAnomalias(this.discrepancias);
        } else {
            throw new Error('Error al cargar anomalías');
        }
    } catch (error) {
        console.error('Error loading anomalias:', error);
        const container = document.getElementById('lista-anomalias');
        if (container) {
            container.innerHTML = `
                <div class="text-center py-3">
                    <p class="text-danger mb-2">Error al cargar anomalias</p>
                    <button class="btn btn-sm btn-outline-primary" onclick="auditorDashboard.loadAnomalias()">
                        <i class="bi bi-arrow-clockwise"></i> Reintentar
                    </button>
                </div>
            `;
        }
    }
};

/**
 * Renderizar anomalías
 */
auditorDashboard.renderAnomalias = function(anomalias) {
    const container = document.getElementById('lista-anomalias');
    
    if (!container) return;
    
    if (anomalias.length === 0) {
        container.innerHTML = `
            <div class="text-center py-3">
                <i class="bi bi-check-circle text-success" style="font-size: 2rem;"></i>
                <p class="text-muted mb-0">No hay anomalías detectadas</p>
            </div>
        `;
        return;
    }
    
    // Agrupar por severidad
    const criticas = anomalias.filter(d => d.severidad === 'critica');
    const altas = anomalias.filter(d => d.severidad === 'alta');
    const medias = anomalias.filter(d => d.severidad === 'media');
    
    let html = '';
    
    // Mostrar críticas
    if (criticas.length > 0) {
        html += '<h6 class="text-danger mb-2"><i class="bi bi-exclamation-octagon"></i> Críticas</h6>';
        criticas.slice(0, 5).forEach(d => {
            html += this.renderAnomaliaItem(d);
        });
    }
    
    // Mostrar altas
    if (altas.length > 0) {
        html += '<h6 class="text-warning mb-2 mt-3"><i class="bi bi-exclamation-triangle"></i> Altas</h6>';
        altas.slice(0, 5).forEach(d => {
            html += this.renderAnomaliaItem(d);
        });
    }
    
    // Mostrar medias (máximo 3)
    if (medias.length > 0) {
        html += '<h6 class="text-info mb-2 mt-3"><i class="bi bi-info-circle"></i> Medias</h6>';
        medias.slice(0, 3).forEach(d => {
            html += this.renderAnomaliaItem(d);
        });
    }
    
    // Total
    html += `
        <div class="mt-3 text-center">
            <small class="text-muted">
                Total: ${anomalias.length} anomalía(s) detectada(s)
            </small>
        </div>
    `;
    
    container.innerHTML = html;
};

/**
 * Renderizar item de anomalía
 */
auditorDashboard.renderAnomaliaItem = function(anomalia) {
    const severidadClass = {
        'critica': 'danger',
        'alta': 'warning',
        'media': 'info'
    };
    
    const badgeClass = severidadClass[anomalia.severidad] || 'secondary';
    const badgeText = anomalia.severidad.toUpperCase();
    
    return `
        <div class="alert alert-${badgeClass} py-2 px-3 mb-2" role="alert" 
             style="cursor: pointer;" onclick="auditorDashboard.verDetalleFormulario(${anomalia.formulario_id})">
            <div class="d-flex justify-content-between align-items-start">
                <div class="flex-grow-1">
                    <strong>${anomalia.mesa_codigo}</strong> - ${anomalia.mesa_nombre}<br>
                    <small>${anomalia.descripcion}</small>
                </div>
                <span class="anomaly-badge anomaly-${anomalia.severidad}">${badgeText}</span>
            </div>
        </div>
    `;
};

/**
 * Cargar incidentes reportados
 */
auditorDashboard.loadIncidentes = async function() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('/api/incidentes?limit=50', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            this.incidentes = data.data || [];
            this.renderIncidentes(this.incidentes);
        } else {
            throw new Error('Error al cargar incidentes');
        }
    } catch (error) {
        console.error('Error loading incidentes:', error);
        const tbody = document.querySelector('#tabla-incidentes tbody');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center py-4">
                        <p class="text-danger mb-2">Error al cargar incidentes</p>
                        <button class="btn btn-sm btn-outline-primary" onclick="auditorDashboard.loadIncidentes()">
                            <i class="bi bi-arrow-clockwise"></i> Reintentar
                        </button>
                    </td>
                </tr>
            `;
        }
    }
};

/**
 * Renderizar incidentes
 */
auditorDashboard.renderIncidentes = function(incidentes) {
    const tbody = document.querySelector('#tabla-incidentes tbody');
    
    if (!tbody) return;
    
    if (incidentes.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center py-4">
                    <p class="text-muted">No hay incidentes reportados</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = incidentes.map(inc => {
        const tipo = inc.tipo_incidente || 'Incidente';
        const severidad = inc.severidad || 'media';
        const estado = inc.estado || 'reportado';
        const fecha = this.formatDate(inc.created_at);
        
        const severidadBadge = {
            'baja': '<span class="badge bg-info">Baja</span>',
            'media': '<span class="badge bg-warning">Media</span>',
            'alta': '<span class="badge bg-danger">Alta</span>'
        }[severidad] || '<span class="badge bg-secondary">N/A</span>';
        
        const estadoBadge = {
            'reportado': '<span class="badge bg-warning">Reportado</span>',
            'en_revision': '<span class="badge bg-info">En Revisión</span>',
            'resuelto': '<span class="badge bg-success">Resuelto</span>'
        }[estado] || '<span class="badge bg-secondary">N/A</span>';
        
        return `
            <tr>
                <td>${tipo}</td>
                <td>${inc.descripcion || 'Sin descripción'}</td>
                <td>${inc.puesto_nombre || 'N/A'}</td>
                <td>${severidadBadge}</td>
                <td>${inc.reportado_por_nombre || 'N/A'}</td>
                <td><small>${fecha}</small></td>
                <td>${estadoBadge}</td>
            </tr>
        `;
    }).join('');
};

/**
 * Cargar resumen para el tab de resumen
 */
auditorDashboard.loadResumen = async function() {
    try {
        const token = localStorage.getItem('access_token');
        
        // Cargar estadísticas por municipio
        const respMunicipios = await fetch('/api/auditor/municipios', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (respMunicipios.ok) {
            const data = await respMunicipios.json();
            this.renderGraficoProgresoDepartamento(data.data || []);
        }
        
        // Cargar consolidado
        const respConsolidado = await fetch('/api/auditor/consolidado', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (respConsolidado.ok) {
            const data = await respConsolidado.json();
            this.renderGraficoEstadoValidacion(data.data);
        }
        
        // Cargar actividad reciente
        this.renderActividadReciente();
        
    } catch (error) {
        console.error('Error loading resumen:', error);
    }
};

/**
 * Renderizar gráfico de progreso por departamento
 */
auditorDashboard.renderGraficoProgresoDepartamento = function(municipios) {
    const canvas = document.getElementById('chart-progreso-departamento');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Destruir gráfico anterior si existe
    if (this.charts.progresoDepartamento) {
        this.charts.progresoDepartamento.destroy();
    }
    
    const labels = municipios.map(m => m.nombre);
    const data = municipios.map(m => m.porcentaje_avance);
    
    this.charts.progresoDepartamento = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Progreso (%)',
                data: data,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
};

/**
 * Renderizar gráfico de estado de validación
 */
auditorDashboard.renderGraficoEstadoValidacion = function(consolidado) {
    const canvas = document.getElementById('chart-estado-validacion');
    if (!canvas || !consolidado) return;
    
    const ctx = canvas.getContext('2d');
    
    // Destruir gráfico anterior si existe
    if (this.charts.estadoValidacion) {
        this.charts.estadoValidacion.destroy();
    }
    
    this.charts.estadoValidacion = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Validados', 'Pendientes', 'Rechazados'],
            datasets: [{
                data: [
                    consolidado.total_formularios || 0,
                    consolidado.formularios_pendientes || 0,
                    consolidado.formularios_rechazados || 0
                ],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(255, 99, 132, 0.5)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
};

/**
 * Renderizar actividad reciente
 */
auditorDashboard.renderActividadReciente = function() {
    const container = document.getElementById('actividad-reciente');
    if (!container) return;
    
    // Por ahora mostrar mensaje
    container.innerHTML = `
        <div class="list-group">
            <div class="list-group-item">
                <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">Sistema de auditoría activo</h6>
                    <small>${this.formatDate(new Date())}</small>
                </div>
                <p class="mb-1">Monitoreo en tiempo real de formularios y anomalías</p>
            </div>
        </div>
    `;
};

/**
 * Ver detalle de formulario
 */
auditorDashboard.verDetalleFormulario = async function(formularioId) {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`/api/formularios/${formularioId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const data = await response.json();
            this.mostrarModalDetalle(data.data);
        } else {
            throw new Error('Error al cargar formulario');
        }
    } catch (error) {
        console.error('Error loading formulario:', error);
        this.showError('Error al cargar formulario: ' + error.message);
    }
};

/**
 * Mostrar modal con detalle del formulario
 */
auditorDashboard.mostrarModalDetalle = function(formulario) {
    // TODO: Implementar modal de detalle
    alert(`Detalle del formulario #${formulario.id}\nEstado: ${formulario.estado}`);
};

/**
 * Buscar formularios
 */
auditorDashboard.buscarFormularios = function(query) {
    if (!query) {
        this.renderFormulariosTable(this.formularios);
        return;
    }
    
    const filtered = this.formularios.filter(f => {
        const searchText = `${f.id} ${f.mesa_nombre} ${f.testigo_nombre}`.toLowerCase();
        return searchText.includes(query.toLowerCase());
    });
    
    this.renderFormulariosTable(filtered);
};

/**
 * Inicializar mapa
 */
auditorDashboard.initMapa = function() {
    const container = document.getElementById('mapa-auditoria');
    if (!container) return;
    
    if (this.mapa) return; // Ya está inicializado
    
    // Inicializar mapa de Leaflet
    this.mapa = L.map('mapa-auditoria').setView([1.6144, -75.6062], 9);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(this.mapa);
    
    // Cargar puestos en el mapa
    this.cargarPuestosEnMapa();
};

/**
 * Cargar puestos en el mapa
 */
auditorDashboard.cargarPuestosEnMapa = async function() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('/api/locations/puestos', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const data = await response.json();
            const puestos = data.data || [];
            
            puestos.forEach(puesto => {
                if (puesto.latitud && puesto.longitud) {
                    const marker = L.marker([puesto.latitud, puesto.longitud])
                        .addTo(this.mapa);
                    
                    marker.bindPopup(`
                        <strong>${puesto.nombre_completo}</strong><br>
                        Código: ${puesto.codigo}
                    `);
                }
            });
        }
    } catch (error) {
        console.error('Error loading puestos:', error);
    }
};

/**
 * Exportar reporte de auditoría
 */
auditorDashboard.exportarReporte = async function() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('/api/auditor/exportar?formato=csv', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `auditoria_${new Date().getTime()}.csv`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
            
            this.showSuccess('Reporte exportado exitosamente');
        } else {
            throw new Error('Error al exportar reporte');
        }
    } catch (error) {
        console.error('Error exporting report:', error);
        this.showError('Error al exportar reporte: ' + error.message);
    }
};

// Exponer el objeto auditorDashboard globalmente
window.auditorDashboard = auditorDashboard;
