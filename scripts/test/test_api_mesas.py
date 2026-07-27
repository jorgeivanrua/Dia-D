"""
Script para probar el endpoint de mesas del testigo
"""
import requests
import json

BASE_URL = "http://localhost:5000"

# Primero hacer login
login_data = {
    "rol": "testigo_electoral",
    "departamento_codigo": "44",
    "municipio_codigo": "01",
    "zona_codigo": "01",
    "puesto_codigo": "01",
    "password": "test123"
}

print("=" * 80)
print("TEST API MESAS TESTIGO")
print("=" * 80)
print()

try:
    # Login
    print("1. Haciendo login...")
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code != 200:
        print(f"❌ Login fallido: {response.status_code}")
        print(response.json())
        exit(1)
    
    data = response.json()
    token = data['data']['access_token']
    print(f"✅ Login exitoso. Token obtenido.")
    print()
    
    # Obtener mesas del puesto
    print("2. Obteniendo mesas del puesto...")
    response = requests.get(
        f"{BASE_URL}/api/testigo/mesas-puesto",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    
    print(f"Status Code: {response.status_code}")
    print()
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Mesas obtenidas exitosamente")
        print()
        print(f"Total mesas: {len(data['data'])}")
        print()
        print("Primeras 3 mesas:")
        for mesa in data['data'][:3]:
            print(f"  Mesa {mesa['mesa_codigo']}:")
            print(f"    ID: {mesa['id']}")
            print(f"    Puesto: {mesa['puesto_nombre']}")
            print(f"    Votantes registrados: {mesa.get('total_votantes_registrados', 'NO DISPONIBLE')}")
            print(f"    Mujeres: {mesa.get('mujeres', 'NO DISPONIBLE')}")
            print(f"    Hombres: {mesa.get('hombres', 'NO DISPONIBLE')}")
            print()
    else:
        print("❌ Error obteniendo mesas")
        print(response.json())
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

print("=" * 80)
