"""
Test para verificar la carga de logos
"""
import requests

BASE_URL = "http://localhost:5000"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
LOGOS_URL = f"{BASE_URL}/api/admin/cargar-logos-partidos"

def test_logos():
    print("=" * 70)
    print("TEST: Carga de Logos de Partidos")
    print("=" * 70)
    
    # 1. Login
    print("\n1. Iniciando sesión como Super Admin...")
    login_response = requests.post(LOGIN_URL, json={
        "nombre": "admin",
        "password": "admin123",
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
    
    # 2. Cargar logos
    print("\n2. Cargando logos de partidos...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    logos_response = requests.post(LOGOS_URL, headers=headers, json={})
    
    print(f"\nStatus Code: {logos_response.status_code}")
    print(f"Response: {logos_response.text}")
    
    if logos_response.status_code != 200:
        print(f"❌ Error en carga: {logos_response.status_code}")
        return
    
    logos_data = logos_response.json()
    
    if not logos_data.get('success'):
        print(f"❌ Carga fallida: {logos_data.get('error')}")
        return
    
    print(f"✅ {logos_data['message']}")
    
    # 3. Mostrar resultados
    print("\n3. Resultados detallados:")
    data = logos_data['data']
    
    print(f"\n   📊 RESUMEN:")
    print(f"   - Total partidos: {data['total_partidos']}")
    print(f"   - Logos actualizados: {data['total_actualizados']}")
    print(f"   - Sin cambios: {data['total_sin_cambios']}")
    print(f"   - Sin logo: {data['total_sin_logo']}")
    
    if data['actualizados']:
        print(f"\n   ✅ ACTUALIZADOS:")
        for p in data['actualizados']:
            print(f"   - {p['nombre']}")
    
    if data['sin_logo']:
        print(f"\n   ⚠️  SIN LOGO:")
        for p in data['sin_logo']:
            print(f"   - {p['nombre']}")
    
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETADO")
    print("=" * 70)

if __name__ == "__main__":
    try:
        test_logos()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
