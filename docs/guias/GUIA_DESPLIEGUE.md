# 🚀 Guía de Despliegue - Sistema de Testigos Electorales

## 📋 Tabla de Contenidos
- [Desarrollo Local](#desarrollo-local)
- [Despliegue en Render](#despliegue-en-render)
- [Despliegue en Heroku](#despliegue-en-heroku)
- [Despliegue en VPS](#despliegue-en-vps)
- [Solución de Problemas](#solución-de-problemas)

---

## 💻 Desarrollo Local

### Inicio Rápido (Recomendado)

**Windows:**
```bash
# 1. Inicializar el sistema
setup.bat

# 2. Iniciar el servidor
start.bat
```

**Linux/Mac:**
```bash
# 1. Dar permisos de ejecución
chmod +x setup.sh start.sh

# 2. Inicializar el sistema
./setup.sh

# 3. Iniciar el servidor
./start.sh
```

### Inicio Manual

```bash
# 1. Crear entorno virtual
python -m venv .venv

# 2. Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Inicializar sistema
python setup.py

# 5. Iniciar servidor
python run.py
```

### Verificar Instalación

Accede a: `http://localhost:5000`

Credenciales por defecto:
- Usuario: `admin`
- Password: `admin123`

---

## 🌐 Despliegue en Render

### Opción 1: Despliegue Automático (Recomendado)

1. **Preparar el repositorio**
   ```bash
   # Asegúrate de tener estos archivos:
   # - render.yaml
   # - render_setup.py
   # - requirements.txt
   # - run.py
   
   git add .
   git commit -m "Preparar para despliegue en Render"
   git push origin main
   ```

2. **Crear servicio en Render**
   - Ve a [dashboard.render.com](https://dashboard.render.com)
   - Click en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Render detectará automáticamente `render.yaml`
   - Click en "Create Web Service"

3. **Configuración automática**
   - El archivo `render.yaml` configura todo automáticamente
   - `render_setup.py` inicializa la base de datos
   - Las variables de entorno se generan automáticamente

4. **Subir archivo DIVIPOLA** (Opcional)
   - Si tienes el archivo `divipola.csv`, súbelo a la carpeta `todos los datos/`
   - O cárgalo manualmente después del despliegue

### Opción 2: Configuración Manual

1. **Crear Web Service**
   - New + → Web Service
   - Conectar repositorio

2. **Configuración del Build**
   ```
   Build Command:
   pip install -r requirements.txt && python render_setup.py
   
   Start Command:
   gunicorn run:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   ```

3. **Variables de Entorno**
   ```
   FLASK_ENV=production
   SECRET_KEY=[generar valor aleatorio]
   JWT_SECRET_KEY=[generar valor aleatorio]
   PYTHONUNBUFFERED=1
   RENDER=true
   ```

4. **Base de Datos** (Opcional - PostgreSQL)
   - Crear PostgreSQL Database (Free tier)
   - Conectar a Web Service
   - Render configurará `DATABASE_URL` automáticamente

### Verificar Despliegue

1. Espera a que termine el build (5-10 minutos)
2. Accede a la URL proporcionada por Render
3. Login con: `admin` / `admin123`
4. **Cambia la contraseña inmediatamente**

---

## 🔴 Despliegue en Heroku

### Preparación

1. **Instalar Heroku CLI**
   ```bash
   # Windows (con Chocolatey)
   choco install heroku-cli
   
   # Mac
   brew tap heroku/brew && brew install heroku
   
   # Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login en Heroku**
   ```bash
   heroku login
   ```

### Despliegue

```bash
# 1. Crear aplicación
heroku create nombre-de-tu-app

# 2. Agregar PostgreSQL (recomendado)
heroku addons:create heroku-postgresql:mini

# 3. Configurar variables de entorno
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
heroku config:set JWT_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')

# 4. Crear Procfile
echo "web: gunicorn run:app --bind 0.0.0.0:\$PORT" > Procfile

# 5. Crear runtime.txt
echo "python-3.11.0" > runtime.txt

# 6. Deploy
git add .
git commit -m "Preparar para Heroku"
git push heroku main

# 7. Inicializar base de datos
heroku run python render_setup.py

# 8. Abrir aplicación
heroku open
```

---

## 🖥️ Despliegue en VPS (Ubuntu/Debian)

### Requisitos
- Ubuntu 20.04+ o Debian 11+
- Acceso root o sudo
- Dominio (opcional)

### Instalación

```bash
# 1. Actualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar dependencias
sudo apt install -y python3 python3-pip python3-venv nginx git

# 3. Clonar repositorio
cd /var/www
sudo git clone https://github.com/tu-usuario/testigos.git
cd testigos

# 4. Configurar entorno
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 5. Inicializar sistema
python setup.py

# 6. Configurar Gunicorn
pip install gunicorn

# 7. Crear servicio systemd
sudo nano /etc/systemd/system/testigos.service
```

**Contenido de testigos.service:**
```ini
[Unit]
Description=Sistema de Testigos Electorales
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/testigos
Environment="PATH=/var/www/testigos/.venv/bin"
Environment="FLASK_ENV=production"
ExecStart=/var/www/testigos/.venv/bin/gunicorn run:app --bind 127.0.0.1:8000 --workers 4

[Install]
WantedBy=multi-user.target
```

```bash
# 8. Iniciar servicio
sudo systemctl start testigos
sudo systemctl enable testigos

# 9. Configurar Nginx
sudo nano /etc/nginx/sites-available/testigos
```

**Contenido de configuración Nginx:**
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /var/www/testigos/frontend/static;
    }
}
```

```bash
# 10. Activar sitio
sudo ln -s /etc/nginx/sites-available/testigos /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 11. Configurar SSL (opcional pero recomendado)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

---

## 🔧 Solución de Problemas

### Error: "Base de datos no encontrada"

**Solución:**
```bash
python setup.py
```

### Error: "No module named 'backend'"

**Solución:**
```bash
# Asegúrate de estar en el directorio correcto
cd /ruta/al/proyecto

# Reinstala dependencias
pip install -r requirements.txt
```

### Error: "Port already in use"

**Solución:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID [número_de_proceso] /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Error: "Cannot connect to database"

**Solución en Render/Heroku:**
```bash
# Verificar DATABASE_URL
heroku config:get DATABASE_URL  # Heroku
# O revisar en Render Dashboard

# Reinicializar base de datos
heroku run python render_setup.py  # Heroku
# O usar Render Shell
```

### Error: "Usuarios no creados"

**Solución:**
```bash
python scripts/create_fixed_users.py
```

### Error: "Ubicaciones no cargadas"

**Solución:**
```bash
# Verificar que existe el archivo
ls "todos los datos/divipola.csv"

# Cargar manualmente
python scripts/load_divipola.py
```

### Logs en Producción

**Render:**
- Dashboard → Tu servicio → Logs

**Heroku:**
```bash
heroku logs --tail
```

**VPS:**
```bash
sudo journalctl -u testigos -f
```

---

## 📊 Checklist de Despliegue

### Antes del Despliegue
- [ ] Código en repositorio Git
- [ ] Archivo `divipola.csv` disponible
- [ ] Variables de entorno configuradas
- [ ] Dependencias actualizadas en `requirements.txt`

### Durante el Despliegue
- [ ] Build exitoso
- [ ] Base de datos inicializada
- [ ] Usuarios creados
- [ ] Ubicaciones cargadas

### Después del Despliegue
- [ ] Aplicación accesible
- [ ] Login funciona
- [ ] Cambiar contraseñas por defecto
- [ ] Verificar funcionalidades principales
- [ ] Configurar backups (producción)
- [ ] Configurar SSL/HTTPS

---

## 🔐 Seguridad en Producción

### Cambios Obligatorios

1. **Cambiar todas las contraseñas**
   ```
   admin → [contraseña segura]
   coord_* → [contraseñas únicas]
   testigo_* → [contraseñas únicas]
   ```

2. **Generar claves secretas únicas**
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

3. **Configurar HTTPS**
   - Usar Certbot (VPS)
   - Render/Heroku lo incluyen automáticamente

4. **Configurar backups**
   - Base de datos diaria
   - Archivos subidos

5. **Monitoreo**
   - Logs de acceso
   - Alertas de errores
   - Uso de recursos

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa esta guía
2. Consulta los logs
3. Abre un issue en GitHub
4. Contacta al equipo de desarrollo

---

**Última actualización:** Noviembre 2025
