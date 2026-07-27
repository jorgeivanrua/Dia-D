# ✅ Checklist de Funcionalidades por Rol

## 🎯 Objetivo
Verificar que todas las funcionalidades de cada rol funcionen correctamente tanto en local como en Render.

---

## 🔐 Autenticación (Todos los Roles)

### Login
- [ ] Página de login se carga correctamente
- [ ] Login con credenciales válidas funciona
- [ ] Login con credenciales inválidas muestra error
- [ ] Mensaje de error es claro y específico
- [ ] Redirección al dashboard correcto según rol

### Sesión
- [ ] Token JWT se genera correctamente
- [ ] Token se almacena en localStorage
- [ ] Sesión persiste al recargar página
- [ ] Logout funciona correctamente
- [ ] Logout limpia el token

### Seguridad
- [ ] Rutas protegidas requieren autenticación
- [ ] Usuarios no pueden acceder a rutas de otros roles
- [ ] Tokens expirados redirigen al login

---

## 👑 Super Administrador

### Dashboard
- [ ] Dashboard se carga sin errores
- [ ] Estadísticas generales se muestran correctamente
- [ ] Gráficos y métricas funcionan

### Gestión de Usuarios
- [ ] Lista de usuarios se carga
- [ ] Puede crear nuevos usuarios
- [ ] Puede editar usuarios existentes
- [ ] Puede cambiar contraseñas
- [ ] Puede activar/desactivar usuarios
- [ ] Puede asignar ubicaciones
- [ ] Filtros por rol funcionan

### Configuración del Sistema
- [ ] Puede acceder a configuración
- [ ] Puede cambiar tema/colores
- [ ] Puede subir logo
- [ ] Puede configurar fondos de login
- [ ] Cambios se aplican inmediatamente

### Configuración Electoral
- [ ] Puede gestionar tipos de elección
- [ ] Puede gestionar partidos políticos
- [ ] Puede gestionar candidatos
- [ ] Puede gestionar coaliciones

### Reportes
- [ ] Puede ver reportes generales
- [ ] Puede exportar datos
- [ ] Puede ver estadísticas por departamento/municipio

---

## 📊 Coordinador Departamental

### Dashboard
- [ ] Dashboard se carga sin errores
- [ ] Estadísticas del departamento se muestran
- [ ] Puede ver formularios de su departamento

### Gestión de Formularios
- [ ] Lista de formularios E-14 se carga
- [ ] Puede ver detalles de formularios
- [ ] Puede validar formularios
- [ ] Puede rechazar formularios con observaciones
- [ ] Filtros por estado funcionan
- [ ] Filtros por municipio funcionan

### Reportes Departamentales
- [ ] Puede ver consolidado departamental
- [ ] Puede ver progreso por municipio
- [ ] Puede ver estadísticas de votación

---

## 🏛️ Coordinador Municipal

### Dashboard
- [ ] Dashboard se carga sin errores
- [ ] Estadísticas del municipio se muestran
- [ ] Puede ver formularios de su municipio

### Gestión de Formularios
- [ ] Lista de formularios E-14 se carga
- [ ] Puede ver detalles de formularios
- [ ] Puede validar formularios
- [ ] Puede rechazar formularios
- [ ] Filtros por puesto funcionan

### Reportes Municipales
- [ ] Puede ver consolidado municipal
- [ ] Puede ver progreso por puesto
- [ ] Puede ver estadísticas de votación

---

## 📍 Coordinador de Puesto

### Dashboard
- [ ] Dashboard se carga sin errores
- [ ] Estadísticas del puesto se muestran
- [ ] Puede ver formularios de su puesto

### Gestión de Formularios
- [ ] Lista de formularios E-14 se carga
- [ ] Puede ver detalles de formularios
- [ ] Puede validar formularios
- [ ] Puede rechazar formularios
- [ ] Puede ver todas las mesas del puesto

### Gestión de Testigos
- [ ] Puede ver testigos asignados
- [ ] Puede verificar presencia de testigos
- [ ] Puede ver estado de cobertura de mesas

---

## 🗳️ Testigo Electoral

### Dashboard
- [ ] Dashboard se carga sin errores
- [ ] Panel de estadísticas se muestra
- [ ] Selector de mesa funciona
- [ ] Panel de mesas del puesto se muestra

### Verificación de Presencia
- [ ] Botón de verificar presencia funciona
- [ ] Geolocalización se captura correctamente
- [ ] Mensaje de confirmación se muestra
- [ ] Botón "Nuevo Formulario" se habilita

### Formulario E-14

#### Información Básica
- [ ] Selector de mesa funciona
- [ ] Selector de tipo de elección funciona
- [ ] Puede cambiar de mesa si cubre varias

#### Captura de Imagen
- [ ] Botón de tomar foto funciona
- [ ] Puede seleccionar imagen de galería
- [ ] Preview de imagen se muestra
- [ ] Imagen se sube correctamente

