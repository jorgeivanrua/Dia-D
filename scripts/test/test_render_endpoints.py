#!/usr/bin/env python3
"""
Script para verificar que los endpoints de Render están funcionando correctamente
"""
import requests
import json

# URL base de tu aplicación en Render
BASE_URL = "https://dia-d-r56corender.onrender.com"

def test_endpoint(url, description):
    """Probar un endpoint y mostrar resultado"""
    print(f"\n{'='*60}")
    print(f"Probando: {description}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS")
            print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ ERROR")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print(f"⏱️ TIMEOUT - El servidor tardó demasiado en responder")
    except requests.exceptions.ConnectionError:
        print(f"🔌 CONNECTION ERROR - No se pudo conectar al servidor")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

def main():
    print("\n" + "="*60)
    print("VERIFICACIÓN DE ENDPOINTS EN RENDER")
    print("="*60)
    
    # Probar endpoints públicos
    test_endpoint(
        f"{BASE_URL}/api/locations/departamentos",
        "Obtener departamentos (Caquetá)"
    )
    
    test_endpoint(
        f"{BASE_URL}/api/locations/municipios/44",
        "Obtener municipios de Caquetá"
    )
    
    test_endpoint(
        f"{BASE_URL}/api/locations/zonas/4401",
        "Obtener zonas de Florencia"
    )
    
    # Probar página de login
    test_endpoint(
        f"{BASE_URL}/auth/login",
        "Página de login"
    )
    
    print("\n" + "="*60)
    print("VERIFICACIÓN COMPLETADA")
    print("="*60)
    print("\nSi todos los endpoints responden con ✅, el despliegue fue exitoso.")
    print("Si hay errores ❌, espera unos minutos y vuelve a ejecutar este script.")
    print("\nPara ejecutar: python test_render_endpoints.py")

if __name__ == "__main__":
    main()
