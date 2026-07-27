# Scripts del Proyecto

## Estructura Organizada

```
scripts/
├── init/     # Scripts de inicialización y carga de datos
├── test/     # Scripts de prueba y verificación
├── fix/      # Scripts de corrección y reparación
├── utils/    # Scripts de utilidades y herramientas
└── README_*.md  # Documentación
```

## 📁 `/init` - Inicialización y Carga de Datos

Scripts para inicializar la base de datos y cargar datos:

**Inicialización del Sistema**:
- `init_db.py` - Inicializar base de datos
- `init_system.py` - Inicializar sistema completo
- `init_configuracion_electoral.py` - Configuración electoral
- `init_super_admin_data.py` - Datos de super admin
- `init_caqueta_electoral_data.py` - Datos electorales de Caquetá

**Carga de Datos**:
- `load_divipola.py` - Cargar división política
- `load_only_caqueta.py` - Cargar solo Caquetá
- `load_basic_data_simple.py` - Datos básicos
- `load_complete_test_data.py` - Datos completos de prueba
- `cargar_divipola_v2.py` - Cargar DIVIPOLA v2
- `cargar_partidos_2023.py` - Partidos políticos 2023
- `cargar_candidatos_2023.py` - Candidatos 2023
- `cargar_logos_bd.py` - Logos de partidos

**Creación de Usuarios**:
- `crear_testigos_iniciales.py` - Testigos iniciales
- `crear_testigos_prueba.py` - Testigos de prueba
- `crear_testigos_puesto_01.py` - Testigos para puesto 01
- `crear_usuarios_caqueta.py` - Usuarios de Caquetá
- `crear_usuarios_florencia.py` - Usuarios de Florencia
- `crear_usuario_monitoreo.py` - Usuario de monitoreo

**Migraciones y Aplicaciones**:
- `migrate_to_alembic.py` - Migrar a Alembic
- `apply_migration_now.py` - Aplicar migración
- `aplicar_migracion_monitoreo.py` - Migración de monitoreo
- `aplicar_optimizaciones.py` - Aplicar optimizaciones
- `aplicar_indices.py` - Aplicar índices

**Limpieza**:
- `clean_system.py` - Limpiar sistema
- `clean_and_reload.py` - Limpiar y recargar

**Deploy**:
- `render_setup.py` - Setup para Render

## 📁 `/test` - Pruebas y Verificación

Scripts para probar funcionalidad y verificar datos:

**Pruebas de API**:
- `test_endpoints.py` - Endpoints generales
- `test_coordinador_municipal_endpoints.py` - Coordinador municipal
- `test_monitoreo_endpoint.py` - Monitoreo
- `test_candidatos_endpoint.py` - Candidatos
- `test_puestos_endpoint.py` - Puestos
- `test_render_endpoints.py` - Endpoints en Render

**Pruebas de Roles**:
- `test_all_roles.py` - Todos los roles
- `test_all_roles_api.py` - API de roles
- `test_usuarios_roles.py` - Usuarios y roles

**Pruebas de Funcionalidad**:
- `test_geolocalizacion.py` - Geolocalización
- `test_bulk_upload.py` - Carga masiva
- `test_logos.py` - Logos
- `test_security_fixes.py` - Fixes de seguridad

**Verificación de Datos**:
- `verificar_sistema_completo.py` - Sistema completo
- `verificacion_completa_sistema.py` - Verificación completa
- `verificar_y_cargar_datos_completo.py` - Verificar y cargar
- `verificar_testigos.py` - Testigos
- `verificar_ubicaciones.py` - Ubicaciones
- `verificar_votantes_mesas.py` - Votantes por mesa
- `verificar_monitoreo.py` - Monitoreo
- `verify_data.py` - Datos generales

**Diagnóstico**:
- `diagnostico_sistema.py` - Sistema
- `diagnostico_testigos.py` - Testigos
- `diagnostico_inicializacion.py` - Inicialización

**Revisión**:
- `revisar_coordinadores_municipales.py` - Coordinadores municipales
- `ver_estructura_bd.py` - Estructura de BD
- `ver_tablas.py` - Tablas
- `ver_codigos_mesa.py` - Códigos de mesa

**Checks**:
- `check_system.py` - Sistema
- `check_db.py` - Base de datos
- `check_logos.py` - Logos
- `check_partidos.py` - Partidos
- `check_monitoreo_user.py` - Usuario monitoreo
- `check_testigo_password.py` - Password testigo
- `check_zona_codigo_bd.py` - Zona código

