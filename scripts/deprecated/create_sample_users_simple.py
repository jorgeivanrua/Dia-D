"""
Script simplificado para crear usuarios de prueba
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location


def create_user(nombre, rol, ubicacion_id, password):
    """Crear un usuario"""
    try:
        user = User(
            nombre=nombre,
            rol=rol,
            ubicacion_id=ubicacion_id,
            activo=True
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"  + {rol}: {nombre}")
        return True
    except Exception as e:
        print(f"  ! Error: {e}")
        db.session.rollback()
        return False


def main():
    app = create_app('development')
    
    with app.app_context():
        print("\n>> Creando usuarios de prueba...")
        
        # Obtener ubicaciones
        caqueta = Location.query.filter_by(tipo='departamento').first()
        florencia = Location.query.filter_by(tipo='municipio').first()
        puesto = Location.query.filter_by(tipo='puesto').first()
        
        usuarios = [
            ('Administrador Sistema', 'super_admin', None, 'Admin123!'),
            ('Admin Departamental', 'admin_departamental', caqueta.id if caqueta else None, 'AdminDept123!'),
            ('Admin Municipal', 'admin_municipal', florencia.id if florencia else None, 'AdminMuni123!'),
            ('Coordinador Departamental', 'coordinador_departamental', caqueta.id if caqueta else None, 'CoordDept123!'),
            ('Coordinador Municipal', 'coordinador_municipal', florencia.id if florencia else None, 'CoordMuni123!'),
            ('Coordinador de Puesto', 'coordinador_puesto', puesto.id if puesto else None, 'CoordPuesto123!'),
            ('Testigo Electoral', 'testigo_electoral', puesto.id if puesto else None, 'Testigo123!'),
            ('Auditor Electoral', 'auditor_electoral', caqueta.id if caqueta else None, 'Auditor123!'),
        ]
        
        creados = 0
        for nombre, rol, ubicacion_id, password in usuarios:
            if create_user(nombre, rol, ubicacion_id, password):
                creados += 1
        
        print(f"\n>> Total usuarios creados: {creados}")
        print(f">> Total en sistema: {User.query.count()}")
        
        print("\n>> CREDENCIALES:")
        print("=" * 60)
        for nombre, rol, _, password in usuarios:
            print(f"{rol}: {password}")
        print("=" * 60)


if __name__ == '__main__':
    main()
