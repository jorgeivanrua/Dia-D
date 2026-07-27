# 🔐 Credenciales del Sistema

## ⚠️ IMPORTANTE

Este documento contiene las credenciales por defecto del sistema. **ESTAS CONTRASEÑAS SON PARA DESARROLLO Y PRUEBAS ÚNICAMENTE**.

En producción, **DEBES CAMBIAR TODAS LAS CONTRASEÑAS** inmediatamente después del primer despliegue.

---

## 👥 Usuarios del Sistema

### Credenciales Oficiales (Local y Render)

Estas credenciales son **idénticas** tanto en desarrollo local como en Render:

| Usuario | Contraseña | Rol | Descripción |
|---------|-----------|-----|-------------|
| **monitoreo** | **Monitoreo2025!** | Monitoreo | Dashboard de monitoreo en tiempo real |
| **auditor** | **test123** | Auditor Electoral | Auditoría del sistema |
| **coord_dept** | **test123** | Coordinador Departamental | Coordinación departamental |
| **coord_mun** | **test123** | Coordinador Municipal | Coordinación municipal |
| **coord_puesto** | **test123** | Coordinador de Puesto | Coordinación de puesto |
| **testigo1** | **test123** | Testigo Electoral | Testigo electoral |

---

## 🔄 Consistencia entre Ambientes

### ✅ Garantía de Consistencia

Las contraseñas están definidas en **un solo lugar** y se usan en todos los ambientes:

**Archivo fuente**: `scripts/inicializar_datos_automatico.py`

```python
usuarios = [
    {'nombre': 'monitoreo', 'rol': 'monitoreo', 'password': 'Monitoreo2025!'},
    {'nombre': 'auditor', 'rol': 'auditor_electoral', 'password': 'test123'},
    {'nombre': 'coord_dept', 'rol': 'coordinador_departamental', 'password': 'test123'},
    {'nombre': 'coord_mun', 'rol': 'coordinador_municipal', 'password': 'test123'},
    {'nombre': 'coord_puesto', 'rol': 'coordinador_puesto', 'password': 'test123'},
    {'nombre': 'testigo1', 'rol': 'testigo_electoral', 'password': 'test123'},
]
```

### Scripts que usan estas credenciales:

1. **Local**: `scripts/inicializar_datos_automatico.py`
2. **Render**: `render_setup.py` (llama al script anterior)
3. **Setup**: `setup.py` (llama al script anterior)

---

## 🧪 Pruebas de Login

### Desarrollo Local

```bash
# Iniciar servidor
python run.py

# Probar login
URL: http://localhost:5000
Usuario: monitoreo
Contraseña: Monitoreo2025!
```

### Render (Producción)

```bash
# URL de tu app en Render
URL: https://tu-app.onrender.com
Usuario: monitoreo
Contraseña: Monitoreo2025!
```

---

## 🔒 Seguridad

### ⚠️ Contraseñas en Texto Plano

**Nota importante**: Las contraseñas se guardan en **texto plano** (sin hashear) para facilitar las pruebas en Render gratuito.

**Archivo**: `backend/models/user.py`

```python
def set_password(self, password):
    """
    Establecer contraseña en texto plano (TEMPORAL - SOLO PARA PRUEBAS)
    """
    # TEMPORAL: Guardar contraseña sin hashear para pruebas en Render gratuito
    self.password_hash = password

def check_password(self, password):
    """Verificar contraseña"""
    return self.password_hash == password
```

### 🔐 Para Producción Real

Si vas a usar el sistema en producción real, **DEBES**:

1. **Cambiar a bcrypt**:
```python
from werkzeug.security import generate_password_hash, check_password_hash

def set_password(self, password):
    self.password_hash = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password_hash, password)
```

2. **Cambiar todas las contraseñas**:
   - Usar contraseñas fuertes (mínimo 12 caracteres)
   - Incluir mayúsculas, minúsculas, números y símbolos
   - No usar contraseñas comunes como "test123"

3. **Implementar políticas de seguridad**:
   - Expiración de contraseñas
   - Bloqueo después de intentos fallidos
   - Autenticación de dos factores (2FA)

---

## 📝 Cambiar Contraseñas

### Opción 1: Desde el Super Admin Dashboard

1. Login como Super Admin
2. Ir a "Usuarios"
3. Seleccionar usuario
4. Clic en "Resetear Contraseña"
5. Ingresar nueva contraseña

### Opción 2: Desde la Base de Datos

```python
from backend.app import create_app
from backend.database import db
from backend.models.user import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(nombre='monitoreo').first()
    user.set_password('NuevaContraseñaSegura123!')
    db.session.commit()
    print(f"✅ Contraseña actualizada para {user.nombre}")
```

