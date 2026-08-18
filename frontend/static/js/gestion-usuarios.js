/**
 * Gestión Automática de Usuarios
 * Sistema para crear testigos, coordinadores y administradores basados en DIVIPOLA
 */

class GestionUsuarios {
    constructor() {
        this.puestosData = [];
        this.municipiosData = [];
        this.departamentosData = [];
    }

    async init() {
        await this.cargarUbicaciones();
        this.setupEventListeners();
    }

    async cargarUbicaciones() {
        try {
            // Cargar puestos
            const puestosResponse = await APIClient.get('/gestion-usuarios/puestos');
            this.puestosData = puestosResponse.puestos || [];

            // Cargar municipios
            const municipiosResponse = await APIClient.get('/gestion-usuarios/municipios');
            this.municipiosData = municipiosResponse.municipios || [];

            // Cargar departamentos
            const departamentosResponse = await APIClient.get('/gestion-usuarios/departamentos');
            this.departamentosData = departamentosResponse.departamentos || [];

            this.populateSelects();
        } catch (error) {
            console.error('Error cargando ubicaciones:', error);
            Utils.showError('Error cargando ubicaciones');
        }
    }

    populateSelects() {
        // Poblar select de puestos para testigos
        const selectPuestoTestigos = document.getElementById('selectPuestoTestigos');
        if (selectPuestoTestigos) {
            selectPuestoTestigos.innerHTML = '<option value="">Seleccione un puesto...</option>';
            this.puestosData.forEach(puesto => {
                const option = document.createElement('option');
                option.value = puesto.id;
                option.textContent = `${puesto.nombre_completo} (${puesto.total_mesas} mesas)`;
                selectPuestoTestigos.appendChild(option);
            });
        }

        // Poblar select de puestos para coordinadores
        const selectPuestoCoordinador = document.getElementById('selectPuestoCoordinador');
        if (selectPuestoCoordinador) {
            selectPuestoCoordinador.innerHTML = '<option value="">Seleccione un puesto...</option>';
            this.puestosData.forEach(puesto => {
                const option = document.createElement('option');
                option.value = puesto.id;
                option.textContent = `${puesto.nombre_completo} (${puesto.total_mesas} mesas)`;
                selectPuestoCoordinador.appendChild(option);
            });
        }

        // Poblar select de municipios
        const selectMunicipio = document.getElementById('selectMunicipio');
        if (selectMunicipio) {
            selectMunicipio.innerHTML = '<option value="">Seleccione un municipio...</option>';
            this.municipiosData.forEach(municipio => {
                const option = document.createElement('option');
                option.value = municipio.id;
                option.textContent = `${municipio.nombre_completo} (${municipio.total_puestos} puestos)`;
                selectMunicipio.appendChild(option);
            });
        }

        // Poblar select de departamentos
        const selectDepartamento = document.getElementById('selectDepartamento');
        if (selectDepartamento) {
            selectDepartamento.innerHTML = '<option value="">Seleccione un departamento...</option>';
            this.departamentosData.forEach(departamento => {
                const option = document.createElement('option');
                option.value = departamento.id;
                option.textContent = `${departamento.nombre_completo} (${departamento.total_municipios} municipios)`;
                selectDepartamento.appendChild(option);
            });
        }
    }

