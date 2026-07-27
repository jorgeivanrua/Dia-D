# Guía de Pruebas Manuales - Sistema Electoral

## 🔑 Credenciales de Prueba

### Super Admin
- **Usuario**: `admin`
- **Password**: `admin123`
- **Dashboard**: https://dia-d.onrender.com/admin/super-admin

### Admin Departamental
- **Usuario**: `admin_caqueta`
- **Password**: `admin123`
- **Dashboard**: https://dia-d.onrender.com/admin/departamental

### Admin Municipal
- **Usuario**: `admin_florencia`
- **Password**: `admin123`
- **Dashboard**: https://dia-d.onrender.com/admin/municipal

### Coordinador Departamental
- **Usuario**: `coord_dpto_caqueta`
- **Password**: `coord123`
- **Dashboard**: https://dia-d.onrender.com/coordinador/departamental

### Coordinador Municipal
- **Usuario**: `coord_mun_florencia`
- **Password**: `coord123`
- **Dashboard**: https://dia-d.onrender.com/coordinador/municipal

### Coordinador de Puesto
- **Usuario**: `coord_puesto_01`
- **Password**: `coord123`
- **Dashboard**: https://dia-d.onrender.com/coordinador/puesto

### Testigo Electoral
- **Usuario**: `testigo_01_1`
- **Password**: `testigo123`
- **Dashboard**: https://dia-d.onrender.com/testigo/dashboard

### Auditor Electoral
- **Usuario**: `auditor_caqueta`
- **Password**: `auditor123`
- **Dashboard**: https://dia-d.onrender.com/auditor/dashboard

---

## 📋 CHECKLIST DE PRUEBAS

### 1️⃣ SUPER ADMIN

#### Login y Navegación
- [ ] Login con credenciales correctas → Redirige a dashboard
- [ ] Dashboard carga sin errores en consola
- [ ] No hay errores 500 en Network tab
- [ ] Logout funciona correctamente

#### Estadísticas
- [ ] Total de usuarios muestra 26
- [ ] Total de puestos muestra número correcto
- [ ] Total de mesas muestra número correcto
- [ ] Gráficos se renderizan correctamente

#### Gestión de Usuarios
- [ ] Tabla muestra los 26 usuarios
- [ ] Filtro por rol funciona
- [ ] Filtro por estado funciona
- [ ] Búsqueda por nombre funciona
- [ ] Botón "Crear Usuario" abre modal
- [ ] Crear usuario funciona
- [ ] Resetear contraseña funciona
- [ ] Activar/Desactivar usuario funciona
- [ ] Botón "Editar" muestra mensaje (en desarrollo)

#### Configuración Electoral
- [ ] Tab "Partidos" muestra 10 partidos
- [ ] Tab "Tipos de Elección" muestra 11 tipos
- [ ] Tab "Candidatos" muestra 29 candidatos
- [ ] Colores de partidos se muestran correctamente

#### Sistema
- [ ] Estado de salud muestra métricas
- [ ] CPU y memoria se actualizan
- [ ] Actividad reciente muestra mensaje "en desarrollo"

---

### 2️⃣ TESTIGO ELECTORAL

#### Login y Navegación
- [ ] Login con credenciales correctas → Redirige a dashboard
- [ ] Dashboard carga sin errores
- [ ] Botón "Nuevo Formulario" está deshabilitado inicialmente

#### Verificación de Presencia
- [ ] Dropdown de mesas carga correctamente
- [ ] Seleccionar mesa habilita botón "Verificar Presencia"
- [ ] Click en "Verificar Presencia" solicita geolocalización
- [ ] Mensaje de éxito aparece
- [ ] Botón "Nuevo Formulario" se habilita
- [ ] NO hay llamadas automáticas a /api/verificacion/presencia

#### Formularios E-14
- [ ] Click en "Nuevo Formulario" abre modal
- [ ] Seleccionar tipo de elección carga candidatos
- [ ] Ingresar votos funciona
- [ ] Validación de votos funciona
- [ ] Subir foto funciona
- [ ] Guardar como borrador funciona
- [ ] Enviar formulario funciona
- [ ] Formulario aparece en la lista

#### Incidentes
- [ ] Botón "Reportar Incidente" abre modal
- [ ] Tipos de incidentes cargan
- [ ] Enviar incidente funciona
- [ ] Incidente aparece en la lista

#### Delitos
- [ ] Botón "Reportar Delito" abre modal
- [ ] Tipos de delitos cargan
- [ ] Enviar delito funciona
- [ ] Delito aparece en la lista

---

### 3️⃣ COORDINADOR DE PUESTO

#### Login y Navegación
- [ ] Login con credenciales correctas → Redirige a dashboard
- [ ] Dashboard carga sin errores

#### Monitoreo de Mesas
- [ ] Tabla muestra mesas del puesto
- [ ] Estado de cada mesa es correcto
- [ ] Testigos asignados se muestran
- [ ] Formularios por mesa se muestran

#### Gestión de Formularios
- [ ] Tabla muestra formularios del puesto
- [ ] Filtro por estado funciona
- [ ] Click en formulario abre detalles
- [ ] Botón "Validar" funciona
- [ ] Botón "Rechazar" funciona
- [ ] Estado se actualiza correctamente

