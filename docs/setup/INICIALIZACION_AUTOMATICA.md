# 🎉 Inicialización Automática de Datos

## 📋 Resumen

El sistema ahora cuenta con **inicialización automática de datos** que carga todos los datos necesarios para el funcionamiento del sistema electoral en cada instalación o deploy.

## ✅ Datos Cargados Automáticamente

### 📍 DIVIPOLA (Ubicaciones)
- **22 Departamentos**: Antioquia, Atlántico, Bogotá D.C., Bolívar, Boyacá, Caldas, Cauca, Córdoba, Cundinamarca, Chocó, Huila, La Guajira, Magdalena, Meta, Nariño, Norte de Santander, Quindío, Risaralda, Santander, Sucre, Tolima, Valle del Cauca
- **1,122 Municipios**
- **2,899 Zonas**
- **13,405 Puestos de votación**

### 🎨 Partidos Políticos (9 partidos)
| Código | Nombre | Color |
|--------|--------|-------|
| PACTO | Pacto Histórico | #FF0000 |
| LIBERAL | Partido Liberal | #FF0000 |
| CONSERVADOR | Partido Conservador | #0000FF |
| VERDE | Alianza Verde | #00FF00 |
| CENTRO_DEM | Centro Democrático | #0080FF |
| CAMBIO_RADICAL | Cambio Radical | #FFA500 |
| U | Partido de la U | #FFFF00 |
| MIRA | MIRA | #800080 |
| OTROS | Otros Partidos | #808080 |

### 🗳️ Tipos de Elección (6 tipos)
1. Senado de la República
2. Cámara de Representantes
3. Gobernación
4. Asamblea Departamental
5. Alcaldía
6. Concejo Municipal

### 👤 Candidatos (7 candidatos de ejemplo)
| Nombre | Partido | Tipo Elección |
|--------|---------|---------------|
| Gustavo Bolívar | Pacto Histórico | Senado |
| María José Pizarro | Pacto Histórico | Senado |
| Iván Cepeda | Pacto Histórico | Senado |
| Juan Fernando Cristo | Partido Liberal | Senado |
| Efraín Cepeda | Partido Conservador | Senado |
| Angélica Lozano | Alianza Verde | Senado |
| María Fernanda Cabal | Centro Democrático | Senado |

### 👥 Usuarios del Sistema (6 usuarios)
| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| **monitoreo** | **Monitoreo2025!** | Monitoreo |
| auditor | test123 | Auditor Electoral |
| coord_dept | test123 | Coordinador Departamental |
| coord_mun | test123 | Coordinador Municipal |
| coord_puesto | test123 | Coordinador de Puesto |
| testigo1 | test123 | Testigo Electoral |

## 🚀 Cómo Usar

### Instalación Automática

#### En Windows
```bash
# Durante la instalación inicial
setup.bat

# O manualmente
scripts\inicializar_datos.bat
```

#### En Linux/Mac
```bash
# Durante la instalación inicial
./setup.sh

# O manualmente
python scripts/inicializar_datos_automatico.py
```

### En Render (Automático)
La inicialización se ejecuta automáticamente durante el deploy a través de `render_setup.py`.

### Verificación
```bash
# Verificar que todos los datos estén cargados
python scripts/verificar_y_cargar_datos_completo.py
```

## 📊 Salida del Script

```
======================================================================
INICIALIZACIÓN AUTOMÁTICA DE DATOS
======================================================================

📍 Cargando datos DIVIPOLA...
   ✅ DIVIPOLA ya cargado

🗳️  Cargando tipos de elección...
   ✅ Cargados 6 tipos de elección

🎨 Cargando partidos políticos...
   ✅ Cargados 9 partidos

👤 Cargando candidatos...
   ✅ Cargados 7 candidatos

👥 Cargando usuarios del sistema...
   ✅ Cargados 6 usuarios

======================================================================
RESUMEN DE INICIALIZACIÓN
======================================================================

📊 Estado:
  ✅ Divipola: OK
  ✅ Tipos_eleccion: OK
  ✅ Partidos: OK
  ✅ Candidatos: OK
  ✅ Usuarios: OK

🎉 ¡TODOS LOS DATOS INICIALIZADOS CORRECTAMENTE!

📝 Credenciales de acceso:
   Monitoreo: monitoreo / Monitoreo2025!
   Otros: [usuario] / test123
```

## 🔧 Archivos Relacionados

### Scripts
- `scripts/inicializar_datos_automatico.py` - Script principal de inicialización
- `scripts/verificar_y_cargar_datos_completo.py` - Verificación de datos
- `scripts/inicializar_datos.bat` - Wrapper para Windows
- `render_setup.py` - Inicialización en Render

### Datos
- `data/divipola.csv` - Datos de ubicaciones DIVIPOLA

## 🎯 Ventajas

### ✅ Automatización Completa
- No requiere intervención manual
- Se ejecuta en cada instalación
- Idempotente (puede ejecutarse múltiples veces sin duplicar datos)

### ✅ Consistencia
- Mismos datos en todos los ambientes
- Datos de prueba listos para usar
- Configuración estándar

### ✅ Rapidez
- Instalación en segundos
- Deploy automático en Render
- Listo para usar inmediatamente

## 🔄 Flujo de Inicialización

```
┌─────────────────────────────────────────────────────────────┐
│                    INICIO DE INSTALACIÓN                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              1. Verificar Base de Datos                      │
│              ✓ Crear tablas si no existen                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              2. Cargar DIVIPOLA                              │
│              ✓ 22 departamentos                              │
│              ✓ 1,122 municipios                              │
│              ✓ 13,405 puestos                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              3. Cargar Tipos de Elección                     │
│              ✓ 6 tipos (Senado, Cámara, etc.)               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              4. Cargar Partidos Políticos                    │
│              ✓ 9 partidos con colores                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              5. Cargar Candidatos                            │
│              ✓ 7 candidatos de ejemplo                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              6. Crear Usuarios del Sistema                   │
│              ✓ 6 usuarios (monitoreo, auditor, etc.)        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    ✅ SISTEMA LISTO                          │
└─────────────────────────────────────────────────────────────┘
```

## 📝 Notas Importantes

### Seguridad
⚠️ **IMPORTANTE**: Las contraseñas por defecto son para desarrollo. En producción:
1. Cambia todas las contraseñas inmediatamente
2. Usa contraseñas fuertes
3. Implementa rotación de contraseñas

### Datos de Producción
- Los datos cargados son de **ejemplo/prueba**
- Para producción, reemplaza con datos reales:
  - Candidatos reales de la elección
  - Partidos participantes
  - Usuarios reales del sistema

### Personalización
Para personalizar los datos iniciales, edita:
- `scripts/inicializar_datos_automatico.py`

## 🆘 Solución de Problemas

### Error: "No se encontró divipola.csv"
```bash
# Verifica que el archivo exista
ls data/divipola.csv

# Si no existe, descárgalo o créalo
```

### Error: "Tabla no existe"
```bash
# Reinicializa la base de datos
python setup.py
```

### Verificar estado de los datos
```bash
# Ver resumen completo
python scripts/verificar_y_cargar_datos_completo.py
```

---

**Versión**: 1.0  
**Fecha**: 28 de Noviembre de 2025  
**Estado**: ✅ IMPLEMENTADO Y FUNCIONANDO
