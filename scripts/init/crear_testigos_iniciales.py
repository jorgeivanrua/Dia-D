"""
Script para crear testigos electorales para los primeros puestos de Florencia
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location


def crear_testigos_iniciales():
    """Crear testigos para los primeros puestos de Florencia"""
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("\n" + "=" * 80)
        print("CREANDO TESTIGOS ELECTORALES PARA PRIMEROS PUESTOS")
        print("=" * 80)
        print()
        
        # Obtener los primeros 10 puestos de Florencia
        puestos = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo='44',
            municipio_codigo='4401',
            activo=True
        ).order_by(Location.puesto_codigo).limit(10).all()
        
        if not puestos:
            print("❌ Error: No se encontraron puestos en Florencia")
            print("   Ejecuta primero: python scripts/load_divipola.py")
            return
        
        print(f"✅ Se encontraron {len(puestos)} puestos en Florencia")
        print()
        
        # Crear testigos
        testigos_creados = 0
        testigos_existentes = 0
        
        for puesto in puestos:
            print(f"📍 Puesto: {puesto.puesto_nombre} (Código: {puesto.puesto_codigo})")
            
            # Crear 3 testigos por puesto
            for i in range(1, 4):
                nombre_testigo = f'testigo_{puesto.puesto_codigo}_{i}'
                
                # Verificar si ya existe
                testigo_existente = User.query.filter_by(
                    nombre=nombre_testigo,
                    rol='testigo_electoral'
                ).first()
                
                if testigo_existente:
                    print(f"   ⚠️  Testigo {i} ya existe: {nombre_testigo}")
                    testigos_existentes += 1
                    continue
                
                # Crear testigo
                testigo = User(
                    nombre=nombre_testigo,
                    rol='testigo_electoral',
                    ubicacion_id=puesto.id,
                    activo=True
                )
                testigo.set_password('test123')
                
                db.session.add(testigo)
                testigos_creados += 1
                print(f"   ✅ Testigo {i} creado: {nombre_testigo}")
            
            print()
        
        # Commit
        db.session.commit()
        
        # Resumen
        print("=" * 80)
        print("RESUMEN")
        print("=" * 80)
        print(f"Puestos procesados: {len(puestos)}")
        print(f"Testigos creados: {testigos_creados}")
        print(f"Testigos ya existentes: {testigos_existentes}")
        print(f"Total testigos: {testigos_creados + testigos_existentes}")
        print()
        
        # Mostrar algunos ejemplos de credenciales
        print("=" * 80)
        print("EJEMPLOS DE CREDENCIALES")
        print("=" * 80)
        print()
        
        primer_puesto = puestos[0]
        print(f"Puesto: {primer_puesto.puesto_nombre}")
        print(f"Código: {primer_puesto.puesto_codigo}")
        print()
        print("Testigos:")
        for i in range(1, 4):
            print(f"  - Usuario: testigo_{primer_puesto.puesto_codigo}_{i}")
            print(f"    Password: test123")
            print(f"    Rol: Testigo Electoral")
            print()
        
        print("=" * 80)
        print("INSTRUCCIONES DE LOGIN")
        print("=" * 80)
        print()
        print("1. Ir a: https://dia-d-x7pe.onrender.com/auth/login")
        print("2. Seleccionar rol: Testigo Electoral")
        print("3. Seleccionar ubicación:")
        print("   - Departamento: CAQUETA")
        print("   - Municipio: FLORENCIA")
        print("   - Zona: (seleccionar la zona del puesto)")
        print("   - Puesto: (seleccionar el puesto)")
        print("4. Ingresar contraseña: test123")
        print()
        print("=" * 80)
        print("✅ TESTIGOS CREADOS EXITOSAMENTE")
        print("=" * 80)


if __name__ == '__main__':
    crear_testigos_iniciales()
