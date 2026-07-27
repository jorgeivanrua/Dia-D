# Instrucciones - Sistema de Monitoreo

## Estado del Sistema

✅ **Sistema de Monitoreo Implementado al 50%**

### Funcionalidades Implementadas:
- ✅ Rol de monitoreo configurado en el modelo User
- ✅ Autenticación sin ubicación para rol monitoreo
- ✅ Blueprint monitoreo_bp registrado
- ✅ Endpoint GET /monitoreo/dashboard
- ✅ Endpoint GET /monitoreo/api/usuarios-activos
- ✅ Endpoint GET /monitoreo/api/estadisticas
- ✅ Template del dashboard con mapa y estadísticas
- ✅ Auto-refresh cada 30 segundos
- ✅ Filtros por tipo de usuario y ubicación

### Funcionalidades Pendientes:
- ⏳ Endpoint GET /api/actividad-reciente
- ⏳ Endpoint GET /api/alertas
- ⏳ Endpoint GET /api/incidentes (sin filtros de jurisdicción)
- ⏳ Endpoint GET /api/delitos (sin filtros de jurisdicción)
- ⏳ Endpoint POST /api/exportar
- ⏳ Feed de actividad reciente en dashboard
- ⏳ Panel de alertas en dashboard
- ⏳ Búsqueda global
- ⏳ Mapa de calor
- ⏳ Comparación entre departamentos

---

## Crear/Verificar Usuario de Monitoreo

### Opción 1: Usando Python directamente

```bash
# Desde la raíz del proyecto
python verificar_monitoreo.py
```

### Opción 2: Usando el script batch (Windows)

```bash
crear_usuario_monitoreo.bat
```

### Opción 3: Manualmente desde Python

```python
from backend.database import db
from backend.models.user import User
from backend.app import create_app

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
    print(f"Usuario creado con ID: {usuario.id}")
```

---

## Credenciales de Acceso

**Usuario:** `monitoreo`  
**Contraseña:** `Monitoreo2025!`

⚠️ **IMPORTANTE:** Cambie la contraseña después del primer login

---

## Cómo Hacer Login

### Método 1: Desde la interfaz web

1. Ir a: `http://localhost:5000/login`
2. Seleccionar rol: **Monitoreo**
3. Ingresar contraseña: `Monitoreo2025!`
4. Click en "Iniciar Sesión"

### Método 2: Usando API REST

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "rol": "monitoreo",
    "password": "Monitoreo2025!"
  }'
```

Respuesta esperada:
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 123,
    "nombre": "monitoreo",
    "rol": "monitoreo",
    "ubicacion_id": null
  }
}
```

---

## Acceder al Dashboard de Monitoreo

### URL del Dashboard:
```
http://localhost:5000/monitoreo/dashboard
```

### Características del Dashboard:

1. **Mapa Global de Usuarios**
   - Muestra todos los usuarios con GPS activo
   - Marcadores con colores según rol:
     - 🟢 Verde: Testigo con presencia verificada
     - 🟡 Amarillo: Testigo sin presencia
     - 🔵 Azul: Coordinador de Puesto
     - 🟣 Morado: Coordinador Municipal
     - 🔴 Rosa: Coordinador Departamental
     - 🔷 Cyan: Auditor

2. **Estadísticas Globales**
   - Testigos con geolocalización
   - Testigos con presencia verificada
   - Coordinadores con geolocalización
   - Formularios recibidos y validados

3. **Filtros**
   - Por tipo de usuario
   - Por departamento
   - Por municipio
   - Por zona
   - Por puesto

4. **Auto-Refresh**
   - Actualización automática cada 30 segundos
   - Puede activarse/desactivarse

---

## Endpoints API Disponibles

### 1. GET /monitoreo/api/usuarios-activos

Obtiene todos los usuarios con geolocalización activa.

**Autenticación:** JWT Required  
**Autorización:** Rol monitoreo

**Respuesta:**
```json
{
  "success": true,
  "data": [
    {
      "id": 45,
      "nombre": "Juan Pérez",
      "rol": "testigo_electoral",
      "latitud": 4.6097,
      "longitud": -74.0817,
      "precision": 10.5,
      "ultima_actualizacion": "2025-11-25T10:30:00",
      "ubicacion": { ... },
      "presencia_verificada": true
    }
  ],
  "total": 150
}
```

### 2. GET /monitoreo/api/estadisticas

Obtiene estadísticas globales del sistema.

