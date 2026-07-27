/**
 * Configuración Electoral - Admin
 */

document.addEventListener('DOMContentLoaded', function() {
    loadTiposEleccion();
    loadPartidos();
    loadCandidatos();
    loadCoaliciones();
});

// ============================================================================
// TIPOS DE ELECCIÓN
// ============================================================================

async function loadTiposEleccion() {
    try {
        const response = await APIClient.getTiposEleccion();
        const container = document.getElementById('tiposContainer');
        
        if (response.data.length === 0) {
            container.innerHTML = '<p class="text-center text-muted">No hay tipos de elección configurados</p>';
            return;
        }
        
        let html = '';
        response.data.forEach(tipo => {
            html += `
                <div class="item-card">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <strong>${tipo.nombre}</strong>
                            <br><small class="text-muted">Código: ${tipo.codigo}</small>
                        </div>
                        <div>
                            <span class="badge ${tipo.activo ? 'bg-success' : 'bg-secondary'}">
                                ${tipo.activo ? 'Activo' : 'Inactivo'}
                            </span>
                        </div>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    } catch (error) {
        console.error('Error loading tipos:', error);
        Utils.showError('Error cargando tipos de elección');
    }
}

function showModalTipoEleccion() {
    document.getElementById('formTipoEleccion').reset();
    new bootstrap.Modal(document.getElementById('modalTipoEleccion')).show();
}

async function saveTipoEleccion() {
    try {
        const form = document.getElementById('formTipoEleccion');
        const formData = new FormData(form);
        
        const data = {
            codigo: formData.get('codigo'),
            nombre: formData.get('nombre'),
            descripcion: formData.get('descripcion'),
            orden: parseInt(formData.get('orden')) || 0
        };
        
        await APIClient.createTipoEleccion(data);
        
        Utils.showSuccess('Tipo de elección creado exitosamente');
        bootstrap.Modal.getInstance(document.getElementById('modalTipoEleccion')).hide();
        loadTiposEleccion();
    } catch (error) {
        Utils.showError('Error al crear tipo de elección: ' + error.message);
    }
}

// ============================================================================
// PARTIDOS
// ============================================================================

async function loadPartidos() {
    try {
        const response = await APIClient.getPartidos();
        const container = document.getElementById('partidosContainer');
        
        if (response.data.length === 0) {
            container.innerHTML = '<p class="text-center text-muted">No hay partidos configurados</p>';
            return;
        }
        
        let html = '';
        response.data.forEach(partido => {
            html += `
                <div class="item-card">
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="d-flex align-items-center gap-3">
                            <div class="color-preview" style="background-color: ${partido.color || '#000'}"></div>
                            <div>
                                <strong>${partido.nombre}</strong>
                                <br><small class="text-muted">${partido.nombre_corto || partido.codigo}</small>
                            </div>
                        </div>
                        <div>
                            <span class="badge ${partido.activo ? 'bg-success' : 'bg-secondary'}">
                                ${partido.activo ? 'Activo' : 'Inactivo'}
                            </span>
                        </div>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    } catch (error) {
        console.error('Error loading partidos:', error);
        Utils.showError('Error cargando partidos');
    }
}

function showModalPartido() {
    document.getElementById('formPartido').reset();
    new bootstrap.Modal(document.getElementById('modalPartido')).show();
}

async function savePartido() {
    try {
        const form = document.getElementById('formPartido');
        const formData = new FormData(form);
        
        const data = {
            codigo: formData.get('codigo'),
            nombre: formData.get('nombre'),
            nombre_corto: formData.get('nombre_corto'),
            color: formData.get('color'),
            orden: parseInt(formData.get('orden')) || 0
        };
        
        await APIClient.createPartido(data);
        
        Utils.showSuccess('Partido creado exitosamente');
        bootstrap.Modal.getInstance(document.getElementById('modalPartido')).hide();
        loadPartidos();
    } catch (error) {
        Utils.showError('Error al crear partido: ' + error.message);
    }
}

// ============================================================================
// CANDIDATOS
// ============================================================================

async function loadCandidatos() {
    try {
        const response = await APIClient.getCandidatos();
        const container = document.getElementById('candidatosContainer');
        
        if (response.data.length === 0) {
            container.innerHTML = '<p class="text-center text-muted">No hay candidatos configurados</p>';
            return;
        }
        
        let html = '';
        response.data.forEach(candidato => {
            const partidoNombre = candidato.partido ? candidato.partido.nombre_corto : 'Independiente';
            const tipoEleccion = candidato.tipo_eleccion ? candidato.tipo_eleccion.nombre : 'N/A';
            
            html += `
                <div class="item-card">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <strong>${candidato.nombre_completo}</strong>
                            ${candidato.numero_lista ? `<span class="badge bg-primary ms-2">#${candidato.numero_lista}</span>` : ''}
                            <br><small class="text-muted">${partidoNombre} - ${tipoEleccion}</small>
                        </div>
                        <div>
                            ${candidato.es_independiente ? '<span class="badge bg-info me-2">Independiente</span>' : ''}
                            <span class="badge ${candidato.activo ? 'bg-success' : 'bg-secondary'}">
                                ${candidato.activo ? 'Activo' : 'Inactivo'}
                            </span>
                        </div>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    } catch (error) {
        console.error('Error loading candidatos:', error);
        Utils.showError('Error cargando candidatos');
    }
}

async function showModalCandidato() {
    document.getElementById('formCandidato').reset();
    
    // Cargar tipos de elección
    try {
        const tiposResponse = await APIClient.getTiposEleccion();
        const tipoSelect = document.getElementById('tipoEleccionSelect');
        tipoSelect.innerHTML = '<option value="">Seleccione...</option>';
        tiposResponse.data.forEach(tipo => {
            tipoSelect.innerHTML += `<option value="${tipo.id}">${tipo.nombre}</option>`;
        });
        
        // Cargar partidos
        const partidosResponse = await APIClient.getPartidos();
        const partidoSelect = document.getElementById('partidoSelect');
        partidoSelect.innerHTML = '<option value="">Independiente</option>';
        partidosResponse.data.forEach(partido => {
            partidoSelect.innerHTML += `<option value="${partido.id}">${partido.nombre_corto || partido.nombre}</option>`;
        });
        
        new bootstrap.Modal(document.getElementById('modalCandidato')).show();
    } catch (error) {
        Utils.showError('Error cargando datos para el formulario');
    }
}

async function saveCandidato() {
    try {
        const form = document.getElementById('formCandidato');
        const formData = new FormData(form);
        
        const data = {
            codigo: formData.get('codigo'),
            nombre_completo: formData.get('nombre_completo'),
            tipo_eleccion_id: parseInt(formData.get('tipo_eleccion_id')),
            partido_id: formData.get('partido_id') ? parseInt(formData.get('partido_id')) : null,
            numero_lista: formData.get('numero_lista') ? parseInt(formData.get('numero_lista')) : null,
            es_independiente: formData.get('es_independiente') === 'on'
        };
        
        await APIClient.createCandidato(data);
        
        Utils.showSuccess('Candidato creado exitosamente');
        bootstrap.Modal.getInstance(document.getElementById('modalCandidato')).hide();
        loadCandidatos();
    } catch (error) {
        Utils.showError('Error al crear candidato: ' + error.message);
    }
}

// ============================================================================
// COALICIONES
// ============================================================================

async function loadCoaliciones() {
    try {
        const response = await APIClient.getCoaliciones();
        const container = document.getElementById('coalicionesContainer');
        
        if (response.data.length === 0) {
            container.innerHTML = '<p class="text-center text-muted">No hay coaliciones configuradas</p>';
            return;
        }
        
        let html = '';
        response.data.forEach(coalicion => {
            const partidos = coalicion.partidos.map(p => p.nombre_corto || p.nombre).join(', ');
            
            html += `
                <div class="item-card">
                    <div>
                        <strong>${coalicion.nombre}</strong>
                        <br><small class="text-muted">Partidos: ${partidos}</small>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    } catch (error) {
        console.error('Error loading coaliciones:', error);
        Utils.showError('Error cargando coaliciones');
    }
}

function showModalCoalicion() {
    Utils.showInfo('Funcionalidad de coaliciones en desarrollo');
}