    async crearTestigosPuesto(puestoId, cantidad = null) {
        const puesto = this.puestosData.find(p => p.id === puestoId);
        const mensaje = cantidad 
            ? `¿Crear ${cantidad} testigo(s) para este puesto?`
            : `¿Crear testigos para todas las mesas disponibles (${puesto ? puesto.total_mesas : '?'} mesas)?`;
        
        if (!confirm(mensaje)) {
            return;
        }

        try {
            Utils.showLoading('Creando testigos...');
            
            const payload = { puesto_id: puestoId };
            if (cantidad !== null) {
                payload.cantidad = cantidad;
            }
            
            const response = await APIClient.post('/gestion-usuarios/crear-testigos-puesto', payload);

            if (response.success) {
                const data = response.data;
                
                // Mostrar credenciales
                this.mostrarCredenciales(
                    `Testigos Creados - ${data.puesto}`,
                    data.testigos_creados
                );

                let mensaje = `${data.total_creados} testigo(s) creado(s) exitosamente\n`;
                mensaje += `Total de testigos en el puesto: ${data.total_testigos_ahora}/${data.total_mesas}\n`;
                
                if (data.espacios_disponibles > 0) {
                    mensaje += `Espacios disponibles: ${data.espacios_disponibles}`;
                } else {
                    mensaje += `Puesto completo (todos los testigos asignados)`;
                }
                
                Utils.showSuccess(mensaje);
                
                if (data.total_existentes_previos > 0) {
                    Utils.showInfo(`Ya existían ${data.total_existentes_previos} testigos en este puesto`);
                }
            } else {
                Utils.showError(response.error || 'Error creando testigos');
            }
        } catch (error) {
            console.error('Error:', error);
            Utils.showError('Error creando testigos: ' + error.message);
        } finally {
            Utils.hideLoading();
        }
    }

    async crearCoordinadorPuesto(puestoId) {
        if (!confirm('¿Crear coordinador para este puesto?')) {
            return;
        }

        try {
            Utils.showLoading('Creando coordinador...');
            
            const response = await APIClient.post('/gestion-usuarios/crear-coordinador-puesto', {
                puesto_id: puestoId
            });

            if (response.success) {
                const data = response.data;
                
                // Mostrar credenciales
                this.mostrarCredenciales(
                    `Coordinador Creado - ${data.puesto}`,
                    [data]
                );

                Utils.showSuccess('Coordinador creado exitosamente');
            } else {
                Utils.showError(response.error || 'Error creando coordinador');
            }
        } catch (error) {
            console.error('Error:', error);
            Utils.showError('Error creando coordinador: ' + error.message);
        } finally {
            Utils.hideLoading();
        }
    }

    async crearUsuariosMunicipio(municipioId) {
        if (!confirm('¿Crear coordinador y administrador municipal?')) {
            return;
        }

        try {
            Utils.showLoading('Creando usuarios municipales...');
            
            const response = await APIClient.post('/gestion-usuarios/crear-usuarios-municipio', {
                municipio_id: municipioId,
                crear_coordinador: true,
                crear_admin: true
            });

            if (response.success) {
                const data = response.data;
                
                // Mostrar credenciales
                this.mostrarCredenciales(
                    `Usuarios Creados - ${data.municipio}`,
                    data.usuarios_creados
                );

                Utils.showSuccess(`${data.usuarios_creados.length} usuarios creados exitosamente`);
            } else {
                Utils.showError(response.error || 'Error creando usuarios');
            }
        } catch (error) {
            console.error('Error:', error);
            Utils.showError('Error creando usuarios: ' + error.message);
        } finally {
            Utils.hideLoading();
        }
    }

    async crearUsuariosDepartamento(departamentoId) {
        if (!confirm('¿Crear coordinador y administrador departamental?')) {
            return;
        }

        try {
            Utils.showLoading('Creando usuarios departamentales...');
            
            const response = await APIClient.post('/gestion-usuarios/crear-usuarios-departamento', {
                departamento_id: departamentoId,
                crear_coordinador: true,
                crear_admin: true
            });

            if (response.success) {
                const data = response.data;
                
                // Mostrar credenciales
                this.mostrarCredenciales(
                    `Usuarios Creados - ${data.departamento}`,
                    data.usuarios_creados
                );

                Utils.showSuccess(`${data.usuarios_creados.length} usuarios creados exitosamente`);
            } else {
                Utils.showError(response.error || 'Error creando usuarios');
            }
        } catch (error) {
            console.error('Error:', error);
            Utils.showError('Error creando usuarios: ' + error.message);
        } finally {
            Utils.hideLoading();
        }
    }

