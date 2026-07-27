# ✅ Solución: Formularios Únicos por Mesa y Tipo de Elección

## 🎯 Requerimiento

**Problema:** Una mesa puede tener múltiples formularios del mismo tipo de elección, causando confusión y datos duplicados.

**Solución:** Cada mesa solo puede tener UN formulario por tipo de elección.

**Ejemplos:**
- ✅ Mesa 01 → Senado (permitido)
- ✅ Mesa 01 → Cámara de Representantes (permitido)
- ❌ Mesa 01 → Senado (duplicado - NO permitido)

---

## 🔧 Cambios Implementados

### 1. Restricción Única en el Modelo ✅

**Archivo:** `backend/models/formulario_e14.py`

**Cambio:**
```python
class FormularioE14(db.Model):
    """Formulario E-14 de mesa electoral"""
    __tablename__ = 'formularios_e14'
    
    # Restricción única: una mesa solo puede tener un formulario por tipo de elección
    __table_args__ = (
        db.UniqueConstraint('mesa_id', 'tipo_eleccion_id', name='uq_mesa_tipo_eleccion'),
    )
```

**Beneficio:** La base de datos rechazará automáticamente intentos de crear duplicados.

---

### 2. Validación en el Servicio ✅

**Archivo:** `backend/services/formulario_service.py`

**Cambio:**
```python
# Validar que no exista ya un formulario para esta mesa y tipo de elección
formulario_existente = FormularioE14.query.filter_by(
    mesa_id=data['mesa_id'],
    tipo_eleccion_id=data['tipo_eleccion_id']
).first()

if formulario_existente:
    tipo_eleccion = TipoEleccion.query.get(data['tipo_eleccion_id'])
    tipo_nombre = tipo_eleccion.nombre if tipo_eleccion else 'esta elección'
    raise ValidationException({
        'mesa_tipo_eleccion': [
            f'Ya existe un formulario para esta mesa y {tipo_nombre}. '
            f'Cada mesa solo puede tener un formulario por tipo de elección.'
        ]
    })
```

**Beneficio:** Mensaje claro al usuario antes de intentar guardar en la base de datos.

---

### 3. Script de Migración ✅

**Archivo:** `backend/migrations/add_unique_constraint_mesa_tipo_eleccion.py`

**Funcionalidad:**
- Detecta y elimina duplicados existentes (mantiene el más reciente)
- Agrega la restricción única a la base de datos
- Puede revertirse con `downgrade()`

**Ejecución:**
```bash
# Aplicar migración
python backend/migrations/add_unique_constraint_mesa_tipo_eleccion.py

# Revertir migración (si es necesario)
python backend/migrations/add_unique_constraint_mesa_tipo_eleccion.py downgrade
```

---

## 📊 Mostrar Tipo de Elección en las Interfaces

### Frontend - Lista de Formularios del Testigo

**Archivo:** `frontend/templates/testigo/dashboard.html`

**Actualizar tabla:**
```html
<table class="table table-striped" id="formsTable">
    <thead>
        <tr>
            <th>Mesa</th>
            <th>Tipo Elección</th>  <!-- NUEVO -->
            <th>Estado</th>
            <th>Total Votos</th>
            <th>Fecha</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody>
        <!-- Se llenará con JavaScript -->
    </tbody>
</table>
```

**JavaScript para renderizar:**
```javascript
function renderFormulariosTestigo(formularios) {
    const tbody = document.querySelector('#formsTable tbody');
    
    if (formularios.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center py-4">
                    <p class="text-muted">No hay formularios registrados</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = formularios.map(form => `
        <tr>
            <td>${form.mesa_codigo || 'N/A'}</td>
            <td>
                <span class="badge bg-primary">
                    ${form.tipo_eleccion_nombre || 'N/A'}
                </span>
            </td>
            <td>${getEstadoBadge(form.estado)}</td>
            <td>${form.total_votos || 0}</td>
            <td>${Utils.formatDate(form.created_at)}</td>
            <td>
                <button class="btn btn-sm btn-info" onclick="verFormulario(${form.id})">
                    <i class="bi bi-eye"></i> Ver
                </button>
            </td>
        </tr>
    `).join('');
}
```

---

### Frontend - Lista de Formularios del Coordinador

**Archivo:** `frontend/templates/coordinador/puesto.html`

**Actualizar tabla:**
```html
<table class="table table-hover" id="formulariosTable">
    <thead>
        <tr>
            <th>Mesa</th>
            <th>Testigo</th>
            <th>Tipo Elección</th>  <!-- NUEVO -->
            <th>Estado</th>
            <th>Total Votos</th>
            <th>Fecha</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody>
        <!-- Se llenará con JavaScript -->
    </tbody>
</table>
```

