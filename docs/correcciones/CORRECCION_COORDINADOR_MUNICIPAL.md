# Corrección Dashboard Coordinador Municipal

## Fecha: 2025-12-06

## Problemas Identificados

Según la captura de pantalla y los errores en consola:

1. **Errores de carga en el dashboard**
   - Múltiples errores 500 (INTERNAL SERVER ERROR)
   - Errores al cargar endpoints:
     - `/api/coordinador-municipal/puestos`
     - `/api/coordinador-municipal/estadisticas`
     - `/api/coordinador-municipal/consolidado`
     - `/api/coordinador-municipal/discrepancias`

2. **Interfaz incompleta**
   - Dashboard muestra "Cargando..." pero no carga datos
   - Estadísticas en 0
   - Tabla de puestos vacía

3. **Falta de funcionalidades**
   - No tiene mapa de geolocalización
   - No tiene gestión de incidentes/delitos
   - No tiene tabla E-24 consolidada

## Soluciones Implementadas

### 1. Correcciones en JavaScript
**Archivo:** `frontend/static/js/coordinador-municipal.js`

**Cambios:**
- ✅ Agregado manejo de errores mejorado en inicialización
- ✅ Agregado logs de depuración
- ✅ Corregido endpoint de perfil (`/auth/profile`)
- ✅ Agregado manejo de errores en `loadUserProfile()`
- ✅ Mejorado manejo de elementos DOM que pueden no existir

### 2. Nuevo Template Mejorado
**Archivo:** `frontend/templates/coordinador/municipal-mejorado.html`

**Características:**
- ✅ Basado en el dashboard del coordinador de puesto
- ✅ Escalado a nivel municipal
- ✅ 6 pestañas completas:
  1. Puestos
  2. E-24 Consolidado
  3. Incidentes
  4. Delitos
  5. Coordinadores
  6. Mapa
- ✅ Responsive y mobile-first
- ✅ Integración con MapaGeolocalizacion

### 3. Documentación
**Archivo:** `MEJORAS_COORDINADOR_MUNICIPAL.md`

Contiene:
- Plan completo de mejoras
- Diferencias entre coordinador de puesto y municipal
- Endpoints necesarios
- Pasos de implementación

## Archivos Modificados

1. `frontend/static/js/coordinador-municipal.js`
   - Mejorado manejo de errores
   - Agregados logs de depuración
   - Corregido endpoint de perfil

## Archivos Creados

1. `frontend/templates/coordinador/municipal-mejorado.html`
   - Template HTML completo y mejorado
   
2. `MEJORAS_COORDINADOR_MUNICIPAL.md`
   - Documentación completa de mejoras
   
3. `CORRECCION_COORDINADOR_MUNICIPAL.md`
   - Este documento

## Próximos Pasos para Completar

### 1. Verificar Endpoints Backend
Los siguientes endpoints deben existir y funcionar:

```python
# Endpoints existentes a verificar
GET /api/coordinador-municipal/puestos
GET /api/coordinador-municipal/estadisticas  
GET /api/coordinador-municipal/consolidado
GET /api/coordinador-municipal/discrepancias
GET /api/coordinador-municipal/puesto/<id>

# Endpoints nuevos a crear
GET /api/coordinador-municipal/incidentes
GET /api/coordinador-municipal/delitos
GET /api/coordinador-municipal/coordinadores
GET /api/coordinador-municipal/e24-datos
POST /api/coordinador-municipal/e24-generar
GET /api/coordinador-municipal/exportar
```

### 2. Actualizar Ruta Frontend
```python
# En backend/routes/frontend.py
@frontend_bp.route('/coordinador/municipal')
@jwt_required()
@role_required(['coordinador_municipal'])
def coordinador_municipal_dashboard():
    return render_template('coordinador/municipal-mejorado.html')
```

### 3. Crear JavaScript Completo
Crear `frontend/static/js/coordinador-municipal-mejorado.js` con todas las funciones necesarias.

### 4. Probar Funcionalidades
- [ ] Login como coordinador municipal
- [ ] Verificar carga de puestos
- [ ] Verificar estadísticas
- [ ] Verificar consolidado
- [ ] Verificar mapa
- [ ] Verificar E-24
- [ ] Verificar incidentes y delitos

## Errores Actuales a Resolver

### Error 1: Endpoints 500
**Problema:** Los endpoints del backend están devolviendo error 500

**Posibles causas:**
1. Servicios no implementados correctamente
2. Errores en queries de base de datos
3. Permisos incorrectos
4. Datos faltantes en la base de datos

**Solución:**
1. Revisar logs del servidor
2. Verificar implementación de servicios
3. Verificar que el usuario tenga ubicación asignada
4. Verificar que existan puestos en el municipio

### Error 2: Datos No Cargan
**Problema:** El dashboard muestra "Cargando..." pero no carga datos

**Causa:** Los endpoints están fallando (error 500)

**Solución:** Resolver los errores del backend primero

## Recomendaciones

### Inmediatas
1. **Revisar logs del servidor** para ver el error exacto de los endpoints
2. **Verificar base de datos** - que el coordinador tenga ubicación asignada
3. **Probar endpoints** con Postman o similar
4. **Usar el template mejorado** una vez resueltos los errores de backend

### A Mediano Plazo
1. Implementar todos los endpoints faltantes
2. Crear JavaScript completo para el template mejorado
3. Agregar tests para los endpoints
4. Documentar el uso del dashboard

### A Largo Plazo
1. Unificar la lógica de coordinadores (puesto, municipal, departamental)
2. Crear componentes reutilizables
3. Implementar caché para mejorar rendimiento
4. Agregar notificaciones en tiempo real

## Comandos Útiles para Depuración

### Ver logs del servidor
```bash
# Si estás usando el servidor de desarrollo
python run.py

# Los errores aparecerán en la consola
```

### Probar endpoints
```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"nombre":"coord_muni","password":"test123"}'

# Obtener puestos (reemplazar TOKEN)
curl -X GET http://localhost:5000/api/coordinador-municipal/puestos \
  -H "Authorization: Bearer TOKEN"
```

### Verificar usuario en base de datos
```python
# En consola de Python
from backend.models.user import User
from backend.models.location import Location

# Buscar coordinador municipal
coord = User.query.filter_by(rol='coordinador_municipal').first()
print(f"Usuario: {coord.nombre}")
print(f"Ubicación ID: {coord.ubicacion_id}")

# Verificar ubicación
if coord.ubicacion_id:
    ubicacion = Location.query.get(coord.ubicacion_id)
    print(f"Ubicación: {ubicacion.nombre_completo}")
    print(f"Tipo: {ubicacion.tipo}")
```

## Estado Final

### Completado ✅
- Correcciones en JavaScript existente
- Nuevo template HTML mejorado
- Documentación completa

### Pendiente ⏳
- Resolver errores 500 en endpoints backend
- Crear JavaScript completo para template mejorado
- Actualizar ruta frontend
- Probar funcionalidades completas

## Contacto y Soporte

Si necesitas ayuda adicional:
1. Revisa los logs del servidor
2. Verifica la base de datos
3. Prueba los endpoints individualmente
4. Consulta la documentación en `MEJORAS_COORDINADOR_MUNICIPAL.md`
