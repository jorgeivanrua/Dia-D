# Checklist de Configuración - Super Admin

## ⚠️ IMPORTANTE
Este checklist debe completarse ANTES de que los testigos comiencen a trabajar. Sin esta configuración, el sistema no funcionará.

## 1. Configuración Inicial del Sistema

### ✅ Tipos de Elección
- [ ] Crear al menos un tipo de elección
- [ ] Configurar si es uninominal (Presidencia, Alcaldía) o lista (Senado, Cámara)
- [ ] Activar los tipos de elección (`activo = True`)
- [ ] Verificar que aparecen en el dashboard

**Ejemplo de tipos comunes**:
- Presidencia y Vicepresidencia
- Senado de la República
- Cámara de Representantes
- Gobernación
- Asamblea Departamental
- Alcaldía
- Concejo Municipal

### ✅ Partidos Políticos
- [ ] Cargar partidos desde Excel o crear manualmente
- [ ] Asignar nombre completo y nombre corto
- [ ] Asignar color hexadecimal (ej: #FF0000)
- [ ] **Cargar logos automáticamente** (recomendado)
- [ ] Activar los partidos (`activo = True`)
- [ ] Definir orden de visualización
- [ ] Verificar que aparecen en el dashboard

**Campos requeridos en Excel**:
```
nombre, nombre_corto, color
Partido Liberal, PL, #FF0000
Partido Conservador, PC, #0000FF
```

**Carga Automática de Logos**:
1. Ir al dashboard del Super Admin
2. En la sección "Partidos Políticos"
3. Hacer clic en el botón "Cargar Logos" (icono de imagen)
4. Confirmar la acción
5. El sistema cargará automáticamente logos desde Wikipedia para:
   - Partido Liberal
   - Partido Conservador
   - Centro Democrático
   - Pacto Histórico
   - Cambio Radical
   - Partido de la U
   - Alianza Verde
   - Polo Democrático
   - MIRA
   - Comunes

**Nota**: Los logos se guardan como URLs en el campo `logo_url` de la tabla `partidos`

### ✅ Candidatos
- [ ] Cargar candidatos desde Excel o crear manualmente
- [ ] Asociar cada candidato a un partido
- [ ] Asociar cada candidato a un tipo de elección
- [ ] Asignar número de lista (si aplica)
- [ ] Marcar candidatos independientes (si aplica)
- [ ] Activar los candidatos (`activo = True`)
- [ ] Verificar que aparecen en el dashboard

**Campos requeridos en Excel**:
```
nombre_completo, partido_nombre, tipo_eleccion_nombre, numero_lista
Juan Pérez, Partido Liberal, Presidencia, 1
María García, Partido Conservador, Presidencia, 2
```

## 2. Configuración de Ubicaciones (DIVIPOLA)

### ✅ Jerarquía Territorial
- [ ] Cargar departamentos
- [ ] Cargar municipios (asociados a departamentos)
- [ ] Cargar puestos de votación (asociados a municipios)
- [ ] Cargar mesas (asociadas a puestos)
- [ ] Configurar total de votantes por mesa
- [ ] Verificar jerarquía completa

**Orden de carga**:
1. Departamentos
2. Municipios
3. Puestos
4. Mesas

## 3. Configuración de Usuarios

### ✅ Crear Usuarios por Rol
- [ ] Super Admin (ya existe)
- [ ] Coordinadores Departamentales (uno por departamento)
- [ ] Coordinadores Municipales (uno por municipio)
- [ ] Coordinadores de Puesto (uno por puesto)
- [ ] Testigos (uno o más por mesa)
- [ ] Auditores (opcional)

**Importante**: Cada usuario debe estar asociado a su ubicación correspondiente.

## 4. Verificación Pre-Operativa

### ✅ Dashboard del Super Admin
- [ ] Los partidos se muestran correctamente
- [ ] Los candidatos se muestran correctamente
- [ ] Los tipos de elección se muestran correctamente
- [ ] Los usuarios se muestran correctamente
- [ ] No hay errores en la consola del navegador

### ✅ Prueba con Usuario Testigo
- [ ] Iniciar sesión como testigo
- [ ] Verificar que ve su mesa asignada
- [ ] Crear nuevo formulario E-14
- [ ] Verificar que se cargan los partidos
- [ ] Verificar que se cargan los candidatos
- [ ] Registrar votos de prueba
- [ ] Guardar formulario

### ✅ Prueba con Coordinador
- [ ] Iniciar sesión como coordinador de puesto
- [ ] Verificar que ve los formularios de su puesto
- [ ] Validar un formulario E-14
- [ ] Consultar consolidado del puesto
- [ ] Generar E-24 de prueba

## 5. Verificación en Base de Datos

### ✅ Consultas SQL de Verificación

```sql
-- 1. Verificar tipos de elección activos
SELECT id, codigo, nombre, activo 
FROM tipos_eleccion 
WHERE activo = 1;
-- Debe retornar al menos 1 registro

-- 2. Verificar partidos activos
SELECT id, codigo, nombre, nombre_corto, activo 
FROM partidos 
WHERE activo = 1;
-- Debe retornar al menos 2 registros

-- 3. Verificar candidatos activos
SELECT c.id, c.nombre_completo, p.nombre as partido, t.nombre as tipo_eleccion
FROM candidatos c
JOIN partidos p ON c.partido_id = p.id
JOIN tipos_eleccion t ON c.tipo_eleccion_id = t.id
WHERE c.activo = 1;
-- Debe retornar al menos 2 registros

-- 4. Verificar jerarquía de ubicaciones
SELECT 
    (SELECT COUNT(*) FROM locations WHERE tipo = 'departamento') as departamentos,
    (SELECT COUNT(*) FROM locations WHERE tipo = 'municipio') as municipios,
    (SELECT COUNT(*) FROM locations WHERE tipo = 'puesto') as puestos,
    (SELECT COUNT(*) FROM locations WHERE tipo = 'mesa') as mesas;
-- Todos deben ser > 0

-- 5. Verificar usuarios por rol
SELECT rol, COUNT(*) as cantidad
FROM users
WHERE activo = 1
GROUP BY rol;
-- Debe haber al menos 1 testigo
```

## 6. Problemas Comunes y Soluciones

### ❌ Los testigos no ven partidos
**Causa**: No hay partidos con `activo = True`
**Solución**: Activar partidos en el dashboard del Super Admin

### ❌ Los testigos no ven candidatos
**Causa**: 
- No hay candidatos con `activo = True`
- Los candidatos no están asociados al tipo de elección correcto
**Solución**: Verificar y corregir en el dashboard

### ❌ No se puede generar E-24
**Causa**: 
- No hay suficientes E-14 validados
- No se cumple el requisito del 80% de puestos completos
**Solución**: Validar más formularios E-14

### ❌ Los votos no se suman correctamente en E-24
**Causa**: Los E-14 no están en estado 'validado'
**Solución**: Los coordinadores deben validar los E-14 primero

## 7. Monitoreo Continuo

### ✅ Durante las Elecciones
- [ ] Monitorear cantidad de E-14 registrados
- [ ] Verificar que los E-14 se están validando
- [ ] Revisar discrepancias reportadas
- [ ] Verificar generación de E-24
- [ ] Monitorear estado del sistema (CPU, memoria, BD)

### ✅ Logs a Revisar
```javascript
// En la consola del navegador del Super Admin
[Fix] X partidos recibidos
[Fix] X candidatos recibidos
[Fix] X tipos recibidos
[Fix] ✓ Partidos renderizados
[Fix] ✓ Candidatos renderizados
[Fix] ✓ Tipos de elección renderizados
```

## 8. Respaldo y Seguridad

### ✅ Antes de Iniciar
- [ ] Hacer respaldo completo de la base de datos
- [ ] Verificar que los respaldos automáticos están funcionando
- [ ] Documentar credenciales de acceso
- [ ] Configurar alertas de sistema

### ✅ Durante las Elecciones
- [ ] Respaldos cada hora
- [ ] Monitorear espacio en disco
- [ ] Verificar integridad de PDFs generados (hash SHA-256)

## Contacto de Soporte

En caso de problemas técnicos:
1. Revisar logs del sistema
2. Verificar este checklist
3. Consultar documentación en `/docs`
4. Contactar al equipo técnico

---

**Última actualización**: 2024
**Versión del sistema**: 1.0
