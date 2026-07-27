/**
 * Lógica de login con ubicación jerárquica
 */
class LoginManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadDepartamentos();
        this.setupPasswordToggle();
    }
    
    setupPasswordToggle() {
        const togglePassword = document.getElementById('togglePassword');
        const passwordInput = document.getElementById('password');
        const eyeIcon = document.getElementById('eyeIcon');
        
        if (togglePassword) {
            togglePassword.addEventListener('click', () => {
                const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInput.setAttribute('type', type);
                
                // Cambiar icono
                if (type === 'text') {
                    eyeIcon.classList.remove('bi-eye');
                    eyeIcon.classList.add('bi-eye-slash');
                } else {
                    eyeIcon.classList.remove('bi-eye-slash');
                    eyeIcon.classList.add('bi-eye');
                }
            });
        }
    }
    
    setupEventListeners() {
        document.getElementById('rol').addEventListener('change', (e) => {
            this.handleRoleChange(e.target.value);
        });
        
        document.getElementById('departamento').addEventListener('change', (e) => {
            this.handleDepartamentoChange(e.target.value);
        });
        
        document.getElementById('municipio').addEventListener('change', (e) => {
            this.handleMunicipioChange(e.target.value);
        });
        
        document.getElementById('zona').addEventListener('change', (e) => {
            this.handleZonaChange(e.target.value);
        });
        
        document.getElementById('loginForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });
    }
    
    handleRoleChange(rol) {
        const locationSection = document.getElementById('locationSection');
        const departamentoGroup = document.getElementById('departamentoGroup');
        const municipioGroup = document.getElementById('municipioGroup');
        const zonaGroup = document.getElementById('zonaGroup');
        const puestoGroup = document.getElementById('puestoGroup');
        
        locationSection.style.display = 'none';
        departamentoGroup.style.display = 'none';
        municipioGroup.style.display = 'none';
        zonaGroup.style.display = 'none';
        puestoGroup.style.display = 'none';
        
        this.clearLocationSelectors();
        
        if (!rol || rol === 'super_admin') {
            return;
        }
        
        locationSection.style.display = 'block';
        
        switch (rol) {
            case 'admin_departamental':
            case 'coordinador_departamental':
            case 'auditor_electoral':
                departamentoGroup.style.display = 'block';
                break;
                
            case 'admin_municipal':
            case 'coordinador_municipal':
                departamentoGroup.style.display = 'block';
                municipioGroup.style.display = 'block';
                break;
                
            case 'coordinador_puesto':
            case 'testigo_electoral':
                departamentoGroup.style.display = 'block';
                municipioGroup.style.display = 'block';
                zonaGroup.style.display = 'block';
                puestoGroup.style.display = 'block';
                break;
        }
    }
    
    clearLocationSelectors() {
        Utils.enableSelect('departamento', true);
        Utils.enableSelect('municipio', false);
        Utils.enableSelect('zona', false);
        Utils.enableSelect('puesto', false);
        
        document.getElementById('municipio').value = '';
        document.getElementById('zona').value = '';
        document.getElementById('puesto').value = '';
    }
    
    async loadDepartamentos() {
        console.log('[LoginManager] Cargando departamentos...');
        try {
            const response = await APIClient.getDepartamentos();
            console.log('[LoginManager] Departamentos recibidos:', response);
            
            if (response && response.data) {
                console.log('[LoginManager] Poblando select con', response.data.length, 'departamentos');
                Utils.populateSelect('departamento', response.data, 'departamento_codigo', 'departamento_nombre', 'Seleccione departamento');
                console.log('[LoginManager] Select poblado exitosamente');
            } else {
                console.error('[LoginManager] Respuesta sin datos:', response);
            }
        } catch (error) {
            console.error('[LoginManager] Error loading departamentos:', error);
            Utils.showError('Error cargando departamentos: ' + error.message);
        }
    }
    
    async handleDepartamentoChange(departamentoId) {
        if (!departamentoId) {
            Utils.enableSelect('municipio', false);
            Utils.enableSelect('zona', false);
            Utils.enableSelect('puesto', false);
            return;
        }
        
        try {
            Utils.setLoading('municipio', true);
            const response = await APIClient.getMunicipios(departamentoId);
            
            Utils.populateSelect('municipio', response.data, 'municipio_codigo', 'municipio_nombre', 'Seleccione municipio');
            Utils.enableSelect('municipio', true);
            Utils.enableSelect('zona', false);
            Utils.enableSelect('puesto', false);
            
        } catch (error) {
            console.error('Error loading municipios:', error);
            Utils.showError('Error cargando municipios: ' + error.message);
        } finally {
            Utils.setLoading('municipio', false);
        }
    }
    
    async handleMunicipioChange(municipioId) {
        if (!municipioId) {
            Utils.enableSelect('zona', false);
            Utils.enableSelect('puesto', false);
            return;
        }
        
        try {
            Utils.setLoading('zona', true);
            const response = await APIClient.getZonas(municipioId);
            
            Utils.populateSelect('zona', response.data, 'zona_codigo', 'nombre_completo', 'Seleccione zona');
            Utils.enableSelect('zona', true);
            Utils.enableSelect('puesto', false);
            
        } catch (error) {
            console.error('Error loading zonas:', error);
            Utils.showError('Error cargando zonas: ' + error.message);
        } finally {
            Utils.setLoading('zona', false);
        }
    }
    
    async handleZonaChange(zonaId) {
        if (!zonaId) {
            Utils.enableSelect('puesto', false);
            return;
        }
        
        try {
            Utils.setLoading('puesto', true);
            const response = await APIClient.getPuestos(zonaId);
            
            Utils.populateSelect('puesto', response.data, 'puesto_codigo', 'puesto_nombre', 'Seleccione puesto');
            Utils.enableSelect('puesto', true);
            
        } catch (error) {
            console.error('Error loading puestos:', error);
            Utils.showError('Error cargando puestos: ' + error.message);
        } finally {
            Utils.setLoading('puesto', false);
        }
    }
    
    async handleLogin() {
        try {
            Utils.toggleSpinner('loginBtn', 'loginText', 'loginSpinner', true);
            
            const formData = Utils.getFormData('loginForm');
            const rol = formData.rol;
            
            const requiredFields = ['rol', 'password'];
            
            if (rol !== 'super_admin') {
                requiredFields.push('departamento');
                
                if (['admin_municipal', 'coordinador_municipal', 'coordinador_puesto', 'testigo_electoral'].includes(rol)) {
                    requiredFields.push('municipio');
                }
                
                if (['coordinador_puesto', 'testigo_electoral'].includes(rol)) {
                    requiredFields.push('zona', 'puesto');
                }
            }
            
            const errors = Utils.validateRequired('loginForm', requiredFields);
            if (errors.length > 0) {
                Utils.showError(errors.join('<br>'));
                return;
            }
            
            const loginData = {
                rol: formData.rol,
                password: formData.password
            };
            
            if (formData.departamento) {
                loginData.departamento_codigo = formData.departamento;
            }
            if (formData.municipio) {
                loginData.municipio_codigo = formData.municipio;
            }
            if (formData.zona) {
                loginData.zona_codigo = formData.zona;
            }
            if (formData.puesto) {
                loginData.puesto_codigo = formData.puesto;
            }
            
            const response = await APIClient.login(loginData);
            
            localStorage.setItem('access_token', response.data.access_token);
            localStorage.setItem('refresh_token', response.data.refresh_token);
            localStorage.setItem('user_data', JSON.stringify(response.data.user));
            
            Utils.showSuccess('Login exitoso. Redirigiendo...');
            
            setTimeout(() => {
                this.redirectToDashboard(response.data.user.rol);
            }, 1500);
            
        } catch (error) {
            console.error('Login error:', error);
            Utils.showError('Error de login: ' + error.message);
        } finally {
            Utils.toggleSpinner('loginBtn', 'loginText', 'loginSpinner', false);
        }
    }
    
    redirectToDashboard(rol) {
        const dashboardUrls = {
            'super_admin': '/admin/dashboard',
            'admin_departamental': '/admin/dashboard',
            'admin_municipal': '/admin/dashboard',
            'coordinador_departamental': '/coordinador/departamental',
            'coordinador_municipal': '/coordinador/municipal',
            'coordinador_puesto': '/coordinador/puesto',
            'testigo_electoral': '/testigo/dashboard',
            'auditor_electoral': '/auditor/dashboard'
        };
        
        const url = dashboardUrls[rol] || '/dashboard';
        window.location.href = url;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new LoginManager();
});


// Inicializar LoginManager cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    console.log('[LoginManager] Inicializando...');
    new LoginManager();
    console.log('[LoginManager] Inicializado correctamente');
});
