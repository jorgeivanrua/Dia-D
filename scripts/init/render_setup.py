"""
Script de inicialización para Render.com
Se ejecuta automáticamente en el despliegue
"""
import os
import sys
import subprocess

def print_header(text):
    """Imprimir encabezado"""
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80 + "\n")

def run_command(command, description):
    """Ejecutar un comando"""
    print(f">> {description}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ {description} completado")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ Error en {description}")
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error ejecutando {description}: {e}")
        return False

def main():
    """Función principal para Render"""
    print_header("RENDER.COM - INICIALIZACIÓN DEL SISTEMA")
    
    # Verificar que estamos en Render
    is_render = os.getenv('RENDER') == 'true'
    if is_render:
        print("✅ Entorno Render detectado")
    else:
        print("⚠️  No se detectó entorno Render, continuando de todos modos...")
    
    # Obtener DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        print(f"✅ DATABASE_URL configurada")
        # Render usa postgres:// pero SQLAlchemy necesita postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
            os.environ['DATABASE_URL'] = database_url
            print("   Ajustado formato de URL para SQLAlchemy")
    else:
        print("⚠️  DATABASE_URL no configurada, usando SQLite local")
    
    # Configurar entorno de producción
    os.environ['FLASK_ENV'] = 'production'
    print("✅ Entorno configurado como 'production'")
    
    # PASO 1: Inicializar base de datos
    print_header("PASO 1: INICIALIZACIÓN DE BASE DE DATOS")
    if not run_command(
        f"{sys.executable} scripts/init_db.py",
        "Crear estructura de base de datos"
    ):
        print("❌ Error crítico en inicialización de BD")
        sys.exit(1)
    
    # PASO 2: Aplicar migraciones
    print_header("PASO 2: APLICACIÓN DE MIGRACIONES")
    migration_script = 'backend/migrations/apply_user_geolocation.py'
    if os.path.exists(migration_script):
        run_command(
            f"{sys.executable} {migration_script}",
            "Aplicar migración de geolocalización"
        )
    
    # PASO 3: Cargar ubicaciones (si existe el archivo)
    print_header("PASO 3: CARGA DE UBICACIONES")
    divipola_paths = [
        'todos los datos/divipola.csv',
        'divipola.csv',
        'data/divipola.csv'
    ]
    
    divipola_found = False
    for path in divipola_paths:
        if os.path.exists(path):
            print(f"✅ Archivo DIVIPOLA encontrado: {path}")
            divipola_found = True
            run_command(
                f"{sys.executable} scripts/load_divipola.py",
                "Cargar datos de ubicaciones"
            )
            break
    
    if not divipola_found:
        print("⚠️  Archivo DIVIPOLA no encontrado")
        print("   Las ubicaciones deberán cargarse manualmente después del despliegue")
    
    # PASO 4: Verificar usuarios básicos del sistema
    print_header("PASO 4: VERIFICACIÓN DE USUARIOS BÁSICOS")
    
    # Los usuarios básicos se crean automáticamente al iniciar la app
    # Solo verificamos que existan
    try:
        from backend.app import create_app
        from backend.database import db
        from backend.models.user import User
        from backend.utils.init_usuarios_basicos import verificar_usuarios_basicos
        
        app = create_app('production')
        with app.app_context():
            user_count = User.query.count()
            usuarios_basicos = User.query.filter_by(es_usuario_basico=True).count()
            
            print(f"📊 Total de usuarios: {user_count}")
            print(f"📊 Usuarios básicos del sistema: {usuarios_basicos}")
            
            if verificar_usuarios_basicos():
                print("✅ Todos los usuarios básicos del sistema están presentes")
            else:
                print("⚠️  Faltan algunos usuarios básicos")
                print("   Se crearán automáticamente al iniciar la aplicación")
    except Exception as e:
        print(f"⚠️  Error verificando usuarios: {e}")
        print("   Los usuarios básicos se crearán al iniciar la aplicación")
    
    # PASO 5: Configuración electoral
    print_header("PASO 5: CONFIGURACIÓN ELECTORAL")
    config_script = 'scripts/init_configuracion_electoral.py'
    if os.path.exists(config_script):
        run_command(
            f"{sys.executable} {config_script}",
            "Inicializar configuración electoral"
        )
    
    # PASO 6: Importación automática de datos desde JSON
    print_header("PASO 6: IMPORTACIÓN AUTOMÁTICA DE DATOS")
    
    # Buscar archivo de datos para importar
    data_paths = [
        'data/render_initial_data.json',
        'render_initial_data.json',
        'initial_data.json'
    ]
    
    data_file_found = False
    for data_path in data_paths:
        if os.path.exists(data_path):
            print(f"✅ Archivo de datos encontrado: {data_path}")
            data_file_found = True
            
            # Importar datos usando el script de importación
            print(">> Importando ubicaciones, usuarios y datos...")
            if run_command(
                f"{sys.executable} scripts/utils/import_data_from_json.py {data_path}",
                "Importar datos desde JSON"
            ):
                print("✅ Datos importados exitosamente")
            else:
                print("⚠️  Error importando datos, continuando...")
            break
    
    if not data_file_found:
        print("⚠️  No se encontró archivo de datos inicial")
        print("   Archivos buscados:")
        for path in data_paths:
            print(f"   - {path}")
        print("\n💡 Para cargar datos automáticamente en Render:")
        print("   1. Exporta tu BD local: python scripts/utils/export_data_to_json.py")
        print("   2. Renombra el archivo a: render_initial_data.json")
        print("   3. Colócalo en la raíz del proyecto")
        print("   4. Haz commit y push")
        print("   5. Render lo importará automáticamente en el próximo despliegue")
    
    # PASO 7: Inicialización automática de datos (scripts adicionales)
    print_header("PASO 7: SCRIPTS DE INICIALIZACIÓN ADICIONALES")
    init_script = 'scripts/inicializar_datos_automatico.py'
    if os.path.exists(init_script):
        run_command(
            f"{sys.executable} {init_script}",
            "Cargar datos básicos automáticamente"
        )
    else:
        print("⚠️  Script de inicialización automática no encontrado")
    
    # RESUMEN
    print_header("INICIALIZACIÓN COMPLETADA")
    print("✅ El sistema está listo para funcionar en Render")
    print("\nCREDENCIALES DE ACCESO:")
    print("-" * 80)
    print("Usuario: admin")
    print("Password: admin123")
    print("-" * 80)
    print("\n⚠️  IMPORTANTE: Cambia las contraseñas después del primer acceso")
    print("=" * 80)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error en inicialización: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
