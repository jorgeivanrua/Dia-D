/**
 * DASHBOARD DE MONITOREO OPTIMIZADO
 * Para múltiples usuarios simultáneos
 * 
 * Características:
 * - Lazy loading de actividades
 * - Clustering de marcadores
 * - Caché local
 * - Actualizaciones incrementales
 * - Debouncing de filtros
 */

// ============================================================================
// CONFIGURACIÓN
// ============================================================================

const CONFIG = {
    AUTO_REFRESH_INTERVAL: 30000, // 30 segundos
    CACHE_DURATION: 20000, // 20 segundos
    DEBOUNCE_DELAY: 300, // 300ms
    PAGE_SIZE: 20,
    MAX_MARKERS: 1000
};

// ============================================================================
// CACHÉ LOCAL
// ============================================================================

class LocalCache {
    constructor() {
        this.cache = new Map();
    }
    
    set(key, value, duration = CONFIG.CACHE_DURATION) {
        this.cache.set(key, {
            value,
            expires: Date.now() + duration
        });
    }
    
    get(key) {
        const item = this.cache.get(key);
        if (!item) return null;
        
        if (Date.now() > item.expires) {
            this.cache.delete(key);
            return null;
        }
        
        return item.value;
    }
    
    clear() {
        this.cache.clear();
    }
    
    delete(key) {
        this.cache.delete(key);
    }
}

const cache = new LocalCache();

// ============================================================================
// UTILIDADES
// ============================================================================

/**
 * Debounce para evitar llamadas excesivas
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle para limitar frecuencia de ejecución
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * Mostrar skeleton loader
 */
function showSkeleton(containerId, count = 3) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    let html = '';
    for (let i = 0; i < count; i++) {
        html += `
            <div class="skeleton-item mb-3">
                <div class="skeleton-line" style="width: 80%;"></div>
                <div class="skeleton-line" style="width: 60%;"></div>
                <div class="skeleton-line" style="width: 40%;"></div>
            </div>
        `;
    }
    container.innerHTML = html;
}

// ============================================================================
// MAPA CON CLUSTERING
// ============================================================================

class MapaMonitoreo {
    constructor(mapId) {
        this.mapId = mapId;
        this.map = null;
        this.markerCluster = null;
        this.markers = [];
        this.init();
    }
    
    init() {
        // Inicializar mapa
        this.map = L.map(this.mapId).setView([4.5709, -74.2973], 6);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(this.map);
        
        // Inicializar cluster group
        this.markerCluster = L.markerClusterGroup({
            maxClusterRadius: 50,
            spiderfyOnMaxZoom: true,
            showCoverageOnHover: true,
            zoomToBoundsOnClick: true,
            disableClusteringAtZoom: 15,
            iconCreateFunction: (cluster) => {
                const count = cluster.getChildCount();
                let size = 'small';
                if (count > 50) size = 'large';
                else if (count > 10) size = 'medium';
                
                return L.divIcon({
                    html: `<div class="marker-cluster marker-cluster-${size}">${count}</div>`,
                    className: 'marker-cluster-custom',
                    iconSize: L.point(40, 40)
                });
            }
        });
        
        this.map.addLayer(this.markerCluster);
    }
    
    actualizarMarcadores(usuarios) {
        // Limpiar marcadores anteriores
        this.markerCluster.clearLayers();
        this.markers = [];
        
        // Limitar número de marcadores
        const usuariosLimitados = usuarios.slice(0, CONFIG.MAX_MARKERS);
        
        // Agregar nuevos marcadores
        usuariosLimitados.forEach(usuario => {
            const color = this.getMarkerColor(usuario);
            const icon = this.createCustomIcon(color);
            
            const marker = L.marker([usuario.latitud, usuario.longitud], { icon });
            
            // Popup con información
            const popupContent = this.createPopupContent(usuario);
            marker.bindPopup(popupContent);
            
            this.markerCluster.addLayer(marker);
            this.markers.push(marker);
        });
        
        // Ajustar vista si hay usuarios
        if (usuariosLimitados.length > 0) {
            const bounds = L.latLngBounds(
                usuariosLimitados.map(u => [u.latitud, u.longitud])
            );
            this.map.fitBounds(bounds, { padding: [50, 50], maxZoom: 12 });
        }
        
        // Actualizar contador
        document.getElementById('usuarios-activos-badge').textContent = 
            `${usuarios.length} usuarios activos`;
    }
    
