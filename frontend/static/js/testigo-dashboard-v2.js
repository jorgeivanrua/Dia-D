/**
 * Dashboard del Testigo Electoral - Versión Completa
 */
let currentUser = null;
let userLocation = null;
let selectedMesa = null;
let mesaSeleccionadaDashboard = null;
let presenciaVerificada = false;
let tiposEleccion = [];
let partidosData = [];
let candidatosData = [];
let votosData = {};
let autoRefreshInterval = null;

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Inicializando dashboard de testigo...');
    
    // Cargar datos esenciales
    loadUserProfile();
    loadForms();
    loadTiposEleccion();
    
    // Cargar tipos de incidentes y delitos (opcional, no bloquea)
    loadTiposIncidentes().catch(err => console.warn('No se pudieron cargar tipos de incidentes:', err));
    loadTiposDelitos().catch(err => console.warn('No se pudieron cargar tipos de delitos:', err));
    
    // Los botones ya están deshabilitados por defecto en el HTML
    // No es necesario llamar a habilitarBotonNuevoFormulario() aquí
    
    // Inicializar SyncManager para sincronización automática
    if (window.syncManager) {
        window.syncManager.init();
    }
    
    console.log('✅ Dashboard inicializado');
    
    // ⭐ MEJORA: Auto-refresh cada 30 segundos
    autoRefreshInterval = setInterval(() => {
        loadForms();  // Actualizar formularios
        if (presenciaVerificada && mesaSeleccionadaDashboard) {
            actualizarPanelMesas();  // Actualizar estado de mesas
        }
    }, 30000);
    
    // ⭐ SINCRONIZACIÓN AUTOMÁTICA cada 5 minutos
    setInterval(() => {
        sincronizarTodosDatosLocales(true);  // Sincronizar silenciosamente
    }, 300000);  // 5 minutos
    
    // Sincronizar al cargar (después de 10 segundos)
    setTimeout(() => {
        sincronizarTodosDatosLocales(true);
    }, 10000);
    
    // setupImagePreview se llama cuando se abre el modal
});

// Limpiar interval al salir
window.addEventListener('beforeunload', function() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
});

/**
 * Verificar presencia del testigo en la mesa seleccionada
 */
async function verificarPresencia() {
    try {
        console.log('=== INICIANDO VERIFICACIÓN DE PRESENCIA ===');
        
        // Verificar que haya una mesa seleccionada
        const selectorMesa = document.getElementById('mesa');
        console.log('Selector mesa:', selectorMesa);
        console.log('Valor seleccionado:', selectorMesa?.value);
        
        if (!selectorMesa.value) {
            if (window.Utils) Utils.showError('Debe seleccionar una mesa primero');
            else alert('Debe seleccionar una mesa primero');
            return;
        }
        
        // Obtener datos de la mesa seleccionada
        const selectedOption = selectorMesa.options[selectorMesa.selectedIndex];
        console.log('Opción seleccionada:', selectedOption);
        console.log('Dataset mesa:', selectedOption?.dataset?.mesa);
        
        if (!selectedOption || !selectedOption.dataset.mesa) {
            if (window.Utils) Utils.showError('Error al obtener datos de la mesa');
            else alert('Error al obtener datos de la mesa');
            return;
        }
        
        mesaSeleccionadaDashboard = JSON.parse(selectedOption.dataset.mesa);
        console.log('Mesa seleccionada dashboard:', mesaSeleccionadaDashboard);
        
        // Llamar al endpoint de verificación de presencia
        console.log('Llamando a API registrar-presencia con mesa_id:', mesaSeleccionadaDashboard.id);
        const response = await APIClient.post('/testigo/registrar-presencia', {
            mesa_id: mesaSeleccionadaDashboard.id
        });
        
        console.log('Respuesta de API:', response);
        
        if (response.success) {
            console.log('✅ Presencia verificada exitosamente');
            
            // IMPORTANTE: Actualizar TODAS las variables globales (igual que incidentes-delitos.js)
            presenciaVerificada = true;
            window.presenciaVerificada = true;
            window.mesaSeleccionadaDashboard = mesaSeleccionadaDashboard;
            
            // También guardar en localStorage como respaldo
            localStorage.setItem('presenciaVerificada', 'true');
            localStorage.setItem('mesaVerificadaId', mesaSeleccionadaDashboard.id);
            localStorage.setItem('mesaVerificadaData', JSON.stringify(mesaSeleccionadaDashboard));
            
            console.log('✅ Variables globales actualizadas:');
            console.log('  - presenciaVerificada (local):', presenciaVerificada);
            console.log('  - window.presenciaVerificada:', window.presenciaVerificada);
            console.log('  - mesaSeleccionadaDashboard (local):', mesaSeleccionadaDashboard);
            console.log('  - window.mesaSeleccionadaDashboard:', window.mesaSeleccionadaDashboard);
            console.log('  - localStorage presenciaVerificada:', localStorage.getItem('presenciaVerificada'));
            console.log('  - localStorage mesaVerificadaData:', localStorage.getItem('mesaVerificadaData'));
            
            // Actualizar UI
            document.getElementById('btnVerificarPresencia').classList.add('d-none');
            document.getElementById('alertaPresenciaVerificada').classList.remove('d-none');
            
            // Actualizar casilla de estado
            const statEstado = document.getElementById('statEstado');
            const statEstadoTexto = document.getElementById('statEstadoTexto');
            if (statEstado) {
                statEstado.innerHTML = '<i class="bi bi-check-circle-fill"></i>';
                statEstado.style.color = '#28a745';
            }
            if (statEstadoTexto) {
                statEstadoTexto.textContent = 'Verificado';
            }
            
            // Mostrar fecha de verificación
            const fechaElement = document.getElementById('presenciaFecha');
            if (fechaElement && response.data.presencia_verificada_at) {
                const fecha = new Date(response.data.presencia_verificada_at);
                // Usar zona horaria de Colombia (America/Bogota)
                const opciones = { 
                    timeZone: 'America/Bogota',
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit',
                    hour12: false
                };
                const fechaColombia = fecha.toLocaleString('es-CO', opciones);
                fechaElement.textContent = `Verificada el ${fechaColombia}`;
            }
            
            // Habilitar botones de nuevo formulario directamente (desktop y móvil)
            console.log('🔧 Habilitando botones de formulario...');
            console.log('🔧 Todos los elementos con ID en el documento:', document.querySelectorAll('[id]').length);
            
            // Función para habilitar botones - MÉTODO DIRECTO
            const habilitarBotones = () => {
                console.log('🔍 Habilitando botones de formulario...');
                
                // Buscar por ID (método más confiable)
                const btnDesktop = document.getElementById('btnNuevoFormulario');
                const btnMobile = document.getElementById('btnNuevoFormularioMobile');
                
                console.log('  - btnDesktop encontrado:', !!btnDesktop);
                console.log('  - btnMobile encontrado:', !!btnMobile);
                
                if (btnDesktop) {
                    btnDesktop.disabled = false;
                    btnDesktop.classList.remove('disabled');
                    btnDesktop.title = 'Crear nuevo formulario E-14';
                    console.log('  ✅ btnNuevoFormulario HABILITADO');
                } else {
                    console.error('  ❌ btnNuevoFormulario NO ENCONTRADO');
                    // Buscar todos los botones para debug
                    const todosBotones = document.querySelectorAll('button');
                    console.log('  📋 Total de botones en la página:', todosBotones.length);
                    todosBotones.forEach((btn, i) => {
                        if (btn.textContent.includes('Formulario')) {
                            console.log(`    Botón ${i}:`, {
                                id: btn.id,
                                text: btn.textContent.trim().substring(0, 30),
                                disabled: btn.disabled
                            });
                        }
                    });
                }
                
                if (btnMobile) {
                    btnMobile.disabled = false;
                    btnMobile.classList.remove('disabled');
                    btnMobile.title = 'Crear nuevo formulario E-14';
                    console.log('  ✅ btnNuevoFormularioMobile HABILITADO');
                } else {
                    console.warn('  ⚠️ btnNuevoFormularioMobile NO ENCONTRADO (puede ser normal en desktop)');
                }
                
                console.log('✅ Habilitación completada');
            };
            
            // Intentar múltiples veces para asegurar que funcione
            habilitarBotones();
            setTimeout(habilitarBotones, 100);
            setTimeout(habilitarBotones, 300);
            setTimeout(habilitarBotones, 500);
            setTimeout(habilitarBotones, 1000);
            
            // Mostrar mensaje de éxito
            if (window.Utils && typeof window.Utils.showSuccess === 'function') {
                Utils.showSuccess('Presencia verificada exitosamente');
            } else {
                alert('Presencia verificada exitosamente');
            }
        } else {
            console.error('❌ Respuesta no exitosa:', response);
        }
    } catch (error) {
        console.error('❌ Error al verificar presencia:', error);
        if (window.Utils) Utils.showError('Error al verificar presencia: ' + error.message);
        else alert('Error al verificar presencia: ' + error.message);
    }
}

/**
 * Habilitar o deshabilitar el botón de nuevo formulario (desktop y móvil)
 */
function habilitarBotonNuevoFormulario() {
    const btnDesktop = document.getElementById('btnNuevoFormulario');
    const btnMobile = document.getElementById('btnNuevoFormularioMobile');
    
    console.log('habilitarBotonNuevoFormulario called');
    console.log('presenciaVerificada:', presenciaVerificada);
    console.log('mesaSeleccionadaDashboard:', mesaSeleccionadaDashboard);
    
    const habilitado = presenciaVerificada && mesaSeleccionadaDashboard;
    
    // Botón desktop
    if (btnDesktop) {
        btnDesktop.disabled = !habilitado;
        if (habilitado) {
            btnDesktop.classList.remove('disabled');
            btnDesktop.title = 'Crear nuevo formulario E-14';
            console.log('✅ Botón desktop habilitado');
        } else {
            btnDesktop.classList.add('disabled');
            btnDesktop.title = 'Debe seleccionar una mesa y verificar presencia primero';
            console.log('❌ Botón desktop deshabilitado');
        }
    }
    
    // Botón móvil
    if (btnMobile) {
        btnMobile.disabled = !habilitado;
        if (habilitado) {
            btnMobile.classList.remove('disabled');
            btnMobile.title = 'Crear nuevo formulario E-14';
            console.log('✅ Botón móvil habilitado');
        } else {
            btnMobile.classList.add('disabled');
            btnMobile.title = 'Debe seleccionar una mesa y verificar presencia primero';
            console.log('❌ Botón móvil deshabilitado');
        }
    }
}

/**
 * Mostrar formulario para crear nuevo E-14
 */
