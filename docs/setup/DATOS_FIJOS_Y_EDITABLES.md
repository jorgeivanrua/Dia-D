# 📋 Datos Fijos y Editables del Sistema

**Fecha**: 29 de Noviembre de 2025  
**Estado**: ✅ CONFIGURADO

---

## 🔒 Datos Fijos (No Editables)

Estos datos están precargados en la base de datos y **NO se pueden modificar** desde la interfaz. Solo se pueden activar/desactivar o usar tal como están.

### 1. Tipos de Elección

**Ubicación en BD**: Tabla `tipos_eleccion`

**Datos fijos**:
- Senado de la República (SENADO)
- Cámara de Representantes (CAMARA)
- Gobernación (GOBERNACION)
- Asamblea Departamental (ASAMBLEA)
- Alcaldía (ALCALDIA)
- Concejo Municipal (CONCEJO)

**Campos fijos**:
- `codigo` - Código único del tipo de elección
- `nombre` - Nombre del tipo de elección
- `descripcion` - Descripción
- `es_uninominal` - Si es uninominal o no
- `permite_lista_cerrada` - Si permite lista cerrada
- `permite_lista_abierta` - Si permite lista abierta
- `permite_coaliciones` - Si permite coaliciones

**Campo editable por Super Admin**:
- `activo` - Activar/desactivar tipo de elección

**Endpoint**:
```
PUT /api/super-admin/tipos-eleccion/{id}/toggle
Body: { "activo": true/false }
```

---

### 2. Ubicaciones DIVIPOLA

**Ubicación en BD**: Tabla `locations`

**Datos fijos**:
- 33 Departamentos
- 1,122 Municipios
- 2,899 Zonas
- 13,405 Puestos
- 19,833 Mesas

**Campos fijos (NO editables)**:
- `departamento_codigo` - Código del departamento
- `municipio_codigo` - Código del municipio
- `zona_codigo` - Código de la zona
- `puesto_codigo` - Código del puesto
- `mesa_codigo` - Código de la mesa
- `departamento_nombre` - Nombre del departamento
- `municipio_nombre` - Nombre del municipio
- `puesto_nombre` - Nombre del puesto
- `mesa_nombre` - Nombre de la mesa
- `nombre_completo` - Nombre completo de la ubicación
- `tipo` - Tipo de ubicación (departamento, municipio, zona, puesto, mesa)

**Campos editables por Super Admin (solo para mesas)**:
- `total_votantes_registrados` - Total de votantes registrados
- `mujeres` - Cantidad de mujeres
- `hombres` - Cantidad de hombres

**Validación**:
- `hombres + mujeres <= total_votantes_registrados`

**Endpoint**:
```
PUT /api/super-admin/locations/mesa/{id}
Body: {
  "total_votantes_registrados": 500,
  "mujeres": 250,
  "hombres": 250
}
```

---

## ✏️ Datos Editables

Estos datos pueden ser creados, editados y eliminados por el Super Admin.

### 1. Partidos Políticos

**Ubicación en BD**: Tabla `partidos`

**Campos editables**:
- `codigo` - Código único del partido
- `nombre` - Nombre completo del partido
- `nombre_corto` - Sigla o nombre corto
- `color` - Color representativo (hex)
- `logo_url` - URL del logo
- `activo` - Activar/desactivar
- `orden` - Orden de visualización

**Endpoints**:
```
GET    /api/super-admin/partidos
POST   /api/super-admin/partidos
PUT    /api/super-admin/partidos/{id}
PUT    /api/super-admin/partidos/{id}/toggle
DELETE /api/super-admin/partidos/{id}
```

---

### 2. Candidatos

**Ubicación en BD**: Tabla `candidatos`

**Campos editables**:
- `codigo` - Código único del candidato
- `nombre_completo` - Nombre completo
- `numero_lista` - Número en la lista
- `partido_id` - ID del partido (FK)
- `tipo_eleccion_id` - ID del tipo de elección (FK)
- `foto_url` - URL de la foto
- `es_independiente` - Si es independiente
- `es_cabeza_lista` - Si es cabeza de lista
- `activo` - Activar/desactivar
- `orden` - Orden de visualización

**Endpoints**:
```
GET    /api/super-admin/candidatos
POST   /api/super-admin/candidatos
PUT    /api/super-admin/candidatos/{id}
PUT    /api/super-admin/candidatos/{id}/toggle
DELETE /api/super-admin/candidatos/{id}
```

---

### 3. Usuarios

**Ubicación en BD**: Tabla `users`

**Campos editables**:
- `nombre` - Nombre de usuario (único)
- `password_hash` - Contraseña (hasheada)
- `rol` - Rol del usuario
- `ubicacion_id` - ID de la ubicación asignada (FK)
- `activo` - Activar/desactivar

**Roles disponibles**:
- `super_admin` - Super Administrador
- `admin_departamental` - Administrador Departamental
- `admin_municipal` - Administrador Municipal
- `coordinador_departamental` - Coordinador Departamental
- `coordinador_municipal` - Coordinador Municipal
- `coordinador_puesto` - Coordinador de Puesto
- `testigo_electoral` - Testigo Electoral
- `auditor_electoral` - Auditor Electoral
- `monitoreo` - Monitoreo en Tiempo Real

