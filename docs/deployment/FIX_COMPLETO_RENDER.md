# 🚨 FIX COMPLETO - Desbloquear y Resetear Contraseñas

## Problema
Los usuarios están bloqueados por intentos fallidos y las contraseñas no coinciden.

## Solución en 3 Pasos

### Paso 1: Desbloquear Usuarios

Abre la consola del navegador (F12) y ejecuta:

```javascript
fetch('https://tu-app.onrender.com/api/emergency/emergency-unlock-users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        emergency_key: 'reset_passwords_2024_emergency'
    })
})
.then(r => r.json())
.then(data => {
    console.log('✅ Paso 1: Usuarios desbloqueados');
    console.log(data);
});
```

### Paso 2: Resetear Contraseñas

```javascript
fetch('https://tu-app.onrender.com/api/emergency/emergency-reset-passwords', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        emergency_key: 'reset_passwords_2024_emergency'
    })
})
.then(r => r.json())
.then(data => {
    console.log('✅ Paso 2: Contraseñas reseteadas');
    console.table(data.usuarios_actualizados);
});
```

### Paso 3: Verificar Usuarios

```javascript
fetch('https://tu-app.onrender.com/api/emergency/emergency-list-users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        emergency_key: 'reset_passwords_2024_emergency'
    })
})
.then(r => r.json())
.then(data => {
    console.log('✅ Paso 3: Verificación');
    console.table(data.usuarios);
});
```

---

## 🎯 Script Completo (TODO EN UNO)

Copia y pega esto en la consola del navegador (F12):

```javascript
// Reemplaza con tu URL de Render
const API_URL = 'https://tu-app.onrender.com';
const EMERGENCY_KEY = 'reset_passwords_2024_emergency';

async function fixCompleto() {
    console.log('🚀 Iniciando fix completo...\n');
    
    try {
        // Paso 1: Desbloquear usuarios
        console.log('📝 Paso 1: Desbloqueando usuarios...');
        const unlockResponse = await fetch(`${API_URL}/api/emergency/emergency-unlock-users`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ emergency_key: EMERGENCY_KEY })
        });
        const unlockData = await unlockResponse.json();
        
        if (unlockData.success) {
            console.log(`✅ ${unlockData.total} usuarios desbloqueados`);
        } else {
            console.error('❌ Error desbloqueando:', unlockData.error);
        }
        
        // Esperar 1 segundo
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Paso 2: Resetear contraseñas
        console.log('\n📝 Paso 2: Reseteando contraseñas...');
        const resetResponse = await fetch(`${API_URL}/api/emergency/emergency-reset-passwords`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ emergency_key: EMERGENCY_KEY })
        });
        const resetData = await resetResponse.json();
        
        if (resetData.success) {
            console.log(`✅ ${resetData.total_actualizados} contraseñas reseteadas`);
            console.table(resetData.usuarios_actualizados);
        } else {
            console.error('❌ Error reseteando:', resetData.error);
        }
        
        // Esperar 1 segundo
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Paso 3: Verificar usuarios
        console.log('\n📝 Paso 3: Verificando usuarios...');
        const listResponse = await fetch(`${API_URL}/api/emergency/emergency-list-users`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ emergency_key: EMERGENCY_KEY })
        });
        const listData = await listResponse.json();
        
        if (listData.success) {
            console.log(`✅ Total usuarios: ${listData.total_usuarios}`);
            console.table(listData.usuarios);
        }
        
        // Resumen final
        console.log('\n' + '='.repeat(60));
        console.log('🎉 FIX COMPLETO - RESUMEN');
        console.log('='.repeat(60));
        console.log('\n📋 Contraseñas actuales:');
        console.log('   Super Admin → admin123');
        console.log('   Monitoreo → test123');
        console.log('   Coordinador Departamental → test123');
        console.log('   Coordinador Municipal → test123');
        console.log('   Coordinador Puesto → test123');
        console.log('   Auditor Electoral → test123');
        console.log('\n✅ Ahora puedes iniciar sesión!');
        console.log('='.repeat(60));
        
    } catch (error) {
        console.error('❌ Error:', error);
    }
}

// Ejecutar
fixCompleto();
```

---

## 🔐 Contraseñas Después del Fix

| Usuario | Contraseña |
|---------|-----------|
| Super Admin | `admin123` |
| Monitoreo | `test123` |
| Coordinador Departamental | `test123` |
| Coordinador Municipal | `test123` |
| Coordinador Puesto | `test123` |
| Auditor Electoral | `test123` |

---

## ✅ Probar Login

Después de ejecutar el script:

1. **Ir al login**: https://tu-app.onrender.com/auth/login
2. **Probar con Super Admin**:
   - Rol: `Super Administrador`
   - Contraseña: `admin123`
3. **O probar con Monitoreo**:
   - Rol: `Monitoreo`
   - Contraseña: `test123`

---

## 🆘 Si Aún No Funciona

### Opción A: Crear usuarios si no existen

```javascript
fetch('https://tu-app.onrender.com/api/emergency/emergency-create-users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        emergency_key: 'reset_passwords_2024_emergency'
    })
})
.then(r => r.json())
.then(data => {
    console.log('✅ Usuarios creados');
    console.log(data);
});
```

### Opción B: Verificar logs en Render

1. Ve a Render Dashboard
2. Selecciona tu servicio
3. Click en "Logs"
4. Busca errores relacionados con autenticación

### Opción C: Verificar variables de entorno

Asegúrate de que estas variables estén configuradas en Render:
- `DATABASE_URL`
- `SECRET_KEY`
- `JWT_SECRET_KEY`

---

## 📱 Usando Postman

Si prefieres usar Postman:

### 1. Desbloquear
```
POST https://tu-app.onrender.com/api/emergency/emergency-unlock-users
Content-Type: application/json

{
    "emergency_key": "reset_passwords_2024_emergency"
}
```

### 2. Resetear
```
POST https://tu-app.onrender.com/api/emergency/emergency-reset-passwords
Content-Type: application/json

{
    "emergency_key": "reset_passwords_2024_emergency"
}
```

### 3. Verificar
```
POST https://tu-app.onrender.com/api/emergency/emergency-list-users
Content-Type: application/json

{
    "emergency_key": "reset_passwords_2024_emergency"
}
```

---

## 🔒 Después de Arreglar

1. **Cambiar la clave de emergencia** en Render:
   - Environment → `EMERGENCY_RESET_KEY` → `tu_clave_super_secreta`

2. **Considerar eliminar** el endpoint de emergencia después de usarlo

3. **Cambiar contraseñas** a unas más seguras en producción

---

**Última actualización**: 30 de Noviembre de 2025