async function showCreateForm() {
    try {
        console.log('=== ABRIENDO FORMULARIO E-14 ===');
        
        // SIEMPRE restaurar desde localStorage primero (es la fuente de verdad)
        const verificadaLS = localStorage.getItem('presenciaVerificada') === 'true';
        const mesaDataLS = localStorage.getItem('mesaVerificadaData');
        
        console.log('📦 Restaurando desde localStorage:');
        console.log('  - presenciaVerificada:', verificadaLS);
        console.log('  - mesaVerificadaData:', mesaDataLS ? 'existe' : 'null');
        
        if (verificadaLS && mesaDataLS) {
            // Restaurar TODAS las variables
            window.presenciaVerificada = true;
            presenciaVerificada = true;
            window.mesaSeleccionadaDashboard = JSON.parse(mesaDataLS);
            mesaSeleccionadaDashboard = JSON.parse(mesaDataLS);
            console.log('✅ Variables restauradas desde localStorage');
            console.log('  - Mesa:', window.mesaSeleccionadaDashboard.mesa_codigo);
        } else {
            console.error('❌ No hay presencia verificada en localStorage');
            if (window.Utils) Utils.showError('Debe seleccionar una mesa y verificar su presencia antes de crear formularios');
            else alert('Debe seleccionar una mesa y verificar su presencia antes de crear formularios');
            return;
        }
        
        console.log('✅ Verificación exitosa, abriendo formulario...');
        
        // Limpiar formulario
        const form = document.getElementById('e14Form');
        if (form) {
            form.reset();
        }
        votosData = {};
        
        // Limpiar preview de imagen
        const imagePreview = document.getElementById('imagePreview');
        if (imagePreview) {
            imagePreview.innerHTML = '<p class="text-muted">Toque el botón para tomar una foto</p>';
        }
        
        // Habilitar tipo de elección
        const tipoEleccionSelect = document.getElementById('tipoEleccion');
        if (tipoEleccionSelect) {
            tipoEleccionSelect.disabled = false;
        }
        
        // Cargar TODAS las mesas del puesto en el selector
        const mesaSelect = document.getElementById('mesaFormulario');
        if (mesaSelect && userLocation) {
            console.log('Cargando mesas del puesto...');
            
            try {
                // Obtener todas las mesas del puesto
                const params = {
                    puesto_codigo: userLocation.puesto_codigo,
                    zona_codigo: userLocation.zona_codigo,
                    municipio_codigo: userLocation.municipio_codigo,
                    departamento_codigo: userLocation.departamento_codigo
                };
                
                console.log('Params para cargar mesas:', params);
                
                const response = await APIClient.get('/locations/mesas', params);
                const mesas = response.data || [];
                
                console.log('Mesas cargadas:', mesas);
                
                // Limpiar selector
                mesaSelect.innerHTML = '<option value="">Seleccione una mesa...</option>';
                
                // Agregar todas las mesas
                mesas.forEach(mesa => {
                    const option = document.createElement('option');
                    option.value = mesa.id;
                    option.textContent = `Mesa ${mesa.mesa_codigo} - ${mesa.puesto_nombre || ''} (${mesa.total_votantes_registrados || 0} votantes)`;
                    option.dataset.mesa = JSON.stringify(mesa);
                    
                    // Pre-seleccionar la mesa actual si existe
                    if (mesaSeleccionadaDashboard && mesa.id === mesaSeleccionadaDashboard.id) {
                        option.selected = true;
                    }
                    
                    mesaSelect.appendChild(option);
                });
                
                // Habilitar el selector para que pueda cambiar de mesa
                mesaSelect.disabled = false;
                
                console.log('✅ Mesas cargadas en selector:', mesas.length);
                console.log('Mesa pre-seleccionada:', mesaSelect.value);
                
                // Si hay una mesa pre-seleccionada, cargar sus votantes
                if (mesaSelect.value) {
                    console.log('Llamando a cambiarMesaFormulario...');
                    await cambiarMesaFormulario();
                } else {
                    console.warn('No hay mesa pre-seleccionada');
                }
                
            } catch (error) {
                console.error('Error cargando mesas:', error);
                Utils.showError('Error al cargar mesas del puesto');
            }
        }
        
        // Mostrar modal
        const modalElement = document.getElementById('formModal');
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
            
            // Configurar preview de imagen cuando se muestre el modal
            modalElement.addEventListener('shown.bs.modal', function() {
                setupImagePreview();
            }, { once: true });
        }
        
    } catch (error) {
        console.error('Error al abrir formulario:', error);
        Utils.showError('Error al abrir formulario: ' + error.message);
    }
}

async function loadUserProfile() {
    try {
        const response = await APIClient.getProfile();
        if (response.success) {
            currentUser = response.data.user;
            userLocation = response.data.ubicacion;
            const contexto = response.data.contexto;
            
            console.log('User profile loaded:', currentUser);
            console.log('User location:', userLocation);
            console.log('Contexto:', contexto);
            
            // ⭐ MEJORA: Mostrar información de contexto
            if (contexto) {
                mostrarContextoTestigo(contexto);
            }
            
            // SOLO para testigos: verificar presencia manualmente
            // Los otros roles se verifican automáticamente
            if (userLocation) {
                // Si es testigo y ya verificó presencia
                if (currentUser.rol === 'testigo_electoral' && userLocation.tipo === 'mesa' && currentUser.presencia_verificada) {
                    mesaSeleccionadaDashboard = userLocation;
                    presenciaVerificada = true;
                    
                    // Mostrar que ya verificó presencia
                    const btnVerificar = document.getElementById('btnVerificarPresencia');
                    const alertaVerificada = document.getElementById('alertaPresenciaVerificada');
                    
                    if (btnVerificar) btnVerificar.classList.add('d-none');
                    if (alertaVerificada) alertaVerificada.classList.remove('d-none');
                    
                    if (currentUser.presencia_verificada_at) {
                        const fecha = new Date(currentUser.presencia_verificada_at);
                        const fechaElement = document.getElementById('presenciaFecha');
                        if (fechaElement) {
                            fechaElement.textContent = 
                                `Verificada el ${fecha.toLocaleDateString()} a las ${fecha.toLocaleTimeString()}`;
                        }
                    }
                    
                    // Habilitar botón de nuevo formulario
                    habilitarBotonNuevoFormulario();
                }
                
                // Cargar mesas disponibles del puesto
                if (userLocation.puesto_codigo) {
                    await loadMesas();
                    await actualizarPanelMesas();
                }
            }
        }
    } catch (error) {
        console.error('Error al cargar perfil:', error);
        Utils.showError('Error al cargar perfil: ' + error.message);
    }
}

/**
 * ⭐ NUEVA FUNCIÓN: Mostrar información de contexto del testigo
 */
function mostrarContextoTestigo(contexto) {
    if (!contexto) return;
    
    // Mostrar información del puesto
    if (contexto.puesto) {
        const puestoInfo = document.getElementById('puestoInfo');
        if (puestoInfo) {
            puestoInfo.textContent = `${contexto.puesto.nombre} - ${contexto.puesto.total_mesas} mesa(s)`;
        }
    }
    
    // Mostrar estadísticas de formularios
    if (contexto.mis_formularios) {
        const stats = contexto.mis_formularios;
        
        // Mostrar panel de estadísticas
        const panelEstadisticas = document.getElementById('estadisticasTestigo');
        if (panelEstadisticas) {
            panelEstadisticas.style.display = 'flex';
        }
        
        // Actualizar contadores
        const totalElement = document.getElementById('totalFormularios');
        if (totalElement) totalElement.textContent = stats.total;
        
        const validadosElement = document.getElementById('formulariosValidados');
        if (validadosElement) validadosElement.textContent = stats.validados;
        
        const pendientesElement = document.getElementById('formulariosPendientes');
        if (pendientesElement) pendientesElement.textContent = stats.pendientes;
        
        const rechazadosElement = document.getElementById('formulariosRechazados');
        if (rechazadosElement) rechazadosElement.textContent = stats.rechazados;
        
        const porcentajeElement = document.getElementById('porcentajeCompletado');
        if (porcentajeElement) {
            porcentajeElement.textContent = stats.porcentaje_completado.toFixed(1) + '%';
        }
        
        console.log('✅ Estadísticas de formularios mostradas:', stats);
    }
}

async function loadMesas() {
    try {
        const params = {
            puesto_codigo: userLocation.puesto_codigo,
            zona_codigo: userLocation.zona_codigo,
            municipio_codigo: userLocation.municipio_codigo,
            departamento_codigo: userLocation.departamento_codigo
        };
        
        console.log('Loading mesas with params:', params);
        
        const response = await APIClient.get('/locations/mesas', params);
        const mesas = response.data;
        
        console.log('Mesas loaded:', mesas);
        
        const selector = document.getElementById('mesa');
        selector.innerHTML = '<option value="">Seleccione mesa...</option>';
        
        mesas.forEach(mesa => {
            const option = document.createElement('option');
            option.value = mesa.id;
            option.textContent = `Mesa ${mesa.mesa_codigo} - ${mesa.puesto_nombre}`;
            option.dataset.mesa = JSON.stringify(mesa);
            selector.appendChild(option);
        });
        
        // Si solo hay una mesa, seleccionarla automáticamente
        if (mesas.length === 1) {
            selector.value = mesas[0].id;
            cambiarMesa();
        }
    } catch (error) {
        console.error('Error loading mesas:', error);
        Utils.showError('Error cargando mesas del puesto');
    }
}

function cambiarMesa() {
    const selector = document.getElementById('mesa');
    const selectedOption = selector.options[selector.selectedIndex];
    
    if (selectedOption && selectedOption.dataset.mesa) {
        selectedMesa = JSON.parse(selectedOption.dataset.mesa);
        mesaSeleccionadaDashboard = selectedMesa;
        
        // Resetear verificación de presencia al cambiar de mesa
        presenciaVerificada = false;
        document.getElementById('btnVerificarPresencia').classList.remove('d-none');
        document.getElementById('alertaPresenciaVerificada').classList.add('d-none');
        
        // Deshabilitar botón de nuevo formulario
        habilitarBotonNuevoFormulario();
        
        // Recargar formularios de esta mesa
        loadForms();
        
        // Actualizar panel lateral con todas las mesas
        actualizarPanelMesas();
    }
}

/**
 * Cambiar mesa en el formulario E-14 y cargar votantes registrados
 */
async function cambiarMesaFormulario() {
    console.log('=== cambiarMesaFormulario llamada ===');
    const selector = document.getElementById('mesaFormulario');
    console.log('Selector encontrado:', !!selector);
    
    if (!selector) {
        console.error('❌ No se encontró el selector mesaFormulario');
        return;
    }
    
    const selectedOption = selector.options[selector.selectedIndex];
    console.log('Opción seleccionada:', selectedOption);
    console.log('Dataset mesa:', selectedOption?.dataset?.mesa);
    
    if (selectedOption && selectedOption.dataset.mesa) {
        const mesaData = JSON.parse(selectedOption.dataset.mesa);
        console.log('Mesa data parseada:', mesaData);
        
        // Actualizar votantes registrados desde DIVIPOLA
        const votantesInput = document.getElementById('votantesRegistrados');
        console.log('Input votantes encontrado:', !!votantesInput);
        
        if (votantesInput) {
            const votantes = mesaData.total_votantes_registrados || 0;
            
            if (votantes > 0) {
                // Si hay datos del censo, usar esos y bloquear el campo
                votantesInput.value = votantes;
                votantesInput.readOnly = true;
                votantesInput.title = 'Total de personas habilitadas para votar en esta mesa según el censo electoral (DIVIPOLA)';
                console.log('✅ Votantes registrados desde DIVIPOLA:', votantes, 'para mesa:', mesaData.mesa_codigo);
            } else {
                // Si no hay datos del censo, permitir ingreso manual
                votantesInput.value = '';
                votantesInput.readOnly = false;
                votantesInput.required = true;
                votantesInput.placeholder = 'Ingrese número de votantes';
                votantesInput.title = 'Ingrese el total de votantes registrados en esta mesa (dato del E-14 físico)';
                console.log('⚠️ No hay datos de DIVIPOLA, permitiendo ingreso manual para mesa:', mesaData.mesa_codigo);
            }
        } else {
            console.error('❌ No se encontró el input votantesRegistrados');
        }
        
        console.log('Mesa seleccionada en formulario:', mesaData);
    } else {
        console.warn('⚠️ No hay opción seleccionada o no tiene dataset.mesa');
        // Limpiar votantes si no hay mesa seleccionada
        const votantesInput = document.getElementById('votantesRegistrados');
        if (votantesInput) {
            votantesInput.value = '';
        }
    }
}

/**
 * ⭐ MEJORADO: Actualizar panel de mesas del puesto
 */
