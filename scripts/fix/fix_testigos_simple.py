"""
Script simple para reasignar testigos de mesas a puestos
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location
from backend.database import db

def fix_testigos():
    """Reasignar testigos de mesas a puestos"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*80)
        print("REASIGNANDO TESTIGOS DE MESAS A PUESTOS")
        print("="*80)
        
        # Buscar todos los testigos
        testigos = User.query.filter_by(rol='testigo_electoral').all()
        
        print(f"\nTotal testigos encontrados: {len(testigos)}")
        
        testigos_actualizados = 0
        
        for testigo in testigos:
            if not testigo.ubicacion_id:
                print(f"Testigo {testigo.nombre} sin ubicacion")
                continue
            
            ubicacion = Location.query.get(testigo.ubicacion_id)
            
            if not ubicacion:
                print(f"Ubicacion no encontrada para testigo {testigo.nombre}")
                continue
            
            print(f"\nTestigo: {testigo.nombre}")
            print(f"  Ubicacion actual tipo: {ubicacion.tipo}")
            
            if ubicacion.tipo != 'mesa':
                print(f"  Ya esta asignado a {ubicacion.tipo}")
                continue
            
            # Buscar el puesto correspondiente
            puesto = Location.query.filter_by(
                tipo='puesto',
                departamento_codigo=ubicacion.departamento_codigo,
                municipio_codigo=ubicacion.municipio_codigo,
                zona_codigo=ubicacion.zona_codigo,
                puesto_codigo=ubicacion.puesto_codigo
            ).first()
            
            if not puesto:
                print(f"  ERROR: No se encontro puesto")
                continue
            
            print(f"  Reasignando de mesa a puesto {puesto.puesto_codigo}")
            
            # Reasignar al puesto
            testigo.ubicacion_id = puesto.id
            testigos_actualizados += 1
        
        db.session.commit()
        
        print("\n" + "="*80)
        print(f"COMPLETADO: {testigos_actualizados} testigos reasignados")
        print("="*80)

if __name__ == '__main__':
    fix_testigos()
