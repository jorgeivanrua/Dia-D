/**
 * Dashboard Super Admin
 * Gestión completa del sistema electoral
 */

let currentUser = null;
let allUsers = [];
let allPartidos = [];
let allCandidatos = [];
let allTiposEleccion = [];
// Usar window.charts para evitar conflictos
window.charts = window.charts || {};

// Exponer variables globalmente para debugging y acceso desde otros scripts
window.allUsers = allUsers;
window.allPartidos = allPartidos;
window.allCandidatos = allCandidatos;
window.allTiposEleccion = allTiposEleccion;

/**
 * Inicializar dashboard
 */
async function initSuperAdminDashboard() {
    try {
        console.log('Inicializando Super Admin Dashboard...');
        
        // Cargar perfil del usuario
        await loadUserProfile();
        
        // Cargar estadísticas principales
        await loadMainStats();
        
        // Cargar actividad reciente
        await loadRecentActivity();
        
        // Inicializar gráficos
        initCharts();
        
        // Cargar datos iniciales
        await loadUsers();
        await loadPartidos();
        await loadTiposEleccion();
        await loadCandidatos();
        await loadCampanas();
        
        // Auto-refresh cada 30 segundos
        setInterval(() => {
            loadMainStats();
            loadRecentActivity();
            updateSystemHealth();
        }, 30000);
        
        console.log('Super Admin Dashboard inicializado correctamente');
        
    } catch (error) {
        console.error('Error inicializando dashboard:', error);
        Utils.showError('Error al cargar el dashboard');
    }
}

/**
 * Cargar perfil del usuario
 */
async function loadUserProfile() {
    try {
        // Verificar que hay token
        const token = localStorage.getItem('access_token');
        if (!token) {
            console.log('No hay token, redirigiendo al login...');
            window.location.href = '/auth/login';
            return;
        }
        
        const response = await APIClient.getProfile();
        
        if (response.success) {
            currentUser = response.data.user;
            
            // Verificar que el usuario es super admin
            if (currentUser.rol !== 'super_admin') {
                console.error('Usuario no es super admin');
                Utils.showError('No tienes permisos para acceder a esta página');
                setTimeout(() => {
                    window.location.href = '/auth/login';
                }, 2000);
                return;
            }
            
            document.getElementById('userInfo').innerHTML = `
                <strong>${currentUser.nombre}</strong> • Super Administrador
                <br><small>Acceso completo al sistema</small>
            `;
        }
    } catch (error) {
        console.error('Error cargando perfil:', error);
        // Si hay error de autenticación, redirigir al login
        if (error.message && (error.message.includes('401') || error.message.includes('token') || error.message.includes('Sesión'))) {
            console.log('Error de autenticación, redirigiendo al login...');
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user_data');
            window.location.href = '/auth/login';
        }
    }
}

/**
 * Cargar estadísticas principales
 */
async function loadMainStats() {
    try {
        const response = await APIClient.get('/super-admin/stats');
        
        if (response.success) {
            const stats = response.data;
            
            // Actualizar UI
            document.getElementById('totalUsuarios').textContent = Utils.formatNumber(stats.totalUsuarios);
            document.getElementById('usuariosChange').textContent = stats.usuariosChange >= 0 ? `+${stats.usuariosChange}` : stats.usuariosChange;
            document.getElementById('totalPuestos').textContent = Utils.formatNumber(stats.totalPuestos);
            document.getElementById('totalMesas').textContent = Utils.formatNumber(stats.totalMesas);
            document.getElementById('totalFormularios').textContent = Utils.formatNumber(stats.totalFormularios);
            document.getElementById('formulariosPendientes').textContent = Utils.formatNumber(stats.formulariosPendientes);
            document.getElementById('totalValidados').textContent = Utils.formatNumber(stats.totalValidados);
            document.getElementById('porcentajeValidados').textContent = stats.porcentajeValidados.toFixed(1);
            
            // Actualizar barra de progreso
            const progressBar = document.querySelector('.progress-bar');
            if (progressBar) {
                progressBar.style.width = `${stats.porcentajeValidados}%`;
                progressBar.setAttribute('aria-valuenow', stats.porcentajeValidados);
            }
        }
    } catch (error) {
        console.error('Error cargando estadísticas:', error);
        Utils.showError('Error al cargar estadísticas del sistema');
    }
}

/**
 * Cargar actividad reciente
 */
async function loadRecentActivity() {
    try {
        const container = document.getElementById('recentActivity');
        
        if (!container) {
            console.warn('Elemento recentActivity no encontrado');
            return;
        }
        
        // Mostrar mensaje mientras se implementa el endpoint real
        container.innerHTML = `
            <div class="text-center py-4">
                <i class="bi bi-clock-history text-muted" style="font-size: 3rem;"></i>
                <p class="text-muted mt-3 mb-1"><strong>Actividad reciente próximamente</strong></p>
                <small class="text-muted">El registro de actividad del sistema está en desarrollo</small>
            </div>
        `;
        
    } catch (error) {
        console.error('Error cargando actividad:', error);
    }
}

/**
 * Actualizar estado de salud del sistema
 */
async function updateSystemHealth() {
    try {
        // Por ahora, mostrar estado estático hasta implementar el endpoint
        const indicator = document.getElementById('systemHealthIndicator');
        const text = document.getElementById('systemHealthText');
        
        if (indicator && text) {
            indicator.className = 'health-indicator health-good';
            text.textContent = 'Sistema operando normalmente';
        }
        
        // Actualizar métricas estáticas
        const cpuElement = document.getElementById('cpuUsage');
        const memoryElement = document.getElementById('memoryUsage');
        const dbElement = document.getElementById('dbStatus');
        
        if (cpuElement) cpuElement.textContent = '0%';
        if (memoryElement) memoryElement.textContent = '0%';
        if (dbElement) {
            dbElement.textContent = 'Conectada';
            dbElement.className = 'text-success';
        }
        
    } catch (error) {
        console.error('Error actualizando salud del sistema:', error);
    }
}

/**
 * Inicializar gráficos
 */
async function initCharts() {
    try {
        // Destruir gráficos existentes antes de crear nuevos
        if (window.charts) {
            if (window.charts.progress) {
                window.charts.progress.destroy();
                window.charts.progress = null;
            }
            if (window.charts.activity) {
                window.charts.activity.destroy();
                window.charts.activity = null;
            }
        } else {
            window.charts = {};
        }
        
        // Por ahora, no cargar gráficos hasta que se implementen los endpoints
        console.log('Gráficos inicializados (pendiente de implementación)');
        
    } catch (error) {
        console.error('Error inicializando gráficos:', error);
    }
}

/**
 * Cargar datos de monitoreo departamental
 */
async function loadMonitoreoDepartamental() {
    try {
        // Endpoint pendiente de implementación
        console.log('Monitoreo departamental pendiente de implementación');
        return;
    } catch (error) {
        console.error('Error cargando monitoreo departamental:', error);
    }
}

/**
 * Actualizar tabla de monitoreo
 */
