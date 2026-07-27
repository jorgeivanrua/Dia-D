"""
Script para preparar datos para despliegue automático en Render
Ejecuta todos los pasos necesarios y genera el archivo render_initial_data.json
"""
import os
import sys
import subprocess
import shutil
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def print_header(text):
    """Imprimir encabezado"""
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80 + "\n")

def run_script(script_path, description):
    """Ejecutar un script Python"""
    print(f">> {description}")
    try:
        result = subprocess.run(
            [sys.executable, script_path],
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
    """Preparar datos para Render"""
    print_header("PREPARAR DATOS PARA RENDER")
    
    print("Este script ejecutará los siguientes pasos:")
    print("1. Marcar usuarios definitivos como básicos")
    print("2. Verificar usuarios básicos")
    print("3. Limpiar usuarios de prueba (opcional)")
    print("4. Exportar BD a JSON")
    print("5. Copiar archivo a data/render_initial_data.json")
    print()
    
    response = input("¿Deseas continuar? (s/n): ")
    if response.lower() != 's':
        print("❌ Operación cancelada")
        sys.exit(0)
    
    # PASO 1: Marcar usuarios definitivos
    print_header("PASO 1: MARCAR USUARIOS DEFINITIVOS COMO BÁSICOS")
    if not run_script(
        'scripts/utils/marcar_usuarios_definitivos_basicos.py',
        'Marcar usuarios definitivos'
    ):
        print("⚠️  Error marcando usuarios, continuando de todos modos...")
    
    # PASO 2: Verificar usuarios básicos
    print_header("PASO 2: VERIFICAR USUARIOS BÁSICOS")
    run_script(
        'scripts/utils/verificar_usuarios_basicos.py',
        'Verificar usuarios básicos'
    )
    
    # PASO 3: Limpiar usuarios de prueba (opcional)
    print_header("PASO 3: LIMPIAR USUARIOS DE PRUEBA")
    response = input("¿Deseas limpiar usuarios de prueba? (s/n): ")
    if response.lower() == 's':
        if not run_script(
            'scripts/utils/limpiar_usuarios_prueba.py',
            'Limpiar usuarios de prueba'
        ):
            print("⚠️  Error limpiando usuarios, continuando de todos modos...")
    else:
        print("⏭️  Omitiendo limpieza de usuarios de prueba")
    
    # PASO 4: Exportar BD
    print_header("PASO 4: EXPORTAR BASE DE DATOS")
    if not run_script(
        'scripts/utils/export_data_to_json.py',
        'Exportar BD a JSON'
    ):
        print("❌ Error exportando BD")
        sys.exit(1)
    
    # PASO 5: Buscar archivo exportado más reciente
    print_header("PASO 5: PREPARAR ARCHIVO PARA RENDER")
    
    # Buscar archivos data_export_*.json
    export_files = [f for f in os.listdir('.') if f.startswith('data_export_') and f.endswith('.json')]
    
    if not export_files:
        print("❌ No se encontró archivo exportado")
        sys.exit(1)
    
    # Ordenar por fecha (más reciente primero)
    export_files.sort(reverse=True)
    latest_export = export_files[0]
    
    print(f"📂 Archivo exportado encontrado: {latest_export}")
    
    # Crear directorio data si no existe
    os.makedirs('data', exist_ok=True)
    
    # Copiar archivo
    target_file = 'data/render_initial_data.json'
    shutil.copy(latest_export, target_file)
    
    print(f"✅ Archivo copiado a: {target_file}")
    
    # Obtener tamaño del archivo
    file_size = os.path.getsize(target_file)
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"📊 Tamaño del archivo: {file_size_mb:.2f} MB")
    
    if file_size_mb > 50:
        print("⚠️  ADVERTENCIA: El archivo es grande (>50MB)")
        print("   Considera usar Git LFS o importar manualmente desde el dashboard")
    
    # RESUMEN
    print_header("PREPARACIÓN COMPLETADA")
    print("✅ Datos preparados para Render")
    print()
    print("📋 Próximos pasos:")
    print("1. Revisar el archivo: data/render_initial_data.json")
    print("2. Hacer commit:")
    print("   git add data/render_initial_data.json")
    print("   git commit -m 'feat: Agregar datos iniciales para Render'")
    print("3. Push a GitHub:")
    print("   git push")
    print("4. Render cargará automáticamente los datos en el próximo despliegue")
    print()
    print("⚠️  IMPORTANTE:")
    print("   - Los usuarios importados tendrán contraseña temporal: test123")
    print("   - Los usuarios básicos existentes NO se sobrescribirán")
    print("=" * 80)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