**HTML de Prueba**:
- `test_mapa.html` - Mapa
- `test_bottom_nav.html` - Navegación inferior
- `TEST_API_SUPER_ADMIN.html` - API super admin

## 📁 `/fix` - Corrección y Reparación

Scripts para corregir problemas y reparar datos:

**Corrección de Usuarios**:
- `fix_usuarios_ubicacion.py` - Ubicación de usuarios
- `fix_testigos_simple.py` - Testigos (simple)
- `fix_testigos_ubicacion.py` - Ubicación de testigos
- `fix_super_admin.py` - Super admin
- `fix_coord_mun_ubicacion.py` - Ubicación coordinador municipal
- `fix_usuario_monitoreo.py` - Usuario monitoreo

**Corrección de Base de Datos**:
- `fix_database_columns.py` - Columnas de BD
- `fix_db_direct.py` - BD directa
- `fix_incidentes_columns.py` - Columnas de incidentes

**Corrección de Código**:
- `fix_imports.py` - Imports
- `fix_imports_v2.py` - Imports v2
- `fix_logos.py` - Logos

**Corrección de Roles**:
- `corregir_roles_universal.py` - Roles universal
- `corregir_roles_usuarios.py` - Roles de usuarios
- `corregir_coordinador_generico.py` - Coordinador genérico

**Desbloqueo y Reset**:
- `desbloquear_coord_mun.py` - Desbloquear coordinador municipal
- `reset_coord_mun_password.py` - Reset password coordinador

## 📁 `/utils` - Utilidades y Herramientas

Scripts de utilidades generales:

**Actualización de Datos**:
- `actualizar_candidatos_completos.py` - Candidatos
- `actualizar_coordenadas_puestos.py` - Coordenadas de puestos
- `actualizar_logos_partidos.py` - Logos de partidos
- `actualizar_votantes_mesas.py` - Votantes por mesa

**Agregar Datos**:
- `add_citrep_tipo_eleccion.py` - Tipo de elección CITREP

**Listar Datos**:
- `listar_municipios_caqueta.py` - Municipios de Caquetá
- `listar_testigos.py` - Testigos

**Asignación**:
- `asignar_ubicacion_testigos.py` - Ubicación a testigos

**Upload**:
- `upload_db_to_render.py` - Subir BD a Render

**Archivos SQL**:
- `crear_indices_monitoreo.sql` - Índices de monitoreo
- `optimizar_bd_monitoreo.sql` - Optimizar BD monitoreo
- `verificar_y_corregir_roles.sql` - Verificar y corregir roles

**Archivos Batch**:
- `actualizar_logos.bat` - Actualizar logos
- `check_system.bat` - Check sistema
- `crear_usuario_monitoreo.bat` - Crear usuario monitoreo
- `inicializar_datos.bat` - Inicializar datos
- `instalar_monitoreo_completo.bat` - Instalar monitoreo
- `test_optimizations.bat` - Test optimizaciones

## Uso Común

### Inicializar Sistema Nuevo
```bash
python scripts/init/init_system.py
python scripts/init/load_complete_test_data.py
```

### Crear Usuarios de Prueba
```bash
python scripts/init/crear_testigos_prueba.py
python scripts/init/crear_usuarios_florencia.py
```

### Verificar Sistema
```bash
python scripts/test/verificar_sistema_completo.py
python scripts/test/check_system.py
```

### Corregir Problemas
```bash
python scripts/fix/fix_usuarios_ubicacion.py
python scripts/fix/corregir_roles_universal.py
```

## Notas

- Todos los scripts deben ejecutarse desde la raíz del proyecto
- Usar entorno virtual activado: `.venv\Scripts\activate`
- Algunos scripts requieren variables de entorno configuradas
- Hacer backup de la BD antes de ejecutar scripts de corrección

## Consolidación y Limpieza Realizada

**Antes**:
- 2 carpetas scripts (raíz y backend/scripts)
- 119+ archivos desorganizados
- Muchos duplicados y obsoletos
- Difícil encontrar el script correcto

**Después**:
- 1 carpeta scripts con 4 subcarpetas organizadas
- Scripts categorizados por función
- Duplicados eliminados
- READMEs en cada subcarpeta
- Fácil navegación y mantenimiento

**Limpieza**:
- ✅ Eliminados scripts duplicados
- ✅ Eliminados scripts obsoletos
- ✅ Archivos reubicados correctamente
- ✅ Estructura clara y mantenible

**Conteo Final**:
- `init/`: ~30 archivos (inicialización y carga)
- `test/`: ~50 archivos (pruebas y verificación)
- `fix/`: ~15 archivos (correcciones)
- `utils/`: ~17 archivos (utilidades)
