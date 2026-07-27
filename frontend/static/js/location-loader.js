/**
 * Location Loader - Funciones compartidas para cargar ubicaciones desde la BD
 * Usado por todos los roles del sistema
 */

/**
 * Cargar partidos en select
 */
async function loadPartidosForSelect(selectId) {
    // Verificar que el usuario esté autenticado
    if (!localStorage.getItem('access_token')) {
        console.warn('Usuario no autenticado, no se pueden cargar partidos');
        return;
    }
    
    try {
        const response = await APIClient.get('/locations/partidos');
        const select = document.getElementById(selectId);
        if (response.success && select) {
            // Limpiar opciones existentes (excepto la primera)
            select.innerHTML = '<option value="">Seleccionar partido...</option>';
            // Agregar partidos activos
            response.data.filter(partido => partido.activo).forEach(partido => {
                const option = document.createElement('option');
                option.value = partido.id;
                option.textContent = `${partido.nombre} (${partido.nombre_corto || 'Sin sigla'})`;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error cargando partidos:', error);
    }
}

/**
 * Cargar tipos de elección en select
 */
async function loadTiposEleccionForSelect(selectId) {
    // Verificar que el usuario esté autenticado
    if (!localStorage.getItem('access_token')) {
        console.warn('Usuario no autenticado, no se pueden cargar tipos de elección');
        return;
    }
    
    try {
        const response = await APIClient.get('/locations/tipos-eleccion');
        const select = document.getElementById(selectId);
        if (response.success && select) {
            // Limpiar opciones existentes (excepto la primera)
            select.innerHTML = '<option value="">Seleccionar tipo...</option>';
            // Agregar tipos activos
            response.data.filter(tipo => tipo.activo).forEach(tipo => {
                const option = document.createElement('option');
                option.value = tipo.id;
                option.textContent = tipo.nombre;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error cargando tipos de elección:', error);
    }
}

/**
 * Cargar departamentos en select (solo Caquetá)
 * Endpoint público - no requiere autenticación
 */
async function loadDepartamentosForSelect(selectId) {
    try {
        const response = await APIClient.get('/locations/departamentos');
        const select = document.getElementById(selectId);
        
        if (!select) {
            console.warn(`Select con id '${selectId}' no encontrado`);
            return;
        }
        
        if (response && response.success && response.data && response.data.length > 0) {
            // Limpiar opciones existentes (excepto la primera)
            select.innerHTML = '<option value="">Seleccionar departamento...</option>';
            
            // Agregar departamentos (solo Caquetá)
            response.data.forEach(depto => {
                const option = document.createElement('option');
                option.value = depto.departamento_codigo;
                option.textContent = depto.departamento_nombre;
                select.appendChild(option);
            });
            
            // Si solo hay un departamento (Caquetá), seleccionarlo automáticamente
            if (response.data.length === 1) {
                select.value = response.data[0].departamento_codigo;
                // Disparar evento change para cargar municipios
                const event = new Event('change', { bubbles: true });
                select.dispatchEvent(event);
            }
        } else {
            console.error('No se recibieron datos de departamentos:', response);
            select.innerHTML = '<option value="">Error cargando departamentos</option>';
        }
    } catch (error) {
        console.error('Error cargando departamentos:', error);
        const select = document.getElementById(selectId);
        if (select) {
            select.innerHTML = '<option value="">Error de conexión</option>';
        }
    }
}

/**
 * Cargar municipios en select
 * Endpoint público - no requiere autenticación
 */
async function loadMunicipiosForSelect(selectId, departamentoId) {
    const select = document.getElementById(selectId);
    
    if (!select) {
        console.warn(`Select con id '${selectId}' no encontrado`);
        return;
    }
    
    if (!departamentoId) {
        select.innerHTML = '<option value="">Seleccione departamento primero</option>';
        return;
    }
    
    try {
        const response = await APIClient.get(`/locations/municipios/${departamentoId}`);
        
        if (response && response.success && response.data) {
            // Limpiar opciones existentes
            select.innerHTML = '<option value="">Seleccionar municipio...</option>';
            
            // Agregar municipios
            response.data.forEach(muni => {
                const option = document.createElement('option');
                option.value = muni.municipio_codigo;
                option.textContent = muni.municipio_nombre;
                select.appendChild(option);
            });
        } else {
            select.innerHTML = '<option value="">No hay municipios disponibles</option>';
        }
    } catch (error) {
        console.error('Error cargando municipios:', error);
        select.innerHTML = '<option value="">Error de conexión</option>';
    }
}

/**
 * Cargar zonas en select
 */
async function loadZonasForSelect(selectId, municipioId) {
    try {
        const response = await APIClient.get(`/locations/zonas/${municipioId}`);
        const select = document.getElementById(selectId);
        if (response.success && select) {
            // Limpiar opciones existentes (excepto la primera)
            select.innerHTML = '<option value="">Seleccionar zona...</option>';
            // Agregar zonas
            response.data.forEach(zona => {
                const option = document.createElement('option');
                option.value = zona.zona_codigo;
                option.textContent = zona.zona_nombre;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error cargando zonas:', error);
    }
}

/**
 * Cargar puestos en select
 */
async function loadPuestosForSelect(selectId, zonaId) {
    try {
        const response = await APIClient.get(`/locations/puestos/${zonaId}`);
        const select = document.getElementById(selectId);
        if (response.success && select) {
            // Limpiar opciones existentes (excepto la primera)
            select.innerHTML = '<option value="">Seleccionar puesto...</option>';
            // Agregar puestos
            response.data.forEach(puesto => {
                const option = document.createElement('option');
                option.value = puesto.puesto_codigo;
                option.textContent = puesto.puesto_nombre;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error cargando puestos:', error);
    }
}

/**
 * Cargar mesas en select
 */
async function loadMesasForSelect(selectId, puestoId) {
    try {
        const response = await APIClient.get(`/locations/mesas/${puestoId}`);
        const select = document.getElementById(selectId);
        if (response.success && select) {
            // Limpiar opciones existentes (excepto la primera)
            select.innerHTML = '<option value="">Seleccionar mesa...</option>';
            // Agregar mesas
            response.data.forEach(mesa => {
                const option = document.createElement('option');
                option.value = mesa.mesa_codigo;
                option.textContent = mesa.mesa_nombre;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error cargando mesas:', error);
    }
}

/**
 * Configurar cascada de ubicaciones
 * @param {string} prefix - Prefijo de los IDs de los selects (ej: 'edit', 'create')
 */
function setupLocationCascade(prefix) {
    const departamentoSelect = document.getElementById(`${prefix}Departamento`);
    const municipioSelect = document.getElementById(`${prefix}Municipio`);
    const zonaSelect = document.getElementById(`${prefix}Zona`);
    const puestoSelect = document.getElementById(`${prefix}Puesto`);
    const mesaSelect = document.getElementById(`${prefix}Mesa`);

    if (departamentoSelect) {
        departamentoSelect.addEventListener('change', async function() {
            const departamentoId = this.value;
            
            // Limpiar selects dependientes
            if (municipioSelect) {
                municipioSelect.innerHTML = '<option value="">Seleccionar municipio...</option>';
            }
            if (zonaSelect) {
                zonaSelect.innerHTML = '<option value="">Seleccionar zona...</option>';
            }
            if (puestoSelect) {
                puestoSelect.innerHTML = '<option value="">Seleccionar puesto...</option>';
            }
            if (mesaSelect) {
                mesaSelect.innerHTML = '<option value="">Seleccionar mesa...</option>';
            }

            if (departamentoId && municipioSelect) {
                await loadMunicipiosForSelect(`${prefix}Municipio`, departamentoId);
            }
        });
    }

    if (municipioSelect) {
        municipioSelect.addEventListener('change', async function() {
            const municipioId = this.value;
            
            // Limpiar selects dependientes
            if (zonaSelect) {
                zonaSelect.innerHTML = '<option value="">Seleccionar zona...</option>';
            }
            if (puestoSelect) {
                puestoSelect.innerHTML = '<option value="">Seleccionar puesto...</option>';
            }
            if (mesaSelect) {
                mesaSelect.innerHTML = '<option value="">Seleccionar mesa...</option>';
            }

            if (municipioId && zonaSelect) {
                await loadZonasForSelect(`${prefix}Zona`, municipioId);
            }
        });
    }

    if (zonaSelect) {
        zonaSelect.addEventListener('change', async function() {
            const zonaId = this.value;
            
            // Limpiar selects dependientes
            if (puestoSelect) {
                puestoSelect.innerHTML = '<option value="">Seleccionar puesto...</option>';
            }
            if (mesaSelect) {
                mesaSelect.innerHTML = '<option value="">Seleccionar mesa...</option>';
            }

            if (zonaId && puestoSelect) {
                await loadPuestosForSelect(`${prefix}Puesto`, zonaId);
            }
        });
    }

    if (puestoSelect) {
        puestoSelect.addEventListener('change', async function() {
            const puestoId = this.value;
            
            // Limpiar select dependiente
            if (mesaSelect) {
                mesaSelect.innerHTML = '<option value="">Seleccionar mesa...</option>';
            }

            if (puestoId && mesaSelect) {
                await loadMesasForSelect(`${prefix}Mesa`, puestoId);
            }
        });
    }
}