async function actualizarPanelMesas() {
    try {
        const panelContainer = document.getElementById('panelMesasPuesto');
        if (!panelContainer) return;
        
        // Verificar que userLocation esté definido
        if (!userLocation || !userLocation.puesto_codigo) {
            panelContainer.innerHTML = `<p class="text-muted text-center py-3">Cargando mesas...</p>`;
            return;
        }
        
        // Obtener todas las mesas del puesto
        const params = {
            puesto_codigo: userLocation.puesto_codigo,
            zona_codigo: userLocation.zona_codigo,
            municipio_codigo: userLocation.municipio_codigo,
            departamento_codigo: userLocation.departamento_codigo
        };
        
        const response = await APIClient.get('/locations/mesas', params);
        const mesas = response.data || [];
        
        // Actualizar contador
        const totalBadge = document.getElementById('totalMesasPuesto');
        if (totalBadge) totalBadge.textContent = mesas.length;
        
        // Obtener formularios para saber qué mesas tienen E-14
        let formularios = [];
        try {
            const formulariosResponse = await APIClient.getFormulariosE14({});
            formularios = formulariosResponse.success ? (formulariosResponse.data.formularios || formulariosResponse.data || []) : [];
        } catch (error) {
            console.warn('No se pudieron cargar formularios:', error);
        }
        
        // Crear mapa de mesas con formularios
        const mesasConFormularios = {};
        formularios.forEach(form => {
            if (!mesasConFormularios[form.mesa_id]) {
                mesasConFormularios[form.mesa_id] = [];
            }
            mesasConFormularios[form.mesa_id].push(form);
        });
        
        // Generar HTML
        if (mesas.length === 0) {
            panelContainer.innerHTML = '<p class="text-muted text-center py-3">No hay mesas en este puesto</p>';
            return;
        }
        
        let html = '<div class="list-group list-group-flush">';
        
        mesas.forEach(mesa => {
            const tieneFormulario = mesasConFormularios[mesa.id] && mesasConFormularios[mesa.id].length > 0;
            const formulario = tieneFormulario ? mesasConFormularios[mesa.id][0] : null;
            const esMiMesa = mesaSeleccionadaDashboard && mesaSeleccionadaDashboard.id === mesa.id;
            
            let estadoBadge = '';
            let borderClass = '';
            let icon = '';
            
            if (esMiMesa && presenciaVerificada) {
                borderClass = 'border-start border-primary border-3';
                icon = '<i class="bi bi-check-circle-fill text-primary"></i>';
            }
            
            if (tieneFormulario) {
                if (formulario.estado === 'validado') {
                    estadoBadge = '<span class="badge bg-success">Validado</span>';
                } else if (formulario.estado === 'pendiente') {
                    estadoBadge = '<span class="badge bg-warning">Pendiente</span>';
                } else if (formulario.estado === 'rechazado') {
                    estadoBadge = '<span class="badge bg-danger">Rechazado</span>';
                } else {
                    estadoBadge = '<span class="badge bg-info">Borrador</span>';
                }
            } else {
                estadoBadge = '<span class="badge bg-secondary">Sin E-14</span>';
            }
            
            html += `
                <div class="list-group-item ${borderClass} p-2">
                    <div class="d-flex justify-content-between align-items-start">
                        <div class="flex-grow-1">
                            <div class="d-flex align-items-center mb-1">
                                ${icon}
                                <strong class="ms-1">Mesa ${mesa.mesa_codigo}</strong>
                            </div>
                            <small class="text-muted d-block">
                                <i class="bi bi-people"></i> ${Utils.formatNumber(mesa.total_votantes_registrados || 0)} votantes
                            </small>
                            ${esMiMesa ? '<small class="text-primary"><i class="bi bi-geo-alt-fill"></i> Mi mesa actual</small>' : ''}
                        </div>
                        <div class="text-end">
                            ${estadoBadge}
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        panelContainer.innerHTML = html;
        
        console.log('✅ Panel de mesas actualizado:', mesas.length, 'mesas');
        
    } catch (error) {
        console.error('Error actualizando panel de mesas:', error);
        const panelContainer = document.getElementById('panelMesasPuesto');
        if (panelContainer) {
            panelContainer.innerHTML = `
                <div class="text-center py-3">
                    <p class="text-danger mb-2">Error al cargar mesas</p>
                    <button class="btn btn-sm btn-outline-primary" onclick="actualizarPanelMesas()">
                        <i class="bi bi-arrow-clockwise"></i> Reintentar
                    </button>
                </div>
            `;
        }
    }
}

/**
 * Seleccionar mesa desde el panel lateral
 */
function seleccionarMesaDesdePanel(mesaId) {
    const selector = document.getElementById('mesa');
    selector.value = mesaId;
    cambiarMesa();
}

async function loadTiposEleccion() {
    try {
        console.log('Cargando tipos de elección...');
        const response = await APIClient.getTiposEleccion();
        console.log('Respuesta tipos de elección:', response);
        
        if (response.success) {
            tiposEleccion = response.data;
            console.log('Tipos de elección cargados:', tiposEleccion.length);
            
            const select = document.getElementById('tipoEleccion');
            if (select) {
                select.innerHTML = '<option value="">Seleccione...</option>';
                
                tiposEleccion.forEach(tipo => {
                    const option = document.createElement('option');
                    option.value = tipo.id;
                    option.textContent = tipo.nombre;
                    option.dataset.tipo = JSON.stringify(tipo);
                    select.appendChild(option);
                    console.log(`  - ${tipo.nombre} (ID: ${tipo.id}, Uninominal: ${tipo.es_uninominal})`);
                });
                
                console.log('✅ Tipos de elección cargados en selector');
            } else {
                console.error('❌ No se encontró el selector tipoEleccion');
            }
        } else {
            console.error('❌ Error en respuesta:', response);
        }
    } catch (error) {
        console.error('❌ Error loading tipos eleccion:', error);
        Utils.showError('Error cargando tipos de elección: ' + error.message);
    }
}

async function cargarPartidosYCandidatos() {
    const tipoEleccionId = document.getElementById('tipoEleccion').value;
    
    if (!tipoEleccionId) {
        document.getElementById('votacionContainer').innerHTML = '<p class="text-muted">Seleccione un tipo de elección</p>';
        return;
    }
    
    try {
        console.log('🔄 Cargando datos para tipo de elección:', tipoEleccionId);
        
        // Obtener información del tipo de elección
        const tipoEleccion = tiposEleccion.find(t => t.id == tipoEleccionId);
        console.log('Tipo de elección seleccionado:', tipoEleccion);
        
        // Cargar partidos
        const partidosResponse = await APIClient.getPartidos();
        partidosData = partidosResponse.success ? partidosResponse.data : [];
        console.log(`✅ Partidos cargados: ${partidosData.length}`);
        
        if (partidosData.length === 0) {
            document.getElementById('votacionContainer').innerHTML = 
                '<div class="alert alert-warning">No hay partidos políticos registrados en el sistema</div>';
            return;
        }
        
        // Cargar candidatos del tipo de elección
        const candidatosResponse = await APIClient.getCandidatos({ tipo_eleccion_id: tipoEleccionId });
        console.log('Respuesta de candidatos:', candidatosResponse);
        candidatosData = candidatosResponse.success ? candidatosResponse.data : [];
        console.log(`📋 Candidatos cargados: ${candidatosData.length}`);
        
        if (candidatosData.length === 0) {
            console.warn(`⚠️ No hay candidatos para ${tipoEleccion?.nombre || 'este tipo de elección'}`);
            // Mostrar mensaje pero permitir continuar con votos de partido
            document.getElementById('votacionContainer').innerHTML = 
                `<div class="alert alert-info">
                    <i class="bi bi-info-circle"></i> 
                    No hay candidatos registrados para ${tipoEleccion?.nombre || 'este tipo de elección'}.
                    Solo podrá registrar votos por partido.
                </div>`;
        }
        
        // Agrupar candidatos por partido
        const candidatosPorPartido = {};
        candidatosData.forEach(candidato => {
            if (!candidatosPorPartido[candidato.partido_id]) {
                candidatosPorPartido[candidato.partido_id] = [];
            }
            candidatosPorPartido[candidato.partido_id].push(candidato);
        });
        console.log('Candidatos agrupados por partido:', candidatosPorPartido);
        
        // Filtrar partidos que no tienen candidatos en el tipo de elección seleccionado
        const partidosConCandidatos = partidosData.filter(partido => {
            const candidatos = candidatosPorPartido[partido.id] || [];
            return candidatos.length > 0;
        });
        console.log(`Partidos con candidatos para ${tipoEleccion?.nombre || 'este tipo de elección'}:`, partidosConCandidatos.length);

        // Renderizar formulario de votación
        renderVotacionForm(candidatosData.length > 0 ? partidosConCandidatos : partidosData, candidatosPorPartido);
        
    } catch (error) {
        console.error('❌ Error loading partidos y candidatos:', error);
        Utils.showError('Error cargando datos de votación: ' + error.message);
        document.getElementById('votacionContainer').innerHTML = 
            `<div class="alert alert-danger">
                <i class="bi bi-exclamation-triangle"></i> 
                Error al cargar datos: ${error.message}
            </div>`;
    }
}

function renderVotacionForm(partidos, candidatosPorPartido) {
    const container = document.getElementById('votacionContainer');
    container.innerHTML = '';
    
    votosData = {};
    
    // Verificar si es elección uninominal
    const tipoEleccionSelect = document.getElementById('tipoEleccion');
    const selectedOption = tipoEleccionSelect.options[tipoEleccionSelect.selectedIndex];
    const tipoEleccion = tiposEleccion.find(t => t.id == tipoEleccionSelect.value);
    const esUninominal = tipoEleccion?.es_uninominal || false;
    
    // Contar total de candidatos
    let totalCandidatos = 0;
    partidos.forEach(partido => {
        const candidatos = candidatosPorPartido[partido.id] || [];
        totalCandidatos += candidatos.length;
    });
    
    // Si hay más de 20 candidatos, usar pestañas por partido
    const usarPestanas = totalCandidatos > 20;
    
    if (usarPestanas) {
        renderVotacionConPestanas(partidos, candidatosPorPartido, esUninominal);
    } else {
        renderVotacionTradicional(partidos, candidatosPorPartido, esUninominal);
    }
}

/**
 * Renderizar votación con pestañas por partido (para elecciones con muchos candidatos)
 */
function renderVotacionConPestanas(partidos, candidatosPorPartido, esUninominal) {
    const container = document.getElementById('votacionContainer');
    
    // Crear pestañas con nav-pills
    let html = `
        <div class="alert alert-info mb-3">
            <i class="bi bi-info-circle"></i>
            <strong>Navegación por partidos:</strong> Use las pestañas para ingresar votos de cada partido
        </div>
        <ul class="nav nav-pills mb-3" id="partidosTabs" role="tablist">
    `;
    
    // Crear pestañas
    partidos.forEach((partido, index) => {
        const candidatos = candidatosPorPartido[partido.id] || [];
        const active = index === 0 ? 'active' : '';
        
        html += `
            <li class="nav-item" role="presentation">
                <button class="nav-link ${active}" 
                        id="tab-partido-${partido.id}" 
                        data-bs-toggle="pill" 
                        data-bs-target="#content-partido-${partido.id}" 
                        type="button" 
                        role="tab"
                        style="border-left: 6px solid ${partido.color}; padding-left: 12px;">
                    <span class="fw-bold">${partido.sigla}</span>
                    <br><small>${candidatos.length} candidato(s)</small>
                </button>
            </li>
        `;
    });
    
    html += `
        </ul>
        <div class="tab-content" id="partidosTabContent">
    `;
    
    // Crear contenido de cada pestaña
    partidos.forEach((partido, index) => {
        const candidatos = candidatosPorPartido[partido.id] || [];
        const active = index === 0 ? 'show active' : '';
        
        html += `
            <div class="tab-pane fade ${active}" 
                 id="content-partido-${partido.id}" 
                 role="tabpanel">
                <div class="card">
                    <div class="card-header" style="background-color: ${partido.color}; border-left: 12px solid ${partido.color};">
                        <div class="row align-items-center">
                            <div class="col-8">
                                <h5 class="mb-0 fw-bold text-white">${partido.nombre}</h5>
                                <span class="badge bg-dark fw-bold">${partido.sigla}</span>
                            </div>
                            ${!esUninominal ? `
                            <div class="col-4 text-end">
                                <label class="form-label mb-1 small d-block text-white">Votos solo partido</label>
                                <input type="number" 
                                       class="form-control form-control-sm text-center fw-bold" 
                                       id="partido_${partido.id}" 
                                       min="0" 
                                       value="0"
                                       onchange="calcularTotales()"
                                       placeholder="0"
                                       style="max-width: 100px; margin-left: auto; font-size: 1.1rem;">
                            </div>
                            ` : ''}
                        </div>
                    </div>
                    <div class="card-body">
        `;
        
        if (candidatos.length === 0) {
            html += '<p class="text-muted mb-0">No hay candidatos registrados para este partido</p>';
        } else {
            // Lista vertical de candidatos (uno debajo del otro)
            candidatos.forEach((candidato, idx) => {
                html += `
                    <div class="mb-2">
                        <div class="card border">
                            <div class="card-body p-2">
                                <div class="row align-items-center">
                                    <div class="col-1 text-center">
                                        <span class="badge bg-dark fs-6">${candidato.numero_lista || idx + 1}</span>
                                    </div>
                                    <div class="col-8">
                                        <small class="fw-bold d-block" style="color: #212529;">${candidato.nombre_completo}</small>
                                    </div>
                                    <div class="col-3 text-end">
                                        <input type="number" 
                                               class="form-control form-control-sm text-center fw-bold" 
                                               id="candidato_${candidato.id}" 
                                               min="0" 
                                               value="0"
                                               onchange="calcularTotales()"
                                               placeholder="0"
                                               style="font-size: 1.1rem;">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            });
        }
        
        // Agregar total del partido
        html += `
                        <div class="mt-3 pt-3 border-top">
                            <div class="row align-items-center">
                                <div class="col-8">
                                    <strong class="fs-5">Total ${partido.sigla}:</strong>
                                    <br><small class="text-muted">(Votos partido + Votos candidatos)</small>
                                </div>
                                <div class="col-4 text-end">
                                    <span id="total_partido_${partido.id}" class="badge bg-primary fs-4 px-3 py-2">0</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

/**
 * Renderizar votación tradicional (para elecciones con pocos candidatos)
 */
function renderVotacionTradicional(partidos, candidatosPorPartido, esUninominal) {
    const container = document.getElementById('votacionContainer');
    
    partidos.forEach(partido => {
        const partidoDiv = document.createElement('div');
        partidoDiv.className = 'card mb-3';
        partidoDiv.style.borderLeft = `8px solid ${partido.color || '#6c757d'}`;
        
        const candidatos = candidatosPorPartido[partido.id] || [];
        
        if (esUninominal) {
            // Elección uninominal: un candidato por partido, sin votos de partido
            const candidato = candidatos[0];
            
            partidoDiv.innerHTML = `
                <div class="card-header" style="background-color: ${partido.color}; border-left: 8px solid ${partido.color};">
                    <div class="row align-items-center">
                        <div class="col-md-8">
                            <h6 class="mb-0 fw-bold text-white">${partido.nombre}</h6>
                            ${candidato ? `<p class="mb-0 small fw-medium text-white"><strong>Candidato:</strong> ${candidato.nombre_completo}</p>` : '<p class="mb-0 small text-white-50">Sin candidato</p>'}
                        </div>
                        <div class="col-md-4">
                            <label class="form-label mb-1 small">Votos</label>
                            <input type="number" 
                                   class="form-control form-control-sm" 
                                   id="${candidato ? `candidato_${candidato.id}` : `partido_${partido.id}`}" 
                                   min="0" 
                                   value="0"
                                   onchange="calcularTotales()"
                                   placeholder="0">
                        </div>
                    </div>
                </div>
            `;
        } else {
            // Elección por listas: múltiples candidatos + votos de partido
            partidoDiv.innerHTML = `
                <div class="card-header" style="background-color: ${partido.color}; border-left: 8px solid ${partido.color};">
                    <div class="row align-items-center">
                        <div class="col-8">
                            <h6 class="mb-0 fw-bold text-white">${partido.nombre}</h6>
                            <span class="badge bg-dark fw-bold">${partido.sigla}</span>
                        </div>
                        <div class="col-4 text-end">
                            <label class="form-label mb-1 small d-block text-white">Votos solo partido</label>
                            <input type="number" 
                                   class="form-control form-control-sm text-center" 
                                   id="partido_${partido.id}" 
                                   min="0" 
                                   value="0"
                                   onchange="calcularTotales()"
                                   placeholder="0"
                                   style="max-width: 80px; margin-left: auto;">
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <div class="row g-2">
                        ${candidatos.map((candidato, idx) => `
                            <div class="col-12 mb-1">
                                <div class="row align-items-center">
                                    <div class="col-1 text-center">
                                        <span class="badge bg-dark">${candidato.numero_lista || idx + 1}</span>
                                    </div>
                                    <div class="col-8">
                                        <small class="fw-bold" style="color: #212529;">${candidato.nombre_completo}</small>
                                    </div>
                                    <div class="col-3 text-end">
                                        <input type="number" 
                                               class="form-control form-control-sm text-center" 
                                               id="candidato_${candidato.id}" 
                                               min="0" 
                                               value="0"
                                               onchange="calcularTotales()"
                                               placeholder="0"
                                               style="max-width: 80px; margin-left: auto;">
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                    ${candidatos.length === 0 ? '<p class="text-muted mb-0 small">No hay candidatos registrados para este partido</p>' : ''}
                    <div class="mt-2 pt-2 border-top">
                        <div class="row align-items-center">
                            <div class="col-8">
                                <strong>Total ${partido.sigla}:</strong>
                            </div>
                            <div class="col-4 text-end">
                                <span id="total_partido_${partido.id}" class="badge bg-primary fs-6">0</span>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
        
        container.appendChild(partidoDiv);
        
        // Inicializar datos de votos
        votosData[partido.id] = {
            partido: partido,
            votosPartido: 0,
            candidatos: candidatos.map(c => ({ ...c, votos: 0 })),
            total: 0,
            esUninominal: esUninominal
        };
    });
    
    calcularTotales();
}

function calcularTotales() {
    console.log('[calcularTotales] Iniciando cálculo...');
    console.log('[calcularTotales] votosData:', votosData);
    
    let votosValidos = 0;
    let maxVotosPartido = 0;
    let partidoGanador = null;
    
    // Calcular por cada partido
    Object.keys(votosData).forEach(partidoId => {
        const data = votosData[partidoId];
        
        // Votos del partido (solo si NO es uninominal)
        let votosPartido = 0;
        if (!data.esUninominal) {
            const inputPartido = document.getElementById(`partido_${partidoId}`);
            votosPartido = parseInt(inputPartido?.value || 0);
            console.log(`[calcularTotales] Partido ${partidoId} - Votos partido: ${votosPartido}`);
        }
        data.votosPartido = votosPartido;
        
        // Votos de candidatos
        let votosCandidatos = 0;
        data.candidatos.forEach(candidato => {
            const inputCandidato = document.getElementById(`candidato_${candidato.id}`);
            const votos = parseInt(inputCandidato?.value || 0);
            candidato.votos = votos;
            votosCandidatos += votos;
            console.log(`[calcularTotales] Candidato ${candidato.id} (${candidato.nombre_completo}): ${votos} votos`);
        });
        
        // Total del partido (votos partido + votos candidatos)
        data.total = votosPartido + votosCandidatos;
        votosValidos += data.total;
        
        console.log(`[calcularTotales] Partido ${partidoId} - Total: ${data.total} (partido: ${votosPartido} + candidatos: ${votosCandidatos})`);
        
        // Actualizar display del total del partido
        const totalSpan = document.getElementById(`total_partido_${partidoId}`);
        if (totalSpan) {
            totalSpan.textContent = Utils.formatNumber(data.total);
        }
        
        // Verificar partido con más votos en esta mesa
        if (data.total > maxVotosPartido) {
            maxVotosPartido = data.total;
            partidoGanador = data.partido;
        }
    });
    
    console.log(`[calcularTotales] Total votos válidos: ${votosValidos}`);
    
    // Obtener otros valores
    const votosNulos = parseInt(document.getElementById('votosNulos')?.value || 0);
    const votosBlanco = parseInt(document.getElementById('votosBlanco')?.value || 0);
    const tarjetasNoMarcadas = parseInt(document.getElementById('tarjetasNoMarcadas')?.value || 0);
    
    console.log(`[calcularTotales] Votos nulos: ${votosNulos}, Votos blanco: ${votosBlanco}, Tarjetas no marcadas: ${tarjetasNoMarcadas}`);
    
    // Calcular totales
    const totalVotos = votosValidos + votosNulos + votosBlanco;
    const totalTarjetas = totalVotos + tarjetasNoMarcadas;
    
    console.log(`[calcularTotales] Total votos: ${totalVotos}, Total tarjetas: ${totalTarjetas}`);
    
    // Actualizar campos automáticos
    const votosValidosInput = document.getElementById('votosValidos');
    const totalVotosInput = document.getElementById('totalVotos');
    const totalTarjetasInput = document.getElementById('totalTarjetas');
    
    if (votosValidosInput) votosValidosInput.value = votosValidos;
    if (totalVotosInput) totalVotosInput.value = totalVotos;
    if (totalTarjetasInput) totalTarjetasInput.value = totalTarjetas;
    
    // Actualizar resumen
    const resumenTotal = document.getElementById('resumenTotal');
    const partidoGanadorSpan = document.getElementById('partidoGanador');
    
    if (resumenTotal) {
        resumenTotal.textContent = Utils.formatNumber(votosValidos);
    }
    
    if (partidoGanadorSpan) {
        partidoGanadorSpan.textContent = partidoGanador ? 
            `${partidoGanador.sigla} (${Utils.formatNumber(maxVotosPartido)} votos)` : '-';
    }
    
    console.log('[calcularTotales] Cálculo completado');
}

async function loadForms() {
    try {
        const params = selectedMesa ? { mesa_id: selectedMesa.id } : {};
        
        // Obtener formularios del servidor
        let formulariosServidor = [];
        try {
            const response = await APIClient.getFormulariosE14(params);
            if (response.success) {
                formulariosServidor = response.data.formularios || response.data || [];
            }
        } catch (error) {
            console.error('Error al cargar formularios del servidor:', error);
            // Continuar para mostrar al menos los borradores locales
        }
        
        // Obtener borradores locales
        const borradoresLocales = obtenerBorradoresLocales();
        const formulariosLocales = Object.values(borradoresLocales).map(borrador => {
            return {
                id: borrador.local_id,
                mesa_id: borrador.mesa_id,
                mesa_codigo: getMesaCodigoById(borrador.mesa_id),
                estado: 'local',
                total_votos: borrador.total_votos,
                created_at: borrador.saved_at,
                es_local: true
            };
        });
        
        // Filtrar borradores locales por mesa si es necesario
        let formulariosLocalesFiltrados = formulariosLocales;
        if (selectedMesa) {
            formulariosLocalesFiltrados = formulariosLocales.filter(f => f.mesa_id === selectedMesa.id);
        }
        
        // Combinar formularios del servidor y locales
        const todosFormularios = [...formulariosServidor, ...formulariosLocalesFiltrados];
        
        updateFormsTable(todosFormularios);
        
        // Actualizar indicador de sincronización
        actualizarIndicadorSincronizacion();
        
        // Actualizar panel lateral
        if (userLocation && userLocation.puesto_codigo) {
            actualizarPanelMesas();
        }
        
    } catch (error) {
        console.error('Error al cargar formularios:', error);
        // Mostrar mensaje en la tabla
        const tbody = document.querySelector('#formsTable tbody');
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center py-4">
                    <p class="text-muted">Error al cargar formularios</p>
                </td>
            </tr>
        `;
    }
}

/**
 * Obtener código de mesa por ID
 */
function getMesaCodigoById(mesaId) {
    const mesaSelect = document.getElementById('mesa');
    for (let i = 0; i < mesaSelect.options.length; i++) {
        const option = mesaSelect.options[i];
        if (option.value == mesaId && option.dataset.mesa) {
            const mesa = JSON.parse(option.dataset.mesa);
            return mesa.mesa_codigo;
        }
    }
    return 'N/A';
}



function updateFormsTable(forms) {
    const tbody = document.querySelector('#formsTable tbody');
    tbody.innerHTML = '';
    
    if (forms.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center py-4">
                    <p class="text-muted">No hay formularios registrados</p>
                </td>
            </tr>
        `;
        return;
    }
    
    forms.forEach(form => {
        const row = document.createElement('tr');
        const estadoLabel = getEstadoLabel(form.estado);
        // Solo se pueden editar borradores y formularios locales
        const puedeEditar = form.estado === 'borrador' || form.estado === 'local';
        const esLocal = form.es_local || form.estado === 'local';
        
        // Hacer la fila clickeable si puede editar
        if (puedeEditar) {
            row.style.cursor = 'pointer';
            row.onclick = () => {
                if (esLocal) {
                    editarBorradorLocal(form.id);
                } else {
                    editForm(form.id);
                }
            };
            row.onmouseover = () => row.style.backgroundColor = '#f8f9fa';
            row.onmouseout = () => row.style.backgroundColor = '';
        }
        
        row.innerHTML = `
            <td>Mesa ${form.mesa_codigo || 'N/A'}</td>
            <td><span class="badge bg-${getStatusColor(form.estado)}">${estadoLabel}</span></td>
            <td>${Utils.formatNumber(form.total_votos)}</td>
            <td>${Utils.formatDate(form.created_at)}</td>
            <td>
                ${puedeEditar ? 
                    `<button class="btn btn-sm btn-outline-warning" onclick="event.stopPropagation(); ${esLocal ? `editarBorradorLocal('${form.id}')` : `editForm(${form.id})`}">
                        <i class="bi bi-pencil"></i> Editar
                    </button>
                    ${esLocal ? 
                        `<button class="btn btn-sm btn-outline-danger ms-1" onclick="event.stopPropagation(); eliminarBorradorLocalPorId('${form.id}')">
                            <i class="bi bi-trash"></i>
                        </button>` : ''
                    }` : 
                    `<button class="btn btn-sm btn-outline-primary" onclick="event.stopPropagation(); viewForm(${form.id})">
                        <i class="bi bi-eye"></i> Ver
                    </button>`
                }
            </td>
        `;
        tbody.appendChild(row);
    });
}

function getStatusColor(estado) {
    const colors = {
        'pendiente': 'info',        // Azul para enviado/pendiente
        'validado': 'success',      // Verde para validado
        'rechazado': 'danger',      // Rojo para rechazado
        'borrador': 'secondary',    // Gris para borrador
        'local': 'warning'          // Amarillo para guardado local
    };
    return colors[estado] || 'secondary';
}

function getEstadoLabel(estado) {
    const labels = {
        'pendiente': '📤 Enviado - Pendiente Revisión',
        'validado': '✅ Validado',
        'rechazado': '❌ Rechazado',
        'borrador': '📝 Borrador',
        'local': '💾 Guardado Localmente'
    };
    return labels[estado] || estado;
}

// NOTA: showCreateForm() está definida en testigo-dashboard-final-fix.js
// Esta definición duplicada ha sido eliminada para evitar conflictos

// Función cambiarMesaFormulario ya está definida arriba (línea ~380)

async function saveForm(accion = 'borrador') {
    console.log('saveForm called with accion:', accion);
    const form = document.getElementById('e14Form');
    
    // Solo validar si se va a enviar
    if (accion === 'enviar' && !form.checkValidity()) {
        console.log('Form validation failed');
        form.reportValidity();
        return;
    }
    
    const mesaId = document.getElementById('mesaFormulario').value;
    console.log('Mesa ID:', mesaId);
    if (!mesaId) {
        Utils.showError('Selecciona una mesa');
        return;
    }
    
    // Deshabilitar botones para prevenir doble envío
    const btnGuardar = document.querySelector('.btn-warning[onclick*="saveForm"]');
    const btnEnviar = document.querySelector('.btn-primary[onclick*="saveForm"]');
    const btnCancelar = document.querySelector('.btn-secondary[data-bs-dismiss="modal"]');
    
    console.log('Disabling buttons...');
    if (btnGuardar) btnGuardar.disabled = true;
    if (btnEnviar) btnEnviar.disabled = true;
    if (btnCancelar) btnCancelar.disabled = true;
    
    try {
        const formData = new FormData(form);
        console.log('FormData created');
        
        // Construir datos de votos por partido y candidato
        const votosPartidos = [];
        const votosCandidatos = [];
        
        Object.keys(votosData).forEach(partidoId => {
            const data = votosData[partidoId];
            
            // Votos del partido
            if (data.votosPartido > 0) {
                votosPartidos.push({
                    partido_id: parseInt(partidoId),
                    votos: data.votosPartido
                });
            }
            
            // Votos de candidatos
            data.candidatos.forEach(candidato => {
                if (candidato.votos > 0) {
                    votosCandidatos.push({
                        candidato_id: candidato.id,
                        votos: candidato.votos
                    });
                }
            });
        });
        
        // Construir objeto de datos
        const data = {
            mesa_id: parseInt(mesaId),
            tipo_eleccion_id: parseInt(formData.get('tipo_eleccion')),
            total_votantes_registrados: parseInt(formData.get('total_votantes_registrados')),
            total_votos: parseInt(formData.get('total_votos')),
            votos_validos: parseInt(formData.get('votos_validos')),
            votos_nulos: parseInt(formData.get('votos_nulos')),
            votos_blanco: parseInt(formData.get('votos_blanco')),
            tarjetas_no_marcadas: parseInt(formData.get('tarjetas_no_marcadas')),
            total_tarjetas: parseInt(formData.get('total_tarjetas')),
            observaciones: formData.get('observaciones') || '',
            estado: accion === 'enviar' ? 'pendiente' : 'borrador',
            votos_partidos: votosPartidos,
            votos_candidatos: votosCandidatos
        };
        
        console.log('Saving form data:', data);
        
        // Intentar guardar en el servidor (tanto borrador como envío)
        try {
            Utils.showInfo(accion === 'borrador' ? 'Guardando borrador...' : 'Enviando formulario...');
            const response = await APIClient.createFormularioE14(data);
            
            if (response.success) {
                // Eliminar borrador local si existe (ya está en BD)
                eliminarBorradorLocal(data.mesa_id, data.tipo_eleccion_id);
                
                const mensaje = accion === 'borrador' ? 
                    '✓ Borrador guardado en el servidor' : 
                    '✓ Formulario E-14 enviado exitosamente para revisión';
                Utils.showSuccess(mensaje);
                
                // Limpiar formulario ANTES de cerrar modal
                form.reset();
                document.getElementById('imagePreview').innerHTML = '<p class="text-muted">Toque el botón para tomar una foto</p>';
                votosData = {};
                
                // Cerrar modal con un pequeño delay para que se vea el mensaje
                setTimeout(() => {
                    const modalElement = document.getElementById('formModal');
                    const modal = bootstrap.Modal.getInstance(modalElement);
                    if (modal) {
                        modal.hide();
                    } else {
                        // Si no hay instancia, crear una y cerrarla
                        const newModal = new bootstrap.Modal(modalElement);
                        newModal.hide();
                    }
                    
                    // Asegurar que el backdrop se elimine
                    document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());
                    document.body.classList.remove('modal-open');
                    document.body.style.removeProperty('overflow');
                    document.body.style.removeProperty('padding-right');
                }, 500);
                
                // Actualizar vistas inmediatamente
                await loadForms();
                await actualizarPanelMesas();
                return;
            } else {
                throw new Error(response.error || 'Error al guardar en el servidor');
            }
        } catch (error) {
            console.error('Error guardando en servidor:', error);
            
            // Si falla, guardar localmente solo como backup
            if (accion === 'borrador') {
                guardarBorradorLocal(data);
                Utils.showWarning('⚠️ Guardado localmente (sin conexión). Se sincronizará automáticamente.');
                
                setTimeout(() => {
                    const modalElement = document.getElementById('formModal');
                    const modal = bootstrap.Modal.getInstance(modalElement);
                    if (modal) {
                        modal.hide();
                    }
                    document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());
                    document.body.classList.remove('modal-open');
                    document.body.style.removeProperty('overflow');
                }, 500);
                
                await loadForms();
                await actualizarPanelMesas();
                return;
            }
            
            // Si es envío y falla, preguntar si guardar como borrador
            if (confirm('No se pudo enviar el formulario. ¿Desea guardarlo como borrador para enviarlo después?')) {
                // Cambiar a borrador y guardar localmente
                data.estado = 'borrador';
                guardarBorradorLocal(data);
                Utils.showWarning('Guardado como borrador local. Se sincronizará cuando haya conexión.');
                
                setTimeout(() => {
                    const modalElement = document.getElementById('formModal');
                    const modal = bootstrap.Modal.getInstance(modalElement);
                    if (modal) {
                        modal.hide();
                    }
                    document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());
                    document.body.classList.remove('modal-open');
                }, 500);
                
                await loadForms();
                await actualizarPanelMesas();
            } else {
                Utils.showError('Error al enviar formulario: ' + error.message);
            }
            return;
        }

        
    } catch (error) {
        console.error('Error saving form:', error);
        Utils.showError('Error al guardar formulario: ' + error.message);
    } finally {
        // Rehabilitar botones
        if (btnGuardar) btnGuardar.disabled = false;
        if (btnEnviar) btnEnviar.disabled = false;
        if (btnCancelar) btnCancelar.disabled = false;
    }
}

/**
 * Guardar borrador en localStorage
 */
function guardarBorradorLocal(data) {
    try {
        // Obtener borradores existentes
        const borradores = obtenerBorradoresLocales();
        
        // Crear clave única para el borrador
        const key = `${data.mesa_id}_${data.tipo_eleccion_id}`;
        
        // Agregar timestamp
        data.saved_at = new Date().toISOString();
        data.local_id = key;
        
        // Guardar o actualizar borrador
        borradores[key] = data;
        
        localStorage.setItem('formularios_e14_borradores', JSON.stringify(borradores));
        
        console.log('Borrador guardado localmente:', key);
    } catch (error) {
        console.error('Error guardando borrador local:', error);
        throw new Error('No se pudo guardar el borrador localmente');
    }
}

/**
 * Obtener todos los borradores locales
 */
function obtenerBorradoresLocales() {
    try {
        const borradores = localStorage.getItem('formularios_e14_borradores');
        return borradores ? JSON.parse(borradores) : {};
    } catch (error) {
        console.error('Error obteniendo borradores locales:', error);
        return {};
    }
}

/**
 * Eliminar borrador local
 */
function eliminarBorradorLocal(mesaId, tipoEleccionId) {
    try {
        const borradores = obtenerBorradoresLocales();
        const key = `${mesaId}_${tipoEleccionId}`;
        
        if (borradores[key]) {
            delete borradores[key];
            localStorage.setItem('formularios_e14_borradores', JSON.stringify(borradores));
            console.log('Borrador local eliminado:', key);
        }
    } catch (error) {
        console.error('Error eliminando borrador local:', error);
    }
}

/**
 * Sincronizar borradores locales con el servidor
 */
async function sincronizarBorradoresLocales(silencioso = false) {
    try {
        const borradores = obtenerBorradoresLocales();
        const keys = Object.keys(borradores);
        
        if (keys.length === 0) {
            console.log('No hay borradores locales para sincronizar');
            if (!silencioso) {
                Utils.showInfo('No hay formularios pendientes de sincronizar');
            }
            return { sincronizados: 0, errores: 0 };
        }
        
        console.log(`Sincronizando ${keys.length} borradores locales...`);
        
        let sincronizados = 0;
        let errores = 0;
        
        for (const key of keys) {
            const borrador = borradores[key];
            
            try {
                // Cambiar estado a pendiente para enviar
                borrador.estado = 'pendiente';
                
                const response = await APIClient.createFormularioE14(borrador);
                
                if (response.success) {
                    eliminarBorradorLocal(borrador.mesa_id, borrador.tipo_eleccion_id);
                    sincronizados++;
                    console.log('Borrador sincronizado:', key);
                } else {
                    errores++;
                    console.error('Error sincronizando borrador:', key, response.error);
                }
            } catch (error) {
                errores++;
                console.error('Error sincronizando borrador:', key, error);
            }
        }
        
        if (!silencioso) {
            if (sincronizados > 0) {
                Utils.showSuccess(`✓ ${sincronizados} formulario(s) sincronizado(s) exitosamente`);
                loadForms();
            }
            
            if (errores > 0) {
                Utils.showWarning(`⚠️ ${errores} formulario(s) no se pudieron sincronizar`);
            }
        }
        
        return { sincronizados, errores };
        
    } catch (error) {
        console.error('Error en sincronización de borradores:', error);
        return { sincronizados: 0, errores: 0 };
    }
}

/**
 * Editar borrador local
 */
async function editarBorradorLocal(localId) {
    try {
        const borradores = obtenerBorradoresLocales();
        const borrador = borradores[localId];
        
        if (!borrador) {
            Utils.showError('Borrador no encontrado');
            return;
        }
        
        // Abrir el modal
        document.getElementById('e14Form').reset();
        
        // Cargar mesa (permitir cambiar si es necesario)
        const mesaSelect = document.getElementById('mesaFormulario');
        mesaSelect.value = borrador.mesa_id;
        mesaSelect.disabled = false; // PERMITIR CAMBIAR MESA
        cambiarMesaFormulario();
        
        // Cargar tipo de elección y DESHABILITAR (no se puede cambiar)
        const tipoEleccionSelect = document.getElementById('tipoEleccion');
        tipoEleccionSelect.value = borrador.tipo_eleccion_id;
        tipoEleccionSelect.disabled = true; // NO PERMITIR CAMBIAR TIPO DE ELECCIÓN
        await cargarPartidosYCandidatos();
        
        // Cargar datos de votación
        document.getElementById('votosNulos').value = borrador.votos_nulos || 0;
        document.getElementById('votosBlanco').value = borrador.votos_blanco || 0;
        document.getElementById('tarjetasNoMarcadas').value = borrador.tarjetas_no_marcadas || 0;
        
        // Cargar votos por partido
        if (borrador.votos_partidos) {
            borrador.votos_partidos.forEach(vp => {
                const input = document.getElementById(`partido_${vp.partido_id}`);
                if (input) input.value = vp.votos;
            });
        }
        
        // Cargar votos por candidato
        if (borrador.votos_candidatos) {
            borrador.votos_candidatos.forEach(vc => {
                const input = document.getElementById(`candidato_${vc.candidato_id}`);
                if (input) input.value = vc.votos;
            });
        }
        
        // Cargar observaciones
        document.querySelector('[name="observaciones"]').value = borrador.observaciones || '';
        
        // Recalcular totales
        calcularTotales();
        
        // Mostrar modal
        new bootstrap.Modal(document.getElementById('formModal')).show();
        
    } catch (error) {
        console.error('Error loading local draft:', error);
        Utils.showError('Error al cargar borrador: ' + error.message);
    }
}

/**
 * Eliminar borrador local por ID
 */
function eliminarBorradorLocalPorId(localId) {
    if (!confirm('¿Está seguro de eliminar este borrador local?')) {
        return;
    }
    
    try {
        const borradores = obtenerBorradoresLocales();
        
        if (borradores[localId]) {
            delete borradores[localId];
            localStorage.setItem('formularios_e14_borradores', JSON.stringify(borradores));
            Utils.showSuccess('Borrador eliminado');
            loadForms();
        }
    } catch (error) {
        console.error('Error eliminando borrador:', error);
        Utils.showError('Error al eliminar borrador');
    }
}

function viewForm(formId) {
    window.open(`/testigo/form/${formId}`, '_blank');
}

async function editForm(formId) {
    try {
        // Cargar el formulario
        const response = await APIClient.getFormularioE14(formId);
        
        if (!response.success) {
            Utils.showError('Error al cargar formulario');
            return;
        }
        
        const formulario = response.data;
        
        // Abrir el modal
        document.getElementById('e14Form').reset();
        
        // Cargar mesa (permitir cambiar si es necesario)
        const mesaSelect = document.getElementById('mesaFormulario');
        mesaSelect.value = formulario.mesa_id;
        mesaSelect.disabled = false; // PERMITIR CAMBIAR MESA
        cambiarMesaFormulario();
        
        // Cargar tipo de elección y DESHABILITAR (no se puede cambiar)
        const tipoEleccionSelect = document.getElementById('tipoEleccion');
        tipoEleccionSelect.value = formulario.tipo_eleccion_id;
        tipoEleccionSelect.disabled = true; // NO PERMITIR CAMBIAR TIPO DE ELECCIÓN
        await cargarPartidosYCandidatos();
        
        // Cargar datos de votación
        document.getElementById('votosNulos').value = formulario.votos_nulos || 0;
        document.getElementById('votosBlanco').value = formulario.votos_blanco || 0;
        document.getElementById('tarjetasNoMarcadas').value = formulario.tarjetas_no_marcadas || 0;
        
        // Cargar votos por partido
        if (formulario.votos_partidos) {
            formulario.votos_partidos.forEach(vp => {
                const input = document.getElementById(`partido_${vp.partido_id}`);
                if (input) input.value = vp.votos;
            });
        }
        
        // Cargar votos por candidato
        if (formulario.votos_candidatos) {
            formulario.votos_candidatos.forEach(vc => {
                const input = document.getElementById(`candidato_${vc.candidato_id}`);
                if (input) input.value = vc.votos;
            });
        }
        
        // Cargar observaciones
        document.querySelector('[name="observaciones"]').value = formulario.observaciones || '';
        
        // Recalcular totales
        calcularTotales();
        
        // Mostrar modal
        new bootstrap.Modal(document.getElementById('formModal')).show();
        
    } catch (error) {
        console.error('Error loading form:', error);
        Utils.showError('Error al cargar formulario: ' + error.message);
    }
}

function setupImagePreview() {
    const input = document.getElementById('imagen');
    const preview = document.getElementById('imagePreview');
    
    if (!input || !preview) {
        console.warn('Image input or preview not found');
        return;
    }
    
    // Remover listeners anteriores clonando el elemento
    const newInput = input.cloneNode(true);
    input.parentNode.replaceChild(newInput, input);
    
    newInput.addEventListener('change', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        const file = e.target.files[0];
        
        if (file) {
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    preview.innerHTML = `<img src="${event.target.result}" alt="Preview" style="max-width: 100%; max-height: 250px; object-fit: contain;">`;
                };
                reader.onerror = function() {
                    preview.innerHTML = '<p class="text-danger">Error al cargar la imagen</p>';
                };
                reader.readAsDataURL(file);
            } else {
                preview.innerHTML = '<p class="text-danger">Por favor seleccione una imagen válida</p>';
            }
        } else {
            preview.innerHTML = '<p class="text-muted">Toque el botón para tomar una foto</p>';
        }
    });
}

/**
 * Verificar presencia del testigo en la mesa
 */


/**
 * Verificar estado de presencia al cargar
 */
async function verificarEstadoPresencia() {
    try {
        const response = await APIClient.getProfile();
        if (response.success && response.data.user) {
            const user = response.data.user;
            
            // Si ya verificó presencia, mostrar alerta
            if (user.presencia_verificada) {
                document.getElementById('btnVerificarPresencia').classList.add('d-none');
                document.getElementById('alertaPresenciaVerificada').classList.remove('d-none');
                
                if (user.presencia_verificada_at) {
                    const fecha = new Date(user.presencia_verificada_at);
                    document.getElementById('presenciaFecha').textContent = 
                        `Verificado el ${fecha.toLocaleDateString()} a las ${fecha.toLocaleTimeString()}`;
                }
            }
        }
    } catch (error) {
        console.error('Error verificando estado de presencia:', error);
    }
}

// Función global para logout
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

// Agregar evento para seleccionar todo el texto en inputs numéricos al hacer focus
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('focus', function(e) {
        if (e.target.type === 'number') {
            e.target.select();
        }
    }, true);
    
    // Verificar estado de presencia al cargar
    verificarEstadoPresencia();
    
    // Intentar sincronizar borradores locales al cargar (silenciosamente)
    setTimeout(() => {
        const borradores = obtenerBorradoresLocales();
        if (Object.keys(borradores).length > 0) {
            console.log('Hay borradores locales pendientes de sincronizar');
            // No sincronizar automáticamente, solo mostrar indicador
        }
    }, 2000);
});


// ============================================
// FUNCIONES PARA INCIDENTES Y DELITOS
// ============================================

/**
 * Cargar tipos de incidentes
 */
async function loadTiposIncidentes() {
    try {
        const response = await APIClient.getTiposIncidentes();
        console.log('Tipos incidentes response:', response);
        
        const select = document.getElementById('tipoIncidente');
        if (select && response.tipos) {
            select.innerHTML = '<option value="">Seleccione tipo de incidente...</option>';
            
            // response.tipos es un objeto con código: descripción
            Object.entries(response.tipos).forEach(([codigo, descripcion]) => {
                const option = document.createElement('option');
                option.value = codigo;
                option.textContent = descripcion;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading tipos incidentes:', error);
    }
}

/**
 * Cargar tipos de delitos
 */
async function loadTiposDelitos() {
    try {
        const response = await APIClient.getTiposDelitos();
        console.log('Tipos delitos response:', response);
        
        const select = document.getElementById('tipoDelito');
        if (select && response.tipos) {
            select.innerHTML = '<option value="">Seleccione tipo de delito...</option>';
            
            // response.tipos es un objeto con código: descripción
            Object.entries(response.tipos).forEach(([codigo, descripcion]) => {
                const option = document.createElement('option');
                option.value = codigo;
                option.textContent = descripcion;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading tipos delitos:', error);
    }
}

/**
 * Reportar incidente
 */
function reportarIncidente() {
    if (!selectedMesa) {
        Utils.showWarning('Por favor selecciona una mesa primero');
        return;
    }
    
    // Actualizar información de la mesa en el modal
    const mesaInfo = document.getElementById('mesaInfoIncidente');
    if (mesaInfo && selectedMesa) {
        mesaInfo.textContent = `Mesa ${selectedMesa.mesa_codigo} - ${selectedMesa.puesto_nombre || ''}`;
    }
    
    document.getElementById('formIncidente').reset();
    new bootstrap.Modal(document.getElementById('incidenteModal')).show();
}

/**
 * Guardar incidente
 */
async function guardarIncidente() {
    const form = document.getElementById('formIncidente');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    if (!selectedMesa) {
        Utils.showError('Debe seleccionar una mesa');
        return;
    }
    
    try {
        const formData = new FormData(form);
        
        const data = {
            mesa_id: selectedMesa.id,
            tipo_incidente: formData.get('tipo_incidente'),
            titulo: formData.get('titulo'),
            severidad: formData.get('severidad'),
            descripcion: formData.get('descripcion')
        };
        
        // Intentar guardar en el servidor
        try {
            const response = await APIClient.reportarIncidente(data);
            
            if (response.success) {
                Utils.showSuccess('✓ Incidente reportado exitosamente');
                bootstrap.Modal.getInstance(document.getElementById('incidenteModal')).hide();
                cargarIncidentes();
            } else {
                throw new Error(response.error || 'Error al reportar incidente');
            }
        } catch (error) {
            console.error('Error guardando incidente en servidor:', error);
            // Guardar localmente usando SyncManager
            if (window.syncManager) {
                window.syncManager.saveIncidentLocally(data);
                Utils.showWarning('⚠️ Incidente guardado localmente. Se sincronizará automáticamente.');
            } else {
                guardarIncidenteLocal(data);
                Utils.showWarning('⚠️ Incidente guardado localmente.');
            }
            bootstrap.Modal.getInstance(document.getElementById('incidenteModal')).hide();
            cargarIncidentes();
        }
        
    } catch (error) {
        console.error('Error guardando incidente:', error);
        Utils.showError('Error al reportar incidente: ' + error.message);
    }
}

/**
 * Guardar incidente en localStorage
 */
function guardarIncidenteLocal(data) {
    try {
        const incidentes = obtenerIncidentesLocales();
        const id = `incidente_${Date.now()}`;
        data.id = id;
        data.sincronizado = false;
        data.fecha_hora = new Date().toISOString();
        incidentes[id] = data;
        localStorage.setItem('incidentes_testigo', JSON.stringify(incidentes));
        console.log('Incidente guardado localmente:', id);
    } catch (error) {
        console.error('Error guardando incidente local:', error);
    }
}

/**
 * Sincronizar incidentes locales con el servidor
 */
async function sincronizarIncidentesLocales(silencioso = false) {
    try {
        const incidentes = obtenerIncidentesLocales();
        const keys = Object.keys(incidentes);
        
        if (keys.length === 0) {
            console.log('No hay incidentes locales para sincronizar');
            return { sincronizados: 0, errores: 0 };
        }
        
        console.log(`Sincronizando ${keys.length} incidentes locales...`);
        
        let sincronizados = 0;
        let errores = 0;
        
        for (const key of keys) {
            const incidente = incidentes[key];
            
            // Solo sincronizar los que no están sincronizados
            if (incidente.sincronizado) {
                continue;
            }
            
            try {
                // Preparar datos para enviar
                const dataToSend = {
                    mesa_id: incidente.mesa_id,
                    tipo_incidente: incidente.tipo_incidente,
                    titulo: incidente.titulo,
                    severidad: incidente.severidad,
                    descripcion: incidente.descripcion
                };
                
                const response = await APIClient.reportarIncidente(dataToSend);
                
                if (response.success) {
                    // Marcar como sincronizado en lugar de eliminar
                    incidente.sincronizado = true;
                    incidente.id_servidor = response.data.id;
                    incidentes[key] = incidente;
                    localStorage.setItem('incidentes_testigo', JSON.stringify(incidentes));
                    
                    sincronizados++;
                    console.log('Incidente sincronizado:', key);
                } else {
                    errores++;
                    console.error('Error sincronizando incidente:', key, response.error);
                }
            } catch (error) {
                errores++;
                console.error('Error sincronizando incidente:', key, error);
            }
        }
        
        if (!silencioso && sincronizados > 0) {
            Utils.showSuccess(`✓ ${sincronizados} incidente(s) sincronizado(s)`);
            cargarIncidentes();
        }
        
        return { sincronizados, errores };
        
    } catch (error) {
        console.error('Error en sincronización de incidentes:', error);
        return { sincronizados: 0, errores: 0 };
    }
}

/**
 * Obtener incidentes locales
 */
function obtenerIncidentesLocales() {
    try {
        const incidentes = localStorage.getItem('incidentes_testigo');
        return incidentes ? JSON.parse(incidentes) : {};
    } catch (error) {
        console.error('Error obteniendo incidentes locales:', error);
        return {};
    }
}

/**
 * Cargar incidentes
 */
async function cargarIncidentes() {
    const lista = document.getElementById('incidentesLista');
    
    try {
        // Cargar incidentes del servidor
        const params = selectedMesa ? { mesa_id: selectedMesa.id } : {};
        const response = await APIClient.getIncidentes(params);
        
        let incidentesServidor = [];
        if (response.success) {
            incidentesServidor = response.data || [];
        }
        
        // Cargar incidentes locales (usar SyncManager si está disponible)
        const incidentesLocalesObj = window.syncManager ? 
            window.syncManager.getLocalIncidents() : 
            obtenerIncidentesLocales();
        const incidentesLocales = Object.values(incidentesLocalesObj);
        
        // Combinar ambos
        const todosIncidentes = [...incidentesServidor, ...incidentesLocales];
        
        if (todosIncidentes.length === 0) {
            lista.innerHTML = '<p class="text-muted text-center py-4">No hay incidentes reportados</p>';
            return;
        }
        
        lista.innerHTML = todosIncidentes.map(incidente => {
            const esLocal = incidente.sincronizado === false;
            const severidadColor = getSeveridadColor(incidente.severidad || 'media');
            
            return `
                <div class="card mb-3 border-${severidadColor}">
                    <div class="card-header bg-${severidadColor} bg-opacity-10">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <h6 class="mb-1">${incidente.titulo || getTipoIncidenteLabel(incidente.tipo_incidente)}</h6>
                                <span class="badge bg-${severidadColor}">${incidente.severidad_label || incidente.severidad || 'Media'}</span>
                            </div>
                            <span class="badge ${esLocal ? 'bg-warning' : 'bg-success'}">
                                ${esLocal ? '💾 Local' : '✓ Reportado'}
                            </span>
                        </div>
                    </div>
                    <div class="card-body">
                        <p class="mb-2">${incidente.descripcion}</p>
                        <small class="text-muted">
                            <i class="bi bi-clock"></i> ${Utils.formatDate(incidente.fecha_hora || incidente.created_at)}
                            ${incidente.mesa_codigo ? `• Mesa ${incidente.mesa_codigo}` : ''}
                        </small>
                    </div>
                </div>
            `;
        }).join('');
        
    } catch (error) {
        console.error('Error cargando incidentes:', error);
        lista.innerHTML = '<div class="alert alert-warning">Error al cargar incidentes</div>';
    }
}

/**
 * Obtener color según severidad
 */
function getSeveridadColor(severidad) {
    const colors = {
        'baja': 'info',
        'media': 'warning',
        'alta': 'danger',
        'critica': 'dark'
    };
    return colors[severidad] || 'warning';
}

/**
 * Obtener label del tipo de incidente
 */
function getTipoIncidenteLabel(tipo) {
    const labels = {
        'retraso_apertura': 'Retraso en apertura',
        'falta_material': 'Falta de material electoral',
        'problemas_tecnicos': 'Problemas técnicos',
        'irregularidades': 'Irregularidades en el proceso',
        'otros': 'Otros'
    };
    return labels[tipo] || tipo;
}

/**
 * Reportar delito
 */
function reportarDelito() {
    if (!selectedMesa) {
        Utils.showWarning('Por favor selecciona una mesa primero');
        return;
    }
    
    // Actualizar información de la mesa en el modal
    const mesaInfo = document.getElementById('mesaInfoDelito');
    if (mesaInfo && selectedMesa) {
        mesaInfo.textContent = `Mesa ${selectedMesa.mesa_codigo} - ${selectedMesa.puesto_nombre || ''}`;
    }
    
    document.getElementById('formDelito').reset();
    new bootstrap.Modal(document.getElementById('delitoModal')).show();
}

/**
 * Guardar delito
 */
async function guardarDelito() {
    const form = document.getElementById('formDelito');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    if (!confirm('¿Está seguro de reportar este delito electoral? Este reporte será enviado a las autoridades competentes.')) {
        return;
    }
    
    if (!selectedMesa) {
        Utils.showError('Debe seleccionar una mesa');
        return;
    }
    
    try {
        const formData = new FormData(form);
        
        const data = {
            mesa_id: selectedMesa.id,
            tipo_delito: formData.get('tipo_delito'),
            titulo: formData.get('titulo'),
            gravedad: formData.get('gravedad'),
            descripcion: formData.get('descripcion'),
            testigos_adicionales: formData.get('testigos_adicionales') || null
        };
        
        // Intentar guardar en el servidor
        try {
            const response = await APIClient.reportarDelito(data);
            
            if (response.success) {
                Utils.showSuccess('✓ Delito reportado exitosamente. Las autoridades han sido notificadas.');
                bootstrap.Modal.getInstance(document.getElementById('delitoModal')).hide();
                cargarDelitos();
            } else {
                throw new Error(response.error || 'Error al reportar delito');
            }
        } catch (error) {
            console.error('Error guardando delito en servidor:', error);
            // Guardar localmente usando SyncManager
            if (window.syncManager) {
                window.syncManager.saveCrimeLocally(data);
                Utils.showWarning('⚠️ Delito guardado localmente. Se sincronizará automáticamente.');
            } else {
                guardarDelitoLocal(data);
                Utils.showWarning('⚠️ Delito guardado localmente.');
            }
            bootstrap.Modal.getInstance(document.getElementById('delitoModal')).hide();
            cargarDelitos();
        }
        
    } catch (error) {
        console.error('Error guardando delito:', error);
        Utils.showError('Error al reportar delito: ' + error.message);
    }
}

/**
 * Guardar delito en localStorage
 */
function guardarDelitoLocal(data) {
    try {
        const delitos = obtenerDelitosLocales();
        const id = `delito_${Date.now()}`;
        data.id = id;
        data.sincronizado = false;
        data.fecha_hora = new Date().toISOString();
        delitos[id] = data;
        localStorage.setItem('delitos_testigo', JSON.stringify(delitos));
        console.log('Delito guardado localmente:', id);
    } catch (error) {
        console.error('Error guardando delito local:', error);
    }
}

/**
 * Sincronizar delitos locales con el servidor
 */
async function sincronizarDelitosLocales(silencioso = false) {
    try {
        const delitos = obtenerDelitosLocales();
        const keys = Object.keys(delitos);
        
        if (keys.length === 0) {
            console.log('No hay delitos locales para sincronizar');
            return { sincronizados: 0, errores: 0 };
        }
        
        console.log(`Sincronizando ${keys.length} delitos locales...`);
        
        let sincronizados = 0;
        let errores = 0;
        
        for (const key of keys) {
            const delito = delitos[key];
            
            // Solo sincronizar los que no están sincronizados
            if (delito.sincronizado) {
                continue;
            }
            
            try {
                // Preparar datos para enviar
                const dataToSend = {
                    mesa_id: delito.mesa_id,
                    tipo_delito: delito.tipo_delito,
                    titulo: delito.titulo,
                    gravedad: delito.gravedad,
                    descripcion: delito.descripcion,
                    testigos_adicionales: delito.testigos_adicionales || null
                };
                
                const response = await APIClient.reportarDelito(dataToSend);
                
                if (response.success) {
                    // Marcar como sincronizado en lugar de eliminar
                    delito.sincronizado = true;
                    delito.id_servidor = response.data.id;
                    delitos[key] = delito;
                    localStorage.setItem('delitos_testigo', JSON.stringify(delitos));
                    
                    sincronizados++;
                    console.log('Delito sincronizado:', key);
                } else {
                    errores++;
                    console.error('Error sincronizando delito:', key, response.error);
                }
            } catch (error) {
                errores++;
                console.error('Error sincronizando delito:', key, error);
            }
        }
        
        if (!silencioso && sincronizados > 0) {
            Utils.showSuccess(`✓ ${sincronizados} delito(s) sincronizado(s)`);
            cargarDelitos();
        }
        
        return { sincronizados, errores };
        
    } catch (error) {
        console.error('Error en sincronización de delitos:', error);
        return { sincronizados: 0, errores: 0 };
    }
}

/**
 * Obtener delitos locales
 */
function obtenerDelitosLocales() {
    try {
        const delitos = localStorage.getItem('delitos_testigo');
        return delitos ? JSON.parse(delitos) : {};
    } catch (error) {
        console.error('Error obteniendo delitos locales:', error);
        return {};
    }
}

/**
 * Cargar delitos
 */
async function cargarDelitos() {
    const lista = document.getElementById('delitosLista');
    
    try {
        // Cargar delitos del servidor
        const params = selectedMesa ? { mesa_id: selectedMesa.id } : {};
        const response = await APIClient.getDelitos(params);
        
        let delitosServidor = [];
        if (response.success) {
            delitosServidor = response.data || [];
        }
        
        // Cargar delitos locales (usar SyncManager si está disponible)
        const delitosLocalesObj = window.syncManager ? 
            window.syncManager.getLocalCrimes() : 
            obtenerDelitosLocales();
        const delitosLocales = Object.values(delitosLocalesObj);
        
        // Combinar ambos
        const todosDelitos = [...delitosServidor, ...delitosLocales];
        
        if (todosDelitos.length === 0) {
            lista.innerHTML = '<p class="text-muted text-center py-4">No hay delitos reportados</p>';
            return;
        }
        
        lista.innerHTML = todosDelitos.map(delito => {
            const esLocal = delito.sincronizado === false;
            const gravedadColor = getGravedadColor(delito.gravedad || 'media');
            
            return `
                <div class="card mb-3 border-${gravedadColor}">
                    <div class="card-header bg-${gravedadColor} bg-opacity-10">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <h6 class="mb-1 text-${gravedadColor}">${delito.titulo || getTipoDelitoLabel(delito.tipo_delito)}</h6>
                                <span class="badge bg-${gravedadColor}">${delito.gravedad_label || delito.gravedad || 'Media'}</span>
                            </div>
                            <span class="badge ${esLocal ? 'bg-warning' : 'bg-success'}">
                                ${esLocal ? '💾 Local' : '✓ Reportado'}
                            </span>
                        </div>
                    </div>
                    <div class="card-body">
                        <p class="mb-2">${delito.descripcion}</p>
                        ${delito.testigos_adicionales ? `<p class="mb-2"><strong>Testigos:</strong> ${delito.testigos_adicionales}</p>` : ''}
                        <small class="text-muted">
                            <i class="bi bi-clock"></i> ${Utils.formatDate(delito.fecha_hora || delito.created_at)}
                            ${delito.mesa_codigo ? `• Mesa ${delito.mesa_codigo}` : ''}
                        </small>
                    </div>
                </div>
            `;
        }).join('');
        
    } catch (error) {
        console.error('Error cargando delitos:', error);
        lista.innerHTML = '<div class="alert alert-warning">Error al cargar delitos</div>';
    }
}

/**
 * Obtener color según gravedad
 */
function getGravedadColor(gravedad) {
    const colors = {
        'leve': 'info',
        'media': 'warning',
        'grave': 'danger',
        'muy_grave': 'dark'
    };
    return colors[gravedad] || 'danger';
}

/**
 * Obtener label del tipo de delito
 */
function getTipoDelitoLabel(tipo) {
    const labels = {
        'compra_votos': 'Compra de votos',
        'coaccion': 'Coacción al votante',
        'fraude': 'Fraude electoral',
        'suplantacion': 'Suplantación de identidad',
        'alteracion': 'Alteración de resultados',
        'otros': 'Otros delitos'
    };
    return labels[tipo] || tipo;
}

/**
 * Sincronizar todos los datos locales con el servidor
 */
async function sincronizarTodosDatosLocales(silencioso = false) {
    try {
        if (!silencioso) {
            console.log('Iniciando sincronización completa de datos locales...');
        }
        
        // Sincronizar formularios E-14
        const resultadosFormularios = await sincronizarBorradoresLocales(silencioso);
        
        // Sincronizar incidentes
        const resultadosIncidentes = await sincronizarIncidentesLocales(silencioso);
        
        // Sincronizar delitos
        const resultadosDelitos = await sincronizarDelitosLocales(silencioso);
        
        // Calcular totales
        const totalSincronizados = resultadosFormularios.sincronizados + 
                                   resultadosIncidentes.sincronizados + 
                                   resultadosDelitos.sincronizados;
        
        const totalErrores = resultadosFormularios.errores + 
                            resultadosIncidentes.errores + 
                            resultadosDelitos.errores;
        
        // Mostrar resumen si no es silencioso
        if (!silencioso && (totalSincronizados > 0 || totalErrores > 0)) {
            let mensaje = '';
            
            if (totalSincronizados > 0) {
                mensaje += `✓ ${totalSincronizados} registro(s) sincronizado(s)`;
            }
            
            if (totalErrores > 0) {
                if (mensaje) mensaje += '\n';
                mensaje += `⚠️ ${totalErrores} registro(s) con error`;
            }
            
            if (totalSincronizados > 0 && totalErrores === 0) {
                Utils.showSuccess(mensaje);
            } else if (totalErrores > 0) {
                Utils.showWarning(mensaje);
            }
            
            // Actualizar vistas
            loadForms();
            cargarIncidentes();
            cargarDelitos();
        }
        
        // Actualizar indicador de sincronización
        actualizarIndicadorSincronizacion();
        
        console.log(`Sincronización completa: ${totalSincronizados} sincronizados, ${totalErrores} errores`);
        
        return { totalSincronizados, totalErrores };
        
    } catch (error) {
        console.error('Error en sincronización completa:', error);
        if (!silencioso) {
            Utils.showError('Error al sincronizar datos');
        }
        return { totalSincronizados: 0, totalErrores: 0 };
    }
}

/**
 * Actualizar indicador de sincronización
 */
function actualizarIndicadorSincronizacion() {
    const borradores = obtenerBorradoresLocales();
    const incidentes = obtenerIncidentesLocales();
    const delitos = obtenerDelitosLocales();
    
    // Contar pendientes
    const borradoresPendientes = Object.keys(borradores).length;
    const incidentesPendientes = Object.values(incidentes).filter(i => !i.sincronizado).length;
    const delitosPendientes = Object.values(delitos).filter(d => !d.sincronizado).length;
    
    const totalPendientes = borradoresPendientes + incidentesPendientes + delitosPendientes;
    
    // Buscar o crear indicador
    let indicador = document.getElementById('indicadorSincronizacion');
    
    if (totalPendientes > 0) {
        if (!indicador) {
            indicador = document.createElement('div');
            indicador.id = 'indicadorSincronizacion';
            indicador.className = 'alert alert-warning d-flex justify-content-between align-items-center';
            indicador.style.position = 'fixed';
            indicador.style.bottom = '20px';
            indicador.style.right = '20px';
            indicador.style.zIndex = '1050';
            indicador.style.minWidth = '300px';
            indicador.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
            document.body.appendChild(indicador);
        }
        
        indicador.innerHTML = `
            <div>
                <i class="bi bi-cloud-upload"></i>
                <strong>${totalPendientes}</strong> registro(s) pendiente(s) de sincronizar
                <br>
                <small class="text-muted">
                    ${borradoresPendientes > 0 ? `${borradoresPendientes} formulario(s) ` : ''}
                    ${incidentesPendientes > 0 ? `${incidentesPendientes} incidente(s) ` : ''}
                    ${delitosPendientes > 0 ? `${delitosPendientes} delito(s)` : ''}
                </small>
            </div>
            <button class="btn btn-sm btn-warning" onclick="sincronizarTodosDatosLocales()">
                <i class="bi bi-arrow-repeat"></i> Sincronizar
            </button>
        `;
    } else {
        // Eliminar indicador si no hay pendientes
        if (indicador) {
            indicador.remove();
        }
    }
}

// Cargar incidentes y delitos al cambiar de pestaña
document.addEventListener('DOMContentLoaded', function() {
    const incidentesTab = document.getElementById('incidentes-tab');
    const delitosTab = document.getElementById('delitos-tab');
    
    if (incidentesTab) {
        incidentesTab.addEventListener('shown.bs.tab', function() {
            cargarIncidentes();
        });
    }
    
    if (delitosTab) {
        delitosTab.addEventListener('shown.bs.tab', function() {
            cargarDelitos();
        });
    }
    
    // Actualizar indicador cada 30 segundos
    setInterval(() => {
        actualizarIndicadorSincronizacion();
    }, 30000);
});


// ============================================================================
// EXPONER FUNCIONES GLOBALMENTE
// ============================================================================
window.showCreateForm = showCreateForm;
window.cambiarMesa = cambiarMesa;
window.cambiarMesaFormulario = cambiarMesaFormulario;
window.verificarPresencia = verificarPresencia;
window.habilitarBotonNuevoFormulario = habilitarBotonNuevoFormulario;
window.loadUserProfile = loadUserProfile;
window.loadMesas = loadMesas;
window.loadForms = loadForms;
window.loadTiposEleccion = loadTiposEleccion;
window.cargarPartidosYCandidatos = cargarPartidosYCandidatos;
window.actualizarPanelMesas = actualizarPanelMesas;
window.saveForm = saveForm;
window.calcularTotales = calcularTotales;
window.setupImagePreview = setupImagePreview;
window.abrirCamara = abrirCamara;

console.log('✅ testigo-dashboard-v2.js cargado - Funciones expuestas globalmente');


// ============================================
// FUNCIONES PARA MANEJO DE FOTOS EN INCIDENTES Y DELITOS
// ============================================

/**
 * Configurar preview de foto para incidente
 */
document.addEventListener('DOMContentLoaded', function() {
    const fotoIncidente = document.getElementById('fotoIncidente');
    if (fotoIncidente) {
        fotoIncidente.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('imgPreviewIncidente').src = e.target.result;
                    document.getElementById('previewIncidente').style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    const fotoDelito = document.getElementById('fotoDelito');
    if (fotoDelito) {
        fotoDelito.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('imgPreviewDelito').src = e.target.result;
                    document.getElementById('previewDelito').style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });
    }
});

/**
 * Limpiar foto de incidente
 */
function limpiarFotoIncidente() {
    document.getElementById('fotoIncidente').value = '';
    document.getElementById('imgPreviewIncidente').src = '';
    document.getElementById('previewIncidente').style.display = 'none';
}

/**
 * Limpiar foto de delito
 */
function limpiarFotoDelito() {
    document.getElementById('fotoDelito').value = '';
    document.getElementById('imgPreviewDelito').src = '';
    document.getElementById('previewDelito').style.display = 'none';
}

/**
 * Abrir cámara para tomar foto del formulario
 */
function abrirCamara() {
    // Crear un input de archivo temporal con capacidad de captura
    const tempInput = document.createElement('input');
    tempInput.type = 'file';
    tempInput.accept = 'image/*';
    tempInput.capture = 'environment'; // Usa la cámara trasera
    tempInput.style.display = 'none';
    
    // Manejar la selección de archivo
    tempInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            // Verificar que sea una imagen
            if (file.type.startsWith('image/')) {
                // Crear un DataTransfer para establecer los archivos en el input principal
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                
                // Establecer el archivo en el input principal del formulario
                const imagenInput = document.getElementById('imagen');
                if (imagenInput) {
                    imagenInput.files = dataTransfer.files;
                    
                    // Disparar el evento change para activar la vista previa
                    const changeEvent = new Event('change');
                    imagenInput.dispatchEvent(changeEvent);
                    
                    console.log('📸 Foto capturada y establecida en el input del formulario');
                } else {
                    console.error('❌ No se encontró el input de imagen principal');
                }
            } else {
                if (window.Utils) {
                    Utils.showError('Por favor seleccione una imagen válida');
                } else {
                    alert('Por favor seleccione una imagen válida');
                }
            }
        }
        
        // Limpiar: eliminar el input temporal
        tempInput.remove();
    });
    
    // Manejar cancelación (cuando no se selecciona ningún archivo)
    tempInput.addEventListener('cancel', function() {
        tempInput.remove();
    });
    
    // Agregar el input al documento y hacer clic en él
    document.body.appendChild(tempInput);
    tempInput.click();
}

// Exponer funciones globalmente
window.loadUserProfile = loadUserProfile;
window.loadMesas = loadMesas;
window.loadForms = loadForms;
window.loadTiposEleccion = loadTiposEleccion;
window.cargarPartidosYCandidatos = cargarPartidosYCandidatos;
window.actualizarPanelMesas = actualizarPanelMesas;
window.saveForm = saveForm;
window.calcularTotales = calcularTotales;
window.setupImagePreview = setupImagePreview;
window.abrirCamara = abrirCamara;

console.log('✅ testigo-dashboard-v2.js cargado - Funciones expuestas globalmente');
