"""
Script universal para corregir roles de usuarios
Funciona con SQLite (local) y PostgreSQL (Render)
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app
from backend.database import db
from backend.models.user import User

def corregir_roles():
    """Corregir roles de usuarios usando SQLAlchemy (funciona con SQLite y PostgreSQL)"""
    
    # Detectar entorno
    env = os.getenv('FLASK_ENV', 'development')
    database_url = os.getenv('DATABASE_URL', 'sqlite:///instance/electoral.db')
    
    print("=" * 80)
    print("CORRECCIÓN DE ROLES DE USUARIOS")
    print("=" * 80)
    print(f"Entorno: {env}")
    print(f"Base de datos: {database_url[:50]}...")
    print()
    
    # Crear app
    app = create_app(env)
    
    with app.app_context():
        # 1. Verificar estado actual
        print("1. ESTADO ACTUAL")
        print("-" * 80)
        
        usuarios_prueba = ['admin', 'testigo', 'coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental']
        
        for nombre in usuarios_prueba:
            user = User.query.filter_by(nombre=nombre).first()
            if user:
                print(f"Usuario: {nombre}")
                print(f"  ID: {user.id}")
                print(f"  Rol actual: {user.rol}")
                print(f"  Activo: {user.activo}")
                print(f"  Contraseña: {user.password_hash}")
                print(f"  Ubicación ID: {user.ubicacion_id}")
                print()
            else:
                print(f"⚠️ Usuario '{nombre}' no encontrado")
                print()
        
        # 2. Aplicar correcciones
        print("2. APLICANDO CORRECCIONES")
        print("-" * 80)
        
        correcciones = [
            ('admin', 'super_admin', 'admin123', None),
            ('testigo', 'testigo_electoral', 'test123', None),
            ('coordinador_puesto', 'coordinador_puesto', 'test123', None),
            ('coordinador_municipal', 'coordinador_municipal', 'test123', None),
            ('coordinador_departamental', 'coordinador_departamental', 'test123', None)
        ]
        
        cambios_totales = 0
        
        for nombre, rol_correcto, password_correcta, ubicacion_id in correcciones:
            user = User.query.filter_by(nombre=nombre).first()
            
            if user:
                cambios = []
                
                # Verificar si necesita corrección de rol
                if user.rol != rol_correcto:
                    user.rol = rol_correcto
                    cambios.append(f"rol: {user.rol} → {rol_correcto}")
                
                # Verificar si necesita corrección de contraseña
                if user.password_hash != password_correcta:
                    user.set_password(password_correcta)
                    cambios.append(f"contraseña: actualizada a {password_correcta}")
                
                # Activar usuario si está inactivo
                if not user.activo:
                    user.activo = True
                    cambios.append("activado")
                
                # Resetear intentos fallidos y bloqueos
                if user.intentos_fallidos > 0:
                    user.intentos_fallidos = 0
                    cambios.append("intentos fallidos reseteados")
                
                if user.bloqueado_hasta:
                    user.bloqueado_hasta = None
                    cambios.append("desbloqueo de cuenta")
                
                if cambios:
                    print(f"✅ Usuario '{nombre}' corregido:")
                    for cambio in cambios:
                        print(f"   - {cambio}")
                    cambios_totales += len(cambios)
                else:
                    print(f"✓ Usuario '{nombre}' ya está correcto")
            else:
                print(f"⚠️ Usuario '{nombre}' no encontrado")
            
            print()
        
        # 3. Commit de cambios
        if cambios_totales > 0:
            try:
                db.session.commit()
                print(f"✅ {cambios_totales} cambios guardados en la base de datos")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error al guardar cambios: {e}")
                return
        else:
            print("✓ No hay cambios que guardar")
        
        print()
        
        # 4. Verificar estado final
        print("3. ESTADO FINAL")
        print("-" * 80)
        
        for nombre in usuarios_prueba:
            user = User.query.filter_by(nombre=nombre).first()
            if user:
                print(f"Usuario: {nombre}")
                print(f"  Rol: {user.rol}")
                print(f"  Activo: {user.activo}")
                print(f"  Contraseña: {user.password_hash}")
                print(f"  Bloqueado: {'Sí' if user.bloqueado_hasta else 'No'}")
                print()
        
        # 5. Estadísticas generales
        print("4. ESTADÍSTICAS GENERALES")
        print("-" * 80)
        
        total_usuarios = User.query.count()
        usuarios_activos = User.query.filter_by(activo=True).count()
        usuarios_bloqueados = User.query.filter(User.bloqueado_hasta.isnot(None)).count()
        
        print(f"Total de usuarios: {total_usuarios}")
        print(f"Usuarios activos: {usuarios_activos}")
        print(f"Usuarios bloqueados: {usuarios_bloqueados}")
        print()
        
        # Usuarios por rol
        from sqlalchemy import func
        roles_count = db.session.query(
            User.rol, 
            func.count(User.id)
        ).group_by(User.rol).all()
        
        print("Usuarios por rol:")
        for rol, count in roles_count:
            print(f"  - {rol}: {count}")
        print()
        
        # 6. Resumen
        print("=" * 80)
        print("RESUMEN")
        print("=" * 80)
        print()
        print("✅ Correcciones aplicadas exitosamente")
        print()
        print("IMPORTANTE:")
        print("  1. Todos los usuarios deben cerrar sesión")
        print("  2. Volver a iniciar sesión para obtener nuevos tokens JWT")
        print("  3. Los tokens antiguos tendrán roles incorrectos")
        print()
        print("CREDENCIALES DE PRUEBA:")
        print("  - admin / admin123 (Super Admin)")
        print("  - testigo / test123 (Testigo Electoral)")
        print("  - coordinador_puesto / test123 (Coordinador de Puesto)")
        print("  - coordinador_municipal / test123 (Coordinador Municipal)")
        print("  - coordinador_departamental / test123 (Coordinador Departamental)")
        print()

if __name__ == '__main__':
    try:
        corregir_roles()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
