# Documentación del Proyecto

Esta carpeta contiene toda la documentación del proyecto organizada por categorías.

## Estructura

### 📁 `/guias`
Guías de uso y referencia:
- Guías de implementación
- Guías de usuario
- Instrucciones de debug
- Checklists
- Troubleshooting
- Inicio rápido

### 📁 `/desarrollo`
Documentación técnica y arquitectura:
- Arquitectura del sistema
- Flujos de datos
- Roles y permisos
- Seguridad
- Sistemas específicos
- Tipos de datos

### 📁 `/setup`
Configuración e instalación:
- Configuración de base de datos
- Datos electorales
- Setup inicial
- Variables de entorno

### 📁 `/sesiones`
Resúmenes de sesiones de trabajo:
- Resúmenes de implementaciones
- Estados de componentes
- Verificaciones realizadas
- Pruebas completadas

### 📁 `/correcciones`
Documentación de correcciones:
- Correcciones de errores
- Soluciones implementadas
- Fixes aplicados

### 📁 `/implementaciones`
Nuevas funcionalidades:
- Implementaciones de features
- Ampliaciones
- Mejoras aplicadas

### 📁 `/optimizaciones`
Optimizaciones realizadas:
- Mejoras de rendimiento
- Optimizaciones de código
- Refactorizaciones

### 📁 `/deployment`
Documentación de despliegue:
- Configuración de Render
- Deploy en producción
- CI/CD

### 📁 `/features`
Documentación de características:
- Features específicas
- Funcionalidades del sistema

### 📁 `/historico`
Documentación histórica:
- Changelogs antiguos
- Documentos de organización
- Archivos de referencia histórica

### 📁 `/testing`
Documentación de pruebas:
- Planes de prueba
- Resultados de testing
- Casos de prueba

### 📁 Raíz de `/docs`
Documentación principal:
- README.md (este archivo)
- INDICE_DOCUMENTACION.md (índice completo)

## Convenciones

### Nombres de Archivos

- **RESUMEN_*.md**: Resúmenes de sesiones o implementaciones completas
- **CORRECCION_*.md**: Documentación de correcciones específicas
- **IMPLEMENTACION_*.md**: Documentación de implementaciones nuevas
- **AMPLIACION_*.md**: Documentación de ampliaciones de funcionalidad
- **OPTIMIZACION_*.md**: Documentación de optimizaciones
- **MEJORAS_*.md**: Documentación de mejoras aplicadas
- **ESTADO_*.md**: Estados actuales de componentes
- **SOLUCION_*.md**: Soluciones a problemas específicos

## Documentos Importantes

### Sesiones Recientes
- `sesiones/RESUMEN_IMPLEMENTACION_FINAL.md` - Última implementación de incidentes/delitos
- `sesiones/RESUMEN_SESION_COORDINADOR_MUNICIPAL.md` - Sesión del coordinador municipal
- `sesiones/RESUMEN_OPTIMIZACION_MOBILE.md` - Optimización móvil

### Implementaciones Clave
- `implementaciones/IMPLEMENTACION_INCIDENTES_DELITOS_MODAL.md` - Modal de incidentes/delitos
- `implementaciones/AMPLIACION_MODAL_INCIDENTES_DELITOS.md` - Ampliación con fotos
- `implementaciones/OPTIMIZACION_MOBILE_TODOS_ROLES.md` - Responsive design

### Correcciones Importantes
- `correcciones/CORRECCION_NAVEGACION_MOVIL.md` - Fix navegación móvil
- `correcciones/CORRECCION_SYNC_MANAGER_ROLES.md` - Fix sync manager
- `correcciones/SOLUCION_ZONA_CODIGO.md` - Solución códigos de zona

## Mantenimiento

Al crear nueva documentación:
1. Usar el prefijo apropiado según el tipo de documento
2. Colocar en la carpeta correspondiente
3. Actualizar este README si es un documento importante
4. Usar formato Markdown consistente
5. Incluir fecha en el documento

## Scripts

Los scripts de prueba y utilidades están en `/scripts`:
- Scripts de prueba: `test_*.py`, `test_*.html`
- Scripts de corrección: `fix_*.py`, `check_*.py`
- Scripts de utilidades: `add_*.py`, `reset_*.py`, etc.
