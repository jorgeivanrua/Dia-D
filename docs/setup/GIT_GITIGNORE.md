# Configuración de Git y .gitignore

## Fecha: 2025-12-07

## Archivos que NO deben estar en Git

### Configuración Local
- ✅ `.kiro/` - Configuración del IDE Kiro (agregado)
- ✅ `.vscode/` - Configuración de VS Code
- ✅ `.idea/` - Configuración de IntelliJ/PyCharm
- ✅ `.env` - Variables de entorno locales
- ✅ `.env.local` - Variables de entorno locales

### Entornos Virtuales
- ✅ `.venv/` - Entorno virtual Python
- ✅ `venv/` - Entorno virtual Python
- ✅ `ENV/` - Entorno virtual Python
- ✅ `env/` - Entorno virtual Python

### Base de Datos
- ✅ `*.db` - Archivos de base de datos SQLite
- ✅ `*.sqlite` - Archivos SQLite
- ✅ `*.sqlite3` - Archivos SQLite
- ✅ `instance/` - Carpeta de instancia Flask

### Archivos Temporales
- ✅ `__pycache__/` - Cache de Python
- ✅ `*.pyc` - Bytecode de Python
- ✅ `*.tmp` - Archivos temporales
- ✅ `*.bak` - Backups
- ✅ `*.swp` - Archivos swap de editores
- ✅ `*.log` - Logs

### Uploads y Datos
- ✅ `uploads/*` - Archivos subidos (excepto .gitkeep)
- ✅ `*.backup` - Backups
- ✅ `*_backup_*` - Backups con timestamp

### Testing
- ✅ `.pytest_cache/` - Cache de pytest
- ✅ `.coverage` - Cobertura de tests
- ✅ `htmlcov/` - Reportes de cobertura

### Sistema Operativo
- ✅ `.DS_Store` - Archivos de macOS
- ✅ `Thumbs.db` - Archivos de Windows

## Archivos que SÍ deben estar en Git

### Código Fuente
- ✅ `backend/` - Código backend
- ✅ `frontend/` - Código frontend
- ✅ `scripts/` - Scripts del proyecto

### Configuración Base
- ✅ `.env.example` - Ejemplo de variables de entorno
- ✅ `.gitignore` - Este archivo
- ✅ `.editorconfig` - Configuración del editor
- ✅ `.pre-commit-config.yaml` - Hooks de pre-commit
- ✅ `.python-version` - Versión de Python

### Documentación
- ✅ `docs/` - Toda la documentación
- ✅ `README.md` - Documentación principal
- ✅ `CHANGELOG.md` - Registro de cambios
- ✅ `CONTRIBUTING.md` - Guía de contribución
- ✅ `LICENSE` - Licencia

### Configuración del Proyecto
- ✅ `requirements.txt` - Dependencias
- ✅ `requirements-dev.txt` - Dependencias de desarrollo
- ✅ `pyproject.toml` - Configuración del proyecto
- ✅ `pytest.ini` - Configuración de pytest
- ✅ `Makefile` - Comandos make

### Deploy
- ✅ `Procfile` - Configuración de Heroku/Render
- ✅ `render.yaml` - Configuración de Render
- ✅ `runtime.txt` - Runtime para deploy

### Migraciones
- ✅ `migrations/` - Migraciones de base de datos

### Scripts de Setup
- ✅ `setup.py` - Script de instalación
- ✅ `setup.sh` - Setup para Linux/Mac
- ✅ `setup.bat` - Setup para Windows
- ✅ `start.sh` - Inicio para Linux/Mac
- ✅ `start.bat` - Inicio para Windows
- ✅ `build.sh` - Build script
- ✅ `run.py` - Script principal

## Corrección Aplicada

### Problema
La carpeta `.kiro/` no estaba en el `.gitignore`, lo que podría causar que configuración local del IDE se suba al repositorio.

### Solución
```gitignore
# IDE
.vscode/
.idea/
.kiro/        # ← Agregado
*.swp
*.swo
*~
.DS_Store
```

### Verificación
```bash
# Verificar que .kiro no está trackeado
git ls-files .kiro

# Si no devuelve nada, está correcto
# Si devuelve archivos, remover con:
git rm -r --cached .kiro
git commit -m "Remove .kiro from repository"
```

## Estado Actual

✅ `.kiro/` agregado al `.gitignore`
✅ `.kiro/` NO está trackeado en Git
✅ Configuración local protegida

## Buenas Prácticas

### Al Agregar Archivos
1. Verificar que no sean archivos locales/temporales
2. Revisar el `.gitignore` antes de commit
3. Usar `git status` para ver qué se va a subir

### Al Clonar el Proyecto
1. Copiar `.env.example` a `.env`
2. Configurar variables de entorno locales
3. Crear entorno virtual
4. Instalar dependencias

### Al Contribuir
1. No subir archivos de configuración local
2. No subir bases de datos
3. No subir archivos temporales
4. Seguir las convenciones del proyecto

## Comandos Útiles

### Ver archivos ignorados
```bash
git status --ignored
```

### Ver archivos trackeados
```bash
git ls-files
```

### Remover archivo del tracking (mantener local)
```bash
git rm --cached archivo.txt
```

### Remover carpeta del tracking (mantener local)
```bash
git rm -r --cached carpeta/
```

### Verificar si un archivo está ignorado
```bash
git check-ignore -v archivo.txt
```

## Mantenimiento

### Mensual
- Revisar archivos nuevos antes de commit
- Verificar que `.gitignore` esté actualizado

### Al Agregar Nuevas Herramientas
- Agregar sus carpetas de configuración al `.gitignore`
- Documentar en este archivo

### Al Cambiar de IDE
- Agregar la carpeta del nuevo IDE al `.gitignore`
- Remover configuración del IDE anterior si está trackeada

## Referencias

- [Git Documentation - gitignore](https://git-scm.com/docs/gitignore)
- [GitHub gitignore templates](https://github.com/github/gitignore)
- [Python gitignore template](https://github.com/github/gitignore/blob/main/Python.gitignore)
