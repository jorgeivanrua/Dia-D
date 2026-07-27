/**
 * Mapa Mejorado para Coordinador Municipal
 * Incluye: filtros, marcadores informativos, alertas en tiempo real
 */

class MapaCoordinadorMunicipal {
    constructor(containerId) {
        this.containerId = containerId;
        this.map = null;
        this.markers = {
            puestos: [],
            coordinadores: [],
            testigos: [],
            incidentes: [],
            delitos: []
        };
        this.layerGroups = {
            puestos: null,
            coordinadores: null,
            testigos: null,
            incidentes: null,
            delitos: null
        };
        this.filtros = {
            zona: '',
            estado: '',
            mostrarCoordinadores: true,
            mostrarTestigos: true,
            mostrarIncidentes: true,
            mostrarDelitos: true
        };
        this.autoRefreshInterval = null;
    }

    /**
     * Inicializar mapa
     */
    async init() {
        try {
            console.log('[Mapa Municipal] Inicializando...');
            
            // Crear mapa
            this.map = L.map(this.containerId).setView([1.6144, -75.6062], 12);
            
            // Agregar capa base
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors',
                maxZoom: 19
            }).addTo(this.map);
            
            // Crear layer groups
            this.layerGroups.puestos = L.layerGroup().addTo(this.map);
            this.layerGroups.coordinadores = L.layerGroup().addTo(this.map);
            this.layerGroups.testigos = L.layerGroup().addTo(this.map);
            this.layerGroups.incidentes = L.layerGroup().addTo(this.map);
            this.layerGroups.delitos = L.layerGroup().addTo(this.map);
            
            // Cargar datos
            await this.cargarDatos();
            
            // Auto-refresh cada 30 segundos
            this.autoRefreshInterval = setInterval(() => {
                this.cargarDatos();
            }, 30000);
            
