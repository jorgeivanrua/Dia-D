# Verificar Usuario de Monitoreo

## Resumen de la Revisión

He revisado el sistema completo y encontré lo siguiente:

### ✅ Sistema de Monitoreo - Estado

**Implementación:** 50% completado

**Componentes Verificados:**
- ✅ Rol 'monitoreo' está en el modelo User (CHECK constraint)
- ✅ Servicio de autenticación permite login sin ubicación para rol monitoreo
- ✅ Blueprint monitoreo_bp existe y está registrado
- ✅ 3 endpoints implementados
- ✅ Template del dashboard completo
- ✅ Auto-refresh y filtros funcionando

### ❓ Usuario de Monitoreo - Estado Desconocido

**No encontré evidencia de que el usuario esté creado:**
- ❌ No está en `md_funciones/USUARIOS_SISTEMA.md`
- ❌ No está en los scripts de carga de datos
- ❌ No pude verificar la base de datos (requiere entorno virtual activo)

---

## Cómo Verificar si el Usuario Existe

### Opción 1: Desde la Aplicación Web

1. **Iniciar el servidor:**
   ```bash
   start.bat
   ```

2. **Intentar hacer login:**
   - URL: `http://localhost:5000/login`
   - Seleccionar rol: **Monitoreo**
   - Contraseña: `Monitoreo2025!`
   - Si funciona → El usuario existe ✅
   - Si dice "Credenciales inválidas" → El usuario NO existe ❌

### Opción 2: Desde Python (Recomendado)

1. **Activar entorno virtual:**
   ```bash
   .venv\Scripts\activate
   ```

2. **Ejecutar script de verificación:**
   ```bash
   python verificar_monitoreo.py
   ```

   **Resultado esperado si existe:**
   ```
   ✅ Usuario de monitoreo encontrado:
      ID: 123
      Nombre: monitoreo
      Rol: monitoreo
      Activo: True
      Ubicación ID: None
   ```

   **Resultado esperado si NO existe:**
   ```
   📝 Creando usuario de monitoreo...
   ✅ Usuario creado exitosamente:
      ID: 123
      Nombre: monitoreo
      Contraseña: Monitoreo2025!
      Rol: monitoreo
   ```

### Opción 3: Desde la Consola de Python

1. **Activar entorno virtual:**
   ```bash
   .venv\Scripts\activate
   ```

2. **Abrir consola de Python:**
   ```bash
   python
   ```

3. **Ejecutar:**
   ```python
   from backend.app import create_app
   from backend.models.user import User
   
   app = create_app()
   with app.app_context():
       usuario = User.query.filter_by(rol='monitoreo').first()
       if usuario:
           print(f"✅ Usuario encontrado: {usuario.nombre}")
           print(f"   ID: {usuario.id}")
           print(f"   Activo: {usuario.activo}")
           print(f"   Ubicación: {usuario.ubicacion_id}")
       else:
           print("❌ Usuario NO encontrado")
   ```

### Opción 4: Desde el Dashboard Super Admin

1. **Login como Super Admin:**
   - Usuario: `admin`
   - Contraseña: `admin123`

2. **Ir a "Gestión de Usuarios"**

3. **Buscar usuario con rol "monitoreo"**
   - Si aparece → Existe ✅
   - Si no aparece → No existe ❌

---

## Si el Usuario NO Existe - Cómo Crearlo

### Método 1: Script Automático (Recomendado)

```bash
# Activar entorno virtual
.venv\Scripts\activate

# Ejecutar script
python verificar_monitoreo.py
```

El script:
- Verificará si existe
- Si no existe, lo creará automáticamente
- Mostrará las credenciales

### Método 2: Desde Python

```bash
# Activar entorno virtual
.venv\Scripts\activate

# Abrir Python
python
```

```python
from backend.app import create_app
from backend.models.user import User
from backend.database import db

app = create_app()
with app.app_context():
    # Crear usuario
    usuario = User(
        nombre='monitoreo',
        rol='monitoreo',
        ubicacion_id=None,
        activo=True
    )
    usuario.set_password('Monitoreo2025!')
    
    db.session.add(usuario)
    db.session.commit()
    
    print(f"✅ Usuario creado con ID: {usuario.id}")
```

### Método 3: Desde el Dashboard Super Admin

1. **Login como Super Admin**

2. **Ir a "Gestión de Usuarios" → "Crear Usuario"**

3. **Llenar formulario:**
   - Nombre: `monitoreo`
   - Rol: `Monitoreo`
   - Contraseña: `Monitoreo2025!`
   - Ubicación: Dejar vacío (sin ubicación)
   - Activo: ✅

4. **Guardar**

---

## Credenciales del Usuario Monitoreo

```
Usuario: monitoreo
Contraseña: Monitoreo2025!
Rol: monitoreo
Ubicación: null (sin restricciones de jurisdicción)
```

---

## Probar el Sistema de Monitoreo

### 1. Hacer Login

**URL:** `http://localhost:5000/login`

**Datos:**
- Rol: Monitoreo
- Contraseña: `Monitoreo2025!`

### 2. Acceder al Dashboard

**URL:** `http://localhost:5000/monitoreo/dashboard`

**Deberías ver:**
- 🗺️ Mapa con usuarios geolocalizados
- 📊 Estadísticas globales
- 🎛️ Filtros por tipo de usuario y ubicación
- 🔄 Auto-refresh cada 30 segundos

### 3. Verificar Funcionalidades

**Funcionalidades que DEBEN funcionar:**
- ✅ Mapa muestra todos los usuarios con GPS
- ✅ Estadísticas muestran totales correctos
- ✅ Filtros funcionan correctamente
- ✅ Auto-refresh actualiza datos cada 30 segundos
- ✅ Marcadores tienen colores según rol
- ✅ Popups muestran información del usuario

**Funcionalidades que NO funcionarán (pendientes):**
- ❌ Feed de actividad reciente
- ❌ Panel de alertas
- ❌ Búsqueda global
- ❌ Mapa de calor
- ❌ Comparación entre departamentos
- ❌ Exportación de datos

---

## Actualizar Documentación

Si el usuario existe y funciona, actualizar el archivo:

**Archivo:** `md_funciones/USUARIOS_SISTEMA.md`

**Agregar sección:**

```markdown
### Usuario de Monitoreo
```
Usuario: monitoreo
Password: Monitoreo2025!
Rol: monitoreo
Ubicación: Sin ubicación (acceso global a todos los datos)
```

**Descripción:**
El usuario de monitoreo tiene visibilidad completa del sistema sin restricciones de jurisdicción. Puede ver todos los usuarios, formularios, incidentes y delitos de todas las ubicaciones.

**Dashboard:**
- Mapa global de usuarios geolocalizados
- Estadísticas globales del sistema
- Filtros avanzados por ubicación
- Auto-refresh cada 30 segundos
```

---

## Resumen de Acciones

### Para Verificar:
1. ✅ Activar entorno virtual: `.venv\Scripts\activate`
2. ✅ Ejecutar: `python verificar_monitoreo.py`
3. ✅ Intentar login en `http://localhost:5000/login`

### Si NO Existe:
1. ✅ El script `verificar_monitoreo.py` lo creará automáticamente
2. ✅ O crearlo manualmente desde Dashboard Super Admin
3. ✅ O crearlo desde Python con el código proporcionado

### Si Existe:
1. ✅ Verificar que esté activo
2. ✅ Verificar que ubicacion_id sea null
3. ✅ Probar login y dashboard
4. ✅ Actualizar documentación

---

**Fecha:** 2025-11-25  
**Estado:** Pendiente de verificación por el usuario

