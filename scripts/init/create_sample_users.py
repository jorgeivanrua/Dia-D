"""
Script para crear usuarios coordinadores y testigos con asignaciones a ubicaciones
Este es el script DEFINITIVO para crear todos los usuarios necesarios
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

def create_sample_users():
    """Crear usuarios de prueba coordinados por ubicación"""
    
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("\n" + "=" * 80)
        print("CREACIÓN DE USUARIOS DE PRUEBA (COORDINADORES Y TESTIGOS)")
        print("=" * 80 + "\n")
        
        users_data = []
        
        # 1. COORDINADOR DEPARTAMENTAL para Caquetá
        dept_caqueta = Location.query.filter_by(
            departamento_codigo='44',
            tipo='departamento'
        ).first()
        
        if dept_caqueta:
            coord_dpto = User.query.filter_by(nombre='coord_dpto_caqueta').first()
            if not coord_dpto:
                coord_dpto = User(
                    nombre='coord_dpto_caqueta',
                    rol='coordinador_departamental',
                    ubicacion_id=dept_caqueta.id,
                    activo=True,
                    es_usuario_basico=False
                )
                coord_dpto.set_password('coord123')
                db.session.add(coord_dpto)
                users_data.append(('coord_dpto_caqueta', 'coord123', 'Coordinador Departamental'))
                print(f"✅ Creado: coord_dpto_caqueta (Coordinador Departamental)")
        
        # 2. COORDINADOR MUNICIPAL para Florencia
        mun_florencia = Location.query.filter_by(
            departamento_codigo='44',
            municipio_codigo='4401',
            tipo='municipio'
        ).first()
        
        if mun_florencia:
            coord_mun = User.query.filter_by(nombre='coord_mun_florencia').first()
            if not coord_mun:
                coord_mun = User(
                    nombre='coord_mun_florencia',
                    rol='coordinador_municipal',
                    ubicacion_id=mun_florencia.id,
                    activo=True,
                    es_usuario_basico=False
                )
                coord_mun.set_password('coord123')
                db.session.add(coord_mun)
                users_data.append(('coord_mun_florencia', 'coord123', 'Coordinador Municipal'))
                print(f"✅ Creado: coord_mun_florencia (Coordinador Municipal)")
        
        # 3. COORDINADOR DE PUESTO para Florencia
        puestos_florencia = Location.query.filter_by(
            municipio_codigo='4401',
            tipo='puesto'
        ).limit(3).all()
        
        for idx, puesto in enumerate(puestos_florencia, 1):
            coord_name = f'coord_puesto_flo_{idx:02d}'
            coord_existing = User.query.filter_by(nombre=coord_name).first()
            
            if not coord_existing:
                coord = User(
                    nombre=coord_name,
                    rol='coordinador_puesto',
                    ubicacion_id=puesto.id,
                    activo=True,
                    es_usuario_basico=False
                )
                coord.set_password('puesto123')
                db.session.add(coord)
                users_data.append((coord_name, 'puesto123', 'Coordinador de Puesto'))
                print(f"✅ Creado: {coord_name} (Coordinador Puesto en {puesto.puesto_nombre})")
        
        # 4. TESTIGOS para puestos de Florencia
        for idx, puesto in enumerate(puestos_florencia, 1):
            testigo_name = f'testigo_flo_{idx:02d}'
            testigo_existing = User.query.filter_by(nombre=testigo_name).first()
            
            if not testigo_existing:
                testigo = User(
                    nombre=testigo_name,
                    rol='testigo_electoral',
                    ubicacion_id=puesto.id,
                    activo=True,
                    es_usuario_basico=False
                )
                testigo.set_password('testigo123')
                db.session.add(testigo)
                users_data.append((testigo_name, 'testigo123', 'Testigo Electoral'))
                print(f"✅ Creado: {testigo_name} (Testigo en {puesto.puesto_nombre})")
        
        # Guardar
        try:
            db.session.commit()
            print(f"\n{'='*80}")
            print(f"✅ {len(users_data)} usuarios creados exitosamente")
            print(f"{'='*80}\n")
            
            print("USUARIOS CREADOS:")
            print("-" * 80)
            for nombre, password, rol in users_data:
                print(f"  • {nombre:30} | {password:15} | {rol}")
            print("-" * 80)
            
            return True
        except Exception as e:
            print(f"\n❌ Error al guardar: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    try:
        success = create_sample_users()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
