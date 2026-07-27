# 🔧 Sistema de Inicialización - Documentación Completa

## 📋 Resumen del Sistema

El sistema ahora cuenta con scripts automatizados para facilitar la inicialización tanto en desarrollo local como en producción (Render).

### Archivos Creados

| Archivo | Propósito | Plataforma |
|---------|-----------|------------|
| `setup.py` | Script principal de inicialización | Todas |
| `setup.bat` | Wrapper para Windows | Windows |
| `setup.sh` | Wrapper para Linux/Mac | Linux/Mac |
| `start.bat` | Inicio rápido del servidor | Windows |
| `start.sh` | Inicio rápido del servidor | Linux/Mac |
| `render_setup.py` | Inicialización para Render | Render.com |
| `render.yaml` | Configuración de Render | Render.com |

---

## 🚀 Uso Básico

### Primera Vez (Instalación Completa)

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### Iniciar Servidor (Después de Instalación)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

---

## 🔍 ¿Qué Hace Cada Script?

### `setup.py` - Inicialización Completa

Ejecuta en orden:

1. **Verificación de archivos**
   - Comprueba que existen todos los archivos necesarios
   - Verifica la presencia de `divipola.csv`

2. **Inicialización de BD** (`scripts/init_db.py`)
   - Crea todas las tablas
   - Estructura completa de la base de datos

3. **Carga de ubicaciones** (`scripts/load_divipola.py`)
   - Carga departamentos, municipios, zonas, puestos y mesas
   - Solo si existe el archivo `divipola.csv`

4. **Migraciones** (`backend/migrations/apply_user_geolocation.py`)
   - Aplica campos de geolocalización a usuarios
   - Agrega: `ultima_latitud`, `ultima_longitud`, etc.

5. **Creación de usuarios** (`scripts/create_fixed_users.py`)
   - Crea usuarios del sistema por rol
   - Super admin, coordinadores, testigos, etc.

6. **Configuración electoral** (`scripts/init_configuracion_electoral.py`)
   - Carga partidos políticos
   - Configura tipos de elección
   - (Si el script existe)

7. **Tablas de formularios** (`scripts/create_formularios_e14_tables.py`)
   - Crea tablas para formularios E-14
   - (Si el script existe)

### `setup.bat` / `setup.sh` - Wrappers

Estos scripts:
1. Verifican que Python esté instalado
2. Crean el entorno virtual (`.venv`)
3. Activan el entorno virtual
4. Instalan dependencias (`pip install -r requirements.txt`)
5. Ejecutan `setup.py`

### `start.bat` / `start.sh` - Inicio Rápido

Estos scripts:
1. Verifican que existe el entorno virtual
2. Verifican que existe la base de datos
3. Si no existe BD, ejecutan `setup.py` automáticamente
4. Inician el servidor con `python run.py`

### `render_setup.py` - Para Render.com

Similar a `setup.py` pero:
- Detecta entorno de Render
- Maneja PostgreSQL si está configurado
- Verifica usuarios existentes antes de crearlos
- Optimizado para despliegue en producción

---

## 🐛 Solución de Problemas Comunes

### Error: "No pyvenv.cfg file"

**Causa:** No estás en un entorno virtual activado

**Solución:**
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# Luego ejecuta
python setup.py
```

### Error: "Base de datos no encontrada"

**Solución:**
```bash
python setup.py
```

### Error: "No module named 'backend'"

**Causa:** Dependencias no instaladas o directorio incorrecto

**Solución:**
```bash
# Verifica que estás en el directorio correcto
cd /ruta/al/proyecto

# Reinstala dependencias
pip install -r requirements.txt
```

### Error: "Archivo divipola.csv no encontrado"

**Solución:**

Opción 1 - Continuar sin ubicaciones:
```bash
# El script preguntará si quieres continuar
# Responde 's' para continuar
```

Opción 2 - Agregar el archivo:
```bash
# Coloca divipola.csv en una de estas ubicaciones:
# - todos los datos/divipola.csv
# - divipola.csv
# - data/divipola.csv
```

### Error: "Puerto 5000 en uso"

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID [número_de_proceso] /F
```

**Linux/Mac:**
```bash
lsof -ti:5000 | xargs kill -9
```

### Error: "Usuarios no creados"

**Solución:**
```bash
# Ejecutar solo el script de usuarios
python scripts/create_fixed_users.py
```

### Error: "Columnas ya existen" (Migraciones)

**Causa:** La migración ya se aplicó anteriormente

**Solución:** Este error es normal y se ignora automáticamente. No afecta el funcionamiento.

### Error: "Permission denied" (Linux/Mac)

**Causa:** Los scripts .sh no tienen permisos de ejecución

**Solución:**
```bash
chmod +x setup.sh start.sh
```

---

## 📊 Flujo de Inicialización

```
┌─────────────────┐
│   setup.bat/sh  │
└────────┬────────┘
         │
         ├─> Verificar Python
         ├─> Crear .venv
         ├─> Instalar dependencias
         │
         v
    ┌─────────┐
    │ setup.py│
    └────┬────┘
         │
         ├─> 1. Verificar archivos
         ├─> 2. init_db.py (crear tablas)
         ├─> 3. load_divipola.py (ubicaciones)
         ├─> 4. apply_user_geolocation.py (migración)
         ├─> 5. create_fixed_users.py (usuarios)
         ├─> 6. init_configuracion_electoral.py
         └─> 7. create_formularios_e14_tables.py
         
         v
    ┌──────────────┐
    │ Sistema Listo│
    └──────────────┘
```

