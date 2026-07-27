"""
Script para crear usuarios de prueba
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location


def create_sample_users():
    """Crear usuarios de prueba para el sistema"""
    app = create_app('development')
    
    with app.app_context():
        print("\n>> Creando usuarios de prueba...")
        
        # Obtener ubicaciones de Caquetá
        caqueta = Location.query.filter_by(tipo='departamento', departamento_codigo='44').first()
        florencia = Location.query.filter_by(tipo='municipio', municipio_codigo='01').first()
        
        # Obtener primer puesto y mesa de Florencia
        puesto_florencia = Location.query.filter_by(
            tipo='puesto',
            municipio_codigo='01'
        ).first()
        
        mesa_florencia = Location.query.filter_by(
            tipo='mesa',
            municipio_codigo='01'
        ).first()
        
        usuarios_creados = 0
        
        # 1. Super Admin
        try:
            if not User.query.filter_by(rol='super_admin').first():
                admin = User(
                    nombre='Administrador Sistema',
                    rol='super_admin',
                    ubicacion_id=None,
                    activo=True
                )
                admin.set_password('Admin123!')
                db.session.add(admin)
                db.session.commit()
                usuarios_creados += 1
                print(f"  + Super Admin creado")
                print(f"    Login: super_admin / Admin123!")
        except Exception as e:
            print(f"  ! Error creando Super Admin: {e}")
            db.session.rollback()
        
        # 2. Admin Departamental (Caquetá)
        if not User.query.filter_by(rol='admin_departamental').first():
            admin_dept = User(
                nombre='Admin Departamental Caqueta',
                rol='admin_departamental',
                ubicacion_id=caqueta.id if caqueta else None,
                activo=True
            )
            admin_dept.set_password('AdminDept123!')
            db.session.add(admin_dept)
            usuarios_creados += 1
            print(f"  + Admin Departamental creado (Caqueta)")
            print(f"    Login: admin_departamental + Caqueta / AdminDept123!")
        
        # 3. Admin Municipal (Florencia)
        if not User.query.filter_by(rol='admin_municipal').first():
            admin_muni = User(
                nombre='Admin Municipal Florencia',
                rol='admin_municipal',
                ubicacion_id=florencia.id if florencia else None,
                activo=True
            )
            admin_muni.set_password('AdminMuni123!')
            db.session.add(admin_muni)
            usuarios_creados += 1
            print(f"  + Admin Municipal creado (Florencia)")
            print(f"    Login: admin_municipal + Florencia / AdminMuni123!")
        
        # 4. Coordinador Departamental
        if not User.query.filter_by(rol='coordinador_departamental').first():
            coord_dept = User(
                nombre='Coordinador Departamental Caqueta',
                rol='coordinador_departamental',
                ubicacion_id=caqueta.id if caqueta else None,
                activo=True
            )
            coord_dept.set_password('CoordDept123!')
            db.session.add(coord_dept)
            usuarios_creados += 1
            print(f"  + Coordinador Departamental creado (Caqueta)")
            print(f"    Login: coordinador_departamental + Caqueta / CoordDept123!")
        
        # 5. Coordinador Municipal
        if not User.query.filter_by(rol='coordinador_municipal').first():
            coord_muni = User(
                nombre='Coordinador Municipal Florencia',
                rol='coordinador_municipal',
                ubicacion_id=florencia.id if florencia else None,
                activo=True
            )
            coord_muni.set_password('CoordMuni123!')
            db.session.add(coord_muni)
            usuarios_creados += 1
            print(f"  + Coordinador Municipal creado (Florencia)")
            print(f"    Login: coordinador_municipal + Florencia / CoordMuni123!")
        
        # 6. Coordinador de Puesto
        if puesto_florencia and not User.query.filter_by(rol='coordinador_puesto').first():
            coord_puesto = User(
                nombre=f'Coordinador {puesto_florencia.puesto_nombre}',
                rol='coordinador_puesto',
                ubicacion_id=puesto_florencia.id,
                activo=True
            )
            coord_puesto.set_password('CoordPuesto123!')
            db.session.add(coord_puesto)
            usuarios_creados += 1
            print(f"  + Coordinador de Puesto creado ({puesto_florencia.puesto_nombre})")
            print(f"    Login: coordinador_puesto + ubicacion / CoordPuesto123!")
        
        # 7. Testigo Electoral
        if mesa_florencia and not User.query.filter_by(rol='testigo_electoral').first():
            testigo = User(
                nombre='Testigo Electoral Mesa 1',
                rol='testigo_electoral',
                ubicacion_id=puesto_florencia.id if puesto_florencia else None,
                activo=True
            )
            testigo.set_password('Testigo123!')
            db.session.add(testigo)
            usuarios_creados += 1
            print(f"  + Testigo Electoral creado")
            print(f"    Login: testigo_electoral + ubicacion / Testigo123!")
        
        # 8. Auditor Electoral
        if not User.query.filter_by(rol='auditor_electoral').first():
            auditor = User(
                nombre='Auditor Electoral Caqueta',
                rol='auditor_electoral',
                ubicacion_id=caqueta.id if caqueta else None,
                activo=True
            )
            auditor.set_password('Auditor123!')
            db.session.add(auditor)
            usuarios_creados += 1
            print(f"  + Auditor Electoral creado (Caqueta)")
            print(f"    Login: auditor_electoral + Caqueta / Auditor123!")
        
        # Commit
        db.session.commit()
        
        print(f"\n>> Usuarios creados: {usuarios_creados}")
        print(f">> Total usuarios en sistema: {User.query.count()}")
        
        print("\n>> CREDENCIALES DE ACCESO:")
        print("=" * 60)
        print("NOTA: El login requiere ROL + UBICACION + PASSWORD")
        print("=" * 60)
        print("\n1. Super Admin:")
        print("   Rol: super_admin")
        print("   Password: Admin123!")
        print("   (No requiere ubicacion)")
        
        print("\n2. Admin Departamental:")
        print("   Rol: admin_departamental")
        print("   Departamento: Caqueta")
        print("   Password: AdminDept123!")
        
        print("\n3. Admin Municipal:")
        print("   Rol: admin_municipal")
        print("   Departamento: Caqueta")
        print("   Municipio: Florencia")
        print("   Password: AdminMuni123!")
        
        print("\n4. Coordinador Departamental:")
        print("   Rol: coordinador_departamental")
        print("   Departamento: Caqueta")
        print("   Password: CoordDept123!")
        
        print("\n5. Coordinador Municipal:")
        print("   Rol: coordinador_municipal")
        print("   Departamento: Caqueta")
        print("   Municipio: Florencia")
        print("   Password: CoordMuni123!")
        
        print("\n6. Coordinador de Puesto:")
        print("   Rol: coordinador_puesto")
        print("   Departamento: Caqueta")
        print("   Municipio: Florencia")
        print("   Zona + Puesto: (seleccionar del sistema)")
        print("   Password: CoordPuesto123!")
        
        print("\n7. Testigo Electoral:")
        print("   Rol: testigo_electoral")
        print("   Departamento: Caqueta")
        print("   Municipio: Florencia")
        print("   Zona + Puesto: (seleccionar del sistema)")
        print("   Password: Testigo123!")
        
        print("\n8. Auditor Electoral:")
        print("   Rol: auditor_electoral")
        print("   Departamento: Caqueta")
        print("   Password: Auditor123!")
        
        print("\n" + "=" * 60)


if __name__ == '__main__':
    create_sample_users()