**Endpoints**:
```
GET    /api/super-admin/users
POST   /api/super-admin/users
PUT    /api/super-admin/users/{id}
POST   /api/super-admin/users/{id}/reset-password
DELETE /api/super-admin/users/{id}
```

---

### 4. Campañas

**Ubicación en BD**: Tabla `campanas`

**Campos editables**:
- `nombre` - Nombre de la campaña
- `descripcion` - Descripción
- `fecha_inicio` - Fecha de inicio
- `fecha_fin` - Fecha de fin
- `activa` - Si está activa
- `configuracion` - Configuración JSON

**Endpoints**:
```
GET    /api/super-admin/campanas
POST   /api/super-admin/campanas
PUT    /api/super-admin/campanas/{id}
PUT    /api/super-admin/campanas/{id}/activar
POST   /api/super-admin/campanas/{id}/reset
DELETE /api/super-admin/campanas/{id}
```

---

## 📊 Resumen de Permisos

| Entidad | Super Admin | Otros Roles |
|---------|-------------|-------------|
| **Tipos de Elección** | ✅ Activar/Desactivar | 👁️ Solo lectura |
| **DIVIPOLA (Ubicaciones)** | ✅ Editar votantes en mesas | 👁️ Solo lectura |
| **Partidos** | ✅ CRUD completo | 👁️ Solo lectura |
| **Candidatos** | ✅ CRUD completo | 👁️ Solo lectura |
| **Usuarios** | ✅ CRUD completo | ❌ Sin acceso |
| **Campañas** | ✅ CRUD completo | ❌ Sin acceso |
| **Formularios E-14** | 👁️ Solo lectura | ✏️ Crear/Validar según rol |
| **Incidentes** | 👁️ Solo lectura | ✏️ Crear/Gestionar según rol |
| **Delitos** | 👁️ Solo lectura | ✏️ Crear/Gestionar según rol |

---

## 🔐 Seguridad

### Validaciones Implementadas

1. **Tipos de Elección**:
   - No se pueden crear nuevos tipos
   - No se pueden eliminar
   - Solo se puede cambiar el estado activo/inactivo

2. **DIVIPOLA**:
   - No se pueden crear nuevas ubicaciones
   - No se pueden eliminar ubicaciones
   - No se pueden modificar códigos ni nombres
   - Solo se pueden editar votantes en mesas
   - Validación: `hombres + mujeres <= total_votantes`

3. **Partidos**:
   - Código único requerido
   - Nombre único requerido
   - Color en formato hex válido

4. **Candidatos**:
   - Debe estar asociado a un partido o ser independiente
   - Debe estar asociado a un tipo de elección
   - Número de lista único por tipo de elección

5. **Usuarios**:
   - Nombre de usuario único
   - Rol válido requerido
   - Ubicación válida según rol

---

## 📝 Ejemplos de Uso

### Activar/Desactivar Tipo de Elección

```javascript
// Desactivar Senado
await APIClient.put('/super-admin/tipos-eleccion/1/toggle', {
    activo: false
});
```

### Actualizar Votantes de una Mesa

```javascript
// Actualizar votantes de la mesa ID 12345
await APIClient.updateSuperAdminMesa(12345, {
    total_votantes_registrados: 500,
    mujeres: 250,
    hombres: 250
});
```

### Crear un Partido

```javascript
await APIClient.post('/super-admin/partidos', {
    codigo: 'NUEVO',
    nombre: 'Partido Nuevo',
    nombre_corto: 'PN',
    color: '#FF5733',
    activo: true,
    orden: 10
});
```

### Crear un Usuario

```javascript
await APIClient.post('/super-admin/users', {
    nombre: 'testigo2',
    password: 'test123',
    rol: 'testigo_electoral',
    ubicacion_id: 12345,
    activo: true
});
```

---

## 🚀 Próximos Pasos

1. **Interfaz de Edición de Mesas**
   - Crear modal para editar votantes de una mesa
   - Validación en tiempo real
   - Confirmación de cambios

2. **Auditoría de Cambios**
   - Registrar quién modificó qué y cuándo
   - Historial de cambios en mesas
   - Logs de activación/desactivación

3. **Importación Masiva**
   - Importar votantes desde Excel
   - Validación de datos
   - Reporte de errores

4. **Exportación de Datos**
   - Exportar ubicaciones con votantes
   - Exportar configuración electoral
   - Formato Excel/CSV

---

## 📚 Referencias

- `backend/models/location.py` - Modelo de ubicaciones
- `backend/models/configuracion_electoral.py` - Modelos de configuración
- `backend/routes/super_admin.py` - Endpoints de Super Admin
- `frontend/static/js/api-client.js` - Cliente API
- `scripts/inicializar_datos_automatico.py` - Script de inicialización

---

**Documento creado por**: Sistema de Configuración  
**Fecha**: 29 de Noviembre de 2025  
**Versión**: 1.0  
**Estado**: ✅ CONFIGURADO
