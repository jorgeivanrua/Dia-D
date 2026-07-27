/**
 * Cliente API para comunicación con el backend
 */
class APIClient {
    static baseURL = '/api';
    
    static getAuthHeaders() {
        const token = localStorage.getItem('access_token');
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        return headers;
    }
    
    static async handleResponse(response) {
        let data;
        
        // Intentar parsear JSON
        try {
            const text = await response.text();
            data = text ? JSON.parse(text) : {};
        } catch (error) {
            console.error('Error parsing response:', error);
            throw new Error(`Error del servidor (${response.status}): No se pudo procesar la respuesta`);
        }
        
        // Manejar errores HTTP
        if (!response.ok) {
            if (response.status === 401) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user_data');
                
                if (window.location.pathname !== '/login' && window.location.pathname !== '/auth/login' && window.location.pathname !== '/') {
                    window.location.href = '/auth/login';
                }
                
                throw new Error(data.error || 'Sesión expirada');
            }
            
            if (response.status === 403) {
                // Error de permisos - probablemente token con rol incorrecto
                console.warn('[APIClient] 403 Forbidden - Posible conflicto de sesión');
                console.warn('  Endpoint:', response.url);
                console.warn('  Error:', data.error);
                
                // No redirigir automáticamente, solo mostrar error
                throw new Error(data.error || 'No tiene permisos para acceder a este recurso');
            }
            
            if (response.status === 404) {
                throw new Error('Endpoint no encontrado. Verifica que el backend esté funcionando correctamente.');
            }
            
            if (response.status === 500) {
                throw new Error(data.error || 'Error interno del servidor');
            }
            
            throw new Error(data.error || `Error ${response.status}: ${response.statusText}`);
        }
        
        // Verificar respuesta exitosa
        if (data.success === false) {
            throw new Error(data.error || 'Error en la petición');
        }
        
