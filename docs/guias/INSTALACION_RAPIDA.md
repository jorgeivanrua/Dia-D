# Instalación Rápida - MVP Sistema Electoral

## Requisitos Previos

- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- Git (opcional)

## Pasos de Instalación

### 1. Clonar o Descargar el Proyecto

```bash
# Si tienes Git
git clone <url-repositorio>
cd sistema-electoral

# O descargar y extraer el ZIP
```

### 2. Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=dev-jwt-secret-change-in-production
DATABASE_URL=sqlite:///electoral.db
UPLOAD_FOLDER=app/static/uploads
```

### 5. Inicializar Base de Datos

```bash
# Crear estructura de base de datos
python mvp/scripts/init_mvp_db.py

# Cargar datos de prueba
python mvp/scripts/load_sample_data.py
```

### 6. Ejecutar Aplicación

```bash
python run.py
```

La aplicación estará disponible en: **http://localhost:5000**

## Usuarios de Prueba

### Superadmin
- **Email:** admin@sistema.com
- **Password:** Admin123!
- **Acceso:** Dashboard de administración completo

### Coordinador de Puesto 1
- **Email:** coord.puesto1@sistema.com
- **Password:** Coord123!
- **Acceso:** Validación de E-14 del Puesto 1

### Coordinador de Puesto 2
- **Email:** coord.puesto2@sistema.com
- **Password:** Coord123!
- **Acceso:** Validación de E-14 del Puesto 2

### Testigos Electorales
- **Email:** testigo.p1m1@sistema.com (Mesa 1, Puesto 1)
- **Email:** testigo.p1m2@sistema.com (Mesa 2, Puesto 1)
- **Email:** testigo.p1m3@sistema.com (Mesa 3, Puesto 1)
- **Email:** testigo.p2m1@sistema.com (Mesa 1, Puesto 2)
- **Email:** testigo.p2m2@sistema.com (Mesa 2, Puesto 2)
- **Password:** Testigo123! (todos)
- **Acceso:** Captura de E-14 de su mesa asignada

## Estructura de Datos de Prueba

### Ubicaciones
- **Departamento:** Antioquia (05)
  - **Municipio:** Medellín (001)
    - **Puesto:** Colegio San José (001)
      - Mesa 001, 002, 003

- **Departamento:** Cundinamarca (25)
  - **Municipio:** Bogotá D.C. (001)
    - **Puesto:** Universidad Nacional (001)
      - Mesa 001, 002

### Formularios E-14 de Prueba
- 1 formulario en estado **Borrador**
- 2 formularios en estado **Enviado** (pendientes de aprobación)
- 1 formulario **Aprobado**
- 1 formulario **Rechazado**

## Flujo de Prueba Recomendado

### 1. Login como Testigo
```
1. Ir a http://localhost:5000/login
2. Ingresar: testigo.p1m1@sistema.com / Testigo123!
3. Ver dashboard con formularios de la mesa asignada
4. Crear nuevo formulario E-14
5. Completar datos y enviar
```

### 2. Login como Coordinador
```
1. Cerrar sesión
2. Ingresar: coord.puesto1@sistema.com / Coord123!
3. Ver formularios pendientes de aprobación
4. Revisar formulario enviado por testigo
5. Aprobar o rechazar con justificación
```

### 3. Login como Admin
```
1. Cerrar sesión
2. Ingresar: admin@sistema.com / Admin123!
3. Ver estadísticas generales
4. Gestionar usuarios
5. Crear nuevo usuario de prueba
```

## Verificación de Instalación

### Verificar Base de Datos
```bash
python check_db.py
```

### Verificar Ubicaciones DIVIPOLA
```bash
python check_divipola.py
```

### Ejecutar Tests (opcional)
```bash
python -m pytest tests/
```

## Solución de Problemas Comunes

### Error: "No module named 'flask'"
```bash
# Asegurarse de que el entorno virtual está activado
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "Database not found"
```bash
# Reinicializar base de datos
python mvp/scripts/init_mvp_db.py
python mvp/scripts/load_sample_data.py
```

### Error: "Port 5000 already in use"
```bash
# Cambiar puerto en run.py o matar proceso
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Error: "JWT token expired"
```bash
# Limpiar localStorage del navegador
# O cerrar sesión y volver a iniciar
```

## Próximos Pasos

1. ✅ Explorar los dashboards por rol
2. ✅ Probar flujo completo de captura y validación E-14
3. ✅ Crear usuarios adicionales
4. ✅ Revisar documentación en `mvp/REQUERIMIENTOS_MVP.md`
5. ✅ Revisar diseño técnico en `mvp/DISEÑO_MVP.md`
6. ✅ Consultar plan de tareas en `mvp/TAREAS_MVP.md`

## Soporte

Para problemas o preguntas:
1. Revisar documentación en carpeta `docs/`
2. Verificar logs en `logs/sistema_electoral.log`
3. Consultar código fuente en `mvp/backend/`

## Despliegue en Producción

Para desplegar en producción, consultar:
- `docs/04_GUIA_DESARROLLO.md`
- Configurar variables de entorno de producción
- Usar PostgreSQL en lugar de SQLite
- Configurar Gunicorn y Nginx
- Habilitar HTTPS con certificado SSL

---

**¡Listo para usar!** 🚀

El MVP está configurado y funcionando. Puedes comenzar a explorar las funcionalidades básicas del sistema electoral.
