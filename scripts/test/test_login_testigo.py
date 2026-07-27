"""
Script para probar el login de un testigo
"""
import requests
import json

BASE_URL = "http://localhost:5000"

# Datos de prueba - Testigo de Florencia
# Según la BD: Depto 44, Muni 01, Zona 01, Puesto 01
login_data = {
    "rol": "testigo_electoral",
    "departamento_codigo": "44",  # Caquetá
    "municipio_codigo": "01",     # Florencia
    "zona_codigo": "01",          # Zona 01
    "puesto_codigo": "01",        # Puesto 01
    "password": "test123"
}

print("=" * 80)
print("TEST DE LOGIN - TESTIGO ELECTORAL")
print("=" * 80)
print()
print("Datos de login:")
print(f"  Rol: {login_data['rol']}")
print(f"  Departamento: {login_data['departamento_codigo']}")
print(f"  Municipio: {login_data['municipio_codigo']}")
print(f"  Zona: {login_data['zona_codigo']}")
print(f"  Puesto: {login_data['puesto_codigo']}")
print(f"  Contraseña: {login_data['password']}")
print()

try:
    print("Enviando petición de login...")
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print()
    
    if response.status_code == 200:
        data = response.json()
        print("✅ LOGIN EXITOSO")
        print()
        print("Datos del usuario:")
        print(json.dumps(data.get('data', {}).get('user', {}), indent=2, ensure_ascii=False))
        print()
        print("Token de acceso recibido:", "Sí" if data.get('data', {}).get('access_token') else "No")
    else:
        print("❌ LOGIN FALLIDO")
        print()
        print("Respuesta:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)
