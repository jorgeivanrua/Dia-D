# ⚡ Inicio Rápido - Sistema de Testigos Electorales

## 🎯 Para Empezar en 2 Minutos

### Windows
```bash
setup.bat
start.bat
```

### Linux/Mac
```bash
chmod +x setup.sh start.sh
./setup.sh
./start.sh
```

### Acceso
- URL: `http://localhost:5000`
- Usuario: `admin`
- Password: `admin123`

---

## 📦 ¿Qué Incluye el Sistema?

### Scripts de Inicialización

| Script | Descripción | Cuándo Usar |
|--------|-------------|-------------|
| `setup.py` | Inicialización completa del sistema | Primera vez o reset completo |
| `setup.bat` / `setup.sh` | Wrapper que crea entorno virtual + setup.py | Primera instalación |
| `start.bat` / `start.sh` | Inicia el servidor de desarrollo | Cada vez que quieras trabajar |
| `render_setup.py` | Inicialización para Render.com | Despliegue en producción |

### Estructura de Archivos

```
📁 Sistema de Testigos
├── 📄 setup.py              # Inicialización completa
├── 📄 setup.bat/sh          # Instalación automática
├── 📄 start.bat/sh          # Inicio rápido del servidor
├── 📄 render_setup.py       # Setup para Render
├── 📄 render.yaml           # Configuración de Render
├── 📄 run.py                # Servidor Flask
├── 📄 requirements.txt      # Dependencias Python
│
├── 📁 backend/              # Lógica del servidor
│   ├── 📁 models/          # Modelos de datos
│   ├── 📁 routes/          # Endpoints API
│   ├── 📁 migrations/      # Migraciones de BD
│   └── 📄 app.py           # Aplicación Flask
│
├── 📁 frontend/             # Interfaz de usuario
│   ├── 📁 static/          # CSS, JS, imágenes
│   └── 📁 templates/       # HTML templates
│
├── 📁 scripts/              # Scripts de utilidad
│   ├── 📄 init_db.py       # Crear base de datos
│   ├── 📄 load_divipola.py # Cargar ubicaciones
│   └── 📄 create_fixed_users.py # Crear usuarios
│
└── 📁 instance/             # Base de datos SQLite
    └── 📄 testigos.db
```

---

## 🚀 Escenarios Comunes

### Primera Instalación

```bash
# Windows
setup.bat

# Linux/Mac
./setup.sh
```

Esto hace:
1. ✅ Crea entorno virtual
2. ✅ Instala dependencias
3. ✅ Crea base de datos
4. ✅ Carga ubicaciones
5. ✅ Crea usuarios
6. ✅ Aplica migraciones

### Iniciar el Servidor

```bash
# Windows
start.bat

# Linux/Mac
./start.sh

# O directamente
python run.py
```

### Reiniciar Base de Datos

```bash
# Activar entorno virtual primero
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

python setup.py
```

### Desplegar en Render

1. Sube tu código a GitHub
2. Conecta el repo en Render
3. Render ejecuta automáticamente `render_setup.py`
4. ¡Listo!

---

## 👥 Usuarios Disponibles

### Después de `setup.py` o `setup.bat/sh`:

| Tipo | Usuario | Password | Descripción |
|------|---------|----------|-------------|
| **Super Admin** | admin | admin123 | Acceso total |
| **Admin Dpto** | admin_caqueta | admin123 | Admin departamental |
| **Admin Mun** | admin_florencia | admin123 | Admin municipal |
| **Coord Dpto** | coord_dpto_caqueta | coord123 | Coordinador departamental |
| **Coord Mun** | coord_mun_florencia | coord123 | Coordinador municipal |
| **Coord Puesto** | coord_puesto_XX | coord123 | Coordinador de puesto |
| **Testigo** | testigo_XX_1 | testigo123 | Testigo electoral |
| **Auditor** | auditor_caqueta | auditor123 | Auditor electoral |

---

## 🔧 Comandos Útiles

### Desarrollo

```bash
# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar nueva dependencia
pip install nombre-paquete
pip freeze > requirements.txt

# Ejecutar tests
pytest

# Ver logs
python run.py
```

### Base de Datos

```bash
# Reiniciar BD completa
python setup.py

# Solo crear usuarios
python scripts/create_fixed_users.py

# Solo cargar ubicaciones
python scripts/load_divipola.py

# Aplicar migración específica
python backend/migrations/apply_user_geolocation.py
```

### Producción

```bash
# Render (automático)
git push origin main

# Heroku
git push heroku main
heroku run python render_setup.py

# VPS
sudo systemctl restart testigos
```

---

## 🐛 Solución Rápida de Problemas

### "No se encuentra Python"
```bash
# Instala Python 3.8+
# Windows: https://python.org
# Linux: sudo apt install python3
# Mac: brew install python3
```

### "Puerto 5000 en uso"
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID [número] /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### "Base de datos no encontrada"
```bash
python setup.py
```

### "No hay usuarios"
```bash
python scripts/create_fixed_users.py
```

### "Error de módulos"
```bash
pip install -r requirements.txt
```

---

## 📚 Documentación Completa

- **[README.md](README.md)** - Documentación general
- **[GUIA_DESPLIEGUE.md](GUIA_DESPLIEGUE.md)** - Guía completa de despliegue
- **[GUIA_PRUEBAS_MANUALES.md](GUIA_PRUEBAS_MANUALES.md)** - Cómo probar el sistema

---

## ✅ Checklist de Verificación

Después de ejecutar `setup.bat` o `setup.sh`:

- [ ] Servidor inicia sin errores
- [ ] Puedes acceder a `http://localhost:5000`
- [ ] Login con `admin` / `admin123` funciona
- [ ] Ves el dashboard de super admin
- [ ] Hay usuarios en el sistema
- [ ] Hay ubicaciones cargadas (si tienes divipola.csv)

---

## 🎓 Próximos Pasos

1. **Explora el sistema**
   - Login con diferentes roles
   - Prueba crear formularios
   - Revisa los dashboards

2. **Personaliza**
   - Cambia contraseñas
   - Configura partidos políticos
   - Carga tus ubicaciones

3. **Despliega**
   - Sigue [GUIA_DESPLIEGUE.md](GUIA_DESPLIEGUE.md)
   - Configura dominio
   - Activa HTTPS

---

## 💡 Tips

- **Desarrollo**: Usa `start.bat` o `start.sh` para inicio rápido
- **Reset**: Ejecuta `setup.py` para reiniciar todo
- **Producción**: Usa `render_setup.py` en Render
- **Backups**: Copia `instance/testigos.db` regularmente
- **Logs**: Revisa la consola para errores

---

## 📞 ¿Necesitas Ayuda?

1. Revisa esta guía
2. Consulta [GUIA_DESPLIEGUE.md](GUIA_DESPLIEGUE.md)
3. Revisa los logs en la consola
4. Abre un issue en GitHub

---

**¡Listo para empezar! 🚀**

Ejecuta `setup.bat` (Windows) o `./setup.sh` (Linux/Mac) y en 2 minutos tendrás el sistema funcionando.
