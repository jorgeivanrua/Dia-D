# Credenciales de Acceso - Sistema Electoral

## ⚠️ IMPORTANTE

Estas son las credenciales **REALES** del sistema. El campo "Usuario" es el que se usa para el login basado en ubicación.

## 🔐 Credenciales por Rol

### Super Administrador
```
Rol: Super Administrador
Usuario en BD: admin
Password: admin123
Ubicación: Ninguna (acceso global)
```

**Cómo iniciar sesión:**
1. Seleccionar rol: "Super Administrador"
2. Ingresar password: `admin123`
3. No se requiere seleccionar ubicación

---

### Coordinador de Puesto
```
Rol: Coordinador de Puesto
Usuario en BD: coord_puesto_01, coord_puesto_02, etc.
Password: coord123
Ubicación: Puesto específico
```

**Cómo iniciar sesión:**
1. Seleccionar rol: "Coordinador de Puesto"
2. Seleccionar:
   - Departamento: Caquetá
   - Municipio: Florencia
   - Zona: 01
   - Puesto: 01 (o el que corresponda)
3. Ingresar password: `coord123`

---

### Testigo Electoral
```
Rol: Testigo Electoral
Usuario en BD: testigo_01_1, testigo_01_2, testigo_02_1, etc.
Password: testigo123
Ubicación: Puesto específico
```

**Cómo iniciar sesión:**
1. Seleccionar rol: "Testigo Electoral"
2. Seleccionar:
   - Departamento: Caquetá
   - Municipio: Florencia
   - Zona: 01
   - Puesto: 01 (o el que corresponda)
3. Ingresar password: `testigo123`

---

### Coordinador Municipal
```
Rol: Coordinador Municipal
Usuario en BD: coord_mun_florencia
Password: coord123
Ubicación: Municipio Florencia
```

**Cómo iniciar sesión:**
1. Seleccionar rol: "Coordinador Municipal"
2. Seleccionar:
   - Departamento: Caquetá
   - Municipio: Florencia
3. Ingresar password: `coord123`

---

### Coordinador Departamental
```
Rol: Coordinador Departamental
Usuario en BD: coord_dpto_caqueta
Password: coord123
Ubicación: Departamento Caquetá
```

**Cómo iniciar sesión:**
1. Seleccionar rol: "Coordinador Departamental"
2. Seleccionar:
   - Departamento: Caquetá
3. Ingresar password: `coord123`

---

### Administrador Municipal
```
Rol: Admin Municipal
Usuario en BD: admin_florencia
Password: admin123
Ubicación: Municipio Florencia
```

**Cómo iniciar sesión:**
1. Seleccionar rol: "Admin Municipal"
2. Seleccionar:
   - Departamento: Caquetá
   - Municipio: Florencia
3. Ingresar password: `admin123`

---

### Administrador Departamental
```
Rol: Admin Departamental
Usuario en BD: admin_caqueta
Password: admin123
Ubicación: Departamento Caquetá
```

**Cómo iniciar sesión:**
1. Seleccionar rol: "Admin Departamental"
2. Seleccionar:
   - Departamento: Caquetá
3. Ingresar password: `admin123`

---

### Auditor Electoral
```
Rol: Auditor Electoral
Usuario en BD: auditor_caqueta
Password: auditor123
Ubicación: Departamento Caquetá
```

**Cómo iniciar sesión:**
1. Seleccionar rol: "Auditor Electoral"
2. Seleccionar:
   - Departamento: Caquetá
3. Ingresar password: `auditor123`

---

## 📋 Resumen de Contraseñas

| Rol | Password |
|-----|----------|
| Super Admin | `admin123` |
| Admin Departamental | `admin123` |
| Admin Municipal | `admin123` |
| Coordinador Departamental | `coord123` |
| Coordinador Municipal | `coord123` |
| Coordinador de Puesto | `coord123` |
| Testigo Electoral | `testigo123` |
| Auditor Electoral | `auditor123` |

## 🔍 Cómo Funciona el Login

El sistema usa **login basado en ubicación**. No se ingresa un "nombre de usuario" tradicional. En su lugar:

1. **Seleccionas tu rol** del dropdown
2. **Seleccionas tu ubicación** (departamento, municipio, zona, puesto según tu rol)
3. **Ingresas tu contraseña**

El sistema busca en la base de datos un usuario que tenga:
- El rol seleccionado
- La ubicación seleccionada
- La contraseña correcta

## ❌ Errores Comunes

### "Credenciales inválidas"

**Causas posibles:**
1. Contraseña incorrecta
2. Ubicación incorrecta (seleccionaste un departamento/municipio/puesto diferente al asignado)
3. Rol incorrecto

**Solución:**
- Verificar que la contraseña sea exactamente como se muestra arriba (distingue mayúsculas/minúsculas)
- Verificar que la ubicación seleccionada sea la correcta
- Para testigos y coordinadores de puesto: asegurarse de seleccionar el puesto correcto

### "Cuenta bloqueada"

**Causa:** Demasiados intentos fallidos (5 intentos)

**Solución:**
- Esperar 30 minutos
- O contactar al Super Admin para desbloquear

### Error 403 "No tiene permisos"

**Causa:** Token JWT con rol incorrecto (sesión antigua)

**Solución:**
1. Cerrar sesión
2. Volver a iniciar sesión
3. Esto generará un nuevo token con el rol correcto

## 🔧 Para Desarrolladores

### Estructura en la Base de Datos

```sql
-- Ejemplo de usuario en la BD
nombre: 'admin'                    -- Este es el identificador único
rol: 'super_admin'
password_hash: 'admin123'          -- Texto plano (temporal)
ubicacion_id: NULL                 -- Sin ubicación para super_admin
activo: TRUE
```

### Cómo se Busca el Usuario en el Login

```python
# El sistema busca así:
user = User.query.filter_by(
    rol=rol_seleccionado,
    ubicacion_id=ubicacion_id,
    activo=True
).first()

# Luego verifica la contraseña:
if user.check_password(password):
    # Login exitoso
```

### Cambiar Contraseñas

Desde el Dashboard Super Admin:
1. Ir a "Gestión de Usuarios"
2. Buscar el usuario
3. Clic en "Resetear Contraseña"

O usar el endpoint:
```bash
POST /api/admin/fix-passwords
```

## 📝 Notas

1. **Las contraseñas están en texto plano** (sin bcrypt) para compatibilidad con Render gratuito
2. **En producción** se deben cambiar todas las contraseñas a contraseñas seguras
3. **El campo `nombre` en la BD** es el identificador único del usuario, no un "nombre de usuario" para login
4. **El login es por ubicación**, no por nombre de usuario tradicional
