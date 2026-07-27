"""
Script simple para verificar y crear usuario de monitoreo
Ejecutar desde la raíz del proyecto con: python verificar_monitoreo.py
"""
from backend.database import db
from backend.models.user import User
from backend.app import create_app


def main():
    print("="*60)
    print("VERIFICACIÓN Y CREACIÓN DE USUARIO DE MONITOREO")
    print("="*60)
    
    app = create_app()
    
    with app.app_context():
        # Verificar si existe
        usuario = User.query.filter_by(rol='monitoreo').first()
        
        if usuario:
            print(f"\n✅ Usuario de monitoreo encontrado:")
            print(f"   ID: {usuario.id}")
            print(f"   Nombre: {usuario.nombre}")
            print(f"   Rol: {usuario.rol}")
            print(f"   Activo: {usuario.activo}")
            print(f"   Ubicación ID: {usuario.ubicacion_id}")
            
            # Asegurar que esté activo y sin ubicación
            cambios = False
            if not usuario.activo:
                usuario.activo = True
                cambios = True
                print("\n   ✓ Usuario activado")
            
            if usuario.ubicacion_id is not None:
                usuario.ubicacion_id = None
                cambios = True
                print("   ✓ ubicacion_id removida")
            
            if cambios:
                db.session.commit()
                print("\n✅ Usuario actualizado correctamente")
        else:
            print("\n📝 Creando usuario de monitoreo...")
            
            usuario = User(
                nombre='monitoreo',
                rol='monitoreo',
                ubicacion_id=None,
                activo=True
            )
            usuario.set_password('Monitoreo2025!')
            
            db.session.add(usuario)
            db.session.commit()
            
            print(f"\n✅ Usuario creado exitosamente:")
            print(f"   ID: {usuario.id}")
            print(f"   Nombre: monitoreo")
            print(f"   Contraseña: Monitoreo2025!")
            print(f"   Rol: monitoreo")
        
        print("\n" + "="*60)
        print("INFORMACIÓN DE LOGIN")
        print("="*60)
        print("\n📋 Credenciales:")
        print("   Usuario: monitoreo")
        print("   Contraseña: Monitoreo2025!")
        print("\n🌐 URL de Login:")
        print("   http://localhost:5000/login")
        print("\n📝 JSON para Login:")
        print('   {"rol": "monitoreo", "password": "Monitoreo2025!"}')
        print("\n🎯 Dashboard:")
        print("   http://localhost:5000/monitoreo/dashboard")
        print("\n" + "="*60)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

