"""Script para probar el endpoint de candidatos"""
import requests
import json

# Primero hacer login
login_response = requests.post('http://localhost:5000/api/auth/login', json={
    'nombre': 'Super Admin',
    'password': 'admin123',
    'rol': 'super_admin'
})

print("Login response:", login_response.status_code)
login_data = login_response.json()

print("Login data:", login_data)

if login_data.get('success'):
    token = login_data.get('access_token') or login_data.get('data', {}).get('access_token')
    if not token:
        print("Error: No se encontró token en la respuesta")
        exit(1)
    print(f"Token obtenido: {token[:20]}...")
    
    # Probar endpoint de candidatos
    candidatos_response = requests.get('http://localhost:5000/api/candidatos', 
        headers={'Authorization': f'Bearer {token}'}
    )
    
    print(f"\nCandidatos response: {candidatos_response.status_code}")
    candidatos_data = candidatos_response.json()
    
    if candidatos_data.get('success'):
        print(f"Total candidatos: {len(candidatos_data['data'])}")
        if len(candidatos_data['data']) > 0:
            print("\nPrimeros 3 candidatos:")
            for c in candidatos_data['data'][:3]:
                print(f"  - {c['nombre_completo']} ({c['cargo']})")
                print(f"    Partido: {c.get('partido', {}).get('nombre', 'N/A')}")
                print(f"    Tipo: {c.get('tipo_eleccion', {}).get('nombre', 'N/A')}")
    else:
        print(f"Error: {candidatos_data.get('error')}")
else:
    print(f"Error en login: {login_data.get('error')}")
