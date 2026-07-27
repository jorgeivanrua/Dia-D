# 🔒 Guía de Seguridad del Sistema Electoral

## ⚠️ IMPORTANTE: Configuración de Seguridad en Producción

### 1. Variables de Entorno Críticas

**OBLIGATORIAS en producción:**

```bash
# Claves secretas (NUNCA usar valores por defecto)
SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria-aqui
JWT_SECRET_KEY=otra-clave-secreta-diferente-para-jwt

# Entorno
FLASK_ENV=production
DEBUG=False

# Base de datos (usar PostgreSQL en producción)
DATABASE_URL=postgresql://usuario:password@host:puerto/database
```

**OPCIONALES (solo para emergencias):**

```bash
# Endpoints de emergencia (mantener deshabilitados)
EMERGENCY_RESET_KEY=clave-super-secreta-solo-para-emergencias
ALLOW_EMERGENCY_ENDPOINTS=false  # Cambiar a true SOLO en emergencias
```

### 2. Contraseñas

#### ✅ Implementación Actual (SEGURA)

El sistema ahora usa **hashing seguro de contraseñas** con Werkzeug:

```python
# Al crear/actualizar usuario
usuario.set_password('contraseña_texto_plano')  # Se hashea automáticamente

# Al verificar login
usuario.check_password('contraseña_ingresada')  # Compara con hash
```

#### 🔐 Contraseñas por Defecto

**IMPORTANTE:** Estas contraseñas DEBEN cambiarse inmediatamente después del primer despliegue:

| Usuario | Contraseña por Defecto | Acción Requerida |
|---------|------------------------|------------------|
| Super Admin | `admin123` | ⚠️ CAMBIAR INMEDIATAMENTE |
| Monitoreo | `test123` | ⚠️ CAMBIAR INMEDIATAMENTE |
| Coordinadores | `test123` | ⚠️ CAMBIAR INMEDIATAMENTE |
| Auditor | `test123` | ⚠️ CAMBIAR INMEDIATAMENTE |

#### 📋 Política de Contraseñas

Al cambiar contraseña, el sistema valida:

- ✅ Mínimo 8 caracteres
- ✅ Al menos una mayúscula
- ✅ Al menos una minúscula
- ✅ Al menos un número

**Recomendación:** Usar contraseñas de 12+ caracteres con símbolos especiales.

### 3. Endpoints de Emergencia

#### 🚨 Uso de Endpoints de Emergencia

Los endpoints en `/api/emergency/*` están **deshabilitados por defecto en producción**.

**Para habilitarlos (SOLO EN EMERGENCIAS):**

1. Configurar variable de entorno:
   ```bash
   EMERGENCY_RESET_KEY=tu-clave-secreta-muy-segura
   ALLOW_EMERGENCY_ENDPOINTS=true
   ```

2. Usar con la clave secreta:
   ```bash
   curl -X POST https://tu-app.com/api/emergency/emergency-reset-passwords \
     -H "Content-Type: application/json" \
     -d '{"emergency_key": "tu-clave-secreta-muy-segura"}'
   ```

3. **IMPORTANTE:** Deshabilitar inmediatamente después de usar:
   ```bash
   ALLOW_EMERGENCY_ENDPOINTS=false
   ```

#### 📋 Endpoints Disponibles

| Endpoint | Descripción | Uso |
|----------|-------------|-----|
| `/emergency-reset-passwords` | Resetea contraseñas de usuarios básicos | Solo emergencias |
| `/emergency-create-users` | Crea usuarios básicos si no existen | Primera instalación |
| `/emergency-unlock-users` | Desbloquea usuarios bloqueados | Emergencias |
| `/emergency-list-users` | Lista todos los usuarios | Diagnóstico |

### 4. Protección contra Ataques

#### 🛡️ Medidas Implementadas

1. **Bloqueo por Intentos Fallidos**
   - Después de 5 intentos fallidos, la cuenta se bloquea por 1 minuto
   - Se registra en logs para auditoría

2. **Tokens JWT**
   - Expiración: 1 hora (access token)
   - Refresh token: 7 días
   - Firmados con clave secreta

3. **CORS Configurado**
   - Solo permite orígenes autorizados
   - Headers de seguridad configurados

4. **Validación de Datos**
   - Validación en backend de todos los inputs
   - Sanitización de datos de usuario

#### 🔍 Monitoreo de Seguridad

**Revisar logs regularmente:**

```bash
# Ver intentos de login fallidos
grep "Credenciales inválidas" logs/app.log

# Ver cuentas bloqueadas
grep "Cuenta bloqueada" logs/app.log

# Ver accesos a endpoints de emergencia
grep "emergency" logs/app.log
```

### 5. Checklist de Seguridad Pre-Producción

Antes de desplegar a producción, verificar:

- [ ] `SECRET_KEY` configurada con valor aleatorio largo
- [ ] `JWT_SECRET_KEY` configurada con valor aleatorio diferente
- [ ] `FLASK_ENV=production`
- [ ] `DEBUG=False`
- [ ] Base de datos PostgreSQL configurada (no SQLite)
- [ ] Todas las contraseñas por defecto cambiadas
- [ ] `ALLOW_EMERGENCY_ENDPOINTS=false` o no configurada
- [ ] HTTPS habilitado en el servidor
- [ ] Logs configurados y monitoreados
- [ ] Backups de base de datos configurados

### 6. Respuesta a Incidentes

#### 🚨 Si se detecta acceso no autorizado:

1. **Inmediato:**
   - Cambiar todas las claves secretas (`SECRET_KEY`, `JWT_SECRET_KEY`)
   - Resetear contraseñas de todos los usuarios
   - Revisar logs de acceso

2. **Corto plazo:**
   - Auditar todos los cambios en la base de datos
   - Verificar integridad de datos
   - Notificar a usuarios afectados

3. **Largo plazo:**
   - Implementar autenticación de dos factores (2FA)
   - Agregar más logging y alertas
   - Revisar y actualizar políticas de seguridad

### 7. Mejores Prácticas

#### ✅ DO (Hacer)

- ✅ Usar HTTPS en producción
- ✅ Cambiar contraseñas regularmente
- ✅ Revisar logs de seguridad
- ✅ Mantener dependencias actualizadas
- ✅ Hacer backups regulares
- ✅ Usar variables de entorno para secretos
- ✅ Implementar rate limiting en API

#### ❌ DON'T (No Hacer)

- ❌ Commitear archivos `.env` al repositorio
- ❌ Usar contraseñas por defecto en producción
- ❌ Dejar `DEBUG=True` en producción
- ❌ Compartir claves secretas por email/chat
- ❌ Usar SQLite en producción
- ❌ Dejar endpoints de emergencia habilitados
- ❌ Ignorar alertas de seguridad

### 8. Contacto de Seguridad

Si encuentras una vulnerabilidad de seguridad:

1. **NO** la publiques públicamente
2. Contacta al equipo de desarrollo directamente
3. Proporciona detalles técnicos y pasos para reproducir
4. Espera confirmación antes de divulgar

---

## 📚 Referencias

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)

---

**Última actualización:** Noviembre 2024
**Versión:** 1.0
