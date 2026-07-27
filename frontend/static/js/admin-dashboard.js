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
        // Datos simulados por ahora
        // TODO: Implementar endpoints reales
        document.getElementById('totalUsuarios').textContent = '8';
        document.getElementById('totalPuestos').textContent = '150';
        document.getElementById('totalFormularios').textContent = '0';
        document.getElementById('totalValidados').textContent = '0';
    }
    
    async loadResumenMunicipios() {
        const container = document.getElementById('resumenMunicipios');
        
        try {
            // TODO: Implementar endpoint real
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // Datos simulados
            const municipios = [
                { nombre: 'Florencia', puestos: 45, formularios: 0, porcentaje: 0 },
                { nombre: 'San Vicente del Caguán', puestos: 25, formularios: 0, porcentaje: 0 },
                { nombre: 'Puerto Rico', puestos: 18, formularios: 0, porcentaje: 0 },
                { nombre: 'El Doncello', puestos: 12, formularios: 0, porcentaje: 0 },
                { nombre: 'Otros', puestos: 50, formularios: 0, porcentaje: 0 }
            ];
            
            let html = '<div class="table-responsive">';
            html += '<table class="table table-hover">';
            html += '<thead><tr><th>Municipio</th><th>Puestos</th><th>Formularios</th><th>Progreso</th></tr></thead>';
            html += '<tbody>';
            
            municipios.forEach(m => {
                html += `
                    <tr>
                        <td><strong>${m.nombre}</strong></td>
                        <td>${m.puestos}</td>
                        <td>${m.formularios}</td>
                        <td>
                            <div class="progress" style="height: 20px;">
                                <div class="progress-bar" role="progressbar" 
                                     style="width: ${m.porcentaje}%" 
                                     aria-valuenow="${m.porcentaje}" 
                                     aria-valuemin="0" 
                                     aria-valuemax="100">
                                    ${m.porcentaje}%
                                </div>
                            </div>
                        </td>
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
