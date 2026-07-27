# Credenciales de Coordinadores Municipales

## Contraseña por Defecto
**Todos los coordinadores:** `test123`

## Lista de Coordinadores Activos

### 1. FLORENCIA (51 puestos)
- **Usuario:** `coord_mun`
- **Contraseña:** `coord123` (fue reseteada)
- **Municipio:** FLORENCIA
- **Código:** 01

### 2. ALBANIA (2 puestos)
- **Usuario:** `ALBANIA`
- **Contraseña:** `test123`
- **Municipio:** ALBANIA
- **Código:** 02

### 3. BELÉN DE LOS ANDAQUÍES (3 puestos)
- **Usuario:** `BELEN_DE_LOS_ANDAQUIES`
- **Contraseña:** `test123`
- **Municipio:** BELEN DE LOS ANDAQUIES
- **Código:** 04

### 4. CARTAGENA DEL CHAIRÁ (7 puestos)
- **Usuario:** `CARTAGENA_DEL_CHAIRA`
- **Contraseña:** `test123`
- **Municipio:** CARTAGENA DEL CHAIRA
- **Código:** 03

### 5. CURILLO (3 puestos)
- **Usuario:** `CURILLO`
- **Contraseña:** `test123`
- **Municipio:** CURILLO
- **Código:** 12

### 6. EL DONCELLO (7 puestos)
- **Usuario:** `EL_DONCELLO`
- **Contraseña:** `test123`
- **Municipio:** EL DONCELLO
- **Código:** 05

### 7. EL PAUJIL (3 puestos)
- **Usuario:** `EL_PAUJIL`
- **Contraseña:** `test123`
- **Municipio:** EL PAUJIL
- **Código:** 06

### 8. LA MONTAÑITA (5 puestos)
- **Usuario:** `LA_MONTAÑITA`
- **Contraseña:** `test123`
- **Municipio:** LA MONTAÑITA
- **Código:** 07

### 9. MILÁN (7 puestos)
- **Usuario:** `MILAN`
- **Contraseña:** `test123`
- **Municipio:** MILAN
- **Código:** 16

### 10. MORELIA (4 puestos) ✅
- **Usuario:** `MORELIA`
- **Contraseña:** `test123`
- **Municipio:** MORELIA
- **Código:** 17

### 11. PUERTO RICO (9 puestos)
- **Usuario:** `PUERTO_RICO`
- **Contraseña:** `test123`
- **Municipio:** PUERTO RICO
- **Código:** 09

### 12. SAN JOSÉ DEL FRAGUA (6 puestos)
- **Usuario:** `SAN_JOSE_DEL_FRAGUA`
- **Contraseña:** `test123`
- **Municipio:** SAN JOSE DEL FRAGUA
- **Código:** 20

### 13. SAN VICENTE DEL CAGUÁN (25 puestos) ✅
- **Usuario:** `SAN_VICENTE_DEL_CAGUAN`
- **Contraseña:** `test123`
- **Municipio:** SAN VICENTE DEL CAGUAN
- **Código:** 10

### 14. SOLANO (12 puestos)
- **Usuario:** `SOLANO`
- **Contraseña:** `test123`
- **Municipio:** SOLANO
- **Código:** 22

### 15. SOLITA (2 puestos)
- **Usuario:** `SOLITA`
- **Contraseña:** `test123`
- **Municipio:** SOLITA
- **Código:** 24

### 16. VALPARAÍSO (4 puestos)
- **Usuario:** `VALPARAISO`
- **Contraseña:** `test123`
- **Municipio:** VALPARAISO
- **Código:** 40

## Cómo Hacer Login

1. Ir a: `http://localhost:5000/login`
2. Seleccionar rol: **Coordinador Municipal**
3. Ingresar usuario (ejemplo: `MORELIA`)
4. Ingresar contraseña: `test123`
5. El sistema cargará automáticamente el municipio asignado

## Después del Login

1. Presionar `Ctrl + Shift + R` para hard refresh
2. El dashboard mostrará los puestos del municipio
3. Al hacer click en un puesto, el modal mostrará:
   - **Zona: 01** (en lugar de "N/A")
   - Información completa del puesto
   - Estadísticas de formularios

## Notas

- ✅ Todos los coordinadores tienen su municipio asignado
- ✅ Cada municipio tiene sus puestos configurados
- ✅ El campo `zona_codigo` existe en la BD y se retorna correctamente
- ⚠️ El usuario `coord_mun` tiene contraseña diferente: `coord123`
- ⚠️ El usuario genérico "Coordinador Municipal" fue desactivado (no tenía ubicación)

## Verificación

Para verificar que todo funciona:
1. Login con cualquier coordinador
2. Verificar que carga el número correcto de puestos
3. Click en un puesto
4. Verificar que el modal muestra "Zona: 01"

## Total
- **16 municipios** con coordinador asignado
- **149 puestos** en total en Caquetá
- **Todos activos y funcionando** ✅
