"""
Script COMPLETO para arreglar usuarios y contraseñas
Crea/actualiza usuarios básicos + testigos
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location


def fix_usuarios_completo():
    """Arreglar todos los usuarios del sistema"""
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("\n" + "=" * 80)
        print("FIX COMPLETO DE USUARIOS Y CONTRASEÑAS")
        print("=" * 80)
        print()
        
        # ========================================
        # PASO 1: USUARIOS BÁSICOS FIJOS (sin ubicación)
        # ========================================
        print("PASO 1: USUARIOS BÁSICOS FIJOS")
        print("-" * 80)
        
        usuarios_basicos = [
            {
                'nombre': 'Super Admin',
                'rol': 'super_admin',
                'password': 'admin123',
                'ubicacion_id': None
            },
            {
                'nombre': 'Monitoreo',
                'rol': 'monitoreo',
                'password': 'test123',
                'ubicacion_id': None
            },
            {
                'nombre': 'Coordinador Departamental',
                'rol': 'coordinador_departamental',
                'password': 'test123',
                'ubicacion_id': None
            },
            {
                'nombre': 'Coordinador Municipal',
                'rol': 'coordinador_municipal',
                'password': 'test123',
                'ubicacion_id': None
            },
            {
                'nombre': 'Coordinador Puesto',
                'rol': 'coordinador_puesto',
                'password': 'test123',
                'ubicacion_id': None
            },
            {
                'nombre': 'Auditor Electoral',
                'rol': 'auditor_electoral',
                'password': 'test123',
                'ubicacion_id': None
            }
        ]
        
        for usuario_data in usuarios_basicos:
            # Buscar usuario por rol y ubicacion_id=None
            usuario = User.query.filter_by(
                rol=usuario_data['rol'],
                ubicacion_id=None
            ).first()
            
            if usuario:
                print(f"[UPDATE] {usuario_data['nombre']} ({usuario_data['rol']})")
                usuario.nombre = usuario_data['nombre']
                usuario.password_hash = usuario_data['password']  # Texto plano
                usuario.activo = True
                usuario.intentos_fallidos = 0
                usuario.bloqueado_hasta = None
                usuario.es_usuario_basico = True
            else:
                print(f"[CREATE] {usuario_data['nombre']} ({usuario_data['rol']})")
                usuario = User(
                    nombre=usuario_data['nombre'],
                    password_hash=usuario_data['password'],  # Texto plano
                    rol=usuario_data['rol'],
                    ubicacion_id=None,
                    activo=True,
                    es_usuario_basico=True
                )
                db.session.add(usuario)
            
            print(f"         ✅ Password: {usuario_data['password']}")
        
        db.session.commit()
        print()
        
        # ========================================
        # PASO 2: USUARIOS CON UBICACIÓN
        # ========================================
        print("PASO 2: USUARIOS CON UBICACIÓN")
        print("-" * 80)
        
        # Obtener Caquetá
        caqueta = Location.query.filter_by(
            tipo='departamento',
            departamento_codigo='44'
        ).first()
        
        # Obtener Florencia
        florencia = Location.query.filter_by(
            tipo='municipio',
            municipio_codigo='4401'
        ).first()
        
        if not caqueta or not florencia:
            print("⚠️  No se encontraron ubicaciones (Caquetá/Florencia)")
            print("   Saltando usuarios con ubicación...")
        else:
            # Admin Departamental
            admin_dept = User.query.filter_by(
                rol='admin_departamental',
                ubicacion_id=caqueta.id
            ).first()
            
            if not admin_dept:
                print("[CREATE] Admin Departamental Caquetá")
                admin_dept = User(
                    nombre='admin_caqueta',
                    password_hash='test123',  # Texto plano
                    rol='admin_departamental',
                    ubicacion_id=caqueta.id,
                    activo=True
                )
                db.session.add(admin_dept)
            else:
                print("[UPDATE] Admin Departamental Caquetá")
                admin_dept.password_hash = 'test123'  # Texto plano
                admin_dept.activo = True
                admin_dept.intentos_fallidos = 0
                admin_dept.bloqueado_hasta = None
            
            # Admin Municipal
            admin_mun = User.query.filter_by(
                rol='admin_municipal',
                ubicacion_id=florencia.id
            ).first()
            
            if not admin_mun:
                print("[CREATE] Admin Municipal Florencia")
                admin_mun = User(
                    nombre='admin_florencia',
                    password_hash='test123',  # Texto plano
                    rol='admin_municipal',
                    ubicacion_id=florencia.id,
                    activo=True
                )
                db.session.add(admin_mun)
            else:
                print("[UPDATE] Admin Municipal Florencia")
                admin_mun.password_hash = 'test123'  # Texto plano
                admin_mun.activo = True
                admin_mun.intentos_fallidos = 0
                admin_mun.bloqueado_hasta = None
            
            db.session.commit()
        
        print()
        
        # ========================================
        # PASO 3: TESTIGOS
        # ========================================
        print("PASO 3: TESTIGOS ELECTORALES")
        print("-" * 80)
        
        # Obtener primeros 5 puestos de Florencia
        puestos = Location.query.filter_by(
            tipo='puesto',
            municipio_codigo='4401'
        ).limit(5).all()
        
        if not puestos:
            print("⚠️  No se encontraron puestos en Florencia")
            print("   Saltando creación de testigos...")
        else:
            testigos_creados = 0
            
            for puesto in puestos:
                # Crear 2 testigos por puesto
                for i in range(1, 3):
                    nombre_testigo = f'testigo_{puesto.puesto_codigo}_{i}'
                    
                    testigo = User.query.filter_by(
                        nombre=nombre_testigo,
                        rol='testigo_electoral'
                    ).first()
                    
                    if not testigo:
                        print(f"[CREATE] Testigo {i} - {puesto.puesto_nombre}")
                        testigo = User(
                            nombre=nombre_testigo,
                            password_hash='test123',  # Texto plano
                            rol='testigo_electoral',
                            ubicacion_id=puesto.id,
                            activo=True
                        )
                        db.session.add(testigo)
                        testigos_creados += 1
                    else:
                        print(f"[UPDATE] Testigo {i} - {puesto.puesto_nombre}")
                        testigo.password_hash = 'test123'  # Texto plano
                        testigo.activo = True
                        testigo.intentos_fallidos = 0
                        testigo.bloqueado_hasta = None
            
            db.session.commit()
            print(f"\n✅ {testigos_creados} testigos procesados")
        
        print()
        
        # ========================================
        # RESUMEN FINAL
        # ========================================
        print("=" * 80)
        print("RESUMEN FINAL")
        print("=" * 80)
        print()
        
        # Contar usuarios por rol
        from sqlalchemy import func
        roles_count = db.session.query(
            User.rol,
            func.count(User.id)
        ).group_by(User.rol).all()
        
        print("Usuarios por rol:")
        for rol, count in roles_count:
            print(f"  - {rol}: {count}")
        
        print()
        print("=" * 80)
        print("CREDENCIALES")
        print("=" * 80)
        print()
        print("🔐 SUPER ADMIN:")
        print("   Rol: super_admin")
        print("   Password: admin123")
        print()
        print("✅ TODOS LOS DEMÁS USUARIOS:")
        print("   Password: test123")
        print()
        print("📋 Usuarios básicos (sin ubicación):")
        print("   - Super Admin (super_admin)")
        print("   - Monitoreo (monitoreo)")
        print("   - Coordinador Departamental (coordinador_departamental)")
        print("   - Coordinador Municipal (coordinador_municipal)")
        print("   - Coordinador Puesto (coordinador_puesto)")
        print("   - Auditor Electoral (auditor_electoral)")
        print()
        print("👥 Usuarios con ubicación:")
        print("   - Admin Departamental (admin_departamental + Caquetá)")
        print("   - Admin Municipal (admin_municipal + Florencia)")
        print("   - Testigos (testigo_electoral + Puesto)")
        print()
        print("=" * 80)
        print("✅ FIX COMPLETO EXITOSO")
        print("=" * 80)
        print()
        
        return True


if __name__ == '__main__':
    try:
        success = fix_usuarios_completo()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