    mostrarCredenciales(titulo, usuarios) {
        let html = `<div class="modal fade" id="credencialesModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-success text-white">
                        <h5 class="modal-title"><i class="bi bi-check-circle-fill"></i> ${titulo}</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="alert alert-warning">
                            <i class="bi bi-exclamation-triangle-fill"></i>
                            <strong>Importante:</strong> Guarda estas credenciales. Solo se mostrarán una vez.
                        </div>
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>Usuario</th>
                                        <th>Contraseña</th>
                                        <th>Rol</th>
                                        ${usuarios[0].mesa ? '<th>Mesa</th>' : ''}
                                        ${usuarios[0].votantes ? '<th>Votantes</th>' : ''}
                                    </tr>
                                </thead>
                                <tbody>`;

        usuarios.forEach(usuario => {
            html += `<tr>
                <td><code>${usuario.username}</code></td>
                <td><code>${usuario.password}</code></td>
                <td><span class="badge bg-primary">${usuario.rol || 'testigo_electoral'}</span></td>
                ${usuario.mesa ? `<td>${usuario.mesa_codigo || usuario.mesa}</td>` : ''}
                ${usuario.votantes ? `<td>${usuario.votantes}</td>` : ''}
            </tr>`;
        });

        html += `</tbody>
                            </table>
                        </div>
                        <button class="btn btn-primary" onclick="gestionUsuarios.copiarCredenciales()">
                            <i class="bi bi-clipboard"></i> Copiar Todas
                        </button>
                        <button class="btn btn-success" onclick="gestionUsuarios.descargarCredenciales('${titulo}')">
                            <i class="bi bi-download"></i> Descargar
                        </button>
                    </div>
                </div>
            </div>
        </div>`;

        // Remover modal anterior si existe
        const oldModal = document.getElementById('credencialesModal');
        if (oldModal) {
            oldModal.remove();
        }

        // Agregar nuevo modal
        document.body.insertAdjacentHTML('beforeend', html);

        // Mostrar modal
        const modal = new bootstrap.Modal(document.getElementById('credencialesModal'));
        modal.show();

        // Guardar credenciales para copiar/descargar
        this.ultimasCredenciales = { titulo, usuarios };
    }

    copiarCredenciales() {
        if (!this.ultimasCredenciales) return;

        let texto = `${this.ultimasCredenciales.titulo}\n`;
        texto += '='.repeat(80) + '\n\n';

        this.ultimasCredenciales.usuarios.forEach(usuario => {
            texto += `Usuario: ${usuario.username}\n`;
            texto += `Contraseña: ${usuario.password}\n`;
            texto += `Rol: ${usuario.rol || 'testigo_electoral'}\n`;
            if (usuario.mesa) texto += `Mesa: ${usuario.mesa}\n`;
            if (usuario.votantes) texto += `Votantes: ${usuario.votantes}\n`;
            texto += '-'.repeat(80) + '\n\n';
        });

        navigator.clipboard.writeText(texto).then(() => {
            Utils.showSuccess('Credenciales copiadas al portapapeles');
        }).catch(err => {
            console.error('Error copiando:', err);
            Utils.showError('Error copiando credenciales');
        });
    }

