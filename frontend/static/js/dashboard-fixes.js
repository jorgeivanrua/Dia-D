/**
 * Correcciones Rápidas para Dashboards
 * Asegura que todos los dashboards funcionen correctamente
 */

console.log('🔧 Cargando correcciones de dashboards...');

// ============================================================================
// CORRECCIÓN 1: Asegurar que window.cacheManager existe
// ============================================================================
if (typeof window.cacheManager === 'undefined') {
    console.warn('⚠️ CacheManager no encontrado, creando versión simple...');
    window.cacheManager = {
        cache: {},
        get: function(key) {
            const item = this.cache[key];
            if (!item) return null;
            if (Date.now() > item.expiry) {
                delete this.cache[key];
                return null;
            }
            return item.data;
        },
        set: function(key, data, ttl = 300000) {
            this.cache[key] = {
                data: data,
                expiry: Date.now() + ttl
            };
        },
        clear: function(key) {
            if (key) {
                delete this.cache[key];
            } else {
                this.cache = {};
            }
        }
    };
}

// ============================================================================
// CORRECCIÓN 2: Asegurar que window.lazyLoadManager existe
// ============================================================================
if (typeof window.lazyLoadManager === 'undefined') {
    console.warn('⚠️ LazyLoadManager no encontrado, creando versión simple...');
    window.lazyLoadManager = {
        observe: function(selector) {
            // Versión simple: cargar todas las imágenes inmediatamente
            const images = document.querySelectorAll(selector);
            images.forEach(img => {
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                }
            });
        }
    };
}

// ============================================================================
// CORRECCIÓN 3: Funciones globales para Super Admin
// ============================================================================

/**
 * Cargar usuarios con manejo de errores
 */
