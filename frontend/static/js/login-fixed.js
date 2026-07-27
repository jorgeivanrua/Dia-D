/**
 * Lógica de login con ubicación jerárquica - VERSIÓN CORREGIDA
 */

// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    console.log('[LOGIN] Inicializando sistema de login...');
    
    // Verificar que las dependencias existan
    if (typeof APIClient === 'undefined') {
        console.error('[LOGIN] APIClient no está definido');
        return;
    }
    
    if (typeof Utils === 'undefined') {
        console.error('[LOGIN] Utils no está definido');
        return;
    }
    
    console.log('[LOGIN] Dependencias verificadas OK');
    
    // Cargar departamentos inmediatamente
    loadDepartamentos();
    
    // Setup event listeners
    setupEventListeners();
    setupPasswordToggle();
    
    console.log('[LOGIN] Sistema inicializado correctamente');
});

function setupPasswordToggle() {
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');
    const eyeIcon = document.getElementById('eyeIcon');
    
    if (togglePassword && passwordInput && eyeIcon) {
        togglePassword.addEventListener('click', () => {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
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

function setupEventListeners() {
    // Rol change
    const rolSelect = document.getElementById('rol');
    if (rolSelect) {
        rolSelect.addEventListener('change', (e) => handleRoleChange(e.target.value));
    }
    
    // Departamento change
    const deptSelect = document.getElementById('departamento');
    if (deptSelect) {
        deptSelect.addEventListener('change', (e) => handleDepartamentoChange(e.target.value));
    }
    
    // Municipio change
    const munSelect = document.getElementById('municipio');
    if (munSelect) {
        munSelect.addEventListener('change', (e) => handleMunicipioChange(e.target.value));
    }
    
    // Zona change
    const zonaSelect = document.getElementById('zona');
    if (zonaSelect) {
        zonaSelect.addEventListener('change', (e) => handleZonaChange(e.target.value));
    }
    
    // Form submit
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            handleLogin();
        });
    }
}

async function loadDepartamentos() {
    console.log('[LOGIN] Cargando departamentos...');
    try {
        const response = await APIClient.getDepartamentos();
        console.log('[LOGIN] Respuesta departamentos:', response);
        
        if (response && response.success && response.data) {
            console.log('[LOGIN] Poblando select con', response.data.length, 'departamentos');
            Utils.populateSelect('departamento', response.data, 'departamento_codigo', 'departamento_nombre', 'Seleccione departamento');
            console.log('[LOGIN] Departamentos cargados exitosamente');
        } else {
            console.error('[LOGIN] Respuesta inválida:', response);
        }
    } catch (error) {
        console.error('[LOGIN] Error cargando departamentos:', error);
        Utils.showError('Error cargando departamentos: ' + error.message);
    }
}

function handleRoleChange(rol) {
    console.log('[LOGIN] Rol seleccionado:', rol);
    
    const locationSection = document.getElementById('locationSection');
    const departamentoGroup = document.getElementById('departamentoGroup');
    const municipioGroup = document.getElementById('municipioGroup');
    const zonaGroup = document.getElementById('zonaGroup');
    const puestoGroup = document.getElementById('puestoGroup');
    
    // Ocultar todo por defecto
    locationSection.style.display = 'none';
    departamentoGroup.style.display = 'none';
    municipioGroup.style.display = 'none';
    zonaGroup.style.display = 'none';
    puestoGroup.style.display = 'none';
    
    clearLocationSelectors();
    
    if (!rol || rol === 'super_admin' || rol === 'monitoreo') {
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

function clearLocationSelectors() {
    Utils.enableSelect('departamento', true);
    Utils.enableSelect('municipio', false);
    Utils.enableSelect('zona', false);
    Utils.enableSelect('puesto', false);
    
    document.getElementById('municipio').value = '';
    document.getElementById('zona').value = '';
    document.getElementById('puesto').value = '';
}

async function handleDepartamentoChange(departamentoId) {
    console.log('[LOGIN] Departamento seleccionado:', departamentoId);
    console.log('[LOGIN] Tipo de departamentoId:', typeof departamentoId);
    
    if (!departamentoId || departamentoId === '') {
        console.log('[LOGIN] Departamento vacío, deshabilitando selects');
        Utils.enableSelect('municipio', false);
        Utils.enableSelect('zona', false);
        Utils.enableSelect('puesto', false);
        return;
    }
    
    try {
        console.log('[LOGIN] Iniciando carga de municipios...');
        Utils.setLoading('municipio', true);
        
        console.log('[LOGIN] Llamando a APIClient.getMunicipios con:', departamentoId);
        const response = await APIClient.getMunicipios(departamentoId);
        console.log('[LOGIN] Respuesta completa:', JSON.stringify(response, null, 2));
        
        if (response && response.success && response.data) {
            console.log('[LOGIN] Poblando select con', response.data.length, 'municipios');
            Utils.populateSelect('municipio', response.data, 'municipio_codigo', 'municipio_nombre', 'Seleccione municipio');
            Utils.enableSelect('municipio', true);
            Utils.enableSelect('zona', false);
            Utils.enableSelect('puesto', false);
            console.log('[LOGIN] Select de municipios poblado exitosamente');
        } else {
            console.error('[LOGIN] Respuesta inválida o sin datos:', response);
            Utils.showError('No se pudieron cargar los municipios');
        }
    } catch (error) {
        console.error('[LOGIN] Error cargando municipios:', error);
        console.error('[LOGIN] Stack trace:', error.stack);
        Utils.showError('Error cargando municipios: ' + error.message);
    } finally {
        Utils.setLoading('municipio', false);
        console.log('[LOGIN] Carga de municipios finalizada');
    }
}

async function handleMunicipioChange(municipioId) {
    console.log('[LOGIN] Municipio seleccionado:', municipioId);
    
    if (!municipioId) {
        Utils.enableSelect('zona', false);
        Utils.enableSelect('puesto', false);
        return;
    }
    
    try {
        Utils.setLoading('zona', true);
        const response = await APIClient.getZonas(municipioId);
        console.log('[LOGIN] Zonas recibidas:', response);
        
        if (response && response.success && response.data) {
            Utils.populateSelect('zona', response.data, 'zona_codigo', 'zona_nombre', 'Seleccione zona');
            Utils.enableSelect('zona', true);
            Utils.enableSelect('puesto', false);
        }
    } catch (error) {
        console.error('[LOGIN] Error cargando zonas:', error);
        Utils.showError('Error cargando zonas: ' + error.message);
    } finally {
        Utils.setLoading('zona', false);
    }
}

async function handleZonaChange(zonaId) {
    console.log('[LOGIN] Zona seleccionada:', zonaId);
    
    if (!zonaId) {
        Utils.enableSelect('puesto', false);
        return;
    }
    
    try {
        Utils.setLoading('puesto', true);
        const response = await APIClient.getPuestos(zonaId);
        console.log('[LOGIN] Puestos recibidos:', response);
        
        if (response && response.success && response.data) {
            Utils.populateSelect('puesto', response.data, 'puesto_codigo', 'puesto_nombre', 'Seleccione puesto');
            Utils.enableSelect('puesto', true);
        }
    } catch (error) {
        console.error('[LOGIN] Error cargando puestos:', error);
        Utils.showError('Error cargando puestos: ' + error.message);
    } finally {
        Utils.setLoading('puesto', false);
    }
}

async function handleLogin() {
    try {
        Utils.toggleSpinner('loginBtn', 'loginText', 'loginSpinner', true);
        
        const formData = Utils.getFormData('loginForm');
        const rol = formData.rol;
        
        const requiredFields = ['rol', 'password'];
        
        // Super admin y monitoreo no requieren ubicación
        if (rol !== 'super_admin' && rol !== 'monitoreo') {
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
            redirectToDashboard(response.data.user.rol);
        }, 1500);
        
    } catch (error) {
        console.error('[LOGIN] Error en login:', error);
        Utils.showError(error.message || 'Error en el login');
    } finally {
        Utils.toggleSpinner('loginBtn', 'loginText', 'loginSpinner', false);
    }
}

function redirectToDashboard(rol) {
    const dashboards = {
        'super_admin': '/admin/super-admin',
        'admin_departamental': '/admin/dashboard',
        'admin_municipal': '/admin/dashboard',
        'coordinador_departamental': '/coordinador/departamental',
        'coordinador_municipal': '/coordinador/municipal',
        'coordinador_puesto': '/coordinador/puesto',
        'testigo_electoral': '/testigo/dashboard',
        'auditor_electoral': '/auditor/dashboard',
        'monitoreo': '/monitoreo/dashboard'
    };
    
    const dashboard = dashboards[rol] || '/dashboard';
    window.location.href = dashboard;
}
