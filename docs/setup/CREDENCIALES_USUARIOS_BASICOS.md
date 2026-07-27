# 🔐 Credenciales de Usuarios Básicos del Sistema

## ⚠️ CONTRASEÑAS SIMPLIFICADAS

**Contraseñas fijas para facilitar el acceso:**

- Super Admin: `admin123`
- Todos los demás usuarios básicos: `test123`

---

## Usuarios Básicos del Sistema

### 1. Super Admin
```
Nombre de usuario: Super Admin
Rol: super_admin
Contraseña: admin123
URL: /admin/super-admin-dashboard
```
**Permisos**: Acceso completo al sistema, único que puede cambiar contraseñas

---

### 2. Monitoreo
```
Nombre de usuario: Monitoreo
Rol: monitoreo
Contraseña: test123
URL: /monitoreo/dashboard
```
**Permisos**: Visualización en tiempo real, solo lectura

---

### 3. Coordinador Departamental
```
Nombre de usuario: Coordinador Departamental
Rol: coordinador_departamental
Contraseña: test123
URL: /coordinador/departamental
```
**Permisos**: Gestión a nivel departamental

---

### 4. Coordinador Municipal
```
Nombre de usuario: Coordinador Municipal
Rol: coordinador_municipal
Contraseña: test123
URL: /coordinador/municipal
```
**Permisos**: Gestión a nivel municipal

---

### 5. Coordinador Puesto
```
Nombre de usuario: Coordinador Puesto
Rol: coordinador_puesto
Contraseña: test123
URL: /coordinador/puesto
```
**Permisos**: Gestión de puesto de votación

---

### 6. Auditor Electoral
```
Nombre de usuario: Auditor Electoral
Rol: auditor_electoral
Contraseña: test123
URL: /auditor/dashboard
```
**Permisos**: Auditoría y revisión

---

## Tabla Resumen

| Usuario | Contraseña | Rol | Dashboard |
|---------|-----------|-----|-----------|
| Super Admin | `admin123` | super_admin | /admin/super-admin-dashboard |
| Monitoreo | `test123` | monitoreo | /monitoreo/dashboard |
| Coordinador Departamental | `test123` | coordinador_departamental | /coordinador/departamental |
| Coordinador Municipal | `test123` | coordinador_municipal | /coordinador/municipal |
| Coordinador Puesto | `test123` | coordinador_puesto | /coordinador/puesto |
| Auditor Electoral | `test123` | auditor_electoral | /auditor/dashboard |

---

## Cómo Iniciar Sesión

1. Ir a: `https://tu-dominio.com/auth/login`
2. Ingresar el nombre de usuario (exactamente como aparece arriba)
3. Ingresar la contraseña:
   - Super Admin: `admin123`
   - Otros usuarios: `test123`
4. Hacer clic en "Iniciar Sesión"

---

## Política de Contraseñas

### ✅ Características

1. **Contraseñas fijas**: No pueden ser cambiadas por los usuarios
2. **Solo Super Admin**: Puede cambiar contraseñas de otros usuarios
3. **Simplicidad**: Fácil de recordar y compartir
4. **Control centralizado**: Gestión desde un solo punto

### 🔒 Restricciones

- Los usuarios básicos **NO pueden cambiar** su propia contraseña
- Solo el **Super Admin** tiene permisos para cambiar contraseñas
- Las contraseñas están **documentadas y fijas**

---

## Cambiar Contraseñas (Solo Super Admin)

### Desde el Dashboard

1. Iniciar sesión como Super Admin
2. Ir a "Gestión de Usuarios"
3. Seleccionar usuario
4. Cambiar contraseña

### Usando API

```javascript
// Cambiar contraseña de un usuario
POST /api/super-admin/cambiar-password-usuario
{
    "user_id": 5,
    "new_password": "nueva_contraseña"
}
```

### Resetear todas las contraseñas

```javascript
// Volver a contraseñas por defecto
POST /api/super-admin/resetear-passwords-basicos
```

---

## Endpoints de Emergencia

Si no tienes acceso a Shell en Render:

```javascript
// Resetear contraseñas desde el navegador
fetch('https://tu-app.onrender.com/api/emergency/emergency-reset-passwords', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        emergency_key: 'reset_passwords_2024_emergency'
    })
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## Seguridad

### Recomendaciones

1. **Cambiar en producción**: Usar contraseñas más seguras
2. **Proteger documentación**: No compartir públicamente
3. **Monitorear accesos**: Revisar logs regularmente
4. **Rotar contraseñas**: Cambiar periódicamente

### Contraseñas Seguras Sugeridas

Para producción, considera:

```
Super Admin: Adm1n$Elect2024!Secure#
Usuarios Básicos: T3st$2024!Secure#Basic
```

---

## Troubleshooting

### No puedo iniciar sesión

1. Verificar que usas el nombre exacto: `Monitoreo` (con mayúscula)
2. Verificar contraseña: `test123` (todo minúsculas)
3. Verificar que el usuario está activo
4. Contactar al Super Admin

### Usuario bloqueado

Después de 5 intentos fallidos, el usuario se bloquea por 30 minutos.

**Solución**: Esperar 30 minutos o contactar al Super Admin para desbloquear.

### Olvidé mi contraseña

**Solución**: Las contraseñas están documentadas aquí. Si eres usuario básico, usa `test123`.

---

## Scripts Útiles

### Crear usuarios básicos

```bash
python scripts/crear_usuarios_basicos.py
```

### Resetear contraseñas

```bash
python scripts/resetear_passwords_render.py
```

### Verificar usuarios

```python
from backend.app import create_app
from backend.models.user import User

app = create_app()
with app.app_context():
    usuarios = User.query.all()
    for u in usuarios:
        print(f"{u.nombre} | {u.rol} | Activo: {u.activo}")
```

---

## Notas Importantes

1. **Contraseñas fijas**: Facilitan el acceso y la gestión
2. **Super Admin**: Único con permisos para cambiar contraseñas
3. **Documentación**: Mantener este archivo actualizado
4. **Seguridad**: Cambiar contraseñas en producción

---

**Última actualización**: 30 de Noviembre de 2025

**RECORDATORIO**: 
- Super Admin: `admin123`
- Usuarios básicos: `test123`
