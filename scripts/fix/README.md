# Scripts de Corrección

Scripts para corregir problemas y reparar datos.

## ⚠️ IMPORTANTE

**Hacer backup de la base de datos antes de ejecutar cualquier script de corrección:**
```bash
copy instance\electoral.db instance\electoral_backup_YYYYMMDD.db
```

## Uso Común

### Corrección de Usuarios
```bash
# Corregir ubicaciones de usuarios
python scripts/fix/fix_usuarios_ubicacion.py

# Corregir roles
python scripts/fix/corregir_roles_universal.py
```

### Corrección de Base de Datos
```bash
# Corregir columnas
python scripts/fix/fix_database_columns.py

# Corrección directa de BD
python scripts/fix/fix_db_direct.py
```

## Categorías

### Corrección de Usuarios
- `fix_usuarios_ubicacion.py` - Ubicación de usuarios
- `fix_testigos_simple.py` - Testigos (simple)
- `fix_testigos_ubicacion.py` - Ubicación de testigos
- `fix_super_admin.py` - Super admin
- `fix_coord_mun_ubicacion.py` - Ubicación coordinador municipal
- `fix_usuario_monitoreo.py` - Usuario monitoreo

### Corrección de Base de Datos
- `fix_database_columns.py` - Columnas de BD
- `fix_db_direct.py` - BD directa
- `fix_incidentes_columns.py` - Columnas de incidentes

### Corrección de Código
- `fix_imports.py` - Imports
- `fix_imports_v2.py` - Imports v2
- `fix_logos.py` - Logos

### Corrección de Roles
- `corregir_roles_universal.py` - Roles universal
- `corregir_roles_usuarios.py` - Roles de usuarios
- `corregir_coordinador_generico.py` - Coordinador genérico

### Desbloqueo y Reset
- `desbloquear_coord_mun.py` - Desbloquear coordinador municipal
- `reset_coord_mun_password.py` - Reset password coordinador

## Flujo Recomendado

1. **Identificar el problema**
   ```bash
   python scripts/test/check_system.py
   ```

2. **Hacer backup**
   ```bash
   copy instance\electoral.db instance\electoral_backup.db
   ```

3. **Ejecutar corrección**
   ```bash
   python scripts/fix/[script_apropiado].py
   ```

4. **Verificar corrección**
   ```bash
   python scripts/test/verificacion_completa_sistema.py
   ```

## Notas de Seguridad

- ✅ **SIEMPRE** hacer backup antes
- ✅ Probar en copia de BD primero
- ✅ Verificar después de ejecutar
- ❌ **NO** ejecutar en producción sin probar
- ❌ **NO** ejecutar múltiples scripts simultáneamente

## Recuperación

Si algo sale mal:
```bash
# Restaurar backup
copy instance\electoral_backup.db instance\electoral.db
```
