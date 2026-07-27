# 📜 Scripts del Sistema Electoral - Guía Actualizada

## 🎯 Scripts Principales (USAR ESTOS)

### 1. `init_system.py` - Inicialización Completa ⭐

**Script principal para inicializar el sistema.**

```bash
# Inicialización normal
python scripts/init_system.py

# Resetear contraseñas de usuarios básicos
python scripts/init_system.py --reset-passwords
```

**Qué hace:**
- ✅ Verifica/crea estructura de base de datos
- ✅ Crea usuarios básicos del sistema
- ✅ Verifica ubicaciones (DIVIPOLA)
- ✅ Verifica configuración electoral

**Cuándo usar:**
- Primera instalación
- Después de clonar el repositorio
- Para verificar que todo esté OK

---

### 2. `load_divipola.py` - Cargar Ubicaciones

**Carga datos de ubicaciones desde archivo CSV.**

```bash
python scripts/load_divipola.py
```

**Qué hace:**
- ✅ Carga departamentos, municipios, zonas, puestos y mesas
- ✅ Crea jerarquía de ubicaciones
- ✅ Importa coordenadas geográficas

**Cuándo usar:**
- Después de `init_system.py` si no hay ubicaciones
- Para actualizar datos de DIVIPOLA

---

### 3. `init_configuracion_electoral.py` - Configuración Electoral

**Carga configuración electoral (partidos, candidatos, tipos de elección).**

```bash
python scripts/init_configuracion_electoral.py
```

**Qué hace:**
- ✅ Crea tipos de elección
- ✅ Carga partidos políticos
- ✅ Carga candidatos de ejemplo

**Cuándo usar:**
- Después de `init_system.py` si no hay configuración electoral
- Para actualizar partidos/candidatos

---

### 4. `migrate_to_alembic.py` - Configurar Migraciones

**Configura Flask-Migrate (Alembic) para migraciones de BD.**

```bash
python scripts/migrate_to_alembic.py
```

**Qué hace:**
- ✅ Inicializa Flask-Migrate
- ✅ Crea migración inicial
- ✅ Aplica migraciones

**Cuándo usar:**
- Una sola vez al configurar el proyecto
- Para migrar de SQL manual a Alembic

---

## 🗂️ Scripts Deprecados (NO USAR)

Los siguientes scripts están deprecados y serán eliminados:

- ❌ `crear_usuarios_basicos.py` → Usar `init_system.py`
- ❌ `crear_usuarios_basicos_fijos.py` → Usar `init_system.py`
- ❌ `fix_usuarios_completo.py` → Usar `init_system.py --reset-passwords`
- ❌ `fix_passwords_render.py` → Usar endpoints de emergencia
- ❌ `resetear_passwords_render.py` → Usar endpoints de emergencia

---

## 🔧 Scripts de Utilidad

### Verificación

```bash
# Verificar sistema completo
python scripts/verificar_sistema_completo.py

# Verificar usuarios
python scripts/verificar_passwords.py

# Verificar datos
python scripts/verify_data.py
```

### Diagnóstico

```bash
# Diagnóstico del sistema
python scripts/diagnostico_sistema.py

# Diagnóstico de testigos
python scripts/diagnostico_testigos.py
```

---

## 📋 Flujo de Instalación Recomendado

### Primera Instalación

```bash
# 1. Inicializar sistema
python scripts/init_system.py

# 2. Cargar ubicaciones
python scripts/load_divipola.py

# 3. Cargar configuración electoral
python scripts/init_configuracion_electoral.py

# 4. Verificar
python scripts/verificar_sistema_completo.py
```

### Actualización/Mantenimiento

```bash
# Resetear contraseñas (emergencia)
python scripts/init_system.py --reset-passwords

# Actualizar configuración
python scripts/init_configuracion_electoral.py
```

---

## 🚨 Emergencias

### Resetear Contraseñas

**Opción 1: Script (recomendado)**
```bash
python scripts/init_system.py --reset-passwords
```

**Opción 2: API (si no tienes acceso al servidor)**
```bash
curl -X POST https://tu-app.com/api/emergency/emergency-reset-passwords \
  -H "Content-Type: application/json" \
  -d '{"emergency_key": "tu-clave-secreta"}'
```

Ver `docs/SEGURIDAD.md` para más información sobre endpoints de emergencia.

---

## 📚 Documentación Adicional

- **Seguridad:** `docs/SEGURIDAD.md`
- **Despliegue:** `GUIA_DESPLIEGUE.md`
- **Inicio Rápido:** `INICIO_RAPIDO.md`

---

**Última actualización:** Noviembre 2024