    getMarkerColor(usuario) {
        if (usuario.rol === 'testigo_electoral') {
            return usuario.presencia_verificada ? '#28a745' : '#ffc107';
        } else if (usuario.rol === 'coordinador_puesto') {
            return '#007bff';
        } else if (usuario.rol === 'coordinador_municipal') {
            return '#6f42c1';
        } else if (usuario.rol === 'coordinador_departamental') {
            return '#e83e8c';
        } else if (usuario.rol === 'auditor_electoral') {
            return '#17a2b8';
        }
        return '#6c757d';
    }
    
    createCustomIcon(color) {
        return L.divIcon({
            className: 'custom-marker',
            html: `<div style="background-color: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 6px rgba(0,0,0,0.3);"></div>`,
            iconSize: [20, 20],
            iconAnchor: [10, 10]
        });
    }
    
    createPopupContent(usuario) {
        let content = `
            <div style="min-width: 200px;">
                <h6><strong>${usuario.nombre}</strong></h6>
                <p class="mb-1"><small><strong>Rol:</strong> ${usuario.rol}</small></p>
        `;
        
        if (usuario.ubicacion) {
            content += `<p class="mb-1"><small><strong>Ubicación:</strong> ${usuario.ubicacion.nombre_completo || 'N/A'}</small></p>`;
        }
        
        if (usuario.rol === 'testigo_electoral') {
            content += `<p class="mb-1"><small><strong>Presencia:</strong> ${usuario.presencia_verificada ? '✅ Verificada' : '⏳ Pendiente'}</small></p>`;
        }
        
        if (usuario.ultima_actualizacion) {
            const fecha = new Date(usuario.ultima_actualizacion);
            content += `<p class="mb-0"><small><strong>Actualizado:</strong> ${fecha.toLocaleString()}</small></p>`;
        }
        
        content += `</div>`;
        return content;
    }
}

// ============================================================================
// GESTOR DE ACTIVIDAD RECIENTE CON LAZY LOADING
// ============================================================================

class ActividadReciente {
    constructor(containerId) {
        this.containerId = containerId;
        this.container = document.getElementById(containerId);
        this.currentPage = 1;
        this.loading = false;
        this.hasMore = true;
        this.setupScrollListener();
    }
    
    setupScrollListener() {
        if (!this.container) return;
        
        this.container.addEventListener('scroll', throttle(() => {
            const { scrollTop, scrollHeight, clientHeight } = this.container;
            
            // Si está cerca del final (100px antes)
            if (scrollTop + clientHeight >= scrollHeight - 100) {
                this.cargarMas();
            }
        }, 500));
    }
    
    async cargarInicial() {
        this.currentPage = 1;
        this.hasMore = true;
        showSkeleton(this.containerId, 5);
        
        try {
            const response = await APIClient.get(
                `/monitoreo/api/actividad-reciente?page=1&limit=${CONFIG.PAGE_SIZE}`
            );
            
            if (response.success) {
                this.renderActividades(response.data, true);
                this.hasMore = response.data.length === CONFIG.PAGE_SIZE;
            }
        } catch (error) {
            console.error('Error cargando actividad:', error);
            this.container.innerHTML = '<p class="text-danger">Error cargando actividad</p>';
        }
    }
    
    async cargarMas() {
        if (this.loading || !this.hasMore) return;
        
        this.loading = true;
        this.currentPage++;
        
        try {
            const response = await APIClient.get(
                `/monitoreo/api/actividad-reciente?page=${this.currentPage}&limit=${CONFIG.PAGE_SIZE}`
            );
            
            if (response.success) {
                this.renderActividades(response.data, false);
                this.hasMore = response.data.length === CONFIG.PAGE_SIZE;
            }
        } catch (error) {
            console.error('Error cargando más actividad:', error);
        } finally {
            this.loading = false;
        }
    }
    
    renderActividades(actividades, replace = false) {
        if (actividades.length === 0) {
            if (replace) {
                this.container.innerHTML = '<p class="text-muted">No hay actividad reciente.</p>';
            }
            return;
        }
        
        let html = '';
        actividades.forEach(act => {
            html += this.renderActividadItem(act);
        });
        
        if (replace) {
            this.container.innerHTML = `<div class="list-group list-group-flush">${html}</div>`;
        } else {
            const listGroup = this.container.querySelector('.list-group');
            if (listGroup) {
                listGroup.insertAdjacentHTML('beforeend', html);
            }
        }
    }
    
