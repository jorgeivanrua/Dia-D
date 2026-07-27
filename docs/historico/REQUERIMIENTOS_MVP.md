# Requerimientos Funcionales - MVP

## 1. Objetivo del MVP

Implementar un sistema funcional mínimo que permita:
- Autenticación de usuarios con roles básicos
- Captura de formularios E-14 por testigos electorales
- Validación y aprobación de E-14 por coordinadores
- Visualización de datos en dashboards por rol

## 2. Alcance del MVP

### 2.1 Funcionalidades INCLUIDAS

#### Autenticación y Seguridad
- ✅ Login con email/password
- ✅ Generación de tokens JWT
- ✅ Logout y cierre de sesión
- ✅ Cambio de contraseña
- ✅ Bloqueo por intentos fallidos (5 intentos)

#### Gestión de Usuarios
- ✅ Crear usuarios (solo admin)
- ✅ Listar usuarios con filtros
- ✅ Actualizar información de usuario
- ✅ Desactivar usuarios
- ✅ Asignar roles y ubicaciones

#### Roles Básicos
- ✅ **Testigo Electoral**: Captura E-14 de su mesa asignada
- ✅ **Coordinador de Puesto**: Valida E-14 de su puesto
- ✅ **Sistemas/Superadmin**: Administración completa

#### Ubicaciones (DIVIPOLA)
- ✅ Jerarquía: Departamento → Municipio → Zona → Puesto → Mesa
- ✅ Carga de datos DIVIPOLA
- ✅ Consulta de ubicaciones por jerarquía
- ✅ Asignación de usuarios a ubicaciones

#### Formularios E-14
- ✅ Crear formulario E-14
- ✅ Validaciones automáticas:
  - Total votos ≤ Votantes registrados
  - Suma de votos = Total votos
  - Unicidad por mesa
- ✅ Adjuntar foto del formulario físico
- ✅ Estados: Borrador, Enviado, Aprobado, Rechazado
- ✅ Aprobar/Rechazar con justificación
- ✅ Historial de cambios

#### Dashboards
- ✅ **Dashboard Testigo**: Mis formularios E-14
- ✅ **Dashboard Coordinador**: Formularios pendientes de aprobación
- ✅ **Dashboard Admin**: Estadísticas generales del sistema

### 2.2 Funcionalidades EXCLUIDAS (Post-MVP)

- ❌ Formularios E-24
- ❌ Detección automática de discrepancias E-14 vs E-24
- ❌ Sistema de alertas y notificaciones
- ❌ Coordinadores municipales y departamentales
- ❌ Auditoría completa con logs detallados
- ❌ Reportes avanzados y exportación
- ❌ Escalamiento automático de alertas
- ❌ Integración con sistemas externos
- ❌ App móvil nativa

## 3. Requisitos No Funcionales

### 3.1 Rendimiento
- Tiempo de respuesta API < 2 segundos
- Soporte para 100 usuarios simultáneos
- Carga de imágenes < 5MB

### 3.2 Seguridad
- Contraseñas hasheadas con bcrypt
- Tokens JWT con expiración (1 hora access, 7 días refresh)
- Validación de entrada en todos los endpoints
- Control de acceso basado en roles (RBAC)

### 3.3 Usabilidad
- Interfaz responsive (móvil y desktop)
- Mensajes de error claros
- Feedback visual en operaciones

### 3.4 Disponibilidad
- Sistema disponible 24/7 durante jornada electoral
- Backup automático de base de datos

## 4. Casos de Uso Principales

### CU-01: Login de Usuario
**Actor**: Cualquier usuario registrado
**Flujo**:
1. Usuario ingresa los datos segun su ubicacion y contraseña
2. Sistema valida credenciales
3. Sistema genera tokens JWT
4. Usuario es redirigido a su dashboard según rol

### CU-02: Captura de E-14 por Testigo
**Actor**: Testigo Electoral
**Flujo**:
1. Testigo accede a su dashboard
2. Selecciona "Crear nuevo E-14"
3. Ingresa datos del formulario
4. Adjunta foto del formulario físico
5. Sistema valida datos automáticamente
6. Testigo envía formulario
7. Sistema cambia estado a "Enviado"