**Autenticación:** JWT Required  
**Autorización:** Rol monitoreo

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "testigos": {
      "total": 500,
      "con_geolocalizacion": 450,
      "con_presencia_verificada": 480,
      "porcentaje_geo": 90.0
    },
    "coordinadores": {
      "total": 100,
      "con_geolocalizacion": 85,
      "porcentaje_geo": 85.0
    },
    "formularios": {
      "total": 450,
      "validados": 380,
      "pendientes": 70
    }
  }
}
```

---

## Verificar que el Sistema Funciona

### 1. Verificar que el usuario existe

```python
from backend.models.user import User
from backend.app import create_app

app = create_app()
with app.app_context():
    usuario = User.query.filter_by(rol='monitoreo').first()
    if usuario:
        print(f"✅ Usuario encontrado: {usuario.nombre}")
        print(f"   Activo: {usuario.activo}")
        print(f"   Ubicación: {usuario.ubicacion_id}")
    else:
        print("❌ Usuario no encontrado")
```

### 2. Verificar que el blueprint está registrado

```python
from backend.app import create_app

app = create_app()
print("Blueprints registrados:")
for blueprint_name in app.blueprints:
    print(f"  - {blueprint_name}")
```

Debe aparecer: `monitoreo`

### 3. Verificar que las rutas existen

```bash
# Listar todas las rutas
python -c "from backend.app import create_app; app = create_app(); print([str(rule) for rule in app.url_map.iter_rules() if 'monitoreo' in str(rule)])"
```

Debe mostrar:
- `/monitoreo/dashboard`
- `/monitoreo/api/usuarios-activos`
- `/monitoreo/api/estadisticas`

---

## Solución de Problemas

### Problema: "Usuario no encontrado"

**Solución:** Ejecutar el script de creación:
```bash
python verificar_monitoreo.py
```

### Problema: "403 Forbidden" al acceder al dashboard

**Causas posibles:**
1. No está autenticado (no hay token JWT)
2. El token expiró
3. El usuario no tiene rol 'monitoreo'

**Solución:**
1. Hacer login nuevamente
2. Verificar que el rol sea 'monitoreo'
3. Verificar que el decorador @role_required('monitoreo') esté en las rutas

### Problema: "404 Not Found" en /monitoreo/dashboard

**Causas posibles:**
1. El blueprint no está registrado
2. El servidor no está corriendo

**Solución:**
1. Verificar que monitoreo_bp esté en backend/app.py
2. Reiniciar el servidor
3. Verificar que el servidor esté corriendo en el puerto correcto

### Problema: El mapa no muestra usuarios

**Causas posibles:**
1. No hay usuarios con geolocalización activa
2. Error en la API
3. Error de JavaScript en el frontend

**Solución:**
1. Verificar que haya usuarios con ultima_latitud y ultima_longitud no nulos
2. Abrir la consola del navegador (F12) y verificar errores
3. Verificar que el endpoint /monitoreo/api/usuarios-activos responda correctamente

### Problema: Las estadísticas muestran 0

**Causas posibles:**
1. No hay datos en la base de datos
2. Error en las queries

**Solución:**
1. Verificar que haya usuarios y formularios en la base de datos
2. Verificar logs del servidor para errores

---

## Próximos Pasos para Completar el Sistema

Para completar el sistema de monitoreo al 100%, se deben implementar:

1. **Endpoint de Actividad Reciente** (2 horas)
   - GET /monitoreo/api/actividad-reciente
   - Últimos 50 eventos del sistema

2. **Endpoint de Alertas** (2 horas)
   - GET /monitoreo/api/alertas
   - Alertas críticas y notificaciones

3. **Endpoints de Reportes** (2 horas)
   - GET /monitoreo/api/incidentes
   - GET /monitoreo/api/delitos
   - Sin filtros de jurisdicción

4. **Endpoint de Exportación** (2 horas)
   - POST /monitoreo/api/exportar
   - Formatos: Excel, CSV, PDF

5. **Componentes Frontend** (4 horas)
   - Feed de actividad reciente
   - Panel de alertas
   - Búsqueda global
   - Mapa de calor
   - Comparación entre departamentos

**Tiempo Total Estimado:** 12 horas

---

## Documentación Adicional

- **Spec Completo:** `.kiro/specs/sistema-monitoreo/`
- **Requirements:** `.kiro/specs/sistema-monitoreo/requirements.md`
- **Design:** `.kiro/specs/sistema-monitoreo/design.md`
- **Tasks:** `.kiro/specs/sistema-monitoreo/tasks.md`

---

**Fecha de Creación:** 2025-11-25  
**Última Actualización:** 2025-11-25  
**Estado:** Sistema Parcialmente Implementado (50%)

