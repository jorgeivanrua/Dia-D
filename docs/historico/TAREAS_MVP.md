# Plan de Tareas - MVP

## Sprint 1: Autenticación y Base de Datos (Semana 1)

### Día 1-2: Configuración Inicial
- [x] Configurar entorno virtual Python
- [x] Instalar dependencias (Flask, SQLAlchemy, JWT, etc.)
- [x] Configurar estructura de proyecto
- [x] Crear configuraciones por ambiente (dev/prod/test)
- [x] Configurar base de datos SQLite
- [x] Configurar Flask-Migrate

### Día 3-4: Modelos Base
- [x] Crear BaseModel con campos comunes
- [x] Crear modelo User con roles
- [x] Crear modelo Location con jerarquía DIVIPOLA
- [x] Crear enums (UserRole, LocationType, FormStatus)
- [x] Generar migraciones iniciales
- [ ] Crear script init_mvp_db.py

### Día 5: Autenticación
- [x] Implementar AuthService
- [x] Crear endpoints de login/logout
- [x] Implementar generación de JWT tokens
- [x] Crear decoradores de autorización
- [ ] Tests unitarios de autenticación

---

## Sprint 2: Gestión de Usuarios y Ubicaciones (Semana 2)

### Día 1-2: CRUD de Usuarios
- [x] Endpoint GET /api/auth/users (listar)
- [x] Endpoint POST /api/auth/users (crear)
- [x] Endpoint PUT /api/auth/users/:id (actualizar)
- [x] Endpoint POST /api/auth/users/:id/deactivate
- [x] Validaciones de datos de usuario
- [ ] Tests de CRUD usuarios

### Día 3-4: Carga de DIVIPOLA
- [x] Crear script load_divipola.py
- [x] Cargar departamentos desde CSV
- [x] Cargar municipios desde CSV
- [x] Cargar puestos y mesas (datos de prueba)
- [x] Endpoints de consulta de ubicaciones
- [ ] Tests de jerarquía DIVIPOLA

### Día 5: Datos de Prueba
- [ ] Script load_sample_data.py
- [ ] Crear usuarios de prueba (admin, coordinadores, testigos)
- [ ] Asignar ubicaciones a usuarios
- [ ] Verificar permisos por rol
- [ ] Documentar credenciales de prueba

---

## Sprint 3: Formularios E-14 (Semana 3)

### Día 1-2: Modelo y Validaciones
- [x] Crear modelo FormE14
- [x] Crear modelo FormE14History
- [ ] Implementar ValidationService
- [ ] Validación: total_votos ≤ votantes_registrados
- [ ] Validación: suma de votos = total_votos
- [ ] Validación: unicidad por mesa
- [ ] Tests de validaciones

### Día 3-4: CRUD de E-14
- [ ] Endpoint POST /api/e14/forms (crear)
- [ ] Endpoint GET /api/e14/forms (listar con filtros)
- [ ] Endpoint GET /api/e14/forms/:id (detalle)
- [ ] Endpoint PUT /api/e14/forms/:id (actualizar)
- [ ] Endpoint POST /api/e14/forms/:id/submit
- [ ] Control de acceso por rol
- [ ] Tests de CRUD E-14

### Día 5: Upload de Fotos
- [ ] Configurar carpeta de uploads
- [ ] Endpoint POST /api/e14/forms/:id/upload-photo
- [ ] Validar tipo y tamaño de archivo
- [ ] Optimizar imagen con Pillow
- [ ] Guardar URL en formulario
- [ ] Tests de upload

---

## Sprint 4: Aprobación y Dashboards (Semana 4)

### Día 1-2: Flujo de Aprobación
- [ ] Endpoint POST /api/e14/forms/:id/approve
- [ ] Endpoint POST /api/e14/forms/:id/reject
- [ ] Validar permisos de coordinador
- [ ] Registrar en FormE14History
- [ ] Notificar cambio de estado
- [ ] Tests de aprobación/rechazo

### Día 3: Dashboard Coordinador
- [ ] Endpoint GET /api/coordination/dashboard
- [ ] Contar formularios pendientes
- [ ] Listar formularios por aprobar
- [ ] Estadísticas del día
- [ ] Tests de dashboard coordinador

### Día 4: Dashboard Admin
- [ ] Endpoint GET /api/admin/stats
- [ ] Estadísticas generales del sistema
- [ ] Usuarios activos
- [ ] Formularios por estado
- [ ] Actividad reciente
- [ ] Tests de dashboard admin

### Día 5: Integración y Testing
- [ ] Tests de integración end-to-end
- [ ] Verificar flujo completo testigo→coordinador
- [ ] Verificar permisos por rol
- [ ] Corregir bugs encontrados
- [ ] Documentar API

---

## Sprint 5: Frontend Básico (Semana 5)

### Día 1: Página de Login
- [ ] Crear template login.html
- [ ] Formulario de login con validación
- [ ] Manejo de errores
- [ ] Guardar tokens en localStorage
- [ ] Redirección según rol

### Día 2: Dashboard Testigo
- [ ] Template dashboard_testigo.html
- [ ] Listar mis formularios E-14
- [ ] Botón "Crear nuevo E-14"
- [ ] Ver estado de formularios
- [ ] Filtros básicos