function updateMonitoreoTable(data) {
    const tbody = document.getElementById('monitoreoTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = data.map(depto => {
        const progressColor = depto.porcentaje_avance >= 80 ? 'success' : depto.porcentaje_avance >= 50 ? 'warning' : 'danger';
        
        return `
            <tr>
                <td><strong>${depto.departamento}</strong></td>
                <td class="text-center">${Utils.formatNumber(depto.total_mesas)}</td>
                <td class="text-center">${Utils.formatNumber(depto.validados)}</td>
                <td class="text-center">${Utils.formatNumber(depto.pendientes)}</td>
                <td class="text-center">${Utils.formatNumber(depto.rechazados)}</td>
                <td class="text-center">${Utils.formatNumber(depto.sin_reporte)}</td>
                <td>
                    <div class="progress" style="height: 20px;">
                        <div class="progress-bar bg-${progressColor}" style="width: ${depto.porcentaje_avance}%">
                            ${depto.porcentaje_avance.toFixed(1)}%
                        </div>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

// ============================================
// GESTIÓN DE USUARIOS
// ============================================

/**
 * Cargar usuarios
 */
async function loadUsers() {
    try {
        console.log('🔄 Cargando usuarios...');
        const response = await APIClient.get('/super-admin/users');
        
        console.log('📦 Respuesta de usuarios:', response);
        
        if (response.success) {
            allUsers = response.data;
            window.allUsers = allUsers; // Actualizar referencia global
            console.log(`✅ ${allUsers.length} usuarios cargados`);
            renderUsers(allUsers);
        } else {
            console.error('❌ Error en respuesta:', response.error);
            Utils.showError('Error al cargar usuarios: ' + (response.error || 'Error desconocido'));
        }
    } catch (error) {
        console.error('❌ Error cargando usuarios:', error);
        Utils.showError('Error al cargar usuarios: ' + error.message);
    }
}

/**
 * Renderizar tabla de usuarios
 */
function renderUsers(users) {
    // Exponer globalmente para debugging
    window.renderUsers = renderUsers;
    const tbody = document.getElementById('usuarios-lista');
    
    if (!tbody) {
        console.error('❌ Elemento usuarios-lista no encontrado en el DOM');
        return;
    }
    
    if (!users) {
        console.error('❌ users es null o undefined');
        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4"><p class="text-danger">Error: No se pudieron cargar los usuarios</p></td></tr>';
        return;
    }
    
    if (!Array.isArray(users)) {
        console.error('❌ users no es un array:', typeof users);
        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4"><p class="text-danger">Error: Formato de datos incorrecto</p></td></tr>';
        return;
    }
    
    if (users.length === 0) {
        console.log('ℹ️ No hay usuarios para mostrar');
        tbody.innerHTML = '<tr style="background: white !important;"><td colspan="7" class="text-center py-4" style="color: #6c757d !important;"><p class="text-muted" style="color: #6c757d !important;">No hay usuarios registrados en el sistema</p></td></tr>';
        return;
    }
    
    console.log(`📊 Renderizando ${users.length} usuarios`);
    
    tbody.innerHTML = users.map(user => {
        // Validar que user tenga las propiedades necesarias
        if (!user.id || !user.nombre || !user.rol) {
            console.warn('⚠️ Usuario con datos incompletos:', user);
            return '';
        }
        
        return `
            <tr style="background: white !important; color: #212529 !important;">
                <td style="color: #212529 !important;">${user.id}</td>
                <td style="color: #212529 !important;"><strong>${user.nombre}</strong></td>
                <td style="color: #212529 !important;"><span class="badge bg-${getRoleBadgeColor(user.rol)}">${user.rol}</span></td>
                <td style="color: #212529 !important;">${user.ubicacion_nombre || '<span class="text-muted" style="color: #6c757d !important;">Sin asignar</span>'}</td>
                <td class="text-center" style="color: #212529 !important;">
                    <span class="badge bg-${user.activo ? 'success' : 'secondary'}">
                        ${user.activo ? 'Activo' : 'Inactivo'}
                    </span>
                </td>
                <td style="color: #212529 !important;"><small>${user.ultimo_acceso ? Utils.formatDateTime(user.ultimo_acceso) : '<span class="text-muted" style="color: #6c757d !important;">Nunca</span>'}</small></td>
                <td class="text-center" style="color: #212529 !important;">
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="editUser(${user.id})" title="Editar">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-outline-warning" onclick="resetUserPassword(${user.id})" title="Resetear contraseña">
                            <i class="bi bi-key"></i>
                        </button>
                        <button class="btn btn-outline-${user.activo ? 'danger' : 'success'}" 
                                onclick="toggleUserStatus(${user.id}, ${!user.activo})" 
                                title="${user.activo ? 'Desactivar' : 'Activar'}">
                            <i class="bi bi-${user.activo ? 'x-circle' : 'check-circle'}"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
    
    // Actualizar contador
    const countElement = document.getElementById('usuarios-count');
    if (countElement) {
        countElement.textContent = users.length;
    }
    
    console.log('✅ Usuarios renderizados correctamente');
}

/**
 * Obtener color de badge según rol
 */
function getRoleBadgeColor(rol) {
    const colors = {
        'super_admin': 'dark',
        'auditor_electoral': 'info',
        'coordinador_departamental': 'primary',
        'coordinador_municipal': 'success',
        'coordinador_puesto': 'warning',
        'testigo_electoral': 'secondary',
        'admin_departamental': 'primary',
        'admin_municipal': 'success'
    };
    return colors[rol] || 'secondary';
}

/**
 * Filtrar usuarios
 */
function filterUsers() {
    const role = document.getElementById('filterRole')?.value || '';
    const status = document.getElementById('filterStatus')?.value || '';
    const search = document.getElementById('searchUser')?.value.toLowerCase() || '';
    
    let filtered = allUsers;
    
    // Filtrar por rol
    if (role) {
        filtered = filtered.filter(user => user.rol === role);
    }
    
    // Filtrar por estado
    if (status) {
        const isActive = status === 'activo';
        filtered = filtered.filter(user => user.activo === isActive);
    }
    
    // Filtrar por búsqueda
    if (search) {
        filtered = filtered.filter(user => 
            user.nombre.toLowerCase().includes(search) ||
            (user.ubicacion_nombre && user.ubicacion_nombre.toLowerCase().includes(search))
        );
    }
    
    renderUsers(filtered);
}

/**
 * Mostrar modal de crear usuario
 */
async function showCreateUserModal() {
    // Crear modal dinámicamente
    const modalHtml = `
        <div class="modal fade" id="createUserModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title"><i class="bi bi-person-plus"></i> Crear Nuevo Usuario</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="createUserForm">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Nombre *</label>
                                    <input type="text" class="form-control" id="userName" required>
                                    <small class="text-muted">Nombre de usuario para login</small>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Rol *</label>
                                    <select class="form-select" id="userRole" required onchange="handleRoleChange()">
                                        <option value="">Seleccione...</option>
                                        <option value="super_admin">Super Admin</option>
                                        <option value="admin_departamental">Admin Departamental</option>
                                        <option value="admin_municipal">Admin Municipal</option>
                                        <option value="coordinador_departamental">Coordinador Departamental</option>
                                        <option value="coordinador_municipal">Coordinador Municipal</option>
                                        <option value="coordinador_puesto">Coordinador de Puesto</option>
                                        <option value="testigo_electoral">Testigo Electoral</option>
                                        <option value="auditor_electoral">Auditor Electoral</option>
                                    </select>
                                </div>
                            </div>
                            
                            <!-- Sección de Ubicación (dinámica según rol) -->
                            <div id="locationSection" style="display: none;">
                                <div class="card bg-light mb-3">
                                    <div class="card-body">
                                        <h6 class="card-title"><i class="bi bi-geo-alt"></i> Ubicación</h6>
                                        
                                        <!-- Departamento -->
                                        <div id="departamentoGroup" class="mb-3" style="display: none;">
                                            <label class="form-label">Departamento *</label>
                                            <select class="form-select" id="userDepartamento">
                                                <option value="">Cargando...</option>
                                            </select>
                                        </div>
                                        
                                        <!-- Municipio -->
                                        <div id="municipioGroup" class="mb-3" style="display: none;">
                                            <label class="form-label">Municipio *</label>
                                            <select class="form-select" id="userMunicipio" disabled>
                                                <option value="">Seleccione departamento primero</option>
                                            </select>
                                        </div>
                                        
                                        <!-- Zona -->
                                        <div id="zonaGroup" class="mb-3" style="display: none;">
                                            <label class="form-label">Zona *</label>
                                            <select class="form-select" id="userZona" disabled>
                                                <option value="">Seleccione municipio primero</option>
                                            </select>
                                        </div>
                                        
                                        <!-- Puesto -->
                                        <div id="puestoGroup" class="mb-3" style="display: none;">
                                            <label class="form-label">Puesto *</label>
                                            <select class="form-select" id="userPuesto" disabled>
                                                <option value="">Seleccione zona primero</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Contraseña *</label>
                                    <input type="password" class="form-control" id="userPassword" required>
                                    <small class="text-muted">Mínimo 6 caracteres</small>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Confirmar Contraseña *</label>
                                    <input type="password" class="form-control" id="userPasswordConfirm" required>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" onclick="guardarNuevoUsuario()">
                            <i class="bi bi-check-lg"></i> Crear Usuario
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Agregar modal al DOM si no existe
    if (!document.getElementById('createUserModal')) {
        document.body.insertAdjacentHTML('beforeend', modalHtml);
    }
    
    // Cargar departamentos
    await loadDepartamentosForUser();
    
    // Configurar eventos de cascada
    setupUserLocationCascade();
    
    // Mostrar modal
    const modal = new bootstrap.Modal(document.getElementById('createUserModal'));
    modal.show();
    
    // Limpiar modal al cerrar
    document.getElementById('createUserModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

/**
 * Manejar cambio de rol para mostrar ubicaciones correspondientes
 */
function handleRoleChange() {
    const rol = document.getElementById('userRole').value;
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
    
    // Super admin no necesita ubicación
    if (!rol || rol === 'super_admin') {
        return;
    }
    
    // Mostrar sección de ubicación
    locationSection.style.display = 'block';
    
    // Mostrar campos según el rol
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

/**
 * Cargar departamentos para el formulario de usuario
 */
async function loadDepartamentosForUser() {
    try {
        const response = await APIClient.getDepartamentos();
        if (response.success && response.data) {
            Utils.populateSelect('userDepartamento', response.data, 'departamento_codigo', 'departamento_nombre', 'Seleccione departamento');
        }
    } catch (error) {
        console.error('Error cargando departamentos:', error);
    }
}

/**
 * Configurar cascada de ubicaciones para formulario de usuario
 */
function setupUserLocationCascade() {
    // Departamento change
    document.getElementById('userDepartamento')?.addEventListener('change', async (e) => {
        const deptoId = e.target.value;
        if (!deptoId) {
            Utils.enableSelect('userMunicipio', false);
            Utils.enableSelect('userZona', false);
            Utils.enableSelect('userPuesto', false);
            return;
        }
        
        try {
            Utils.setLoading('userMunicipio', true);
            const response = await APIClient.getMunicipios(deptoId);
            Utils.populateSelect('userMunicipio', response.data, 'municipio_codigo', 'municipio_nombre', 'Seleccione municipio');
            Utils.enableSelect('userMunicipio', true);
            Utils.enableSelect('userZona', false);
            Utils.enableSelect('userPuesto', false);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            Utils.setLoading('userMunicipio', false);
        }
    });
    
    // Municipio change
    document.getElementById('userMunicipio')?.addEventListener('change', async (e) => {
        const muniId = e.target.value;
        if (!muniId) {
            Utils.enableSelect('userZona', false);
            Utils.enableSelect('userPuesto', false);
            return;
        }
        
        try {
            Utils.setLoading('userZona', true);
            const response = await APIClient.getZonas(muniId);
            Utils.populateSelect('userZona', response.data, 'zona_codigo', 'zona_nombre', 'Seleccione zona');
            Utils.enableSelect('userZona', true);
            Utils.enableSelect('userPuesto', false);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            Utils.setLoading('userZona', false);
        }
    });
    
    // Zona change
    document.getElementById('userZona')?.addEventListener('change', async (e) => {
        const zonaId = e.target.value;
        if (!zonaId) {
            Utils.enableSelect('userPuesto', false);
            return;
        }
        
        try {
            Utils.setLoading('userPuesto', true);
            const response = await APIClient.getPuestos(zonaId);
            Utils.populateSelect('userPuesto', response.data, 'puesto_codigo', 'puesto_nombre', 'Seleccione puesto');
            Utils.enableSelect('userPuesto', true);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            Utils.setLoading('userPuesto', false);
        }
    });
}

/**
 * Guardar nuevo usuario
 */
async function guardarNuevoUsuario() {
    const nombre = document.getElementById('userName').value.trim();
    const rol = document.getElementById('userRole').value;
    const password = document.getElementById('userPassword').value;
    const passwordConfirm = document.getElementById('userPasswordConfirm').value;
    
    // Validaciones
    if (!nombre || !rol || !password) {
        Utils.showError('Todos los campos son requeridos');
        return;
    }
    
    if (password.length < 6) {
        Utils.showError('La contraseña debe tener al menos 6 caracteres');
        return;
    }
    
    if (password !== passwordConfirm) {
        Utils.showError('Las contraseñas no coinciden');
        return;
    }
    
    // Obtener ubicación según el rol
    let ubicacion_data = {};
    if (rol !== 'super_admin') {
        const departamento = document.getElementById('userDepartamento')?.value;
        const municipio = document.getElementById('userMunicipio')?.value;
        const zona = document.getElementById('userZona')?.value;
        const puesto = document.getElementById('userPuesto')?.value;
        
        // Validar ubicación según rol
        if (['admin_departamental', 'coordinador_departamental', 'auditor_electoral'].includes(rol)) {
            if (!departamento) {
                Utils.showError('Debe seleccionar un departamento');
                return;
            }
            ubicacion_data = { departamento_codigo: departamento, tipo: 'departamento' };
        } else if (['admin_municipal', 'coordinador_municipal'].includes(rol)) {
            if (!departamento || !municipio) {
                Utils.showError('Debe seleccionar departamento y municipio');
                return;
            }
            ubicacion_data = { departamento_codigo: departamento, municipio_codigo: municipio, tipo: 'municipio' };
        } else if (['coordinador_puesto', 'testigo_electoral'].includes(rol)) {
            if (!departamento || !municipio || !zona || !puesto) {
                Utils.showError('Debe seleccionar departamento, municipio, zona y puesto');
                return;
            }
            ubicacion_data = { 
                departamento_codigo: departamento, 
                municipio_codigo: municipio,
                zona_codigo: zona,
                puesto_codigo: puesto,
                tipo: 'puesto'
            };
        }
    }
    
    try {
        Utils.showInfo('Creando usuario...');
        
        const response = await APIClient.post('/super-admin/users', {
            nombre: nombre,
            rol: rol,
            password: password,
            ubicacion_data: ubicacion_data,
            activo: true
        });
        
        if (response.success) {
            Utils.showSuccess('Usuario creado exitosamente');
            
            // Cerrar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('createUserModal'));
            modal.hide();
            
            // Recargar lista de usuarios
            await loadUsers();
        } else {
            Utils.showError(response.error || 'Error al crear usuario');
        }
    } catch (error) {
        console.error('Error creando usuario:', error);
        Utils.showError('Error al crear usuario: ' + error.message);
    }
}

/**
 * Editar usuario
 */
async function editUser(userId) {
    try {
        const user = allUsers.find(u => u.id === userId);
        if (!user) {
            Utils.showError('Usuario no encontrado');
            return;
        }
        
        // Crear modal de edición
        const modalHtml = `
            <div class="modal fade" id="editUserModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Editar Usuario</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="mb-3">
                                <label class="form-label">Nombre Completo *</label>
                                <input type="text" class="form-control" id="editUserNombre" value="${user.nombre}">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Rol *</label>
                                <select class="form-select" id="editUserRol">
                                    <option value="testigo_electoral" ${user.rol === 'testigo_electoral' ? 'selected' : ''}>Testigo Electoral</option>
                                    <option value="coordinador_puesto" ${user.rol === 'coordinador_puesto' ? 'selected' : ''}>Coordinador de Puesto</option>
                                    <option value="coordinador_municipal" ${user.rol === 'coordinador_municipal' ? 'selected' : ''}>Coordinador Municipal</option>
                                    <option value="coordinador_departamental" ${user.rol === 'coordinador_departamental' ? 'selected' : ''}>Coordinador Departamental</option>
                                    <option value="auditor_electoral" ${user.rol === 'auditor_electoral' ? 'selected' : ''}>Auditor Electoral</option>
                                    <option value="super_admin" ${user.rol === 'super_admin' ? 'selected' : ''}>Super Admin</option>
                                    <option value="monitoreo" ${user.rol === 'monitoreo' ? 'selected' : ''}>Monitoreo</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Ubicación</label>
                                <input type="text" class="form-control" id="editUserUbicacion" value="${user.ubicacion || ''}" readonly>
                                <small class="text-muted">La ubicación se gestiona desde la asignación de mesa/puesto</small>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                            <button type="button" class="btn btn-primary" onclick="guardarEdicionUser(${userId})">Guardar Cambios</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        const modal = new bootstrap.Modal(document.getElementById('editUserModal'));
        modal.show();
        
        document.getElementById('editUserModal').addEventListener('hidden.bs.modal', function() {
            this.remove();
        });
        
    } catch (error) {
        console.error('Error editando usuario:', error);
        Utils.showError('Error al editar usuario');
    }
}

/**
 * Guardar edición de usuario
 */
