# 🚀 GUÍA RÁPIDA: CARGA MASIVA DE DATOS ELECTORALES

**Versión:** 1.0.0  
**Fecha:** 1 de Diciembre de 2025

---

## 📋 INICIO RÁPIDO (5 MINUTOS)

### 1. Acceder al Sistema
```
http://localhost:5000/admin/super-admin-dashboard
```
- Iniciar sesión como Super Admin
- Ir a la pestaña **"Configuración"**
- Scroll hasta **"Carga Masiva de Datos"**

### 2. Seleccionar Tipo de Carga
Elegir según lo que necesites cargar:
- **Partidos Políticos** → Para cargar partidos nuevos
- **Candidatos - Elección Uninominal** → Para Presidencia, Gobernación, Alcaldía
- **Candidatos - Lista Cerrada** → Para Senado, Cámara, Asamblea
- **Candidatos - Lista Abierta** → Para Concejo con voto preferente

### 3. Configurar Parámetros
- Seleccionar **Tipo de Elección** (ej: Senado, Cámara, Alcaldía)
- Seleccionar **Departamento** (ej: CAQUETÁ)
- Seleccionar **Municipio** (si aplica)
- Marcar opciones:
  - ✅ **Validar datos antes de cargar** (recomendado)
  - ☐ **Crear partidos si no existen** (si los partidos no están en BD)
  - ☐ **Sobrescribir datos existentes** (solo si quieres actualizar)

### 4. Preparar Archivo CSV
- Click en **"Descargar Plantilla"**
- Abrir plantilla en Excel o Google Sheets
- Llenar con tus datos
- Guardar como CSV (UTF-8)

### 5. Cargar y Validar
- Arrastrar archivo CSV a la zona de drop
- Click en **"Validar Archivo"**
- Revisar resultados:
  - ✅ **Verde** = Todo bien
  - ⚠️ **Amarillo** = Advertencias (puedes continuar)
  - ❌ **Rojo** = Errores (debes corregir)

### 6. Confirmar Carga
- Si no hay errores, click en **"Confirmar Carga"**
- Esperar mensaje de éxito
- Verificar datos en la pestaña correspondiente

---

## 📊 PLANTILLAS CSV POR TIPO

### Partidos Políticos
```csv
codigo,nombre,nombre_corto,color,logo_url,activo
LIBERAL,Partido Liberal Colombiano,Partido Liberal,#FF0000,,TRUE
CONSERVADOR,Partido Conservador Colombiano,Partido Conservador,#0000FF,,TRUE
```

### Candidatos Alcaldía (Uninominal)
```csv
partido_codigo,candidato_nombre,candidato_cedula,es_independiente,foto_url
LIBERAL,Juan Pérez García,12345678,FALSE,
CONSERVADOR,María López Silva,23456789,FALSE,
```

### Candidatos Senado (Lista Cerrada)
```csv
partido_codigo,numero_lista,candidato_nombre,candidato_cedula,es_cabeza_lista,foto_url
LIBERAL,1,Ana García Rodríguez,12345678,TRUE,
LIBERAL,2,Pedro Martínez López,23456789,FALSE,
LIBERAL,3,Sofía Hernández Cruz,34567890,FALSE,
```

### Candidatos Concejo (Lista Abierta)
```csv
partido_codigo,numero_lista,candidato_nombre,candidato_cedula,es_cabeza_lista,permite_voto_preferente,foto_url
VERDE,1,Roberto Silva Mora,12345678,TRUE,TRUE,
VERDE,2,Lucía Ramírez Torres,23456789,FALSE,TRUE,
```

---

## ✅ REGLAS IMPORTANTES

### Para TODOS los tipos:
1. ✅ Primera fila debe ser el **header** (nombres de columnas)
2. ✅ Archivo debe ser **CSV** (no Excel)
3. ✅ Encoding debe ser **UTF-8**
4. ✅ Tamaño máximo **10 MB**
5. ✅ No dejar celdas vacías en columnas requeridas

