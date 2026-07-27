# Scripts de Prueba y Verificación

Scripts para probar funcionalidad y verificar el estado del sistema.

## Uso Común

### Verificación Completa del Sistema
```bash
# Verificar todo el sistema
python scripts/test/verificacion_completa_sistema.py

# Check general del sistema
python scripts/test/check_system.py

# Verificar base de datos
python scripts/test/check_db.py
```

### Pruebas de Roles
```bash
# Probar todos los roles
python scripts/test/test_all_roles.py

# Probar usuarios y roles
python scripts/test/test_usuarios_roles.py
```

### Pruebas de Endpoints
```bash
# Endpoints generales
python scripts/test/test_endpoints.py

# Coordinador municipal
python scripts/test/test_coordinador_municipal_endpoints.py

# Monitoreo
python scripts/test/test_monitoreo_endpoint.py
```

## Categorías

### Verificación del Sistema
- `verificacion_completa_sistema.py` - Verificación completa
- `verificar_sistema_completo.py` - Sistema completo
- `check_system.py` - Check general
- `check_db.py` - Base de datos
- `check_db_data.py` - Datos de BD
- `verify_data.py` - Verificar datos

### Diagnóstico
- `diagnostico_sistema.py` - Sistema
- `diagnostico_testigos.py` - Testigos
- `diagnostico_inicializacion.py` - Inicialización

### Pruebas de API
- `test_endpoints.py` - Endpoints generales
- `test_coordinador_municipal_endpoints.py` - Coordinador municipal
- `test_monitoreo_endpoint.py` - Monitoreo
- `test_monitoreo_endpoints.py` - Endpoints de monitoreo
- `test_candidatos_endpoint.py` - Candidatos
- `test_puestos_endpoint.py` - Puestos
- `test_render_endpoints.py` - Render

### Pruebas de Roles
- `test_all_roles.py` - Todos los roles
- `test_usuarios_roles.py` - Usuarios y roles
- `test_login_testigo.py` - Login testigo

### Pruebas de Funcionalidad
- `test_geolocalizacion.py` - Geolocalización
- `test_bulk_upload.py` - Carga masiva
- `test_logos.py` - Logos
- `test_logos_sistema.py` - Sistema de logos
- `test_security_fixes.py` - Fixes de seguridad
- `test_puestos_alertas.py` - Alertas de puestos

### Verificación de Datos
- `verificar_testigos.py` - Testigos
- `verificar_ubicaciones.py` - Ubicaciones
- `verificar_ubicaciones_coordinadores.py` - Ubicaciones coordinadores
- `verificar_votantes_mesas.py` - Votantes por mesa
- `verificar_monitoreo.py` - Monitoreo
- `verificar_passwords.py` - Passwords
- `verificar_roles_jwt.py` - Roles JWT

### Revisión
- `revisar_coordinadores_municipales.py` - Coordinadores municipales
- `ver_estructura_bd.py` - Estructura BD
- `ver_tablas.py` - Tablas
- `ver_codigos_mesa.py` - Códigos de mesa

### Checks Específicos
- `check_logos.py` - Logos
- `check_partidos.py` - Partidos
- `check_monitoreo_user.py` - Usuario monitoreo
- `check_testigo_password.py` - Password testigo
- `check_zona_codigo_bd.py` - Zona código

### HTML de Prueba
- `test_mapa.html` - Mapa
- `test_bottom_nav.html` - Navegación inferior
- `TEST_API_SUPER_ADMIN.html` - API super admin

### Batch Scripts
- `check_system.bat` - Check sistema (Windows)
- `test_optimizations.bat` - Test optimizaciones (Windows)

## Notas

- Ejecutar desde la raíz del proyecto
- Activar entorno virtual: `.venv\Scripts\activate`
- Algunos requieren servidor corriendo
- Los .html abrir en navegador
