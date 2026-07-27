# Instrucciones de Debug - Usuarios No Visibles

## 🔍 Pasos para Diagnosticar

### 1. Refrescar el Navegador
- Presiona **Ctrl + Shift + R** (Windows) o **Cmd + Shift + R** (Mac)
- Esto forzará la recarga de todos los archivos JavaScript

### 2. Abrir la Consola del Navegador
- Presiona **F12** o **Ctrl + Shift + I**
- Ve a la pestaña "Console"

### 3. Buscar el Output de Debug
Deberías ver dos bloques de debug:

```
=== DEBUG USUARIOS ===
1. Elemento usuarios-lista: ENCONTRADO/NO ENCONTRADO
2. Contenido HTML: ...
3. Número de filas: X
4. allUsers: X usuarios / NO CARGADO
5. Primeros 3 usuarios: ...
6. Intentando forzar re-render...
7. Re-render ejecutado / Función no disponible
8. Estilos del tbody: ...
=== FIN DEBUG ===

=== DEBUG CANDIDATOS ===
...
=== FIN DEBUG ===
```

### 4. Verificar Información Clave

#### ✅ Si todo está bien:
- Elemento usuarios-lista: **ENCONTRADO**
- allUsers: **376 usuarios** (o el número correcto)
- Número de filas: **> 0**
- Re-render ejecutado: **Sí**
- Estilos background: **rgb(255, 255, 255)** (blanco)
- Estilos color: **rgb(33, 37, 41)** (negro)

#### ❌ Si hay problemas:

**Problema 1: Elemento NO ENCONTRADO**
- El HTML no se cargó correctamente
- Verificar que estás en la pestaña correcta del dashboard

**Problema 2: allUsers NO CARGADO o 0 usuarios**
- El endpoint no está respondiendo
- Verificar en la pestaña "Network" si hay errores 401, 500, etc.
- Verificar que el servidor esté corriendo

**Problema 3: Número de filas = 0 o 1**
- Los datos no se están renderizando
- Verificar si hay errores de JavaScript en consola

**Problema 4: Estilos incorrectos**
- Los estilos CSS están siendo sobrescritos
- Verificar que los estilos inline tengan `!important`

### 5. Información a Reportar

Si los usuarios no se ven, copia y pega en tu respuesta:

1. **Output completo de "=== DEBUG USUARIOS ==="**
2. **Errores en consola** (si los hay, en rojo)
3. **Pestaña en la que estás** (Usuarios, Partidos, Candidatos, etc.)
4. **Respuesta del endpoint** (pestaña Network > /api/super-admin/users)

## 🔧 Soluciones Rápidas

### Solución 1: Forzar Re-render desde Consola
```javascript
// Copiar y pegar en la consola del navegador
if (window.allUsers && window.renderUsers) {
    window.renderUsers(window.allUsers);
    console.log('Re-render forzado');
}
```

### Solución 2: Recargar Usuarios
```javascript
// Copiar y pegar en la consola del navegador
if (typeof loadUsers === 'function') {
    loadUsers();
    console.log('Recargando usuarios...');
}
```

### Solución 3: Verificar Datos
```javascript
// Copiar y pegar en la consola del navegador
console.log('allUsers:', window.allUsers);
console.log('Elemento:', document.getElementById('usuarios-lista'));
```

## 📊 Estado Esperado

- **Servidor**: Corriendo en puerto 5000
- **Usuarios en BD**: 376
- **Endpoint**: `/api/super-admin/users` debe devolver 200 OK
- **Elemento HTML**: `usuarios-lista` debe existir
- **JavaScript**: `allUsers` debe tener 376 elementos
- **Renderizado**: Tabla debe tener 376 filas

## 🚨 Si Nada Funciona

1. Verificar que el servidor esté corriendo (proceso 11)
2. Verificar que puedas hacer login
3. Verificar que seas super_admin
4. Intentar con otro navegador
5. Limpiar caché del navegador completamente
