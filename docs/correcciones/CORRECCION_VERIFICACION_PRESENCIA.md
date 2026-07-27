# Corrección: Verificación de Presencia Automática

## 🔴 Problema

El sistema estaba verificando la presencia del testigo **automáticamente** al cargar el dashboard, ANTES de que el testigo seleccionara su mesa. Esto causaba:

1. ❌ Llamadas al endpoint `/api/verificacion/presencia` sin mesa seleccionada
2. ❌ Errores en los logs porque no había contexto de mesa
3. ❌ Confusión para el usuario
4. ❌ Datos incorrectos en el sistema

## ✅ Solución Implementada

La verificación de presencia ahora se ejecuta **SOLO** cuando el testigo:

1. Selecciona su mesa del dropdown
2. Hace clic en el botón "Verificar Presencia"

### Cambios en `verificacion-presencia.js`

#### ANTES (Incorrecto):
```javascript
init() {
    console.log('VerificacionPresencia: Inicializando...');
    
    // ❌ Verificaba presencia automáticamente al cargar
    this.verificarPresenciaInicial();
    
    // Iniciaba ping automático inmediatamente
    this.iniciarPingAutomatico();
    
    // ...
}
```

#### DESPUÉS (Correcto):
```javascript
init() {
    console.log('VerificacionPresencia: Inicializando...');
    
    // ✅ NO verifica presencia automáticamente
    // La presencia se verifica SOLO cuando el testigo hace clic en "Verificar Presencia"
    
    // Iniciar ping automático solo si ya hay presencia verificada
    const presenciaYaVerificada = sessionStorage.getItem('presencia_verificada');
    if (presenciaYaVerificada) {
        console.log('Presencia ya verificada previamente, iniciando ping automático');
        this.iniciarPingAutomatico();
    } else {
        console.log('Presencia no verificada aún, esperando acción del usuario');
    }
    
    // ...
}
```

### Flujo Correcto de Verificación

```
1. Testigo inicia sesión
   ↓
2. Dashboard carga (NO se verifica presencia)
   ↓
3. Testigo selecciona su mesa del dropdown
   ↓
4. Testigo hace clic en "Verificar Presencia"
   ↓
5. Sistema obtiene geolocalización (si está disponible)
   ↓
6. Sistema llama a /api/verificacion/presencia con:
   - mesa_id (de la mesa seleccionada)
   - latitud y longitud (si están disponibles)
   ↓
7. Backend actualiza:
   - user.presencia_verificada = True
   - user.presencia_verificada_at = now()
   - user.ubicacion_id = mesa_id
   - user.ultima_latitud = latitud
   - user.ultima_longitud = longitud
   ↓
8. Frontend inicia ping automático cada 5 minutos
   ↓
9. Testigo puede crear formularios E-14
```

## 🔧 Mejoras Adicionales

### 1. Ping Automático Inteligente

El ping automático ahora solo se inicia DESPUÉS de verificar presencia:

```javascript
async verificarPresencia(latitud = null, longitud = null) {
    // ... código de verificación ...
    
    if (data.success) {
        // Marcar presencia como verificada
        sessionStorage.setItem('presencia_verificada', 'true');
        
        // ✅ Iniciar ping automático DESPUÉS de verificar presencia
        if (!this.pingInterval) {
            console.log('Iniciando ping automático después de verificar presencia');
            this.iniciarPingAutomatico();
        }
        
        return data.data;
    }
}
```

### 2. Persistencia de Estado

Se usa `sessionStorage` para recordar si la presencia ya fue verificada:

- **Primera vez**: No hay ping automático hasta que el usuario verifique
- **Recarga de página**: Si ya verificó antes, el ping automático se reanuda
- **Nueva sesión**: Se requiere nueva verificación

## 📊 Impacto de la Corrección

### Antes:
```
Logs del servidor:
❌ POST /api/verificacion/presencia - 400 Bad Request (sin mesa_id)
❌ POST /api/verificacion/presencia - 400 Bad Request (sin mesa_id)
❌ POST /api/verificacion/presencia - 400 Bad Request (sin mesa_id)
```

### Después:
```
Logs del servidor:
✅ (Silencio hasta que el usuario haga clic en "Verificar Presencia")
✅ POST /api/verificacion/presencia - 200 OK (con mesa_id correcto)
✅ POST /api/verificacion/ping - 200 OK (cada 5 minutos)
```

## 🔍 Cómo Verificar la Corrección

### 1. Abrir Dashboard del Testigo

1. Ir a https://dia-d.onrender.com/auth/login
2. Iniciar sesión como testigo (ej: `testigo_01_1` / `testigo123`)
3. Abrir DevTools (F12) → Pestaña "Console"
4. Abrir DevTools (F12) → Pestaña "Network"

### 2. Verificar que NO hay llamadas automáticas

En la pestaña "Network", NO deberías ver:
- ❌ Llamadas a `/api/verificacion/presencia` al cargar
- ❌ Errores 400 o 500

En la consola, deberías ver:
```
VerificacionPresencia: Inicializando...
Presencia no verificada aún, esperando acción del usuario
```

### 3. Seleccionar Mesa y Verificar

1. Seleccionar una mesa del dropdown
2. Hacer clic en "Verificar Presencia"
3. En "Network", deberías ver:
   - ✅ POST `/api/verificacion/presencia` → 200 OK
4. En la consola, deberías ver:
   ```
   Presencia verificada: {...}
   Iniciando ping automático después de verificar presencia
   Ping automático iniciado (cada 5 minutos)
   ```

### 4. Verificar Ping Automático

Después de 5 minutos, deberías ver en "Network":
- ✅ POST `/api/verificacion/ping` → 200 OK

## 📝 Archivos Modificados

```
✅ frontend/static/js/verificacion-presencia.js
   - Eliminada verificación automática en init()
   - Ping automático solo después de verificar presencia
   - Mejor manejo de sessionStorage

✅ CORRECCION_VERIFICACION_PRESENCIA.md
   - Este documento
```

## 🚀 Despliegue

```bash
git add -A
git commit -m "Fix: Eliminar verificación automática de presencia

- La presencia ahora se verifica SOLO cuando el testigo hace clic en el botón
- Ping automático se inicia DESPUÉS de verificar presencia
- Eliminadas llamadas automáticas al endpoint /api/verificacion/presencia
- Mejor manejo de sessionStorage para persistencia de estado"

git push origin main
```

## ✅ Resultado Esperado

Después del despliegue:

1. ✅ NO hay llamadas automáticas a `/api/verificacion/presencia`
2. ✅ NO hay errores en los logs del servidor
3. ✅ El testigo debe seleccionar su mesa primero
4. ✅ El testigo debe hacer clic en "Verificar Presencia"
5. ✅ Solo entonces se verifica la presencia y se inicia el ping automático
6. ✅ Los logs del servidor están limpios

---

**Fecha**: 22 de Noviembre de 2025  
**Problema**: Verificación automática de presencia sin mesa seleccionada  
**Solución**: Verificación manual solo cuando el usuario hace clic en el botón
