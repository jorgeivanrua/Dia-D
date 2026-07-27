# Usuarios del Sistema Electoral

## Usuarios Fijos (No son de prueba)

El sistema tiene usuarios **fijos** con roles específicos. Estos NO son usuarios de prueba, son los usuarios reales del sistema.

## Credenciales de Acceso

### Super Administrador
```
Usuario: admin
Password: admin123
Rol: super_admin
Ubicación: Sin ubicación (acceso global)
```

### Administradores Departamentales
```
Usuario: admin_caqueta
Password: admin123
Rol: admin_departamental
Ubicación: Departamento Caquetá
```

### Administradores Municipales
```
Usuario: admin_florencia
Password: admin123
Rol: admin_municipal
Ubicación: Municipio Florencia
```

### Coordinadores Departamentales
```
Usuario: coord_dpto_caqueta
Password: coord123
Rol: coordinador_departamental
Ubicación: Departamento Caquetá
```

### Coordinadores Municipales
```
Usuario: coord_mun_florencia
Password: coord123
Rol: coordinador_municipal
Ubicación: Municipio Florencia
```

### Coordinadores de Puesto
```
Usuario: coord_puesto_01, coord_puesto_02, ..., coord_puesto_10
Password: coord123
Rol: coordinador_puesto
Ubicación: Puesto específico (01, 02, etc.)
```

### Testigos Electorales
```
Usuario: testigo_01_1, testigo_01_2, testigo_02_1, testigo_02_2, ...
Password: testigo123
Rol: testigo_electoral
Ubicación: Puesto específico
```

### Auditores
```
Usuario: auditor_caqueta
Password: auditor123
Rol: auditor_electoral
Ubicación: Departamento Caquetá
```

### Usuario de Monitoreo
```
Usuario: monitoreo
Password: Monitoreo2025!
Rol: monitoreo
Ubicación: Sin ubicación (acceso global)
```

**Descripción:**
El usuario de monitoreo tiene visibilidad completa del sistema sin restricciones de jurisdicción. Puede ver todos los usuarios, formularios, incidentes y delitos de todas las ubicaciones.

**Dashboard:** `http://localhost:5000/monitoreo/dashboard`

**Funcionalidades:**
- 🗺️ Mapa global de usuarios geolocalizados
- 📊 Estadísticas globales del sistema
- 🎛️ Filtros avanzados por ubicación
- 🔄 Auto-refresh cada 30 segundos

## Estructura de Nombres de Usuario

### Patrón de Nombres

- **Super Admin**: `admin`
- **Administradores**: `admin_{ubicacion}`
- **Coordinadores Departamentales**: `coord_dpto_{departamento}`
- **Coordinadores Municipales**: `coord_mun_{municipio}`
- **Coordinadores de Puesto**: `coord_puesto_{codigo_puesto}`
- **Testigos**: `testigo_{codigo_puesto}_{numero}`
- **Auditores**: `auditor_{ubicacion}`
- **Monitoreo**: `monitoreo`

### Ejemplos

```
admin                    → Super Admin
admin_caqueta           → Admin Departamental Caquetá
admin_florencia         → Admin Municipal Florencia
coord_dpto_caqueta      → Coordinador Departamental Caquetá
coord_mun_florencia     → Coordinador Municipal Florencia
coord_puesto_01         → Coordinador Puesto 01
testigo_01_1            → Testigo 1 del Puesto 01
testigo_01_2            → Testigo 2 del Puesto 01
auditor_caqueta         → Auditor Electoral Caquetá
monitoreo               → Usuario de Monitoreo (acceso global)
```

## Login en el Sistema

### Formato de Login

Para iniciar sesión, los usuarios deben proporcionar:

1. **Rol**: Seleccionar su rol del dropdown
2. **Ubicación**: Seleccionar departamento, municipio, zona, puesto según su rol
3. **Password**: Ingresar su contraseña

### Ejemplo de Login - Super Admin

```
Rol: Super Administrador
Password: admin123
```

### Ejemplo de Login - Coordinador de Puesto

