"""
Script para crear usuarios de prueba para Florencia, Caquetá
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from werkzeug.security import generate_password_hash


def crear_usuarios_florencia():
    """Crear usuarios de prueba para Florencia"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("CREANDO USUARIOS DE PRUEBA PARA FLORENCIA, CAQUETÁ")
        print("=" * 60)
        
        # Buscar Florencia (municipio)
        florencia = Location.query.filter_by(
            tipo='municipio',
            municipio_nombre='FLORENCIA'
        ).first()
        
        if not florencia:
            print("❌ No se encontró el municipio de Florencia")
            return
        
        print(f"\n✓ Municipio encontrado: {florencia.nombre_completo}")
        print(f"  Código: {florencia.municipio_codigo}")
        
        # Buscar departamento de Caquetá
        caqueta = Location.query.filter_by(
            tipo='departamento',
            departamento_nombre='CAQUETA'
        ).first()
        
        if not caqueta:
            print("❌ No se encontró el departamento de Caquetá")
            return
        
        print(f"✓ Departamento encontrado: {caqueta.nombre_completo}")
        
        usuarios_crear = []
        
        # 1. Coordinador Municipal de Florencia
        coord_municipal = User.query.filter_by(nombre='coord_municipal_florencia').first()
        if not coord_municipal:
            coord_municipal = User(
                nombre='coord_municipal_florencia',
                password_hash=generate_password_hash('password123'),
                rol='coordinador_municipal',
                ubicacion_id=florencia.id,
                activo=True
            )
            usuarios_crear.append(('Coordinador Municipal', coord_municipal, 'coord_municipal_florencia'))
        else:
            print(f"\n⚠️  Coordinador Municipal ya existe: {coord_municipal.nombre}")
        
        # 2. Coordinador Departamental de Caquetá
        coord_departamental = User.query.filter_by(nombre='coord_departamental_caqueta').first()
        if not coord_departamental:
            coord_departamental = User(
                nombre='coord_departamental_caqueta',
                password_hash=generate_password_hash('password123'),
                rol='coordinador_departamental',
                ubicacion_id=caqueta.id,
                activo=True
            )
            usuarios_crear.append(('Coordinador Departamental', coord_departamental, 'coord_departamental_caqueta'))
        else:
            print(f"⚠️  Coordinador Departamental ya existe: {coord_departamental.nombre}")
        
        # 3. Auditor Electoral de Caquetá
        auditor = User.query.filter_by(nombre='auditor_caqueta').first()
        if not auditor:
            auditor = User(
                nombre='auditor_caqueta',
                password_hash=generate_password_hash('password123'),
                rol='auditor_electoral',
                ubicacion_id=caqueta.id,
                activo=True
            )
            usuarios_crear.append(('Auditor Electoral', auditor, 'auditor_caqueta'))
        else:
            print(f"⚠️  Auditor Electoral ya existe: {auditor.nombre}")
        
        # 4. Super Admin (sin ubicación específica)
        super_admin = User.query.filter_by(nombre='superadmin').first()
        if not super_admin:
            super_admin = User(
                nombre='superadmin',
                password_hash=generate_password_hash('password123'),
                rol='super_admin',
                ubicacion_id=None,  # Super admin no tiene ubicación específica
                activo=True
            )
            usuarios_crear.append(('Super Admin', super_admin, 'superadmin'))
        else:
            print(f"⚠️  Super Admin ya existe: {super_admin.nombre}")
        
        # Guardar usuarios
        if usuarios_crear:
            print(f"\n📝 Creando {len(usuarios_crear)} usuario(s) nuevo(s)...")
            for rol, usuario, username in usuarios_crear:
                db.session.add(usuario)
            
            db.session.commit()
            print("✓ Usuarios creados exitosamente")
        else:
            print("\n✓ Todos los usuarios ya existen")
        
        # Mostrar resumen
        print("\n" + "=" * 60)
        print("RESUMEN DE USUARIOS DE PRUEBA")
        print("=" * 60)
        
        usuarios_resumen = [
            ('Coordinador Municipal', 'coord_municipal_florencia', 'coordinador_municipal', florencia.nombre_completo),
            ('Coordinador Departamental', 'coord_departamental_caqueta', 'coordinador_departamental', caqueta.nombre_completo),
            ('Auditor Electoral', 'auditor_caqueta', 'auditor_electoral', caqueta.nombre_completo),
            ('Super Admin', 'superadmin', 'super_admin', 'Nacional (sin ubicación)'),
        ]
        
        print("\n{:<30} {:<35} {:<25} {}".format("ROL", "USERNAME", "ROL SISTEMA", "UBICACIÓN"))
        print("-" * 120)
        
        for rol, username, rol_sistema, ubicacion in usuarios_resumen:
            usuario = User.query.filter_by(nombre=username).first()
            if usuario:
                print("{:<30} {:<35} {:<25} {}".format(
                    rol, 
                    username, 
                    rol_sistema,
                    ubicacion
                ))
        
        print("\n" + "=" * 60)
        print("CREDENCIALES DE ACCESO")
        print("=" * 60)
        print("Contraseña para todos: password123")
        print("\nURLs de acceso:")
        print("  - Coordinador Municipal:     http://localhost:5000/coordinador/municipal")
        print("  - Coordinador Departamental:  http://localhost:5000/coordinador/departamental")
        print("  - Auditor Electoral:          http://localhost:5000/auditor/dashboard")
        print("  - Super Admin:                http://localhost:5000/admin/dashboard")
        print("\n" + "=" * 60)


if __name__ == '__main__':
    crear_usuarios_florencia()
