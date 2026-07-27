"""
Script de diagnóstico del sistema de inicialización
Verifica el estado de todos los componentes
"""
import os
import sys
from pathlib import Path

def print_header(text):
    """Imprimir encabezado"""
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80 + "\n")

def check_item(description, condition, details=""):
    """Verificar un item"""
    status = "✅" if condition else "❌"
    print(f"{status} {description}")
    if details:
        print(f"   {details}")
    return condition

def main():
    """Función principal de diagnóstico"""
    print_header("DIAGNÓSTICO DEL SISTEMA DE INICIALIZACIÓN")
    
    all_ok = True
    
    # 1. VERIFICAR ESTRUCTURA DE DIRECTORIOS
    print_header("1. ESTRUCTURA DE DIRECTORIOS")
    
    dirs_required = [
        ('backend', 'Directorio backend'),
        ('backend/models', 'Modelos de datos'),
        ('backend/routes', 'Rutas API'),
        ('backend/migrations', 'Migraciones'),
        ('frontend', 'Directorio frontend'),
        ('frontend/static', 'Archivos estáticos'),
        ('frontend/templates', 'Templates HTML'),
        ('scripts', 'Scripts de utilidad'),
        ('instance', 'Directorio de base de datos')
    ]
    
    for dir_path, description in dirs_required:
        exists = os.path.isdir(dir_path)
        check_item(description, exists, dir_path)
        if not exists:
            all_ok = False
    
    # 2. VERIFICAR ARCHIVOS PRINCIPALES
    print_header("2. ARCHIVOS PRINCIPALES")
    
    files_required = [
        ('run.py', 'Script de ejecución'),
        ('setup.py', 'Script de inicialización'),
        ('requirements.txt', 'Dependencias Python'),
        ('backend/app.py', 'Aplicación Flask'),
        ('backend/database.py', 'Configuración de BD'),
        ('backend/models/user.py', 'Modelo de usuarios'),
        ('backend/models/location.py', 'Modelo de ubicaciones')
    ]
    
    for file_path, description in files_required:
        exists = os.path.isfile(file_path)
        check_item(description, exists, file_path)
        if not exists:
            all_ok = False
    
    # 3. VERIFICAR SCRIPTS DE INICIALIZACIÓN
    print_header("3. SCRIPTS DE INICIALIZACIÓN")
    
    scripts = [
        ('scripts/init_db.py', 'Inicialización de BD', True),
        ('scripts/load_divipola.py', 'Carga de ubicaciones', True),
        ('scripts/create_fixed_users.py', 'Creación de usuarios', True),
        ('backend/migrations/apply_user_geolocation.py', 'Migración de geolocalización', True),
        ('scripts/init_configuracion_electoral.py', 'Configuración electoral', False),
        ('scripts/create_formularios_e14_tables.py', 'Tablas de formularios', False)
    ]
    
    for script_path, description, required in scripts:
        exists = os.path.isfile(script_path)
        status = "✅" if exists else ("❌" if required else "⚠️")
        req_text = "(requerido)" if required else "(opcional)"
        print(f"{status} {description} {req_text}")
        print(f"   {script_path}")
        if required and not exists:
            all_ok = False
    
    # 4. VERIFICAR ARCHIVO DIVIPOLA
    print_header("4. ARCHIVO DE DATOS")
    
    divipola_paths = [
        'todos los datos/divipola.csv',
        'divipola.csv',
        'data/divipola.csv'
    ]
    
    divipola_found = False
    for path in divipola_paths:
        if os.path.exists(path):
            check_item("Archivo DIVIPOLA encontrado", True, path)
            divipola_found = True
            
            # Verificar tamaño
            size = os.path.getsize(path)
            size_mb = size / (1024 * 1024)
            print(f"   Tamaño: {size_mb:.2f} MB")
            break
    
    if not divipola_found:
        check_item("Archivo DIVIPOLA", False, "No encontrado en ninguna ubicación")
        print("   Ubicaciones buscadas:")
        for path in divipola_paths:
            print(f"   - {path}")
    
    # 5. VERIFICAR ENTORNO VIRTUAL
    print_header("5. ENTORNO VIRTUAL")
    
    venv_exists = os.path.isdir('.venv')
    check_item("Entorno virtual (.venv)", venv_exists)
    
    if venv_exists:
        # Verificar activación
        in_venv = hasattr(sys, 'real_prefix') or (
            hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
        )
        check_item("Entorno virtual activado", in_venv)
        
        if not in_venv:
            print("\n   Para activar:")
            print("   Windows: .venv\\Scripts\\activate")
            print("   Linux/Mac: source .venv/bin/activate")
    
    # 6. VERIFICAR DEPENDENCIAS
    print_header("6. DEPENDENCIAS PYTHON")
    
    try:
        import flask
        check_item("Flask", True, f"v{flask.__version__}")
    except ImportError:
        check_item("Flask", False, "No instalado")
        all_ok = False
    
    try:
        import flask_sqlalchemy
        check_item("Flask-SQLAlchemy", True)
    except ImportError:
        check_item("Flask-SQLAlchemy", False, "No instalado")
        all_ok = False
    
    try:
        import flask_jwt_extended
        check_item("Flask-JWT-Extended", True)
    except ImportError:
        check_item("Flask-JWT-Extended", False, "No instalado")
        all_ok = False
    
    try:
        import bcrypt
        check_item("bcrypt", True)
    except ImportError:
        check_item("bcrypt", False, "No instalado")
        all_ok = False
    
    # 7. VERIFICAR BASE DE DATOS
    print_header("7. BASE DE DATOS")
    
    db_path = 'instance/testigos.db'
    db_exists = os.path.isfile(db_path)
    check_item("Base de datos", db_exists, db_path)
    
    if db_exists:
        size = os.path.getsize(db_path)
        size_kb = size / 1024
        print(f"   Tamaño: {size_kb:.2f} KB")
        
        # Intentar conectar y verificar tablas
        try:
            sys.path.insert(0, os.path.abspath('.'))
            from backend.app import create_app
            from backend.database import db
            from backend.models.user import User
            from backend.models.location import Location
            
            app = create_app('development')
            with app.app_context():
                # Contar usuarios
                try:
                    user_count = User.query.count()
                    check_item("Usuarios en BD", user_count > 0, f"{user_count} usuarios")
                except Exception as e:
                    check_item("Tabla de usuarios", False, str(e))
                
                # Contar ubicaciones
                try:
                    location_count = Location.query.count()
                    check_item("Ubicaciones en BD", location_count > 0, f"{location_count} ubicaciones")
                except Exception as e:
                    check_item("Tabla de ubicaciones", False, str(e))
        
        except Exception as e:
            check_item("Conexión a BD", False, str(e))
    else:
        print("   La base de datos no existe. Ejecuta: python setup.py")
    
    # 8. VERIFICAR SCRIPTS DE INICIO
    print_header("8. SCRIPTS DE INICIO")
    
    startup_scripts = [
        ('setup.bat', 'Setup para Windows'),
        ('setup.sh', 'Setup para Linux/Mac'),
        ('start.bat', 'Inicio para Windows'),
        ('start.sh', 'Inicio para Linux/Mac'),
        ('render_setup.py', 'Setup para Render'),
        ('render.yaml', 'Configuración de Render')
    ]
    
    for script, description in startup_scripts:
        exists = os.path.isfile(script)
        check_item(description, exists, script)
    
    # 9. VERIFICAR CONFIGURACIÓN
    print_header("9. CONFIGURACIÓN")
    
    env_exists = os.path.isfile('.env')
    check_item("Archivo .env", env_exists)
    
    if not env_exists:
        print("   El sistema usará valores por defecto")
        print("   Para personalizar, crea un archivo .env")
    
    # RESUMEN FINAL
    print_header("RESUMEN")
    
    if all_ok and db_exists:
        print("✅ SISTEMA COMPLETAMENTE CONFIGURADO")
        print("\nPara iniciar el servidor:")
        print("  Windows: start.bat")
        print("  Linux/Mac: ./start.sh")
        print("  O directamente: python run.py")
        print("\nAcceso:")
        print("  URL: http://localhost:5000")
        print("  Usuario: admin")
        print("  Password: admin123")
    
    elif all_ok and not db_exists:
        print("⚠️  SISTEMA LISTO PARA INICIALIZAR")
        print("\nEjecuta la inicialización:")
        print("  Windows: setup.bat")
        print("  Linux/Mac: ./setup.sh")
        print("  O directamente: python setup.py")
    
    else:
        print("❌ SISTEMA INCOMPLETO")
        print("\nProblemas detectados:")
        print("  - Revisa los items marcados con ❌")
        print("  - Asegúrate de estar en el directorio correcto")
        print("  - Verifica que todos los archivos estén presentes")
        print("\nPara más ayuda, consulta:")
        print("  - INICIO_RAPIDO.md")
        print("  - SISTEMA_INICIALIZACION.md")
        print("  - GUIA_DESPLIEGUE.md")
    
    print("\n" + "=" * 80 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Diagnóstico cancelado")
    except Exception as e:
        print(f"\n\n❌ Error en diagnóstico: {e}")
        import traceback
        traceback.print_exc()
