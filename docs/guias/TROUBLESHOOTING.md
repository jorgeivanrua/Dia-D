# 🔧 Guía de Solución de Problemas

## Problemas Comunes y Soluciones

---

## 🔴 Problemas de Instalación

### Error: "Python no está instalado"

**Síntoma:**
```
'python' no se reconoce como un comando interno o externo
```

**Solución:**
1. Instala Python 3.8 o superior desde [python.org](https://python.org)
2. Durante la instalación, marca "Add Python to PATH"
3. Reinicia la terminal
4. Verifica: `python --version`

---

### Error: "No se puede crear el entorno virtual"

**Síntoma:**
```
Error: No module named 'venv'
```

**Solución:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-venv

# Fedora/CentOS
sudo dnf install python3-venv

# Windows
# Reinstala Python con todas las opciones
```

---

### Error: "pip install falla"

**Síntoma:**
```
ERROR: Could not install packages due to an OSError
```

**Solución:**
```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar con permisos de usuario
pip install -r requirements.txt --user

# Limpiar caché
pip cache purge
pip install -r requirements.txt
```

---

## 🔴 Problemas de Base de Datos

### Error: "Base de datos no encontrada"

**Síntoma:**
```
sqlite3.OperationalError: unable to open database file
```

**Solución:**
```bash
# Crear directorio instance si no existe
mkdir instance

# Inicializar sistema
python scripts/init_system.py
```

---

### Error: "Base de datos corrupta"

**Síntoma:**
```
sqlite3.DatabaseError: database disk image is malformed
```

**Solución:**
```bash
# Hacer backup
cp instance/electoral.db instance/electoral_backup.db

# Limpiar y reinicializar
python scripts/clean_system.py
python scripts/init_system.py
```

---

### Error: "No such column: users.es_usuario_basico"

**Síntoma:**
```
sqlite3.OperationalError: no such column: users.es_usuario_basico
```

**Solución:**
```bash
# Aplicar migración
python backend/migrations/add_es_usuario_basico.py

# O reinicializar
python scripts/clean_system.py
python scripts/init_system.py
```

---

## 🔴 Problemas de Autenticación

### Error: "Credenciales inválidas"

**Síntoma:**
Login falla con usuario y contraseña correctos

**Solución:**
```bash
# Verificar que las contraseñas estén hasheadas
python scripts/check_system.py

# Si están en texto plano, resetear
python scripts/init_system.py --reset-passwords
```

**Contraseñas por defecto:**
- Super Admin: `admin123`
- Otros usuarios: `test123`

---

### Error: "Cuenta bloqueada"

**Síntoma:**
```
Cuenta bloqueada por múltiples intentos fallidos
```

**Solución:**
```bash
# Esperar 1 minuto (bloqueo temporal)
# O desbloquear manualmente con endpoint de emergencia
```

---

## 🔴 Problemas de Puerto

### Error: "Puerto 5000 en uso"

**Síntoma:**
```
OSError: [Errno 48] Address already in use
```

**Solución:**

**Windows:**
```bash
# Ver qué proceso usa el puerto
netstat -ano | findstr :5000

# Matar proceso (reemplaza PID)
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
# Ver qué proceso usa el puerto
lsof -i :5000

# Matar proceso
kill -9 <PID>
```

**O usar otro puerto:**
```bash
# Editar .env
PORT=5001

# O ejecutar directamente
PORT=5001 python run.py
```

---

## 🔴 Problemas de Dependencias

### Error: "ModuleNotFoundError"

**Síntoma:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solución:**
```bash
# Activar entorno virtual
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

---

### Error: "Versión incompatible"

**Síntoma:**
```
ImportError: cannot import name 'X' from 'Y'
```

**Solución:**
```bash
# Reinstalar dependencias
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# O recrear entorno virtual
rm -rf .venv
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
pip install -r requirements.txt
```

---

## 🔴 Problemas de Datos

### Error: "No hay ubicaciones"

**Síntoma:**
Sistema funciona pero no hay departamentos/municipios

**Solución:**
```bash
# Verificar archivo DIVIPOLA
ls "todos los datos/divipola.csv"

# Cargar ubicaciones
python scripts/load_divipola.py
```

---

### Error: "No hay usuarios"

**Síntoma:**
No se puede hacer login, no existen usuarios

**Solución:**
```bash
# Crear usuarios básicos
python scripts/init_system.py

# Verificar
python scripts/check_system.py
```

---

## 🔴 Problemas de Permisos

### Error: "Permission denied"

**Síntoma:**
```
PermissionError: [Errno 13] Permission denied
```

**Solución:**

**Windows:**
```bash
# Ejecutar como administrador
# O cambiar permisos del directorio
```

**Linux/Mac:**
```bash
# Cambiar permisos
chmod -R 755 .

# O ejecutar con sudo (no recomendado)
sudo python run.py
```

---

## 🔴 Problemas de Render/Producción

### Error: "Build failed"

**Síntoma:**
Despliegue en Render falla

**Solución:**
1. Verificar `requirements.txt` está actualizado
2. Verificar `runtime.txt` tiene versión correcta de Python
3. Verificar `build.sh` tiene permisos de ejecución
4. Revisar logs de Render para error específico

---

### Error: "Database not initialized"

**Síntoma:**
App en Render arranca pero no tiene datos

**Solución:**
```bash
# Usar endpoint de inicialización
curl -X POST https://tu-app.onrender.com/init-db-manual

# O usar endpoint de emergencia
curl -X POST https://tu-app.onrender.com/api/emergency/emergency-create-users \
  -H "Content-Type: application/json" \
  -d '{"emergency_key": "tu-clave-secreta"}'
```

---

## 🔧 Comandos de Diagnóstico

### Verificar Sistema Completo

```bash
python scripts/check_system.py
```

### Verificar Base de Datos

```bash
python -c "
from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location

app = create_app()
with app.app_context():
    print(f'Usuarios: {User.query.count()}')
    print(f'Ubicaciones: {Location.query.count()}')
"
```

### Verificar Contraseñas

```bash
python -c "
from backend.app import create_app
from backend.models.user import User

app = create_app()
with app.app_context():
    user = User.query.first()
    print(f'Hash length: {len(user.password_hash)}')
    print(f'Is hashed: {len(user.password_hash) > 50}')
"
```

---

## 🆘 Solución Nuclear

Si nada funciona, resetea todo:

```bash
# 1. Limpiar sistema
python scripts/clean_system.py

# 2. Eliminar entorno virtual
rm -rf .venv  # o rmdir /s .venv en Windows

# 3. Reinstalar todo
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate
pip install -r requirements.txt

# 4. Reinicializar
python scripts/init_system.py

# 5. Verificar
python scripts/check_system.py

# 6. Iniciar
python run.py
```

---

## 📞 Obtener Ayuda

Si el problema persiste:

1. **Revisa los logs:**
   - `logs/app.log` (si existe)
   - Terminal output

2. **Ejecuta diagnóstico:**
   ```bash
   python scripts/check_system.py > diagnostico.txt
   ```

3. **Recopila información:**
   - Sistema operativo
   - Versión de Python
   - Mensaje de error completo
   - Pasos para reproducir

4. **Contacta soporte:**
   - Crea un issue en GitHub
   - Incluye el archivo `diagnostico.txt`
   - Incluye logs relevantes

---

## 📚 Documentación Adicional

- **Guía de Seguridad:** `docs/SEGURIDAD.md`
- **Análisis del Sistema:** `ANALISIS_INICIO_LOCAL.md`
- **Guía de Scripts:** `scripts/README_NUEVO.md`

---

**Última actualización:** 30 de Noviembre de 2024  
**Versión:** 1.1.0
