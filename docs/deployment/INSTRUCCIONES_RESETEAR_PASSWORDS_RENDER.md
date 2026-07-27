# 🔧 Instrucciones para Resetear Contraseñas en Render

## Problema
Las contraseñas no funcionan en Render. Necesitamos resetearlas.

## Solución Rápida

### Opción 1: Ejecutar Script en Consola de Render (RECOMENDADO)

1. **Ir a Render Dashboard**
   - https://dashboard.render.com
   - Seleccionar tu servicio web

2. **Abrir Shell**
   - Click en "Shell" en el menú lateral
   - Esperar a que se conecte

3. **Ejecutar el script**
   ```bash
   python scripts/fix_passwords_render.py
   ```

4. **Verificar salida**
   - Deberías ver: "✓ Contraseñas actualizadas exitosamente"
   - Lista de usuarios con sus contraseñas

---

### Opción 2: Ejecutar Comandos Directamente en Shell de Render

1. **Abrir Shell en Render**

2. **Ejecutar Python interactivo**
   ```bash
   python
   ```

3. **Copiar y pegar este código completo:**

```python
from backend.app import create_app
from backend.database import db
from backend.models.user import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Super Admin
    u = User.query.filter_by(rol='super_admin').first()
    if u:
        u.password_hash = generate_password_hash('admin123')
        u.activo = True
        u.intentos_fallidos = 0
        u.bloqueado_hasta = None
        print(f"✓ {u.nombre} → admin123")
    
    # Monitoreo
    u = User.query.filter_by(rol='monitoreo').first()
    if u:
        u.password_hash = generate_password_hash('monitoreo123')
        u.activo = True
        u.intentos_fallidos = 0
        u.bloqueado_hasta = None
        print(f"✓ {u.nombre} → monitoreo123")
    
    # Coordinador Departamental
    u = User.query.filter_by(rol='coordinador_departamental').first()
    if u:
        u.password_hash = generate_password_hash('coord_dept123')
        u.activo = True
        u.intentos_fallidos = 0
        u.bloqueado_hasta = None
        print(f"✓ {u.nombre} → coord_dept123")
    
    # Coordinador Municipal
    u = User.query.filter_by(rol='coordinador_municipal').first()
    if u:
        u.password_hash = generate_password_hash('coord_muni123')
        u.activo = True
        u.intentos_fallidos = 0
        u.bloqueado_hasta = None
        print(f"✓ {u.nombre} → coord_muni123")
    
    # Coordinador Puesto
    u = User.query.filter_by(rol='coordinador_puesto').first()
    if u:
        u.password_hash = generate_password_hash('coord_puesto123')
        u.activo = True
        u.intentos_fallidos = 0
        u.bloqueado_hasta = None
        print(f"✓ {u.nombre} → coord_puesto123")
    
    # Auditor Electoral
    u = User.query.filter_by(rol='auditor_electoral').first()
    if u:
        u.password_hash = generate_password_hash('auditor123')
        u.activo = True
        u.intentos_fallidos = 0
        u.bloqueado_hasta = None
        print(f"✓ {u.nombre} → auditor123")
    
    # Guardar cambios
    db.session.commit()
    print("\n✓✓✓ CONTRASEÑAS ACTUALIZADAS ✓✓✓")
```

4. **Salir de Python**
   ```python
   exit()
   ```

---

### Opción 3: Crear Usuarios si No Existen

Si los usuarios no existen en la base de datos, ejecutar:

```bash
python scripts/crear_usuarios_basicos.py
```

---

## Contraseñas Actualizadas

Después de ejecutar el script, estas serán las contraseñas:

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| Super Admin | `admin123` | super_admin |
| Monitoreo | `monitoreo123` | monitoreo |
| Coordinador Departamental | `coord_dept123` | coordinador_departamental |
| Coordinador Municipal | `coord_muni123` | coordinador_municipal |
| Coordinador Puesto | `coord_puesto123` | coordinador_puesto |
| Auditor Electoral | `auditor123` | auditor_electoral |

---

## Verificar que Funcionó

1. **Ir al login de tu aplicación**
   - https://tu-app.onrender.com/auth/login

2. **Probar con Monitoreo**
   - Usuario: `Monitoreo`
   - Contraseña: `monitoreo123`

3. **Si funciona**
   - ✅ Las contraseñas están correctas
   - Puedes iniciar sesión con cualquier usuario

4. **Si NO funciona**
   - Verificar que el script se ejecutó sin errores
   - Verificar que los usuarios existen en la BD
   - Revisar logs de Render

---

## Troubleshooting

### Error: "Usuario no encontrado"

Los usuarios no existen en la base de datos. Ejecutar:

```bash
python scripts/crear_usuarios_basicos.py
```

### Error: "Module not found"

Asegurarse de estar en el directorio raíz del proyecto:

```bash
cd /opt/render/project/src
python scripts/fix_passwords_render.py
```

### Error: "Database connection failed"

Verificar que las variables de entorno están configuradas en Render:
- `DATABASE_URL`
- `SECRET_KEY`
- `JWT_SECRET_KEY`

### Los usuarios están bloqueados

El script ya resetea los intentos fallidos y desbloquea usuarios automáticamente.

---

## Después de Resetear

1. **Probar login** con cada usuario
2. **Cambiar contraseñas** a unas más seguras en producción
3. **Documentar** las nuevas contraseñas de forma segura
4. **Eliminar** este archivo de instrucciones si contiene información sensible

---

## Comandos Útiles en Render Shell

```bash
# Ver usuarios en la base de datos
python -c "from backend.app import create_app; from backend.models.user import User; app = create_app(); app.app_context().push(); users = User.query.all(); [print(f'{u.id} | {u.nombre} | {u.rol} | Activo: {u.activo}') for u in users]"

# Ver logs de la aplicación
tail -f /var/log/render.log

# Reiniciar servicio (desde dashboard de Render)
# Manual Restart → Restart Service
```

---

## Contacto

Si tienes problemas, revisar:
1. Logs de Render
2. Variables de entorno
3. Estado de la base de datos
4. Conexión a PostgreSQL

---

**Última actualización**: 30 de Noviembre de 2025
