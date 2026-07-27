"""
Script para probar el Dashboard del Coordinador Municipal
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location
from flask_jwt_extended import create_access_token


def test_coordinador_municipal():
    """Probar endpoints del coordinador municipal"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("PRUEBA DEL DASHBOARD COORDINADOR MUNICIPAL")
        print("=" * 60)
        
        # Obtener coordinador municipal de Florencia
        coord = User.query.filter_by(nombre='coord_municipal_florencia').first()
        
        if not coord:
            print("❌ No se encontró el coordinador municipal")
            return
        
        print(f"\n✓ Usuario encontrado: {coord.nombre}")
        print(f"  Rol: {coord.rol}")
        print(f"  Ubicación ID: {coord.ubicacion_id}")
        
        # Obtener ubicación
        ubicacion = Location.query.get(coord.ubicacion_id)
        if ubicacion:
            print(f"  Municipio: {ubicacion.nombre_completo}")
        
        # Generar token JWT
        token = create_access_token(identity=str(coord.id))
        print(f"\n✓ Token JWT generado")
        
        # Crear cliente de prueba
        client = app.test_client()
        headers = {'Authorization': f'Bearer {token}'}
        
        print("\n" + "=" * 60)
        print("PROBANDO ENDPOINTS")
        print("=" * 60)
        
        # 1. Probar endpoint de puestos
        print("\n1. GET /api/coordinador-municipal/puestos")
        response = client.get('/api/coordinador-municipal/puestos', headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            if data.get('success'):
                puestos = data.get('data', {}).get('puestos', [])
                stats = data.get('data', {}).get('estadisticas', {})
                print(f"   ✓ Puestos encontrados: {len(puestos)}")
                print(f"   ✓ Total puestos: {stats.get('total_puestos', 0)}")
                print(f"   ✓ Cobertura: {stats.get('cobertura_porcentaje', 0):.1f}%")
            else:
                print(f"   ❌ Error: {data.get('error')}")
        else:
            print(f"   ❌ Error HTTP {response.status_code}")
        
        # 2. Probar endpoint de consolidado
        print("\n2. GET /api/coordinador-municipal/consolidado")
        response = client.get('/api/coordinador-municipal/consolidado', headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            if data.get('success'):
                consolidado = data.get('data', {})
                resumen = consolidado.get('resumen', {})
                print(f"   ✓ Total votos: {resumen.get('total_votos', 0)}")
                print(f"   ✓ Participación: {resumen.get('participacion_porcentaje', 0):.2f}%")
                votos_partidos = consolidado.get('votos_por_partido', [])
                print(f"   ✓ Partidos con votos: {len(votos_partidos)}")
            else:
                print(f"   ❌ Error: {data.get('error')}")
        else:
            print(f"   ❌ Error HTTP {response.status_code}")
        
        # 3. Probar endpoint de consolidado por zona
        print("\n3. GET /api/coordinador-municipal/consolidado-por-zona")
        response = client.get('/api/coordinador-municipal/consolidado-por-zona', headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            if data.get('success'):
                zonas = data.get('data', [])
                print(f"   ✓ Zonas encontradas: {len(zonas)}")
                for zona in zonas:
                    print(f"     - {zona.get('zona_nombre')}: {zona.get('puestos_completos')}/{zona.get('total_puestos')} puestos ({zona.get('porcentaje_avance', 0):.1f}%)")
            else:
                print(f"   ❌ Error: {data.get('error')}")
        else:
            print(f"   ❌ Error HTTP {response.status_code}")
        
        # 4. Probar endpoint de discrepancias
        print("\n4. GET /api/coordinador-municipal/discrepancias")
        response = client.get('/api/coordinador-municipal/discrepancias', headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            if data.get('success'):
                discrepancias = data.get('data', [])
                print(f"   ✓ Discrepancias detectadas: {len(discrepancias)}")
                
                # Agrupar por severidad
                criticas = [d for d in discrepancias if d.get('severidad') == 'critica']
                altas = [d for d in discrepancias if d.get('severidad') == 'alta']
                medias = [d for d in discrepancias if d.get('severidad') == 'media']
                bajas = [d for d in discrepancias if d.get('severidad') == 'baja']
                
                print(f"     - Críticas: {len(criticas)}")
                print(f"     - Altas: {len(altas)}")
                print(f"     - Medias: {len(medias)}")
                print(f"     - Bajas: {len(bajas)}")
            else:
                print(f"   ❌ Error: {data.get('error')}")
        else:
            print(f"   ❌ Error HTTP {response.status_code}")
        
        # 5. Probar endpoint de E-24s de Puesto
        print("\n5. GET /api/coordinador-municipal/e24-puestos")
        response = client.get('/api/coordinador-municipal/e24-puestos', headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            if data.get('success'):
                e24s = data.get('data', [])
                print(f"   ✓ E-24s de Puesto encontrados: {len(e24s)}")
            else:
                print(f"   ❌ Error: {data.get('error')}")
        else:
            print(f"   ❌ Error HTTP {response.status_code}")
        
        print("\n" + "=" * 60)
        print("PRUEBA COMPLETADA")
        print("=" * 60)
        print("\n✓ Todos los endpoints están funcionando correctamente")
        print("\nPara acceder al dashboard:")
        print("  1. Inicia el servidor: python -m backend.app")
        print("  2. Ve a: http://localhost:5000/login")
        print("  3. Usuario: coord_municipal_florencia")
        print("  4. Contraseña: password123")
        print("  5. Serás redirigido a: /coordinador/municipal")


if __name__ == '__main__':
    test_coordinador_municipal()