    renderActividadItem(act) {
        const fecha = new Date(act.timestamp);
        const tiempoRelativo = this.getRelativeTime(fecha);
        
        let badgeClass = 'secondary';
        let badgeText = '';
        
        if (act.tipo === 'formulario') {
            badgeClass = act.estado === 'validado' ? 'success' : 
                        act.estado === 'pendiente' ? 'warning' : 'danger';
            badgeText = act.estado;
        } else if (act.tipo === 'incidente') {
            badgeClass = act.severidad === 'critica' ? 'danger' : 
                        act.severidad === 'alta' ? 'warning' : 'info';
            badgeText = act.severidad;
        }
        
        return `
            <div class="list-group-item">
                <div class="d-flex w-100 justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <div class="d-flex align-items-center mb-1">
                            <i class="bi bi-${act.icono || 'info-circle'} me-2 text-primary"></i>
                            <strong>${act.titulo}</strong>
                        </div>
                        <p class="mb-1 small text-muted">${act.descripcion}</p>
                        <small class="text-muted">
                            <i class="bi bi-person"></i> ${act.usuario || 'Sistema'} • 
                            <i class="bi bi-clock"></i> ${tiempoRelativo}
                        </small>
                    </div>
                    ${badgeText ? `<span class="badge bg-${badgeClass}">${badgeText}</span>` : ''}
                </div>
            </div>
        `;
    }
    
    getRelativeTime(date) {
        const now = new Date();
        const diff = Math.floor((now - date) / 1000);
        
        if (diff < 60) return 'Hace un momento';
        if (diff < 3600) return `Hace ${Math.floor(diff / 60)} minutos`;
        if (diff < 86400) return `Hace ${Math.floor(diff / 3600)} horas`;
        return `Hace ${Math.floor(diff / 86400)} días`;
    }
}

// ============================================================================
// GESTOR PRINCIPAL
// ============================================================================

class MonitoreoManager {
    constructor() {
        this.mapa = null;
        this.actividad = null;
        this.autoRefreshInterval = null;
        this.filtros = {
            tipoUsuario: '',
            departamento: '',
            municipio: '',
            zona: '',
            puesto: ''
        };
        this.todosLosUsuarios = [];
    }
    
    async init() {
        // Inicializar componentes
        this.mapa = new MapaMonitoreo('mapa-monitoreo');
        this.actividad = new ActividadReciente('actividad-reciente-container');
        
        // Cargar datos iniciales
        await this.cargarDatosIniciales();
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Iniciar auto-refresh
        this.setupAutoRefresh();
        
        console.log('✅ Monitoreo Manager inicializado');
    }
    
    async cargarDatosIniciales() {
        await Promise.all([
            this.cargarEstadisticas(),
            this.cargarUsuariosActivos(),
            this.cargarAlertas(),
            this.actividad.cargarInicial()
        ]);
    }
    
    async cargarEstadisticas() {
        try {
            // Intentar obtener del caché
            const cacheKey = 'estadisticas';
            let stats = cache.get(cacheKey);
            
            if (!stats) {
                const response = await APIClient.get('/monitoreo/api/estadisticas');
                if (response.success) {
                    stats = response.data;
                    cache.set(cacheKey, stats);
                }
            }
            
            if (stats) {
                this.actualizarEstadisticas(stats);
            }
        } catch (error) {
            console.error('Error cargando estadísticas:', error);
        }
    }
    
    actualizarEstadisticas(stats) {
        document.getElementById('stat-testigos-geo').textContent = stats.testigos.con_geolocalizacion;
        document.getElementById('stat-testigos-porcentaje').textContent = `${stats.testigos.porcentaje_geo}% del total`;
        document.getElementById('stat-testigos-presencia').textContent = stats.testigos.con_presencia_verificada;
        
        document.getElementById('stat-coordinadores-geo').textContent = stats.coordinadores.con_geolocalizacion;
        document.getElementById('stat-coordinadores-porcentaje').textContent = `${stats.coordinadores.porcentaje_geo}% del total`;
        
        document.getElementById('stat-formularios').textContent = stats.formularios.total;
        document.getElementById('stat-formularios-validados').textContent = `${stats.formularios.validados} validados`;
    }
    