```
Rol: Coordinador de Puesto
Departamento: Caquetá
Municipio: Florencia
Zona: 01
Puesto: 01
Password: coord123
```

### Ejemplo de Login - Testigo Electoral

```
Rol: Testigo Electoral
Departamento: Caquetá
Municipio: Florencia
Zona: 01
Puesto: 01
Password: testigo123
```

## Contraseñas por Rol

| Rol | Password |
|-----|----------|
| Super Admin | admin123 |
| Admin Departamental | admin123 |
| Admin Municipal | admin123 |
| Coordinador Departamental | coord123 |
| Coordinador Municipal | coord123 |
| Coordinador de Puesto | coord123 |
| Testigo Electoral | testigo123 |
| Auditor Electoral | auditor123 |
| Monitoreo | Monitoreo2025! |

## Seguridad

⚠️ **IMPORTANTE**: Estas contraseñas son para el sistema de desarrollo/staging. En producción:

1. Cambiar todas las contraseñas a contraseñas seguras
2. Usar el endpoint `/api/auth/change-password` para cambiar contraseñas
3. Implementar políticas de contraseñas fuertes
4. Considerar autenticación de dos factores (2FA)

## Agregar Nuevos Usuarios

### Desde el Dashboard Super Admin

1. Login como `admin` / `admin123`
2. Ir a "Gestión de Usuarios"
3. Clic en "Crear Usuario"
4. Llenar formulario:
   - Nombre completo
   - Rol
   - Ubicación (departamento, municipio, zona, puesto según rol)
   - Contraseña
5. Guardar

### Desde Script

Editar `scripts/create_fixed_users.py` y agregar el nuevo usuario a la lista `usuarios_fijos`:

```python
{
    'nombre': 'nuevo_usuario',
    'nombre_completo': 'Nombre Completo del Usuario',
    'rol': 'testigo_electoral',
    'ubicacion_id': puesto.id,
    'password': 'password123'
}
```

Luego ejecutar:
```bash
python scripts/create_fixed_users.py
```

## Resetear Usuarios

Si necesitas resetear todos los usuarios y volver a crearlos:

```bash
python scripts/create_fixed_users.py
```

⚠️ **ADVERTENCIA**: Esto eliminará TODOS los usuarios existentes y creará los usuarios fijos desde cero.

## Verificar Usuarios

Para ver todos los usuarios del sistema:

1. Login como Super Admin
2. Dashboard Super Admin → "Diagnóstico del Sistema"
3. Ver lista de usuarios por rol

O desde línea de comandos:

```bash
python scripts/verificar_roles_jwt.py
```

## Problemas Comunes

### "Credenciales inválidas"

**Causa**: Usuario o contraseña incorrectos, o ubicación incorrecta

**Solución**:
1. Verificar que el usuario existe
2. Verificar la contraseña
3. Verificar que la ubicación seleccionada sea correcta
4. Verificar que el rol seleccionado sea correcto

### "Cuenta bloqueada"

**Causa**: Demasiados intentos fallidos de login (5 intentos)

**Solución**:
1. Esperar 30 minutos
2. O contactar al Super Admin para desbloquear la cuenta
3. Super Admin puede usar "Corregir Roles" para desbloquear todas las cuentas

### Error 403 "No tiene permisos"

**Causa**: Token JWT con rol incorrecto (sesión antigua)

**Solución**:
1. Cerrar sesión
2. Volver a iniciar sesión
3. Esto generará un nuevo token con el rol correcto

## Mantenimiento

### Cambiar Contraseñas Masivamente

Desde el Dashboard Super Admin:
1. Clic en "Arreglar Contraseñas"
2. Esto actualizará todas las contraseñas a los valores por defecto

### Desbloquear Cuentas

Desde el Dashboard Super Admin:
1. Clic en "Corregir Roles"
2. Esto desbloqueará todas las cuentas y reseteará intentos fallidos

### Activar/Desactivar Usuarios

Desde el Dashboard Super Admin:
1. Ir a "Gestión de Usuarios"
2. Buscar el usuario
3. Clic en "Activar" o "Desactivar"
