/**
 * Sistema de Geolocalización y Mapas
 * Visualización en tiempo real de usuarios y puestos de votación
 */

class MapaGeolocalizacion {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.map = null;
        this.markers = {};
        this.puestosData = []; // Almacenar datos de puestos para filtrado
        this.filtrosActivos = {
            testigos: true,
            coordinadores: true,
            incidentes: false,
            delitos: false,
            pendientes: false,
            completados: false
        };
        this.options = {
            center: options.center || [4.5709, -74.2973], // Bogotá por defecto
            zoom: options.zoom || 6,
            autoUpdate: options.autoUpdate !== false,
            updateInterval: options.updateInterval || 30000, // 30 segundos
            showPuestos: options.showPuestos !== false,
            showUsuarios: options.showUsuarios !== false
        };
        this.updateInterval = null;
    }

    /**
     * Inicializar mapa
     */
    async init() {
        try {
            const container = document.getElementById(this.containerId);
            if (!container) {
                console.error('Contenedor del mapa no encontrado:', this.containerId);
                return false;
            }

            // Crear mapa con Leaflet
            this.map = L.map(this.containerId).setView(this.options.center, this.options.zoom);

            // Agregar capa de OpenStreetMap
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors',
                maxZoom: 19
            }).addTo(this.map);

            // Cargar datos iniciales
            await this.cargarDatos();

            // Iniciar actualización automática
            if (this.options.autoUpdate) {
                this.iniciarActualizacionAutomatica();
            }

            console.log('Mapa inicializado correctamente');
            return true;

        } catch (error) {
            console.error('Error inicializando mapa:', error);
            return false;
        }
    }

    /**
     * Cargar datos de puestos y usuarios
     */
    async cargarDatos() {
        try {
            // Cargar puestos de votación
            if (this.options.showPuestos) {
                await this.cargarPuestos();
            }

            // Cargar usuarios geolocalizados
            if (this.options.showUsuarios) {
                await this.cargarUsuarios();
            }

        } catch (error) {
            console.error('Error cargando datos:', error);
        }
    }

    /**
     * Cargar puestos de votación
     */
    async cargarPuestos() {
        try {
            const response = await fetch('/api/locations/puestos-geolocalizados', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            const data = await response.json();

            if (data.success && data.data) {
                // Almacenar datos para filtrado
                this.puestosData = data.data.filter(puesto => puesto.latitud && puesto.longitud);
                
                // Aplicar filtros y mostrar markers
                this.aplicarFiltros();
            }

        } catch (error) {
            console.error('Error cargando puestos:', error);
        }
    }

    /**
     * Cargar usuarios geolocalizados
     */
    async cargarUsuarios() {
        try {
            const response = await fetch('/api/verificacion/usuarios-geolocalizados', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            const data = await response.json();

            if (data.success && data.data) {
                data.data.forEach(usuario => {
                    if (usuario.latitud && usuario.longitud) {
                        this.agregarMarkerUsuario(usuario);
                    }
                });
            }

        } catch (error) {
            console.error('Error cargando usuarios:', error);
        }
    }

    /**
     * Agregar marker de puesto de votación
     */
    agregarMarkerPuesto(puesto) {
        const markerId = `puesto_${puesto.id}`;

        // Eliminar marker anterior si existe
        if (this.markers[markerId]) {
            this.map.removeLayer(this.markers[markerId]);
        }

        // Determinar color según porcentaje de avance
        const porcentaje = puesto.porcentaje_avance || 0;
        let colorPuesto = '#dc3545'; // Rojo por defecto (0%)
        let estadoTexto = 'Sin votos';
        
        if (porcentaje >= 100) {
            colorPuesto = '#28a745'; // Verde - completado
            estadoTexto = 'Completado';
        } else if (porcentaje > 0) {
            colorPuesto = '#ffc107'; // Amarillo - en progreso
            estadoTexto = 'En progreso';
        }

        // Determinar si hay alertas
        const tieneAlertas = puesto.tiene_alertas || false;
        const tieneAlertasCriticas = puesto.tiene_alertas_criticas || false;
        
        // Icono de alerta si hay incidentes o delitos
        let iconoAlerta = '';
        if (tieneAlertasCriticas) {
            iconoAlerta = '<span class="alerta-critica" title="¡Alerta Crítica!">⚠️</span>';
        } else if (tieneAlertas) {
            iconoAlerta = '<span class="alerta-normal" title="Alerta">⚠️</span>';
        }

        // Icono personalizado para puestos con número de mesa y alerta
        const iconoPuesto = L.divIcon({
            className: 'custom-marker-puesto',
            html: `
                <div class="marker-pin-puesto" style="background-color: ${colorPuesto};">
                    <span class="mesa-numero">${puesto.puesto_codigo || ''}</span>
                </div>
                ${iconoAlerta}
            `,
            iconSize: [30, 40],
            iconAnchor: [15, 40],
            popupAnchor: [0, -40]
        });

        // Crear marker
        const marker = L.marker([puesto.latitud, puesto.longitud], {
            icon: iconoPuesto,
            title: puesto.nombre_completo
        });

        // Construir sección de alertas si existen
        let seccionAlertas = '';
        if (tieneAlertas) {
            const incidentesActivos = (puesto.incidentes && puesto.incidentes.total) || 0;
            const incidentesCriticos = (puesto.incidentes && puesto.incidentes.criticos) || 0;
            const delitosActivos = (puesto.delitos && puesto.delitos.total) || 0;
            const delitosGraves = (puesto.delitos && puesto.delitos.graves) || 0;
            
            seccionAlertas = '<hr style="margin: 8px 0;">';
            seccionAlertas += '<div class="alertas-section">';
            
            if (incidentesActivos > 0) {
                const badgeClass = incidentesCriticos > 0 ? 'bg-danger' : 'bg-warning';
                seccionAlertas += `<p class="mb-1"><strong>⚠️ Incidentes:</strong> <span class="badge ${badgeClass}">${incidentesActivos}</span>`;
                if (incidentesCriticos > 0) {
                    seccionAlertas += ` <span class="badge bg-danger">¡${incidentesCriticos} críticos!</span>`;
                }
                seccionAlertas += '</p>';
            }
            
            if (delitosActivos > 0) {
                const badgeClass = delitosGraves > 0 ? 'bg-danger' : 'bg-warning';
                seccionAlertas += `<p class="mb-1"><strong>🚨 Delitos:</strong> <span class="badge ${badgeClass}">${delitosActivos}</span>`;
                if (delitosGraves > 0) {
                    seccionAlertas += ` <span class="badge bg-danger">¡${delitosGraves} graves!</span>`;
                }
                seccionAlertas += '</p>';
            }
            
            seccionAlertas += '</div>';
        }
        
        // Popup con información mejorada
        const popupContent = `
            <div class="marker-popup">
                <h6><i class="bi bi-building"></i> ${puesto.puesto_nombre || 'Puesto'}</h6>
                <p class="mb-1"><strong>📍 Código:</strong> ${puesto.puesto_codigo}</p>
                <p class="mb-1"><strong>🏛️ Municipio:</strong> ${puesto.municipio_nombre}</p>
                <p class="mb-1"><strong>🗺️ Departamento:</strong> ${puesto.departamento_nombre}</p>
                ${puesto.direccion ? `<p class="mb-1"><strong>📫 Dirección:</strong> ${puesto.direccion}</p>` : ''}
                <hr style="margin: 8px 0;">
                <p class="mb-1"><strong>🗳️ Total Mesas:</strong> ${puesto.total_mesas || 0}</p>
                <p class="mb-1"><strong>📋 E-14 Recibidos:</strong> ${puesto.total_formularios || 0}</p>
                <p class="mb-1"><strong>✅ E-14 Validados:</strong> ${puesto.formularios_validados || 0} / ${puesto.total_mesas || 0}</p>
                <p class="mb-1">
                    <strong>📊 Avance:</strong> 
                    <span class="badge" style="background-color: ${colorPuesto};">${porcentaje.toFixed(1)}%</span>
                    <span class="badge bg-secondary">${estadoTexto}</span>
                </p>
                <div class="progress mt-2" style="height: 8px;">
                    <div class="progress-bar" style="width: ${porcentaje}%; background-color: ${colorPuesto};"></div>
                </div>
                ${seccionAlertas}
            </div>
        `;

        marker.bindPopup(popupContent);
        marker.addTo(this.map);

        this.markers[markerId] = marker;
    }

    /**
     * Agregar marker de usuario
     */
    agregarMarkerUsuario(usuario) {
        const markerId = `usuario_${usuario.id}`;

        // Eliminar marker anterior si existe
        if (this.markers[markerId]) {
            this.map.removeLayer(this.markers[markerId]);
        }

        // Aplicar filtros de testigos y coordinadores
        const esTestigo = usuario.rol === 'testigo_electoral';
        const esCoordinador = usuario.rol && usuario.rol.includes('coordinador');
        
        // Si el filtro de testigos está desactivado y es testigo, no mostrar
        if (esTestigo && !this.filtrosActivos.testigos) {
            return;
        }
        
        // Si el filtro de coordinadores está desactivado y es coordinador, no mostrar
        if (esCoordinador && !this.filtrosActivos.coordinadores) {
            return;
        }

        // Determinar color según estado
        const colorEstado = this.getColorEstado(usuario.estado);
        const iconoRol = this.getIconoRol(usuario.rol);

        // Icono personalizado para usuarios
        const iconoUsuario = L.divIcon({
            className: 'custom-marker-usuario',
            html: `<div class="marker-pin marker-usuario marker-${usuario.estado}"><i class="bi ${iconoRol}"></i></div>`,
            iconSize: [30, 42],
            iconAnchor: [15, 42],
            popupAnchor: [0, -42]
        });

        // Crear marker
        const marker = L.marker([usuario.latitud, usuario.longitud], {
            icon: iconoUsuario,
            title: usuario.nombre
        });

        // Popup con información
        const estadoBadge = this.getEstadoBadge(usuario.estado);
        const tiempoInactivo = usuario.minutos_inactivo !== null 
            ? `${usuario.minutos_inactivo} min` 
            : 'Nunca';

        const popupContent = `
            <div class="marker-popup">
                <h6><i class="bi ${iconoRol}"></i> ${usuario.nombre}</h6>
                <p class="mb-1"><strong>Rol:</strong> ${this.formatearRol(usuario.rol)}</p>
                <p class="mb-1"><strong>Estado:</strong> ${estadoBadge}</p>
                <p class="mb-1"><strong>Inactivo:</strong> ${tiempoInactivo}</p>
                ${usuario.ubicacion_nombre ? `<p class="mb-1"><strong>Ubicación:</strong> ${usuario.ubicacion_nombre}</p>` : ''}
                <p class="mb-0"><strong>Última actualización:</strong><br>${new Date(usuario.ultima_geolocalizacion_at).toLocaleString()}</p>
            </div>
        `;

        marker.bindPopup(popupContent);
        marker.addTo(this.map);

        this.markers[markerId] = marker;
    }

    /**
     * Obtener color según estado
     */
    getColorEstado(estado) {
        const colores = {
            'activo': '#28a745',
            'inactivo': '#ffc107',
            'ausente': '#dc3545'
        };
        return colores[estado] || '#6c757d';
    }

    /**
     * Obtener icono según rol
     */
    getIconoRol(rol) {
        const iconos = {
            'testigo_electoral': 'bi-person-check',
            'coordinador_puesto': 'bi-person-badge',
            'coordinador_municipal': 'bi-person-workspace',
            'coordinador_departamental': 'bi-person-gear',
            'auditor_electoral': 'bi-shield-check',
            'super_admin': 'bi-star'
        };
        return iconos[rol] || 'bi-person';
    }

    /**
     * Formatear nombre del rol
     */
    formatearRol(rol) {
        const roles = {
            'testigo_electoral': 'Testigo Electoral',
            'coordinador_puesto': 'Coordinador de Puesto',
            'coordinador_municipal': 'Coordinador Municipal',
            'coordinador_departamental': 'Coordinador Departamental',
            'auditor_electoral': 'Auditor Electoral',
            'super_admin': 'Super Admin'
        };
        return roles[rol] || rol;
    }

    /**
     * Obtener badge de estado
     */
    getEstadoBadge(estado) {
        const badges = {
            'activo': '<span class="badge bg-success">Activo</span>',
            'inactivo': '<span class="badge bg-warning">Inactivo</span>',
            'ausente': '<span class="badge bg-danger">Ausente</span>'
        };
        return badges[estado] || '<span class="badge bg-secondary">Desconocido</span>';
    }

    /**
     * Centrar mapa en una ubicación
     */
    centrarEn(latitud, longitud, zoom = 15) {
        if (this.map) {
            this.map.setView([latitud, longitud], zoom);
        }
    }

    /**
     * Ajustar vista para mostrar todos los markers
     */
    ajustarVista() {
        if (this.map && Object.keys(this.markers).length > 0) {
            const group = L.featureGroup(Object.values(this.markers));
            this.map.fitBounds(group.getBounds().pad(0.1));
        }
    }

    /**
     * Iniciar actualización automática
     */
    iniciarActualizacionAutomatica() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }

        this.updateInterval = setInterval(() => {
            this.actualizar();
        }, this.options.updateInterval);

        console.log(`Actualización automática del mapa iniciada (cada ${this.options.updateInterval / 1000}s)`);
    }

    /**
     * Detener actualización automática
     */
    detenerActualizacionAutomatica() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
            console.log('Actualización automática del mapa detenida');
        }
    }

    /**
     * Actualizar datos del mapa
     */
    async actualizar() {
        try {
            await this.cargarDatos();
            console.log('Mapa actualizado:', new Date().toLocaleTimeString());
        } catch (error) {
            console.error('Error actualizando mapa:', error);
        }
    }

    /**
     * Limpiar todos los markers
     */
    limpiarMarkers() {
        Object.values(this.markers).forEach(marker => {
            this.map.removeLayer(marker);
        });
        this.markers = {};
    }

    /**
     * Aplicar filtros a los puestos
     */
    aplicarFiltros() {
        // Limpiar markers de puestos existentes
        Object.keys(this.markers).forEach(markerId => {
            if (markerId.startsWith('puesto_')) {
                this.map.removeLayer(this.markers[markerId]);
                delete this.markers[markerId];
            }
        });

        // Filtrar puestos según criterios activos
        let puestosFiltrados = this.puestosData;

        // Si no hay filtros activos, mostrar todos
        const hayFiltrosActivos = Object.values(this.filtrosActivos).some(f => f);
        
        if (hayFiltrosActivos) {
            puestosFiltrados = this.puestosData.filter(puesto => {
                let cumpleFiltros = true;

                // Filtro de incidentes (lógica AND)
                if (this.filtrosActivos.incidentes) {
                    cumpleFiltros = cumpleFiltros && (puesto.incidentes_activos > 0);
                }

                // Filtro de delitos (lógica AND)
                if (this.filtrosActivos.delitos) {
                    cumpleFiltros = cumpleFiltros && (puesto.delitos_activos > 0);
                }

                // Filtro de pendientes (lógica AND)
                if (this.filtrosActivos.pendientes) {
                    const pendientes = (puesto.total_mesas || 0) - (puesto.formularios_validados || 0);
                    cumpleFiltros = cumpleFiltros && (pendientes > 0);
                }

                // Filtro de completados (lógica AND)
                if (this.filtrosActivos.completados) {
                    cumpleFiltros = cumpleFiltros && (puesto.porcentaje_avance >= 100);
                }

                return cumpleFiltros;
            });
        }

        // Agregar markers de puestos filtrados
        puestosFiltrados.forEach(puesto => {
            this.agregarMarkerPuesto(puesto);
        });

        // Actualizar contador si existe
        this.actualizarContadorPuestos(puestosFiltrados.length, this.puestosData.length);

        console.log(`Filtros aplicados: ${puestosFiltrados.length} de ${this.puestosData.length} puestos mostrados`);
    }

    /**
     * Activar/desactivar filtro
     */
    toggleFiltro(tipoFiltro) {
        if (this.filtrosActivos.hasOwnProperty(tipoFiltro)) {
            this.filtrosActivos[tipoFiltro] = !this.filtrosActivos[tipoFiltro];
            this.aplicarFiltros();
            return this.filtrosActivos[tipoFiltro];
        }
        return false;
    }

    /**
     * Establecer estado de un filtro
     */
    setFiltro(tipoFiltro, activo) {
        if (this.filtrosActivos.hasOwnProperty(tipoFiltro)) {
            this.filtrosActivos[tipoFiltro] = activo;
            this.aplicarFiltros();
        }
    }

    /**
     * Limpiar todos los filtros
     */
    limpiarFiltros() {
        this.filtrosActivos = {
            testigos: true,
            coordinadores: true,
            incidentes: false,
            delitos: false,
            pendientes: false,
            completados: false
        };
        this.aplicarFiltros();
    }

    /**
     * Obtener estado de filtros
     */
    getFiltrosActivos() {
        return { ...this.filtrosActivos };
    }

    /**
     * Actualizar contador de puestos visibles
     */
    actualizarContadorPuestos(visibles, total) {
        const contadorElement = document.getElementById('contador-puestos-visibles');
        if (contadorElement) {
            contadorElement.textContent = `Mostrando ${visibles} de ${total} puestos`;
        }
    }

    /**
     * Buscar puesto por código, municipio o mesa
     */
    async buscarPuesto(termino) {
        if (!termino || termino.trim() === '') {
            return { success: false, message: 'Ingrese un término de búsqueda' };
        }

        const terminoLower = termino.toLowerCase().trim();
        
        // Buscar en los datos cargados
        const resultados = this.puestosData.filter(puesto => {
            const codigoPuesto = (puesto.puesto_codigo || '').toLowerCase();
            const municipio = (puesto.municipio_nombre || '').toLowerCase();
            const nombrePuesto = (puesto.puesto_nombre || '').toLowerCase();
            
            return codigoPuesto.includes(terminoLower) ||
                   municipio.includes(terminoLower) ||
                   nombrePuesto.includes(terminoLower);
        });

        if (resultados.length === 0) {
            return { 
                success: false, 
                message: 'No se encontraron puestos con ese criterio de búsqueda' 
            };
        }

        // Si hay un solo resultado, centrar en él
        if (resultados.length === 1) {
            const puesto = resultados[0];
            this.centrarEn(puesto.latitud, puesto.longitud, 16);
            this.resaltarMarker(`puesto_${puesto.id}`);
            
            return {
                success: true,
                message: `Puesto encontrado: ${puesto.puesto_nombre}`,
                resultados: resultados
            };
        }

        // Si hay múltiples resultados, ajustar vista para mostrarlos todos
        const bounds = L.latLngBounds(resultados.map(p => [p.latitud, p.longitud]));
        this.map.fitBounds(bounds.pad(0.1));

        return {
            success: true,
            message: `Se encontraron ${resultados.length} puestos`,
            resultados: resultados
        };
    }

    /**
     * Resaltar un marker temporalmente
     */
    resaltarMarker(markerId, duracion = 3000) {
        const marker = this.markers[markerId];
        if (marker) {
            // Abrir popup
            marker.openPopup();
            
            // Agregar clase de resaltado si es posible
            const markerElement = marker.getElement();
            if (markerElement) {
                markerElement.classList.add('marker-resaltado');
                
                // Remover clase después de la duración
                setTimeout(() => {
                    markerElement.classList.remove('marker-resaltado');
                }, duracion);
            }
        }
    }

    /**
     * Destruir mapa
     */
    destroy() {
        this.detenerActualizacionAutomatica();
        if (this.map) {
            this.map.remove();
            this.map = null;
        }
        this.markers = {};
        this.puestosData = [];
        console.log('Mapa destruido');
    }
}

