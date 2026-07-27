"""
Script para verificar que zona_codigo se retorna correctamente
"""
import requests
import json

# Configuración
BASE_URL = 'http://localhost:5000'
USERNAME = 'coord_mun'
PASSWORD = 'coord123'

def test_zona_codigo():
    """Probar que el endpoint retorna zona_codigo"""
    
    # 1. Login
    print("1. Haciendo login...")
    login_response = requests.post(
        f'{BASE_URL}/api/auth/login',
        json={
            'username': USERNAME,
            'password': PASSWORD,
            'rol': 'coordinador_municipal'
        }
    )
    
    if login_response.status_code != 200:
        print(f"❌ Error en login: {login_response.status_code}")
        print(login_response.text)
        return
    
    token = login_response.json()['data']['token']
    print(f"✅ Login exitoso")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # 2. Obtener lista de puestos
    print("\n2. Obteniendo lista de puestos...")
    puestos_response = requests.get(
        f'{BASE_URL}/api/coordinador-municipal/puestos',
        headers=headers
    )
    
    if puestos_response.status_code != 200:
        print(f"❌ Error obteniendo puestos: {puestos_response.status_code}")
        print(puestos_response.text)
        return
    
    puestos_data = puestos_response.json()
    puestos = puestos_data['data']['puestos']
    print(f"✅ Obtenidos {len(puestos)} puestos")
    
    # Verificar zona_codigo en lista
    print("\n3. Verificando zona_codigo en lista de puestos:")
    for i, puesto in enumerate(puestos[:3]):  # Primeros 3
        zona = puesto.get('zona_codigo', 'NO EXISTE')
        print(f"   Puesto {puesto['codigo']}: zona_codigo = '{zona}'")
    
    # 3. Obtener detalle del primer puesto
    if puestos:
        primer_puesto_id = puestos[0]['id']
        print(f"\n4. Obteniendo detalle del puesto ID {primer_puesto_id}...")
        
        detalle_response = requests.get(
            f'{BASE_URL}/api/coordinador-municipal/puesto/{primer_puesto_id}',
            headers=headers
        )
        
        if detalle_response.status_code != 200:
            print(f"❌ Error obteniendo detalle: {detalle_response.status_code}")
            print(detalle_response.text)
            return
        
        detalle_data = detalle_response.json()
        print(f"✅ Detalle obtenido")
        
        # Verificar estructura de respuesta
        print("\n5. Estructura de respuesta:")
        print(json.dumps(detalle_data, indent=2, ensure_ascii=False))
        
        # Verificar zona_codigo específicamente
        puesto_info = detalle_data.get('data', {}).get('puesto', {})
        zona_codigo = puesto_info.get('zona_codigo')
        
        print(f"\n6. Verificación de zona_codigo:")
        print(f"   ✓ Existe en respuesta: {'zona_codigo' in puesto_info}")
        print(f"   ✓ Valor: '{zona_codigo}'")
        print(f"   ✓ Tipo: {type(zona_codigo)}")
        
        if zona_codigo:
            print(f"\n✅ ÉXITO: zona_codigo se retorna correctamente: '{zona_codigo}'")
        else:
            print(f"\n⚠️ ADVERTENCIA: zona_codigo es None o vacío")
    else:
        print("❌ No hay puestos para probar")

if __name__ == '__main__':
    test_zona_codigo()
