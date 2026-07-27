"""
Script de prueba para verificar la carga de datos del Caquetá
"""
import requests
import json

# Configuración
BASE_URL = "http://localhost:5000"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
CAQUETA_URL = f"{BASE_URL}/api/super-admin/init-caqueta-data"

# Credenciales del super admin
USERNAME = "admin"
PASSWORD = "admin123"

def test_caqueta_data():
    print("=" * 70)
    print("TEST: Carga de Datos Electorales del Caquetá")
    print("=" * 70)
    
    # 1. Login
    print("\n1. Iniciando sesión como Super Admin...")
    login_response = requests.post(LOGIN_URL, json={
        "nombre": USERNAME,
        "password": PASSWORD,
        "rol": "super_admin"
    })
    
    if login_response.status_code != 200:
        print(f"❌ Error en login: {login_response.status_code}")
        print(login_response.text)
        return
    
    login_data = login_response.json()
    if not login_data.get('success'):
        print(f"❌ Login fallido: {login_data.get('error')}")
        return
    
    token = login_data['data']['access_token']
    print(f"✅ Login exitoso")
    
    # 2. Cargar datos del Caquetá
    print("\n2. Cargando datos electorales del Caquetá...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    caqueta_response = requests.post(CAQUETA_URL, headers=headers, json={})
    
    if caqueta_response.status_code != 200:
        print(f"❌ Error en carga: {caqueta_response.status_code}")
        print(caqueta_response.text)
        return
    
    caqueta_data = caqueta_response.json()
    
    if not caqueta_data.get('success'):
        print(f"❌ Carga fallida: {caqueta_data.get('error')}")
        return
    
    print(f"✅ {caqueta_data['message']}")
    
    # 3. Mostrar resultados
    print("\n3. Resultados detallados:")
    data = caqueta_data['data']
    details = data['details']
    
    print(f"\n   📊 SENADO 2022:")
    print(f"   - Creados: {details['senado']['created']}")
    print(f"   - Ya existían: {details['senado']['existing']}")
    
    print(f"\n   📊 CÁMARA CAQUETÁ 2022:")
    print(f"   - Creados: {details['camara']['created']}")
    print(f"   - Ya existían: {details['camara']['existing']}")
    
    print(f"\n   📊 ASAMBLEA DEPARTAMENTAL 2023:")
    print(f"   - Creados: {details['asamblea']['created']}")
    print(f"   - Ya existían: {details['asamblea']['existing']}")
    
    print(f"\n   📈 TOTALES:")
    print(f"   - Total creados: {data['total_created']}")
    print(f"   - Total existentes: {data['total_existing']}")
    print(f"   - GRAN TOTAL: {data['total_created'] + data['total_existing']} candidatos")
    
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETADO EXITOSAMENTE")
    print("=" * 70)

if __name__ == "__main__":
    try:
        test_caqueta_data()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