    async cargarUsuariosActivos() {
        try {
            const cacheKey = 'usuarios_activos';
            let usuarios = cache.get(cacheKey);
            
            if (!usuarios) {
                const response = await APIClient.get('/monitoreo/api/usuarios-activos');
                if (response.success) {
                    usuarios = response.data;
                    cache.set(cacheKey, usuarios);
                }
            }
            
            if (usuarios) {
                this.todosLosUsuarios = usuarios;
                this.aplicarFiltros();
            }
        } catch (error) {
            console.error('Error cargando usuarios:', error);
        }
    }
    
    async cargarAlertas() {
        try {
            const response = await APIClient.get('/monitoreo/api/alertas');
            if (response.success) {
                this.renderAlertas(response.data);
            }
        } catch (error) {
            console.error('Error cargando alertas:', error);
        }
    }
    
    renderAlertas(alertas) {
        const container = document.getElementById('alertas-container');
        if (!container) return;
        
        if (alertas.length === 0) {
            container.innerHTML = '<p class="text-success mb-0"><i class="bi bi-check-circle"></i> No hay alertas. Todo funciona correctamente.</p>';
            return;
        }
        
        let html = '<div class="row g-2">';
        alertas.forEach(alerta => {
            html += `
                <div class="col-md-6">
                    <div class="alert alert-${alerta.tipo} mb-0">
                        <div class="d-flex align-items-start">
                            <i class="bi bi-${alerta.icono || 'info-circle'} me-2" style="font-size: 1.5rem;"></i>
                            <div class="flex-grow-1">
                                <strong>${alerta.titulo}</strong>
                                <p class="mb-0 small">${alerta.descripcion}</p>
                            </div>
                            <span class="badge bg-${alerta.tipo}">${alerta.cantidad}</span>
                        </div>
                    </div>
                </div>
            `;
        });
        html += '</div>';
        container.innerHTML = html;
    }
    
    aplicarFiltros() {
        let usuariosFiltrados = [...this.todosLosUsuarios];
        
        // Aplicar filtros
        if (this.filtros.tipoUsuario) {
            if (this.filtros.tipoUsuario === 'coordinadores') {
                usuariosFiltrados = usuariosFiltrados.filter(u => u.rol.includes('coordinador'));
            } else {
                usuariosFiltrados = usuariosFiltrados.filter(u => u.rol === this.filtros.tipoUsuario);
            }
        }
        
        // Actualizar mapa
        this.mapa.actualizarMarcadores(usuariosFiltrados);
    }
    
    setupEventListeners() {
        // Filtro de tipo de usuario
        const filtroTipo = document.getElementById('filtro-tipo-usuario');
        if (filtroTipo) {
            filtroTipo.addEventListener('change', debounce(() => {
                this.filtros.tipoUsuario = filtroTipo.value;
                this.aplicarFiltros();
            }, CONFIG.DEBOUNCE_DELAY));
        }
        
        // Botón de actualización manual
        const btnRefresh = document.querySelector('.refresh-btn');
        if (btnRefresh) {
            btnRefresh.addEventListener('click', () => this.cargarDatosIniciales());
        }
    }
    
    setupAutoRefresh() {
        const checkbox = document.getElementById('auto-refresh');
        if (!checkbox) return;
        
        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                this.autoRefreshInterval = setInterval(() => {
                    this.cargarDatosIniciales();
                    document.getElementById('ultima-actualizacion').textContent = new Date().toLocaleString();
                }, CONFIG.AUTO_REFRESH_INTERVAL);
            } else {
                clearInterval(this.autoRefreshInterval);
            }
        });
        
        // Iniciar si está checked
        if (checkbox.checked) {
            this.autoRefreshInterval = setInterval(() => {
                this.cargarDatosIniciales();
                document.getElementById('ultima-actualizacion').textContent = new Date().toLocaleString();
            }, CONFIG.AUTO_REFRESH_INTERVAL);
        }
    }
}

// ============================================================================
// INICIALIZACIÓN
// ============================================================================

let monitoreoManager;

document.addEventListener('DOMContentLoaded', async () => {
    monitoreoManager = new MonitoreoManager();
    await monitoreoManager.init();
});

// Función de logout
async function logout() {
    try {
        await APIClient.logout();
    } catch (error) {
        console.error('Error al cerrar sesión:', error);
    } finally {
        localStorage.clear();
        window.location.href = '/auth/login';
    }
}

// Exportar para uso global
window.monitoreoManager = monitoreoManager;
window.logout = logout;
