/**
 * Sistema de Verificación de Presencia
 * Funciona para todos los roles: testigos, coordinadores, auditores
 */

class VerificacionPresencia {
    constructor() {
        this.pingInterval = null;
        this.estadoEquipoInterval = null;
        this.PING_INTERVAL_MS = 5 * 60 * 1000; // 5 minutos
        this.ESTADO_EQUIPO_INTERVAL_MS = 2 * 60 * 1000; // 2 minutos
    }

    /**
     * Inicializar sistema de verificación
     */
    init() {
        console.log('VerificacionPresencia: Inicializando...');
        
        // ⚠️ NO verificar presencia automáticamente
        // La presencia se verifica SOLO cuando el testigo hace clic en "Verificar Presencia"
        // después de seleccionar su mesa
        
        // Iniciar ping automático solo si ya hay presencia verificada
        const presenciaYaVerificada = sessionStorage.getItem('presencia_verificada');
        if (presenciaYaVerificada) {
            console.log('Presencia ya verificada previamente, iniciando ping automático');
            this.iniciarPingAutomatico();
        } else {
            console.log('Presencia no verificada aún, esperando acción del usuario');
        }
        
        // Detectar cuando el usuario vuelve a la pestaña
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden && presenciaYaVerificada) {
                this.ping();
            }
        });
    }

    /**
     * Verificar presencia inicial con geolocalización
     */
    async verificarPresenciaInicial() {
        try {
            // Verificar que hay token antes de continuar
            if (!localStorage.getItem('access_token')) {
                console.log('VerificacionPresencia: No hay token, saltando verificación');
                return;
            }
            
            // Intentar obtener geolocalización
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        this.verificarPresencia(position.coords.latitude, position.coords.longitude);
                    },
                    (error) => {
                        // No mostrar error, solo log
                        console.log('Geolocalización no disponible, continuando sin coordenadas');
                        this.verificarPresencia();
                    },
                    {
                        timeout: 5000,
                        maximumAge: 60000
                    }
                );
            } else {
                this.verificarPresencia();
            }
        } catch (error) {
            console.log('Error en verificación inicial:', error.message);
            // No propagar el error
        }
    }

    /**
     * Verificar presencia del usuario
     */
    async verificarPresencia(latitud = null, longitud = null) {
        try {
            // Verificar que hay token
            const token = localStorage.getItem('access_token');
            if (!token) {
                console.log('VerificacionPresencia: No hay token disponible');
                return null;
            }
            
            const response = await fetch('/api/verificacion/presencia', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    latitud: latitud,
                    longitud: longitud
                })
            });

            const data = await response.json();

            if (data.success) {
                console.log('Presencia verificada:', data.data);
                
                // Marcar presencia como verificada
                sessionStorage.setItem('presencia_verificada', 'true');
                
                // Iniciar ping automático después de verificar presencia
                if (!this.pingInterval) {
                    console.log('Iniciando ping automático después de verificar presencia');
                    this.iniciarPingAutomatico();
                }
                
                // Mostrar notificación
                if (typeof Utils !== 'undefined') {
                    Utils.showSuccess('✅ Presencia verificada exitosamente');
                }
                
                return data.data;
            } else {
                console.log('Error verificando presencia:', data.error);
                return null;
            }
        } catch (error) {
            console.log('Error en verificarPresencia:', error.message);
            return null;
        }
    }

    /**
     * Ping rápido para mantener presencia activa
     */
    async ping() {
        try {
            // Verificar que hay token
            const token = localStorage.getItem('access_token');
            if (!token) {
                console.log('VerificacionPresencia: No hay token para ping');
                return false;
            }
            
            const response = await fetch('/api/verificacion/ping', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();

            if (data.success) {
                console.log('Ping exitoso:', new Date().toLocaleTimeString());
                return true;
            } else {
                console.log('Error en ping:', data.error);
                return false;
            }
        } catch (error) {
            console.log('Error en ping:', error.message);
            return false;
        }
    }

    /**
     * Iniciar ping automático cada 5 minutos
     */
    iniciarPingAutomatico() {
        // Limpiar intervalo anterior si existe
        if (this.pingInterval) {
            clearInterval(this.pingInterval);
        }

        // Iniciar nuevo intervalo
        this.pingInterval = setInterval(() => {
            this.ping();
        }, this.PING_INTERVAL_MS);

        console.log('Ping automático iniciado (cada 5 minutos)');
    }

    /**
     * Detener ping automático
     */
    detenerPingAutomatico() {
        if (this.pingInterval) {
            clearInterval(this.pingInterval);
            this.pingInterval = null;
            console.log('Ping automático detenido');
        }
    }

    /**
     * Obtener estado del equipo bajo supervisión
     */
    async obtenerEstadoEquipo() {
        try {
            const response = await fetch('/api/verificacion/estado-equipo', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            const data = await response.json();

            if (data.success) {
                return data.data;
            } else {
                console.error('Error obteniendo estado del equipo:', data.error);
                return null;
            }
        } catch (error) {
            console.error('Error en obtenerEstadoEquipo:', error);
            return null;
        }
    }

    /**
     * Renderizar estado del equipo en un contenedor
     */
    async renderizarEstadoEquipo(containerId) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error('Contenedor no encontrado:', containerId);
            return;
        }

        try {
            const estadoData = await this.obtenerEstadoEquipo();

            if (!estadoData) {
                container.innerHTML = '<p class="text-muted">No se pudo cargar el estado del equipo</p>';
                return;
            }

            const { equipo, estadisticas } = estadoData;

            // Renderizar estadísticas
            const statsHtml = `
                <div class="row mb-3">
                    <div class="col-md-3">
                        <div class="card bg-light">
                            <div class="card-body text-center">
                                <h6 class="text-muted mb-2">Total</h6>
                                <h3>${estadisticas.total}</h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card bg-success bg-opacity-10">
                            <div class="card-body text-center">
                                <h6 class="text-muted mb-2">Activos</h6>
                                <h3 class="text-success">${estadisticas.presentes}</h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card bg-warning bg-opacity-10">
                            <div class="card-body text-center">
                                <h6 class="text-muted mb-2">Inactivos</h6>
                                <h3 class="text-warning">${estadisticas.inactivos}</h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card bg-danger bg-opacity-10">
                            <div class="card-body text-center">
                                <h6 class="text-muted mb-2">Ausentes</h6>
                                <h3 class="text-danger">${estadisticas.ausentes}</h3>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="progress mb-3" style="height: 30px;">
                    <div class="progress-bar bg-success" style="width: ${estadisticas.porcentaje_presencia}%">
                        ${estadisticas.porcentaje_presencia}% Presencia
                    </div>
                </div>
            `;

            // Renderizar lista del equipo
            const equipoHtml = equipo.map(miembro => {
                const estadoBadge = this.getEstadoBadge(miembro.estado);
                const tiempoInactivo = miembro.minutos_inactivo !== null 
                    ? `${miembro.minutos_inactivo} min` 
                    : 'Nunca';
                
                return `
                    <tr>
                        <td>${miembro.nombre}</td>
                        <td>${miembro.rol}</td>
                        <td>${miembro.ubicacion}</td>
                        <td>${estadoBadge}</td>
                        <td>${tiempoInactivo}</td>
                        <td>
                            ${miembro.ultimo_acceso 
                                ? new Date(miembro.ultimo_acceso).toLocaleString() 
                                : 'Nunca'}
                        </td>
                    </tr>
                `;
            }).join('');

            container.innerHTML = `
                ${statsHtml}
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>Nombre</th>
                                <th>Rol</th>
                                <th>Ubicación</th>
                                <th>Estado</th>
                                <th>Inactivo</th>
                                <th>Último Acceso</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${equipoHtml || '<tr><td colspan="6" class="text-center text-muted">No hay miembros del equipo</td></tr>'}
                        </tbody>
                    </table>
                </div>
            `;

        } catch (error) {
            console.error('Error renderizando estado del equipo:', error);
            container.innerHTML = '<p class="text-danger">Error al cargar el estado del equipo</p>';
        }
    }

    /**
     * Obtener badge de estado
     */
    getEstadoBadge(estado) {
        const badges = {
            'activo': '<span class="badge bg-success"><i class="bi bi-check-circle"></i> Activo</span>',
            'inactivo': '<span class="badge bg-warning"><i class="bi bi-clock"></i> Inactivo</span>',
            'ausente': '<span class="badge bg-danger"><i class="bi bi-x-circle"></i> Ausente</span>'
        };
        return badges[estado] || '<span class="badge bg-secondary">Desconocido</span>';
    }

    /**
     * Iniciar actualización automática del estado del equipo
     */
    iniciarActualizacionEstadoEquipo(containerId) {
        // Renderizar inmediatamente
        this.renderizarEstadoEquipo(containerId);

        // Limpiar intervalo anterior si existe
        if (this.estadoEquipoInterval) {
            clearInterval(this.estadoEquipoInterval);
        }

        // Iniciar nuevo intervalo
        this.estadoEquipoInterval = setInterval(() => {
            this.renderizarEstadoEquipo(containerId);
        }, this.ESTADO_EQUIPO_INTERVAL_MS);

        console.log('Actualización automática del estado del equipo iniciada (cada 2 minutos)');
    }

    /**
     * Detener actualización automática del estado del equipo
     */
    detenerActualizacionEstadoEquipo() {
        if (this.estadoEquipoInterval) {
            clearInterval(this.estadoEquipoInterval);
            this.estadoEquipoInterval = null;
            console.log('Actualización automática del estado del equipo detenida');
        }
    }

    /**
     * Destruir instancia y limpiar intervalos
     */
    destroy() {
        this.detenerPingAutomatico();
        this.detenerActualizacionEstadoEquipo();
        console.log('VerificacionPresencia: Destruido');
    }
}

// Crear instancia global
window.verificacionPresencia = new VerificacionPresencia();
