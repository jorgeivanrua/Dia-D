"""
Script para verificar el estado de los usuarios básicos del sistema
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

def verificar_usuarios_basicos():
    """
    Verificar que todos los usuarios básicos del sistema existan
    """
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("=" * 80)
        print("VERIFICACIÓN DE USUARIOS BÁSICOS DEL SISTEMA".center(80))
        print("=" * 80)
        print()
        
        # 1. Usuarios Globales
        print("📋 1. Usuarios Globales:")
        print("-" * 80)
        
        roles_globales = {
            'super_admin': 'Super Admin',
            'monitoreo': 'Monitoreo'
        }
        
        todos_presentes = True
        
        for rol, nombre_esperado in roles_globales.items():
            usuario = User.query.filter_by(
                rol=rol,
                es_usuario_basico=True,
                activo=True
            ).first()
            
            if usuario:
                print(f"✅ {nombre_esperado:35} | {usuario.nombre:30} | ID: {usuario.id}")
            else:
                print(f"❌ {nombre_esperado:35} | NO ENCONTRADO")
                todos_presentes = False
        
        print("-" * 80)
        print()
        
        # 2. Coordinadores Departamentales (1 por departamento)
        print("📋 2. Coordinadores Departamentales (1 por departamento):")
        print("-" * 80)
        
        departamentos = Location.query.filter_by(tipo='departamento').count()
        coord_depto_basicos = User.query.filter_by(
            rol='coordinador_departamental',
            es_usuario_basico=True,
            activo=True
        ).count()
        
        print(f"   Departamentos: {departamentos}")
        print(f"   Coordinadores básicos: {coord_depto_basicos}")
        
        if coord_depto_basicos < departamentos:
            print(f"   ⚠️  Faltan {departamentos - coord_depto_basicos} coordinadores departamentales")
            todos_presentes = False
        else:
            print(f"   ✅ Todos los departamentos tienen coordinador básico")
        
        print("-" * 80)
        print()
        
        # 3. Coordinadores Municipales (1 por municipio)
        print("📋 3. Coordinadores Municipales (1 por municipio):")
        print("-" * 80)
        
        municipios = Location.query.filter_by(tipo='municipio').count()
        coord_muni_basicos = User.query.filter_by(
            rol='coordinador_municipal',
            es_usuario_basico=True,
            activo=True
        ).count()
        
        print(f"   Municipios: {municipios}")
        print(f"   Coordinadores básicos: {coord_muni_basicos}")
        
        if coord_muni_basicos < municipios:
            print(f"   ⚠️  Faltan {municipios - coord_muni_basicos} coordinadores municipales")
            todos_presentes = False
        else:
            print(f"   ✅ Todos los municipios tienen coordinador básico")
        
        print("-" * 80)
        print()
        
        # 4. Coordinadores de Puesto (1 por puesto)
        print("📋 4. Coordinadores de Puesto (1 por puesto):")
        print("-" * 80)
        
        puestos = Location.query.filter_by(tipo='puesto').count()
        coord_puesto_basicos = User.query.filter_by(
            rol='coordinador_puesto',
            es_usuario_basico=True,
            activo=True
        ).count()
        
        print(f"   Puestos: {puestos}")
        print(f"   Coordinadores básicos: {coord_puesto_basicos}")
        
        if coord_puesto_basicos < puestos:
            print(f"   ⚠️  Faltan {puestos - coord_puesto_basicos} coordinadores de puesto")
            todos_presentes = False
        else:
            print(f"   ✅ Todos los puestos tienen coordinador básico")
        
        print("-" * 80)
        print()
        
        # 5. Testigos (1 por puesto)
        print("📋 5. Testigos (1 por puesto):")
        print("-" * 80)
        
        testigos_basicos = User.query.filter_by(
            rol='testigo_electoral',
            es_usuario_basico=True,
            activo=True
        ).count()
        
        print(f"   Puestos: {puestos}")
        print(f"   Testigos básicos: {testigos_basicos}")
        
        if testigos_basicos < puestos:
            print(f"   ⚠️  Faltan {puestos - testigos_basicos} testigos básicos")
            todos_presentes = False
        else:
            print(f"   ✅ Todos los puestos tienen testigo básico")
        
        print("-" * 80)
        print()
        
        # Estadísticas generales
        total_usuarios = User.query.count()
        total_basicos = User.query.filter_by(es_usuario_basico=True).count()
        total_prueba = total_usuarios - total_basicos
        
        print("📊 Estadísticas generales:")
        print(f"   Total de usuarios: {total_usuarios}")
        print(f"   Usuarios básicos del sistema: {total_basicos}")
        print(f"   Usuarios de prueba/temporales: {total_prueba}")
        print()
        
        if todos_presentes:
            print("=" * 80)
            print("✅ TODOS LOS USUARIOS BÁSICOS ESTÁN PRESENTES".center(80))
            print("=" * 80)
        else:
            print("=" * 80)
            print("⚠️  FALTAN USUARIOS BÁSICOS".center(80))
            print("=" * 80)
            print()
            print("💡 Ejecuta la aplicación para crear automáticamente los usuarios faltantes")
            print("   O ejecuta: python backend/utils/init_usuarios_basicos.py")

if __name__ == '__main__':
    try:
        verificar_usuarios_basicos()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
