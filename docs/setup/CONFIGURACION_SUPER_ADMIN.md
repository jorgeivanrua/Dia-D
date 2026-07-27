# 🔐 Configuración del Super Admin

## 📋 Resumen

El Super Admin tiene control total sobre qué datos están disponibles en el sistema. Todas las configuraciones se respetan en tiempo real en todos los endpoints.

## 🎯 Áreas de Configuración

### 1. 🎨 Partidos Políticos

**Panel:** Dashboard Super Admin → Partidos

**Configuración disponible:**
- ✅ Activar/Desactivar partidos
- ✅ Editar información (nombre, color, logo)
- ✅ Establecer orden de visualización
- ✅ Eliminar partidos

**Impacto en el sistema:**
```python
# Todos los endpoints filtran por activo=True
partidos = Partido.query.filter_by(activo=True).all()
```

**Endpoints afectados:**
- `GET /api/locations/partidos` - Solo partidos activos
- `GET /api/testigo/tipos-eleccion` - Solo muestra partidos activos
- Formularios E-14 - Solo permiten seleccionar partidos activos

**Ejemplo:**
```
Si desactivas "Centro Democrático":
❌ No aparecerá en formularios E-14
❌ No se podrá registrar votos para ese partido
✅ Los datos históricos se mantienen
```

---

### 2. 👤 Candidatos

**Panel:** Dashboard Super Admin → Candidatos

**Configuración disponible:**
- ✅ Activar/Desactivar candidatos
- ✅ Asignar a tipo de elección
- ✅ Asignar a partido
- ✅ Establecer número de lista
- ✅ Marcar como cabeza de lista
- ✅ Eliminar candidatos

**Impacto en el sistema:**
```python
# Filtrado por activo y tipo de elección
candidatos = Candidato.query.filter_by(
    activo=True,
    tipo_eleccion_id=tipo_eleccion_id
).all()
```

**Endpoints afectados:**
- `GET /api/testigo/candidatos/<tipo_eleccion_id>` - Solo candidatos activos
- Formularios E-14 - Solo candidatos activos del tipo de elección

**Ejemplo:**
```
Si desactivas "Gustavo Bolívar":
❌ No aparecerá en formularios de Senado
❌ No se podrá registrar votos para ese candidato
✅ Los datos históricos se mantienen
```

---

### 3. 🗳️ Tipos de Elección

**Panel:** Dashboard Super Admin → Tipos de Elección

**Configuración disponible:**
- ✅ Activar/Desactivar tipos de elección
- ✅ Configurar si es uninominal
- ✅ Permitir lista cerrada/abierta
- ✅ Permitir coaliciones
- ✅ Establecer orden

**Impacto en el sistema:**
```python
# Solo tipos activos
tipos = TipoEleccion.query.filter_by(activo=True).all()
```

**Endpoints afectados:**
- `GET /api/testigo/tipos-eleccion` - Solo tipos activos
- Formularios E-14 - Solo tipos de elección activos

**Ejemplo:**
```
Si desactivas "Concejo Municipal":
❌ No aparecerá en formularios E-14
❌ No se podrán registrar actas de Concejo
✅ Los datos históricos se mantienen
```

---

### 4. 👥 Usuarios

**Panel:** Dashboard Super Admin → Usuarios

**Configuración disponible:**
- ✅ Crear usuarios
- ✅ Asignar roles
- ✅ Asignar ubicaciones
- ✅ Activar/Desactivar usuarios
- ✅ Resetear contraseñas
- ✅ Ver historial de acceso

**Roles disponibles:**
1. **Super Admin** - Control total del sistema
2. **Monitoreo** - Dashboard de monitoreo en tiempo real
3. **Auditor Electoral** - Auditoría y reportes
4. **Coordinador Departamental** - Coordinación departamental
5. **Coordinador Municipal** - Coordinación municipal
6. **Coordinador de Puesto** - Coordinación de puesto
7. **Testigo Electoral** - Registro de formularios E-14

**Impacto en el sistema:**
```python
# Solo usuarios activos pueden hacer login
user = User.query.filter_by(
    nombre=username,
    activo=True
).first()
```

**Ejemplo:**
```
Si desactivas un testigo:
❌ No podrá hacer login
❌ No podrá registrar formularios
✅ Sus datos históricos se mantienen
✅ Puede reactivarse en cualquier momento
```

---

### 5. 📍 Ubicaciones (Departamentos y Municipios)

