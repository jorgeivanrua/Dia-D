#!/usr/bin/env python
"""
Script para verificar el endpoint de formularios del dashboard de monitoreo
"""
import requests
import json

BASE_URL = 'http://localhost:5000'

def test_login():
    """Login como usuario de monitoreo"""
    print("1. Intentando login como monitoreo...")
    response = requests.post(f'{BASE_URL}/api/auth/login', json={
        'nombre': 'monitoreo',
        'password': 'test123'
    })
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            token = data.get('access_token')
            print(f"   ✅ Login exitoso")
            return token
        else:
            print(f"   ❌ Login falló: {data.get('error')}")
            return None
    else:
        print(f"   ❌ Error HTTP {response.status_code}")
        return None

def test_formularios_endpoint(token):
    """Probar endpoint de formularios"""
    print("\n2. Probando endpoint /api/formularios/todos...")
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f'{BASE_URL}/api/formularios/todos', headers=headers)
    
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            formularios = data.get('data', [])
            print(f"   ✅ Endpoint funciona correctamente")
            print(f"   📊 Total formularios: {len(formularios)}")
            return True
        else:
            print(f"   ❌ Respuesta no exitosa: {data.get('error')}")
            return False
    else:
        print(f"   ❌ Error HTTP {response.status_code}")
        try:
            print(f"   Respuesta: {response.json()}")
        except:
            print(f"   Respuesta: {response.text}")
        return False

def test_estadisticas_endpoint(token):
    """Probar endpoint de estadísticas"""
    print("\n3. Probando endpoint /api/monitoreo/estadisticas...")
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f'{BASE_URL}/api/monitoreo/estadisticas', headers=headers)
    
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✅ Endpoint funciona correctamente")
            print(f"   📊 Estadísticas: {json.dumps(data.get('data'), indent=2)}")
            return True
        else:
            print(f"   ❌ Respuesta no exitosa: {data.get('error')}")
            return False
    else:
        print(f"   ❌ Error HTTP {response.status_code}")
        try:
            print(f"   Respuesta: {response.json()}")
        except:
            print(f"   Respuesta: {response.text}")
        return False

def test_puestos_endpoint(token):
    """Probar endpoint de puestos geolocalizados"""
    print("\n4. Probando endpoint /api/locations/puestos-geolocalizados...")
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f'{BASE_URL}/api/locations/puestos-geolocalizados', headers=headers)
    
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            puestos = data.get('data', [])
            print(f"   ✅ Endpoint funciona correctamente")
            print(f"   📊 Total puestos: {len(puestos)}")
            return True
        else:
            print(f"   ❌ Respuesta no exitosa: {data.get('error')}")
            return False
    else:
        print(f"   ❌ Error HTTP {response.status_code}")
        try:
            print(f"   Respuesta: {response.json()}")
        except:
            print(f"   Respuesta: {response.text}")
        return False

def main():
    print("=" * 60)
    print("VERIFICACIÓN DE ENDPOINTS DEL DASHBOARD DE MONITOREO")
    print("=" * 60)
    
    # Login
    token = test_login()
    if not token:
        print("\n❌ No se pudo obtener token de autenticación")
        return
    
    # Probar endpoints
    results = []
    results.append(("Formularios", test_formularios_endpoint(token)))
    results.append(("Estadísticas", test_estadisticas_endpoint(token)))
    results.append(("Puestos", test_puestos_endpoint(token)))
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ OK" if result else "❌ FALLO"
        print(f"{name:20} {status}")
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    print(f"\nTotal: {passed}/{total} pruebas exitosas")

if __name__ == '__main__':
    main()
