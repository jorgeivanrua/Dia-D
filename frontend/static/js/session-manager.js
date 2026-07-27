/**
 * Session Manager - Detecta cambios de sesión entre pestañas
 * DESHABILITADO: Causa problemas al tener múltiples pestañas abiertas
 * 
 * En su lugar, se recomienda:
 * 1. Usar una pestaña por usuario
 * 2. Cerrar sesión antes de cambiar de usuario
 * 3. Usar navegadores diferentes para diferentes roles
 */
class SessionManager {
    constructor() {
        this.currentToken = null;
        this.currentRole = null;
        this.checkInterval = null;
        this.enabled = false; // DESHABILITADO por defecto
    }
    
    /**
     * Inicializar el gestor de sesión
     */
    init() {
        if (!this.enabled) {
            console.log('[SessionManager] Disabled - Multiple tabs are allowed');
            return;
        }
        
        // Guardar token y rol actual
        this.currentToken = localStorage.getItem('access_token');
        const userData = localStorage.getItem('user_data');
        if (userData) {
            try {
                const user = JSON.parse(userData);
                this.currentRole = user.rol;
            } catch (e) {
                console.error('Error parsing user data:', e);
            }
        }
        
        // Escuchar cambios en localStorage (otras pestañas)
        window.addEventListener('storage', (e) => {
            if (e.key === 'access_token' || e.key === 'user_data') {
                this.handleSessionChange();
            }
        });
        
        // Verificar cada 5 segundos si el token cambió
        this.checkInterval = setInterval(() => {
            this.checkSession();
        }, 5000);
        
        console.log('[SessionManager] Initialized');
    }
    
    /**
     * Habilitar el gestor de sesión
     */
    enable() {
        this.enabled = true;
        this.init();
    }
    
    /**
     * Deshabilitar el gestor de sesión
     */
    disable() {
        this.enabled = false;
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
            this.checkInterval = null;
        }
    }
    
    /**
     * Verificar si la sesión cambió
     */
    checkSession() {
        if (!this.enabled) return;
        
        const newToken = localStorage.getItem('access_token');
        const userData = localStorage.getItem('user_data');
        let newRole = null;
        
        if (userData) {
            try {
                const user = JSON.parse(userData);
                newRole = user.rol;
            } catch (e) {
                console.error('Error parsing user data:', e);
            }
        }
        
        // Si el token o el rol cambió, recargar la página
        if (newToken !== this.currentToken || newRole !== this.currentRole) {
            console.log('[SessionManager] Session changed detected');
            console.log('  Old token:', this.currentToken?.substring(0, 20) + '...');
            console.log('  New token:', newToken?.substring(0, 20) + '...');
            console.log('  Old role:', this.currentRole);
            console.log('  New role:', newRole);
            
            this.handleSessionChange();
        }
    }
    
    /**
     * Manejar cambio de sesión
     */
    handleSessionChange() {
        if (!this.enabled) return;
        
        console.log('[SessionManager] Reloading page due to session change...');
        
        // Mostrar mensaje
        const message = document.createElement('div');
        message.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #fff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            z-index: 10000;
            text-align: center;
        `;
        message.innerHTML = `
            <h3>Sesión Actualizada</h3>
            <p>Se detectó un cambio de sesión en otra pestaña.</p>
            <p>Recargando página...</p>
        `;
        document.body.appendChild(message);
        
        // Recargar después de 1 segundo
        setTimeout(() => {
            window.location.reload();
        }, 1000);
    }
    
    /**
     * Destruir el gestor
     */
    destroy() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
        }
    }
}

// Crear instancia global
window.sessionManager = new SessionManager();

// Auto-inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.sessionManager.init();
    });
} else {
    window.sessionManager.init();
}
