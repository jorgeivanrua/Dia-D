"""
Script de inicialización completa del sistema
Ejecuta todos los pasos necesarios para tener el sistema funcionando
"""
import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Imprimir encabezado"""
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80 + "\n")

def print_step(number, text):
    """Imprimir paso"""
    print(f"\n{'='*80}")
    print(f"PASO {number}: {text}")
    print(f"{'='*80}\n")

def run_script(script_path, description):
    """Ejecutar un script Python"""
    print(f">> Ejecutando: {description}")
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=False,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ {description} completado")
            return True
        else:
            print(f"❌ Error en {description}")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando {description}: {e}")
        return False

def check_file_exists(filepath, description):
    """Verificar que un archivo existe"""
    if os.path.exists(filepath):
        print(f"✅ {description} encontrado")
        return True
    else:
        print(f"❌ {description} NO encontrado: {filepath}")
        return False

def main():
    """Función principal de inicialización"""
    print_header("SISTEMA DE TESTIGOS ELECTORALES - INICIALIZACIÓN COMPLETA")
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('backend') or not os.path.exists('frontend'):
        print("❌ Error: Este script debe ejecutarse desde el directorio raíz del proyecto")
        print("   Asegúrate de estar en el directorio que contiene las carpetas 'backend' y 'frontend'")
        sys.exit(1)
    
    print("✅ Directorio correcto detectado")
    
    # Crear archivo .env si no existe
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ Archivo .env creado desde .env.example")
        else:
            print("⚠️  Archivo .env.example no encontrado")
    
    # PASO 1: Verificar archivos necesarios
    print_step(1, "VERIFICACIÓN DE ARCHIVOS")
    
    archivos_necesarios = [
        ('backend/app.py', 'Aplicación principal'),
        ('backend/models/user.py', 'Modelo de usuarios'),
        ('backend/models/location.py', 'Modelo de ubicaciones'),
        ('scripts/init_db.py', 'Script de inicialización de BD'),
        ('scripts/load_divipola.py', 'Script de carga de ubicaciones'),
        ('scripts/create_fixed_users.py', 'Script de creación de usuarios'),
        ('requirements.txt', 'Dependencias Python')
    ]
    
    all_files_ok = True
    for filepath, description in archivos_necesarios:
        if not check_file_exists(filepath, description):
            all_files_ok = False
    
    if not all_files_ok:
        print("\n❌ Faltan archivos necesarios. No se puede continuar.")
        sys.exit(1)
    
    # Verificar archivo DIVIPOLA
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
            break
    
    if not divipola_found:
        print("\n⚠️  ADVERTENCIA: No se encontró el archivo divipola.csv")
        print("   Ubicaciones esperadas:")
        for path in divipola_paths:
            print(f"   - {path}")
        print("\n   El sistema se inicializará pero sin datos de ubicaciones.")
        print("   Deberás cargar el archivo manualmente después.")
        response = input("\n¿Continuar de todos modos? (s/n): ")
        if response.lower() != 's':
            sys.exit(0)
    
    # PASO 2: Crear base de datos
    print_step(2, "INICIALIZACIÓN DE BASE DE DATOS")
    if not run_script('scripts/init_db.py', 'Crear estructura de base de datos'):
        print("\n❌ Error crítico en la inicialización de la BD")
        sys.exit(1)
    
    # PASO 3: Cargar ubicaciones (si existe el archivo)
    if divipola_found:
        print_step(3, "CARGA DE UBICACIONES (DIVIPOLA)")
        if not run_script('scripts/load_divipola.py', 'Cargar datos de ubicaciones'):
            print("\n⚠️  Error cargando ubicaciones, pero continuando...")
    else:
        print_step(3, "CARGA DE UBICACIONES (OMITIDO)")
        print("⚠️  Archivo DIVIPOLA no encontrado. Paso omitido.")
    
    # PASO 4: Aplicar migración de geolocalización
    print_step(4, "APLICACIÓN DE MIGRACIONES")
    migration_script = 'backend/migrations/apply_user_geolocation.py'
    if os.path.exists(migration_script):
        if not run_script(migration_script, 'Aplicar migración de geolocalización'):
            print("\n⚠️  Error en migración, pero continuando...")
    else:
        print("⚠️  Script de migración no encontrado, omitiendo...")
    
    # PASO 5: Crear usuarios del sistema
    print_step(5, "CREACIÓN DE USUARIOS DEL SISTEMA")
    if not run_script('scripts/init_system.py', 'Inicializar usuarios del sistema'):
        print("\n⚠️  Error creando usuarios, pero continuando...")
    
    # PASO 6: Inicializar configuración electoral (si existe)
    print_step(6, "CONFIGURACIÓN ELECTORAL")
    config_script = 'scripts/init_configuracion_electoral.py'
    if os.path.exists(config_script):
        if not run_script(config_script, 'Inicializar configuración electoral'):
            print("\n⚠️  Error en configuración electoral, pero continuando...")
    else:
        print("⚠️  Script de configuración electoral no encontrado, omitiendo...")
    
    # PASO 7: Crear tablas de formularios (si existe)
    print_step(7, "TABLAS DE FORMULARIOS")
    forms_script = 'scripts/create_formularios_e14_tables.py'
    if os.path.exists(forms_script):
        if not run_script(forms_script, 'Crear tablas de formularios E-14'):
            print("\n⚠️  Error creando tablas de formularios, pero continuando...")
    else:
        print("⚠️  Script de formularios no encontrado, omitiendo...")
    
    # RESUMEN FINAL
    print_header("INICIALIZACIÓN COMPLETADA")
    
    print("✅ El sistema ha sido inicializado correctamente\n")
    
    print("CREDENCIALES DE ACCESO:")
    print("-" * 80)
    print("\n🔑 SUPER ADMIN:")
    print("   Usuario: admin")
    print("   Password: admin123")
    print("\n🔑 COORDINADORES:")
    print("   Usuario: coord_dpto_caqueta / coord_mun_florencia / coord_puesto_XX")
    print("   Password: test123")
    print("\n🔑 TESTIGOS:")
    print("   Usuario: testigo_XX_1 / testigo_XX_2")
    print("   Password: test123")
    print("\n🔑 ADMINISTRADORES:")
    print("   Usuario: admin_caqueta / admin_florencia")
    print("   Password: admin123")
    print("\n🔑 AUDITOR:")
    print("   Usuario: auditor_caqueta")
    print("   Password: test123")
    
    print("\n" + "=" * 80)
    print("SIGUIENTE PASO: EJECUTAR LA APLICACIÓN")
    print("=" * 80)
    print("\nPara iniciar el servidor, ejecuta:")
    print("  python run.py")
    print("\nO en Windows:")
    print("  start.bat")
    print("\nLa aplicación estará disponible en: http://localhost:5000")
    print("\n" + "=" * 80)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Inicialización cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
