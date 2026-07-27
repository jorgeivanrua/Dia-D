"""
Script para limpiar el sistema y resetear a estado inicial
USAR CON CUIDADO: Elimina la base de datos y todos los datos
"""
import os
import sys
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def print_header(text):
    """Imprimir encabezado"""
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80)


def clean_database():
    """Eliminar base de datos"""
    print("\n[1/5] Limpiando base de datos...")
    
    db_path = 'instance/electoral.db'
    
    if os.path.exists(db_path):
        # Hacer backup antes de eliminar
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f'instance/electoral_backup_{timestamp}.db'
        
        try:
            shutil.copy(db_path, backup_path)
            print(f"   [OK] Backup creado: {backup_path}")
        except Exception as e:
            print(f"   [!] No se pudo crear backup: {e}")
        
        try:
            os.remove(db_path)
            print(f"   [OK] Base de datos eliminada: {db_path}")
            return True
        except Exception as e:
            print(f"   [X] Error eliminando BD: {e}")
            return False
    else:
        print("   [i] Base de datos no existe")
        return True


def clean_pycache():
    """Eliminar archivos __pycache__ y .pyc"""
    print("\n[2/5] Limpiando archivos Python temporales...")
    
    count = 0
    for root, dirs, files in os.walk('.'):
        # Eliminar directorios __pycache__
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(pycache_path)
                count += 1
            except Exception as e:
                print(f"   [!] Error eliminando {pycache_path}: {e}")
        
        # Eliminar archivos .pyc
        for file in files:
            if file.endswith('.pyc'):
                pyc_path = os.path.join(root, file)
                try:
                    os.remove(pyc_path)
                    count += 1
                except Exception as e:
                    print(f"   [!] Error eliminando {pyc_path}: {e}")
    
    print(f"   [OK] {count} archivos/directorios eliminados")
    return True


def clean_logs():
    """Eliminar archivos de logs"""
    print("\n[3/5] Limpiando logs...")
    
    if os.path.exists('logs'):
        try:
            shutil.rmtree('logs')
            print("   [OK] Directorio logs eliminado")
            return True
        except Exception as e:
            print(f"   [X] Error eliminando logs: {e}")
            return False
    else:
        print("   [i] Directorio logs no existe")
        return True


def clean_test_artifacts():
    """Eliminar artefactos de tests"""
    print("\n[4/5] Limpiando artefactos de tests...")
    
    artifacts = ['.pytest_cache', 'htmlcov', '.coverage', 'test_output.txt', 'check_output.txt']
    count = 0
    
    for artifact in artifacts:
        if os.path.exists(artifact):
            try:
                if os.path.isdir(artifact):
                    shutil.rmtree(artifact)
                else:
                    os.remove(artifact)
                print(f"   [OK] Eliminado: {artifact}")
                count += 1
            except Exception as e:
                print(f"   [!] Error eliminando {artifact}: {e}")
    
    if count == 0:
        print("   [i] No hay artefactos de tests")
    
    return True


def clean_uploads():
    """Limpiar archivos subidos (opcional)"""
    print("\n[5/5] Limpiando archivos subidos...")
    
    if os.path.exists('uploads'):
        response = input("   [?] Eliminar archivos subidos? (s/n): ")
        if response.lower() == 's':
            try:
                shutil.rmtree('uploads')
                os.makedirs('uploads')
                print("   [OK] Archivos subidos eliminados")
                return True
            except Exception as e:
                print(f"   [X] Error: {e}")
                return False
        else:
            print("   [i] Archivos subidos conservados")
            return True
    else:
        print("   [i] Directorio uploads no existe")
        return True


def main():
    """Función principal"""
    print_header("LIMPIEZA DEL SISTEMA ELECTORAL")
    
    print("\n[!] ADVERTENCIA: Esta operación eliminará:")
    print("    - Base de datos (se creará backup)")
    print("    - Archivos Python temporales")
    print("    - Logs")
    print("    - Artefactos de tests")
    print("    - Archivos subidos (opcional)")
    print("\n[!] Esta acción NO se puede deshacer")
    
    response = input("\n[?] Continuar con la limpieza? (s/n): ")
    
    if response.lower() != 's':
        print("\n[i] Operación cancelada")
        return 0
    
    # Ejecutar limpieza
    results = []
    results.append(clean_database())
    results.append(clean_pycache())
    results.append(clean_logs())
    results.append(clean_test_artifacts())
    results.append(clean_uploads())
    
    # Resumen
    print("\n" + "=" * 80)
    print("RESUMEN DE LIMPIEZA")
    print("=" * 80)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n[OK] Operaciones exitosas: {passed}/{total}")
    
    if passed == total:
        print("\n[*] LIMPIEZA COMPLETADA")
        print("\nPara reinicializar el sistema, ejecuta:")
        print("  python scripts/init_system.py")
        return 0
    else:
        print(f"\n[!] {total - passed} operación(es) fallaron")
        return 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[!] Operación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[X] Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