---

## 🔄 Reiniciar el Sistema

Si necesitas empezar de cero:

```bash
# 1. Eliminar base de datos
# Windows:
del instance\testigos.db

# Linux/Mac:
rm instance/testigos.db

# 2. Reinicializar
python setup.py

# O usar el wrapper completo
# Windows:
setup.bat

# Linux/Mac:
./setup.sh
```

---

## 🌐 Despliegue en Render

### Configuración Automática

1. **Subir código a GitHub**
   ```bash
   git add .
   git commit -m "Preparar para Render"
   git push origin main
   ```

2. **Crear servicio en Render**
   - Dashboard → New + → Web Service
   - Conectar repositorio
   - Render detecta `render.yaml` automáticamente

3. **Variables de entorno** (Automáticas)
   - `SECRET_KEY`: Generada automáticamente
   - `JWT_SECRET_KEY`: Generada automáticamente
   - `FLASK_ENV`: production
   - `RENDER`: true

4. **Build Command** (Automático desde render.yaml)
   ```bash
   pip install -r requirements.txt && python render_setup.py
   ```

5. **Start Command** (Automático desde render.yaml)
   ```bash
   gunicorn run:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   ```

### Usar PostgreSQL en Render (Opcional)

Edita `render.yaml` y descomenta:

```yaml
databases:
  - name: dia-d-db
    plan: free

envVars:
  - key: DATABASE_URL
    fromDatabase:
      name: dia-d-db
      property: connectionString
```

---

## ✅ Verificación Post-Instalación

Después de ejecutar `setup.bat` o `setup.sh`, verifica:

### 1. Base de Datos
```bash
# Debe existir
ls instance/testigos.db  # Linux/Mac
dir instance\testigos.db  # Windows
```

### 2. Usuarios Creados
```bash
# Ejecutar en Python
python -c "from backend.app import create_app; from backend.models.user import User; app = create_app(); app.app_context().push(); print(f'Usuarios: {User.query.count()}')"
```

### 3. Ubicaciones Cargadas
```bash
# Ejecutar en Python
python -c "from backend.app import create_app; from backend.models.location import Location; app = create_app(); app.app_context().push(); print(f'Ubicaciones: {Location.query.count()}')"
```

### 4. Servidor Funciona
```bash
# Iniciar servidor
python run.py

# Acceder a http://localhost:5000
# Login: admin / admin123
```

---

## 📝 Logs y Debugging

### Ver logs durante inicialización

Los scripts muestran progreso en tiempo real:
- ✅ = Operación exitosa
- ❌ = Error crítico (detiene ejecución)
- ⚠️ = Advertencia (continúa ejecución)

### Logs del servidor

```bash
# El servidor muestra logs en consola
python run.py

# Verás:
# - Requests HTTP
# - Errores de aplicación
# - Queries SQL (en modo debug)
```

### Debugging de scripts

Para ver más detalles, ejecuta scripts individuales:

```bash
# Activar entorno virtual primero
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

# Ejecutar script específico
python scripts/init_db.py
python scripts/load_divipola.py
python scripts/create_fixed_users.py
```

---

## 🎯 Casos de Uso

### Desarrollo Local - Primera Vez
```bash
setup.bat  # o ./setup.sh
start.bat  # o ./start.sh
```

### Desarrollo Local - Día a Día
```bash
start.bat  # o ./start.sh
```

### Reset Completo
```bash
# Eliminar BD
del instance\testigos.db  # Windows
rm instance/testigos.db   # Linux/Mac

# Reinicializar
setup.bat  # o ./setup.sh
```

### Solo Recrear Usuarios
```bash
python scripts/create_fixed_users.py
```

### Solo Cargar Ubicaciones
```bash
python scripts/load_divipola.py
```

### Despliegue en Render
```bash
git push origin main
# Render ejecuta automáticamente render_setup.py
```

---

## 🔐 Seguridad

### Contraseñas por Defecto

**⚠️ IMPORTANTE:** Cambia estas contraseñas en producción

| Usuario | Password | Cuándo Cambiar |
|---------|----------|----------------|
| admin | admin123 | Inmediatamente en producción |
| coord_* | coord123 | Antes de dar acceso |
| testigo_* | testigo123 | Antes de dar acceso |
| admin_* | admin123 | Inmediatamente en producción |
| auditor_* | auditor123 | Antes de dar acceso |

### Claves Secretas

En producción (Render):
- `SECRET_KEY`: Se genera automáticamente
- `JWT_SECRET_KEY`: Se genera automáticamente

En desarrollo local:
- Definidas en `.env` o valores por defecto

---

## 📞 Soporte

Si encuentras problemas:

1. **Revisa esta documentación**
2. **Consulta [INICIO_RAPIDO.md](INICIO_RAPIDO.md)**
3. **Revisa [GUIA_DESPLIEGUE.md](GUIA_DESPLIEGUE.md)**
4. **Verifica los logs en consola**
5. **Abre un issue en GitHub**

---

## 🎓 Próximos Pasos

Después de la inicialización exitosa:

1. ✅ Accede a `http://localhost:5000`
2. ✅ Login con `admin` / `admin123`
3. ✅ Explora el dashboard
4. ✅ Cambia contraseñas
5. ✅ Configura partidos políticos
6. ✅ Prueba crear formularios
7. ✅ Despliega en Render

---

**Última actualización:** Noviembre 2025
