# Troubleshooting - Errores en Render

## 🔴 Problema Actual

### Error 1: Variable PORT incorrecta
```
Error: 'SPORT' is not a valid port number.
```

**Causa:** Render está interpretando mal la variable `$PORT` como `SPORT`

**Solución:**
1. Ir a Dashboard de Render → Servicio "dia-d" → Settings
2. Verificar "Start Command"
3. Debe decir: `gunicorn run:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
4. Si dice algo diferente, corregir y guardar
5. Hacer "Manual Deploy" → "Clear build cache & deploy"

### Error 2: Endpoints 404
```
GET /api/locations/departamentos 404 (Not Found)
```

**Causa:** El servidor en Render no se ha actualizado con los últimos cambios

**Solución:**
1. Verificar que el último commit se desplegó correctamente
2. Revisar logs de build en Render
3. Si el build falló, hacer redeploy manual
4. Verificar que no haya errores de sintaxis en Python

## 🔧 Pasos para Resolver

### Paso 1: Verificar Configuración en Render

1. **Ir a Dashboard:**
   - https://dashboard.render.com
   - Seleccionar servicio "dia-d"

2. **Verificar Settings:**
   - Start Command debe ser: `gunicorn run:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - Build Command debe ser: `pip install -r requirements.txt && python render_setup.py`
   - Environment debe tener:
     - `FLASK_ENV=production`
     - `SECRET_KEY` (auto-generado)
     - `JWT_SECRET_KEY` (auto-generado)
     - `PYTHONUNBUFFERED=1`
     - `RENDER=true`

3. **Verificar Logs:**
   - Ir a "Logs" tab
   - Buscar errores de Python
   - Verificar que dice "Build successful"
   - Verificar que dice "Your service is live"

### Paso 2: Limpiar Caché y Redesplegar

1. **En Dashboard de Render:**
   - Ir a "Manual Deploy"
   - Seleccionar "Clear build cache & deploy"
   - Esperar a que complete (5-10 minutos)

2. **Verificar nuevo despliegue:**
   - Revisar logs en tiempo real
   - Confirmar que no hay errores
   - Verificar que el servicio inicia correctamente

### Paso 3: Probar Endpoints

Una vez desplegado, probar en el navegador:

```
https://dia-d.onrender.com/api/locations/departamentos
```

Debe retornar:
```json
{
  "success": true,
  "data": [{
    "departamento_codigo": "44",
    "departamento_nombre": "CAQUETA"
  }]
}
```

## 🐛 Errores Comunes

### Error: "Module not found"
**Solución:** Verificar que todas las dependencias estén en `requirements.txt`

### Error: "Database not found"
**Solución:** El script `render_setup.py` debe crear la BD automáticamente

### Error: "Port already in use"
**Solución:** Render maneja esto automáticamente, no debería pasar

### Error: "Timeout"
**Solución:** Aumentar timeout en start command: `--timeout 120`

## 📋 Checklist de Verificación

- [ ] Último commit pusheado a GitHub
- [ ] Build en Render completado sin errores
- [ ] Start Command correcto (`$PORT` no `SPORT`)
- [ ] Variables de entorno configuradas
- [ ] Logs no muestran errores de Python
- [ ] Servicio marcado como "Live"
- [ ] Endpoint `/api/locations/departamentos` responde
- [ ] Login carga lista de departamentos

## 🔄 Si Nada Funciona

### Opción 1: Redesplegar desde cero

1. En Render Dashboard, ir a Settings
2. Scroll hasta el final
3. Click en "Delete Service"
4. Crear nuevo servicio desde GitHub
5. Usar configuración de `render.yaml`

### Opción 2: Usar SQLite local temporalmente

1. Comentar configuración de PostgreSQL en `render.yaml`
2. Usar SQLite (ya configurado por defecto)
3. Redesplegar

### Opción 3: Revisar render_setup.py

Verificar que el script de setup funciona:
```bash
python render_setup.py
```

## 📞 Información de Contacto

- **Logs de Render:** https://dashboard.render.com/web/[service-id]/logs
- **Documentación Render:** https://render.com/docs
- **Repositorio GitHub:** https://github.com/jorgeivanrua/mvp

## 🧪 Script de Verificación

Ejecuta este script para verificar que los endpoints funcionan:

```bash
python test_render_endpoints.py
```

Este script probará:
- `/api/locations/departamentos` - Debe retornar Caquetá
- `/api/locations/municipios/44` - Debe retornar municipios
- `/api/locations/zonas/4401` - Debe retornar zonas de Florencia
- `/auth/login` - Debe cargar la página de login

## ⏱️ Tiempos de Despliegue

- **Build:** 3-5 minutos
- **Deploy:** 2-3 minutos
- **Total:** 5-8 minutos aproximadamente

**Nota:** Los servicios gratuitos de Render se duermen después de 15 minutos de inactividad. La primera petición puede tardar 30-60 segundos en responder mientras el servicio se "despierta".

## 🔍 Verificar Estado del Despliegue

1. Ve a: https://dashboard.render.com
2. Busca el servicio "dia-d"
3. Verifica que diga "Live" (verde)
4. Si dice "Building" o "Deploying", espera a que termine
5. Si dice "Failed", revisa los logs

---

**Última actualización:** 2025-11-27  
**Estado:** Cambios pusheados - Esperando redespliegue automático en Render (~5-8 minutos)
