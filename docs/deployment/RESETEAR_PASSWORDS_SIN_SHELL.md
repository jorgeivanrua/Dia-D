# 🚨 Resetear Contraseñas SIN Acceso a Shell (Render Free)

## Problema
No tienes acceso a Shell en Render Free, pero necesitas resetear las contraseñas.

## Solución: Endpoint de Emergencia

He creado endpoints especiales que puedes llamar desde tu navegador o Postman.

---

## 📋 Paso 1: Listar Usuarios Actuales

### Usando el Navegador:

1. Abre tu navegador
2. Ve a la consola de desarrollador (F12)
3. Ve a la pestaña "Console"
4. Pega este código:

```javascript
fetch('https://tu-app.onrender.com/api/emergency/emergency-list-users', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        emergency_key: 'reset_passwords_2024_emergency'
    })
})
.then(r => r.json())
.then(data => console.log(data));
```

### Usando Postman:

```
POST https://tu-app.onrender.com/api/emergency/emergency-list-users

Headers:
Content-Type: application/json

Body (raw JSON):
{
    "emergency_key": "reset_passwords_2024_emergency"
}
```

---

## 🔧 Paso 2: Resetear Contraseñas

### Usando el Navegador:

```javascript
fetch('https://tu-app.onrender.com/api/emergency/emergency-reset-passwords', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        emergency_key: 'reset_passwords_2024_emergency'
    })
})
.then(r => r.json())
.then(data => {
    console.log('✅ Contraseñas reseteadas:');
    console.table(data.usuarios_actualizados);
});
```

### Usando Postman:

```
POST https://tu-app.onrender.com/api/emergency/emergency-reset-passwords

Headers:
Content-Type: application/json

Body (raw JSON):
{
    "emergency_key": "reset_passwords_2024_emergency"
}
```

### Usando cURL:

```bash
curl -X POST https://tu-app.onrender.com/api/emergency/emergency-reset-passwords \
  -H "Content-Type: application/json" \
  -d '{"emergency_key": "reset_passwords_2024_emergency"}'
```

---

## 👥 Paso 3: Crear Usuarios si No Existen

Si los usuarios no existen en la base de datos:

### Usando el Navegador:

```javascript
fetch('https://tu-app.onrender.com/api/emergency/emergency-create-users', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        emergency_key: 'reset_passwords_2024_emergency'
    })
})
.then(r => r.json())
.then(data => {
    console.log('✅ Usuarios creados:');
    console.table(data.usuarios_creados);
});
```

### Usando Postman:

```
POST https://tu-app.onrender.com/api/emergency/emergency-create-users

Headers:
Content-Type: application/json

Body (raw JSON):
{
    "emergency_key": "reset_passwords_2024_emergency"
}
```

---

## 🔐 Contraseñas Después del Reset

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| Super Admin | `admin123` | super_admin |
| Monitoreo | `test123` | monitoreo |
| Coordinador Departamental | `test123` | coordinador_departamental |
| Coordinador Municipal | `test123` | coordinador_municipal |
| Coordinador Puesto | `test123` | coordinador_puesto |
| Auditor Electoral | `test123` | auditor_electoral |

---

## ✅ Verificar que Funcionó

1. **Ir al login**: https://tu-app.onrender.com/auth/login
2. **Probar con Monitoreo**:
   - Usuario: `Monitoreo`
   - Contraseña: `test123`
3. **Si funciona**: ✅ ¡Listo!

---

## 🔒 Seguridad

### Cambiar la Clave de Emergencia

1. **En Render Dashboard**:
   - Ve a tu servicio
   - Environment → Add Environment Variable
   - Nombre: `EMERGENCY_RESET_KEY`
   - Valor: `tu_clave_super_secreta_123`

2. **Usar la nueva clave**:
```javascript
{
    "emergency_key": "tu_clave_super_secreta_123"
}
```

### Desactivar el Endpoint Después

Una vez que hayas reseteado las contraseñas, puedes:

1. **Eliminar el blueprint** de `app.py`
2. **O cambiar la clave** a algo que solo tú sepas
3. **O agregar validación de IP** para que solo funcione desde tu IP

---

## 📱 Ejemplo Completo con Fetch

Copia y pega esto en la consola del navegador (F12):

```javascript
// Reemplaza con tu URL de Render
const API_URL = 'https://tu-app.onrender.com';
const EMERGENCY_KEY = 'reset_passwords_2024_emergency';

async function resetearPasswords() {
    try {
        console.log('🔍 Listando usuarios...');
        
        // 1. Listar usuarios
        const listResponse = await fetch(`${API_URL}/api/emergency/emergency-list-users`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ emergency_key: EMERGENCY_KEY })
        });
        const listData = await listResponse.json();
        console.log('📋 Usuarios actuales:', listData);
        
        // 2. Resetear contraseñas
        console.log('\n🔧 Reseteando contraseñas...');
        const resetResponse = await fetch(`${API_URL}/api/emergency/emergency-reset-passwords`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ emergency_key: EMERGENCY_KEY })
        });
        const resetData = await resetResponse.json();
        
        if (resetData.success) {
            console.log('✅ ¡Contraseñas reseteadas exitosamente!');
            console.table(resetData.usuarios_actualizados);
            console.log('\n🎉 Ahora puedes iniciar sesión con:');
            resetData.usuarios_actualizados.forEach(u => {
                console.log(`   ${u.nombre}: ${u.password}`);
            });
        } else {
            console.error('❌ Error:', resetData.error);
        }
        
    } catch (error) {
        console.error('❌ Error:', error);
    }
}

// Ejecutar
resetearPasswords();
```

---

## 🆘 Troubleshooting

### Error 403: "Clave de emergencia inválida"

- Verificar que estás usando la clave correcta
- Si configuraste `EMERGENCY_RESET_KEY` en Render, usar esa clave

### Error 404: "Not Found"

- Verificar que el código se haya desplegado en Render
- Hacer push y esperar a que Render redeploy
- Verificar la URL: debe ser `/api/emergency/emergency-reset-passwords`

### Error 500: "Internal Server Error"

- Revisar logs en Render Dashboard
- Verificar que la base de datos esté conectada
- Verificar variables de entorno

### Los usuarios no existen

- Usar el endpoint `emergency-create-users` primero
- Luego usar `emergency-reset-passwords`

---

## 📝 Notas Importantes

1. **Este endpoint es temporal**: Úsalo solo para emergencias
2. **Cambia la clave**: Usa una clave secreta en producción
3. **Desactívalo después**: Una vez que funcione, considera eliminarlo
4. **No compartas la clave**: Mantenla privada

---

## 🎯 Resumen Rápido

1. **Hacer push** del código (ya está hecho)
2. **Esperar** a que Render redeploy (2-3 minutos)
3. **Abrir consola** del navegador (F12)
4. **Ejecutar** el script de arriba
5. **Probar login** con las contraseñas reseteadas

---

**Última actualización**: 30 de Noviembre de 2025
