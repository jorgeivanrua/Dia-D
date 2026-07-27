"""
Script para limpiar usuarios de prueba y mantener solo usuarios básicos del sistema
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User

def limpiar_usuarios_prueba():
    """
    Eliminar todos los usuarios que NO son usuarios básicos del sistema
    Mantiene solo:
    - Super Admin
    - Monitoreo
    - Coordinador Departamental
    - Coordinador Municipal
    - Coordinador Puesto
    - Auditor Electoral
    - Testigos marcados como usuarios básicos
    """
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("=" * 80)
        print("LIMPIEZA DE USUARIOS DE PRUEBA".center(80))
        print("=" * 80)
        print()
        
        # Contar usuarios antes
        total_antes = User.query.count()
        usuarios_basicos = User.query.filter_by(es_usuario_basico=True).count()
        usuarios_prueba = total_antes - usuarios_basicos
        
        print(f"📊 Estado actual:")
        print(f"   Total de usuarios: {total_antes}")
        print(f"   Usuarios básicos del sistema: {usuarios_basicos}")
        print(f"   Usuarios de prueba: {usuarios_prueba}")
        print()
        
        if usuarios_prueba == 0:
            print("✅ No hay usuarios de prueba para eliminar")
            return
        
        # Confirmar acción
        print("⚠️  ADVERTENCIA: Se eliminarán todos los usuarios que NO sean usuarios básicos")
        print()
        respuesta = input("¿Desea continuar? (si/no): ").strip().lower()
        
        if respuesta not in ['si', 's', 'yes', 'y']:
            print("❌ Operación cancelada")
            return
        
        print()
        print("🗑️  Eliminando usuarios de prueba...")
        
        # Eliminar usuarios que NO son básicos
        usuarios_eliminados = User.query.filter_by(es_usuario_basico=False).delete()
        db.session.commit()
        
        print(f"✅ {usuarios_eliminados} usuarios de prueba eliminados")
        print()
        
        # Mostrar usuarios restantes
        print("👥 Usuarios básicos del sistema:")
        print("-" * 80)
        usuarios_restantes = User.query.filter_by(es_usuario_basico=True).order_by(User.rol, User.nombre).all()
        
        for usuario in usuarios_restantes:
            ubicacion = ""
            if usuario.ubicacion_id:
                ubicacion = f" (Ubicación ID: {usuario.ubicacion_id})"
            print(f"   • {usuario.nombre:30} | {usuario.rol:30} | {'Activo' if usuario.activo else 'Inactivo'}{ubicacion}")
        
        print("-" * 80)
        print(f"Total: {len(usuarios_restantes)} usuarios básicos")
        print()
        print("=" * 80)
        print("✅ LIMPIEZA COMPLETADA".center(80))
        print("=" * 80)

if __name__ == '__main__':
    try:
        limpiar_usuarios_prueba()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
