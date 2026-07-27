"""
Script para crear usuarios del Caquetá con ubicaciones
"""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location
from backend.database import db

def crear_usuarios_caqueta():
    """Crear estructura de usuarios para el Caquetá"""
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("CREACIÓN DE USUARIOS PARA EL CAQUETÁ")
        print("=" * 80)
        print()
        
        # 1. Verificar que existen ubicaciones del Caquetá
        print("1. VERIFICANDO UBICACIONES DEL CAQUETÁ")
        print("-" * 80)
        
        departamento = Location.query.filter_by(
            tipo='departamento',
            departamento_codigo='44'
        ).first()
        
        if not departamento:
            print("❌ No se encontró el departamento del Caquetá")
            print("   Ejecuta primero: python backend/scripts/init_caqueta_electoral_data.py")
            return
        
        municipios = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo='44'
        ).all()
        
        puestos = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo='44'
        ).all()
        
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo='44'
        ).all()
        
        print(f"✅ Departamento: {departamento.nombre_completo}")
        print(f"✅ Municipios: {len(municipios)}")
        print(f"✅ Puestos: {len(puestos)}")
        print(f"✅ Mesas: {len(mesas)}")
        print()
        
        # 2. Crear Coordinador Departamental
        print("2. CREANDO COORDINADOR DEPARTAMENTAL")
        print("-" * 80)
        
        coord_depto = User.query.filter_by(
            rol='coordinador_departamental',
            ubicacion_id=departamento.id
        ).first()
        
        if not coord_depto:
            coord_depto = User(
                nombre='CAQUETA',
                rol='coordinador_departamental',
                ubicacion_id=departamento.id,
                activo=True,
                es_usuario_basico=False
            )
            coord_depto.set_password('test123')
            db.session.add(coord_depto)
            print(f"✅ Creado: CAQUETA (Coordinador Departamental)")
        else:
            print(f"ℹ️  Ya existe: {coord_depto.nombre}")
        
        print()
        
        # 3. Crear Coordinadores Municipales
        print("3. CREANDO COORDINADORES MUNICIPALES")
        print("-" * 80)
        
        coords_muni_creados = 0
        for municipio in municipios:
            # Nombre de usuario basado en el municipio
            nombre_usuario = municipio.municipio_nombre.upper().replace(' ', '_')
            
            coord_muni = User.query.filter_by(
                rol='coordinador_municipal',
                ubicacion_id=municipio.id
            ).first()
            
            if not coord_muni:
                coord_muni = User(
                    nombre=nombre_usuario,
                    rol='coordinador_municipal',
                    ubicacion_id=municipio.id,
                    activo=True,
                    es_usuario_basico=False
                )
                coord_muni.set_password('test123')
                db.session.add(coord_muni)
                coords_muni_creados += 1
                print(f"✅ Creado: {nombre_usuario} ({municipio.municipio_nombre})")
        
        print(f"\n✅ Total: {coords_muni_creados} coordinadores municipales creados")
        print()
        
        # 4. Crear Coordinadores de Puesto
        print("4. CREANDO COORDINADORES DE PUESTO")
        print("-" * 80)
        
        coords_puesto_creados = 0
        for puesto in puestos:
            # Nombre de usuario basado en municipio y puesto
            municipio_nombre = puesto.municipio_nombre.upper().replace(' ', '_')
            nombre_usuario = f"{municipio_nombre}_P{puesto.puesto_codigo}"
            
            coord_puesto = User.query.filter_by(
                rol='coordinador_puesto',
                ubicacion_id=puesto.id
            ).first()
            
            if not coord_puesto:
                coord_puesto = User(
                    nombre=nombre_usuario,
                    rol='coordinador_puesto',
                    ubicacion_id=puesto.id,
                    activo=True,
                    es_usuario_basico=False
                )
                coord_puesto.set_password('test123')
                db.session.add(coord_puesto)
                coords_puesto_creados += 1
                
                if coords_puesto_creados <= 5:  # Mostrar solo los primeros 5
                    print(f"✅ Creado: {nombre_usuario}")
        
        if coords_puesto_creados > 5:
            print(f"   ... y {coords_puesto_creados - 5} más")
        
        print(f"\n✅ Total: {coords_puesto_creados} coordinadores de puesto creados")
        print()
        
        # 5. Crear Testigos
        print("5. CREANDO TESTIGOS ELECTORALES")
        print("-" * 80)
        
        testigos_creados = 0
        for mesa in mesas:
            # Nombre de usuario basado en municipio, puesto y mesa
            municipio_nombre = mesa.municipio_nombre.upper().replace(' ', '_')
            nombre_usuario = f"{municipio_nombre}_P{mesa.puesto_codigo}_M{mesa.mesa_codigo}"
            
            testigo = User.query.filter_by(
                rol='testigo_electoral',
                ubicacion_id=mesa.id
            ).first()
            
            if not testigo:
                testigo = User(
                    nombre=nombre_usuario,
                    rol='testigo_electoral',
                    ubicacion_id=mesa.id,
                    activo=True,
                    es_usuario_basico=False
                )
                testigo.set_password('test123')
                db.session.add(testigo)
                testigos_creados += 1
                
                if testigos_creados <= 5:  # Mostrar solo los primeros 5
                    print(f"✅ Creado: {nombre_usuario}")
        
        if testigos_creados > 5:
            print(f"   ... y {testigos_creados - 5} más")
        
        print(f"\n✅ Total: {testigos_creados} testigos creados")
        print()
        
        # 6. Guardar todos los cambios
        print("6. GUARDANDO CAMBIOS")
        print("-" * 80)
        
        try:
            db.session.commit()
            print("✅ Todos los usuarios guardados exitosamente")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al guardar: {e}")
            return
        
        print()
        
        # 7. Resumen final
        print("=" * 80)
        print("RESUMEN DE CREACIÓN")
        print("=" * 80)
        print()
        print(f"✅ Coordinador Departamental: 1")
        print(f"✅ Coordinadores Municipales: {coords_muni_creados}")
        print(f"✅ Coordinadores de Puesto: {coords_puesto_creados}")
        print(f"✅ Testigos Electorales: {testigos_creados}")
        print(f"\n📊 TOTAL USUARIOS CREADOS: {1 + coords_muni_creados + coords_puesto_creados + testigos_creados}")
        print()
        print("🔐 CONTRASEÑAS:")
        print("   • Super Admin: admin123")
        print("   • Todos los demás: test123")
        print()
        print("⚠️  IMPORTANTE: Estos usuarios están listos para usar")
        print("   Cada usuario está vinculado a su ubicación geográfica")
        print()
        print("=" * 80)

if __name__ == '__main__':
    crear_usuarios_caqueta()