    descargarCredenciales(titulo) {
        if (!this.ultimasCredenciales) return;

        let texto = `${this.ultimasCredenciales.titulo}\n`;
        texto += '='.repeat(80) + '\n\n';

        this.ultimasCredenciales.usuarios.forEach(usuario => {
            texto += `Usuario: ${usuario.username}\n`;
            texto += `Contraseña: ${usuario.password}\n`;
            texto += `Rol: ${usuario.rol || 'testigo_electoral'}\n`;
            if (usuario.mesa) texto += `Mesa: ${usuario.mesa}\n`;
            if (usuario.votantes) texto += `Votantes: ${usuario.votantes}\n`;
            texto += '-'.repeat(80) + '\n\n';
        });

        const blob = new Blob([texto], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `credenciales_${Date.now()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        Utils.showSuccess('Credenciales descargadas');
    }

    setupEventListeners() {
        // Selector de puesto para testigos - mostrar info
        const selectPuestoTestigos = document.getElementById('selectPuestoTestigos');
        if (selectPuestoTestigos) {
            selectPuestoTestigos.addEventListener('change', (e) => {
                const puestoId = e.target.value;
                if (puestoId) {
                    const puesto = this.puestosData.find(p => p.id == puestoId);
                    if (puesto) {
                        const info = document.getElementById('infoPuestoTestigos');
                        if (info) {
                            info.textContent = `Este puesto tiene ${puesto.total_mesas} mesas. Máximo ${puesto.total_mesas} testigos.`;
                        }
                        // Actualizar el max del input
                        const cantidadInput = document.getElementById('cantidadTestigos');
                        if (cantidadInput) {
                            cantidadInput.max = puesto.total_mesas;
                        }
                    }
                }
            });
        }
        
        // Botón crear testigos (cantidad específica)
        const btnCrearTestigos = document.getElementById('btnCrearTestigos');
        if (btnCrearTestigos) {
            btnCrearTestigos.addEventListener('click', () => {
                const puestoId = document.getElementById('selectPuestoTestigos').value;
                const cantidad = document.getElementById('cantidadTestigos').value;
                
                if (puestoId) {
                    this.crearTestigosPuesto(parseInt(puestoId), parseInt(cantidad) || 1);
                } else {
                    Utils.showError('Seleccione un puesto');
                }
            });
        }
        
        // Botón crear todos los testigos
        const btnCrearTodosTestigos = document.getElementById('btnCrearTodosTestigos');
        if (btnCrearTodosTestigos) {
            btnCrearTodosTestigos.addEventListener('click', () => {
                const puestoId = document.getElementById('selectPuestoTestigos').value;
                
                if (puestoId) {
                    this.crearTestigosPuesto(parseInt(puestoId), null); // null = crear todos
                } else {
                    Utils.showError('Seleccione un puesto');
                }
            });
        }

        // Botón crear coordinador de puesto
        const btnCrearCoordinadorPuesto = document.getElementById('btnCrearCoordinadorPuesto');
        if (btnCrearCoordinadorPuesto) {
            btnCrearCoordinadorPuesto.addEventListener('click', () => {
                const puestoId = document.getElementById('selectPuestoCoordinador').value;
                if (puestoId) {
                    this.crearCoordinadorPuesto(parseInt(puestoId));
                } else {
                    Utils.showError('Seleccione un puesto');
                }
            });
        }

        // Botón crear usuarios municipales
        const btnCrearUsuariosMunicipio = document.getElementById('btnCrearUsuariosMunicipio');
        if (btnCrearUsuariosMunicipio) {
            btnCrearUsuariosMunicipio.addEventListener('click', () => {
                const municipioId = document.getElementById('selectMunicipio').value;
                if (municipioId) {
                    this.crearUsuariosMunicipio(parseInt(municipioId));
                } else {
                    Utils.showError('Seleccione un municipio');
                }
            });
        }

        // Botón crear usuarios departamentales
        const btnCrearUsuariosDepartamento = document.getElementById('btnCrearUsuariosDepartamento');
        if (btnCrearUsuariosDepartamento) {
            btnCrearUsuariosDepartamento.addEventListener('click', () => {
                const departamentoId = document.getElementById('selectDepartamento').value;
                if (departamentoId) {
                    this.crearUsuariosDepartamento(parseInt(departamentoId));
                } else {
                    Utils.showError('Seleccione un departamento');
                }
            });
        }
    }
}

// Instancia global
const gestionUsuarios = new GestionUsuarios();

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    // Verificar si estamos en la página de gestión de usuarios
    if (document.getElementById('gestionTabs') || document.getElementById('selectPuestoTestigos')) {
        gestionUsuarios.init();
    }
});