**Panel:** Dashboard Super Admin → Ubicaciones

**Configuración disponible:**
- ✅ Activar/Desactivar departamentos
- ✅ Activar/Desactivar municipios
- ✅ Activar/Desactivar zonas
- ✅ Activar/Desactivar puestos
- ✅ Activar/Desactivar mesas

**Impacto en el sistema:**
```python
# Todos los endpoints filtran por activo=True
ubicaciones = Location.query.filter_by(activo=True).all()
```

**Endpoints afectados:**
- `GET /api/locations/departamentos` - Solo departamentos activos
- `GET /api/locations/municipios/<codigo>` - Solo municipios activos
- `GET /api/locations/zonas/<codigo>` - Solo zonas activas
- `GET /api/locations/puestos/<codigo>` - Solo puestos activos
- `GET /api/locations/mesas` - Solo mesas activas
- Login de testigos - Solo ubicaciones activas

**Ejemplo:**
```
Si desactivas el departamento de "Caquetá":
❌ No aparecerá en selectores
❌ Testigos de Caquetá no podrán hacer login
❌ No se podrán registrar formularios de Caquetá
✅ Los datos históricos se mantienen
✅ Puede reactivarse para futuras elecciones
```

---

## 🔄 Flujo de Configuración

### Escenario 1: Preparar Sistema para Elecciones de Senado

```
1. Super Admin accede al dashboard
2. Va a "Tipos de Elección"
3. Activa solo "Senado"
4. Desactiva otros tipos (Cámara, Concejo, etc.)
5. Va a "Candidatos"
6. Activa solo candidatos de Senado
7. Va a "Partidos"
8. Activa solo partidos que participan en Senado
```

**Resultado:**
- ✅ Testigos solo ven formularios de Senado
- ✅ Solo pueden registrar candidatos de Senado
- ✅ Solo aparecen partidos participantes

### Escenario 2: Limitar a un Departamento Específico

```
1. Super Admin accede al dashboard
2. Va a "Ubicaciones"
3. Desactiva todos los departamentos excepto "Antioquia"
4. Verifica que municipios de Antioquia estén activos
```

**Resultado:**
- ✅ Solo aparece Antioquia en selectores
- ✅ Testigos de otros departamentos no pueden hacer login
- ✅ Sistema enfocado en un solo departamento

### Escenario 3: Desactivar Usuario Temporal

```
1. Super Admin accede al dashboard
2. Va a "Usuarios"
3. Busca el usuario "testigo1"
4. Clic en "Desactivar"
```

**Resultado:**
- ✅ Usuario no puede hacer login
- ✅ Datos históricos se mantienen
- ✅ Puede reactivarse cuando sea necesario

---

## 🛡️ Seguridad y Validaciones

### Validaciones en Backend

Todos los endpoints validan que los datos estén activos:

```python
# Ejemplo: Endpoint de partidos
@locations_bp.route('/partidos', methods=['GET'])
@jwt_required()
def get_partidos():
    partidos = Partido.query.filter_by(activo=True).order_by(Partido.nombre).all()
    return jsonify({
        'success': True,
        'data': [partido.to_dict() for partido in partidos]
    })
```

### Validaciones en Frontend

El frontend también valida antes de mostrar:

```javascript
// Ejemplo: Cargar partidos
async function loadPartidos() {
    const response = await APIClient.get('/locations/partidos');
    // Solo muestra partidos activos (ya filtrados por backend)
    const partidos = response.data.filter(p => p.activo);
    renderPartidos(partidos);
}
```

### Validaciones en Formularios

Los formularios E-14 validan que:
- ✅ El tipo de elección esté activo
- ✅ Los partidos estén activos
- ✅ Los candidatos estén activos
- ✅ La ubicación esté activa

```python
# Ejemplo: Validación al registrar formulario
def validar_formulario(data):
    tipo_eleccion = TipoEleccion.query.get(data['tipo_eleccion_id'])
    if not tipo_eleccion or not tipo_eleccion.activo:
        raise ValueError('Tipo de elección no válido')
    
    for voto in data['votos_partidos']:
        partido = Partido.query.get(voto['partido_id'])
        if not partido or not partido.activo:
            raise ValueError(f'Partido {voto["partido_id"]} no válido')
```

---

## 📊 Impacto en Reportes y Estadísticas

### Datos Históricos

**Importante:** Desactivar un elemento NO elimina los datos históricos.