**JavaScript para renderizar:**
```javascript
function renderFormulariosTable(formularios) {
    const tbody = document.querySelector('#formulariosTable tbody');
    
    if (formularios.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center py-4">
                    <p class="text-muted">No hay formularios ${estadoFiltro ? 'en estado ' + estadoFiltro : ''}</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = formularios.map(form => {
        const estadoBadge = getEstadoBadge(form.estado);
        const fecha = Utils.formatDate(form.created_at);
        const puedeValidar = form.estado === 'pendiente';
        
        return `
            <tr style="cursor: ${puedeValidar ? 'pointer' : 'default'};" 
                ${puedeValidar ? `onclick="abrirModalValidacion(${form.id})"` : ''}>
                <td>
                    <strong>${form.mesa_codigo || 'N/A'}</strong><br>
                    <small class="text-muted">${form.mesa_nombre || ''}</small>
                </td>
                <td>${form.testigo_nombre || 'N/A'}</td>
                <td>
                    <span class="badge bg-primary">
                        ${form.tipo_eleccion_nombre || 'N/A'}
                    </span>
                </td>
                <td>${estadoBadge}</td>
                <td><strong>${Utils.formatNumber(form.total_votos)}</strong></td>
                <td><small>${fecha}</small></td>
                <td>
                    ${puedeValidar ? 
                        `<button class="btn btn-sm btn-primary" onclick="event.stopPropagation(); abrirModalValidacion(${form.id})">
                            <i class="bi bi-eye"></i> Revisar
                        </button>` :
                        `<button class="btn btn-sm btn-outline-secondary" onclick="event.stopPropagation(); verDetalles(${form.id})">
                            <i class="bi bi-info-circle"></i> Ver
                        </button>`
                    }
                </td>
            </tr>
        `;
    }).join('');
}
```

---

### Frontend - Cards para Móvil (Coordinador)