#### Equipo
- [ ] Tabla muestra testigos del puesto
- [ ] Estado de presencia es correcto
- [ ] Última actividad se muestra

---

### 4️⃣ COORDINADOR MUNICIPAL

#### Login y Navegación
- [ ] Login con credenciales correctas → Redirige a dashboard
- [ ] Dashboard carga sin errores

#### Monitoreo de Puestos
- [ ] Tabla muestra puestos del municipio
- [ ] Estado de cada puesto es correcto
- [ ] Avance por puesto se muestra

#### Estadísticas
- [ ] Total de mesas es correcto
- [ ] Formularios recibidos es correcto
- [ ] Formularios validados es correcto
- [ ] Gráficos se renderizan

#### Equipo
- [ ] Tabla muestra coordinadores de puesto
- [ ] Tabla muestra testigos del municipio
- [ ] Estado de presencia es correcto

---

### 5️⃣ COORDINADOR DEPARTAMENTAL

#### Login y Navegación
- [ ] Login con credenciales correctas → Redirige a dashboard
- [ ] Dashboard carga sin errores

#### Monitoreo de Municipios
- [ ] Tabla muestra municipios del departamento
- [ ] Estado de cada municipio es correcto
- [ ] Avance por municipio se muestra

#### Estadísticas
- [ ] Total de puestos es correcto
- [ ] Total de mesas es correcto
- [ ] Formularios recibidos es correcto
- [ ] Gráficos se renderizan

---

### 6️⃣ AUDITOR ELECTORAL

#### Login y Navegación
- [ ] Login con credenciales correctas → Redirige a dashboard
- [ ] Dashboard carga sin errores

#### Auditoría de Formularios
- [ ] Tabla muestra todos los formularios
- [ ] Filtro por estado funciona
- [ ] Filtro por ubicación funciona
- [ ] Click en formulario abre detalles

#### Reportes
- [ ] Botón "Generar Reporte" funciona
- [ ] Exportar datos funciona
- [ ] Estadísticas de auditoría se muestran

#### Incidentes y Delitos
- [ ] Tabla muestra todos los incidentes
- [ ] Tabla muestra todos los delitos
- [ ] Filtros funcionan

---

## 🔍 VERIFICACIÓN DE ERRORES

### Para cada rol, verificar en DevTools:

#### Console Tab
- [ ] No hay errores rojos
- [ ] No hay warnings críticos
- [ ] Logs de depuración son claros

#### Network Tab
- [ ] No hay errores 500
- [ ] No hay errores 404
- [ ] No hay errores 403 (excepto al intentar acceder a recursos no autorizados)
- [ ] Tiempos de respuesta son razonables (<2 segundos)

#### Application Tab
- [ ] Token se guarda en localStorage
- [ ] sessionStorage se usa correctamente
- [ ] No hay datos sensibles expuestos

---

## 🐛 REPORTE DE BUGS

### Formato de Reporte

```
**Rol**: [Nombre del rol]
**Funcionalidad**: [Qué estabas haciendo]
**Pasos para Reproducir**:
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

**Resultado Esperado**: [Qué debería pasar]
**Resultado Actual**: [Qué pasó realmente]
**Severidad**: [Crítico / Alto / Medio / Bajo]
**Logs de Consola**: [Copiar errores de consola]
**Screenshot**: [Si es posible]
```

### Ejemplo

```
**Rol**: Testigo Electoral
**Funcionalidad**: Crear formulario E-14
**Pasos para Reproducir**:
1. Login como testigo
2. Seleccionar mesa
3. Verificar presencia
4. Click en "Nuevo Formulario"
5. Llenar datos
6. Click en "Enviar"

**Resultado Esperado**: Formulario se envía y aparece en la lista
**Resultado Actual**: Error 500 en consola
**Severidad**: Crítico
**Logs de Consola**: 
```
POST /api/testigo/formularios 500 Internal Server Error
Error: Cannot read property 'id' of undefined
```
```

---

## 📊 MATRIZ DE PRUEBAS

| Funcionalidad | Super Admin | Testigo | Coord. Puesto | Coord. Municipal | Coord. Dpto | Auditor |
|---------------|-------------|---------|---------------|------------------|-------------|---------|
| Login | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| Dashboard carga | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| Estadísticas | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| Crear formulario | N/A | ⬜ | N/A | N/A | N/A | N/A |
| Validar formulario | N/A | N/A | ⬜ | ⬜ | ⬜ | N/A |
| Ver formularios | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| Reportar incidente | N/A | ⬜ | ⬜ | ⬜ | ⬜ | N/A |
| Ver incidentes | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| Gestionar usuarios | ⬜ | N/A | N/A | N/A | N/A | N/A |
| Ver equipo | N/A | N/A | ⬜ | ⬜ | ⬜ | ⬜ |
| Logout | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

**Leyenda**:
- ⬜ Pendiente de probar
- ✅ Probado y funciona
- ❌ Probado y falla
- N/A No aplica para este rol

---

## 🚀 SCRIPT DE PRUEBAS AUTOMATIZADO

Para ejecutar pruebas automatizadas:

```bash
python test_all_roles.py
```

Este script probará:
- Login de cada rol
- Obtención de perfil
- Endpoints principales
- Generará un reporte de resultados

---

**Fecha**: 22 de Noviembre de 2025  
**Versión**: 1.0  
**Estado**: Listo para pruebas
