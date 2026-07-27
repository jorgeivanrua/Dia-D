# 🔒 Usuarios Básicos Fijos del Sistema

## Concepto

Los **usuarios básicos fijos** son 6 usuarios que SIEMPRE existen en el sistema, independientemente de las ubicaciones o configuraciones. Son como las ubicaciones: datos fundamentales que se crean automáticamente en cada despliegue.

## Los 6 Usuarios Básicos Fijos

| Usuario | Rol | Contraseña | Ubicación | Modificable |
|---------|-----|-----------|-----------|-------------|
| Super Admin | super_admin | `admin123` | Sin ubicación | ❌ Solo super admin |
| Monitoreo | monitoreo | `test123` | Sin ubicación | ❌ Solo super admin |
| Coordinador Departamental | coordinador_departamental | `test123` | Sin ubicación | ❌ Solo super admin |
| Coordinador Municipal | coordinador_municipal | `test123` | Sin ubicación | ❌ Solo super admin |
| Coordinador Puesto | coordinador_puesto | `test123` | Sin ubicación | ❌ Solo super admin |
| Auditor Electoral | auditor_electoral | `test123` | Sin ubicación | ❌ Solo super admin |

## Características

### ✅ Siempre Existen

- Se crean automáticamente en cada despliegue
- Si ya existen, se actualizan (contraseñas, estado, etc.)
- No se pueden eliminar desde la interfaz
- Están marcados con `es_usuario_basico = True` en la BD

### 🔒 Protección

- **NO se pueden eliminar** (ni siquiera el super admin)
- **Solo el super admin** puede modificar sus contraseñas
- **Solo el super admin** puede activar/desactivar
- Los usuarios básicos **NO pueden cambiar** su propia contraseña

### 📍 Sin Ubicación

- Estos usuarios NO tienen `ubicacion_id`
- Son usuarios "globales" del sistema
- Se usan para acceso general, no para ubicaciones específicas

## Flujo de Creación en Despliegue

### 1. Build Script (`build.sh`)

```bash
echo "🗄️ Inicializando base de datos..."
python scripts/init_db.py

echo "🔄 Ejecutando migraciones..."
python backend/migrations/add_es_usuario_basico.py

echo "📍 Cargando ubicaciones..."
python scripts/load_divipola.py

echo "👥 Creando usuarios básicos fijos del sistema..."
python scripts/crear_usuarios_basicos_fijos.py

echo "👥 Creando usuarios adicionales del sistema..."
python scripts/create_fixed_users.py
```

### 2. Script de Usuarios Básicos

El script `crear_usuarios_basicos_fijos.py`:

1. **Verifica** si cada usuario básico existe
2. **Si existe**: Actualiza contraseña, desbloquea, activa
3. **Si NO existe**: Crea el usuario con contraseña correcta
4. **Marca** todos como `es_usuario_basico = True`
5. **Commit** de todos los cambios

### 3. Resultado

Después de cada despliegue:
- ✅ Los 6 usuarios básicos existen
- ✅ Tienen las contraseñas correctas
- ✅ Están desbloqueados y activos
- ✅ Están marcados como usuarios básicos fijos

## Diferencia con Otros Usuarios

### Usuarios Básicos Fijos

```python
User(
    nombre='Super Admin',
    rol='super_admin',
    ubicacion_id=None,  # Sin ubicación
    es_usuario_basico=True,  # Marcado como fijo
    password='admin123'
)
```

### Usuarios Normales

```python
User(
    nombre='testigo_4401010101_1',
    rol='testigo_electoral',
    ubicacion_id=123,  # Con ubicación específica
    es_usuario_basico=False,  # NO es fijo
    password='test123'
)
```

## Protecciones Implementadas

### 1. En el Modelo (`backend/models/user.py`)

```python
class User(db.Model):
    # ...
    es_usuario_basico = db.Column(db.Boolean, default=False, nullable=False)
```

### 2. En las Rutas de Gestión