#### Datos de Votación
- [ ] Votantes registrados se cargan automáticamente
- [ ] Puede ingresar votos nulos
- [ ] Puede ingresar votos en blanco
- [ ] Puede ingresar tarjetas no marcadas
- [ ] Totales se calculan automáticamente

#### Votos por Partido
- [ ] Partidos se cargan correctamente
- [ ] Candidatos se cargan por tipo de elección
- [ ] Puede ingresar votos por partido
- [ ] Puede ingresar votos por candidato
- [ ] Totales por partido se calculan
- [ ] Partido ganador se muestra

#### Guardado
- [ ] Puede guardar como borrador
- [ ] Puede enviar para revisión
- [ ] Validaciones funcionan correctamente
- [ ] Mensajes de error son claros

### Gestión de Formularios
- [ ] Lista de formularios se muestra
- [ ] Puede ver formularios propios
- [ ] Puede editar borradores
- [ ] Puede ver estado de formularios
- [ ] Indicadores de estado son claros

### Sincronización Offline
- [ ] Borradores se guardan localmente
- [ ] Sincronización automática funciona
- [ ] Indicador de sincronización se muestra
- [ ] Conflictos se manejan correctamente

### Incidentes y Delitos
- [ ] Puede reportar incidentes
- [ ] Puede reportar delitos
- [ ] Formularios de reporte funcionan
- [ ] Reportes se envían correctamente

---

## 🔍 Auditor Electoral

### Dashboard
- [ ] Dashboard se carga sin errores
- [ ] Puede ver todos los formularios
- [ ] Puede ver estadísticas generales

### Auditoría
- [ ] Puede ver detalles completos de formularios
- [ ] Puede ver historial de cambios
- [ ] Puede ver quién validó/rechazó
- [ ] Puede generar reportes de auditoría

### Reportes
- [ ] Puede ver inconsistencias
- [ ] Puede ver formularios rechazados
- [ ] Puede exportar datos para análisis

---

## 🌐 Funcionalidades Generales

### Responsive Design
- [ ] Funciona en desktop (1920x1080)
- [ ] Funciona en tablet (768x1024)
- [ ] Funciona en móvil (375x667)
- [ ] Menús se adaptan correctamente
- [ ] Tablas son scrolleables en móvil

### Performance
- [ ] Páginas cargan en menos de 3 segundos
- [ ] Imágenes se optimizan automáticamente
- [ ] No hay memory leaks en JavaScript
- [ ] Consultas a BD son eficientes

### Accesibilidad
- [ ] Contraste de colores es adecuado
- [ ] Textos son legibles
- [ ] Botones tienen tamaño adecuado
- [ ] Formularios tienen labels claros

### Manejo de Errores
- [ ] Errores de red se manejan gracefully
- [ ] Mensajes de error son claros
- [ ] Usuario puede recuperarse de errores
- [ ] Logs se registran correctamente

---

## 🚀 Despliegue en Render

### Configuración
- [ ] render.yaml está configurado correctamente
- [ ] Variables de entorno están definidas
- [ ] Base de datos está configurada
- [ ] Dominio está configurado (si aplica)

### Build
- [ ] Build se completa sin errores
- [ ] Dependencias se instalan correctamente
- [ ] Migraciones se ejecutan automáticamente
- [ ] Usuarios se crean automáticamente

### Runtime
- [ ] Aplicación inicia correctamente
- [ ] Health checks pasan
- [ ] Logs son accesibles
- [ ] No hay errores en producción

### Funcionalidad
- [ ] Login funciona en producción
- [ ] Todas las rutas son accesibles
- [ ] Imágenes se cargan correctamente
- [ ] API responde correctamente

---

## 📝 Notas de Prueba

### Ambiente Local
**Fecha:** ___________
**Probado por:** ___________
**Resultado:** ⬜ Aprobado ⬜ Con observaciones ⬜ Rechazado

**Observaciones:**
```
[Escribe aquí las observaciones]
```

### Ambiente Render
**Fecha:** ___________
**URL:** ___________
**Probado por:** ___________
**Resultado:** ⬜ Aprobado ⬜ Con observaciones ⬜ Rechazado

**Observaciones:**
```
[Escribe aquí las observaciones]
```

---

## 🔧 Problemas Conocidos

### Críticos (Bloquean funcionalidad)
- [ ] Ninguno identificado

### Mayores (Afectan experiencia)
- [ ] Ninguno identificado

### Menores (Mejoras deseables)
- [ ] Ninguno identificado

---

## ✅ Criterios de Aceptación

Para considerar el sistema listo para producción:

1. **Funcionalidad:** ≥ 95% de funcionalidades operativas
2. **Performance:** Tiempo de carga < 3 segundos
3. **Seguridad:** Sin vulnerabilidades críticas
4. **Estabilidad:** Sin errores críticos en 24 horas de prueba
5. **Usabilidad:** Feedback positivo de usuarios de prueba

---

**Última actualización:** Noviembre 22, 2025
**Versión:** 1.0
