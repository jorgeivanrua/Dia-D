"""
Script para verificar la contraseña de un testigo
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location
from backend.database import db

def check_testigo():
    """Verificar testigos y sus contraseñas"""
    app = create_app()
    
    with app.app_context():
        # Buscar testigos
        testigos = User.query.filter_by(rol='testigo_electoral').limit(5).all()
        
        print("\n" + "="*80)
        print("TESTIGOS ENCONTRADOS")
        print("="*80)
        
        if not testigos:
            print("❌ No hay testigos en la base de datos")
            return
        
        for testigo in testigos:
            ubicacion = Location.query.get(testigo.ubicacion_id) if testigo.ubicacion_id else None
            
            print(f"\n📋 Testigo: {testigo.nombre}")
            print(f"   ID: {testigo.id}")
            print(f"   Activo: {testigo.activo}")
            
            if ubicacion:
                print(f"   Ubicación: {ubicacion.nombre_completo}")
                print(f"   Tipo: {ubicacion.tipo}")
                if ubicacion.tipo == 'puesto':
                    print(f"   Puesto Código: {ubicacion.puesto_codigo}")
                    print(f"   Municipio: {ubicacion.municipio_codigo}")
                    print(f"   Zona: {ubicacion.zona_codigo}")
            
            # Probar contraseñas comunes
            passwords_to_test = [
                'testigo123',
                'Testigo123!',
                'test123',
                '123456',
                'password'
            ]
            
            print(f"\n   Probando contraseñas:")
            for pwd in passwords_to_test:
                if testigo.check_password(pwd):
                    print(f"   ✅ Contraseña correcta: '{pwd}'")
                    break
            else:
                print(f"   ❌ Ninguna contraseña común funciona")
        
        print("\n" + "="*80)

if __name__ == '__main__':
    check_testigo()
