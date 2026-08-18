/**
 * Dashboard del Administrador
 */
class AdminDashboard {
    constructor() {
        this.userData = null;
        this.init();
    }
    
    async init() {
        if (!this.checkAuth()) {
            window.location.href = '/auth/login';
            return;
        }
        
        await this.loadUserData();
        await this.loadStats();
        await this.loadResumenMunicipios();
        await this.loadActividadReciente();
    }
    
    checkAuth() {
        const token = localStorage.getItem('access_token');
        const userData = localStorage.getItem('user_data');
        
        if (!token || !userData) {
            return false;
        }
        
        try {
            this.userData = JSON.parse(userData);
            return true;
        } catch (e) {
            return false;
        }
    }
    
    async loadUserData() {
        try {
            const response = await APIClient.getProfile();
            this.userData = response.data;
            
            const rolName = this.getRoleName(this.userData.rol);
            const ubicacion = this.userData.ubicacion?.nombre_completo || 'Nivel Nacional';
            
            document.getElementById('userInfo').innerHTML = `
                <strong>${this.userData.nombre}</strong> - ${rolName}<br>
                <small>${ubicacion}</small>
            `;
        } catch (error) {
            console.error('Error loading user data:', error);
        }
    }
    
    async loadStats() {
        try {
            const response = await APIClient.get('/admin/stats');
            
            if (response.success && response.data) {
                const stats = response.data;
                
                document.getElementById('totalUsuarios').textContent = Utils.formatNumber(stats.total_usuarios);
                document.getElementById('totalPuestos').textContent = Utils.formatNumber(stats.total_puestos);
                document.getElementById('totalFormularios').textContent = Utils.formatNumber(stats.total_formularios);
                document.getElementById('totalValidados').textContent = Utils.formatNumber(stats.formularios_completados);
            }
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }
    
    async loadResumenMunicipios() {
        const container = document.getElementById('resumenMunicipios');
        
        try {
            const response = await APIClient.get('/admin/ubicaciones?tipo=municipio');
            
            const municipios = (response.success && response.data) ? response.data : [];
            
            if (municipios.length === 0) {
                container.innerHTML = '<div class="alert alert-info">No hay municipios registrados</div>';
                return;
            }
            
            let html = '<div class="table-responsive">';
            html += '<table class="table table-hover">';
            html += '<thead><tr><th>Municipio</th><th>Votantes Registrados</th></tr></thead>';
            html += '<tbody>';
            
            municipios.forEach(m => {
                html += `
                    <tr>
                        <td><strong>${m.nombre_completo}</strong></td>
                        <td>${Utils.formatNumber(m.total_votantes_registrados || 0)}</td>
                    </tr>
                `;
            });
            
            html += '</tbody></table></div>';
            container.innerHTML = html;
            
        } catch (error) {
            console.error('Error loading resumen:', error);
            container.innerHTML = '<div class="alert alert-danger">Error cargando datos</div>';
        }
    }
    
    async loadActividadReciente() {
        const container = document.getElementById('actividadReciente');
        
        try {
            // TODO: Implementar endpoint real
            await new Promise(resolve => setTimeout(resolve, 500));
            
            const actividades = []; // Datos simulados
            
            if (actividades.length === 0) {
                container.innerHTML = `
                    <div class="text-center py-4">
                        <p class="text-muted">No hay actividad reciente</p>
                    </div>
                `;
                return;
            }
            
            // Renderizar actividades
            let html = '<div class="list-group">';
            actividades.forEach(act => {
                html += `
                    <div class="list-group-item">
                        <div class="d-flex w-100 justify-content-between">
                            <h6 class="mb-1">${act.titulo}</h6>
                            <small>${Utils.formatDate(act.fecha)}</small>
                        </div>
                        <p class="mb-1">${act.descripcion}</p>
                        <small class="text-muted">${act.usuario}</small>
                    </div>
                `;
            });
            html += '</div>';
            
            container.innerHTML = html;
            
        } catch (error) {
            console.error('Error loading actividad:', error);
        }
    }
    
    getRoleName(rol) {
        const roles = {
            'super_admin': 'Super Administrador',
            'admin_departamental': 'Administrador Departamental',
            'admin_municipal': 'Administrador Municipal',
            'coordinador_departamental': 'Coordinador Departamental',
            'coordinador_municipal': 'Coordinador Municipal',
            'coordinador_puesto': 'Coordinador de Puesto',
            'testigo_electoral': 'Testigo Electoral',
            'auditor_electoral': 'Auditor Electoral'
        };
        return roles[rol] || rol;
    }
}

// Funciones globales para acciones rápidas
function gestionarUsuarios() {
    Utils.showInfo('Módulo de gestión de usuarios en desarrollo');
}

function verReportes() {
    Utils.showInfo('Módulo de reportes en desarrollo');
}

function configuracion() {
    Utils.showInfo('Módulo de configuración en desarrollo');
}

function auditoria() {
    Utils.showInfo('Módulo de auditoría en desarrollo');
}

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

document.addEventListener('DOMContentLoaded', () => {
    new AdminDashboard();
});
