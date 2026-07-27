"""
Script para diagnosticar la asignación de testigos y verificación de presencia
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location

app = create_app('development')

with app.app_context():
    print("\n" + "="*80)
    print("DIAGNÓSTICO DE TESTIGOS Y VERIFICACIÓN DE PRESENCIA")
    print("="*80)
    
    # Obtener todos los testigos
    testigos = User.query.filter_by(rol='testigo_electoral', activo=True).all()
    
    print(f"\n📊 Total de testigos activos: {len(testigos)}\n")
    
    for testigo in testigos:
        print(f"\n👤 Testigo: {testigo.nombre}")
        print(f"   ID: {testigo.id}")
        print(f"   Ubicación ID: {testigo.ubicacion_id}")
        print(f"   Presencia verificada: {'✅ SÍ' if testigo.presencia_verificada else '❌ NO'}")
        
        if testigo.presencia_verificada_at:
            print(f"   Verificada el: {testigo.presencia_verificada_at}")
        
        # Obtener la ubicación (mesa) asignada
        if testigo.ubicacion_id:
            ubicacion = Location.query.get(testigo.ubicacion_id)
            if ubicacion:
                print(f"   Asignado a: {ubicacion.tipo} - {ubicacion.nombre_completo}")
                print(f"   Códigos: Depto={ubicacion.departamento_codigo}, Mun={ubicacion.municipio_codigo}, Zona={ubicacion.zona_codigo}, Puesto={ubicacion.puesto_codigo}, Mesa={ubicacion.mesa_codigo}")
                
                # Buscar el puesto correspondiente
                if ubicacion.tipo == 'mesa':
                    puesto = Location.query.filter_by(
                        tipo='puesto',
                        departamento_codigo=ubicacion.departamento_codigo,
                        municipio_codigo=ubicacion.municipio_codigo,
                        zona_codigo=ubicacion.zona_codigo,
                        puesto_codigo=ubicacion.puesto_codigo
                    ).first()
                    
                    if puesto:
                        print(f"   Puesto correspondiente: {puesto.nombre_completo} (ID: {puesto.id})")
                        
                        # Buscar coordinador de ese puesto
                        coordinador = User.query.filter_by(
                            rol='coordinador_puesto',
                            ubicacion_id=puesto.id,
                            activo=True
                        ).first()
                        
                        if coordinador:
                            print(f"   Coordinador del puesto: {coordinador.nombre}")
                        else:
                            print(f"   ⚠️  No hay coordinador asignado a este puesto")
            else:
                print(f"   ⚠️  Ubicación no encontrada")
        else:
            print(f"   ⚠️  Sin ubicación asignada")
    
    print("\n" + "="*80)
    print("COORDINADORES DE PUESTO")
    print("="*80)
    
    coordinadores = User.query.filter_by(rol='coordinador_puesto', activo=True).all()
    
    print(f"\n📊 Total de coordinadores de puesto: {len(coordinadores)}\n")
    
    for coordinador in coordinadores:
        print(f"\n👤 Coordinador: {coordinador.nombre}")
        print(f"   ID: {coordinador.id}")
        print(f"   Ubicación ID: {coordinador.ubicacion_id}")
        
        if coordinador.ubicacion_id:
            puesto = Location.query.get(coordinador.ubicacion_id)
            if puesto:
                print(f"   Puesto asignado: {puesto.nombre_completo}")
                print(f"   Códigos: Depto={puesto.departamento_codigo}, Mun={puesto.municipio_codigo}, Zona={puesto.zona_codigo}, Puesto={puesto.puesto_codigo}")
                
                # Buscar mesas de este puesto
                mesas = Location.query.filter_by(
                    tipo='mesa',
                    departamento_codigo=puesto.departamento_codigo,
                    municipio_codigo=puesto.municipio_codigo,
                    zona_codigo=puesto.zona_codigo,
                    puesto_codigo=puesto.puesto_codigo
                ).all()
                
                print(f"   Mesas en este puesto: {len(mesas)}")
                
                # Buscar testigos en esas mesas
                mesa_ids = [mesa.id for mesa in mesas]
                testigos_puesto = User.query.filter(
                    User.ubicacion_id.in_(mesa_ids),
                    User.rol == 'testigo_electoral',
                    User.activo == True
                ).all()
                
                print(f"   Testigos asignados: {len(testigos_puesto)}")
                
                for t in testigos_puesto:
                    mesa = Location.query.get(t.ubicacion_id)
                    estado = "✅ Presente" if t.presencia_verificada else "❌ Ausente"
                    print(f"      - {t.nombre} (Mesa {mesa.mesa_codigo if mesa else '?'}) - {estado}")
    
    print("\n" + "="*80)
