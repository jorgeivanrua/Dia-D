# 🔧 Plan de Corrección - Dashboard Super Admin

## 📋 Problemas Identificados

### 1. Tab Usuarios
- ❌ Botón "Editar" no funciona
- ✅ Botón "Resetear Contraseña" funciona
- ✅ Botón "Activar/Desactivar" funciona

### 2. Tab Configuración - Candidatos
- ❌ Botón "Habilitar/Deshabilitar" existe pero necesita verificación
- ❌ Botón "Editar" no funciona completamente

### 3. Tab Configuración - Partidos
- ❌ Falta botón "Habilitar/Deshabilitar"
- ❌ Botón "Editar" necesita verificación

### 4. Tab Configuración - Tipos de Elección
- ❌ Falta botón "Habilitar/Deshabilitar"
- ❌ Botón "Editar" necesita verificación

### 5. Filtrado por Estado Activo
- ❌ Testigos ven TODOS los tipos de elección (deben ver solo activos)
- ❌ Testigos ven TODOS los candidatos (deben ver solo activos)
- ❌ Testigos ven TODOS los partidos (deben ver solo activos)

---

## 🎯 Soluciones a Implementar

### Fase 1: Corregir Funcionalidad de Edición

#### 1.1 Usuarios - Implementar Modal de Edición
```javascript
async function editUser(userId) {
    // Cargar datos del usuario
    // Mostrar modal con formulario
    // Permitir editar: nombre, rol, ubicación
    // Guardar cambios
}
```

#### 1.2 Candidatos - Completar Modal de Edición
```javascript
async function editCandidato(candidatoId) {
    // Cargar datos del candidato
    // Mostrar modal con formulario
    // Permitir editar: nombre, partido, tipo elección, número lista
    // Guardar cambios
}
```

#### 1.3 Partidos - Implementar Modal de Edición
```javascript
async function editPartido(partidoId) {
    // Cargar datos del partido
    // Mostrar modal con formulario
    // Permitir editar: nombre, sigla, color
    // Guardar cambios
}
```

#### 1.4 Tipos de Elección - Implementar Modal de Edición
```javascript
async function editTipoEleccion(tipoId) {
    // Cargar datos del tipo
    // Mostrar modal con formulario
    // Permitir editar: nombre, descripción
    // Guardar cambios
}
```

### Fase 2: Implementar Toggle de Estado

#### 2.1 Partidos - Agregar Toggle
```javascript
async function togglePartido(partidoId, activo) {
    // Llamar API para cambiar estado
    // Actualizar UI
    // Mostrar confirmación
}
```

**HTML:**
```html
<button class="btn btn-sm btn-${partido.activo ? 'warning' : 'success'}" 
        onclick="togglePartido(${partido.id}, ${!partido.activo})">
    <i class="bi bi-toggle-${partido.activo ? 'on' : 'off'}"></i>
</button>
```

#### 2.2 Tipos de Elección - Agregar Toggle
```javascript
async function toggleTipoEleccion(tipoId, activo) {
    // Llamar API para cambiar estado
    // Actualizar UI
    // Mostrar confirmación
}
```

**HTML:**
```html
<button class="btn btn-sm btn-${tipo.activo ? 'warning' : 'success'}" 
        onclick="toggleTipoEleccion(${tipo.id}, ${!tipo.activo})">
    <i class="bi bi-toggle-${tipo.activo ? 'on' : 'off'}"></i>
</button>
```

### Fase 3: Filtrar por Estado Activo en Formularios

#### 3.1 Backend - Modificar Endpoints
```python
# routes/testigo.py o routes/api.py

@bp.route('/api/tipos-eleccion', methods=['GET'])
def get_tipos_eleccion():
    # Agregar filtro: .filter_by(activo=True)
    tipos = TipoEleccion.query.filter_by(activo=True).all()
    return jsonify([tipo.to_dict() for tipo in tipos])

@bp.route('/api/candidatos', methods=['GET'])
def get_candidatos():
    # Agregar filtro: .filter_by(activo=True)
    candidatos = Candidato.query.filter_by(activo=True).all()
    return jsonify([candidato.to_dict() for candidato in candidatos])

@bp.route('/api/partidos', methods=['GET'])
def get_partidos():
    # Agregar filtro: .filter_by(activo=True)
    partidos = Partido.query.filter_by(activo=True).all()
    return jsonify([partido.to_dict() for partido in partidos])
```

#### 3.2 Frontend - Verificar Carga
```javascript
// En testigo-dashboard.js
async function cargarTiposEleccion() {
    // Ya debe filtrar automáticamente por activo=True desde backend
    const response = await fetch('/api/tipos-eleccion');
    const tipos = await response.json();
    // Renderizar solo tipos activos
}
```

---

## 📝 Archivos a Modificar

### Frontend:
1. ✅ `frontend/static/js/super-admin-dashboard.js`
   - Implementar `editUser()`
   - Implementar `editCandidato()`
   - Implementar `editPartido()`
   - Implementar `editTipoEleccion()`
   - Implementar `togglePartido()`
   - Implementar `toggleTipoEleccion()`

2. ✅ `frontend/templates/admin/super-admin-dashboard.html`
   - Agregar botones toggle a partidos
   - Agregar botones toggle a tipos de elección
   - Agregar modales de edición

### Backend:
3. ✅ `backend/routes/api.py` o `backend/routes/testigo.py`
   - Modificar endpoint `/api/tipos-eleccion` para filtrar activos
   - Modificar endpoint `/api/candidatos` para filtrar activos
   - Modificar endpoint `/api/partidos` para filtrar activos

4. ✅ `backend/routes/super_admin.py`
   - Agregar endpoint `PUT /super-admin/partidos/<id>/toggle`
   - Agregar endpoint `PUT /super-admin/tipos-eleccion/<id>/toggle`
   - Agregar endpoint `PUT /super-admin/partidos/<id>`
   - Agregar endpoint `PUT /super-admin/tipos-eleccion/<id>`

---

## 🎯 Resultado Esperado

### Dashboard Super Admin:
- ✅ Todos los botones de editar funcionan
- ✅ Todos los botones de habilitar/deshabilitar funcionan
- ✅ Modales de edición completos y funcionales
- ✅ Feedback visual claro de estados

### Formularios de Testigos:
- ✅ Solo ven tipos de elección activos
- ✅ Solo ven candidatos activos
- ✅ Solo ven partidos activos
- ✅ Experiencia limpia sin opciones deshabilitadas

---

## 🚀 Orden de Implementación

1. **Backend primero** - Agregar endpoints y filtros
2. **Frontend después** - Implementar funciones y modales
3. **Testing** - Verificar funcionalidad completa
4. **Commit y Push** - Subir cambios

---

**Fecha:** 2025-11-26  
**Estado:** 📝 Planificado  
**Próximo Paso:** Implementar correcciones

