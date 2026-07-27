"""
Probar endpoint de puestos
"""
import requests

# Login
print("1. Login...")
response = requests.post(
    "http://localhost:5000/api/auth/login",
    json={
        "rol": "monitoreo",
        "nombre": "monitoreo",
        "password": "monitoreo123"
    }
)

if not response.json().get('success'):
    print(f"Error en login: {response.json()}")
    exit(1)

token = response.json()['data']['access_token']
print(f"✓ Token obtenido")

# Probar endpoint de puestos
print("\n2. Probando endpoint /api/locations/puestos-todos...")
response = requests.get(
    "http://localhost:5000/api/locations/puestos-todos",
    headers={"Authorization": f"Bearer {token}"}
)

print(f"Status: {response.status_code}")
data = response.json()
print(f"Success: {data.get('success')}")

if data.get('success'):
    puestos = data.get('data', [])
    total = data.get('total', 0)
    
    print(f"\n✓ Total puestos: {total}")
    print(f"✓ Puestos en respuesta: {len(puestos)}")
    
    if puestos:
        print(f"\nPrimeros 5 puestos:")
        for p in puestos[:5]:
            print(f"  - {p['nombre']}")
            print(f"    Coords: {p['latitud']}, {p['longitud']}")
            print(f"    Municipio: {p['municipio_nombre']}")
else:
    print(f"✗ Error: {data.get('error')}")
