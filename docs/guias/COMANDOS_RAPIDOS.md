# ⚡ Comandos Rápidos - Sistema de Testigos Electorales

## 🚀 Inicio Rápido

### Primera Vez (Instalación Completa)
```bash
# Windows
setup.bat

# Linux/Mac
chmod +x setup.sh && ./setup.sh
```

### Inicio Diario
```bash
# Windows
start.bat

# Linux/Mac
./start.sh
```

---

## 🔧 Comandos de Desarrollo

### Activar Entorno Virtual
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Iniciar Servidor
```bash
python run.py
```

### Inicializar Sistema Completo
```bash
python setup.py
```

---

## 🗄️ Base de Datos

### Crear Base de Datos
```bash
python scripts/init_db.py
```

### Cargar Ubicaciones (DIVIPOLA)
```bash
python scripts/load_divipola.py
```

### Crear Usuarios
```bash
python scripts/create_fixed_users.py
```

### Aplicar Migración de Geolocalización
```bash
python backend/migrations/apply_user_geolocation.py
```

### Reiniciar Base de Datos Completa
```bash
# Windows
del instance\testigos.db
python setup.py

# Linux/Mac
rm instance/testigos.db
python setup.py
```

---

## 🔍 Verificación

### Verificación Completa del Sistema
```bash
python verificacion_completa_sistema.py
```

### Diagnóstico de Inicialización
```bash
python diagnostico_inicializacion.py
```

### Verificación Rápida (Windows)
```bash
check_system.bat
```

### Verificar Correcciones del Testigo
```bash
python test_testigo_fix.py
```

---

## 🌐 Despliegue en Render

### Preparar para Despliegue
```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

### Verificar Estado en Render
```bash
# Acceder a: https://dashboard.render.com
# Ver logs del servicio
```

---

## 🧪 Testing

### Ejecutar Tests
```bash
pytest
```

### Ejecutar Tests con Cobertura
```bash
pytest --cov=backend
```

### Test de Todos los Roles
```bash
python test_all_roles.py
```

---

## 📊 Información del Sistema

### Ver Usuarios en BD
```bash
python -c "from backend.app import create_app; from backend.models.user import User; app = create_app(); app.app_context().push(); print(f'Usuarios: {User.query.count()}')"
```

### Ver Ubicaciones en BD
```bash
python -c "from backend.app import create_app; from backend.models.location import Location; app = create_app(); app.app_context().push(); print(f'Ubicaciones: {Location.query.count()}')"
```

### Ver Formularios en BD
```bash
python -c "from backend.app import create_app; from backend.models.formulario_e14 import FormularioE14; app = create_app(); app.app_context().push(); print(f'Formularios: {FormularioE14.query.count()}')"
```

---

## 🔐 Gestión de Usuarios

### Cambiar Contraseña de Usuario
```python
# Ejecutar en Python shell
from backend.app import create_app
from backend.models.user import User
from backend.database import db

app = create_app()
with app.app_context():
    user = User.query.filter_by(nombre='admin').first()
    user.set_password('nueva_contraseña')
    db.session.commit()
    print('Contraseña actualizada')
```

### Crear Usuario Manualmente
```python
from backend.app import create_app
from backend.models.user import User
from backend.database import db

app = create_app()
with app.app_context():
    user = User(
        nombre='nuevo_usuario',
        rol='testigo_electoral',
        activo=True
    )
    user.set_password('contraseña123')
    db.session.add(user)
    db.session.commit()
    print(f'Usuario creado: {user.id}')
```

---

## 🐛 Debugging

### Ver Logs del Servidor
```bash
# Los logs aparecen en la consola donde ejecutaste run.py
python run.py
```

### Ver Logs en Render
```bash
# Dashboard de Render → Tu servicio → Logs
```

### Limpiar Caché de Python
```bash
# Windows
del /s /q __pycache__
del /s /q *.pyc

# Linux/Mac
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

---

## 📦 Gestión de Dependencias

### Actualizar Dependencias
```bash
pip install --upgrade -r requirements.txt
```

### Agregar Nueva Dependencia
```bash
pip install nombre-paquete
pip freeze > requirements.txt
```

### Ver Dependencias Instaladas
```bash
pip list
```

---

## 🔄 Git

### Estado del Repositorio
```bash
git status
```

### Agregar Cambios
```bash
git add .
```

### Commit
```bash
git commit -m "Descripción de cambios"
```

### Push
```bash
git push origin main
```

### Ver Historial
```bash
git log --oneline
```

### Crear Branch
```bash
git checkout -b nombre-branch
```

---

## 🧹 Limpieza

### Limpiar Entorno Virtual
```bash
# Windows
rmdir /s /q .venv

# Linux/Mac
rm -rf .venv
```

### Limpiar Base de Datos
```bash
# Windows
del instance\testigos.db

# Linux/Mac
rm instance/testigos.db
```

### Limpiar Todo y Reiniciar
```bash
# Windows
rmdir /s /q .venv
del instance\testigos.db
setup.bat

# Linux/Mac
rm -rf .venv
rm instance/testigos.db
./setup.sh
```

---

## 📱 Acceso Rápido

### URLs Locales
- **Aplicación:** http://localhost:5000
- **Login:** http://localhost:5000/login
- **API:** http://localhost:5000/api/

### Credenciales por Defecto
```
Super Admin:
  Usuario: admin
  Password: admin123

Coordinador:
  Usuario: coord_dpto_caqueta
  Password: coord123

Testigo:
  Usuario: testigo_01_1
  Password: testigo123
```

---

## 🆘 Solución Rápida de Problemas

### Error: "No pyvenv.cfg file"
```bash
rmdir /s /q .venv  # Windows
rm -rf .venv       # Linux/Mac
python -m venv .venv
```

### Error: "Base de datos no encontrada"
```bash
python setup.py
```

### Error: "Puerto 5000 en uso"
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID [número] /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Error: "No module named 'backend'"
```bash
pip install -r requirements.txt
```

### Error: "Usuarios no creados"
```bash
python scripts/create_fixed_users.py
```

---

## 📚 Documentación Rápida

### Ver Documentación
```bash
# Windows
start README.md

# Linux/Mac
open README.md  # Mac
xdg-open README.md  # Linux
```

### Documentos Importantes
- `README.md` - Documentación principal
- `INICIO_RAPIDO.md` - Guía de inicio
- `GUIA_DESPLIEGUE.md` - Guía de despliegue
- `CHECKLIST_FUNCIONALIDADES.md` - Checklist de pruebas
- `ESTADO_SISTEMA_FINAL.md` - Estado del sistema

---

## 💡 Tips

### Desarrollo Rápido
```bash
# Terminal 1: Servidor
python run.py

# Terminal 2: Logs
tail -f logs/app.log  # Si tienes logs en archivo
```

### Backup Rápido
```bash
# Backup de BD
copy instance\testigos.db instance\testigos.db.backup  # Windows
cp instance/testigos.db instance/testigos.db.backup    # Linux/Mac
```

### Restaurar Backup
```bash
# Restaurar BD
copy instance\testigos.db.backup instance\testigos.db  # Windows
cp instance/testigos.db.backup instance/testigos.db    # Linux/Mac
```

---

**Última actualización:** Noviembre 22, 2025
**Versión:** 1.0.0

*Guarda este archivo para referencia rápida* 📌
