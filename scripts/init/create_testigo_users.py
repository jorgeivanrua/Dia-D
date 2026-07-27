"""
Script para crear usuarios testigo electoral para cada puesto de votación
"""
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

def create_testigo_users():
    """
    Crear un usuario testigo para cada puesto de votación
    """
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("\n" + "=" * 80)
        print("CREACIÓN DE USUARIOS TESTIGO ELECTORAL")
        print("=" * 80 + "\n")
        
        # Obtener todos los puestos de votación
        puestos = Location.query.filter_by(tipo='puesto').all()
        print(f"Total de puestos encontrados: {len(puestos)}\n")
        
        testigos_creados = 0
        testigos_ya_existen = 0
        
        for puesto in puestos:
            # Obtener municipio y zona para nombre descriptivo
            municipio = puesto.municipio_nombre or 'SIN_MUNICIPIO'
            zona = puesto.zona_codigo[-2:] if puesto.zona_codigo else '00'
            puesto_codigo = puesto.puesto_codigo[-4:] if puesto.puesto_codigo else '0000'
            
            # Crear nombre de usuario para testigo
            nombre_testigo = f"testigo_{municipio[:3].upper()}_{puesto_codigo}"
            nombre_completo = f"Testigo {puesto.puesto_nombre or 'Desconocido'}"
            
            # Verificar si ya existe
            existing = User.query.filter_by(nombre=nombre_testigo).first()
            if existing:
                testigos_ya_existen += 1
                continue
            
            try:
                # Crear usuario testigo
                testigo = User(
                    nombre=nombre_testigo,
                    rol='testigo_electoral',
                    ubicacion_id=puesto.id,
                    activo=True,
                    es_usuario_basico=False
                )
                # Establecer contraseña
                testigo.set_password('testigo123')
                
                db.session.add(testigo)
                testigos_creados += 1
                
                print(f"✅ Creado: {nombre_testigo} -> Puesto: {puesto.puesto_nombre}")
            except Exception as e:
                print(f"❌ Error creando testigo para {puesto.puesto_nombre}: {e}")
                db.session.rollback()
                continue
        
        # Guardar cambios
        try:
            db.session.commit()
            print(f"\n" + "=" * 80)
            print(f"✅ USUARIOS CREADOS: {testigos_creados}")
            print(f"✓ Usuarios que ya existían: {testigos_ya_existen}")
            print("=" * 80 + "\n")
        except Exception as e:
            print(f"\n❌ Error al guardar: {e}")
            db.session.rollback()
            return False
        
        return True

if __name__ == '__main__':
    try:
        success = create_testigo_users()
        if success:
            print("✅ Creación de usuarios testigo completada correctamente")
            sys.exit(0)
        else:
            print("❌ Error durante la creación de usuarios testigo")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