window.loadUsersWithOptimizations = async function() {
    try {
        console.log('📥 Cargando usuarios...');
        const response = await APIClient.get('/super-admin/users');
        
        if (response.success && response.data) {
            console.log(`✅ ${response.data.length} usuarios cargados`);
            
            // Actualizar tabla
            const tbody = document.querySelector('#usersTable tbody');
            if (tbody) {
                if (response.data.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="6" class="text-center">No hay usuarios registrados</td></tr>';
                } else {
                    tbody.innerHTML = response.data.map(user => `
                        <tr>
                            <td>${user.id}</td>
                            <td>${user.nombre}</td>
                            <td>${user.rol}</td>
                            <td>${user.ubicacion_nombre || 'Sin asignar'}</td>
                            <td>
                                <span class="badge ${user.activo ? 'bg-success' : 'bg-danger'}">
                                    ${user.activo ? 'Activo' : 'Inactivo'}
                                </span>
                            </td>
                            <td>
                                <button class="btn btn-sm btn-primary" onclick="editUser(${user.id})">
                                    <i class="bi bi-pencil"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('');
                }
            }
            
            // Actualizar contador
            const userCount = document.getElementById('userCount');
            if (userCount) {
                userCount.textContent = response.data.length;
            }
        }
    } catch (error) {
        console.error('❌ Error cargando usuarios:', error);
        const tbody = document.querySelector('#usersTable tbody');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Error al cargar usuarios</td></tr>';
        }
    }
};

/**
 * Cargar partidos con caché
 */
window.loadPartidosWithCache = async function() {
    try {
        console.log('📥 Cargando partidos...');
        
        // Intentar caché
        let partidos = window.cacheManager.get('partidos');
        
        if (!partidos) {
            const response = await APIClient.get('/super-admin/partidos');
            if (response.success && response.data) {
                partidos = response.data;
                window.cacheManager.set('partidos', partidos, 300000); // 5 min
            }
        }
        
        if (partidos) {
            console.log(`✅ ${partidos.length} partidos cargados`);
            
            // Actualizar tabla
            const tbody = document.querySelector('#partidosTable tbody');
            if (tbody) {
                if (partidos.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="5" class="text-center">No hay partidos registrados</td></tr>';
                } else {
                    tbody.innerHTML = partidos.map(partido => `
                        <tr>
                            <td>${partido.id}</td>
                            <td>
                                <span class="badge" style="background-color: ${partido.color}">
                                    ${partido.nombre_corto}
                                </span>
                            </td>
                            <td>${partido.nombre}</td>
                            <td>
                                <span class="badge ${partido.activo ? 'bg-success' : 'bg-danger'}">
                                    ${partido.activo ? 'Activo' : 'Inactivo'}
                                </span>
                            </td>
                            <td>
                                <button class="btn btn-sm btn-primary" onclick="editPartido(${partido.id})">
                                    <i class="bi bi-pencil"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('');
                }
            }
        }
    } catch (error) {
        console.error('❌ Error cargando partidos:', error);
    }
};

/**
 * Cargar tipos de elección con caché
 */
window.loadTiposEleccionWithCache = async function() {
    try {
        console.log('📥 Cargando tipos de elección...');
        
        let tipos = window.cacheManager.get('tipos_eleccion');
        
        if (!tipos) {
            const response = await APIClient.get('/super-admin/tipos-eleccion');
            if (response.success && response.data) {
                tipos = response.data;
                window.cacheManager.set('tipos_eleccion', tipos, 300000);
            }
        }
        
        if (tipos) {
            console.log(`✅ ${tipos.length} tipos de elección cargados`);
            
            const tbody = document.querySelector('#tiposEleccionTable tbody');
            if (tbody) {
                if (tipos.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="4" class="text-center">No hay tipos de elección registrados</td></tr>';
                } else {
                    tbody.innerHTML = tipos.map(tipo => `
                        <tr>
                            <td>${tipo.id}</td>
                            <td>${tipo.nombre}</td>
                            <td>
                                <span class="badge ${tipo.activo ? 'bg-success' : 'bg-danger'}">
                                    ${tipo.activo ? 'Activo' : 'Inactivo'}
                                </span>
                            </td>
                            <td>
                                <button class="btn btn-sm btn-primary" onclick="editTipoEleccion(${tipo.id})">
                                    <i class="bi bi-pencil"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('');
                }
            }
        }
    } catch (error) {
        console.error('❌ Error cargando tipos de elección:', error);
    }
};

/**
 * Cargar candidatos con caché
 */
window.loadCandidatosWithCache = async function() {
    try {
        console.log('📥 Cargando candidatos...');
        
        let candidatos = window.cacheManager.get('candidatos');
        
        if (!candidatos) {
            const response = await APIClient.get('/super-admin/candidatos');
            if (response.success && response.data) {
                candidatos = response.data;
                window.cacheManager.set('candidatos', candidatos, 300000);
            }
        }
        
        if (candidatos) {
            console.log(`✅ ${candidatos.length} candidatos cargados`);
            
            const tbody = document.querySelector('#candidatosTable tbody');
            if (tbody) {
                if (candidatos.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="5" class="text-center">No hay candidatos registrados</td></tr>';
                } else {
                    tbody.innerHTML = candidatos.map(candidato => `
                        <tr>
                            <td>${candidato.id}</td>
                            <td>${candidato.nombre_completo}</td>
                            <td>${candidato.partido_nombre || 'Sin partido'}</td>
                            <td>${candidato.tipo_eleccion_nombre || 'Sin tipo'}</td>
                            <td>
                                <span class="badge ${candidato.activo ? 'bg-success' : 'bg-danger'}">
                                    ${candidato.activo ? 'Activo' : 'Inactivo'}
                                </span>
                            </td>
                            <td>
                                <button class="btn btn-sm btn-primary" onclick="editCandidato(${candidato.id})">
                                    <i class="bi bi-pencil"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('');
                }
            }
        }
    } catch (error) {
        console.error('❌ Error cargando candidatos:', error);
    }
};

// ============================================================================
// CORRECCIÓN 4: Funciones para Dashboard de Testigo
// ============================================================================

/**
 * Mostrar botones de acción en dashboard de testigo
 */
window.showTestigoButtons = function() {
    // Botón de nuevo formulario
    const btnNuevoFormulario = document.getElementById('btnNuevoFormulario');
    if (btnNuevoFormulario) {
        btnNuevoFormulario.classList.remove('d-none');
        btnNuevoFormulario.style.display = 'inline-flex';
    }
    
    // Botones de incidentes y delitos
    const btnReportarIncidente = document.querySelector('[onclick="reportarIncidente()"]');
    if (btnReportarIncidente) {
        btnReportarIncidente.classList.remove('d-none');
        btnReportarIncidente.style.display = 'inline-flex';
    }
    
    const btnReportarDelito = document.querySelector('[onclick="reportarDelito()"]');
    if (btnReportarDelito) {
        btnReportarDelito.classList.remove('d-none');
        btnReportarDelito.style.display = 'inline-flex';
    }
    
    console.log('✅ Botones de testigo mostrados');
};

/**
 * Habilitar botón de nuevo formulario
 */
window.enableNewFormButton = function() {
    const btn = document.getElementById('btnNuevoFormulario');
    if (btn) {
        btn.disabled = false;
        btn.title = 'Crear nuevo formulario E-14';
        console.log('✅ Botón de nuevo formulario habilitado');
    }
};

// ============================================================================
// CORRECCIÓN 5: Auto-inicialización
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Aplicando correcciones de dashboards...');
    
    // Detectar qué dashboard estamos
    const path = window.location.pathname;
    
    if (path.includes('super-admin') || path.includes('admin')) {
        console.log('📊 Dashboard de Super Admin detectado');
        
        // Esperar un poco para que otros scripts carguen
        setTimeout(() => {
            // Si initSuperAdminDashboard no existe, crear una versión básica
            if (typeof window.initSuperAdminDashboard === 'undefined') {
                console.warn('⚠️ initSuperAdminDashboard no encontrado, creando versión básica...');
                window.initSuperAdminDashboard = async function() {
                    console.log('🚀 Inicializando Super Admin Dashboard (versión básica)...');
                    
                    try {
                        await loadUsersWithOptimizations();
                        await loadPartidosWithCache();
                        await loadTiposEleccionWithCache();
                        await loadCandidatosWithCache();
                        
                        console.log('✅ Dashboard inicializado');
                    } catch (error) {
                        console.error('❌ Error inicializando dashboard:', error);
                    }
                };
                
                // Inicializar
                window.initSuperAdminDashboard();
            }
        }, 500);
    }
    
    if (path.includes('testigo')) {
        console.log('📊 Dashboard de Testigo detectado');
        
        // Mostrar botones
        setTimeout(() => {
            showTestigoButtons();
        }, 500);
    }
});

console.log('✅ Correcciones de dashboards cargadas');
