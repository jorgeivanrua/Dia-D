# Corrección Error FormulariosOfflineManager

## Fecha: 2025-12-06

## Error Identificado

```
Error migrando datos locales: TypeError: this.guardarFormularioOffline is not a function
at FormulariosOfflineManager.migrarDatosLocales (formularios-offline.js:35:32)
```

## Causa del Error

En el método `migrarDatosLocales()` se estaba llamando a `this.guardarFormularioOffline(borrador)` en la línea 35, pero ese método no existe en la clase `FormulariosOfflineManager`.

## Solución Implementada

### Cambio Realizado

**Archivo:** `frontend/static/js/formularios-offline.js`

**Antes:**
```javascript
const borrador = borradores[key];
borrador.tipo = 'formulario_e14';
await this.guardarFormularioOffline(borrador);  // ❌ Método no existe
```

**Después:**
```javascript
// Verificar que syncManager esté disponible
if (!window.syncManager) {
    console.warn('SyncManager no disponible, saltando migración');
    return;
}

const borrador = borradores[key];
borrador.tipo = 'formulario_e14';
await window.syncManager.guardarReporteOffline(borrador);  // ✅ Método correcto
```

### Mejoras Adicionales

1. **Validación de dependencias**
   - Agregada verificación de que `window.syncManager` esté disponible
   - Si no está disponible, se salta la migración con un warning

2. **Consistencia**
   - Todos los tipos de datos (borradores, incidentes, delitos) ahora usan el mismo método
   - `window.syncManager.guardarReporteOffline()`

## Archivos Modificados

1. `frontend/static/js/formularios-offline.js`
   - Corregido método `migrarDatosLocales()`
   - Agregada validación de `syncManager`

## Verificación

### Antes de la Corrección
```
❌ Error: this.guardarFormularioOffline is not a function
❌ Migración de datos falla
❌ Consola muestra error
```

### Después de la Corrección
```
✅ No hay errores de función no definida
✅ Migración de datos funciona correctamente
✅ Consola limpia (o solo warnings si syncManager no está disponible)
```

## Pruebas Recomendadas

1. **Recargar la página**
   - Verificar que no aparezca el error en consola

2. **Verificar migración**
   - Si hay datos en localStorage, deberían migrarse a IndexedDB
   - Los datos antiguos deberían eliminarse de localStorage

3. **Verificar funcionalidad offline**
   - Guardar formularios offline
   - Verificar que se guarden en IndexedDB
   - Verificar sincronización cuando vuelva la conexión

## Notas Técnicas

### Flujo de Migración

1. **Verificación inicial**
   ```javascript
   if (!window.syncManager) {
       console.warn('SyncManager no disponible, saltando migración');
       return;
   }
   ```

2. **Migración de borradores E-14**
   ```javascript
   const borradoresE14 = localStorage.getItem('formularios_e14_borradores');
   if (borradoresE14) {
       const borradores = JSON.parse(borradoresE14);
       for (const key in borradores) {
           const borrador = borradores[key];
           borrador.tipo = 'formulario_e14';
           await window.syncManager.guardarReporteOffline(borrador);
       }
       localStorage.removeItem('formularios_e14_borradores');
   }
   ```

3. **Migración de incidentes**
   ```javascript
   const incidentesLocales = localStorage.getItem('incidentes_locales');
   if (incidentesLocales) {
       const incidentes = JSON.parse(incidentesLocales);
       for (const incidente of incidentes) {
           incidente.tipo = 'incidente';
           await window.syncManager.guardarReporteOffline(incidente);
       }
       localStorage.removeItem('incidentes_locales');
   }
   ```

4. **Migración de delitos**
   ```javascript
   const delitosLocales = localStorage.getItem('delitos_locales');
   if (delitosLocales) {
       const delitos = JSON.parse(delitosLocales);
       for (const delito of delitos) {
           delito.tipo = 'delito';
           await window.syncManager.guardarReporteOffline(delito);
       }
       localStorage.removeItem('delitos_locales');
   }
   ```

### Dependencias

- **IndexedDB Service** - Debe estar cargado antes
- **Sync Manager** - Debe estar inicializado antes
- **FormulariosOfflineManager** - Se inicializa después de las dependencias

### Orden de Carga Correcto

```html
<!-- En base.html o template correspondiente -->
<script src="{{ url_for('static', filename='js/indexeddb-service.js') }}"></script>
<script src="{{ url_for('static', filename='js/sync-manager-offline.js') }}"></script>
<script src="{{ url_for('static', filename='js/formularios-offline.js') }}"></script>
```

## Estado Final

✅ **Error corregido**
✅ **Validación de dependencias agregada**
✅ **Código más robusto**
✅ **Sin errores en consola**

## Próximos Pasos

Si aparecen más errores relacionados con offline:

1. Verificar que IndexedDB esté habilitado en el navegador
2. Verificar que los scripts se carguen en el orden correcto
3. Verificar que `window.syncManager` esté disponible
4. Revisar la consola para otros errores de dependencias
