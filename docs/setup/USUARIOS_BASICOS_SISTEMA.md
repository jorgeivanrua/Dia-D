# Usuarios Básicos del Sistema

## Descripción

El sistema mantiene automáticamente un conjunto de usuarios básicos que siempre deben existir en la base de datos. Estos usuarios se crean automáticamente al iniciar la aplicación si no existen.

## Usuarios Básicos

### 1. Super Admin
- **Nombre**: Super Admin
- **Rol**: `super_admin`
- **Password**: `admin123` ⚠️ (cambiar en producción)
- **Descripción**: Administrador principal del sistema con acceso completo
- **Permisos**:
  - Gestión completa de usuarios
  - Configuración del sistema
  - Acceso a todas las funcionalidades
  - Gestión de campañas
  - Auditoría del sistema

### 2. Monitoreo
- **Nombre**: Monitoreo
- **Rol**: `monitoreo`
- **Password**: `monitoreo123` ⚠️ (cambiar en producción)
- **Descripción**: Usuario de monitoreo en tiempo real
- **Permisos**:
  - Visualización de mapa en tiempo real
  - Estadísticas del sistema
  - Seguimiento de usuarios activos
  - Métricas de rendimiento
  - Solo lectura (no puede modificar datos)

### 3. Coordinador Departamental
- **Nombre**: Coordinador Departamental
- **Rol**: `coordinador_departamental`
- **Password**: `coord_dept123` ⚠️ (cambiar en producción)
- **Descripción**: Coordinador a nivel departamental
- **Permisos**:
  - Gestión de formularios del departamento
  - Validación de formularios
  - Reportes departamentales
  - Gestión de coordinadores municipales

### 4. Coordinador Municipal
- **Nombre**: Coordinador Municipal
- **Rol**: `coordinador_municipal`
- **Password**: `coord_muni123` ⚠️ (cambiar en producción)
- **Descripción**: Coordinador a nivel municipal
- **Permisos**:
  - Gestión de formularios del municipio
  - Validación de formularios
  - Reportes municipales
  - Gestión de coordinadores de puesto

### 5. Coordinador Puesto
- **Nombre**: Coordinador Puesto
- **Rol**: `coordinador_puesto`
- **Password**: `coord_puesto123` ⚠️ (cambiar en producción)
- **Descripción**: Coordinador de puesto de votación
- **Permisos**:
  - Gestión de formularios del puesto
  - Validación de formularios
  - Reportes del puesto
  - Gestión de testigos

### 6. Auditor Electoral
- **Nombre**: Auditor Electoral
- **Rol**: `auditor_electoral`
- **Password**: `auditor123` ⚠️ (cambiar en producción)
- **Descripción**: Auditor del proceso electoral
- **Permisos**:
  - Auditoría de formularios
  - Revisión de incidentes y delitos
  - Generación de reportes de auditoría
  - Acceso de solo lectura a la mayoría de datos

---

## Inicialización Automática

### Al Iniciar la Aplicación

Los usuarios básicos se crean automáticamente cuando la aplicación inicia:

```python
# En backend/app.py
with app.app_context():
    from backend.utils.init_usuarios_basicos import init_usuarios_basicos
    init_usuarios_basicos()
```

### Comportamiento

1. **Si el usuario no existe**: Se crea con la contraseña por defecto
2. **Si el usuario existe**: Se verifica que esté activo
3. **Si el usuario está inactivo**: Se activa automáticamente

---

## Script Manual

Si necesitas crear/actualizar los usuarios manualmente:

```bash
python scripts/crear_usuarios_basicos.py
```

Este script:
- Crea usuarios que no existen
- Actualiza usuarios existentes
- Muestra un resumen completo
- Lista las contraseñas actuales

---

## Cambiar Contraseñas en Producción

### ⚠️ IMPORTANTE

Las contraseñas por defecto son para desarrollo. **DEBEN cambiarse en producción**.

### Método 1: Desde el Dashboard de Super Admin

1. Iniciar sesión como Super Admin
2. Ir a "Gestión de Usuarios"
3. Buscar el usuario
4. Hacer clic en "Cambiar Contraseña"
5. Ingresar nueva contraseña segura

