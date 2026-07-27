# Contraseñas Fijas para Usuarios Básicos

## Política de Contraseñas

Los usuarios básicos del sistema tienen **contraseñas fijas** que solo pueden ser cambiadas por el **Super Admin**.

## Usuarios Básicos y sus Contraseñas Fijas

### 🔐 Credenciales Permanentes

| Usuario | Contraseña | Rol | Puede Cambiar |
|---------|-----------|-----|---------------|
| Super Admin | `admin123` | super_admin | ✅ Sí (solo su propia) |
| Monitoreo | `test123` | monitoreo | ❌ No |
| Coordinador Departamental | `test123` | coordinador_departamental | ❌ No |
| Coordinador Municipal | `test123` | coordinador_municipal | ❌ No |
| Coordinador Puesto | `test123` | coordinador_puesto | ❌ No |
| Auditor Electoral | `test123` | auditor_electoral | ❌ No |

## Restricciones Implementadas

### 1. Usuarios Básicos NO pueden cambiar su contraseña

Si un usuario básico (excepto super admin) intenta cambiar su contraseña, recibirá el error:

```json
{
  "success": false,
  "error": "Los usuarios básicos no pueden cambiar su contraseña. Solo el super admin puede hacerlo."
}
```

### 2. Solo Super Admin puede cambiar contraseñas

El Super Admin tiene endpoints especiales para gestionar contraseñas:

- `POST /api/super-admin/cambiar-password-usuario` - Cambiar contraseña de cualquier usuario
- `POST /api/super-admin/resetear-passwords-basicos` - Resetear todas las contraseñas a valores por defecto
- `GET /api/super-admin/usuarios-basicos` - Listar usuarios básicos
- `POST /api/super-admin/activar-desactivar-usuario` - Activar/desactivar usuarios

## Cómo Cambiar Contraseñas (Solo Super Admin)

### Método 1: Cambiar contraseña individual

```javascript
// Desde el dashboard de Super Admin
const response = await APIClient.post('/super-admin/cambiar-password-usuario', {
    user_id: 5,
    new_password: 'nueva_contraseña_segura'
});
```

### Método 2: Resetear todas las contraseñas

```javascript
// Resetear todas las contraseñas a valores por defecto
const response = await APIClient.post('/super-admin/resetear-passwords-basicos');
```

### Método 3: Script Python

```python
from backend.app import create_app
from backend.models.user import User
from backend.database import db
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    # Cambiar contraseña específica
    user = User.query.filter_by(rol='monitoreo').first()
    user.password_hash = generate_password_hash('nueva_contraseña')
    db.session.commit()
    print('✓ Contraseña actualizada')
```

## Ventajas de Contraseñas Fijas

### ✅ Beneficios

1. **Control centralizado**: Solo el super admin gestiona credenciales
2. **Seguridad**: Los usuarios no pueden debilitar la seguridad con contraseñas débiles
3. **Simplicidad**: No hay que recordar múltiples contraseñas cambiantes
4. **Auditoría**: Todas las contraseñas están documentadas y controladas
5. **Recuperación**: Fácil reseteo si alguien olvida su contraseña
6. **Consistencia**: Mismas credenciales en todos los entornos

### ⚠️ Consideraciones

1. **Responsabilidad del Super Admin**: Debe mantener las contraseñas seguras
2. **Documentación**: Las contraseñas deben estar documentadas de forma segura
3. **Rotación**: El super admin debe cambiar las contraseñas periódicamente
4. **Acceso físico**: Proteger el acceso a la documentación de contraseñas

## Flujo de Trabajo

### Para Usuarios Básicos

1. **Recibir credenciales** del super admin
2. **Iniciar sesión** con las credenciales proporcionadas
3. **NO intentar cambiar** la contraseña (no funcionará)
4. **Contactar al super admin** si necesita cambio de contraseña

### Para Super Admin

1. **Proporcionar credenciales** a los usuarios básicos
2. **Cambiar contraseñas** cuando sea necesario
3. **Resetear contraseñas** si alguien las olvida
4. **Rotar contraseñas** periódicamente por seguridad
5. **Mantener documentación** actualizada

## Endpoints Disponibles

### Para Super Admin

```
GET  /api/super-admin/usuarios-basicos
POST /api/super-admin/cambiar-password-usuario
POST /api/super-admin/resetear-passwords-basicos
POST /api/super-admin/activar-desactivar-usuario
```

### Para Todos los Usuarios

```
POST /api/auth/change-password  # Bloqueado para usuarios básicos
```

## Mensajes de Error

### Usuario básico intenta cambiar contraseña

```json
{
  "success": false,
  "error": "Los usuarios básicos no pueden cambiar su contraseña. Solo el super admin puede hacerlo."
}
```

### Usuario no autorizado intenta cambiar contraseña de otro

```json
{
  "success": false,
  "error": "Solo el super admin puede cambiar contraseñas de otros usuarios"
}
```

## Seguridad Adicional

### Recomendaciones

1. **Cambiar contraseñas por defecto** inmediatamente en producción
2. **Usar contraseñas complejas** (mínimo 12 caracteres)
3. **Rotar contraseñas** cada 90 días
4. **Monitorear accesos** de usuarios básicos
5. **Mantener logs** de cambios de contraseña
6. **Backup de credenciales** en lugar seguro

### Contraseñas Seguras Sugeridas

```
Super Admin: Adm1n$Elect2024!Secure#
Usuarios Básicos: T3st$2024!Secure#Basic
```

## Troubleshooting

### Usuario no puede iniciar sesión

1. **Verificar credenciales**: Usar exactamente las contraseñas documentadas
2. **Verificar estado**: El usuario debe estar activo
3. **Contactar super admin**: Para verificar/resetear contraseña

### Super admin necesita cambiar contraseña

1. **Usar endpoint específico**: `/api/super-admin/cambiar-password-usuario`
2. **Usar script Python**: Para cambios masivos
3. **Usar reseteo masivo**: Para volver a valores por defecto

### Contraseña olvidada

1. **Contactar super admin**: Único autorizado para resetear
2. **Usar reseteo masivo**: Si múltiples usuarios olvidan
3. **Verificar documentación**: Las contraseñas están documentadas

## Implementación Técnica

### Modificaciones Realizadas

1. **auth.py**: Bloqueado cambio de contraseña para usuarios básicos
2. **super_admin_users.py**: Nuevos endpoints para gestión de contraseñas
3. **app.py**: Registrado nuevo blueprint

### Validaciones Implementadas

```python
# Verificar si es usuario básico
usuarios_basicos = ['super_admin', 'monitoreo', 'coordinador_departamental', 
                   'coordinador_municipal', 'coordinador_puesto', 'auditor_electoral']

if current_user.rol in usuarios_basicos and current_user.rol != 'super_admin':
    return jsonify({
        'success': False,
        'error': 'Los usuarios básicos no pueden cambiar su contraseña. Solo el super admin puede hacerlo.'
    }), 403
```

## Conclusión

El sistema de contraseñas fijas proporciona:

- ✅ **Control centralizado** de credenciales
- ✅ **Seguridad mejorada** con gestión profesional
- ✅ **Simplicidad operativa** para usuarios finales
- ✅ **Auditoría completa** de cambios de contraseña
- ✅ **Recuperación fácil** en caso de olvido

Las contraseñas permanecen **fijas y documentadas**, solo el **Super Admin** puede modificarlas cuando sea necesario.
