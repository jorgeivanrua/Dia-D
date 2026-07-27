# 🔧 Scripts del Sistema Electoral

Esta carpeta contiene todos los scripts de utilidades, instalación y mantenimiento del sistema.

## 📋 Categorías

### 🚀 Instalación y Setup
- `instalar_monitoreo_completo.bat` - Instalación completa del sistema de monitoreo
- `setup.bat` / `setup.sh` - Setup inicial del proyecto (en raíz)

### 🗄️ Base de Datos
- `crear_indices_monitoreo.sql` - Índices de optimización (24 índices)
- `aplicar_indices.py` - Aplicador de índices
- `init_db_simple.py` - Inicialización simple de BD

### 📊 Carga de Datos
- `cargar_divipola_v2.py` - Cargar datos DIVIPOLA (versión actual)
- `cargar_logos_bd.py` - Cargar logos de partidos
- `actualizar_logos_partidos.py` - Actualizar logos

### ✅ Verificación
- `verificar_monitoreo.py` - Verificación completa del sistema de monitoreo
- `check_monitoreo_user.py` - Verificar usuario de monitoreo
- `check_system.bat` - Verificación del sistema

### 🧪 Testing
- `test_optimizations.bat` - Pruebas de optimizaciones
- `test_render_endpoints.py` - Pruebas de endpoints para Render

### 👤 Usuarios
- `crear_usuario_monitoreo.bat` - Crear usuario de monitoreo

### 🚀 Deployment
- `render_setup.py` - Setup para Render

### 📦 Deprecated
- `deprecated/` - Scripts antiguos (no usar)
  - `cargar_divipola.py` - Primera versión
  - `cargar_divipola_simple.py` - Versión simplificada

## 🎯 Scripts Principales

### Para Empezar
```bash
# Windows
scripts\instalar_monitoreo_completo.bat

# Linux/Mac
chmod +x scripts/instalar_monitoreo_completo.sh
./scripts/instalar_monitoreo_completo.sh
```

### Verificar Sistema
```bash
python scripts\verificar_monitoreo.py
python scripts\check_monitoreo_user.py
```

### Cargar Datos
```bash
python scripts\cargar_divipola_v2.py
python scripts\cargar_logos_bd.py
```

### Optimizar BD
```bash
python scripts\aplicar_indices.py
```

## 📚 Documentación

Para más información, consulta:
- `../docs/INICIO_RAPIDO_MONITOREO.md` - Inicio rápido
- `../docs/GUIA_COMPLETA_MONITOREO.md` - Guía completa
- `../docs/ESTRUCTURA_PROYECTO_MONITOREO.md` - Estructura del proyecto

---

**Última actualización**: 28 de Noviembre de 2025
