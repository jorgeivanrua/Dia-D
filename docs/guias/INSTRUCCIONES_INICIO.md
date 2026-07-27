# 🚀 Instrucciones de Inicio - Sistema de Testigos Electorales

## ✅ Sistema Inicializado Correctamente

La base de datos ha sido creada exitosamente con:
- ✅ Todas las tablas creadas
- ✅ Ubicaciones cargadas (DIVIPOLA - Caquetá)
- ✅ Usuarios del sistema creados
- ✅ Migraciones aplicadas
- ✅ Configuración electoral lista

---

## 🎯 Para Iniciar el Servidor

### Opción 1: Usando el Script de Inicio (Recomendado)

Abre una **nueva terminal** y ejecuta:

```bash
# Windows
start.bat

# O manualmente:
.venv\Scripts\activate
python run.py
```

### Opción 2: Comando Directo

```bash
# Activar entorno virtual
.venv\Scripts\activate

# Iniciar servidor
python run.py
```

---

## 🌐 Acceder a la Aplicación

Una vez que el servidor esté corriendo, verás un mensaje como:

```
>> Iniciando aplicacion en modo development
>> Servidor corriendo en http://0.0.0.0:5000
>> Base de datos: sqlite:///C:\mvp\instance\testigos.db
 * Serving Flask app 'backend.app'
 * Debug mode: on
```

**Abre tu navegador y ve a:**
```
http://localhost:5000
```

---

## 🔐 Credenciales de Acceso

### Super Administrador
```
Usuario: admin
Password: admin123
```

### Coordinador Departamental
```
Usuario: coord_dpto_caqueta
Password: coord123
```

### Coordinador Municipal
```
Usuario: coord_mun_florencia
Password: coord123
```

### Coordinador de Puesto
```
Usuario: coord_puesto_01
Password: coord123
```

### Testigo Electoral
```
Usuario: testigo_01_1
Password: testigo123
```

### Auditor
```
Usuario: auditor_caqueta
Password: auditor123
```

---

## 🔧 Solución de Problemas

### El servidor no inicia

1. **Verifica que el entorno virtual esté activado:**
   ```bash
   # Deberías ver (.venv) al inicio de la línea de comando
   .venv\Scripts\activate
   ```

2. **Verifica que las dependencias estén instaladas:**
   ```bash
   pip list | findstr Flask
   ```

3. **Verifica que la base de datos existe:**
   ```bash
   dir instance\testigos.db
   ```

### Puerto 5000 en uso

Si ves un error de "Address already in use":

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID [número_del_proceso] /F

# Luego intenta de nuevo
python run.py
```

### Error de módulos no encontrados

```bash
pip install -r requirements.txt
```

---

## 📊 Verificar que Todo Funciona

1. **Servidor corriendo:** Deberías ver logs en la terminal
2. **Página de login:** http://localhost:5000 debe cargar
3. **Login exitoso:** Usa admin / admin123
4. **Dashboard carga:** Deberías ver el dashboard del super admin

---

## 🚀 Despliegue en Render

El sistema ya está configurado para Render. Solo necesitas:

1. **Subir a GitHub:**
   ```bash
   git add .
   git commit -m "Sistema listo para producción"
   git push origin main
   ```

2. **En Render Dashboard:**
   - New + → Web Service
   - Conectar repositorio
   - Render detecta `render.yaml` automáticamente
   - Click "Create Web Service"

3. **Esperar build:**
   - Render ejecuta `render_setup.py` automáticamente
   - Crea BD, usuarios, y aplica migraciones
   - Inicia con gunicorn

4. **Acceder:**
   - URL proporcionada por Render
   - Login: admin / admin123
   - **¡Cambiar contraseña inmediatamente!**

---

## 📝 Notas Importantes

### Para Desarrollo Local
- El servidor se ejecuta en modo DEBUG
- Los cambios en el código se recargan automáticamente
- Los logs son más detallados

### Para Producción (Render)
- El servidor usa gunicorn
- Modo DEBUG desactivado
- Variables de entorno seguras
- HTTPS automático

---

## 🎉 ¡Listo!

El sistema está completamente funcional. Disfruta desarrollando con el Sistema de Testigos Electorales.

**Documentación adicional:**
- `README.md` - Documentación principal
- `INICIO_RAPIDO.md` - Guía de inicio rápido
- `GUIA_DESPLIEGUE.md` - Guía completa de despliegue
- `COMANDOS_RAPIDOS.md` - Comandos útiles

---

**Fecha:** Noviembre 23, 2025
**Estado:** ✅ Sistema Inicializado y Listo