### Método 2: Script Python

```python
from backend.app import create_app
from backend.models.user import User
from backend.database import db
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    # Cambiar contraseña de Super Admin
    user = User.query.filter_by(rol='super_admin').first()
    user.password_hash = generate_password_hash('nueva_contraseña_segura')
    db.session.commit()
    print('Contraseña actualizada')
```

### Método 3: Variables de Entorno

Puedes configurar contraseñas personalizadas usando variables de entorno:

```bash
# En .env
SUPER_ADMIN_PASSWORD=contraseña_segura_123
MONITOREO_PASSWORD=contraseña_segura_456
# ... etc
```

---

## Verificación

### Verificar que los Usuarios Existen

```python
from backend.utils.init_usuarios_basicos import verificar_usuarios_basicos

if verificar_usuarios_basicos():
    print("✓ Todos los usuarios básicos existen")
else:
    print("✗ Faltan usuarios básicos")
```

### Listar Usuarios Básicos

```bash
# En la consola de Python
from backend.models.user import User

roles_basicos = [
    'super_admin',
    'monitoreo',
    'coordinador_departamental',
    'coordinador_municipal',
    'coordinador_puesto',
    'auditor_electoral'
]

for rol in roles_basicos:
    user = User.query.filter_by(rol=rol, activo=True).first()
    if user:
        print(f"✓ {rol}: {user.nombre} (ID: {user.id})")
    else:
        print(f"✗ {rol}: NO ENCONTRADO")
```

---

## Seguridad

### Recomendaciones

1. **Cambiar contraseñas inmediatamente en producción**
2. **Usar contraseñas fuertes** (mínimo 12 caracteres, mayúsculas, minúsculas, números, símbolos)
3. **No compartir credenciales** entre usuarios
4. **Rotar contraseñas periódicamente** (cada 90 días)
5. **Habilitar autenticación de dos factores** (si está disponible)
6. **Monitorear accesos** de estos usuarios críticos
7. **Mantener logs de auditoría** de todas las acciones

### Contraseñas Seguras Ejemplo

```
Super Admin: Adm1n$3cur3!2024#Elect
Monitoreo: M0n1t0r$3cur3!2024#View
Coordinador Dept: C00rd$D3pt!2024#Mgmt
Coordinador Muni: C00rd$Mun1!2024#Mgmt
Coordinador Puesto: C00rd$Pu3st0!2024#Mgmt
Auditor: Aud1t0r$3cur3!2024#Rev
```

---

## Troubleshooting

### Problema: Usuario no puede iniciar sesión

**Solución**:
1. Verificar que el usuario esté activo
2. Verificar que la contraseña sea correcta
3. Ejecutar script de creación de usuarios
4. Verificar logs del servidor

### Problema: Usuario no tiene permisos

**Solución**:
1. Verificar el rol del usuario
2. Verificar que el rol esté correctamente asignado
3. Verificar decoradores `@role_required` en las rutas

### Problema: Usuarios no se crean automáticamente

**Solución**:
1. Verificar logs de la aplicación al iniciar
2. Ejecutar script manual: `python scripts/crear_usuarios_basicos.py`
3. Verificar que la base de datos esté accesible
4. Verificar permisos de escritura en la base de datos

---

## Archivos Relacionados

- `backend/utils/init_usuarios_basicos.py` - Inicialización automática
- `scripts/crear_usuarios_basicos.py` - Script manual
- `backend/app.py` - Llamada a inicialización
- `backend/models/user.py` - Modelo de usuario

---

## Logs

Los logs de inicialización de usuarios se pueden ver en:

```bash
# Logs de la aplicación
tail -f logs/app.log | grep "usuario básico"

# O en Render
# Dashboard > Logs > Buscar "usuario básico"
```

---

## Conclusión

Los usuarios básicos son esenciales para el funcionamiento del sistema. Se crean automáticamente al iniciar la aplicación, pero es crucial cambiar las contraseñas por defecto en producción para mantener la seguridad del sistema.