// Estilos CSS para los markers personalizados
const estilosMarkers = `
<style>
.custom-marker-puesto, .custom-marker-usuario {
    background: transparent;
    border: none;
}

.marker-pin {
    width: 30px;
    height: 42px;
    border-radius: 50% 50% 50% 0;
    position: relative;
    transform: rotate(-45deg);
    display: flex;
    align-items: center;
    justify-content: center;
}

.marker-pin i {
    transform: rotate(45deg);
    font-size: 16px;
    color: white;
}

.marker-pin-puesto {
    width: 30px;
    height: 40px;
    border-radius: 15px 15px 15px 0;
    position: relative;
    transform: rotate(-45deg);
    display: flex;
    align-items: center;
    justify-content: center;
    border: 3px solid white;
    box-shadow: 0 3px 8px rgba(0,0,0,0.4);
    cursor: pointer;
    transition: transform 0.2s;
}

.marker-pin-puesto:hover {
    transform: rotate(-45deg) scale(1.1);
}

.marker-pin-puesto .mesa-numero {
    transform: rotate(45deg);
    font-size: 11px;
    font-weight: bold;
    color: white;
    text-shadow: 0 1px 2px rgba(0,0,0,0.5);
}

.custom-marker-puesto .alerta-critica {
    position: absolute;
    top: -8px;
    right: -8px;
    font-size: 18px;
    animation: pulse-alert 1.5s infinite;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));
    z-index: 1000;
}

.custom-marker-puesto .alerta-normal {
    position: absolute;
    top: -8px;
    right: -8px;
    font-size: 16px;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));
    z-index: 1000;
}

@keyframes pulse-alert {
    0%, 100% {
        transform: scale(1);
        opacity: 1;
    }
    50% {
        transform: scale(1.2);
        opacity: 0.8;
    }
}

.marker-popup .alertas-section {
    background-color: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 8px;
    border-radius: 4px;
    margin-top: 8px;
}

.marker-popup .alertas-section p {
    margin-bottom: 4px !important;
}

.marker-puesto {
    background: #007bff;
    border: 3px solid #0056b3;
}

.marker-usuario {
    border: 3px solid rgba(0,0,0,0.2);
}

.marker-usuario.marker-activo {
    background: #28a745;
}

.marker-usuario.marker-inactivo {
    background: #ffc107;
}

.marker-usuario.marker-ausente {
    background: #dc3545;
}

.marker-popup {
    min-width: 250px;
}

.marker-popup h6 {
    margin-bottom: 10px;
    color: #333;
    border-bottom: 2px solid #007bff;
    padding-bottom: 5px;
}

.marker-popup p {
    font-size: 13px;
    color: #666;
}

.marker-popup .progress {
    border-radius: 4px;
    overflow: hidden;
}

.marker-popup .badge {
    font-size: 11px;
    padding: 4px 8px;
}

.marker-resaltado {
    animation: resaltar-marker 1s ease-in-out 3;
}

@keyframes resaltar-marker {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.3);
    }
}
</style>
`;

// Inyectar estilos
if (!document.getElementById('marker-styles')) {
    const styleElement = document.createElement('div');
    styleElement.id = 'marker-styles';
    styleElement.innerHTML = estilosMarkers;
    document.head.appendChild(styleElement);
}