### Día 3: Formulario E-14
- [ ] Template form_e14.html
- [ ] Campos de captura de datos
- [ ] Validación en tiempo real
- [ ] Upload de foto
- [ ] Botón enviar
- [ ] Mensajes de éxito/error

### Día 4: Dashboard Coordinador
- [ ] Template dashboard_coordinador.html
- [ ] Listar formularios pendientes
- [ ] Ver detalle de E-14
- [ ] Botones aprobar/rechazar
- [ ] Modal de justificación
- [ ] Actualización en tiempo real

### Día 5: Dashboard Admin
- [ ] Template dashboard_admin.html
- [ ] Estadísticas generales
- [ ] Gráficos básicos
- [ ] Lista de usuarios
- [ ] Botón crear usuario
- [ ] Modal de creación de usuario

---

## Sprint 6: Refinamiento y Despliegue (Semana 6)

### Día 1-2: Mejoras de UX
- [ ] Diseño responsive
- [ ] Mensajes de feedback claros
- [ ] Loading states
- [ ] Manejo de errores amigable
- [ ] Validación de formularios
- [ ] Accesibilidad básica

### Día 3: Optimización
- [ ] Optimizar queries de base de datos
- [ ] Agregar índices necesarios
- [ ] Cachear datos estáticos
- [ ] Comprimir respuestas JSON
- [ ] Optimizar carga de imágenes

### Día 4: Documentación
- [ ] Documentar API con ejemplos
- [ ] Guía de instalación
- [ ] Guía de uso por rol
- [ ] Troubleshooting común
- [ ] README completo

### Día 5: Despliegue
- [ ] Configurar variables de entorno producción
- [ ] Migrar a PostgreSQL
- [ ] Configurar Gunicorn
- [ ] Configurar Nginx (opcional)
- [ ] Backup de base de datos
- [ ] Monitoreo básico

---

## Checklist de Entrega MVP

### Funcionalidades Core
- [ ] Login/Logout funcional
- [ ] Gestión de usuarios (admin)
- [ ] Carga de DIVIPOLA completa
- [ ] Captura de E-14 por testigos
- [ ] Validaciones automáticas
- [ ] Aprobación/Rechazo por coordinadores
- [ ] Dashboards por rol

### Calidad
- [ ] Tests unitarios > 70% cobertura
- [ ] Tests de integración principales flujos
- [ ] Sin errores críticos
- [ ] Validación de seguridad básica
- [ ] Logs configurados

### Documentación
- [ ] README con instrucciones
- [ ] Documentación de API
- [ ] Guía de usuario por rol
- [ ] Datos de prueba documentados

### Despliegue
- [ ] Aplicación desplegada
- [ ] Base de datos configurada
- [ ] Backup automático
- [ ] Monitoreo básico

---

## Estimación de Esfuerzo

| Sprint | Días | Horas | Complejidad |
|--------|------|-------|-------------|
| Sprint 1 | 5 | 40h | Media |
| Sprint 2 | 5 | 40h | Media |
| Sprint 3 | 5 | 40h | Alta |
| Sprint 4 | 5 | 40h | Alta |
| Sprint 5 | 5 | 40h | Media |
| Sprint 6 | 5 | 40h | Baja |
| **Total** | **30 días** | **240h** | **6 semanas** |

---

## Riesgos y Mitigación

### Riesgo 1: Validaciones complejas de E-14
**Impacto**: Alto
**Probabilidad**: Media
**Mitigación**: Crear suite completa de tests, validar con datos reales

### Riesgo 2: Carga de datos DIVIPOLA incompleta
**Impacto**: Alto
**Probabilidad**: Baja
**Mitigación**: Validar datos fuente, crear script de verificación

### Riesgo 3: Problemas de permisos por rol
**Impacto**: Alto
**Probabilidad**: Media
**Mitigación**: Tests exhaustivos de autorización, matriz de permisos clara

### Riesgo 4: Upload de imágenes pesadas
**Impacto**: Medio
**Probabilidad**: Alta
**Mitigación**: Validar tamaño, comprimir automáticamente, límite de 5MB

### Riesgo 5: Rendimiento con muchos formularios
**Impacto**: Medio
**Probabilidad**: Media
**Mitigación**: Paginación, índices en BD, cacheo de consultas frecuentes

---

## Dependencias Externas

- Python 3.9+
- Flask 2.3.3
- SQLAlchemy 2.0.23
- PostgreSQL (producción)
- Servidor web (Nginx/Apache)
- Certificado SSL

---

## Criterios de Éxito

1. ✅ Usuario testigo puede capturar E-14 en < 3 minutos
2. ✅ Coordinador puede aprobar E-14 en < 1 minuto
3. ✅ Sistema valida datos correctamente 100% de casos
4. ✅ Sin errores críticos en flujo principal
5. ✅ Tiempo de respuesta API < 2 segundos
6. ✅ Sistema soporta 100 usuarios simultáneos
7. ✅ Interfaz funciona en móvil y desktop
8. ✅ Documentación completa y clara

---

## Próximos Pasos Post-MVP

1. Implementar formularios E-24
2. Sistema de detección de discrepancias
3. Alertas automáticas
4. Coordinadores municipales y departamentales
5. Auditoría completa
6. Reportes avanzados
7. Exportación de datos
8. App móvil nativa
9. Integración con sistemas externos
10. Dashboard de visualización en tiempo real