async function guardarEdicionUser(userId) {
    const nombre = document.getElementById('editUserNombre').value.trim();
    const rol = document.getElementById('editUserRol').value;
    
    if (!nombre || !rol) {
        Utils.showError('El nombre y rol son requeridos');
        return;
    }
    
    try {
        const response = await APIClient.put(`/super-admin/users/${userId}`, {
            nombre: nombre,
            rol: rol
        });
        
        if (response.success) {
            Utils.showSuccess('Usuario actualizado exitosamente');
            bootstrap.Modal.getInstance(document.getElementById('editUserModal')).hide();
            await loadUsers();
        } else {
            Utils.showError(response.error || 'Error al actualizar usuario');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al actualizar usuario');
    }
}

/**
 * Resetear contraseña de usuario
 */
async function resetUserPassword(userId) {
    try {
        const user = allUsers.find(u => u.id === userId);
        if (!user) {
            Utils.showError('Usuario no encontrado');
            return;
        }
        
        const newPassword = prompt(`Ingrese nueva contraseña para ${user.nombre}:`);
        if (!newPassword) return;
        
        if (newPassword.length < 6) {
            Utils.showError('La contraseña debe tener al menos 6 caracteres');
            return;
        }
        
        const response = await APIClient.post(`/super-admin/users/${userId}/reset-password`, {
            password: newPassword
        });
        
        if (response.success) {
            Utils.showSuccess('Contraseña reseteada exitosamente');
        } else {
            Utils.showError(response.error || 'Error al resetear contraseña');
        }
    } catch (error) {
        console.error('Error reseteando contraseña:', error);
        Utils.showError('Error al resetear contraseña');
    }
}

/**
 * Cambiar estado de usuario (activar/desactivar)
 */
async function toggleUserStatus(userId, newStatus) {
    try {
        const user = allUsers.find(u => u.id === userId);
        if (!user) {
            Utils.showError('Usuario no encontrado');
            return;
        }
        
        const action = newStatus ? 'activar' : 'desactivar';
        if (!confirm(`¿Está seguro de ${action} al usuario ${user.nombre}?`)) {
            return;
        }
        
        const response = await APIClient.put(`/super-admin/users/${userId}`, {
            activo: newStatus
        });
        
        if (response.success) {
            Utils.showSuccess(`Usuario ${action}do exitosamente`);
            await loadUsers(); // Recargar lista
        } else {
            Utils.showError(response.error || `Error al ${action} usuario`);
        }
    } catch (error) {
        console.error('Error cambiando estado de usuario:', error);
        Utils.showError('Error al cambiar estado del usuario');
    }
}

// ============================================
// CONFIGURACIÓN
// ============================================

/**
 * Cargar partidos
 * NOTA: Esta función está deshabilitada porque partidos-manager.js se encarga de cargar y renderizar
 */
async function loadPartidos() {
    // Deshabilitado - partidos-manager.js maneja la carga y renderizado
    console.log('[Super Admin] loadPartidos() deshabilitado - usando partidos-manager.js');
    return;
}

/**
 * Renderizar partidos
 * NOTA: Esta función está deshabilitada porque partidos-manager.js se encarga del renderizado
 */
function renderPartidos() {
    // Deshabilitado - partidos-manager.js maneja el renderizado
    console.log('[Super Admin] renderPartidos() deshabilitado - usando partidos-manager.js');
    return;
}

/**
 * Cargar logos de partidos desde Wikipedia
 */
async function cargarLogosPartidos() {
    if (!confirm('¿Desea cargar los logos de los partidos políticos colombianos desde Wikipedia?\n\nEsto actualizará los logos de los partidos que coincidan con los nombres estándar.')) {
        return;
    }
    
    try {
        Utils.showInfo('Cargando logos de partidos...');
        
        const response = await APIClient.post('/admin/cargar-logos-partidos', {});
        
        if (response.success) {
            const data = response.data;
            
            // Mostrar resultado detallado
            let mensaje = `✅ Logos cargados exitosamente:\n\n`;
            mensaje += `📊 Total de partidos: ${data.total_partidos}\n`;
            mensaje += `✅ Logos actualizados: ${data.total_actualizados}\n`;
            mensaje += `ℹ️  Sin cambios: ${data.total_sin_cambios}\n`;
            mensaje += `⚠️  Sin logo encontrado: ${data.total_sin_logo}\n\n`;
            
            if (data.actualizados.length > 0) {
                mensaje += `Partidos actualizados:\n`;
                data.actualizados.forEach(p => {
                    mensaje += `  • ${p.nombre}\n`;
                });
            }
            
            if (data.sin_logo.length > 0) {
                mensaje += `\nPartidos sin logo:\n`;
                data.sin_logo.forEach(p => {
                    mensaje += `  • ${p.nombre}\n`;
                });
            }
            
            alert(mensaje);
            Utils.showSuccess(response.message);
            
            // Recargar lista de partidos
            await loadPartidos();
        } else {
            Utils.showError(response.error || 'Error al cargar logos');
        }
    } catch (error) {
        console.error('Error cargando logos:', error);
        Utils.showError('Error al cargar logos: ' + error.message);
    }
}

/**
 * Cargar tipos de elección
 */
async function loadTiposEleccion() {
    try {
        console.log('[Super Admin] Cargando tipos de elección...');
        const response = await APIClient.getSuperAdminTiposEleccion();
        console.log('[Super Admin] Respuesta tipos de elección:', response);
        
        if (response.success) {
            allTiposEleccion = response.data;
            window.allTiposEleccion = allTiposEleccion; // Actualizar referencia global
            console.log('[Super Admin] Tipos de elección cargados:', allTiposEleccion.length);
            renderTiposEleccion();
        } else {
            console.error('[Super Admin] Error en respuesta:', response);
        }
    } catch (error) {
        console.error('[Super Admin] Error cargando tipos de elección:', error);
        Utils.showError('Error cargando tipos de elección: ' + error.message);
    }
}

/**
 * Renderizar tipos de elección
 */
function renderTiposEleccion() {
    const container = document.getElementById('electionTypesList');
    
    if (allTiposEleccion.length === 0) {
        container.innerHTML = '<p class="text-muted">No hay tipos de elección registrados</p>';
        return;
    }
    
    container.innerHTML = allTiposEleccion.map(tipo => {
        let detalles = [];
        if (tipo.es_uninominal) {
            detalles.push('Uninominal');
        } else {
            if (tipo.permite_lista_cerrada) detalles.push('Lista cerrada');
            if (tipo.permite_lista_abierta) detalles.push('Lista abierta');
            if (tipo.permite_coaliciones) detalles.push('Coaliciones');
        }
        
        return `
            <div class="d-flex align-items-center justify-content-between mb-2 p-2 border rounded ${!tipo.activo ? 'opacity-50' : ''}">
                <div class="flex-grow-1">
                    <strong>${tipo.nombre}</strong>
                    <br><small class="text-muted">${detalles.join(' • ')}</small>
                    ${!tipo.activo ? '<br><span class="badge bg-secondary">Deshabilitado</span>' : '<br><span class="badge bg-success">Habilitado</span>'}
                </div>
                <div class="d-flex gap-1">
                    <button class="btn btn-sm btn-${tipo.activo ? 'warning' : 'success'}" 
                            onclick="toggleTipoEleccion(${tipo.id}, ${!tipo.activo})"
                            title="${tipo.activo ? 'Deshabilitar' : 'Habilitar'}">
                        <i class="bi bi-${tipo.activo ? 'toggle-on' : 'toggle-off'}"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-info" onclick="verDetallesTipo(${tipo.id})" title="Ver detalles">
                        <i class="bi bi-info-circle"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-primary" onclick="editTipoEleccion(${tipo.id})">
                        <i class="bi bi-pencil"></i>
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Ver detalles de un tipo de elección
 */
function verDetallesTipo(tipoId) {
    const tipo = allTiposEleccion.find(t => t.id === tipoId);
    if (!tipo) return;
    
    let detallesHtml = `
        <p><strong>Nombre:</strong> ${tipo.nombre}</p>
        <p><strong>Descripción:</strong> ${tipo.descripcion || 'N/A'}</p>
        <p><strong>Tipo:</strong> ${tipo.es_uninominal ? 'Uninominal (candidato único)' : 'Por corporación (listas)'}</p>
    `;
    
    if (!tipo.es_uninominal) {
        detallesHtml += `
            <p><strong>Configuración de listas:</strong></p>
            <ul>
                <li>Lista cerrada: ${tipo.permite_lista_cerrada ? '✅ Sí' : '❌ No'}</li>
                <li>Lista abierta (voto preferente): ${tipo.permite_lista_abierta ? '✅ Sí' : '❌ No'}</li>
                <li>Coaliciones: ${tipo.permite_coaliciones ? '✅ Sí' : '❌ No'}</li>
            </ul>
        `;
    }
    
    detallesHtml += `<p><strong>Estado:</strong> ${tipo.activo ? '<span class="badge bg-success">Habilitado</span>' : '<span class="badge bg-secondary">Deshabilitado</span>'}</p>`;
    
    const modalHtml = `
        <div class="modal fade" id="detallesTipoModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Detalles del Tipo de Elección</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${detallesHtml}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('detallesTipoModal'));
    modal.show();
    
    document.getElementById('detallesTipoModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

/**
 * Cargar candidatos
 */
async function loadCandidatos() {
    try {
        console.log('[Super Admin] Cargando candidatos...');
        const response = await APIClient.getSuperAdminCandidatos();
        console.log('[Super Admin] Respuesta candidatos:', response);
        
        if (response.success) {
            allCandidatos = response.data;
            window.allCandidatos = allCandidatos; // Actualizar referencia global
            console.log('[Super Admin] Candidatos cargados:', allCandidatos.length);
            populateCandidatoFilters();
            renderCandidatos();
        } else {
            console.error('[Super Admin] Error en respuesta:', response);
        }
    } catch (error) {
        console.error('[Super Admin] Error cargando candidatos:', error);
        Utils.showError('Error cargando candidatos: ' + error.message);
    }
}

/**
 * Renderizar candidatos
 */
function renderCandidatos(candidatos = null) {
    const tbody = document.getElementById('candidatos-lista');
    const candidatosToRender = candidatos || allCandidatos;
    
    if (candidatosToRender.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4"><p class="text-muted">No hay candidatos que coincidan con los filtros</p></td></tr>';
        return;
    }
    
    tbody.innerHTML = candidatosToRender.map(candidato => `
        <tr class="${!candidato.activo ? 'opacity-50' : ''}">
            <td>${candidato.nombre_completo || candidato.nombre}</td>
            <td>${candidato.partido_nombre || 'Independiente'}</td>
            <td>${candidato.tipo_eleccion_nombre || 'N/A'}</td>
            <td>${candidato.numero_lista || '-'}</td>
            <td><span class="badge bg-${candidato.activo ? 'success' : 'secondary'}">${candidato.activo ? 'Habilitado' : 'Deshabilitado'}</span></td>
            <td>
                <button class="btn btn-sm btn-${candidato.activo ? 'warning' : 'success'}" 
                        onclick="toggleCandidato(${candidato.id}, ${!candidato.activo})"
                        title="${candidato.activo ? 'Deshabilitar' : 'Habilitar'}">
                    <i class="bi bi-${candidato.activo ? 'toggle-on' : 'toggle-off'}"></i>
                </button>
                <button class="btn btn-sm btn-outline-primary" onclick="editCandidato(${candidato.id})">
                    <i class="bi bi-pencil"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

/**
 * Filtrar candidatos
 */
function filterCandidatos() {
    const partidoFilter = document.getElementById('filterCandidatoPartido')?.value || '';
    const tipoFilter = document.getElementById('filterCandidatoTipo')?.value || '';
    const sortBy = document.getElementById('sortCandidatos')?.value || 'nombre_asc';
    const searchText = document.getElementById('searchCandidato')?.value.toLowerCase() || '';
    
    let filtered = [...allCandidatos];
    
    // Filtrar por partido
    if (partidoFilter) {
        filtered = filtered.filter(c => c.partido_nombre === partidoFilter);
    }
    
    // Filtrar por tipo de elección
    if (tipoFilter) {
        filtered = filtered.filter(c => c.tipo_eleccion_nombre === tipoFilter);
    }
    
    // Buscar por texto
    if (searchText) {
        filtered = filtered.filter(c => 
            (c.nombre_completo || c.nombre || '').toLowerCase().includes(searchText) ||
            (c.partido_nombre || '').toLowerCase().includes(searchText)
        );
    }
    
    // Ordenar
    filtered.sort((a, b) => {
        switch(sortBy) {
            case 'nombre_asc':
                return (a.nombre_completo || a.nombre || '').localeCompare(b.nombre_completo || b.nombre || '');
            case 'nombre_desc':
                return (b.nombre_completo || b.nombre || '').localeCompare(a.nombre_completo || a.nombre || '');
            case 'partido_asc':
                return (a.partido_nombre || '').localeCompare(b.partido_nombre || '');
            case 'partido_desc':
                return (b.partido_nombre || '').localeCompare(a.partido_nombre || '');
            case 'numero_asc':
                return (a.numero_lista || 999) - (b.numero_lista || 999);
            case 'numero_desc':
                return (b.numero_lista || 0) - (a.numero_lista || 0);
            default:
                return 0;
        }
    });
    
    renderCandidatos(filtered);
}

/**
 * Poblar filtros de candidatos
 */
function populateCandidatoFilters() {
    // Obtener partidos únicos
    const partidos = [...new Set(allCandidatos.map(c => c.partido_nombre).filter(Boolean))].sort();
    const partidoSelect = document.getElementById('filterCandidatoPartido');
    if (partidoSelect) {
        partidoSelect.innerHTML = '<option value="">Todos los partidos</option>' +
            partidos.map(p => `<option value="${p}">${p}</option>`).join('');
    }
    
    // Obtener tipos de elección únicos
    const tipos = [...new Set(allCandidatos.map(c => c.tipo_eleccion_nombre).filter(Boolean))].sort();
    const tipoSelect = document.getElementById('filterCandidatoTipo');
    if (tipoSelect) {
        tipoSelect.innerHTML = '<option value="">Todos los tipos</option>' +
            tipos.map(t => `<option value="${t}">${t}</option>`).join('');
    }
}

// ============================================
// ACCIONES RÁPIDAS
// ============================================

/**
 * Mostrar modal de configuración
 */
function showConfigModal() {
    alert('🔧 CONFIGURACIÓN DEL SISTEMA\n\n' +
          'Esta funcionalidad permite configurar:\n' +
          '- Parámetros generales del sistema\n' +
          '- Configuración de notificaciones\n' +
          '- Ajustes de seguridad\n\n' +
          '📝 Estado: En desarrollo\n' +
          '🎯 Disponible en: Próxima versión');
}

/**
 * Exportar todos los datos
 */
async function exportAllData() {
    alert('📥 EXPORTAR DATOS\n\n' +
          'Esta funcionalidad permite exportar:\n' +
          '- Todos los usuarios del sistema\n' +
          '- Formularios E-14 enviados\n' +
          '- Ubicaciones y mesas\n\n' +
          '📝 Estado: En desarrollo\n' +
          '🎯 Disponible en: Próxima versión');
}

/**
 * Crear respaldo
 */
async function createBackup() {
    alert('💾 CREAR RESPALDO\n\n' +
          'Esta funcionalidad permite:\n' +
          '- Crear backup completo de la BD\n' +
          '- Descargar respaldo en formato SQL\n\n' +
          '📝 Estado: En desarrollo\n' +
          '⚠️ Render hace respaldos automáticos de PostgreSQL');
}

/**
 * Exportar logs de auditoría
 */
function exportAuditLogs() {
    Utils.showInfo('Exportando logs de auditoría...');
    // TODO: Implementar exportación de logs
}

/**
 * Filtrar logs de auditoría
 */
function filterAuditLogs() {
    const user = document.getElementById('auditFilterUser').value;
    const action = document.getElementById('auditFilterAction').value;
    const date = document.getElementById('auditFilterDate').value;
    
    console.log('Filtrando logs:', { user, action, date });
    // TODO: Implementar filtrado real
}

// ============================================
// FUNCIONES DE EDICIÓN
// ============================================

// Las funciones editPartido, editTipoEleccion y editCandidato 
// están implementadas completamente más abajo (líneas 2075+)

function showCreatePartyModal() {
    const modalHtml = `
        <div class="modal fade" id="createPartyModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Crear Nuevo Partido</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label">Código *</label>
                            <input type="text" class="form-control" id="newPartidoCodigo" placeholder="Ej: PL, PC, CD">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Nombre Completo *</label>
                            <input type="text" class="form-control" id="newPartidoNombre" placeholder="Ej: Partido Liberal Colombiano">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Nombre Corto / Sigla *</label>
                            <input type="text" class="form-control" id="newPartidoNombreCorto" placeholder="Ej: Liberal, PL">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Color</label>
                            <input type="color" class="form-control" id="newPartidoColor" value="#FF0000">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Logo URL (opcional)</label>
                            <input type="text" class="form-control" id="newPartidoLogo" placeholder="https://...">
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" onclick="guardarNuevoPartido()">Crear Partido</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('createPartyModal'));
    modal.show();
    
    document.getElementById('createPartyModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

async function guardarNuevoPartido() {
    const codigo = document.getElementById('newPartidoCodigo').value.trim();
    const nombre = document.getElementById('newPartidoNombre').value.trim();
    const nombreCorto = document.getElementById('newPartidoNombreCorto').value.trim();
    const color = document.getElementById('newPartidoColor').value;
    const logoUrl = document.getElementById('newPartidoLogo').value.trim();
    
    if (!codigo || !nombre || !nombreCorto) {
        Utils.showError('El código, nombre y nombre corto son requeridos');
        return;
    }
    
    try {
        const response = await APIClient.post('/configuracion/partidos', {
            codigo: codigo,
            nombre: nombre,
            nombre_corto: nombreCorto,
            color: color,
            logo_url: logoUrl || null
        });
        
        if (response.success) {
            Utils.showSuccess('Partido creado exitosamente');
            bootstrap.Modal.getInstance(document.getElementById('createPartyModal')).hide();
            await loadPartidos();
        } else {
            Utils.showError(response.error || 'Error al crear partido');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al crear partido');
    }
}

function showCreateElectionTypeModal() {
    const modalHtml = `
        <div class="modal fade" id="createElectionTypeModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Crear Tipo de Elección</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label">Código *</label>
                            <input type="text" class="form-control" id="newTipoCodigo" placeholder="Ej: PRES, SEN, CAM">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Nombre *</label>
                            <input type="text" class="form-control" id="newTipoNombre" placeholder="Ej: Presidente, Senado">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Descripción</label>
                            <textarea class="form-control" id="newTipoDescripcion" rows="2"></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Tipo de Elección</label>
                            <select class="form-select" id="newTipoCategoria">
                                <option value="uninominal">Uninominal (Presidente, Gobernador, Alcalde)</option>
                                <option value="corporacion">Por Corporación (Senado, Cámara, Asamblea, Concejo)</option>
                            </select>
                        </div>
                        <div id="newOpcionesLista" style="display:none;">
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="newListaCerrada" checked>
                                <label class="form-check-label" for="newListaCerrada">
                                    Permite lista cerrada
                                </label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="newListaAbierta">
                                <label class="form-check-label" for="newListaAbierta">
                                    Permite lista abierta (voto preferente)
                                </label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="newCoaliciones">
                                <label class="form-check-label" for="newCoaliciones">
                                    Permite coaliciones
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" onclick="guardarNuevoTipoEleccion()">Crear Tipo</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('createElectionTypeModal'));
    
    // Manejar cambio de categoría
    document.getElementById('newTipoCategoria').addEventListener('change', function() {
        const opcionesLista = document.getElementById('newOpcionesLista');
        opcionesLista.style.display = this.value === 'corporacion' ? 'block' : 'none';
    });
    
    modal.show();
    
    document.getElementById('createElectionTypeModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

async function guardarNuevoTipoEleccion() {
    const codigo = document.getElementById('newTipoCodigo').value.trim();
    const nombre = document.getElementById('newTipoNombre').value.trim();
    const descripcion = document.getElementById('newTipoDescripcion').value.trim();
    const categoria = document.getElementById('newTipoCategoria').value;
    
    if (!codigo || !nombre) {
        Utils.showError('El código y nombre son requeridos');
        return;
    }
    
    const esUninominal = categoria === 'uninominal';
    const listaCerrada = !esUninominal && document.getElementById('newListaCerrada').checked;
    const listaAbierta = !esUninominal && document.getElementById('newListaAbierta').checked;
    const coaliciones = !esUninominal && document.getElementById('newCoaliciones').checked;
    
    try {
        const response = await APIClient.post('/super-admin/tipos-eleccion', {
            codigo: codigo,
            nombre: nombre,
            descripcion: descripcion,
            es_uninominal: esUninominal,
            permite_lista_cerrada: listaCerrada,
            permite_lista_abierta: listaAbierta,
            permite_coaliciones: coaliciones
        });
        
        if (response.success) {
            Utils.showSuccess('Tipo de elección creado exitosamente');
            bootstrap.Modal.getInstance(document.getElementById('createElectionTypeModal')).hide();
            await loadTiposEleccion();
        } else {
            Utils.showError(response.error || 'Error al crear tipo de elección');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al crear tipo de elección');
    }
}

function showCreateCandidateModal() {
    const modalHtml = `
        <div class="modal fade" id="createCandidateModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Crear Nuevo Candidato</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label">Código *</label>
                            <input type="text" class="form-control" id="newCandidatoCodigo" placeholder="Se genera automáticamente">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Nombre Completo *</label>
                            <input type="text" class="form-control" id="newCandidatoNombre" placeholder="Ej: Juan Pérez García">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Partido</label>
                            <select class="form-select" id="newCandidatoPartido">
                                <option value="">Independiente</option>
                                ${allPartidos.map(p => `<option value="${p.id}">${p.nombre}</option>`).join('')}
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Tipo de Elección *</label>
                            <select class="form-select" id="newCandidatoTipoEleccion">
                                ${allTiposEleccion.map(t => `<option value="${t.id}">${t.nombre}</option>`).join('')}
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Número de Lista (opcional)</label>
                            <input type="number" class="form-control" id="newCandidatoNumeroLista" min="1">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Foto URL (opcional)</label>
                            <input type="text" class="form-control" id="newCandidatoFoto" placeholder="https://...">
                        </div>
                        <div class="form-check mb-2">
                            <input class="form-check-input" type="checkbox" id="newCandidatoIndependiente">
                            <label class="form-check-label" for="newCandidatoIndependiente">
                                Candidato Independiente
                            </label>
                        </div>
                        <div class="form-check mb-2">
                            <input class="form-check-input" type="checkbox" id="newCandidatoCabezaLista">
                            <label class="form-check-label" for="newCandidatoCabezaLista">
                                Cabeza de Lista
                            </label>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" onclick="guardarNuevoCandidato()">Crear Candidato</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('createCandidateModal'));
    modal.show();
    
    document.getElementById('createCandidateModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

async function guardarNuevoCandidato() {
    const codigo = document.getElementById('newCandidatoCodigo').value.trim();
    const nombre = document.getElementById('newCandidatoNombre').value.trim();
    const partidoId = document.getElementById('newCandidatoPartido').value;
    const tipoEleccionId = document.getElementById('newCandidatoTipoEleccion').value;
    const numeroLista = document.getElementById('newCandidatoNumeroLista').value;
    const fotoUrl = document.getElementById('newCandidatoFoto').value.trim();
    const esIndependiente = document.getElementById('newCandidatoIndependiente').checked;
    const esCabezaLista = document.getElementById('newCandidatoCabezaLista').checked;
    
    if (!nombre || !tipoEleccionId) {
        Utils.showError('El nombre y tipo de elección son requeridos');
        return;
    }
    
    try {
        const response = await APIClient.post('/configuracion/candidatos', {
            codigo: codigo || `CAND_${Date.now()}`,
            nombre_completo: nombre,
            partido_id: partidoId || null,
            tipo_eleccion_id: parseInt(tipoEleccionId),
            numero_lista: numeroLista ? parseInt(numeroLista) : null,
            foto_url: fotoUrl || null,
            es_independiente: esIndependiente,
            es_cabeza_lista: esCabezaLista
        });
        
        if (response.success) {
            Utils.showSuccess('Candidato creado exitosamente');
            bootstrap.Modal.getInstance(document.getElementById('createCandidateModal')).hide();
            await loadCandidatos();
        } else {
            Utils.showError(response.error || 'Error al crear candidato');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al crear candidato');
    }
}

// ============================================
// FUNCIÓN DE LOGOUT
// ============================================

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


// ============================================
// CARGA MASIVA DE DATOS
// ============================================

/**
 * Cargar usuarios desde archivo Excel
 */
async function uploadUsers(input) {
    const file = input.files[0];
    if (!file) return;
    
    try {
        Utils.showInfo('Cargando usuarios...');
        
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/api/super-admin/upload/users', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showUploadResult(result, 'success');
            await loadUsers(); // Recargar lista de usuarios
        } else {
            showUploadResult(result, 'danger');
        }
        
    } catch (error) {
        console.error('Error cargando usuarios:', error);
        Utils.showError('Error al cargar usuarios: ' + error.message);
    } finally {
        input.value = ''; // Limpiar input
    }
}

/**
 * Cargar ubicaciones (DIVIPOLA) desde archivo Excel
 */
async function uploadLocations(input) {
    const file = input.files[0];
    if (!file) return;
    
    try {
        Utils.showInfo('Cargando ubicaciones...');
        
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/api/super-admin/upload/locations', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showUploadResult(result, 'success');
        } else {
            showUploadResult(result, 'danger');
        }
        
    } catch (error) {
        console.error('Error cargando ubicaciones:', error);
        Utils.showError('Error al cargar ubicaciones: ' + error.message);
    } finally {
        input.value = ''; // Limpiar input
    }
}

/**
 * Cargar partidos desde archivo Excel
 */
async function uploadPartidos(input) {
    const file = input.files[0];
    if (!file) return;
    
    try {
        Utils.showInfo('Cargando partidos...');
        
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/api/super-admin/upload/partidos', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showUploadResult(result, 'success');
            await loadPartidos(); // Recargar lista de partidos
        } else {
            showUploadResult(result, 'danger');
        }
        
    } catch (error) {
        console.error('Error cargando partidos:', error);
        Utils.showError('Error al cargar partidos: ' + error.message);
    } finally {
        input.value = ''; // Limpiar input
    }
}

/**
 * Cargar candidatos desde archivo Excel
 */
async function uploadCandidatos(input) {
    const file = input.files[0];
    if (!file) return;
    
    try {
        Utils.showInfo('Cargando candidatos...');
        
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/api/super-admin/upload/candidatos', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showUploadResult(result, 'success');
            await loadCandidatos(); // Recargar lista de candidatos
        } else {
            showUploadResult(result, 'danger');
        }
        
    } catch (error) {
        console.error('Error cargando candidatos:', error);
        Utils.showError('Error al cargar candidatos: ' + error.message);
    } finally {
        input.value = ''; // Limpiar input
    }
}

/**
 * Mostrar resultado de carga masiva
 */
function showUploadResult(result, type) {
    const resultDiv = document.getElementById('uploadResult');
    const contentDiv = document.getElementById('uploadResultContent');
    
    if (!resultDiv || !contentDiv) return;
    
    let html = '';
    
    if (result.success && result.data) {
        html = `
            <p class="mb-2"><strong>${result.message}</strong></p>
            <ul class="mb-0">
                <li>Total procesados: ${result.data.total_processed}</li>
                <li>Creados exitosamente: ${result.data.total_created}</li>
                <li>Errores: ${result.data.total_errors}</li>
            </ul>
        `;
        
        if (result.data.errors && result.data.errors.length > 0) {
            html += `
                <hr>
                <p class="mb-2"><strong>Errores encontrados:</strong></p>
                <ul class="small mb-0" style="max-height: 200px; overflow-y: auto;">
                    ${result.data.errors.map(error => `<li>${error}</li>`).join('')}
                </ul>
            `;
        }
    } else {
        html = `<p class="mb-0"><strong>Error:</strong> ${result.error || 'Error desconocido'}</p>`;
    }
    
    contentDiv.innerHTML = html;
    resultDiv.querySelector('.alert').className = `alert alert-${type}`;
    resultDiv.style.display = 'block';
    
    // Auto-ocultar después de 10 segundos si es exitoso
    if (type === 'success') {
        setTimeout(() => {
            resultDiv.style.display = 'none';
        }, 10000);
    }
}

/**
 * Descargar plantilla de usuarios (Excel con datos de ejemplo)
 */
async function downloadTemplateUsers() {
    try {
        const response = await fetch('/api/super-admin/download/template/users', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'plantilla_usuarios.xlsx';
            document.body.appendChild(a);
            a.click();
            a.remove();
            Utils.showSuccess('Plantilla de usuarios descargada con datos de ejemplo');
        } else {
            Utils.showError('Error al descargar plantilla');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al descargar plantilla: ' + error.message);
    }
}

/**
 * Descargar plantilla de ubicaciones (Excel con datos de ejemplo)
 */
async function downloadTemplateLocations() {
    try {
        const response = await fetch('/api/super-admin/download/template/locations', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'plantilla_divipola.xlsx';
            document.body.appendChild(a);
            a.click();
            a.remove();
            Utils.showSuccess('Plantilla de DIVIPOLA descargada con datos de ejemplo');
        } else {
            Utils.showError('Error al descargar plantilla');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al descargar plantilla: ' + error.message);
    }
}

/**
 * Descargar plantilla de partidos (Excel con datos de ejemplo)
 */
async function downloadTemplatePartidos() {
    try {
        const response = await fetch('/api/super-admin/download/template/partidos', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'plantilla_partidos.xlsx';
            document.body.appendChild(a);
            a.click();
            a.remove();
            Utils.showSuccess('Plantilla de partidos descargada con datos de ejemplo');
        } else {
            Utils.showError('Error al descargar plantilla');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al descargar plantilla: ' + error.message);
    }
}

/**
 * Descargar plantilla de candidatos (Excel con datos de ejemplo)
 */
async function downloadTemplateCandidatos() {
    try {
        const response = await fetch('/api/super-admin/download/template/candidatos', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'plantilla_candidatos.xlsx';
            document.body.appendChild(a);
            a.click();
            a.remove();
            Utils.showSuccess('Plantilla de candidatos descargada con datos de ejemplo');
        } else {
            Utils.showError('Error al descargar plantilla');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al descargar plantilla: ' + error.message);
    }
}

/**
 * Función auxiliar para descargar CSV
 */
function downloadCSV(content, filename) {
    const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}


// ============================================
// GESTIÓN DE HABILITACIÓN
// ============================================

/**
 * Habilitar/Deshabilitar tipo de elección
 */
async function toggleTipoEleccion(tipoId, activo) {
    try {
        const response = await APIClient.put(`/super-admin/tipos-eleccion/${tipoId}`, {
            activo: activo
        });
        
        if (response.success) {
            Utils.showSuccess(`Tipo de elección ${activo ? 'habilitado' : 'deshabilitado'} exitosamente`);
            await loadTiposEleccion();
        } else {
            Utils.showError(response.error || 'Error al actualizar tipo de elección');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al actualizar tipo de elección');
    }
}

/**
 * Habilitar/Deshabilitar partido
 */
async function togglePartido(partidoId, activo) {
    try {
        const response = await APIClient.put(`/super-admin/partidos/${partidoId}/toggle`, {
            activo: activo
        });
        
        if (response.success) {
            Utils.showSuccess(`Partido ${activo ? 'habilitado' : 'deshabilitado'} para recolección de datos`);
            await loadPartidos();
        } else {
            Utils.showError(response.error || 'Error al actualizar partido');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al actualizar partido');
    }
}

/**
 * Habilitar/Deshabilitar candidato
 */
async function toggleCandidato(candidatoId, activo) {
    try {
        const response = await APIClient.put(`/super-admin/candidatos/${candidatoId}/toggle`, {
            activo: activo
        });
        
        if (response.success) {
            Utils.showSuccess(`Candidato ${activo ? 'habilitado' : 'deshabilitado'} para recolección de datos`);
            await loadCandidatos();
        } else {
            Utils.showError(response.error || 'Error al actualizar candidato');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al actualizar candidato');
    }
}

/**
 * Habilitar/Deshabilitar tipo de elección
 */
async function toggleTipoEleccion(tipoId, activo) {
    try {
        const response = await APIClient.put(`/super-admin/tipos-eleccion/${tipoId}/toggle`, {
            activo: activo
        });
        
        if (response.success) {
            Utils.showSuccess(`Tipo de elección ${activo ? 'habilitado' : 'deshabilitado'} para recolección de datos`);
            await loadElectionTypes();
        } else {
            Utils.showError(response.error || 'Error al actualizar tipo de elección');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al actualizar tipo de elección');
    }
}

/**
 * Crear nuevo tipo de elección
 */
async function createTipoEleccion() {
    // Mostrar modal personalizado
    const modalHtml = `
        <div class="modal fade" id="createTipoEleccionModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Crear Tipo de Elección</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label">Nombre *</label>
                            <input type="text" class="form-control" id="tipoNombre" placeholder="Ej: Presidente, Senado, Cámara">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Descripción</label>
                            <textarea class="form-control" id="tipoDescripcion" rows="2"></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Tipo de Elección</label>
                            <select class="form-select" id="tipoCategoria">
                                <option value="uninominal">Uninominal (Presidente, Gobernador, Alcalde)</option>
                                <option value="corporacion">Por Corporación (Senado, Cámara, Asamblea, Concejo)</option>
                            </select>
                        </div>
                        <div id="opcionesLista" style="display:none;">
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="listaC errada" checked>
                                <label class="form-check-label" for="listaCerrada">
                                    Permite lista cerrada
                                </label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="listaAbierta">
                                <label class="form-check-label" for="listaAbierta">
                                    Permite lista abierta (voto preferente)
                                </label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="coaliciones">
                                <label class="form-check-label" for="coaliciones">
                                    Permite coaliciones
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" onclick="guardarTipoEleccion()">Crear</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Agregar modal al DOM
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('createTipoEleccionModal'));
    
    // Manejar cambio de categoría
    document.getElementById('tipoCategoria').addEventListener('change', function() {
        const opcionesLista = document.getElementById('opcionesLista');
        opcionesLista.style.display = this.value === 'corporacion' ? 'block' : 'none';
    });
    
    modal.show();
    
    // Limpiar modal al cerrar
    document.getElementById('createTipoEleccionModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

/**
 * Guardar nuevo tipo de elección
 */
async function guardarTipoEleccion() {
    const nombre = document.getElementById('tipoNombre').value.trim();
    const descripcion = document.getElementById('tipoDescripcion').value.trim();
    const categoria = document.getElementById('tipoCategoria').value;
    
    if (!nombre) {
        Utils.showError('El nombre es requerido');
        return;
    }
    
    const esUninominal = categoria === 'uninominal';
    const listaCerrada = !esUninominal && document.getElementById('listaCerrada').checked;
    const listaAbierta = !esUninominal && document.getElementById('listaAbierta').checked;
    const coaliciones = !esUninominal && document.getElementById('coaliciones').checked;
    
    try {
        const response = await APIClient.post('/super-admin/tipos-eleccion', {
            nombre: nombre,
            descripcion: descripcion,
            es_uninominal: esUninominal,
            permite_lista_cerrada: listaCerrada,
            permite_lista_abierta: listaAbierta,
            permite_coaliciones: coaliciones,
            activo: true
        });
        
        if (response.success) {
            Utils.showSuccess('Tipo de elección creado exitosamente');
            bootstrap.Modal.getInstance(document.getElementById('createTipoEleccionModal')).hide();
            await loadTiposEleccion();
        } else {
            Utils.showError(response.error || 'Error al crear tipo de elección');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al crear tipo de elección');
    }
}


// ============================================
// GESTIÓN DE CAMPAÑAS
// ============================================

let allCampanas = [];
let allTemas = [];

/**
 * Cargar campañas
 */
async function loadCampanas() {
    try {
        const response = await APIClient.get('/super-admin/campanas');
        
        if (response.success) {
            allCampanas = response.data;
            renderCampanas();
        }
    } catch (error) {
        console.error('Error cargando campañas:', error);
        Utils.showError('Error al cargar campañas');
    }
}

/**
 * Renderizar campañas
 */
function renderCampanas() {
    const container = document.getElementById('campanasContainer');
    
    if (!allCampanas || allCampanas.length === 0) {
        container.innerHTML = '<p class="text-muted text-center">No hay campañas registradas</p>';
        return;
    }
    
    container.innerHTML = allCampanas.map(campana => `
        <div class="card mb-3 ${campana.activa ? 'border-success' : ''}">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <h6 class="card-title">
                            ${campana.nombre}
                            ${campana.activa ? '<span class="badge bg-success ms-2">ACTIVA</span>' : ''}
                            ${campana.completada ? '<span class="badge bg-secondary ms-2">Completada</span>' : ''}
                        </h6>
                        <p class="card-text text-muted small">${campana.descripcion || 'Sin descripción'}</p>
                        <div class="d-flex gap-2 align-items-center">
                            <span class="badge" style="background-color: ${campana.color_primario}">Color Primario</span>
                            <span class="badge" style="background-color: ${campana.color_secundario}">Color Secundario</span>
                            ${campana.es_candidato_unico ? '<span class="badge bg-info">Candidato Único</span>' : ''}
                            ${campana.es_partido_completo ? '<span class="badge bg-warning">Partido Completo</span>' : ''}
                        </div>
                    </div>
                    <div class="btn-group-vertical">
                        ${!campana.activa ? `
                            <button class="btn btn-sm btn-success" onclick="activarCampana(${campana.id})" title="Activar campaña">
                                <i class="bi bi-check-circle"></i> Activar
                            </button>
                        ` : ''}
                        <button class="btn btn-sm btn-warning" onclick="resetCampana(${campana.id})" title="Resetear datos">
                            <i class="bi bi-arrow-clockwise"></i> Reset
                        </button>
                        ${!campana.activa ? `
                            <button class="btn btn-sm btn-danger" onclick="deleteCampana(${campana.id})" title="Eliminar campaña">
                                <i class="bi bi-trash"></i> Eliminar
                            </button>
                        ` : ''}
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

/**
 * Mostrar modal para crear campaña
 */
function showCreateCampanaModal() {
    const modalHtml = `
        <div class="modal fade" id="createCampanaModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Crear Nueva Campaña</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Nombre *</label>
                                <input type="text" class="form-control" id="campanaNombre" placeholder="Ej: Campaña Presidencial 2026">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Código</label>
                                <input type="text" class="form-control" id="campanaCodigo" placeholder="Se genera automáticamente">
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Descripción</label>
                            <textarea class="form-control" id="campanaDescripcion" rows="2"></textarea>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Fecha Inicio</label>
                                <input type="date" class="form-control" id="campanaFechaInicio">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Fecha Fin</label>
                                <input type="date" class="form-control" id="campanaFechaFin">
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Color Primario</label>
                                <input type="color" class="form-control" id="campanaColorPrimario" value="#1e3c72">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Color Secundario</label>
                                <input type="color" class="form-control" id="campanaColorSecundario" value="#2a5298">
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Tipo de Campaña</label>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="campanaCandidatoUnico">
                                <label class="form-check-label" for="campanaCandidatoUnico">
                                    Campaña de candidato único
                                </label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="campanaPartidoCompleto">
                                <label class="form-check-label" for="campanaPartidoCompleto">
                                    Campaña de partido completo (múltiples elecciones)
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" onclick="guardarCampana()">Crear Campaña</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('createCampanaModal'));
    modal.show();
    
    document.getElementById('createCampanaModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

/**
 * Guardar nueva campaña
 */
async function guardarCampana() {
    const nombre = document.getElementById('campanaNombre').value.trim();
    
    if (!nombre) {
        Utils.showError('El nombre es requerido');
        return;
    }
    
    try {
        const response = await APIClient.post('/super-admin/campanas', {
            nombre: nombre,
            codigo: document.getElementById('campanaCodigo').value.trim(),
            descripcion: document.getElementById('campanaDescripcion').value.trim(),
            fecha_inicio: document.getElementById('campanaFechaInicio').value,
            fecha_fin: document.getElementById('campanaFechaFin').value,
            color_primario: document.getElementById('campanaColorPrimario').value,
            color_secundario: document.getElementById('campanaColorSecundario').value,
            es_candidato_unico: document.getElementById('campanaCandidatoUnico').checked,
            es_partido_completo: document.getElementById('campanaPartidoCompleto').checked
        });
        
        if (response.success) {
            Utils.showSuccess('Campaña creada exitosamente');
            bootstrap.Modal.getInstance(document.getElementById('createCampanaModal')).hide();
            await loadCampanas();
        } else {
            Utils.showError(response.error || 'Error al crear campaña');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al crear campaña');
    }
}

/**
 * Activar campaña
 */
async function activarCampana(campanaId) {
    if (!confirm('¿Está seguro de activar esta campaña? Se desactivarán las demás.')) {
        return;
    }
    
    try {
        const response = await APIClient.put(`/super-admin/campanas/${campanaId}/activar`);
        
        if (response.success) {
            Utils.showSuccess('Campaña activada exitosamente');
            await loadCampanas();
        } else {
            Utils.showError(response.error || 'Error al activar campaña');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al activar campaña');
    }
}

/**
 * Resetear campaña
 */
async function resetCampana(campanaId) {
    const confirmText = prompt('Esta acción eliminará TODOS los datos de la campaña (formularios, incidentes, delitos).\\n\\nEscriba "CONFIRMAR_RESET" para continuar:');
    
    if (confirmText !== 'CONFIRMAR_RESET') {
        return;
    }
    
    try {
        const response = await APIClient.post(`/super-admin/campanas/${campanaId}/reset`, {
            confirmacion: 'CONFIRMAR_RESET'
        });
        
        if (response.success) {
            Utils.showSuccess(`Campaña reseteada. ${response.data.formularios_eliminados} formularios, ${response.data.incidentes_eliminados} incidentes y ${response.data.delitos_eliminados} delitos eliminados.`);
            await loadCampanas();
        } else {
            Utils.showError(response.error || 'Error al resetear campaña');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al resetear campaña');
    }
}

/**
 * Eliminar campaña
 */
async function deleteCampana(campanaId) {
    const confirmText = prompt('Esta acción eliminará PERMANENTEMENTE la campaña y todos sus datos.\\n\\nEscriba "CONFIRMAR_ELIMINACION" para continuar:');
    
    if (confirmText !== 'CONFIRMAR_ELIMINACION') {
        return;
    }
    
    try {
        const response = await APIClient.delete(`/super-admin/campanas/${campanaId}`, {
            confirmacion: 'CONFIRMAR_ELIMINACION'
        });
        
        if (response.success) {
            Utils.showSuccess('Campaña eliminada exitosamente');
            await loadCampanas();
        } else {
            Utils.showError(response.error || 'Error al eliminar campaña');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al eliminar campaña');
    }
}


// ============================================
// TESTING Y AUDITORÍA
// ============================================

/**
 * Cargar datos de prueba
 */
async function loadTestData() {
    if (!confirm('¿Está seguro de cargar datos de prueba?\\n\\nEsto creará:\\n- Usuarios de prueba para todos los roles\\n- Ubicaciones de ejemplo\\n- Partidos y candidatos\\n- Una campaña de prueba\\n\\nCredenciales: usuario_test / test123')) {
        return;
    }
    
    try {
        Utils.showInfo('Cargando datos de prueba... Esto puede tardar un momento.');
        
        const response = await APIClient.post('/super-admin/test/load-data', {});
        
        if (response.success) {
            Utils.showSuccess('Datos de prueba cargados exitosamente');
            
            // Mostrar detalles
            const modalHtml = `
                <div class="modal fade" id="testDataModal" tabindex="-1">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header bg-success text-white">
                                <h5 class="modal-title">✅ Datos de Prueba Cargados</h5>
                                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <h6>🔑 Credenciales de Acceso:</h6>
                                <div class="table-responsive">
                                    <table class="table table-sm">
                                        <thead>
                                            <tr>
                                                <th>Usuario</th>
                                                <th>Contraseña</th>
                                                <th>Rol</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td><code>admin_test</code></td>
                                                <td><code>test123</code></td>
                                                <td>Super Admin</td>
                                            </tr>
                                            <tr>
                                                <td><code>auditor_test</code></td>
                                                <td><code>test123</code></td>
                                                <td>Auditor</td>
                                            </tr>
                                            <tr>
                                                <td><code>coord_dept_test</code></td>
                                                <td><code>test123</code></td>
                                                <td>Coordinador Departamental</td>
                                            </tr>
                                            <tr>
                                                <td><code>coord_mun_test</code></td>
                                                <td><code>test123</code></td>
                                                <td>Coordinador Municipal</td>
                                            </tr>
                                            <tr>
                                                <td><code>coord_puesto_test</code></td>
                                                <td><code>test123</code></td>
                                                <td>Coordinador Puesto</td>
                                            </tr>
                                            <tr>
                                                <td><code>testigo_test_1</code></td>
                                                <td><code>test123</code></td>
                                                <td>Testigo</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                                <div class="alert alert-info mt-3">
                                    <strong>💡 Tip:</strong> Puede cerrar sesión y probar con cualquiera de estos usuarios para verificar las funcionalidades de cada rol.
                                </div>
                                <pre class="bg-light p-3 rounded"><code>${response.output || 'Datos cargados exitosamente'}</code></pre>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                                <button type="button" class="btn btn-primary" onclick="runSystemAudit()">
                                    <i class="bi bi-clipboard-check"></i> Ejecutar Auditoría
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            const modal = new bootstrap.Modal(document.getElementById('testDataModal'));
            modal.show();
            
            document.getElementById('testDataModal').addEventListener('hidden.bs.modal', function() {
                this.remove();
            });
            
            // Recargar datos
            await loadMainStats();
            await loadUsers();
        } else {
            Utils.showError(response.error || 'Error al cargar datos de prueba');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al cargar datos de prueba');
    }
}

/**
 * Inicializar datos electorales (partidos, candidatos, tipos de elección)
 */
async function initElectoralData() {
    if (!confirm('¿Desea inicializar los datos electorales?\n\nEsto creará:\n- 7 Tipos de Elección (Presidencia, Senado, Cámara, etc.)\n- 10 Partidos Políticos\n- 6 Candidatos de ejemplo\n\nLos datos existentes no se duplicarán.')) {
        return;
    }
    
    try {
        Utils.showInfo('Inicializando datos electorales...');
        
        const response = await APIClient.post('/super-admin/init-test-data', {});
        
        if (response.success) {
            const data = response.data;
            
            // Crear mensaje detallado
            let detailsHtml = '<ul class="list-unstyled mb-0">';
            
            if (data.tipos_eleccion.created > 0) {
                detailsHtml += `<li>✅ ${data.tipos_eleccion.created} tipos de elección creados</li>`;
            }
            if (data.tipos_eleccion.existing > 0) {
                detailsHtml += `<li>ℹ️ ${data.tipos_eleccion.existing} tipos de elección ya existían</li>`;
            }
            
            if (data.partidos.created > 0) {
                detailsHtml += `<li>✅ ${data.partidos.created} partidos creados</li>`;
            }
            if (data.partidos.existing > 0) {
                detailsHtml += `<li>ℹ️ ${data.partidos.existing} partidos ya existían</li>`;
            }
            
            if (data.candidatos.created > 0) {
                detailsHtml += `<li>✅ ${data.candidatos.created} candidatos creados</li>`;
            }
            if (data.candidatos.existing > 0) {
                detailsHtml += `<li>ℹ️ ${data.candidatos.existing} candidatos ya existían</li>`;
            }
            
            detailsHtml += '</ul>';
            
            // Mostrar modal con resultados
            const modalHtml = `
                <div class="modal fade" id="initDataModal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header bg-success text-white">
                                <h5 class="modal-title">✅ Datos Electorales Inicializados</h5>
                                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <p class="mb-3">${response.message}</p>
                                ${detailsHtml}
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                                <button type="button" class="btn btn-primary" onclick="location.reload()">
                                    <i class="bi bi-arrow-clockwise"></i> Recargar Página
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Remover modal anterior si existe
            const existingModal = document.getElementById('initDataModal');
            if (existingModal) {
                existingModal.remove();
            }
            
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            const modal = new bootstrap.Modal(document.getElementById('initDataModal'));
            modal.show();
            
            document.getElementById('initDataModal').addEventListener('hidden.bs.modal', function() {
                this.remove();
            });
            
            Utils.showSuccess('Datos electorales inicializados correctamente');
            
            // Recargar datos en el dashboard
            setTimeout(() => {
                if (typeof loadPartidosFixed === 'function') loadPartidosFixed();
                if (typeof loadCandidatosFixed === 'function') loadCandidatosFixed();
                if (typeof loadTiposEleccionFixed === 'function') loadTiposEleccionFixed();
            }, 1000);
            
        } else {
            Utils.showError(response.error || 'Error al inicializar datos');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al inicializar datos electorales');
    }
}

/**
 * Inicializar datos electorales del Caquetá
 */
async function initCaquetaData() {
    if (!confirm('¿Desea cargar los datos electorales del Caquetá?\n\nEsto creará candidatos basados en las elecciones reales:\n- Senado 2022 (~30 candidatos)\n- Cámara Caquetá 2022 (~22 candidatos)\n- Asamblea Departamental 2023 (~20 candidatos)\n\nTotal: ~72 candidatos reales')) {
        return;
    }
    
    try {
        Utils.showInfo('Cargando datos electorales del Caquetá...');
        
        const response = await APIClient.post('/super-admin/init-caqueta-data', {});
        
        if (response.success) {
            Utils.showSuccess(response.message);
            
            // Recargar datos en el dashboard
            setTimeout(() => {
                if (typeof loadCandidatosFixed === 'function') loadCandidatosFixed();
                location.reload();
            }, 2000);
            
        } else {
            Utils.showError(response.error || 'Error al cargar datos del Caquetá');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al cargar datos electorales del Caquetá');
    }
}

/**
 * Ejecutar auditoría del sistema
 */
async function runSystemAudit() {
    try {
        Utils.showInfo('Ejecutando auditoría del sistema...');
        
        const response = await APIClient.get('/super-admin/test/audit');
        
        if (response.success) {
            const audit = response.data;
            
            // Crear modal con resultados
            const checksHtml = audit.checks.map(check => {
                const icon = check.status === 'pass' ? '✅' : '❌';
                const badgeClass = check.status === 'pass' ? 'success' : 'danger';
                
                let detailsHtml = '';
                if (check.details) {
                    detailsHtml = '<ul class="small mb-0">';
                    for (const [key, value] of Object.entries(check.details)) {
                        detailsHtml += `<li>${key}: ${value}</li>`;
                    }
                    detailsHtml += '</ul>';
                }
                
                return `
                    <div class="card mb-2">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start">
                                <div>
                                    <h6 class="mb-1">${icon} ${check.name}</h6>
                                    <p class="mb-1 text-muted small">${check.message}</p>
                                    ${detailsHtml}
                                </div>
                                <span class="badge bg-${badgeClass}">${check.status.toUpperCase()}</span>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
            
            const statusClass = audit.status === 'success' ? 'success' : 'warning';
            const statusIcon = audit.status === 'success' ? '✅' : '⚠️';
            
            const modalHtml = `
                <div class="modal fade" id="auditModal" tabindex="-1">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header bg-${statusClass} text-white">
                                <h5 class="modal-title">${statusIcon} Auditoría del Sistema</h5>
                                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <div class="alert alert-${statusClass}">
                                    <strong>${audit.message}</strong>
                                    <br><small>Ejecutado: ${new Date(audit.timestamp).toLocaleString()}</small>
                                </div>
                                <h6 class="mb-3">Resultados de Verificación:</h6>
                                ${checksHtml}
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                                <button type="button" class="btn btn-primary" onclick="runSystemAudit()">
                                    <i class="bi bi-arrow-clockwise"></i> Ejecutar Nuevamente
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Remover modal anterior si existe
            const existingModal = document.getElementById('auditModal');
            if (existingModal) {
                existingModal.remove();
            }
            
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            const modal = new bootstrap.Modal(document.getElementById('auditModal'));
            modal.show();
            
            document.getElementById('auditModal').addEventListener('hidden.bs.modal', function() {
                this.remove();
            });
            
            if (audit.status === 'success') {
                Utils.showSuccess('Auditoría completada: Todos los checks pasaron');
            } else {
                Utils.showWarning('Auditoría completada con advertencias');
            }
        } else {
            Utils.showError(response.error || 'Error al ejecutar auditoría');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al ejecutar auditoría');
    }
}


// ============================================
// FUNCIONES DE EDICIÓN
// ============================================

/**
 * Editar partido
 */
async function editPartido(partidoId) {
    const partido = allPartidos.find(p => p.id === partidoId);
    if (!partido) {
        Utils.showError('Partido no encontrado');
        return;
    }
    
    const modalHtml = `
        <div class="modal fade" id="editPartidoModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Editar Partido</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label">Nombre Completo *</label>
                            <input type="text" class="form-control" id="editPartidoNombre" value="${partido.nombre}">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Nombre Corto / Sigla *</label>
                            <input type="text" class="form-control" id="editPartidoNombreCorto" value="${partido.nombre_corto || ''}">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Color</label>
                            <input type="color" class="form-control" id="editPartidoColor" value="${partido.color || '#6c757d'}">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Logo URL (opcional)</label>
                            <input type="text" class="form-control" id="editPartidoLogo" value="${partido.logo_url || ''}">
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" onclick="guardarEdicionPartido(${partidoId})">Guardar Cambios</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('editPartidoModal'));
    modal.show();
    
    document.getElementById('editPartidoModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

/**
 * Guardar edición de partido
 */
async function guardarEdicionPartido(partidoId) {
    const nombre = document.getElementById('editPartidoNombre').value.trim();
    const nombreCorto = document.getElementById('editPartidoNombreCorto').value.trim();
    const color = document.getElementById('editPartidoColor').value;
    const logoUrl = document.getElementById('editPartidoLogo').value.trim();
    
    if (!nombre || !nombreCorto) {
        Utils.showError('El nombre y nombre corto son requeridos');
        return;
    }
    
    try {
        const response = await APIClient.put(`/super-admin/partidos/${partidoId}`, {
            nombre: nombre,
            nombre_corto: nombreCorto,
            color: color,
            logo_url: logoUrl || null
        });
        
        if (response.success) {
            Utils.showSuccess('Partido actualizado exitosamente');
            bootstrap.Modal.getInstance(document.getElementById('editPartidoModal')).hide();
            await loadPartidos();
        } else {
            Utils.showError(response.error || 'Error al actualizar partido');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al actualizar partido');
    }
}

/**
 * Editar tipo de elección
 */
async function editTipoEleccion(tipoId) {
    const tipo = allTiposEleccion.find(t => t.id === tipoId);
    if (!tipo) {
        Utils.showError('Tipo de elección no encontrado');
        return;
    }
    
    const modalHtml = `
        <div class="modal fade" id="editTipoEleccionModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Editar Tipo de Elección</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label">Nombre *</label>
                            <input type="text" class="form-control" id="editTipoNombre" value="${tipo.nombre}">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Descripción</label>
                            <textarea class="form-control" id="editTipoDescripcion" rows="2">${tipo.descripcion || ''}</textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Tipo de Elección</label>
                            <select class="form-select" id="editTipoCategoria">
                                <option value="uninominal" ${tipo.es_uninominal ? 'selected' : ''}>Uninominal (Presidente, Gobernador, Alcalde)</option>
                                <option value="corporacion" ${!tipo.es_uninominal ? 'selected' : ''}>Por Corporación (Senado, Cámara, Asamblea, Concejo)</option>
                            </select>
                        </div>
                        <div id="editOpcionesLista" style="display:${tipo.es_uninominal ? 'none' : 'block'};">
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="editListaCerrada" ${tipo.permite_lista_cerrada ? 'checked' : ''}>
                                <label class="form-check-label" for="editListaCerrada">
                                    Permite lista cerrada
                                </label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="editListaAbierta" ${tipo.permite_lista_abierta ? 'checked' : ''}>
                                <label class="form-check-label" for="editListaAbierta">
                                    Permite lista abierta (voto preferente)
                                </label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="editCoaliciones" ${tipo.permite_coaliciones ? 'checked' : ''}>
                                <label class="form-check-label" for="editCoaliciones">
                                    Permite coaliciones
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" onclick="guardarEdicionTipoEleccion(${tipoId})">Guardar Cambios</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('editTipoEleccionModal'));
    
    // Manejar cambio de categoría
    document.getElementById('editTipoCategoria').addEventListener('change', function() {
        const opcionesLista = document.getElementById('editOpcionesLista');
        opcionesLista.style.display = this.value === 'corporacion' ? 'block' : 'none';
    });
    
    modal.show();
    
    document.getElementById('editTipoEleccionModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

/**
 * Guardar edición de tipo de elección
 */
async function guardarEdicionTipoEleccion(tipoId) {
    const nombre = document.getElementById('editTipoNombre').value.trim();
    const descripcion = document.getElementById('editTipoDescripcion').value.trim();
    const categoria = document.getElementById('editTipoCategoria').value;
    
    if (!nombre) {
        Utils.showError('El nombre es requerido');
        return;
    }
    
    const esUninominal = categoria === 'uninominal';
    const listaCerrada = !esUninominal && document.getElementById('editListaCerrada').checked;
    const listaAbierta = !esUninominal && document.getElementById('editListaAbierta').checked;
    const coaliciones = !esUninominal && document.getElementById('editCoaliciones').checked;
    
    try {
        const response = await APIClient.put(`/super-admin/tipos-eleccion/${tipoId}`, {
            nombre: nombre,
            descripcion: descripcion,
            es_uninominal: esUninominal,
            permite_lista_cerrada: listaCerrada,
            permite_lista_abierta: listaAbierta,
            permite_coaliciones: coaliciones
        });
        
        if (response.success) {
            Utils.showSuccess('Tipo de elección actualizado exitosamente');
            bootstrap.Modal.getInstance(document.getElementById('editTipoEleccionModal')).hide();
            await loadTiposEleccion();
        } else {
            Utils.showError(response.error || 'Error al actualizar tipo de elección');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al actualizar tipo de elección');
    }
}

/**
 * Editar candidato
 */
async function editCandidato(candidatoId) {
    const candidato = allCandidatos.find(c => c.id === candidatoId);
    if (!candidato) {
        Utils.showError('Candidato no encontrado');
        return;
    }
    
    const modalHtml = `
        <div class="modal fade" id="editCandidatoModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Editar Candidato</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label">Nombre Completo *</label>
                            <input type="text" class="form-control" id="editCandidatoNombre" value="${candidato.nombre_completo || candidato.nombre}">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Partido</label>
                            <select class="form-select" id="editCandidatoPartido">
                                <option value="">Independiente</option>
                                ${allPartidos.map(p => `
                                    <option value="${p.id}" ${p.id === candidato.partido_id ? 'selected' : ''}>${p.nombre}</option>
                                `).join('')}
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Tipo de Elección *</label>
                            <select class="form-select" id="editCandidatoTipoEleccion">
                                ${allTiposEleccion.map(t => `
                                    <option value="${t.id}" ${t.id === candidato.tipo_eleccion_id ? 'selected' : ''}>${t.nombre}</option>
                                `).join('')}
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Número de Lista (opcional)</label>
                            <input type="number" class="form-control" id="editCandidatoNumeroLista" value="${candidato.numero_lista || ''}" min="1">
                            <small class="text-muted">Solo para elecciones por listas</small>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Foto URL (opcional)</label>
                            <input type="text" class="form-control" id="editCandidatoFoto" value="${candidato.foto_url || ''}">
                        </div>
                        <div class="form-check mb-2">
                            <input class="form-check-input" type="checkbox" id="editCandidatoIndependiente" ${candidato.es_independiente ? 'checked' : ''}>
                            <label class="form-check-label" for="editCandidatoIndependiente">
                                Candidato Independiente
                            </label>
                        </div>
                        <div class="form-check mb-2">
                            <input class="form-check-input" type="checkbox" id="editCandidatoCabezaLista" ${candidato.es_cabeza_lista ? 'checked' : ''}>
                            <label class="form-check-label" for="editCandidatoCabezaLista">
                                Cabeza de Lista
                            </label>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" onclick="guardarEdicionCandidato(${candidatoId})">Guardar Cambios</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('editCandidatoModal'));
    modal.show();
    
    document.getElementById('editCandidatoModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

/**
 * Guardar edición de candidato
 */
async function guardarEdicionCandidato(candidatoId) {
    const nombre = document.getElementById('editCandidatoNombre').value.trim();
    const partidoId = document.getElementById('editCandidatoPartido').value;
    const tipoEleccionId = document.getElementById('editCandidatoTipoEleccion').value;
    const numeroLista = document.getElementById('editCandidatoNumeroLista').value;
    const fotoUrl = document.getElementById('editCandidatoFoto').value.trim();
    const esIndependiente = document.getElementById('editCandidatoIndependiente').checked;
    const esCabezaLista = document.getElementById('editCandidatoCabezaLista').checked;
    
    if (!nombre || !tipoEleccionId) {
        Utils.showError('El nombre y tipo de elección son requeridos');
        return;
    }
    
    try {
        const response = await APIClient.put(`/super-admin/candidatos/${candidatoId}`, {
            nombre_completo: nombre,
            partido_id: partidoId || null,
            tipo_eleccion_id: parseInt(tipoEleccionId),
            numero_lista: numeroLista ? parseInt(numeroLista) : null,
            foto_url: fotoUrl || null,
            es_independiente: esIndependiente,
            es_cabeza_lista: esCabezaLista
        });
        
        if (response.success) {
            Utils.showSuccess('Candidato actualizado exitosamente');
            bootstrap.Modal.getInstance(document.getElementById('editCandidatoModal')).hide();
            await loadCandidatos();
        } else {
            Utils.showError(response.error || 'Error al actualizar candidato');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al actualizar candidato');
    }
}

// Nota: La inicialización se hace desde el template HTML
// No agregar addEventListener aquí para evitar doble inicialización


/**
 * Arreglar contraseñas - Actualizar todas a texto plano
 */
async function fixPasswords() {
    if (!confirm('¿Actualizar todas las contraseñas a texto plano?\n\nEsto NO borrará datos, solo actualizará las contraseñas.')) {
        return;
    }
    
    try {
        Utils.showInfo('Actualizando contraseñas...');
        
        const response = await APIClient.post('/admin/fix-passwords', {});
        
        if (response.success) {
            let message = '✅ Contraseñas actualizadas exitosamente!\n\n';
            message += 'CONTRASEÑAS:\n';
            for (const [rol, password] of Object.entries(response.passwords)) {
                message += `${rol}: ${password}\n`;
            }
            
            alert(message);
            Utils.showSuccess('Contraseñas actualizadas. Puedes seguir usando el sistema.');
        } else {
            Utils.showError('Error al actualizar contraseñas: ' + (response.error || 'Error desconocido'));
        }
    } catch (error) {
        console.error('Error actualizando contraseñas:', error);
        Utils.showError('Error al actualizar contraseñas: ' + error.message);
    }
}

/**
 * Resetear base de datos
 * ADVERTENCIA: Esto borrará todos los datos y recreará la BD desde cero
 */
async function resetDatabase() {
    // Confirmación múltiple para evitar borrados accidentales
    if (!confirm('⚠️ ADVERTENCIA: Esto borrará TODA la base de datos y la recreará desde cero.\n\n¿Estás seguro de que quieres continuar?')) {
        return;
    }
    
    if (!confirm('⚠️ ÚLTIMA CONFIRMACIÓN: Se perderán TODOS los datos actuales.\n\nLa aplicación se reiniciará automáticamente.\n\n¿Continuar?')) {
        return;
    }
    
    try {
        Utils.showInfo('Reseteando base de datos...');
        
        const response = await APIClient.post('/admin/reset-database', {});
        
        if (response.success) {
            Utils.showSuccess('✅ Base de datos reseteada. La aplicación se reiniciará en 5 segundos...');
            
            // Esperar 5 segundos y recargar la página
            setTimeout(() => {
                // Limpiar tokens
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user_data');
                
                // Redirigir al login
                window.location.href = '/auth/login';
            }, 5000);
        } else {
            Utils.showError('Error al resetear base de datos: ' + (response.error || 'Error desconocido'));
        }
    } catch (error) {
        console.error('Error reseteando base de datos:', error);
        Utils.showError('Error al resetear base de datos: ' + error.message);
    }
}


/**
 * Corregir roles de usuarios
 */
async function fixRoles() {
    if (!confirm('¿Corregir roles de usuarios de prueba?\n\nEsto actualizará:\n- admin → super_admin\n- testigo → testigo_electoral\n- coordinador_puesto → coordinador_puesto\n- coordinador_municipal → coordinador_municipal\n- coordinador_departamental → coordinador_departamental\n\nTambién reseteará contraseñas y desbloqueará cuentas.')) {
        return;
    }
    
    try {
        Utils.showInfo('Corrigiendo roles...');
        
        const response = await APIClient.post('/admin/fix-roles', {});
        
        if (response.success) {
            let message = '✅ Roles corregidos exitosamente!\n\n';
            message += `Total de cambios: ${response.message}\n\n`;
            message += 'RESULTADOS:\n';
            
            for (const resultado of response.resultados) {
                message += `\n${resultado.usuario}: ${resultado.status}`;
                if (resultado.cambios.length > 0) {
                    message += '\n  - ' + resultado.cambios.join('\n  - ');
                }
            }
            
            message += '\n\n⚠️ IMPORTANTE:\n';
            for (const nota of response.importante) {
                message += `- ${nota}\n`;
            }
            
            alert(message);
            Utils.showSuccess('Roles corregidos. Todos los usuarios deben cerrar sesión y volver a iniciar sesión.');
            
            // Recargar estadísticas
            await loadMainStats();
        } else {
            Utils.showError('Error al corregir roles: ' + (response.error || 'Error desconocido'));
        }
    } catch (error) {
        console.error('Error corrigiendo roles:', error);
        Utils.showError('Error al corregir roles: ' + error.message);
    }
}

/**
 * Ejecutar diagnóstico del sistema
 */
async function runDiagnostico() {
    try {
        Utils.showInfo('Ejecutando diagnóstico...');
        
        const response = await APIClient.get('/admin/diagnostico');
        
        if (response.success) {
            const data = response.data;
            
            let message = '📊 DIAGNÓSTICO DEL SISTEMA\n\n';
            
            // Estadísticas
            message += '=== ESTADÍSTICAS ===\n';
            message += `Total de usuarios: ${data.estadisticas.total_usuarios}\n`;
            message += `Usuarios activos: ${data.estadisticas.usuarios_activos}\n`;
            message += `Usuarios bloqueados: ${data.estadisticas.usuarios_bloqueados}\n`;
            message += `Usuarios inactivos: ${data.estadisticas.usuarios_inactivos}\n\n`;
            
            // Roles
            message += '=== USUARIOS POR ROL ===\n';
            for (const [rol, count] of Object.entries(data.roles)) {
                message += `${rol}: ${count}\n`;
            }
            message += '\n';
            
            // Usuarios de prueba
            message += '=== USUARIOS DE PRUEBA ===\n';
            for (const user of data.usuarios_prueba) {
                message += `\n${user.nombre}:\n`;
                message += `  Rol: ${user.rol}\n`;
                message += `  Activo: ${user.activo ? 'Sí' : 'No'}\n`;
                message += `  Bloqueado: ${user.bloqueado ? 'Sí' : 'No'}\n`;
                if (user.presencia_verificada !== null) {
                    message += `  Presencia: ${user.presencia_verificada ? 'Verificada' : 'No verificada'}\n`;
                }
            }
            message += '\n';
            
            // Problemas
            if (data.problemas.length > 0) {
                message += '=== ⚠️ PROBLEMAS DETECTADOS ===\n';
                for (const problema of data.problemas) {
                    message += `- ${problema}\n`;
                }
            } else {
                message += '=== ✅ NO HAY PROBLEMAS ===\n';
            }
            
            message += '\n';
            message += `Base de datos: ${data.database_url}\n`;
            
            alert(message);
            Utils.showSuccess('Diagnóstico completado');
        } else {
            Utils.showError('Error al ejecutar diagnóstico: ' + (response.error || 'Error desconocido'));
        }
    } catch (error) {
        console.error('Error ejecutando diagnóstico:', error);
        Utils.showError('Error al ejecutar diagnóstico: ' + error.message);
    }
}


/**
 * Cargar datos de prueba
 */
async function loadTestData() {
    if (!confirm('¿Está seguro de cargar datos de prueba?\n\nEsto creará usuarios, formularios y datos de ejemplo en el sistema.')) {
        return;
    }
    
    try {
        Utils.showInfo('Cargando datos de prueba...');
        
        const response = await APIClient.post('/super-admin/test/load-data', {});
        
        if (response.success) {
            Utils.showSuccess('Datos de prueba cargados exitosamente');
            
            // Recargar estadísticas
            await loadMainStats();
            await loadUsers();
        } else {
            Utils.showError(response.error || 'Error al cargar datos de prueba');
        }
    } catch (error) {
        console.error('Error cargando datos de prueba:', error);
        Utils.showError('Error al cargar datos de prueba: ' + error.message);
    }
}

/**
 * Ejecutar auditoría del sistema
 */
async function runSystemAudit() {
    try {
        Utils.showInfo('Ejecutando auditoría del sistema...');
        
        const response = await APIClient.get('/super-admin/test/audit');
        
        if (response.success) {
            const audit = response.data;
            
            let message = '📊 AUDITORÍA DEL SISTEMA\n\n';
            message += '=== ESTADÍSTICAS ===\n';
            message += `Total usuarios: ${audit.total_usuarios || 0}\n`;
            message += `Total ubicaciones: ${audit.total_ubicaciones || 0}\n`;
            message += `Total formularios: ${audit.total_formularios || 0}\n\n`;
            
            message += '=== PROBLEMAS DETECTADOS ===\n';
            if (audit.problemas && audit.problemas.length > 0) {
                audit.problemas.forEach(p => {
                    message += `⚠️ ${p}\n`;
                });
            } else {
                message += '✅ No se detectaron problemas\n';
            }
            
            alert(message);
            Utils.showSuccess('Auditoría completada');
        } else {
            Utils.showError(response.error || 'Error al ejecutar auditoría');
        }
    } catch (error) {
        console.error('Error ejecutando auditoría:', error);
        Utils.showError('Error al ejecutar auditoría: ' + error.message);
    }
}


/**
 * Cargar logs de auditoría
 */
async function loadAuditLogs() {
    try {
        const response = await APIClient.get('/super-admin/audit-logs?limit=50');
        
        if (response.success) {
            renderAuditLogs(response.data);
        }
    } catch (error) {
        console.error('Error cargando logs de auditoría:', error);
        const tbody = document.getElementById('auditLogsTableBody');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4"><p class="text-muted">Error al cargar logs de auditoría</p></td></tr>';
        }
    }
}

/**
 * Renderizar logs de auditoría
 */
function renderAuditLogs(logs) {
    const tbody = document.getElementById('auditLogsTableBody');
    if (!tbody) return;
    
    if (!logs || logs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4"><p class="text-muted">No hay logs de auditoría disponibles</p></td></tr>';
        return;
    }
    
    tbody.innerHTML = logs.map(log => `
        <tr>
            <td>${log.id}</td>
            <td>${log.user_nombre}</td>
            <td><span class="badge bg-info">${log.accion}</span></td>
            <td>${log.recurso || 'N/A'}</td>
            <td><small>${log.ip_address || 'N/A'}</small></td>
            <td><small>${Utils.formatDateTime(log.created_at)}</small></td>
        </tr>
    `).join('');
}

/**
 * Cargar incidentes y delitos
 */
async function loadIncidentesDelitos() {
    try {
        const response = await APIClient.get('/super-admin/incidentes-delitos');
        
        if (response.success) {
            renderIncidentesDelitos(response.data);
        }
    } catch (error) {
        console.error('Error cargando incidentes y delitos:', error);
        Utils.showError('Error al cargar incidentes y delitos');
    }
}

/**
 * Renderizar incidentes y delitos
 */
function renderIncidentesDelitos(data) {
    // Renderizar incidentes
    const incidentesTbody = document.getElementById('incidentesTableBody');
    if (incidentesTbody) {
        if (!data.incidentes || data.incidentes.length === 0) {
            incidentesTbody.innerHTML = '<tr><td colspan="7" class="text-center py-4"><p class="text-muted">No hay incidentes reportados</p></td></tr>';
        } else {
            incidentesTbody.innerHTML = data.incidentes.map(inc => {
                const severidadBadge = getSeveridadBadge(inc.severidad);
                const estadoBadge = getEstadoBadge(inc.estado);
                
                return `
                    <tr>
                        <td>${inc.id}</td>
                        <td>
                            <strong>${inc.titulo}</strong><br>
                            <small class="text-muted">${inc.descripcion.substring(0, 50)}...</small>
                        </td>
                        <td>${severidadBadge}</td>
                        <td>
                            <strong>${inc.reportado_por}</strong><br>
                            <small class="text-muted">${inc.reportado_por_rol}</small>
                        </td>
                        <td>
                            <small>${inc.ubicacion}</small>
                        </td>
                        <td>${estadoBadge}</td>
                        <td><small>${Utils.formatDateTime(inc.fecha_reporte)}</small></td>
                    </tr>
                `;
            }).join('');
        }
    }
    
    // Renderizar delitos
    const delitosTbody = document.getElementById('delitosTableBody');
    if (delitosTbody) {
        if (!data.delitos || data.delitos.length === 0) {
            delitosTbody.innerHTML = '<tr><td colspan="7" class="text-center py-4"><p class="text-muted">No hay delitos reportados</p></td></tr>';
        } else {
            delitosTbody.innerHTML = data.delitos.map(delito => {
                const gravedadBadge = getGravedadBadge(delito.gravedad);
                const estadoBadge = getEstadoBadge(delito.estado);
                
                return `
                    <tr>
                        <td>${delito.id}</td>
                        <td>
                            <strong>${delito.titulo}</strong><br>
                            <small class="text-muted">${delito.descripcion.substring(0, 50)}...</small>
                        </td>
                        <td>${gravedadBadge}</td>
                        <td>
                            <strong>${delito.reportado_por}</strong><br>
                            <small class="text-muted">${delito.reportado_por_rol}</small>
                        </td>
                        <td>
                            <small>${delito.ubicacion}</small>
                        </td>
                        <td>${estadoBadge}</td>
                        <td><small>${Utils.formatDateTime(delito.fecha_reporte)}</small></td>
                    </tr>
                `;
            }).join('');
        }
    }
    
    // Actualizar contadores
    const incidentesCount = document.getElementById('totalIncidentes');
    const delitosCount = document.getElementById('totalDelitos');
    if (incidentesCount) incidentesCount.textContent = data.total_incidentes || 0;
    if (delitosCount) delitosCount.textContent = data.total_delitos || 0;
}

/**
 * Obtener badge de severidad
 */
function getSeveridadBadge(severidad) {
    const badges = {
        'baja': '<span class="badge bg-secondary">Baja</span>',
        'media': '<span class="badge bg-info">Media</span>',
        'alta': '<span class="badge bg-warning">Alta</span>',
        'critica': '<span class="badge bg-danger">Crítica</span>'
    };
    return badges[severidad] || '<span class="badge bg-secondary">N/A</span>';
}

/**
 * Obtener badge de gravedad
 */
function getGravedadBadge(gravedad) {
    const badges = {
        'leve': '<span class="badge bg-secondary">Leve</span>',
        'grave': '<span class="badge bg-warning">Grave</span>',
        'muy_grave': '<span class="badge bg-danger">Muy Grave</span>'
    };
    return badges[gravedad] || '<span class="badge bg-secondary">N/A</span>';
}

/**
 * Obtener badge de estado
 */
function getEstadoBadge(estado) {
    const badges = {
        'reportado': '<span class="badge bg-warning">Reportado</span>',
        'en_revision': '<span class="badge bg-info">En Revisión</span>',
        'en_investigacion': '<span class="badge bg-info">En Investigación</span>',
        'resuelto': '<span class="badge bg-success">Resuelto</span>',
        'cerrado': '<span class="badge bg-secondary">Cerrado</span>',
        'desestimado': '<span class="badge bg-secondary">Desestimado</span>'
    };
    return badges[estado] || '<span class="badge bg-secondary">N/A</span>';
}

// Agregar event listeners para cargar datos al cambiar de pestaña
document.addEventListener('DOMContentLoaded', function() {
    // Pestaña de auditoría
    const auditTab = document.getElementById('auditoria-tab');
    if (auditTab) {
        auditTab.addEventListener('shown.bs.tab', function() {
            loadAuditLogs();
        });
    }
    
    // Pestaña de incidentes
    const incidentesTab = document.getElementById('incidentes-tab');
    if (incidentesTab) {
        incidentesTab.addEventListener('shown.bs.tab', function() {
            loadIncidentesDelitos();
        });
    }
    
    // Pestaña de monitoreo
    const monitoreoTab = document.getElementById('monitoreo-tab');
    if (monitoreoTab) {
        monitoreoTab.addEventListener('shown.bs.tab', function() {
            loadMonitoreoDepartamental();
        });
    }
});


// ============================================
// FUNCIONES DE IMPORTACIÓN DE DATOS
// ============================================

/**
 * Descargar template de partidos
 */
async function descargarTemplatePartidos() {
    try {
        const response = await fetch('/api/admin/import/partidos/template', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `template_partidos_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            Utils.showSuccess('✅ Plantilla descargada');
        } else {
            throw new Error('Error al descargar plantilla');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al descargar plantilla');
    }
}

/**
 * Descargar template de candidatos
 */
async function descargarTemplateCandidatos() {
    try {
        const response = await fetch('/api/admin/import/candidatos/template', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `template_candidatos_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            Utils.showSuccess('✅ Plantilla descargada');
        } else {
            throw new Error('Error al descargar plantilla');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al descargar plantilla');
    }
}

/**
 * Importar partidos desde CSV
 */
async function importarPartidos() {
    try {
        const fileInput = document.getElementById('filePartidos');
        const resultadoDiv = document.getElementById('resultadoPartidos');
        
        if (!fileInput.files || fileInput.files.length === 0) {
            Utils.showError('Seleccione un archivo CSV');
            return;
        }
        
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        
        Utils.showInfo('Importando partidos...');
        resultadoDiv.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div> Procesando...';
        
        const response = await fetch('/api/admin/import/partidos', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            const { creados, actualizados, errores } = data.data;
            
            let html = `
                <div class="alert alert-success">
                    <strong>✅ Importación completada</strong><br>
                    Creados: ${creados}<br>
                    Actualizados: ${actualizados}
                </div>
            `;
            
            if (errores && errores.length > 0) {
                html += `
                    <div class="alert alert-warning">
                        <strong>⚠️ Errores encontrados:</strong>
                        <ul class="mb-0 mt-2">
                            ${errores.map(e => `<li>${e}</li>`).join('')}
                        </ul>
                    </div>
                `;
            }
            
            resultadoDiv.innerHTML = html;
            Utils.showSuccess(`✅ ${creados} partidos creados, ${actualizados} actualizados`);
            
            // Limpiar input
            fileInput.value = '';
        } else {
            throw new Error(data.error || 'Error al importar');
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('resultadoPartidos').innerHTML = `
            <div class="alert alert-danger">
                <strong>❌ Error:</strong> ${error.message}
            </div>
        `;
        Utils.showError('Error al importar partidos');
    }
}

/**
 * Importar candidatos desde CSV
 */
async function importarCandidatos() {
    try {
        const fileInput = document.getElementById('fileCandidatos');
        const resultadoDiv = document.getElementById('resultadoCandidatos');
        
        if (!fileInput.files || fileInput.files.length === 0) {
            Utils.showError('Seleccione un archivo CSV');
            return;
        }
        
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        
        Utils.showInfo('Importando candidatos...');
        resultadoDiv.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div> Procesando...';
        
        const response = await fetch('/api/admin/import/candidatos', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            const { creados, actualizados, errores } = data.data;
            
            let html = `
                <div class="alert alert-success">
                    <strong>✅ Importación completada</strong><br>
                    Creados: ${creados}<br>
                    Actualizados: ${actualizados}
                </div>
            `;
            
            if (errores && errores.length > 0) {
                html += `
                    <div class="alert alert-warning">
                        <strong>⚠️ Errores encontrados:</strong>
                        <ul class="mb-0 mt-2">
                            ${errores.map(e => `<li>${e}</li>`).join('')}
                        </ul>
                    </div>
                `;
            }
            
            resultadoDiv.innerHTML = html;
            Utils.showSuccess(`✅ ${creados} candidatos creados, ${actualizados} actualizados`);
            
            // Limpiar input
            fileInput.value = '';
        } else {
            throw new Error(data.error || 'Error al importar');
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('resultadoCandidatos').innerHTML = `
            <div class="alert alert-danger">
                <strong>❌ Error:</strong> ${error.message}
            </div>
        `;
        Utils.showError('Error al importar candidatos');
    }
}

/**
 * Subir logo de partido
 */
async function subirLogoPartido() {
    try {
        const codigoInput = document.getElementById('codigoPartidoLogo');
        const fileInput = document.getElementById('logoPartido');
        const resultadoDiv = document.getElementById('resultadoLogo');
        
        const codigo = codigoInput.value.trim();
        
        if (!codigo) {
            Utils.showError('Ingrese el código del partido');
            return;
        }
        
        if (!fileInput.files || fileInput.files.length === 0) {
            Utils.showError('Seleccione un archivo de imagen');
            return;
        }
        
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        
        Utils.showInfo('Subiendo logo...');
        resultadoDiv.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div> Subiendo...';
        
        const response = await fetch(`/api/admin/import/logos/partido/${codigo}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultadoDiv.innerHTML = `
                <div class="alert alert-success">
                    <strong>✅ Logo subido exitosamente</strong><br>
                    <img src="${data.data.logo_url}" alt="Logo" style="max-width: 100px; margin-top: 10px;">
                </div>
            `;
            Utils.showSuccess('✅ Logo subido exitosamente');
            
            // Limpiar inputs
            codigoInput.value = '';
            fileInput.value = '';
        } else {
            throw new Error(data.error || 'Error al subir logo');
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('resultadoLogo').innerHTML = `
            <div class="alert alert-danger">
                <strong>❌ Error:</strong> ${error.message}
            </div>
        `;
        Utils.showError('Error al subir logo');
    }
}

/**
 * Subir foto de candidato
 */
async function subirFotoCandidato() {
    try {
        const codigoInput = document.getElementById('codigoCandidatoFoto');
        const fileInput = document.getElementById('fotoCandidato');
        const resultadoDiv = document.getElementById('resultadoFoto');
        
        const codigo = codigoInput.value.trim();
        
        if (!codigo) {
            Utils.showError('Ingrese el código del candidato');
            return;
        }
        
        if (!fileInput.files || fileInput.files.length === 0) {
            Utils.showError('Seleccione un archivo de imagen');
            return;
        }
        
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        
        Utils.showInfo('Subiendo foto...');
        resultadoDiv.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div> Subiendo...';
        
        const response = await fetch(`/api/admin/import/fotos/candidato/${codigo}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultadoDiv.innerHTML = `
                <div class="alert alert-success">
                    <strong>✅ Foto subida exitosamente</strong><br>
                    <img src="${data.data.foto_url}" alt="Foto" style="max-width: 100px; margin-top: 10px;">
                </div>
            `;
            Utils.showSuccess('✅ Foto subida exitosamente');
            
            // Limpiar inputs
            codigoInput.value = '';
            fileInput.value = '';
        } else {
            throw new Error(data.error || 'Error al subir foto');
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('resultadoFoto').innerHTML = `
            <div class="alert alert-danger">
                <strong>❌ Error:</strong> ${error.message}
            </div>
        `;
        Utils.showError('Error al subir foto');
    }
}


/**
 * Toggle mostrar/ocultar contraseña en la tabla de usuarios
 */
function togglePassword(userId) {
    const passwordInput = document.getElementById(`pwd-${userId}`);
    const eyeIcon = document.getElementById(`eye-${userId}`);
    
    if (passwordInput && eyeIcon) {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        if (type === 'text') {
            eyeIcon.classList.remove('bi-eye');
            eyeIcon.classList.add('bi-eye-slash');
        } else {
            eyeIcon.classList.remove('bi-eye-slash');
            eyeIcon.classList.add('bi-eye');
        }
    }
}