            console.log('[Mapa Municipal] Inicializado correctamente');
        } catch (error) {
            console.error('[Mapa Municipal] Error inicializando:', error);
            Utils.showError('Error al inicializar el mapa');
        }
    }

    /**
     * Cargar datos del mapa
     */
    async cargarDatos() {
        try {
            const params = {};
            if (this.filtros.zona) params.zona = this.filtros.zona;
            if (this.filtros.estado) params.estado = this.filtros.estado;
            
            const response = await APIClient.get('/coordinador-municipal/mapa-datos', params);
            
            if (response.success) {
                this.renderizarDatos(response.data);
            } else {
                throw new Error(response.error || 'Error al cargar datos del mapa');
            }
        } catch (error) {
            console.error('[Mapa Municipal] Error cargando datos:', error);
        }
    }

    /**
     * Renderizar datos en el mapa
     */
    renderizarDatos(data) {
        // Limpiar marcadores existentes
        this.limpiarMarcadores();
        
        // Centrar mapa
        if (data.centro) {
            this.map.setView([data.centro.latitud, data.centro.longitud], data.centro.zoom);
        }
        
        // Renderizar puestos
        if (data.puestos) {
            data.puestos.forEach(puesto => {
                if (puesto.latitud && puesto.longitud) {
                    this.agregarMarcadorPuesto(puesto);
                }
            });
        }
        
        // Renderizar coordinadores
        if (data.coordinadores && this.filtros.mostrarCoordinadores) {
            data.coordinadores.forEach(coord => {
                this.agregarMarcadorCoordinador(coord);
            });
        }
        
        // Renderizar testigos
        if (data.testigos && this.filtros.mostrarTestigos) {
            data.testigos.forEach(testigo => {
                this.agregarMarcadorTestigo(testigo);
            });
        }
        
        // Renderizar incidentes
        if (data.incidentes && this.filtros.mostrarIncidentes) {
            data.incidentes.forEach(incidente => {
                this.agregarMarcadorIncidente(incidente);
            });
        }
        
        // Renderizar delitos
        if (data.delitos && this.filtros.mostrarDelitos) {
            data.delitos.forEach(delito => {
                this.agregarMarcadorDelito(delito);
            });
        }
        
        // Actualizar estadísticas
        if (data.estadisticas) {
            this.actualizarEstadisticas(data.estadisticas);
        }
    }

    /**
     * Agregar marcador de puesto
     */
    agregarMarcadorPuesto(puesto) {
        // Color según estado
        const colores = {
            'completo': '#28a745',
            'incompleto': '#ffc107',
            'con_discrepancias': '#dc3545'
        };
        
        const color = colores[puesto.estado] || '#6c757d';
        
        // Icono personalizado
        const icon = L.divIcon({
            className: 'custom-marker-puesto',
            html: `
                <div style="
                    background-color: ${color};
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    border: 3px solid white;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                    font-size: 12px;
                ">
                    ${puesto.tiene_alertas ? '!' : ''}
                </div>
            `,
            iconSize: [30, 30],
            iconAnchor: [15, 15]
        });
        
        // Crear marcador
        const marker = L.marker([puesto.latitud, puesto.longitud], { icon })
            .bindPopup(this.crearPopupPuesto(puesto))
            .addTo(this.layerGroups.puestos);
        
        this.markers.puestos.push(marker);
    }

    /**
     * Crear popup para puesto
     */
    crearPopupPuesto(puesto) {
        const estadoBadge = this.getEstadoBadge(puesto.estado);
        
        return `
            <div class="popup-puesto" style="min-width: 250px;">
                <h6 class="mb-2">
                    <i class="bi bi-building"></i> ${puesto.nombre}
                </h6>
                <p class="mb-1"><small><strong>Código:</strong> ${puesto.codigo}</small></p>
                <p class="mb-1"><small><strong>Zona:</strong> ${puesto.zona_codigo || 'N/A'}</small></p>
                <p class="mb-2"><small><strong>Estado:</strong> ${estadoBadge}</small></p>
                
                <div class="mb-2">
                    <div class="progress" style="height: 20px;">
                        <div class="progress-bar ${puesto.porcentaje_avance >= 100 ? 'bg-success' : 'bg-primary'}" 
                             style="width: ${puesto.porcentaje_avance}%">
                            ${puesto.porcentaje_avance.toFixed(0)}%
                        </div>
                    </div>
                    <small class="text-muted">${puesto.formularios_validados}/${puesto.total_mesas} mesas</small>
                </div>
                
                ${puesto.coordinador ? `
                    <p class="mb-1"><small><strong>Coordinador:</strong> ${puesto.coordinador.nombre}</small></p>
                ` : ''}
                
                ${puesto.incidentes > 0 || puesto.delitos > 0 ? `
                    <div class="alert alert-warning py-1 px-2 mb-2">
                        <small>
                            ${puesto.incidentes > 0 ? `<i class="bi bi-exclamation-triangle"></i> ${puesto.incidentes} incidente(s)` : ''}
                            ${puesto.delitos > 0 ? `<i class="bi bi-shield-exclamation"></i> ${puesto.delitos} delito(s)` : ''}
                        </small>
                    </div>
                ` : ''}
                
                <button class="btn btn-sm btn-primary w-100" onclick="verDetallePuesto(${puesto.id})">
                    <i class="bi bi-eye"></i> Ver Detalles
                </button>
            </div>
        `;
    }

    /**
     * Agregar marcador de coordinador
     */
    agregarMarcadorCoordinador(coord) {
        // Color según estado de conexión
        const colores = {
            'activo': '#28a745',
            'inactivo': '#ffc107',
            'ausente': '#6c757d'
        };
        
        const color = colores[coord.estado_conexion] || '#6c757d';
        
        const icon = L.divIcon({
            className: 'custom-marker-coordinador',
            html: `
                <div style="
                    background-color: ${color};
                    width: 24px;
                    height: 24px;
                    border-radius: 50%;
                    border: 2px solid white;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 10px;
                ">
                    <i class="bi bi-person-fill"></i>
                </div>
            `,
            iconSize: [24, 24],
            iconAnchor: [12, 12]
        });
        
        const marker = L.marker([coord.latitud, coord.longitud], { icon })
            .bindPopup(this.crearPopupCoordinador(coord))
            .addTo(this.layerGroups.coordinadores);
        
        this.markers.coordinadores.push(marker);
    }

    /**
     * Crear popup para coordinador
     */
    crearPopupCoordinador(coord) {
        const estadoBadge = {
            'activo': '<span class="badge bg-success">Activo</span>',
            'inactivo': '<span class="badge bg-warning text-dark">Inactivo</span>',
            'ausente': '<span class="badge bg-secondary">Ausente</span>'
        }[coord.estado_conexion] || '';
        
        return `
            <div class="popup-coordinador" style="min-width: 200px;">
                <h6 class="mb-2">
                    <i class="bi bi-person-badge"></i> ${coord.nombre}
                </h6>
                <p class="mb-1"><small><strong>Rol:</strong> Coordinador de Puesto</small></p>
                <p class="mb-1"><small><strong>Puesto:</strong> ${coord.puesto.nombre}</small></p>
                <p class="mb-2"><small><strong>Estado:</strong> ${estadoBadge}</small></p>
                ${coord.ultima_actualizacion ? `
                    <p class="mb-0"><small class="text-muted">Última actualización: ${Utils.formatDate(coord.ultima_actualizacion)}</small></p>
                ` : ''}
            </div>
        `;
    }

    /**
     * Agregar marcador de testigo
     */
    agregarMarcadorTestigo(testigo) {
        const color = testigo.presencia_verificada ? '#17a2b8' : '#6c757d';
        
        const icon = L.divIcon({
            className: 'custom-marker-testigo',
            html: `
                <div style="
                    background-color: ${color};
                    width: 20px;
                    height: 20px;
                    border-radius: 50%;
                    border: 2px solid white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                "></div>
            `,
            iconSize: [20, 20],
            iconAnchor: [10, 10]
        });
        
        const marker = L.marker([testigo.latitud, testigo.longitud], { icon })
            .bindPopup(this.crearPopupTestigo(testigo))
            .addTo(this.layerGroups.testigos);
        
        this.markers.testigos.push(marker);
    }

    /**
     * Crear popup para testigo
     */
    crearPopupTestigo(testigo) {
        return `
            <div class="popup-testigo" style="min-width: 180px;">
                <h6 class="mb-2">
                    <i class="bi bi-person"></i> ${testigo.nombre}
                </h6>
                <p class="mb-1"><small><strong>Rol:</strong> Testigo Electoral</small></p>
                <p class="mb-1"><small><strong>Puesto:</strong> ${testigo.puesto.nombre}</small></p>
                <p class="mb-2">
                    <small><strong>Presencia:</strong> 
                        ${testigo.presencia_verificada ? 
                            '<span class="badge bg-success">Verificada</span>' : 
                            '<span class="badge bg-secondary">No verificada</span>'}
                    </small>
                </p>
            </div>
        `;
    }

    /**
     * Agregar marcador de incidente
     */
    agregarMarcadorIncidente(incidente) {
        const colores = {
            'baja': '#ffc107',
            'media': '#fd7e14',
            'alta': '#dc3545',
            'critica': '#721c24'
        };
        
        const color = colores[incidente.severidad] || '#ffc107';
        
        const icon = L.divIcon({
            className: 'custom-marker-incidente',
            html: `
                <div style="
                    background-color: ${color};
                    width: 26px;
                    height: 26px;
                    border-radius: 4px;
                    border: 2px solid white;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 14px;
                ">
                    <i class="bi bi-exclamation-triangle-fill"></i>
                </div>
            `,
            iconSize: [26, 26],
            iconAnchor: [13, 13]
        });
        
        const marker = L.marker([incidente.latitud, incidente.longitud], { icon })
            .bindPopup(this.crearPopupIncidente(incidente))
            .addTo(this.layerGroups.incidentes);
        
        this.markers.incidentes.push(marker);
    }

    /**
     * Crear popup para incidente
     */
    crearPopupIncidente(incidente) {
        const severidadBadge = {
            'baja': '<span class="badge bg-warning text-dark">Baja</span>',
            'media': '<span class="badge bg-warning">Media</span>',
            'alta': '<span class="badge bg-danger">Alta</span>',
            'critica': '<span class="badge bg-danger">Crítica</span>'
        }[incidente.severidad] || '';
        
        return `
            <div class="popup-incidente" style="min-width: 220px;">
                <h6 class="mb-2">
                    <i class="bi bi-exclamation-triangle"></i> Incidente
                </h6>
                <p class="mb-1"><small><strong>Tipo:</strong> ${incidente.tipo_incidente}</small></p>
                <p class="mb-1"><small><strong>Severidad:</strong> ${severidadBadge}</small></p>
                <p class="mb-1"><small><strong>Puesto:</strong> ${incidente.puesto.nombre}</small></p>
                <p class="mb-2"><small>${incidente.descripcion}</small></p>
                <p class="mb-0"><small class="text-muted">${Utils.formatDate(incidente.fecha_reporte)}</small></p>
            </div>
        `;
    }

    /**
     * Agregar marcador de delito
     */
    agregarMarcadorDelito(delito) {
        const icon = L.divIcon({
            className: 'custom-marker-delito',
            html: `
                <div style="
                    background-color: #721c24;
                    width: 28px;
                    height: 28px;
                    border-radius: 4px;
                    border: 2px solid white;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 14px;
                ">
                    <i class="bi bi-shield-exclamation"></i>
                </div>
            `,
            iconSize: [28, 28],
            iconAnchor: [14, 14]
        });
        
        const marker = L.marker([delito.latitud, delito.longitud], { icon })
            .bindPopup(this.crearPopupDelito(delito))
            .addTo(this.layerGroups.delitos);
        
        this.markers.delitos.push(marker);
    }

    /**
     * Crear popup para delito
     */
    crearPopupDelito(delito) {
        const gravedadBadge = {
            'leve': '<span class="badge bg-warning text-dark">Leve</span>',
            'grave': '<span class="badge bg-danger">Grave</span>',
            'muy_grave': '<span class="badge bg-danger">Muy Grave</span>'
        }[delito.gravedad] || '';
        
        return `
            <div class="popup-delito" style="min-width: 220px;">
                <h6 class="mb-2">
                    <i class="bi bi-shield-exclamation"></i> Delito Electoral
                </h6>
                <p class="mb-1"><small><strong>Tipo:</strong> ${delito.tipo_delito}</small></p>
                <p class="mb-1"><small><strong>Gravedad:</strong> ${gravedadBadge}</small></p>
                <p class="mb-1"><small><strong>Puesto:</strong> ${delito.puesto.nombre}</small></p>
                <p class="mb-2"><small>${delito.descripcion}</small></p>
                <p class="mb-0"><small class="text-muted">${Utils.formatDate(delito.fecha_reporte)}</small></p>
            </div>
        `;
    }

    /**
     * Limpiar marcadores
     */
    limpiarMarcadores() {
        Object.keys(this.layerGroups).forEach(key => {
            if (this.layerGroups[key]) {
                this.layerGroups[key].clearLayers();
            }
        });
        
        Object.keys(this.markers).forEach(key => {
            this.markers[key] = [];
        });
    }

    /**
     * Aplicar filtros
     */
    aplicarFiltros(filtros) {
        this.filtros = { ...this.filtros, ...filtros };
        
        // Mostrar/ocultar layers
        if (this.filtros.mostrarCoordinadores) {
            this.layerGroups.coordinadores.addTo(this.map);
        } else {
            this.map.removeLayer(this.layerGroups.coordinadores);
        }
        
        if (this.filtros.mostrarTestigos) {
            this.layerGroups.testigos.addTo(this.map);
        } else {
            this.map.removeLayer(this.layerGroups.testigos);
        }
        
        if (this.filtros.mostrarIncidentes) {
            this.layerGroups.incidentes.addTo(this.map);
        } else {
            this.map.removeLayer(this.layerGroups.incidentes);
        }
        
        if (this.filtros.mostrarDelitos) {
            this.layerGroups.delitos.addTo(this.map);
        } else {
            this.map.removeLayer(this.layerGroups.delitos);
        }
        
        // Recargar datos con nuevos filtros
        this.cargarDatos();
    }

    /**
     * Obtener badge de estado
     */
    getEstadoBadge(estado) {
        const badges = {
            'completo': '<span class="badge bg-success">Completo</span>',
            'incompleto': '<span class="badge bg-warning text-dark">Incompleto</span>',
            'con_discrepancias': '<span class="badge bg-danger">Con Discrepancias</span>'
        };
        return badges[estado] || `<span class="badge bg-secondary">${estado}</span>`;
    }

    /**
     * Actualizar estadísticas
     */
    actualizarEstadisticas(stats) {
        // Actualizar badges en el mapa
        const badge = document.getElementById('usuarios-activos-badge');
        if (badge) {
            const total = stats.coordinadores_activos + stats.testigos_activos;
            badge.textContent = `${total} usuarios activos`;
        }
    }

    /**
     * Destruir mapa
     */
    destroy() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
        }
        
        if (this.map) {
            this.map.remove();
        }
    }
}

// Función global para ver detalle de puesto
function verDetallePuesto(puestoId) {
    if (typeof seleccionarPuesto === 'function') {
        seleccionarPuesto(puestoId);
        
        // Cambiar a tab de puestos
        const puestosTab = document.getElementById('puestos-tab');
        if (puestosTab) {
            puestosTab.click();
        }
    }
}