        return data;
    }
    
    static async get(endpoint, params = {}) {
        const url = new URL(`${window.location.origin}${this.baseURL}${endpoint}`);
        Object.keys(params).forEach(key => {
            if (params[key] !== null && params[key] !== undefined) {
                url.searchParams.append(key, params[key]);
            }
        });
        
        const response = await fetch(url, {
            method: 'GET',
            headers: this.getAuthHeaders()
        });
        
        return this.handleResponse(response);
    }
    
    static async post(endpoint, data) {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'POST',
            headers: this.getAuthHeaders(),
            body: JSON.stringify(data)
        });
        
        return this.handleResponse(response);
    }
    
    // Métodos específicos de autenticación
    static async login(credentials) {
        return this.post('/auth/login', credentials);
    }
    
    static async logout() {
        return this.post('/auth/logout', {});
    }
    
    static async getProfile() {
        return this.get('/auth/profile');
    }
    
    static async changePassword(passwords) {
        return this.post('/auth/change-password', passwords);
    }
    
    // Métodos de ubicaciones
    static async getDepartamentos() {
        return this.get('/locations/departamentos');
    }
    
    static async getMunicipios(departamentoId) {
        return this.get(`/locations/municipios/${departamentoId}`);
    }
    
    static async getZonas(municipioId) {
        return this.get(`/locations/zonas/${municipioId}`);
    }
    
    static async getPuestos(zonaId) {
        return this.get(`/locations/puestos/${zonaId}`);
    }
    
    static async getMesas(puestoId) {
        // Si params es un objeto, extraer puesto_codigo
        if (typeof puestoId === 'object' && puestoId.puesto_codigo) {
            puestoId = puestoId.puesto_codigo;
        }
        return this.get(`/locations/mesas/${puestoId}`);
    }
    
    // Métodos de configuración electoral (para testigos)
    static async getTiposEleccion() {
        return this.get('/testigo/tipos-eleccion');
    }
    
    static async getPartidos() {
        return this.get('/testigo/partidos');
    }
    
    static async getCandidatos(params = {}) {
        return this.get('/testigo/candidatos', params);
    }
    
    static async getCoaliciones() {
        return this.get('/configuracion/coaliciones');
    }
    
    // Métodos de configuración electoral (para super admin)
    static async getSuperAdminTiposEleccion() {
        return this.get('/super-admin/tipos-eleccion');
    }
    
    static async getSuperAdminPartidos() {
        return this.get('/super-admin/partidos');
    }
    
    static async getSuperAdminCandidatos(params = {}) {
        return this.get('/super-admin/candidatos', params);
    }
    
    static async getSuperAdminStats() {
        return this.get('/super-admin/stats');
    }
    
    static async getSuperAdminUsers(params = {}) {
        return this.get('/super-admin/users', params);
    }
    
    // Métodos de ubicaciones (para super admin)
    static async getSuperAdminMesa(mesaId) {
        return this.get(`/super-admin/locations/mesa/${mesaId}`);
    }
    
    static async updateSuperAdminMesa(mesaId, data) {
        return this.put(`/super-admin/locations/mesa/${mesaId}`, data);
    }
    
    static async createTipoEleccion(data) {
        return this.post('/configuracion/tipos-eleccion', data);
    }
    
    static async createPartido(data) {
        return this.post('/configuracion/partidos', data);
    }
    
    static async createCandidato(data) {
        return this.post('/configuracion/candidatos', data);
    }
    
    static async createCoalicion(data) {
        return this.post('/configuracion/coaliciones', data);
    }
    // ==========================================
    // FORMULARIOS E-14
    // ==========================================
    
    static async getFormulariosE14(params = {}) {
        // Para testigos, usar endpoint específico
        return this.get('/formularios/mis-formularios', params);
    }
    
    static async getFormulariosPuesto(params = {}) {
        // Para coordinadores de puesto
        return this.get('/formularios/puesto', params);
    }
    
    static async getFormularioE14(id) {
        return this.get(`/formularios/${id}`);
    }
    
    static async createFormularioE14(data) {
        return this.post('/formularios', data);
    }
    
    static async updateFormularioE14(id, data) {
        return this.put(`/formularios/${id}`, data);
    }
    
    static async validarFormularioE14(id, cambios = null, comentario = '') {
        return this.put(`/formularios/${id}/validar`, { cambios, comentario });
    }
    
    static async rechazarFormularioE14(id, motivo) {
        return this.put(`/formularios/${id}/rechazar`, { motivo });
    }
    
    static async deleteFormularioE14(id) {
        return this.delete(`/formularios/${id}`);
    }
    
    static async put(endpoint, data) {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'PUT',
            headers: this.getAuthHeaders(),
            body: JSON.stringify(data)
        });
        
        return this.handleResponse(response);
    }
    
    static async delete(endpoint) {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'DELETE',
            headers: this.getAuthHeaders()
        });
        
        return this.handleResponse(response);
    }
    
    // ==================== INCIDENTES Y DELITOS ====================
    
    /**
     * Crear un incidente electoral
     */
    static async crearIncidente(data) {
        return this.post('/incidentes', data);
    }
    
    /**
     * Obtener incidentes con filtros opcionales
     */
    static async obtenerIncidentes(filtros = {}) {
        return this.get('/incidentes', filtros);
    }
    
    /**
     * Obtener detalle de un incidente
     */
    static async obtenerIncidente(id) {
        return this.get(`/incidentes/${id}`);
    }
    
    /**
     * Actualizar estado de un incidente
     */
    static async actualizarEstadoIncidente(id, estado, comentario = null) {
        return this.put(`/incidentes/${id}/estado`, { estado, comentario });
    }
    
    /**
     * Obtener tipos de incidentes disponibles
     */
    static async obtenerTiposIncidentes() {
        return this.get('/incidentes/tipos');
    }
    
    /**
     * Crear un delito electoral
     */
    static async crearDelito(data) {
        return this.post('/delitos', data);
    }
    
    /**
     * Obtener delitos con filtros opcionales
     */
    static async obtenerDelitos(filtros = {}) {
        return this.get('/delitos', filtros);
    }
    
    /**
     * Obtener detalle de un delito
     */
    static async obtenerDelito(id) {
        return this.get(`/delitos/${id}`);
    }
    
    /**
     * Actualizar estado de un delito
     */
    static async actualizarEstadoDelito(id, estado, comentario = null) {
        return this.put(`/delitos/${id}/estado`, { estado, comentario });
    }
    
    /**
     * Denunciar formalmente un delito
     */
    static async denunciarDelito(id, numeroDenuncia, autoridadCompetente) {
        return this.post(`/delitos/${id}/denunciar`, {
            numero_denuncia: numeroDenuncia,
            autoridad_competente: autoridadCompetente
        });
    }
    
    /**
     * Obtener tipos de delitos disponibles
     */
    static async obtenerTiposDelitos() {
        return this.get('/delitos/tipos');
    }
    
    /**
     * Obtener estadísticas de incidentes y delitos
     */
    static async obtenerEstadisticasReportes() {
        return this.get('/reportes/estadisticas');
    }
    
    /**
     * Obtener notificaciones del usuario
     */
    static async obtenerNotificaciones(soloNoLeidas = false) {
        return this.get('/notificaciones', { solo_no_leidas: soloNoLeidas });
    }
    
    /**
     * Marcar notificación como leída
     */
    static async marcarNotificacionLeida(id) {
        return this.put(`/notificaciones/${id}/leer`, {});
    }
    
    // ============================================
    // MÉTODOS ADICIONALES PARA TESTIGOS
    // ============================================
    
    /**
     * Obtener tipos de incidentes
     */
    static async getTiposIncidentes() {
        return this.get('/incidentes/tipos');
    }
    
    /**
     * Obtener tipos de delitos
     */
    static async getTiposDelitos() {
        return this.get('/delitos/tipos');
    }
    
    /**
     * Reportar incidente (alias para testigos)
     */
    static async reportarIncidente(data) {
        return this.crearIncidente(data);
    }
    
    /**
     * Obtener incidentes (alias para testigos)
     */
    static async getIncidentes(params = {}) {
        return this.obtenerIncidentes(params);
    }
    
    /**
     * Obtener incidente por ID (alias para testigos)
     */
    static async getIncidente(id) {
        return this.obtenerIncidente(id);
    }
    
    /**
     * Reportar delito (alias para testigos)
     */
    static async reportarDelito(data) {
        return this.crearDelito(data);
    }
    
    /**
     * Obtener delitos (alias para testigos)
     */
    static async getDelitos(params = {}) {
        return this.obtenerDelitos(params);
    }
    
    /**
     * Obtener delito por ID (alias para testigos)
     */
    static async getDelito(id) {
        return this.obtenerDelito(id);
    }
}

// Exponer APIClient globalmente
window.APIClient = APIClient;
