# 🧪 ARCHIVOS CSV DE PRUEBA - CARGA MASIVA

Este directorio contiene archivos CSV de prueba para el sistema de carga masiva electoral.

---

## 📁 ARCHIVOS INCLUIDOS

### 1. partidos.csv
**Registros:** 5 partidos políticos  
**Uso:** Probar carga de partidos  
**Contenido:**
- Partido Liberal Colombiano
- Partido Conservador Colombiano
- Alianza Verde
- Partido de la U
- Polo Democrático Alternativo

### 2. candidatos_alcaldia.csv
**Registros:** 5 candidatos  
**Uso:** Probar elección uninominal (Alcaldía)  
**Características:**
- Un candidato por partido
- Cédulas únicas
- Sin independientes

### 3. candidatos_senado.csv
**Registros:** 25 candidatos  
**Uso:** Probar lista cerrada (Senado)  
**Características:**
- 5 candidatos por partido
- Números de lista 1-5
- Un cabeza de lista por partido

### 4. candidatos_camara_caqueta.csv
**Registros:** 15 candidatos  
**Uso:** Probar lista cerrada departamental (Cámara)  
**Características:**
- 3 candidatos por partido
- Números de lista 1-3
- Específico para Caquetá

### 5. candidatos_concejo.csv
**Registros:** 35 candidatos  
**Uso:** Probar lista abierta (Concejo)  
**Características:**
- 7 candidatos por partido
- Voto preferente habilitado
- Números de lista 1-7

### 6. coaliciones.csv
**Registros:** 5 coaliciones  
**Uso:** Probar carga de coaliciones  
**Contenido:**
- Coalición Centro Esperanza (3 partidos)
- Pacto Histórico (2 partidos)

### 7. candidatos_con_errores.csv
**Registros:** 3 candidatos con errores  
**Uso:** Probar validación de errores  
**Errores incluidos:**
- Partido inexistente
- Números de lista duplicados
- Cédulas duplicadas
- Múltiples cabezas de lista

---

## 🚀 CÓMO USAR

### Opción 1: Usar archivos directamente
1. Ir al dashboard de Super Admin
2. Seleccionar tipo de carga correspondiente
3. Arrastrar archivo CSV
4. Validar y confirmar

### Opción 2: Regenerar archivos
```bash
python test_bulk_upload.py
```

---

## ✅ VALIDACIÓN

Todos los archivos (excepto `candidatos_con_errores.csv`) están validados y listos para cargar sin errores.

### Estructura Validada:
- ✅ Encoding UTF-8
- ✅ Headers correctos
- ✅ Datos válidos
- ✅ Sin duplicados
- ✅ Formato correcto

---

## 📊 ESTADÍSTICAS

| Archivo | Registros | Tamaño | Partidos |
|---------|-----------|--------|----------|
| partidos.csv | 5 | ~500 bytes | 5 |
| candidatos_alcaldia.csv | 5 | ~400 bytes | 5 |
| candidatos_senado.csv | 25 | ~2 KB | 5 |
| candidatos_camara_caqueta.csv | 15 | ~1.2 KB | 5 |
| candidatos_concejo.csv | 35 | ~2.8 KB | 5 |
| coaliciones.csv | 5 | ~300 bytes | 5 |
| candidatos_con_errores.csv | 3 | ~250 bytes | 2 |

**Total:** 93 registros

---

## 🎯 CASOS DE PRUEBA

### Caso 1: Carga Exitosa de Partidos
**Archivo:** partidos.csv  
**Resultado esperado:** 5 partidos creados

### Caso 2: Carga Exitosa de Candidatos Uninominales
**Archivo:** candidatos_alcaldia.csv  
**Configuración:** Tipo = Alcaldía, Municipio = Florencia  
**Resultado esperado:** 5 candidatos creados

### Caso 3: Carga Exitosa de Lista Cerrada
**Archivo:** candidatos_senado.csv  
**Configuración:** Tipo = Senado, Departamento = Nacional  
**Resultado esperado:** 25 candidatos creados, 5 cabezas de lista

### Caso 4: Validación de Errores
**Archivo:** candidatos_con_errores.csv  
**Resultado esperado:** 
- ❌ Validación falla
- ⚠️ Muestra 4+ errores
- ❌ No permite confirmar carga

---

## 🔧 PERSONALIZACIÓN

Para crear tus propios archivos de prueba:

1. **Copiar plantilla:**
   ```bash
   cp partidos.csv mis_partidos.csv
   ```

2. **Editar en Excel o Google Sheets**

3. **Guardar como CSV (UTF-8)**

4. **Probar en el sistema**

---

## ⚠️ NOTAS IMPORTANTES

1. **No modificar nombres de columnas** - El sistema espera nombres exactos
2. **Usar UTF-8** - Otros encodings pueden causar errores
3. **No dejar celdas vacías** - Usar "" para campos opcionales
4. **Respetar formato de colores** - Usar #RRGGBB (hexadecimal)
5. **Cédulas únicas** - No repetir cédulas entre candidatos

---

## 📞 SOPORTE

Si los archivos no funcionan:
1. Verificar encoding (debe ser UTF-8)
2. Verificar que no hay caracteres especiales
3. Regenerar con `python test_bulk_upload.py`
4. Consultar GUIA_RAPIDA_CARGA_MASIVA.md

---

**Generado por:** test_bulk_upload.py  
**Fecha:** 1 de Diciembre de 2025  
**Versión:** 1.0.0
