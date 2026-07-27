"""
Script para verificar que el sistema está listo para auditoría
Verifica: servidor, base de datos, datos de prueba, dependencias
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from colorama import init, Fore, Style

init(autoreset=True)

BASE_URL = 'http://localhost:5000'


def check_server():
    """Verificar que el servidor esté corriendo"""
    print(f"\n{Fore.CYAN}1. Verificando servidor...{Style.RESET_ALL}")
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"{Fore.GREEN}   ✅ Servidor accesible en {BASE_URL}{Style.RESET_ALL}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}   ❌ Servidor no accesible{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   ℹ️  Inicia el servidor con: python run.py{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}   ❌ Error: {str(e)}{Style.RESET_ALL}")
        return False


def check_database():
    """Verificar conexión a base de datos"""
    print(f"\n{Fore.CYAN}2. Verificando base de datos...{Style.RESET_ALL}")
    try:
        from backend.app import create_app
        from backend.database import db
        
        app = create_app()
        with app.app_context():
            # Intentar una consulta simple
            db.session.execute(db.text('SELECT 1'))
            print(f"{Fore.GREEN}   ✅ Conexión a base de datos exitosa{Style.RESET_ALL}")
            return True
    except Exception as e:
        print(f"{Fore.RED}   ❌ Error de conexión: {str(e)}{Style.RESET_ALL}")
        return False


def check_test_data():
    """Verificar que existan datos de prueba"""
    print(f"\n{Fore.CYAN}3. Verificando datos de prueba...{Style.RESET_ALL}")
    try:
        from backend.app import create_app
        from backend.models.user import User
        from backend.models.location import Location
        from backend.models.partido_politico import PartidoPolitico as Partido
        from backend.models.candidato import Candidato
        
        app = create_app()
        with app.app_context():
            # Verificar usuarios de prueba
            admin = User.query.filter_by(nombre='admin_test').first()
            testigo = User.query.filter_by(nombre='testigo_test_1').first()
            
            if not admin or not testigo:
                print(f"{Fore.RED}   ❌ Usuarios de prueba no encontrados{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}   ℹ️  Ejecuta: python backend/scripts/load_complete_test_data.py{Style.RESET_ALL}")
                return False
            
            # Contar datos
            users_count = User.query.count()
            locations_count = Location.query.count()
            partidos_count = Partido.query.count()
            candidatos_count = Candidato.query.count()
            
            print(f"{Fore.GREEN}   ✅ Datos de prueba encontrados:{Style.RESET_ALL}")
            print(f"      • Usuarios: {users_count}")
            print(f"      • Ubicaciones: {locations_count}")
            print(f"      • Partidos: {partidos_count}")
            print(f"      • Candidatos: {candidatos_count}")
            
            if users_count < 10 or locations_count < 10:
                print(f"{Fore.YELLOW}   ⚠️  Pocos datos de prueba, considera recargar{Style.RESET_ALL}")
                return False
            
            return True
    except Exception as e:
        print(f"{Fore.RED}   ❌ Error: {str(e)}{Style.RESET_ALL}")
        return False


def check_dependencies():
    """Verificar dependencias necesarias"""
    print(f"\n{Fore.CYAN}4. Verificando dependencias...{Style.RESET_ALL}")
    
    dependencies = [
        ('requests', 'requests'),
        ('colorama', 'colorama'),
        ('flask', 'Flask'),
        ('sqlalchemy', 'SQLAlchemy'),
    ]
    
    all_ok = True
    for module_name, package_name in dependencies:
        try:
            __import__(module_name)
            print(f"{Fore.GREEN}   ✅ {package_name}{Style.RESET_ALL}")
        except ImportError:
            print(f"{Fore.RED}   ❌ {package_name} no instalado{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}      Instala con: pip install {package_name}{Style.RESET_ALL}")
            all_ok = False
    
    return all_ok


def check_api_endpoints():
    """Verificar que los endpoints principales estén disponibles"""
    print(f"\n{Fore.CYAN}5. Verificando endpoints API...{Style.RESET_ALL}")
    
    # Primero hacer login para obtener token
    try:
        response = requests.post(
            f'{BASE_URL}/api/auth/login',
            json={'nombre': 'admin_test', 'password': 'test123'},
            timeout=5
        )
        
        if response.status_code != 200:
            print(f"{Fore.RED}   ❌ No se pudo hacer login con usuario de prueba{Style.RESET_ALL}")
            return False
        
        token = response.json().get('access_token')
        headers = {'Authorization': f'Bearer {token}'}
        
        # Verificar algunos endpoints clave
        endpoints = [
            '/api/super-admin/usuarios',
            '/api/configuracion/tipos-eleccion',
            '/api/configuracion/partidos',
        ]
        
        all_ok = True
        for endpoint in endpoints:
            try:
                response = requests.get(f'{BASE_URL}{endpoint}', headers=headers, timeout=5)
                if response.status_code == 200:
                    print(f"{Fore.GREEN}   ✅ {endpoint}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}   ⚠️  {endpoint} - Status: {response.status_code}{Style.RESET_ALL}")
                    all_ok = False
            except Exception as e:
                print(f"{Fore.RED}   ❌ {endpoint} - Error: {str(e)}{Style.RESET_ALL}")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"{Fore.RED}   ❌ Error al verificar endpoints: {str(e)}{Style.RESET_ALL}")
        return False


def main():
    """Ejecutar todas las verificaciones"""
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"  VERIFICACIÓN DE SISTEMA PARA AUDITORÍA")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    checks = [
        ('Servidor', check_server),
        ('Base de datos', check_database),
        ('Datos de prueba', check_test_data),
        ('Dependencias', check_dependencies),
        ('Endpoints API', check_api_endpoints),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"{Fore.RED}   ❌ Error inesperado: {str(e)}{Style.RESET_ALL}")
            results[name] = False
    
    # Resumen
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"  RESUMEN DE VERIFICACIÓN")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    all_passed = True
    for name, passed in results.items():
        if passed:
            print(f"{Fore.GREEN}✅ {name}: OK{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ {name}: FALLO{Style.RESET_ALL}")
            all_passed = False
    
    print()
    
    if all_passed:
        print(f"{Fore.GREEN}{'='*60}")
        print(f"  ✅ SISTEMA LISTO PARA AUDITORÍA")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}Ejecuta la auditoría con:{Style.RESET_ALL}")
        print(f"  python backend/tests/test_audit_system.py\n")
        return 0
    else:
        print(f"{Fore.RED}{'='*60}")
        print(f"  ❌ SISTEMA NO ESTÁ LISTO")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}Corrige los problemas indicados arriba antes de continuar.{Style.RESET_ALL}\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