**JavaScript para cards:**
```javascript
function renderFormulariosCards(formularios) {
    const container = document.getElementById('formulariosCards');
    
    if (!container) return;
    
    if (formularios.length === 0) {
        container.innerHTML = `
            <div class="text-center py-5">
                <i class="bi bi-inbox" style="font-size: 3rem; color: var(--text-tertiary);"></i>
                <p class="text-muted mt-3">No hay formularios ${estadoFiltro ? 'en estado ' + estadoFiltro : ''}</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = formularios.map(form => {
        const estadoBadge = getEstadoBadgeV2(form.estado);
        const fecha = Utils.formatDate(form.created_at);
        const puedeValidar = form.estado === 'pendiente';
        
        return `
            <div class="formulario-card" onclick="${puedeValidar ? `abrirModalValidacion(${form.id})` : `verDetalles(${form.id})`}">
                <div class="formulario-card-header">
                    <div class="formulario-card-title">
                        <h6><i class="bi bi-table"></i> Mesa ${form.mesa_codigo || 'N/A'}</h6>
                        <p><i class="bi bi-person"></i> ${form.testigo_nombre || 'N/A'}</p>
                        <p>
                            <span class="badge bg-primary">
                                ${form.tipo_eleccion_nombre || 'N/A'}
                            </span>
                        </p>
                    </div>
                    <div class="formulario-card-badge">
                        ${estadoBadge}
                    </div>
                </div>
                <div class="formulario-card-body">
                    <div class="formulario-card-info">
                        <div class="formulario-card-info-item">
                            <label>Total Votos</label>
                            <span>${Utils.formatNumber(form.total_votos)}</span>
                        </div>
                        <div class="formulario-card-info-item">
                            <label>Fecha</label>
                            <span>${fecha}</span>
                        </div>
                    </div>
                    <div>
                        ${puedeValidar ? 
                            `<button class="btn btn-primary btn-sm" onclick="event.stopPropagation(); abrirModalValidacion(${form.id})">
                                <i class="bi bi-eye"></i>
                            </button>` :
                            `<button class="btn btn-outline-secondary btn-sm" onclick="event.stopPropagation(); verDetalles(${form.id})">
                                <i class="bi bi-info-circle"></i>
                            </button>`
                        }
                    </div>
                </div>
            </div>
        `;
    }).join('');
}
```

---

### Frontend - Selector de Tipo de Elección (Testigo)

**Mejorar el selector para mostrar advertencia:**

```javascript
// Al seleccionar tipo de elección, verificar si ya existe
async function onTipoEleccionChange() {
    const mesaId = document.getElementById('mesa_id').value;
    const tipoEleccionId = document.getElementById('tipo_eleccion_id').value;
    
    if (!mesaId || !tipoEleccionId) return;
    
    try {
        // Verificar si ya existe un formulario
        const response = await APIClient.get('/formularios/verificar-existente', {
            mesa_id: mesaId,
            tipo_eleccion_id: tipoEleccionId
        });
        
        if (response.data.existe) {
            // Mostrar advertencia
            const tipoNombre = response.data.tipo_eleccion_nombre;
            Utils.showWarning(
                `Ya existe un formulario para esta mesa y ${tipoNombre}. ` +
                `Cada mesa solo puede tener un formulario por tipo de elección.`
            );
            
            // Deshabilitar botón de guardar
            document.getElementById('btnGuardarFormulario').disabled = true;
        } else {
            // Habilitar botón de guardar
            document.getElementById('btnGuardarFormulario').disabled = false;
        }
    } catch (error) {
        console.error('Error al verificar formulario:', error);
    }
}
```

---

## 🔄 Endpoint de Verificación (Opcional)

**Archivo:** `backend/routes/formularios_e14.py`

**Agregar endpoint:**
```python
@formularios_bp.route('/verificar-existente', methods=['GET'])
@jwt_required()
@role_required(['testigo_electoral'])
def verificar_formulario_existente():
    """
    Verificar si ya existe un formulario para una mesa y tipo de elección
    """
    try:
        mesa_id = request.args.get('mesa_id', type=int)
        tipo_eleccion_id = request.args.get('tipo_eleccion_id', type=int)
        
        if not mesa_id or not tipo_eleccion_id:
            return jsonify({
                'success': False,
                'error': 'Se requieren mesa_id y tipo_eleccion_id'
            }), 400
        
        formulario = FormularioE14.query.filter_by(
            mesa_id=mesa_id,
            tipo_eleccion_id=tipo_eleccion_id
        ).first()
        
        tipo_eleccion = TipoEleccion.query.get(tipo_eleccion_id)
        
        return jsonify({
            'success': True,
            'data': {
                'existe': formulario is not None,
                'tipo_eleccion_nombre': tipo_eleccion.nombre if tipo_eleccion else None,
                'formulario_id': formulario.id if formulario else None,
                'formulario_estado': formulario.estado if formulario else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

---

## 📊 Resumen de Cambios

### Backend:
1. ✅ Restricción única en modelo `FormularioE14`
2. ✅ Validación en `FormularioService.crear_formulario()`
3. ✅ Import de `TipoEleccion` en servicio
4. ✅ Script de migración para base de datos
5. ⏳ Endpoint de verificación (opcional)

### Frontend:
1. ⏳ Agregar columna "Tipo Elección" en tablas
2. ⏳ Mostrar tipo de elección en cards móviles
3. ⏳ Validación en tiempo real al seleccionar tipo
4. ⏳ Mensajes de error claros al usuario

---

## 🧪 Testing

### Casos de Prueba:

1. **Crear primer formulario:**
   - Mesa: 01
   - Tipo: Senado
   - Resultado: ✅ Éxito

2. **Crear segundo formulario (diferente tipo):**
   - Mesa: 01
   - Tipo: Cámara
   - Resultado: ✅ Éxito

3. **Intentar duplicado:**
   - Mesa: 01
   - Tipo: Senado
   - Resultado: ❌ Error con mensaje claro

4. **Verificar en lista:**
   - Debe mostrar ambos formularios
   - Cada uno con su tipo de elección visible

---

## 🚀 Despliegue

### Pasos:

1. **Ejecutar migración:**
```bash
python backend/migrations/add_unique_constraint_mesa_tipo_eleccion.py
```

2. **Commit cambios:**
```bash
git add backend/models/formulario_e14.py
git add backend/services/formulario_service.py
git add backend/migrations/add_unique_constraint_mesa_tipo_eleccion.py
git commit -m "feat: Restricción única mesa + tipo elección en formularios E14"
```

3. **Deploy a producción**

4. **Actualizar frontend** (siguiente fase)

---

## ✅ Beneficios

- ✅ **Integridad de datos** - No más duplicados
- ✅ **Claridad** - Tipo de elección siempre visible
- ✅ **Validación temprana** - Error antes de guardar
- ✅ **Mensajes claros** - Usuario sabe qué pasó
- ✅ **Migración segura** - Elimina duplicados existentes

---

**Estado:** ✅ Backend Implementado - Frontend Pendiente
**Prioridad:** 🟡 MEDIA - Mejora de calidad de datos
**Fecha:** 2025-11-25
