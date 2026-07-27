"""
Script de prueba para endpoints del coordinador municipal
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def login(username, password, rol="coordinador_municipal"):
    """Login y obtener token"""
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"nombre": username, "password": password, "rol": rol}
    )
    if response.status_code == 200:
        data = response.json()
        return data.get('access_token')
    else:
        print(f"❌ Error en login: {response.status_code}")
        print(response.text)
        return None

def test_endpoint(token, endpoint, method='GET', params=None):
    """Probar un endpoint"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"\n{'='*60}")
    print(f"Probando: {method} {endpoint}")
    print(f"{'='*60}")
    
    if method == 'GET':
        response = requests.get(
            f"{BASE_URL}{endpoint}",
            headers=headers,
            params=params
        )
    else:
        response = requests.post(
            f"{BASE_URL}{endpoint}",
            headers=headers,
            json=params
        )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"✅ Éxito")
            
            # Mostrar resumen de datos
            if 'data' in data:
                if isinstance(data['data'], list):
                    print(f"   Total items: {len(data['data'])}")
                    if len(data['data']) > 0:
                        print(f"   Primer item: {json.dumps(data['data'][0], indent=2)[:200]}...")
                elif isinstance(data['data'], dict):
                    print(f"   Keys: {list(data['data'].keys())}")
                    for key, value in data['data'].items():
                        if isinstance(value, list):
                            print(f"   {key}: {len(value)} items")
                        elif isinstance(value, dict):
                            print(f"   {key}: {list(value.keys())}")
                        else:
                            print(f"   {key}: {value}")
        else:
            print(f"❌ Error: {data.get('error')}")
    else:
        print(f"❌ Error HTTP: {response.status_code}")
        print(response.text[:500])

def main():
    print("="*60)
    print("TEST DE ENDPOINTS - COORDINADOR MUNICIPAL")
    print("="*60)
    
    # Login
    print("\n1. Login...")
    token = login("coord_mun", "test123", "coordinador_municipal")
    
    if not token:
        print("❌ No se pudo obtener token. Intentando con FLORENCIA...")
        token = login("FLORENCIA", "test123", "coordinador_municipal")
    
    if not token:
        print("❌ No se pudo hacer login. Verifica que el servidor esté corriendo.")
        return
    
    print(f"✅ Token obtenido: {token[:20]}...")
    
    # Probar endpoints
    endpoints = [
        ("/api/coordinador-municipal/puestos", "GET", None),
        ("/api/coordinador-municipal/consolidado", "GET", None),
        ("/api/coordinador-municipal/discrepancias", "GET", None),
        ("/api/coordinador-municipal/estadisticas", "GET", None),
        ("/api/coordinador-municipal/incidentes", "GET", None),
        ("/api/coordinador-municipal/incidentes", "GET", {"estado": "reportado"}),
        ("/api/coordinador-municipal/delitos", "GET", None),
        ("/api/coordinador-municipal/delitos", "GET", {"estado": "reportado"}),
        ("/api/coordinador-municipal/coordinadores", "GET", None),
        ("/api/coordinador-municipal/coordinadores", "GET", {"estado": "activo"}),
        ("/api/coordinador-municipal/geolocalizacion", "GET", None),
    ]
    
    resultados = {
        'exitosos': 0,
        'fallidos': 0
    }
    
    for endpoint, method, params in endpoints:
        try:
            test_endpoint(token, endpoint, method, params)
            resultados['exitosos'] += 1
        except Exception as e:
            print(f"❌ Excepción: {str(e)}")
            resultados['fallidos'] += 1
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    print(f"✅ Exitosos: {resultados['exitosos']}")
    print(f"❌ Fallidos: {resultados['fallidos']}")
    print(f"Total: {resultados['exitosos'] + resultados['fallidos']}")
    
    if resultados['fallidos'] == 0:
        print("\n🎉 ¡Todos los endpoints funcionan correctamente!")
    else:
        print(f"\n⚠️ {resultados['fallidos']} endpoint(s) con problemas")

if __name__ == "__main__":
    main()
