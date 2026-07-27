/**
 * NotificacionesManager - Gestión de notificaciones en tiempo real
 * 
 * Maneja la conexión WebSocket, recepción de notificaciones,
 * actualización de badge y visualización de toasts.
 */

class NotificacionesManager {
    constructor() {
        this.socket = null;
        this.notificaciones = [];
        this.callbacks = [];
        this.connected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 3000; // 3 segundos
    }

    /**
     * Inicializar y conectar al servidor WebSocket
     */
    async init() {
        try {
            // Cargar Socket.IO desde CDN si no está disponible
            if (typeof io === 'undefined') {
                await this.loadSocketIO();
            }

            // Obtener token de autenticación
            const token = this.getAuthToken();
            if (!token) {
                console.warn('No hay token de autenticación, notificaciones deshabilitadas');
                return;
            }

            // Conectar al servidor
            this.connect(token);

            // Cargar notificaciones existentes
            await this.loadNotificaciones();

        } catch (error) {
            console.error('Error inicializando NotificacionesManager:', error);
        }
    }

    /**
     * Cargar librería Socket.IO desde CDN
     */
    loadSocketIO() {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = 'https://cdn.socket.io/4.5.4/socket.io.min.js';
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    /**
     * Obtener token de autenticación
     */
    getAuthToken() {
        return localStorage.getItem('token') || sessionStorage.getItem('token');
    }

    /**
     * Obtener ID del usuario actual
     */
    getUserId() {
        const userDataStr = localStorage.getItem('userData') || sessionStorage.getItem('userData');
        if (userDataStr) {
            try {
                const userData = JSON.parse(userDataStr);
                return userData.id || userData.user_id;
            } catch (e) {
                console.error('Error parseando userData:', e);
            }
        }
        return null;
    }

    /**
     * Conectar al servidor WebSocket
     */
    connect(token) {
        try {
            // Configurar conexión
            this.socket = io({
                auth: {
                    token: token
                },
                reconnection: true,
                reconnectionDelay: this.reconnectDelay,
                reconnectionAttempts: this.maxReconnectAttempts
            });

            // Event handlers
            this.socket.on('connect', () => this.handleConnect());
            this.socket.on('disconnect', () => this.handleDisconnect());
            this.socket.on('connected', (data) => this.handleConnected(data));
            this.socket.on('nueva_notificacion', (data) => this.handleNuevaNotificacion(data));
            this.socket.on('actualizar_mapa', (data) => this.handleActualizarMapa(data));
            this.socket.on('error', (error) => this.handleError(error));

            console.log('WebSocket configurado');

        } catch (error) {
            console.error('Error conectando WebSocket:', error);
        }
    }

    /**
     * Handler: Conexión establecida
     */
    handleConnect() {
        console.log('✅ Conectado al servidor de notificaciones');
        this.connected = true;
        this.reconnectAttempts = 0;

        // Registrar usuario
        const userId = this.getUserId();
        if (userId) {
            this.socket.emit('register', { user_id: userId });
        }
    }

    /**
     * Handler: Desconexión
     */
    handleDisconnect() {
        console.log('❌ Desconectado del servidor de notificaciones');
        this.connected = false;

        // Intentar reconectar
        this.reconnectAttempts++;
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            console.log(`Reintentando conexión (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
        }
    }

    /**
     * Handler: Confirmación de conexión
     */
    handleConnected(data) {
        console.log('Registrado en servidor:', data);
    }

    /**
     * Handler: Nueva notificación recibida
     */
    handleNuevaNotificacion(notificacion) {
        console.log('📬 Nueva notificación:', notificacion);

        // Agregar a lista local
        this.notificaciones.unshift(notificacion);

        // Actualizar badge
        this.actualizarBadge();

        // Mostrar toast
        this.mostrarToast(notificacion);

        // Notificar a callbacks registrados
        this.callbacks.forEach(callback => {
            try {
                callback(notificacion);
            } catch (error) {
                console.error('Error en callback de notificación:', error);
            }
        });

        // Reproducir sonido (opcional)
        this.reproducirSonido();
    }

    /**
     * Handler: Actualizar mapa
     */
    handleActualizarMapa(data) {
        console.log('🗺️ Actualizar mapa solicitado');

        // Emitir evento personalizado para que el mapa se actualice
        const event = new CustomEvent('mapa-actualizar', { detail: data });
        window.dispatchEvent(event);
    }

    /**
     * Handler: Error
     */
    handleError(error) {
        console.error('Error en WebSocket:', error);
    }

    /**
     * Cargar notificaciones existentes desde el servidor
     */
    async loadNotificaciones() {
        try {
            const token = this.getAuthToken();
            const response = await fetch('/api/notificaciones', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    this.notificaciones = data.notificaciones || [];
                    this.actualizarBadge();
                }
            }
        } catch (error) {
            console.error('Error cargando notificaciones:', error);
        }
    }

    /**
     * Actualizar badge de notificaciones no leídas
     */
    actualizarBadge() {
        const noLeidas = this.notificaciones.filter(n => !n.leida).length;
        
        // Actualizar badge en navbar
        const badge = document.getElementById('notificaciones-badge');
        if (badge) {
            badge.textContent = noLeidas;
            badge.style.display = noLeidas > 0 ? 'inline-block' : 'none';
        }

        // Actualizar título de la página
        if (noLeidas > 0) {
            document.title = `(${noLeidas}) ${this.getOriginalTitle()}`;
        } else {
            document.title = this.getOriginalTitle();
        }
    }

    /**
     * Obtener título original de la página
     */
    getOriginalTitle() {
        const title = document.title;
        // Remover contador si existe
        return title.replace(/^\(\d+\)\s*/, '');
    }

    /**
     * Mostrar toast de notificación
     */
    mostrarToast(notificacion) {
        // Verificar si Toastify está disponible
        if (typeof Toastify === 'undefined') {
            // Fallback: usar alert nativo o crear toast personalizado
            this.mostrarToastPersonalizado(notificacion);
            return;
        }

        // Determinar color según tipo
        let backgroundColor = '#4CAF50'; // Verde por defecto
        if (notificacion.tipo === 'nuevo_incidente') {
            if (notificacion.severidad === 'crítica' || notificacion.severidad === 'critica') {
                backgroundColor = '#f44336'; // Rojo
            } else if (notificacion.severidad === 'alta') {
                backgroundColor = '#ff9800'; // Naranja
            }
        } else if (notificacion.tipo === 'nuevo_delito') {
            backgroundColor = '#9c27b0'; // Púrpura
        }

        // Mostrar toast
        Toastify({
            text: `<strong>${notificacion.titulo}</strong><br>${notificacion.mensaje.substring(0, 100)}...`,
            duration: 5000,
            gravity: 'top',
            position: 'right',
            backgroundColor: backgroundColor,
            stopOnFocus: true,
            escapeMarkup: false,
            onClick: () => {
                this.navegarANotificacion(notificacion);
            }
        }).showToast();
    }

    /**
     * Mostrar toast personalizado (fallback)
     */
    mostrarToastPersonalizado(notificacion) {
        // Crear elemento de toast
        const toast = document.createElement('div');
        toast.className = 'notificacion-toast';
        toast.innerHTML = `
            <div class="notificacion-toast-content">
                <strong>${notificacion.titulo}</strong>
                <p>${notificacion.mensaje.substring(0, 100)}...</p>
            </div>
        `;

        // Agregar estilos inline
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #333;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 10000;
            max-width: 350px;
            cursor: pointer;
            animation: slideIn 0.3s ease-out;
        `;

        // Agregar al DOM
        document.body.appendChild(toast);

        // Click para navegar
        toast.addEventListener('click', () => {
            this.navegarANotificacion(notificacion);
            document.body.removeChild(toast);
        });

        // Auto-remover después de 5 segundos
        setTimeout(() => {
            if (toast.parentNode) {
                toast.style.animation = 'slideOut 0.3s ease-in';
                setTimeout(() => {
                    if (toast.parentNode) {
                        document.body.removeChild(toast);
                    }
                }, 300);
            }
        }, 5000);
    }

    /**
     * Navegar a la notificación
     */
    navegarANotificacion(notificacion) {
        // Marcar como leída
        this.marcarLeida(notificacion.id);

        // Navegar según tipo
        if (notificacion.incidente_id) {
            window.location.href = `/incidentes/${notificacion.incidente_id}`;
        } else if (notificacion.delito_id) {
            window.location.href = `/delitos/${notificacion.delito_id}`;
        }
    }

    /**
     * Marcar notificación como leída
     */
    async marcarLeida(notificacionId) {
        try {
            const token = this.getAuthToken();
            const response = await fetch(`/api/notificaciones/${notificacionId}/leer`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                // Actualizar en lista local
                const notif = this.notificaciones.find(n => n.id === notificacionId);
                if (notif) {
                    notif.leida = true;
                    this.actualizarBadge();
                }
            }
        } catch (error) {
            console.error('Error marcando notificación como leída:', error);
        }
    }

    /**
     * Reproducir sonido de notificación
     */
    reproducirSonido() {
        try {
            // Crear audio context si no existe
            if (!this.audioContext) {
                this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }

            // Crear oscilador para sonido simple
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);

            oscillator.frequency.value = 800; // Frecuencia en Hz
            oscillator.type = 'sine';

            gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);

            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 0.3);

        } catch (error) {
            // Silenciar errores de audio
            console.debug('No se pudo reproducir sonido:', error);
        }
    }

    /**
     * Registrar callback para nuevas notificaciones
     */
    onNuevaNotificacion(callback) {
        if (typeof callback === 'function') {
            this.callbacks.push(callback);
        }
    }

    /**
     * Obtener todas las notificaciones
     */
    getNotificaciones() {
        return this.notificaciones;
    }

    /**
     * Obtener notificaciones no leídas
     */
    getNoLeidas() {
        return this.notificaciones.filter(n => !n.leida);
    }

    /**
     * Obtener contador de no leídas
     */
    getContadorNoLeidas() {
        return this.notificaciones.filter(n => !n.leida).length;
    }

    /**
     * Desconectar del servidor
     */
    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
            this.socket = null;
            this.connected = false;
        }
    }
}

// Crear instancia global
window.notificacionesManager = new NotificacionesManager();

// Auto-inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.notificacionesManager.init();
    });
} else {
    window.notificacionesManager.init();
}

// Agregar estilos CSS para animaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }

    .notificacion-toast {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    .notificacion-toast-content strong {
        display: block;
        margin-bottom: 5px;
        font-size: 14px;
    }

    .notificacion-toast-content p {
        margin: 0;
        font-size: 13px;
        opacity: 0.9;
    }
`;
document.head.appendChild(style);
