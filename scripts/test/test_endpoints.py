#!/usr/bin/env python3
"""
Script de verificación de endpoints
"""
import requests

BASE_URL = "http://localhost:5000"

def test_endpoint(endpoint, name):
    """Probar un endpoint"""
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        status = "✅ OK" if response.status_code == 200 else f"❌ {response.status_code}"
        
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('data', [])) if isinstance(data.get('data'), list) else 'N/A'
            print(f"{status} - {name}: {count} registros")
        else:
            print(f"{status} - {name}")
            
    except Exception as e:
        print(f"❌ ERROR - {name}: {str(e)}")

if __name__ == "__main__":
    print("=" * 60)
    print("VERIFICACIÓN DE ENDPOINTS")
    print("=" * 60)
    
    # Endpoints públicos
    test_endpoint("/api/candidatos", "Candidatos")
    test_endpoint("/api/partidos", "Partidos")
    test_endpoint("/api/configuracion/tipos-eleccion", "Tipos de Elección")
    test_endpoint("/api/locations/puestos-geolocalizados", "Puestos Geolocalizados")
    
    print("=" * 60)
