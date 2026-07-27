# Resumen de Carga de Datos DIVIPOLA

## ✅ Proceso Completado

Se ha realizado exitosamente la carga completa de datos DIVIPOLA en la base de datos del sistema electoral.

## 📊 Datos Cargados

### Total Nacional
- **Departamentos:** 33
- **Municipios:** 1,122
- **Zonas:** 2,899
- **Puestos:** 13,405
- **Mesas:** 19,833

### Caquetá (Código 44) - Datos Específicos
- **Departamento:** CAQUETA
- **Municipios:** 16
  1. ALBANIA
  2. BELEN DE LOS ANDAQUIES
  3. CARTAGENA DEL CHAIRA
  4. CURILLO
  5. EL DONCELLO
  6. EL PAUJIL
  7. FLORENCIA (Capital)
  8. LA MONTAÑITA
  9. MILAN
  10. MORELIA
  11. PUERTO RICO
  12. SAN JOSE DEL FRAGUA
  13. SAN VICENTE DEL CAGUAN
  14. SOLANO
  15. SOLITA
  16. VALPARAISO

- **Zonas:** 38
- **Puestos:** 150
- **Mesas:** 196

## 🔧 Scripts Utilizados

### 1. `cargar_divipola_simple.py`
Script principal de carga sin emojis para compatibilidad con Windows.

**Características:**
- Limpia la tabla `locations` antes de cargar
- Procesa datos jerárquicamente (departamento → municipio → zona → puesto → mesa)
- Incluye información geográfica (latitud, longitud, dirección)
- Registra votantes por género (mujeres, hombres, total)
- Commits parciales cada 1,000 registros para optimización

**Uso:**
```bash
python cargar_divipola_simple.py
```

### 2. `cargar_divipola_v2.py`
Script alternativo con soporte para SQLAlchemy y PostgreSQL.

**Características:**
- Compatible con SQLite y PostgreSQL
- Detecta automáticamente `divipola.csv` o `divipola1.csv`
- Soporte para variables de entorno
- Manejo de errores detallado

## 📁 Archivo Fuente

**Archivo:** `divipola.csv`
- **Formato:** CSV con encabezados
- **Codificación:** UTF-8
- **Registros:** 19,833 mesas electorales
- **Columnas principales:**
  - `dd`: Código departamento (2 dígitos)
  - `mm`: Código municipio (2 dígitos)
  - `zz`: Código zona (2 dígitos)
  - `pp`: Código puesto (2 dígitos)
  - `mesa`: Número de mesa (2 dígitos)
  - `departamento`: Nombre del departamento
  - `municipio`: Nombre del municipio
  - `puesto`: Nombre del puesto de votación
  - `mesa_nombre`: Nombre completo de la mesa
  - `mujeres_mesa`: Votantes mujeres registradas
  - `hombres_mesa`: Votantes hombres registrados
  - `total_mesa`: Total votantes registrados
  - `comuna`: Comuna o sector
  - `direccion`: Dirección del puesto
  - `LATITUD`: Coordenada latitud
  - `LONGITUD`: Coordenada longitud

## 🗄️ Estructura de Base de Datos

### Tabla: `locations`

**Campos principales:**
- `id`: Identificador único
- `departamento_codigo`: Código del departamento (ej: '44')
- `municipio_codigo`: Código del municipio (ej: '4401')
- `zona_codigo`: Código de la zona (ej: '440101')
- `puesto_codigo`: Código del puesto (ej: '44010101')
- `mesa_codigo`: Código de la mesa (ej: '4401010101')
- `departamento_nombre`: Nombre del departamento
- `municipio_nombre`: Nombre del municipio
- `puesto_nombre`: Nombre del puesto
- `mesa_nombre`: Nombre de la mesa
- `nombre_completo`: Nombre jerárquico completo
- `tipo`: Tipo de ubicación ('departamento', 'municipio', 'zona', 'puesto', 'mesa')
- `parent_id`: ID del padre en la jerarquía
- `total_votantes_registrados`: Total de votantes
- `mujeres`: Votantes mujeres
- `hombres`: Votantes hombres
- `comuna`: Comuna o sector
- `direccion`: Dirección física
- `latitud`: Coordenada geográfica
- `longitud`: Coordenada geográfica
- `activo`: Estado (1 = activo, 0 = inactivo)

## 🔗 Integración con el Sistema

Los datos cargados están disponibles a través de:

1. **Endpoints API** (`/api/locations`)
   - `/departamentos` - Lista departamentos (solo Caquetá)
   - `/municipios/{codigo}` - Municipios por departamento
   - `/zonas/{codigo}` - Zonas por municipio
   - `/puestos/{codigo}` - Puestos por zona
   - `/mesas/{codigo}` - Mesas por puesto

2. **Frontend** (`location-loader.js`)
   - Funciones JavaScript para cargar datos en selects
   - Sistema de cascada automática
   - Disponible globalmente en todos los dashboards

## ✅ Verificación

Para verificar la carga de datos:

```python
import sqlite3

conn = sqlite3.connect('instance/electoral.db')
cursor = conn.cursor()

# Verificar Caquetá
cursor.execute("SELECT COUNT(*) FROM locations WHERE departamento_codigo='44'")
print(f"Total registros Caquetá: {cursor.fetchone()[0]}")

# Por tipo
for tipo in ['departamento', 'municipio', 'zona', 'puesto', 'mesa']:
    cursor.execute(f"SELECT COUNT(*) FROM locations WHERE tipo='{tipo}' AND departamento_codigo='44'")
    print(f"{tipo.capitalize()}: {cursor.fetchone()[0]}")

conn.close()
```

## 📝 Notas Importantes

1. **Código de Caquetá:** 44 (no 18)
2. **Jerarquía:** Departamento → Municipio → Zona → Puesto → Mesa
3. **Códigos:** Se construyen concatenando códigos de niveles superiores
4. **Filtrado:** El sistema solo muestra datos de Caquetá en producción
5. **Actualización:** Para recargar datos, ejecutar `cargar_divipola_simple.py`

## 🚀 Próximos Pasos

- ✅ Datos cargados y verificados
- ✅ Endpoints API funcionando
- ✅ Frontend integrado
- ✅ Documentación actualizada
- ⏳ Pruebas en producción pendientes

---

**Fecha de Carga:** 2025-11-27  
**Registros Totales:** 19,833  
**Estado:** ✅ Completado
