"""
Script para diagnosticar y corregir problemas con usuarios de ubicación completa
"""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location
from backend.database import db

def diagnosticar_usuarios():
    """Diagnosticar problemas con usuarios"""
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("DIAGNÓSTICO DE USUARIOS CON UBICACIÓN")
        print("=" * 80)
        print()
        
        # 1. Verificar usuario de monitoreo
        print("1. VERIFICANDO USUARIO DE MONITOREO")
        print("-" * 80)
        
        monitoreo = User.query.filter_by(rol='monitoreo').first()
        if monitoreo:
            print(f"✅ Usuario monitoreo encontrado:")
            print(f"   ID: {monitoreo.id}")
            print(f"   Nombre: {monitoreo.nombre}")
            print(f"   Rol: {monitoreo.rol}")
            print(f"   Ubicación ID: {monitoreo.ubicacion_id}")
            print(f"   Activo: {monitoreo.activo}")
            print(f"   Bloqueado hasta: {monitoreo.bloqueado_hasta}")
            print(f"   Intentos fallidos: {monitoreo.intentos_fallidos}")
            
            # Verificar contraseña
            if monitoreo.check_password('test123'):
                print(f"   ✅ Contraseña 'test123' es correcta")
            else:
                print(f"   ❌ Contraseña 'test123' NO es correcta")
                print(f"   🔧 Corrigiendo contraseña...")
                monitoreo.set_password('test123')
                monitoreo.intentos_fallidos = 0
                monitoreo.bloqueado_hasta = None
                db.session.commit()
                print(f"   ✅ Contraseña corregida")
        else:
            print("❌ Usuario monitoreo NO encontrado")
            print("🔧 Creando usuario monitoreo...")
            monitoreo = User(
                nombre='MONITOREO',
                rol='monitoreo',
                ubicacion_id=None,
                activo=True,
                es_usuario_basico=False
            )
            monitoreo.set_password('test123')
            db.session.add(monitoreo)
            db.session.commit()
            print("✅ Usuario monitoreo creado")
        
        print()
        
        # 2. Verificar testigos electorales
        print("2. VERIFICANDO TESTIGOS ELECTORALES")
        print("-" * 80)
        
        testigos = User.query.filter_by(rol='testigo_electoral').all()
        print(f"Total testigos: {len(testigos)}")
        
        testigos_con_problema = []
        for testigo in testigos:
            # Verificar que tenga ubicación
            if not testigo.ubicacion_id:
                testigos_con_problema.append(testigo)
                print(f"❌ Testigo {testigo.nombre} (ID: {testigo.id}) sin ubicación")
                continue
            
            # Verificar que la ubicación exista
            ubicacion = Location.query.get(testigo.ubicacion_id)
            if not ubicacion:
                testigos_con_problema.append(testigo)
                print(f"❌ Testigo {testigo.nombre} (ID: {testigo.id}) con ubicación inválida")
                continue
            
            # Verificar que la ubicación sea de tipo puesto
            if ubicacion.tipo != 'puesto':
                testigos_con_problema.append(testigo)
                print(f"❌ Testigo {testigo.nombre} (ID: {testigo.id}) con ubicación tipo '{ubicacion.tipo}' (debe ser 'puesto')")
                continue
            
            # Verificar contraseña
            if not testigo.check_password('test123'):
                testigos_con_problema.append(testigo)
                print(f"❌ Testigo {testigo.nombre} (ID: {testigo.id}) con contraseña incorrecta")
        
        if testigos_con_problema:
            print(f"\n⚠️  {len(testigos_con_problema)} testigos con problemas")
        else:
            print(f"\n✅ Todos los testigos están correctos")
        
        print()
        
        # 3. Verificar coordinadores de puesto
        print("3. VERIFICANDO COORDINADORES DE PUESTO")
        print("-" * 80)
        
        coords_puesto = User.query.filter_by(rol='coordinador_puesto').all()
        print(f"Total coordinadores de puesto: {len(coords_puesto)}")
        
        coords_con_problema = []
        for coord in coords_puesto:
            # Verificar que tenga ubicación
            if not coord.ubicacion_id:
                coords_con_problema.append(coord)
                print(f"❌ Coordinador {coord.nombre} (ID: {coord.id}) sin ubicación")
                continue
            
            # Verificar que la ubicación exista
            ubicacion = Location.query.get(coord.ubicacion_id)
            if not ubicacion:
                coords_con_problema.append(coord)
                print(f"❌ Coordinador {coord.nombre} (ID: {coord.id}) con ubicación inválida")
                continue
            
            # Verificar que la ubicación sea de tipo puesto
            if ubicacion.tipo != 'puesto':
                coords_con_problema.append(coord)
                print(f"❌ Coordinador {coord.nombre} (ID: {coord.id}) con ubicación tipo '{ubicacion.tipo}' (debe ser 'puesto')")
                continue
            
            # Verificar contraseña
            if not coord.check_password('test123'):
                coords_con_problema.append(coord)
                print(f"❌ Coordinador {coord.nombre} (ID: {coord.id}) con contraseña incorrecta")
        
        if coords_con_problema:
            print(f"\n⚠️  {len(coords_con_problema)} coordinadores con problemas")
        else:
            print(f"\n✅ Todos los coordinadores están correctos")
        
        print()
        
        # 4. Corregir contraseñas
        print("4. CORRIGIENDO CONTRASEÑAS")
        print("-" * 80)
        
        usuarios_corregidos = 0
        for usuario in testigos_con_problema + coords_con_problema:
            if not usuario.check_password('test123'):
                usuario.set_password('test123')
                usuario.intentos_fallidos = 0
                usuario.bloqueado_hasta = None
                usuarios_corregidos += 1
                print(f"✅ Contraseña corregida para {usuario.nombre}")
        
        if usuarios_corregidos > 0:
            db.session.commit()
            print(f"\n✅ {usuarios_corregidos} contraseñas corregidas")
        else:
            print("\nℹ️  No hay contraseñas que corregir")
        
        print()
        
        # 5. Mostrar ejemplo de login para testigo
        print("5. EJEMPLO DE LOGIN PARA TESTIGO")
        print("-" * 80)
        
        testigo_ejemplo = testigos[0] if testigos else None
        if testigo_ejemplo and testigo_ejemplo.ubicacion_id:
            ubicacion = Location.query.get(testigo_ejemplo.ubicacion_id)
            if ubicacion:
                print(f"Usuario: {testigo_ejemplo.nombre}")
                print(f"Rol: testigo_electoral")
                print(f"Departamento: {ubicacion.departamento_codigo} ({ubicacion.departamento_nombre})")
                print(f"Municipio: {ubicacion.municipio_codigo} ({ubicacion.municipio_nombre})")
                print(f"Zona: {ubicacion.zona_codigo} ({ubicacion.zona_nombre})")
                print(f"Puesto: {ubicacion.puesto_codigo} ({ubicacion.puesto_nombre})")
                print(f"Contraseña: test123")
        
        print()
        
        # 6. Mostrar ejemplo de login para monitoreo
        print("6. EJEMPLO DE LOGIN PARA MONITOREO")
        print("-" * 80)
        print(f"Usuario: MONITOREO")
        print(f"Rol: monitoreo")
        print(f"Contraseña: test123")
        print(f"Nota: No requiere seleccionar ubicación")
        
        print()
        print("=" * 80)
        print("DIAGNÓSTICO COMPLETADO")
        print("=" * 80)

if __name__ == "__main__":
    try:
        diagnosticar_usuarios()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