### CU-03: Validación de E-14 por Coordinador
**Actor**: Coordinador de Puesto
**Flujo**:
1. Coordinador accede a dashboard
2. Ve lista de E-14 pendientes
3. Selecciona un formulario
4. Revisa datos y foto
5. Aprueba o rechaza con justificación
6. Sistema actualiza estado del formulario
7. Sistema registra en historial

### CU-04: Gestión de Usuarios por Admin
**Actor**: Sistemas/Superadmin
**Flujo**:
1. Admin accede a panel de administración
2. Crea nuevo usuario
3. Asigna rol y ubicación
4. Sistema genera contraseña temporal
5. Admin entrega credenciales al usuario

## 5. Validaciones de Negocio

### Formulario E-14
1. **Total Votos ≤ Votantes Registrados**
   - `total_votos <= mesa.total_votantes_registrados`

2. **Suma de Votos = Total Votos**
   - `votos_partido_1 + votos_partido_2 + ... + votos_nulos + votos_no_marcados = total_votos`

3. **Unicidad por Mesa**
   - Solo un E-14 aprobado por mesa

4. **Campos Obligatorios**
   - Mesa asignada
   - Total votos
   - Votos por partido
   - Foto del formulario

### Usuarios
1. **Email único** en el sistema
2. **Contraseña fuerte**: Mínimo 8 caracteres, mayúscula, minúscula, número
3. **Rol válido** según enumeración
4. **Ubicación válida** según jerarquía DIVIPOLA

## 6. Modelo de Datos Simplificado

### Entidades Principales
- **User**: id, nombre, email, password_hash, rol, ubicacion_id, activo
- **Location**: id, departamento_codigo, municipio_codigo, puesto_codigo, mesa_codigo, nombre_completo, tipo, total_votantes_registrados
- **FormE14**: id, mesa_id, testigo_id, total_votos, votos_partido_*, votos_nulos, votos_no_marcados, foto_url, estado, observaciones
- **FormE14History**: id, form_id, usuario_id, accion, estado_anterior, estado_nuevo, justificacion, timestamp

## 7. Criterios de Aceptación

### Sprint 1: Autenticación y Usuarios
- [ ] Usuario puede hacer login con ubicacion/password
- [ ] Sistema genera tokens JWT válidos
- [ ] Admin puede crear usuarios con roles
- [ ] Usuario puede cambiar su contraseña
- [ ] Sistema bloquea después de 5 intentos fallidos

### Sprint 2: Ubicaciones DIVIPOLA
- [ ] Sistema carga datos DIVIPOLA correctamente
- [ ] Jerarquía departamento→municipio→puesto→mesa funciona
- [ ] Usuarios pueden consultar ubicaciones según su rol
- [ ] Admin puede asignar ubicaciones a usuarios

### Sprint 3: Formularios E-14
- [ ] Testigo puede crear E-14 para su mesa
- [ ] Sistema valida datos automáticamente
- [ ] Testigo puede adjuntar foto
- [ ] Coordinador ve E-14 pendientes de su puesto
- [ ] Coordinador puede aprobar/rechazar con justificación
- [ ] Sistema registra historial de cambios

### Sprint 4: Dashboards
- [ ] Dashboard testigo muestra sus E-14
- [ ] Dashboard coordinador muestra pendientes
- [ ] Dashboard admin muestra estadísticas
- [ ] Interfaz responsive funciona en móvil

## 8. Datos de Prueba

### Usuarios
- 1 Superadmin
- 2 Coordinadores de Puesto
- 5 Testigos Electorales

### Ubicaciones
- 2 Departamentos
- 4 Municipios (2 por departamento)
- 4 Puestos (1 por municipio)
- 10 Mesas (2-3 por puesto)

### Formularios
- 5 E-14 en estado "Enviado"
- 3 E-14 en estado "Aprobado"
- 2 E-14 en estado "Rechazado"

## 9. Métricas de Éxito

- ✅ 100% de usuarios pueden hacer login
- ✅ 100% de validaciones funcionan correctamente
- ✅ 0 errores críticos en flujo principal
- ✅ Tiempo de captura E-14 < 3 minutos
- ✅ Tiempo de validación E-14 < 1 minuto
