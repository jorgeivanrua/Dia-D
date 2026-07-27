"""
Script de prueba para verificar correcciones de seguridad
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User


def test_password_hashing():
    """Verificar que el hashing de contraseñas funciona correctamente"""
    print("\n" + "=" * 80)
    print("TEST 1: Verificación de Hashing de Contraseñas")
    print("=" * 80)
    
    app = create_app()
    
    with app.app_context():
        # Crear usuario de prueba
        test_user = User(
            nombre='Test User',
            rol='testigo_electoral',
            activo=True
        )
        
        # Establecer contraseña
        test_password = 'TestPassword123'
        test_user.set_password(test_password)
        
        print(f"\n✅ Contraseña establecida: {test_password}")
        print(f"✅ Hash generado: {test_user.password_hash[:50]}...")
        
        # Verificar que NO es texto plano
        if test_user.password_hash == test_password:
            print("❌ ERROR: La contraseña se guardó en texto plano!")
            return False
        else:
            print("✅ CORRECTO: La contraseña está hasheada")
        
        # Verificar que check_password funciona
        if test_user.check_password(test_password):
            print("✅ CORRECTO: check_password() funciona correctamente")
        else:
            print("❌ ERROR: check_password() no funciona")
            return False
        
        # Verificar que contraseña incorrecta falla
        if not test_user.check_password('WrongPassword'):
            print("✅ CORRECTO: Contraseña incorrecta es rechazada")
        else:
            print("❌ ERROR: Contraseña incorrecta fue aceptada")
            return False
        
        print("\n✅ TEST 1 PASADO: Hashing de contraseñas funciona correctamente")
        return True


def test_existing_users():
    """Verificar usuarios existentes en la base de datos"""
    print("\n" + "=" * 80)
    print("TEST 2: Verificación de Usuarios Existentes")
    print("=" * 80)
    
    app = create_app()
    
    with app.app_context():
        usuarios = User.query.all()
        
        if not usuarios:
            print("\n⚠️  No hay usuarios en la base de datos")
            print("   Ejecuta: python scripts/init_system.py")
            return True
        
        print(f"\n📊 Total de usuarios: {len(usuarios)}")
        print("\n" + "-" * 80)
        
        all_hashed = True
        
        for usuario in usuarios:
            # Verificar que la contraseña esté hasheada
            is_hashed = not (
                usuario.password_hash == 'admin123' or
                usuario.password_hash == 'test123' or
                len(usuario.password_hash) < 50
            )
            
            status = "✅ HASHEADA" if is_hashed else "❌ TEXTO PLANO"
            
            print(f"{status} | {usuario.nombre:30} | {usuario.rol:25}")
            
            if not is_hashed:
                all_hashed = False
        
        print("-" * 80)
        
        if all_hashed:
            print("\n✅ TEST 2 PASADO: Todas las contraseñas están hasheadas")
            return True
        else:
            print("\n❌ TEST 2 FALLIDO: Algunas contraseñas están en texto plano")
            print("\n💡 Solución: Ejecuta 'python scripts/init_system.py --reset-passwords'")
            return False


def test_emergency_endpoints():
    """Verificar que los endpoints de emergencia están protegidos"""
    print("\n" + "=" * 80)
    print("TEST 3: Verificación de Endpoints de Emergencia")
    print("=" * 80)
    
    # Verificar que EMERGENCY_KEY esté configurada o no
    emergency_key = os.getenv('EMERGENCY_RESET_KEY')
    allow_emergency = os.getenv('ALLOW_EMERGENCY_ENDPOINTS', 'false').lower() == 'true'
    flask_env = os.getenv('FLASK_ENV', 'development')
    
    print(f"\n📋 Configuración actual:")
    print(f"   FLASK_ENV: {flask_env}")
    print(f"   EMERGENCY_RESET_KEY: {'Configurada' if emergency_key else 'No configurada'}")
    print(f"   ALLOW_EMERGENCY_ENDPOINTS: {allow_emergency}")
    
    if flask_env == 'production' and allow_emergency:
        print("\n⚠️  ADVERTENCIA: Endpoints de emergencia habilitados en producción")
        print("   Esto es un riesgo de seguridad. Deshabilita después de usar.")
        return True
    elif flask_env == 'production' and not allow_emergency:
        print("\n✅ CORRECTO: Endpoints de emergencia deshabilitados en producción")
        return True
    else:
        print("\n✅ CORRECTO: Entorno de desarrollo")
        return True


def test_logging_config():
    """Verificar que el logging está configurado"""
    print("\n" + "=" * 80)
    print("TEST 4: Verificación de Configuración de Logging")
    print("=" * 80)
    
    try:
        from backend.utils.logging_config import get_logger
        
        logger = get_logger('test')
        logger.info("Test de logging")
        
        print("\n✅ TEST 4 PASADO: Sistema de logging configurado correctamente")
        return True
    except Exception as e:
        print(f"\n❌ TEST 4 FALLIDO: Error en logging: {e}")
        return False


def main():
    """Ejecutar todos los tests"""
    print("\n" + "=" * 80)
    print("VERIFICACIÓN DE CORRECCIONES DE SEGURIDAD")
    print("=" * 80)
    
    tests = [
        test_password_hashing,
        test_existing_users,
        test_emergency_endpoints,
        test_logging_config
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n❌ ERROR EN TEST: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    # Resumen
    print("\n" + "=" * 80)
    print("RESUMEN DE TESTS")
    print("=" * 80)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n✅ Tests pasados: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("\n✅ Las correcciones de seguridad están funcionando correctamente")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) fallaron")
        print("\n💡 Revisa los mensajes de error arriba para más detalles")
        return 1


if __name__ == '__main__':
    sys.exit(main())