### Opción 3: Script de Cambio Masivo

```python
# scripts/cambiar_contraseñas.py
from backend.app import create_app
from backend.database import db
from backend.models.user import User

def cambiar_contraseñas():
    app = create_app()
    with app.app_context():
        usuarios = User.query.all()
        for user in usuarios:
            nueva_password = input(f"Nueva contraseña para {user.nombre}: ")
            user.set_password(nueva_password)
        db.session.commit()
        print("✅ Todas las contraseñas actualizadas")

if __name__ == '__main__':
    cambiar_contraseñas()
```

---

## 🔍 Verificar Contraseñas

### Script de Verificación

```python
# scripts/verificar_contraseñas.py
from backend.app import create_app
from backend.models.user import User

def verificar_contraseñas():
    app = create_app()
    with app.app_context():
        usuarios = [
            ('monitoreo', 'Monitoreo2025!'),
            ('auditor', 'test123'),
            ('coord_dept', 'test123'),
            ('coord_mun', 'test123'),
            ('coord_puesto', 'test123'),
            ('testigo1', 'test123'),
        ]
        
        print("\n🔍 Verificando contraseñas...\n")
        
        for nombre, password in usuarios:
            user = User.query.filter_by(nombre=nombre).first()
            if user:
                if user.check_password(password):
                    print(f"✅ {nombre}: Contraseña correcta")
                else:
                    print(f"❌ {nombre}: Contraseña incorrecta")
            else:
                print(f"⚠️  {nombre}: Usuario no encontrado")

if __name__ == '__main__':
    verificar_contraseñas()
```

---

## 📊 Tabla de Accesos por Rol

| Rol | Dashboard | Funciones Principales |
|-----|-----------|----------------------|
| **Monitoreo** | `/monitoreo/dashboard` | Ver métricas en tiempo real, mapa de testigos, gráficos |
| **Auditor Electoral** | `/auditor/dashboard` | Auditoría de formularios, reportes, logs |
| **Coordinador Departamental** | `/coordinador/departamental` | Validar formularios, gestionar coordinadores |
| **Coordinador Municipal** | `/coordinador/municipal` | Validar formularios, gestionar testigos |
| **Coordinador de Puesto** | `/coordinador/puesto` | Validar formularios de su puesto |
| **Testigo Electoral** | `/testigo/dashboard` | Registrar formularios E-14, reportar incidentes |

---

## 🆘 Problemas Comunes

### Problema: "Contraseña incorrecta"

**Solución**:
1. Verificar que estás usando la contraseña correcta:
   - `monitoreo`: `Monitoreo2025!` (con mayúscula y signo de exclamación)
   - Otros: `test123` (todo minúsculas)

2. Verificar en la base de datos:
```python
from backend.models.user import User
user = User.query.filter_by(nombre='monitoreo').first()
print(f"Contraseña guardada: {user.password_hash}")
```

3. Reinicializar datos:
```bash
python scripts/inicializar_datos_automatico.py
```

### Problema: "Usuario no encontrado"

**Solución**:
1. Verificar que los usuarios existen:
```bash
python scripts/verificar_y_cargar_datos_completo.py
```

2. Si no existen, inicializar:
```bash
python scripts/inicializar_datos_automatico.py
```

### Problema: "Contraseñas diferentes en local y Render"

**Solución**:
1. Verificar que ambos usan el mismo script de inicialización
2. Verificar que `render_setup.py` llama a `inicializar_datos_automatico.py`
3. Redesplegar en Render para forzar reinicialización

---

## 📚 Referencias

### Archivos Relacionados
- `scripts/inicializar_datos_automatico.py` - Script de inicialización
- `render_setup.py` - Setup para Render
- `backend/models/user.py` - Modelo de usuario
- `backend/routes/auth.py` - Rutas de autenticación

### Documentación Relacionada
- `docs/INICIALIZACION_AUTOMATICA.md` - Guía de inicialización
- `docs/CONFIGURACION_SUPER_ADMIN.md` - Guía del Super Admin
- `docs/PRUEBAS_SISTEMA.md` - Guía de pruebas

---

## ⚠️ RECORDATORIO FINAL

**ESTAS CONTRASEÑAS SON PARA DESARROLLO Y PRUEBAS ÚNICAMENTE**

En producción real:
1. ✅ Cambiar todas las contraseñas
2. ✅ Usar contraseñas fuertes
3. ✅ Implementar bcrypt para hashear
4. ✅ Implementar políticas de seguridad
5. ✅ Implementar 2FA si es posible

---

**Fecha**: 29 de Noviembre 2025  
**Versión**: 1.0  
**Estado**: ✅ DOCUMENTADO
