#!/usr/bin/env python3
"""
Script de pruebas para verificar funcionalidad de todos los roles
"""
import requests
import json
from datetime import datetime

BASE_URL = "https://dia-d.onrender.com"

# Credenciales de prueba
CREDENTIALS = {
    'super_admin': {'username': 'admin', 'password': 'admin123'},
    'admin_departamental': {'username': 'admin_caqueta', 'password': 'admin123'},
    'admin_municipal': {'username': 'admin_florencia', 'password': 'admin123'},
    'coordinador_departamental': {'username': 'coord_dpto_caqueta', 'password': 'coord123'},
    'coordinador_municipal': {'username': 'coord_mun_florencia', 'password': 'coord123'},
    'coordinador_puesto': {'username': 'coord_puesto_01', 'password': 'coord123'},
    'testigo_electoral': {'username': 'testigo_01_1', 'password': 'testigo123'},
    'auditor_electoral': {'username': 'auditor_caqueta', 'password': 'auditor123'}
}

class RoleTester:
    def __init__(self, role_name, credentials):
        self.role_name = role_name
        self.credentials = credentials
        self.token = None
        self.results = []
    
    def log(self, test_name, success, message=""):
        status = "✅" if success else "❌"
        self.results.append({
            'test': test_name,
            'success': success,
            'message': message
        })
        print(f"  {status} {test_name}: {message}")
    
    def login(self):
        """Probar login"""
        try:
            response = requests.post(
                f"{BASE_URL}/api/auth/login",
                json={
                    'nombre': self.credentials['username'],
                    'password': self.credentials['password']
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.token = data['data']['access_token']
                    self.log("Login", True, f"Token obtenido")
                    return True
                else:
                    self.log("Login", False, data.get('error', 'Error desconocido'))
                    return False
            else:
                self.log("Login", False, f"Status {response.status_code}")
                return False
        except Exception as e:
            self.log("Login", False, str(e))
            return False
    
    def get_profile(self):
        """Obtener perfil del usuario"""
        try:
            response = requests.get(
                f"{BASE_URL}/api/auth/profile",
                headers={'Authorization': f'Bearer {self.token}'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    user = data['data']['user']
                    self.log("Perfil", True, f"Rol: {user['rol']}")
                    return True
                else:
                    self.log("Perfil", False, data.get('error'))
                    return False
            else:
                self.log("Perfil", False, f"Status {response.status_code}")
                return False
        except Exception as e:
            self.log("Perfil", False, str(e))
            return False
    
    def test_super_admin_endpoints(self):
        """Probar endpoints de Super Admin"""
        endpoints = [
            ('/api/super-admin/stats', 'GET', 'Estadísticas'),
            ('/api/super-admin/users', 'GET', 'Lista de usuarios'),
            ('/api/super-admin/system-health', 'GET', 'Estado del sistema'),
        ]
        
        for endpoint, method, name in endpoints:
            try:
                response = requests.get(
                    f"{BASE_URL}{endpoint}",
                    headers={'Authorization': f'Bearer {self.token}'},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        self.log(name, True, "Datos obtenidos")
                    else:
                        self.log(name, False, data.get('error'))
                else:
                    self.log(name, False, f"Status {response.status_code}")
            except Exception as e:
                self.log(name, False, str(e))
    
    def test_testigo_endpoints(self):
        """Probar endpoints de Testigo"""
        endpoints = [
            ('/api/testigo/partidos', 'GET', 'Partidos'),
            ('/api/testigo/tipos-eleccion', 'GET', 'Tipos de elección'),
            ('/api/testigo/candidatos', 'GET', 'Candidatos'),
            ('/api/testigo/formularios', 'GET', 'Formularios'),
        ]
        
        for endpoint, method, name in endpoints:
            try:
                response = requests.get(
                    f"{BASE_URL}{endpoint}",
                    headers={'Authorization': f'Bearer {self.token}'},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        self.log(name, True, "Datos obtenidos")
                    else:
                        self.log(name, False, data.get('error'))
                else:
                    self.log(name, False, f"Status {response.status_code}")
            except Exception as e:
                self.log(name, False, str(e))
    
    def test_coordinador_endpoints(self):
        """Probar endpoints de Coordinador"""
        endpoints = [
            ('/api/coordinador/stats', 'GET', 'Estadísticas'),
            ('/api/coordinador/equipo', 'GET', 'Equipo'),
        ]
        
        for endpoint, method, name in endpoints:
            try:
                response = requests.get(
                    f"{BASE_URL}{endpoint}",
                    headers={'Authorization': f'Bearer {self.token}'},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        self.log(name, True, "Datos obtenidos")
                    else:
                        self.log(name, False, data.get('error'))
                else:
                    self.log(name, False, f"Status {response.status_code}")
            except Exception as e:
                self.log(name, False, str(e))
    
    def run_tests(self):
        """Ejecutar todas las pruebas para este rol"""
        print(f"\n{'='*60}")
        print(f"🧪 Probando rol: {self.role_name.upper()}")
        print(f"{'='*60}")
        
        # Login
        if not self.login():
            print(f"❌ No se pudo hacer login, saltando pruebas")
            return
        
        # Perfil
        if not self.get_profile():
            print(f"❌ No se pudo obtener perfil, saltando pruebas")
            return
        
        # Pruebas específicas por rol
        if self.role_name == 'super_admin':
            self.test_super_admin_endpoints()
        elif self.role_name == 'testigo_electoral':
            self.test_testigo_endpoints()
        elif 'coordinador' in self.role_name:
            self.test_coordinador_endpoints()
        
        # Resumen
        total = len(self.results)
        passed = sum(1 for r in self.results if r['success'])
        failed = total - passed
        
        print(f"\n📊 Resumen: {passed}/{total} pruebas exitosas ({failed} fallidas)")
        
        return self.results

def main():
    """Ejecutar pruebas para todos los roles"""
    print(f"\n{'='*60}")
    print(f"🚀 INICIANDO PRUEBAS DE TODOS LOS ROLES")
    print(f"{'='*60}")
    print(f"Base URL: {BASE_URL}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_results = {}
    
    for role_name, credentials in CREDENTIALS.items():
        tester = RoleTester(role_name, credentials)
        results = tester.run_tests()
        all_results[role_name] = results
    
    # Resumen global
    print(f"\n{'='*60}")
    print(f"📊 RESUMEN GLOBAL")
    print(f"{'='*60}")
    
    for role_name, results in all_results.items():
        if results:
            total = len(results)
            passed = sum(1 for r in results if r['success'])
            status = "✅" if passed == total else "⚠️" if passed > 0 else "❌"
            print(f"{status} {role_name}: {passed}/{total} pruebas exitosas")
        else:
            print(f"❌ {role_name}: No se pudo hacer login")
    
    print(f"\n{'='*60}")
    print(f"✅ PRUEBAS COMPLETADAS")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
