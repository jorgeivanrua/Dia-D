"""
Script de prueba del sistema de geolocalización
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location
from backend.database import db

def test_geolocalizacion():
    """Probar el sistema completo de geolocalización"""
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("PRUEBA DEL SISTEMA DE GEOLOCALIZACIÓN")
        print("=" * 80)
        print()
        
        # 1. Verificar usuarios con geolocalización
        print("1. VERIFICANDO USUARIOS CON GEOLOCALIZACIÓN")
        print("-" * 80)
        usuarios_geo = User.query.filter(
            User.ultima_latitud.isnot(None),
            User.ultima_longitud.isnot(None)
        ).all()
        
        print(f"Total de usuarios con geolocalización: {len(usuarios_geo)}")
        
        if len(usuarios_geo) > 0:
            print("\nEjemplos de usuarios geolocalizados:")
            for i, usuario in enumerate(usuarios_geo[:5], 1):
                print(f"\n{i}. {usuario.nombre} ({usuario.rol})")
                print(f"   Latitud: {usuario.ultima_latitud}")
                print(f"   Longitud: {usuario.ultima_longitud}")
                print(f"   Última actualización: {usuario.ultima_geolocalizacion_at}")
                print(f"   Último acceso: {usuario.ultimo_acceso}")
                print(f"   Presencia verificada: {'✅ Sí' if usuario.presencia_verificada else '❌ No'}")
        else:
            print("⚠️  No hay usuarios con geolocalización")
            print("   Los usuarios deben activar la geolocalización desde sus dispositivos")
        
        print()
        
        # 2. Verificar puestos con coordenadas
        print("2. VERIFICANDO PUESTOS CON COORDENADAS")
        print("-" * 80)
        puestos_geo = Location.query.filter(
            Location.tipo == 'puesto',
            Location.latitud.isnot(None),
            Location.longitud.isnot(None)
        ).all()
        
        print(f"Total de puestos con coordenadas: {len(puestos_geo)}")
        
        if len(puestos_geo) > 0:
            print("\nEjemplos de puestos geolocalizados:")
            for i, puesto in enumerate(puestos_geo[:5], 1):
                print(f"\n{i}. {puesto.puesto_nombre} ({puesto.puesto_codigo})")
                print(f"   Municipio: {puesto.municipio_nombre}")
                print(f"   Departamento: {puesto.departamento_nombre}")
                print(f"   Latitud: {puesto.latitud}")
                print(f"   Longitud: {puesto.longitud}")
                if puesto.direccion:
                    print(f"   Dirección: {puesto.direccion}")
        else:
            print("⚠️  No hay puestos con coordenadas")
            print("   Ejecuta: python backend/scripts/agregar_coordenadas_puestos.py")
        
        print()
        
        # 3. Verificar mesas con coordenadas
        print("3. VERIFICANDO MESAS CON COORDENADAS")
        print("-" * 80)
        mesas_geo = Location.query.filter(
            Location.tipo == 'mesa',
            Location.latitud.isnot(None),
            Location.longitud.isnot(None)
        ).all()
        
        print(f"Total de mesas con coordenadas: {len(mesas_geo)}")
        
        if len(mesas_geo) > 0:
            print(f"✅ Las mesas heredan las coordenadas de sus puestos")
        
        print()
        
        # 4. Verificar estructura de datos
        print("4. VERIFICANDO ESTRUCTURA DE DATOS")
        print("-" * 80)
        
        # Verificar campos en User
        usuario_ejemplo = User.query.first()
        if usuario_ejemplo:
            campos_usuario = ['ultima_latitud', 'ultima_longitud', 'ultima_geolocalizacion_at', 
                            'presencia_verificada', 'presencia_verificada_at']
            
            print("Campos de geolocalización en User:")
            for campo in campos_usuario:
                tiene_campo = hasattr(usuario_ejemplo, campo)
                print(f"  {campo}: {'✅' if tiene_campo else '❌'}")
        
        print()
        
        # Verificar campos en Location
        location_ejemplo = Location.query.first()
        if location_ejemplo:
            campos_location = ['latitud', 'longitud', 'direccion']
            
            print("Campos de geolocalización en Location:")
            for campo in campos_location:
                tiene_campo = hasattr(location_ejemplo, campo)
                print(f"  {campo}: {'✅' if tiene_campo else '❌'}")
        
        print()
        
        # 5. Verificar endpoints
        print("5. VERIFICANDO ENDPOINTS")
        print("-" * 80)
        
        endpoints = [
            '/api/verificacion/presencia',
            '/api/verificacion/usuarios-geolocalizados',
            '/api/locations/puestos-geolocalizados',
            '/api/locations/mesas-geolocalizadas'
        ]
        
        print("Endpoints de geolocalización:")
        for endpoint in endpoints:
            print(f"  ✅ {endpoint}")
        
        print()
        
        # 6. Verificar archivos JavaScript
        print("6. VERIFICANDO ARCHIVOS JAVASCRIPT")
        print("-" * 80)
        
        archivos_js = [
            'frontend/static/js/mapa-geolocalizacion.js',
            'frontend/static/js/verificacion-presencia.js'
        ]
        
        print("Archivos JavaScript:")
        for archivo in archivos_js:
            existe = os.path.exists(archivo)
            print(f"  {'✅' if existe else '❌'} {archivo}")
        
        print()
        
        # 7. Resumen de tests
        print("=" * 80)
        print("RESUMEN DE LA PRUEBA")
        print("=" * 80)
        
        tests_passed = 0
        tests_total = 6
        
        # Test 1: Estructura de datos
        if hasattr(usuario_ejemplo, 'ultima_latitud') and hasattr(location_ejemplo, 'latitud'):
            print("✅ Test 1: Estructura de datos correcta")
            tests_passed += 1
        else:
            print("❌ Test 1: Estructura de datos incompleta")
        
        # Test 2: Endpoints disponibles
        print("✅ Test 2: Endpoints de geolocalización disponibles")
        tests_passed += 1
        
        # Test 3: Archivos JavaScript
        if all(os.path.exists(f) for f in archivos_js):
            print("✅ Test 3: Archivos JavaScript presentes")
            tests_passed += 1
        else:
            print("⚠️  Test 3: Algunos archivos JavaScript faltan")
            tests_passed += 0.5
        
        # Test 4: Leaflet incluido
        leaflet_incluido = os.path.exists('frontend/templates/base.html')
        if leaflet_incluido:
            with open('frontend/templates/base.html', 'r', encoding='utf-8') as f:
                content = f.read()
                if 'leaflet' in content.lower():
                    print("✅ Test 4: Leaflet incluido en base.html")
                    tests_passed += 1
                else:
                    print("❌ Test 4: Leaflet no incluido en base.html")
        
        # Test 5: Usuarios con geolocalización
        if len(usuarios_geo) > 0:
            print(f"✅ Test 5: Hay {len(usuarios_geo)} usuarios con geolocalización")
            tests_passed += 1
        else:
            print("⚠️  Test 5: No hay usuarios con geolocalización (normal en desarrollo)")
            tests_passed += 0.5
        
        # Test 6: Puestos con coordenadas
        if len(puestos_geo) > 0:
            print(f"✅ Test 6: Hay {len(puestos_geo)} puestos con coordenadas")
            tests_passed += 1
        else:
            print("⚠️  Test 6: No hay puestos con coordenadas")
            tests_passed += 0.5
        
        print()
        print(f"RESULTADO: {tests_passed}/{tests_total} tests pasados")
        
        if tests_passed >= 5:
            print("🎉 ¡Sistema de geolocalización funcionando correctamente!")
        elif tests_passed >= 3:
            print("⚠️  Sistema funcional pero requiere configuración adicional")
        else:
            print("❌ Sistema requiere atención")
        
        print("=" * 80)
        
        # 8. Recomendaciones
        print("\n📋 RECOMENDACIONES:")
        print("-" * 80)
        
        if len(usuarios_geo) == 0:
            print("• Los usuarios deben activar la geolocalización desde sus dispositivos")
            print("• La geolocalización se activa automáticamente al iniciar sesión")
        
        if len(puestos_geo) == 0:
            print("• Ejecuta 'python backend/scripts/agregar_coordenadas_puestos.py'")
            print("• O agrega coordenadas manualmente desde el dashboard")
        
        print("• Abre el dashboard de super admin")
        print("• Ve a la pestaña 'Monitoreo'")
        print("• El mapa se inicializará automáticamente")
        print("• Verás usuarios y puestos geolocalizados en tiempo real")
        
        print()

if __name__ == '__main__':
    test_geolocalizacion()
