"""
Script para probar el endpoint /locations/mesas
"""
import requests
import json

BASE_URL = "http://localhost:5000"

print("=" * 80)
print("TEST ENDPOINT /locations/mesas")
print("=" * 80)
print()

try:
    # Probar endpoint sin autenticación (público)
    print("Obteniendo mesas del puesto 01 de Florencia...")
    response = requests.get(
        f"{BASE_URL}/api/locations/mesas",
        params={
            "departamento_codigo": "44",
            "municipio_codigo": "01",
            "zona_codigo": "01",
            "puesto_codigo": "01"
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
        print("Datos de las mesas:")
        for mesa in data['data']:
            print(f"  Mesa {mesa['mesa_codigo']}:")
            print(f"    ID: {mesa['id']}")
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