```
Ejemplo:
- Tienes 100 formularios con votos para "Centro Democrático"
- Desactivas "Centro Democrático"
- Los 100 formularios siguen en la BD
- Los reportes históricos siguen mostrando esos votos
- Pero NO se pueden registrar nuevos votos para ese partido
```

### Reportes en Tiempo Real

Los reportes y dashboards muestran:
- ✅ Datos históricos de elementos desactivados
- ✅ Indicador visual de elementos desactivados
- ✅ Filtros para incluir/excluir desactivados

```javascript
// Ejemplo: Dashboard de monitoreo
const formularios = await getFormularios();
// Muestra todos los formularios, incluso con partidos desactivados
// Pero marca visualmente los partidos desactivados
```

---

## 🔧 Casos de Uso Comunes

### 1. Preparar Sistema para Día de Elecciones

```
✅ Activar solo tipos de elección del día
✅ Activar solo candidatos participantes
✅ Activar solo partidos participantes
✅ Activar solo ubicaciones donde hay votación
✅ Activar solo usuarios asignados
```

### 2. Pruebas y Testing

```
✅ Crear usuarios de prueba
✅ Activar solo un departamento pequeño
✅ Activar solo un tipo de elección
✅ Realizar pruebas
✅ Desactivar usuarios de prueba después
```

### 3. Elecciones Parciales

```
✅ Activar solo departamentos con elecciones
✅ Activar solo tipos de elección correspondientes
✅ Desactivar ubicaciones sin elecciones
```

### 4. Mantenimiento Post-Elecciones

```
✅ Desactivar todos los usuarios temporales
✅ Mantener datos históricos
✅ Preparar para próximas elecciones
```

---

## 📝 Mejores Prácticas

### ✅ Hacer

1. **Planificar antes de activar**
   - Revisar qué tipos de elección se necesitan
   - Verificar candidatos y partidos
   - Confirmar ubicaciones

2. **Probar en ambiente de desarrollo**
   - Activar/desactivar elementos
   - Verificar que formularios funcionen
   - Confirmar que reportes sean correctos

3. **Documentar cambios**
   - Registrar qué se activó/desactivó
   - Anotar fecha y razón
   - Mantener historial

4. **Comunicar a coordinadores**
   - Informar qué está activo
   - Explicar limitaciones
   - Dar soporte si hay dudas

### ❌ Evitar

1. **NO eliminar datos**
   - Usar desactivar en lugar de eliminar
   - Mantener datos históricos
   - Permite reactivar si es necesario

2. **NO desactivar durante votación**
   - Planificar cambios antes o después
   - Evitar interrumpir proceso
   - Coordinar con equipo

3. **NO desactivar sin avisar**
   - Comunicar cambios
   - Dar tiempo de preparación
   - Explicar razones

---

## 🆘 Solución de Problemas

### Problema: "No aparecen partidos en formulario"

**Causa:** Partidos desactivados

**Solución:**
1. Super Admin → Partidos
2. Verificar que partidos necesarios estén activos
3. Activar partidos requeridos
4. Refrescar formulario

### Problema: "Testigo no puede hacer login"

**Causa:** Usuario o ubicación desactivados

**Solución:**
1. Super Admin → Usuarios
2. Verificar que usuario esté activo
3. Verificar que ubicación asignada esté activa
4. Activar si es necesario

### Problema: "No aparece tipo de elección"

**Causa:** Tipo de elección desactivado

**Solución:**
1. Super Admin → Tipos de Elección
2. Verificar que tipo esté activo
3. Activar tipo requerido
4. Refrescar formulario

---

## 📚 Referencias

### Modelos de Base de Datos

- `backend/models/configuracion_electoral.py` - Partidos, Candidatos, Tipos de Elección
- `backend/models/location.py` - Ubicaciones
- `backend/models/user.py` - Usuarios

### Endpoints Relacionados

- `backend/routes/locations.py` - Endpoints de ubicaciones
- `backend/routes/super_admin.py` - Panel de Super Admin
- `backend/routes/testigo.py` - Endpoints de testigos

### Documentación Adicional

- `docs/GUIA_COMPLETA_MONITOREO.md` - Guía del sistema de monitoreo
- `docs/INICIALIZACION_AUTOMATICA.md` - Datos iniciales del sistema

---

**Versión**: 1.0  
**Fecha**: 28 de Noviembre 2025  
**Autor**: Equipo de Desarrollo  
**Estado**: ✅ DOCUMENTADO
