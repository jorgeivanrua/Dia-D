"""
Script para marcar testigos específicos como usuarios básicos del sistema
Esto asegura que al menos 1 testigo por puesto sea persistente
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

def marcar_testigos_basicos():
    """
    Marcar al menos 1 testigo por puesto como usuario básico del sistema
    """
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("=" * 80)
        print("MARCAR TESTIGOS COMO USUARIOS BÁSICOS".center(80))
        print("=" * 80)
        print()
        
        # Obtener todos los puestos de votación
        puestos = Location.query.filter_by(tipo='puesto').all()
        
        print(f"📊 Encontrados {len(puestos)} puestos de votación")
        print()
        
        testigos_marcados = 0
        puestos_sin_testigo = []
        
        for puesto in puestos:
            # Buscar testigos en este puesto
            testigos = User.query.filter_by(
                rol='testigo_electoral',
                ubicacion_id=puesto.id,
                activo=True
            ).all()
            
            if not testigos:
                puestos_sin_testigo.append(puesto.nombre_completo)
                continue
            
            # Verificar si ya hay un testigo básico
            testigo_basico = next((t for t in testigos if t.es_usuario_basico), None)
            
            if testigo_basico:
                print(f"✅ {puesto.nombre_completo}: Ya tiene testigo básico ({testigo_basico.nombre})")
            else:
                # Marcar el primer testigo como básico
                primer_testigo = testigos[0]
                primer_testigo.es_usuario_basico = True
                testigos_marcados += 1
                print(f"🔧 {puesto.nombre_completo}: Marcando testigo básico ({primer_testigo.nombre})")
        
        if testigos_marcados > 0:
            db.session.commit()
            print()
            print(f"✅ {testigos_marcados} testigos marcados como usuarios básicos")
        
        if puestos_sin_testigo:
            print()
            print("⚠️  Puestos sin testigos:")
            for puesto in puestos_sin_testigo:
                print(f"   • {puesto}")
        
        print()
        print("=" * 80)
        print("✅ PROCESO COMPLETADO".center(80))
        print("=" * 80)

if __name__ == '__main__':
    try:
        marcar_testigos_basicos()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
