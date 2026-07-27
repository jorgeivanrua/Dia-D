# GUÍA DE GESTIÓN DE USUARIOS - SUPER ADMIN

## 🔐 IMPORTANTE SOBRE CONTRASEÑAS

Las contraseñas en el sistema están **hasheadas** (encriptadas) por seguridad. Esto significa que:

- ✅ **NO se pueden ver** las contraseñas originales
- ✅ **NO se pueden recuperar** las contraseñas olvidadas
- ✅ **SÍ se pueden resetear** a una nueva contraseña

En la tabla de usuarios verás `••••••••` en la columna de contraseña, indicando que está hasheada.

---

## 📋 FUNCIONALIDADES DISPONIBLES

### 1. Ver Usuarios
- Accede a la pestaña **"Usuarios"** en el dashboard
- Verás una tabla con todos los usuarios del sistema
- Información mostrada:
  - ID
  - Nombre
  - Rol
  - Ubicación
  - Contraseña (hasheada)
  - Estado (Activo/Inactivo)
  - Último acceso
  - Acciones

### 2. Crear Nuevo Usuario

**Pasos:**
1. Click en el botón **"+ Nuevo Usuario"**
2. Llenar el formulario:
   - **Nombre**: Nombre de usuario para login
   - **Rol**: Seleccionar el rol apropiado
   - **Ubicación**: Se muestra automáticamente según el rol seleccionado
   - **Contraseña**: Mínimo 6 caracteres
   - **Confirmar Contraseña**: Debe coincidir con la anterior
3. Click en **"Crear Usuario"**

**Roles disponibles:**
- Super Admin (sin ubicación)
- Admin Departamental (requiere departamento)
- Admin Municipal (requiere departamento y municipio)
- Coordinador Departamental (requiere departamento)
- Coordinador Municipal (requiere departamento y municipio)
- Coordinador de Puesto (requiere departamento, municipio, zona y puesto)
- Testigo Electoral (requiere departamento, municipio, zona y puesto)
- Auditor Electoral (requiere departamento)

### 3. Editar Usuario

**Pasos:**
1. En la tabla de usuarios, click en el botón **✏️ (Editar)**
2. Modificar los campos necesarios:
   - Nombre
   - Rol
3. Click en **"Guardar Cambios"**

**Nota:** La ubicación no se puede editar desde aquí. Si necesitas cambiar la ubicación, debes crear un nuevo usuario.

### 4. Resetear Contraseña

**Pasos:**
1. En la tabla de usuarios, click en el botón **🔑 (Resetear contraseña)**
2. Ingresa la nueva contraseña en el prompt
3. Confirma la acción

**Importante:**
- La nueva contraseña debe tener mínimo 6 caracteres
- El usuario podrá iniciar sesión inmediatamente con la nueva contraseña
- No hay forma de recuperar la contraseña anterior

### 5. Activar/Desactivar Usuario

**Pasos:**
1. En la tabla de usuarios, click en el botón **❌ (Desactivar)** o **✓ (Activar)**
2. Confirma la acción

**Efectos:**
- **Usuario Inactivo**: No puede iniciar sesión
- **Usuario Activo**: Puede iniciar sesión normalmente

---

## 🔍 FILTROS Y BÚSQUEDA

### Filtrar por Rol
1. Usa el dropdown **"Todos los roles"**
2. Selecciona el rol que deseas ver
3. La tabla se actualizará automáticamente

### Filtrar por Estado
1. Usa el dropdown **"Todos los estados"**
2. Selecciona "Activo" o "Inactivo"
3. La tabla se actualizará automáticamente

### Buscar por Nombre
1. Usa el campo de búsqueda
2. Escribe el nombre del usuario
3. La tabla se filtrará en tiempo real

---

## 📊 CONTRASEÑAS ACTUALES DEL SISTEMA

### Usuarios Existentes (antes de la creación del Caquetá):

**Super Admin:**
- Usuario: `Super Admin` o `super_admin`
- Contraseña: `admin123`

**Usuarios de Prueba:**
- Usuario: `monitoreo`, `auditor`, `coord_dept`, `coord_mun`, `coord_puesto`, `testigo1`
- Contraseña: `test123`

### Usuarios del Caquetá (363 usuarios):

**Coordinador Departamental:**
- Usuario: `CAQUETA`
- Contraseña: `test123`

**Coordinadores Municipales (16):**
- Formato: `NOMBRE_MUNICIPIO` (ej: `FLORENCIA`, `ALBANIA`)
- Contraseña: `test123`

**Coordinadores de Puesto (150):**
- Formato: `MUNICIPIO_P##` (ej: `FLORENCIA_P01`, `ALBANIA_P10`)
- Contraseña: `test123`

**Testigos Electorales (196):**
- Formato: `MUNICIPIO_P##_M##` (ej: `FLORENCIA_P01_M01`)
- Contraseña: `test123`

---

## ⚠️ RECOMENDACIONES DE SEGURIDAD

### Para Producción:
1. **Cambiar todas las contraseñas por defecto**
   - Especialmente la del Super Admin
   - Usar contraseñas fuertes (mínimo 12 caracteres)
   - Incluir mayúsculas, minúsculas, números y símbolos

2. **Desactivar usuarios no utilizados**
   - Revisar periódicamente la lista de usuarios
   - Desactivar cuentas inactivas

3. **Documentar cambios de contraseña**
   - Mantener un registro de cuándo se resetean contraseñas
   - Notificar a los usuarios afectados

4. **Revisar accesos**
   - Monitorear la columna "Último acceso"
   - Investigar accesos sospechosos

### Para Desarrollo:
- Las contraseñas `test123` y `admin123` son solo para pruebas
- No usar estas contraseñas en producción
- Cambiarlas antes de desplegar el sistema

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### "No puedo ver la contraseña de un usuario"
**Solución:** Las contraseñas están hasheadas por seguridad. No se pueden ver. Si necesitas que un usuario acceda, resetea su contraseña.

### "Olvidé la contraseña del Super Admin"
**Solución:** 
1. Accede con otro usuario Super Admin (si existe)
2. O ejecuta el script de reseteo:
   ```bash
   python backend/scripts/reset_super_admin_password.py
   ```

### "No puedo editar la ubicación de un usuario"
**Solución:** La ubicación no se puede editar. Debes:
1. Desactivar el usuario actual
2. Crear un nuevo usuario con la ubicación correcta

### "El botón de Nuevo Usuario no funciona"
**Solución:**
1. Verifica que estés en la pestaña "Usuarios"
2. Recarga la página (Ctrl+F5)
3. Verifica la consola del navegador (F12) para errores

### "No se cargan los departamentos/municipios"
**Solución:**
1. Verifica que la base de datos tenga ubicaciones cargadas
2. Ejecuta: `python scripts/load_only_caqueta.py`
3. Recarga la página

---

## 📞 CONTACTO Y SOPORTE

Si encuentras algún problema no documentado aquí:
1. Revisa los logs del sistema en `instance/logs/`
2. Verifica la consola del navegador (F12)
3. Consulta la documentación técnica en `docs/`

---

**Última actualización:** 30 de Noviembre de 2025
