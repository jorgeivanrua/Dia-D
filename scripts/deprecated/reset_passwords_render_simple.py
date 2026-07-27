"""
Script para resetear contraseñas en Render
"""
import requests
import json

# URL de tu aplicación en Render
RENDER_URL = "https://dia-o.onrender.com"

def reset_passwords():
    """Resetear todas las contraseñas en Render"""
    
    print("🔄 Reseteando contraseñas en Render...")
    print(f"📡 URL: {RENDER_URL}")
    
    try:
        # Llamar al endpoint de reseteo
        url = f"{RENDER_URL}/reset-all-passwords-secret-endpoint-2024"
        
        print(f"\n📤 Enviando petición a: {url}")
        
        response = requests.post(url, timeout=30)
        
        print(f"\n📥 Respuesta recibida:")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ {data.get('message')}")
            print(f"\n👥 Usuarios actualizados: {data.get('usuarios_actualizados')}")
            
            if 'usuarios' in data:
                print("\n📋 Lista de usuarios y contraseñas:")
                print("-" * 60)
                for usuario in data['usuarios']:
                    print(f"   Usuario: {usuario['username']}")
                    print(f"   Nombre: {usuario['nombre']}")
                    print(f"   Rol: {usuario['rol']}")
                    print(f"   Contraseña: {usuario['password']}")
                    print("-" * 60)
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except requests.exceptions.Timeout:
        print("\n⏱️  Timeout: La petición tardó demasiado")
        print("   Esto es normal en Render si el servicio estaba dormido")
        print("   Intenta nuevamente en 30 segundos")
    except requests.exceptions.ConnectionError:
        print("\n❌ Error de conexión")
        print("   Verifica que la URL sea correcta y que el servicio esté activo")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == '__main__':
    reset_passwords()
