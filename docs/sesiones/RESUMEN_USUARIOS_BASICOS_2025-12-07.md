# Resumen: Sistema de Usuarios Básicos Definitivos

**Fecha**: 2025-12-07  
**Sesión**: Continuación - Configuración de usuarios persistentes  
**Estado**: ✅ Completado

## Problema Identificado

Los usuarios básicos del sistema no estaban correctamente definidos. Inicialmente se pensó que solo Super Admin y Monitoreo eran usuarios básicos, pero el usuario aclaró que **todos los coordinadores y testigos definitivos** (1 por ubicación) deben ser usuarios básicos del sistema.

## Solución Implementada

### Definición de Usuarios Básicos Definitivos

**Usuarios Globales** (sin ubicación):
- Super Admin (1)
- Monitoreo (1)

**Usuarios por Ubicación** (1 por cada):
- Coordinador Departamental (1 por departamento)
- Coordinador Municipal (1 por municipio)
- Coordinador de Puesto (1 por puesto)
- Testigo Electoral (1 por puesto)

### Scripts Creados

#### 1. `marcar_usuarios_definitivos_basicos.py` ⭐ PRINCIPAL
Script que marca automáticamente todos los usuarios definitivos como básicos:
- Marca Super Admin y Monitoreo
- Marca 1 coordinador departamental por departamento
- Marca 1 coordinador municipal por municipio
- Marca 1 coordinador de puesto por puesto
- Marca 1 testigo por puesto
- Si hay múltiples usuarios en una ubicación, marca solo el primero
- Reporta ubicaciones sin usuarios

**Uso**:
```bash
python scripts/utils/marcar_usuarios_definitivos_basicos.py
```

#### 2. `verificar_usuarios_basicos.py`
Verifica que todos los usuarios básicos estén presentes:
- Muestra usuarios globales (Super Admin, Monitoreo)
- Cuenta coordinadores departamentales vs departamentos
- Cuenta coordinadores municipales vs municipios
- Cuenta coordinadores de puesto vs puestos
- Cuenta testigos básicos vs puestos
- Muestra estadísticas generales

**Uso**:
```bash
python scripts/utils/verificar_usuarios_basicos.py
```

#### 3. `limpiar_usuarios_prueba.py`
Elimina todos los usuarios que NO son básicos:
- Solicita confirmación antes de eliminar
- Protege usuarios con `es_usuario_basico=True`
- Muestra usuarios restantes después de limpieza

**Uso**:
```bash
python scripts/utils/limpiar_usuarios_prueba.py
```

#### 4. `marcar_testigos_basicos.py`
Marca solo testigos como usuarios básicos (uso específico):
```bash
python scripts/utils/marcar_testigos_basicos.py
```

### Protección en Importación

Modificado `backend/routes/database_backup.py`:
- NO sobrescribe usuarios con `es_usuario_basico=True`
- Actualiza usuarios existentes que NO son básicos
- Crea nuevos usuarios si no existen
- Protege usuarios definitivos del sistema

### Inicialización Automática

Modificado `backend/utils/init_usuarios_basicos.py`:
- Solo crea Super Admin y Monitoreo automáticamente
- Los coordinadores y testigos se marcan manualmente con el script
- Función `verificar_usuarios_basicos()` solo verifica usuarios globales

## Flujo de Trabajo Recomendado

### Desarrollo Local

1. **Marcar usuarios definitivos**:
```bash
python scripts/utils/marcar_usuarios_definitivos_basicos.py
```

2. **Verificar**:
```bash
python scripts/utils/verificar_usuarios_basicos.py
```

3. **Limpiar usuarios de prueba**:
```bash
python scripts/utils/limpiar_usuarios_prueba.py
```

4. **Exportar BD limpia**:
```bash
python scripts/utils/export_data_to_json.py
```

### Despliegue en Render

1. Render crea Super Admin y Monitoreo automáticamente
2. Importar BD desde Super Admin Dashboard
3. Los usuarios básicos NO se sobrescriben
4. Usuarios importados reciben contraseña temporal `test123`

## Archivos Modificados

### Backend
- `backend/utils/init_usuarios_basicos.py` - Solo crea usuarios globales
- `backend/routes/database_backup.py` - Protección de usuarios básicos en importación

### Scripts Nuevos
- `scripts/utils/marcar_usuarios_definitivos_basicos.py` ⭐
- `scripts/utils/verificar_usuarios_basicos.py`
- `scripts/utils/limpiar_usuarios_prueba.py`
- `scripts/utils/marcar_testigos_basicos.py`

### Documentación
- `docs/implementaciones/SISTEMA_USUARIOS_BASICOS.md` - Documentación completa
- `scripts/utils/README.md` - Actualizado con nuevos scripts

## Reglas Importantes

1. **1 usuario básico por ubicación**: Solo el primer usuario de cada ubicación se marca como básico
2. **Usuarios adicionales**: Si hay múltiples usuarios en una ubicación, los demás son respaldo/adicionales
3. **Protección multicapa**: Usuarios básicos protegidos en importación y limpieza
4. **Inicialización automática**: Solo Super Admin y Monitoreo se crean al iniciar la app
5. **Marcado manual**: Coordinadores y testigos se marcan con el script después de crear ubicaciones

## Testing

### Verificar usuarios básicos
```bash
python scripts/utils/verificar_usuarios_basicos.py
```

**Salida esperada**:
- ✅ Super Admin y Monitoreo presentes
- Conteo de coordinadores por tipo vs ubicaciones
- Conteo de testigos vs puestos
- Estadísticas generales

### Marcar usuarios definitivos
```bash
python scripts/utils/marcar_usuarios_definitivos_basicos.py
```

**Resultado**:
- Marca automáticamente todos los usuarios definitivos
- Reporta ubicaciones sin usuarios
- Muestra resumen de usuarios básicos por tipo

## Próximos Pasos

1. ✅ Sistema de usuarios básicos definitivos implementado
2. ✅ Protección en importación de BD
3. ✅ Scripts de utilidades creados
4. ✅ Documentación completa
5. ⏳ Probar en Render con PostgreSQL
6. ⏳ Ejecutar `marcar_usuarios_definitivos_basicos.py` en local
7. ⏳ Exportar BD limpia y subir a Render

## Commit

```
feat: Sistema de usuarios básicos definitivos con protección en importación

- Usuarios básicos definitivos (1 por ubicación)
- Protección en importación de BD
- Scripts de utilidades completos
- Documentación actualizada
```

**Commit hash**: e338c7b  
**Pusheado**: ✅ Sí
