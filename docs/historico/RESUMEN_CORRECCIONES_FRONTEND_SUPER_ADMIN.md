# 📝 Resumen de Correcciones Frontend - Super Admin

## 🎯 Objetivo
Implementar funcionalidad completa de edición y toggle para todos los elementos del dashboard super admin.

---

## ✅ Estado Actual

### Funciones que YA funcionan:
- ✅ `toggleUserStatus()` - Activar/desactivar usuarios
- ✅ `resetUserPassword()` - Resetear contraseña
- ✅ `toggleCandidato()` - Habilitar/deshabilitar candidatos

### Funciones que NO funcionan o están incompletas:
- ❌ `editUser()` - Solo muestra mensaje "en desarrollo"
- ❌ `editCandidato()` - Implementación duplicada/incompleta
- ❌ `editPartido()` - No existe o incompleta
- ❌ `editTipoEleccion()` - No existe
- ❌ `togglePartido()` - No existe en JavaScript
- ❌ `toggleTipoEleccion()` - No existe en JavaScript

---

## 🔧 Correcciones a Implementar

### 1. Implementar `editUser(userId)`
```javascript
async function editUser(userId) {
    // 1. Buscar usuario
    // 2. Crear modal con formulario
    // 3. Cargar datos actuales
    // 4. Permitir editar: nombre, rol, ubicación
    // 5. Guardar cambios via API
    // 6. Actualizar tabla
}
```

**Modal HTML necesario:**
```html
<div class="modal" id="editUserModal">
    <form id="editUserForm">
        <input name="nombre" required>
        <select name="rol" required>
        <select name="departamento">
        <select name="municipio">
        <select name="zona">
        <select name="puesto">
    </form>
</div>
```

### 2. Implementar `editCandidato(candidatoId)`
```javascript
async function editCandidato(candidatoId) {
    // 1. Buscar candidato
    // 2. Crear modal con formulario
    // 3. Cargar datos actuales
    // 4. Permitir editar: nombre, partido, tipo elección, número lista
    // 5. Guardar cambios via API
    // 6. Actualizar tabla
}
```

### 3. Implementar `editPartido(partidoId)`
```javascript
async function editPartido(partidoId) {
    // 1. Buscar partido
    // 2. Crear modal con formulario
    // 3. Cargar datos actuales
    // 4. Permitir editar: nombre, sigla, color
    // 5. Guardar cambios via API
    // 6. Actualizar lista
}
```

### 4. Implementar `editTipoEleccion(tipoId)`
```javascript
async function editTipoEleccion(tipoId) {
    // 1. Buscar tipo
    // 2. Crear modal con formulario
    // 3. Cargar datos actuales
    // 4. Permitir editar: nombre, descripción
    // 5. Guardar cambios via API
    // 6. Actualizar lista
}
```

### 5. Implementar `togglePartido(partidoId, activo)`
```javascript
async function togglePartido(partidoId, activo) {
    // 1. Confirmar acción
    // 2. Llamar API PUT /super-admin/partidos/{id}/toggle
    // 3. Actualizar UI
    // 4. Mostrar mensaje de éxito
}
```

### 6. Implementar `toggleTipoEleccion(tipoId, activo)`
```javascript
async function toggleTipoEleccion(tipoId, activo) {
    // 1. Confirmar acción
    // 2. Llamar API PUT /super-admin/tipos-eleccion/{id}/toggle
    // 3. Actualizar UI
    // 4. Mostrar mensaje de éxito
}
```

---

## 📄 Cambios en HTML

### Partidos - Agregar botones toggle
**Ubicación:** Función `loadPartidos()` en super-admin-dashboard.js

**Cambio:**
```javascript
// ANTES:
html += `
    <div class="d-flex justify-content-between align-items-center mb-2">
        <span>${partido.nombre}</span>
        <button onclick="editPartido(${partido.id})">Editar</button>
    </div>
`;

// DESPUÉS:
html += `
    <div class="d-flex justify-content-between align-items-center mb-2">
        <span>${partido.nombre}</span>
        <span class="badge bg-${partido.activo ? 'success' : 'secondary'}">
            ${partido.activo ? 'Activo' : 'Inactivo'}
        </span>
        <div class="btn-group btn-group-sm">
            <button class="btn btn-${partido.activo ? 'warning' : 'success'}" 
                    onclick="togglePartido(${partido.id}, ${!partido.activo})"
                    title="${partido.activo ? 'Desactivar' : 'Activar'}">
                <i class="bi bi-toggle-${partido.activo ? 'on' : 'off'}"></i>
            </button>
            <button class="btn btn-outline-primary" 
                    onclick="editPartido(${partido.id})"
                    title="Editar">
                <i class="bi bi-pencil"></i>
            </button>
        </div>
    </div>
`;
```

### Tipos de Elección - Agregar botones toggle
**Ubicación:** Función `loadElectionTypes()` en super-admin-dashboard.js

**Cambio similar al de partidos**

---

## 📊 Estimación de Trabajo

| Tarea | Complejidad | Tiempo Est. |
|-------|-------------|-------------|
| editUser() | Media | 15 min |
| editCandidato() | Media | 15 min |
| editPartido() | Baja | 10 min |
| editTipoEleccion() | Baja | 10 min |
| togglePartido() | Baja | 5 min |
| toggleTipoEleccion() | Baja | 5 min |
| Actualizar HTML | Media | 10 min |
| Testing | - | 10 min |
| **TOTAL** | - | **~80 min** |

---

## 🚀 Plan de Implementación

### Opción A: Todo de una vez
- Implementar todas las funciones
- Actualizar todo el HTML
- Hacer un solo commit grande
- **Ventaja:** Completar todo rápido
- **Desventaja:** Commit grande, difícil de revisar

### Opción B: Por partes
1. **Parte 1:** Funciones toggle (togglePartido, toggleTipoEleccion)
2. **Parte 2:** Funciones edit simples (editPartido, editTipoEleccion)
3. **Parte 3:** Funciones edit complejas (editUser, editCandidato)
4. **Parte 4:** Actualizar HTML y testing
- **Ventaja:** Commits pequeños, fácil de revisar
- **Desventaja:** Más tiempo total

---

## 💡 Recomendación

Dado que:
- Las funciones son similares entre sí
- El backend ya está listo
- Son cambios independientes

**Recomiendo: Opción A - Todo de una vez**

Esto nos permite:
- Completar la funcionalidad completa
- Hacer un solo commit coherente
- Probar todo junto
- Tener el dashboard 100% funcional

---

**Fecha:** 2025-11-26  
**Estado:** 📝 Planificado  
**Decisión:** Pendiente del usuario

