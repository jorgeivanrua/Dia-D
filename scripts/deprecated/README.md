# 📦 Scripts Deprecados

Este directorio contiene scripts antiguos que han sido reemplazados por versiones mejoradas.

**⚠️ NO USAR ESTOS SCRIPTS**

---

## 🔄 Reemplazos

### Scripts de Usuarios

Todos estos scripts han sido reemplazados por **`scripts/init_system.py`**:

- ❌ `crear_usuarios_basicos.py`
- ❌ `crear_usuarios_basicos_fijos.py`
- ❌ `create_fixed_users.py`
- ❌ `create_sample_users.py`
- ❌ `create_sample_users_simple.py`
- ❌ `create_test_users.py`
- ❌ `create_users_simple_passwords.py`
- ❌ `fix_usuarios_completo.py`

**✅ Usar en su lugar:**
```bash
python scripts/init_system.py
```

---

### Scripts de Passwords

Todos estos scripts han sido reemplazados por **`scripts/init_system.py --reset-passwords`**:

- ❌ `actualizar_passwords_render.py`
- ❌ `actualizar_passwords_texto_plano.py`
- ❌ `actualizar_todas_passwords_texto_plano.py`
- ❌ `fix_passwords_render.py`
- ❌ `reset_passwords_render_simple.py`
- ❌ `reset_passwords_via_api.py`
- ❌ `resetear_passwords_render.py`

**✅ Usar en su lugar:**
```bash
python scripts/init_system.py --reset-passwords
```

O usar los endpoints de emergencia (ver `docs/SEGURIDAD.md`)

---

## 📚 Documentación Actualizada

- **Guía de Scripts:** `scripts/README_NUEVO.md`
- **Seguridad:** `docs/SEGURIDAD.md`
- **Análisis del Sistema:** `ANALISIS_INICIO_LOCAL.md`

---

## 🗑️ Eliminación Futura

Estos scripts serán eliminados permanentemente en una versión futura.

Si necesitas alguna funcionalidad específica de estos scripts, contacta al equipo de desarrollo.

---

**Fecha de deprecación:** 30 de Noviembre de 2024  
**Versión:** 1.1.0
