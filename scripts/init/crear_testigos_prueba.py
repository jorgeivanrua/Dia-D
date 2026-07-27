"""
Script para crear testigos de prueba
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.app import create_app


def crear_testigos_prueba():
    print("\n" + "="*60)
    print("CREACION DE TESTIGOS DE PRUEBA")
    print("="*60 + "\n")
    
    puesto = Location.query.filter_by(puesto_codigo='01', tipo='puesto').first()
    
    if not puesto:
        print("ERROR: Puesto 01 no encontrado")
        return
    
    print(f"Puesto encontrado: {puesto.nombre_completo}")
    
    mesas = Location.query.filter_by(
        puesto_codigo='01',
        tipo='mesa',
        departamento_codigo=puesto.departamento_codigo,
        municipio_codigo=puesto.municipio_codigo,
        zona_codigo=puesto.zona_codigo
    ).limit(3).all()
    
    print(f"\nMesas encontradas: {len(mesas)}")
    
    if len(mesas) == 0:
        print("ERROR: No se encontraron mesas")
        return
    
    print("\n" + "="*60)
    print("CREANDO TESTIGOS")
    print("="*60 + "\n")
    
    testigos_creados = 0
    
    for i, mesa in enumerate(mesas, 1):
        print(f"{i}. Mesa {mesa.mesa_codigo} (ID: {mesa.id})")
        
        testigo_existente = User.query.filter_by(
            ubicacion_id=mesa.id,
            rol='testigo_electoral'
        ).first()
        
        if testigo_existente:
            print(f"   Ya existe testigo: {testigo_existente.nombre}")
            continue
        
        testigo = User()
        testigo.nombre = f"Testigo Mesa {mesa.mesa_codigo}"
        testigo.set_password("testigo123")
        testigo.rol = 'testigo_electoral'
        testigo.ubicacion_id = mesa.id
        testigo.activo = True
        testigo.presencia_verificada = False
        
        try:
            db.session.add(testigo)
            db.session.commit()
            
            print(f"   Testigo creado: {testigo.nombre}")
            print(f"   Usuario: {testigo.nombre}")
            print(f"   Password: testigo123")
            print(f"   ID: {testigo.id}")
            testigos_creados += 1
            
        except Exception as e:
            db.session.rollback()
            print(f"   Error: {str(e)}")
        
        print()
    
    print("="*60)
    print("RESUMEN")
    print("="*60)
    print(f"Testigos creados: {testigos_creados}/{len(mesas)}")
    print()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        crear_testigos_prueba()
