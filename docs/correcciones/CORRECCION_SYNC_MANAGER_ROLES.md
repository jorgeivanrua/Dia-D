# Corrección - SyncManager por Roles

## Fecha: 2025-12-06

## 🐛 Problema

El `SyncManager` se estaba inicializando en todos los dashboards, incluyendo roles que no crean formularios offline (como coordinador municipal, monitoreo, auditor, etc.). Esto causaba:

- ❌ Error 403 al intentar sincronizar reportes inexistentes
- ❌ Logs de error innecesarios en consola
- ❌ Intentos de sincronización fallidos cada 30 segundos
- ❌ Consumo de recursos innecesario

**Error en consola:**
```
POST http://localhost:5000/api/formularios 403 (FORBIDDEN)
Error sincronizando reporte: Error: No tiene permisos para acceder a este recurso
```

## ✅ Solución

Modificado `SyncManager` para que solo se active en roles que realmente necesitan sincronización offline.

### Cambios Implementados

**Archivo:** `frontend/static/js/sync-manager-offline.js`

#### 1. Validación de Roles en `init()`

```javascript
init() {
    // Verificar si el rol actual necesita sincronización
    const rolesConSincronizacion = ['testigo', 'coordinador_puesto'];
    const currentUserRol = this.getCurrentUserRole();
    
    if (!rolesConSincronizacion.includes(currentUserRol)) {
        console.log(`SyncManager: Sincronización deshabilitada para rol ${currentUserRol}`);
        return;
    }
    
    // ... resto del código de inicialización
}
```

#### 2. Nueva Función `getCurrentUserRole()`

```javascript
/**
 * Obtener rol del usuario actual desde el token
 */
getCurrentUserRole() {
    try {
        const token = localStorage.getItem('token');
        if (!token) return null;
        
        // Decodificar JWT (simple, sin validación)
        const payload = JSON.parse(atob(token.split('.')[1]));
        return payload.rol || null;
    } catch (error) {
        console.error('Error obteniendo rol del usuario:', error);
        return null;
    }
}
```

## 📊 Roles y Sincronización

### Roles CON Sincronización ✅
Estos roles crean formularios offline que necesitan sincronizarse:

1. **testigo** - Crea formularios E-14, incidentes y delitos
2. **coordinador_puesto** - Puede crear reportes y gestionar formularios

### Roles SIN Sincronización ❌
Estos roles solo consultan datos, no crean formularios offline:

1. **coordinador_municipal** - Solo consulta y supervisa
2. **coordinador_departamental** - Solo consulta y supervisa
3. **monitoreo** - Solo consulta en tiempo real
4. **auditor_electoral** - Solo consulta y audita
5. **super_admin** - Gestiona configuración, no crea formularios

## 🎯 Comportamiento Actual

### Para Testigos y Coordinadores de Puesto
```
SyncManager inicializado
Sincronizando reportes pendientes...
✅ Sincronización completada
```

### Para Coordinador Municipal y Otros Roles
```
SyncManager: Sincronización deshabilitada para rol coordinador_municipal
```

**Sin errores 403, sin intentos de sincronización innecesarios.**

## 🧪 Cómo Verificar

### 1. Dashboard Coordinador Municipal
1. Abrir `http://localhost:5000/coordinador/municipal`
2. Abrir consola del navegador (F12)
3. Verificar mensaje: `SyncManager: Sincronización deshabilitada para rol coordinador_municipal`
4. ✅ No debe haber errores 403
5. ✅ No debe haber intentos de sincronización

### 2. Dashboard Testigo
1. Abrir dashboard de testigo
2. Abrir consola del navegador
3. Verificar mensaje: `SyncManager inicializado`
4. ✅ Debe intentar sincronizar reportes pendientes
5. ✅ Funcionalidad offline debe funcionar

### 3. Dashboard Monitoreo
1. Abrir `http://localhost:5000/monitoreo/dashboard`
2. Abrir consola del navegador
3. Verificar mensaje: `SyncManager: Sincronización deshabilitada para rol monitoreo`
4. ✅ No debe haber errores 403

## 📝 Ventajas de Esta Solución

1. ✅ **Elimina errores innecesarios** - No más 403 en roles que no crean formularios
2. ✅ **Mejora el rendimiento** - No se ejecutan sincronizaciones innecesarias
3. ✅ **Logs más limpios** - Solo mensajes relevantes en consola
4. ✅ **Código más eficiente** - Recursos solo donde se necesitan
5. ✅ **Fácil de mantener** - Lista de roles centralizada y clara

## 🔧 Agregar Nuevos Roles

Si en el futuro se necesita agregar un rol que cree formularios offline:

```javascript
const rolesConSincronizacion = [
    'testigo', 
    'coordinador_puesto',
    'nuevo_rol_aqui'  // Agregar aquí
];
```

## ⚠️ Consideraciones

### ¿Por qué no eliminar completamente SyncManager?

El `SyncManager` es necesario para:
- Testigos que crean formularios E-14 offline
- Coordinadores de puesto que gestionan reportes
- Funcionalidad offline en general

**No se puede eliminar**, solo se desactiva selectivamente por rol.

### ¿Qué pasa si un rol necesita sincronización en el futuro?

Simplemente agregar el rol a la lista `rolesConSincronizacion` y el SyncManager se activará automáticamente para ese rol.

## 📊 Impacto

### Antes de la Corrección
- ❌ Errores 403 en todos los dashboards de supervisión
- ❌ Logs de error cada 30 segundos
- ❌ Intentos de sincronización fallidos
- ❌ Consumo de recursos innecesario

### Después de la Corrección
- ✅ Sin errores 403 en dashboards de supervisión
- ✅ Logs limpios y relevantes
- ✅ Sincronización solo donde se necesita
- ✅ Mejor rendimiento general

## ✅ Checklist de Verificación

- [x] SyncManager deshabilitado para coordinador_municipal
- [x] SyncManager deshabilitado para monitoreo
- [x] SyncManager deshabilitado para auditor_electoral
- [x] SyncManager deshabilitado para super_admin
- [x] SyncManager activo para testigo
- [x] SyncManager activo para coordinador_puesto
- [x] Sin errores 403 en dashboards de supervisión
- [x] Funcionalidad offline funciona en testigos
- [x] Sin errores de diagnóstico en JavaScript

## 🎉 Conclusión

El `SyncManager` ahora es inteligente y solo se activa en roles que realmente necesitan sincronización offline. Esto elimina errores innecesarios y mejora el rendimiento general del sistema.

**Estado:** ✅ CORREGIDO Y PROBADO
