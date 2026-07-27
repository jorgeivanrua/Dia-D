"""
Script para probar endpoints de monitoreo
"""
import requests
import json

# Configuración
BASE_URL = "http://localhost:5000/api"

def test_login():
    """Probar login con usuario monitoreo"""
    print("\n=== PROBANDO LOGIN ===")
    
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "rol": "monitoreo",
            "nombre": "monitoreo",
            "password": "monitoreo123"
        }
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Success: {data.get('success')}")
    
    if data.get('success'):
        token = data.get('data', {}).get('access_token') or data.get('access_token')
        if token:
            print(f"Token obtenido: {token[:50]}...")
            return token
        else:
            print(f"Error: No se encontró access_token en la respuesta")
            print(f"Respuesta completa: {json.dumps(data, indent=2)}")
            return None
    else:
        print(f"Error: {data.get('error')}")
        return None


def test_endpoint(endpoint, token, name):
    """Probar un endpoint específico"""
    print(f"\n=== PROBANDO {name} ===")
    print(f"Endpoint: {endpoint}")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        # Monitoreo no usa /api prefix
        url = f"http://localhost:5000{endpoint}"
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        
        data = response.json()
        print(f"Success: {data.get('success')}")
        
        if data.get('success'):
            print(f"[OK] {name} funciona correctamente")
            # Mostrar primeras líneas de datos
            if 'data' in data:
                data_str = json.dumps(data['data'], indent=2)
                lines = data_str.split('\n')[:10]
                print("Datos (primeras 10 líneas):")
                print('\n'.join(lines))
                if len(data_str.split('\n')) > 10:
                    print("...")
        else:
            print(f"[ERROR] Error: {data.get('error')}")
            
    except Exception as e:
        print(f"[ERROR] Excepcion: {str(e)}")


def main():
    print("=" * 60)
    print("PRUEBA DE ENDPOINTS DE MONITOREO")
    print("=" * 60)
    
    # 1. Login
    token = test_login()
    if not token:
        print("\n✗ No se pudo obtener token. Abortando pruebas.")
        return
    
    # 2. Probar endpoints (sin /api porque monitoreo no tiene ese prefijo)
    endpoints = [
        ("/monitoreo/usuarios-activos", "Usuarios Activos"),
        ("/monitoreo/estadisticas", "Estadísticas"),
        ("/monitoreo/alertas", "Alertas"),
        ("/monitoreo/actividad-reciente", "Actividad Reciente"),
        ("/monitoreo/metricas-rendimiento", "Métricas de Rendimiento"),
        ("/monitoreo/mapa-calor", "Mapa de Calor"),
        ("/monitoreo/tendencias", "Tendencias"),
        ("/monitoreo/comparativa-departamentos", "Comparativa de Departamentos"),
        ("/monitoreo/predicciones", "Predicciones"),
    ]
    
    for endpoint, name in endpoints:
        test_endpoint(endpoint, token, name)
    
    print("\n" + "=" * 60)
    print("PRUEBAS COMPLETADAS")
    print("=" * 60)


if __name__ == "__main__":
    main()