### Para Partidos:
1. ✅ Código debe ser **único** (no repetir)
2. ✅ Color debe ser **hexadecimal** (#FF0000)
3. ✅ Nombre corto máximo 20 caracteres

### Para Candidatos:
1. ✅ Cédula debe ser **única** (no repetir)
2. ✅ Partido debe **existir** (o marcar "Crear partidos")
3. ✅ Nombre completo (no solo apellido)

### Para Listas (Senado, Cámara, Asamblea, Concejo):
1. ✅ Número de lista debe ser **único por partido**
2. ✅ Solo **UN** cabeza de lista por partido (es_cabeza_lista = TRUE)
3. ✅ Números de lista deben ser **consecutivos** (1, 2, 3...)

---

## ⚠️ ERRORES COMUNES Y SOLUCIONES

### Error: "Faltan columnas requeridas"
**Causa:** El CSV no tiene todas las columnas necesarias  
**Solución:** Descargar plantilla y no modificar nombres de columnas

### Error: "Partido no existe"
**Causa:** El partido no está en la base de datos  
**Solución:** 
- Opción 1: Marcar "Crear partidos si no existen"
- Opción 2: Cargar primero los partidos

### Error: "Cédula duplicada"
**Causa:** Hay dos candidatos con la misma cédula  
**Solución:** Verificar que todas las cédulas sean únicas

### Error: "Múltiples cabezas de lista"
**Causa:** Hay más de un candidato con es_cabeza_lista = TRUE en el mismo partido  
**Solución:** Solo el primer candidato debe tener TRUE, los demás FALSE

### Error: "Números de lista duplicados"
**Causa:** Dos candidatos del mismo partido tienen el mismo número  
**Solución:** Asignar números únicos (1, 2, 3, 4...)

### Error: "Color inválido"
**Causa:** El color no está en formato hexadecimal  
**Solución:** Usar formato #RRGGBB (ej: #FF0000 para rojo)

---

## 🧪 ARCHIVOS DE PRUEBA

Se incluyen archivos CSV de ejemplo en `data/test_bulk_upload/`:

1. **partidos.csv** - 5 partidos de ejemplo
2. **candidatos_alcaldia.csv** - 5 candidatos uninominales
3. **candidatos_senado.csv** - 25 candidatos (5 por partido)
4. **candidatos_camara_caqueta.csv** - 15 candidatos del Caquetá
5. **candidatos_concejo.csv** - 35 candidatos con voto preferente

**Para generar archivos de prueba:**
```bash
python test_bulk_upload.py
```

---

## 💡 TIPS Y MEJORES PRÁCTICAS

### Antes de Cargar:
1. ✅ **Validar en Excel** primero (revisar duplicados, formato)
2. ✅ **Hacer backup** de la BD antes de cargas grandes
3. ✅ **Probar con archivo pequeño** primero (5-10 registros)
4. ✅ **Usar plantilla** siempre (no crear desde cero)

### Durante la Carga:
1. ✅ **Leer advertencias** cuidadosamente
2. ✅ **No cerrar ventana** mientras carga
3. ✅ **Esperar mensaje de éxito** antes de continuar

### Después de Cargar:
1. ✅ **Verificar datos** en la pestaña correspondiente
2. ✅ **Contar registros** (debe coincidir con CSV)
3. ✅ **Revisar partidos** creados automáticamente

---

## 📞 SOPORTE

### Si algo no funciona:

1. **Abrir consola del navegador** (F12)
   - Buscar errores en rojo
   - Copiar mensaje de error

2. **Verificar archivo CSV:**
   - Abrir en editor de texto (Notepad++)
   - Verificar que es UTF-8
   - Verificar que no hay caracteres raros

3. **Intentar con archivo de prueba:**
   - Usar uno de los archivos en `data/test_bulk_upload/`
   - Si funciona, el problema es tu archivo

4. **Revisar logs del backend:**
   - Ver terminal donde corre Flask
   - Buscar mensajes de error

---

## 🎯 CASOS DE USO FRECUENTES

### Caso 1: Cargar Candidatos al Senado
1. Tipo: **Candidatos - Lista Cerrada**
2. Elección: **Senado**
3. Departamento: **Nacional** (o el que corresponda)
4. Plantilla: Llenar con candidatos ordenados por partido
5. Validar que cada partido tenga máximo 100 candidatos

### Caso 2: Cargar Candidatos a la Cámara por Departamento
1. Tipo: **Candidatos - Lista Cerrada**
2. Elección: **Cámara de Representantes**
3. Departamento: **CAQUETÁ** (o el que corresponda)
4. Plantilla: Llenar con candidatos del departamento
5. Validar números de lista únicos por partido

### Caso 3: Cargar Candidatos a Alcaldía
1. Tipo: **Candidatos - Elección Uninominal**
2. Elección: **Alcaldía**
3. Municipio: **FLORENCIA** (o el que corresponda)
4. Plantilla: Un candidato por partido
5. Validar que no hay duplicados

---

## ⏱️ TIEMPOS ESTIMADOS

| Registros | Tiempo de Carga | Tiempo de Validación |
|-----------|----------------|---------------------|
| 10        | 1-2 segundos   | 1 segundo           |
| 50        | 3-5 segundos   | 2 segundos          |
| 100       | 5-10 segundos  | 3-5 segundos        |
| 500       | 20-30 segundos | 10-15 segundos      |
| 1000      | 40-60 segundos | 20-30 segundos      |

*Tiempos aproximados, pueden variar según el servidor*

---

## ✨ RESUMEN

1. **Descargar plantilla** → Llenar con datos → Guardar como CSV
2. **Arrastrar archivo** → Validar → Revisar resultados
3. **Confirmar carga** → Esperar éxito → Verificar datos

**¡Es así de simple!** 🎉

---

**Sistema Electoral del Caquetá**  
**Carga Masiva de Datos - Guía Rápida**  
**Versión 1.0.0 - Diciembre 2025**