```python
@gestion_usuarios_bp.route('/eliminar-usuario/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required(['super_admin'])
def eliminar_usuario(user_id):
    usuario = User.query.get(user_id)
    
    # Protección: No se pueden eliminar usuarios básicos
    if usuario.es_usuario_basico:
        return jsonify({
            'success': False,
            'error': 'Los usuarios básicos fijos no se pueden eliminar'
        }), 403
    
    # ... resto del código
```

### 3. En el Script de Despliegue

```python
# SIEMPRE se ejecuta en cada despliegue
python scripts/crear_usuarios_basicos_fijos.py
```

## Ventajas

### ✅ Garantía de Existencia

- Los usuarios básicos SIEMPRE existen
- No hay riesgo de que se eliminen accidentalmente
- El sistema siempre tiene usuarios funcionales

### ✅ Contraseñas Consistentes

- Después de cada despliegue, las contraseñas son conocidas
- `admin123` para super admin
- `test123` para los demás
- Fácil de documentar y compartir

### ✅ Desbloqueo Automático

- Si un usuario se bloquea, el siguiente despliegue lo desbloquea
- No hay riesgo de quedarse sin acceso

### ✅ Simplicidad

- No hay que crear usuarios manualmente
- No hay que recordar múltiples contraseñas
- Todo está automatizado

## Uso en Producción

### Primer Despliegue

1. Render ejecuta `build.sh`
2. Se crean los 6 usuarios básicos
3. Contraseñas: `admin123` y `test123`

### Despliegues Posteriores

1. Render ejecuta `build.sh`
2. Se actualizan los 6 usuarios básicos
3. Contraseñas se resetean a valores por defecto
4. Usuarios se desbloquean

### Cambiar Contraseñas en Producción

**Opción 1: Desde el Dashboard (Recomendado)**

1. Iniciar sesión como Super Admin
2. Ir a "Gestión de Usuarios"
3. Seleccionar usuario básico
4. Cambiar contraseña
5. ⚠️ La contraseña se mantendrá hasta el próximo despliegue

**Opción 2: Modificar el Script**

1. Editar `scripts/crear_usuarios_basicos_fijos.py`
2. Cambiar las contraseñas en el array `usuarios_basicos`
3. Hacer commit y push
4. Render redeploy automáticamente

```python
usuarios_basicos = [
    {
        'nombre': 'Super Admin',
        'rol': 'super_admin',
        'password': 'MiPasswordSeguro123!',  # Nueva contraseña
        'descripcion': 'Administrador principal del sistema'
    },
    # ...
]
```

## Troubleshooting

### Usuario básico no existe

**Causa**: El script no se ejecutó correctamente en el despliegue

**Solución**:
1. Revisar logs de Render
2. Ejecutar manualmente: `python scripts/crear_usuarios_basicos_fijos.py`
3. O usar endpoint de emergencia

### Contraseña no funciona

**Causa**: La contraseña fue cambiada y luego hubo un redeploy

**Solución**:
1. Usar las contraseñas por defecto: `admin123` / `test123`
2. O ejecutar endpoint de emergencia para resetear

### Usuario bloqueado

**Causa**: Múltiples intentos fallidos

**Solución**:
1. Esperar 1 minuto (bloqueo temporal)
2. O hacer un redeploy (desbloquea automáticamente)
3. O usar endpoint de emergencia

## Endpoints de Emergencia

Si necesitas resetear los usuarios básicos sin hacer redeploy:

```javascript
// Desbloquear usuarios
fetch('https://tu-app.onrender.com/api/emergency/emergency-unlock-users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ emergency_key: 'reset_passwords_2024_emergency' })
})

// Resetear contraseñas
fetch('https://tu-app.onrender.com/api/emergency/emergency-reset-passwords', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ emergency_key: 'reset_passwords_2024_emergency' })
})
```

## Resumen

Los usuarios básicos fijos son como las **ubicaciones del sistema**: datos fundamentales que siempre deben existir. Se crean automáticamente en cada despliegue, tienen contraseñas conocidas y documentadas, y solo el super admin puede modificarlos.

**Contraseñas por defecto:**
- Super Admin: `admin123`
- Todos los demás: `test123`

**Protección:**
- No se pueden eliminar
- Solo super admin puede modificar
- Se recrean/actualizan en cada despliegue

---

**Última actualización**: 30 de Noviembre de 2025
