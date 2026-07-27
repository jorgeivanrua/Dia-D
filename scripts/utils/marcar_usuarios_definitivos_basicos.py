"""
Script para marcar usuarios definitivos como usuarios básicos del sistema

USUARIOS BÁSICOS DEFINITIVOS:
- Super Admin (1 global)
- Monitoreo (1 global)
- Coordinador Departamental (1 por departamento)
- Coordinador Municipal (1 por municipio)
- Coordinador Puesto (1 por puesto)
- Testigo (1 por puesto)
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

def marcar_usuarios_definitivos():
    """
    Marcar usuarios definitivos como usuarios básicos del sistema
    """
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("=" * 80)
        print("MARCAR USUARIOS DEFINITIVOS COMO BÁSICOS".center(80))
        print("=" * 80)
        print()
        
        usuarios_marcados = 0
        
        # 1. Super Admin y Monitoreo (ya deberían estar marcados)
        print("📋 1. Usuarios Globales:")
        print("-" * 80)
        
        for rol in ['super_admin', 'monitoreo']:
            usuarios = User.query.filter_by(rol=rol, activo=True).all()
            for usuario in usuarios:
                if not usuario.es_usuario_basico:
                    usuario.es_usuario_basico = True
                    usuarios_marcados += 1
                    print(f"🔧 Marcando: {usuario.nombre} ({rol})")
                else:
                    print(f"✅ Ya básico: {usuario.nombre} ({rol})")
        
        print()
        
        # 2. Coordinadores Departamentales (1 por departamento)
        print("📋 2. Coordinadores Departamentales (1 por departamento):")
        print("-" * 80)
        
        departamentos = Location.query.filter_by(tipo='departamento').all()
        for depto in departamentos:
            coordinadores = User.query.filter_by(
                rol='coordinador_departamental',
                ubicacion_id=depto.id,
                activo=True
            ).all()
            
            if not coordinadores:
                print(f"⚠️  {depto.nombre_completo}: Sin coordinador departamental")
                continue
            
            # Marcar el primero como básico
            coordinador_basico = next((c for c in coordinadores if c.es_usuario_basico), None)
            
            if coordinador_basico:
                print(f"✅ {depto.nombre_completo}: {coordinador_basico.nombre}")
            else:
                coordinadores[0].es_usuario_basico = True
                usuarios_marcados += 1
                print(f"🔧 {depto.nombre_completo}: Marcando {coordinadores[0].nombre}")
            
            # Advertir si hay múltiples coordinadores
            if len(coordinadores) > 1:
                print(f"   ⚠️  Hay {len(coordinadores)} coordinadores, solo el primero es básico")
        
        print()
        
        # 3. Coordinadores Municipales (1 por municipio)
        print("📋 3. Coordinadores Municipales (1 por municipio):")
        print("-" * 80)
        
        municipios = Location.query.filter_by(tipo='municipio').all()
        municipios_sin_coordinador = []
        
        for municipio in municipios:
            coordinadores = User.query.filter_by(
                rol='coordinador_municipal',
                ubicacion_id=municipio.id,
                activo=True
            ).all()
            
            if not coordinadores:
                municipios_sin_coordinador.append(municipio.nombre_completo)
                continue
            
            # Marcar el primero como básico
            coordinador_basico = next((c for c in coordinadores if c.es_usuario_basico), None)
            
            if coordinador_basico:
                print(f"✅ {municipio.nombre_completo}: {coordinador_basico.nombre}")
            else:
                coordinadores[0].es_usuario_basico = True
                usuarios_marcados += 1
                print(f"🔧 {municipio.nombre_completo}: Marcando {coordinadores[0].nombre}")
            
            # Advertir si hay múltiples coordinadores
            if len(coordinadores) > 1:
                print(f"   ⚠️  Hay {len(coordinadores)} coordinadores, solo el primero es básico")
        
        if municipios_sin_coordinador:
            print(f"\n⚠️  {len(municipios_sin_coordinador)} municipios sin coordinador")
        
        print()
        
        # 4. Coordinadores de Puesto (1 por puesto)
        print("📋 4. Coordinadores de Puesto (1 por puesto):")
        print("-" * 80)
        
        puestos = Location.query.filter_by(tipo='puesto').all()
        puestos_sin_coordinador = []
        
        for puesto in puestos:
            coordinadores = User.query.filter_by(
                rol='coordinador_puesto',
                ubicacion_id=puesto.id,
                activo=True
            ).all()
            
            if not coordinadores:
                puestos_sin_coordinador.append(puesto.nombre_completo)
                continue
            
            # Marcar el primero como básico
            coordinador_basico = next((c for c in coordinadores if c.es_usuario_basico), None)
            
            if coordinador_basico:
                print(f"✅ {puesto.nombre_completo}: {coordinador_basico.nombre}")
            else:
                coordinadores[0].es_usuario_basico = True
                usuarios_marcados += 1
                print(f"🔧 {puesto.nombre_completo}: Marcando {coordinadores[0].nombre}")
            
            # Advertir si hay múltiples coordinadores
            if len(coordinadores) > 1:
                print(f"   ⚠️  Hay {len(coordinadores)} coordinadores, solo el primero es básico")
        
        if puestos_sin_coordinador:
            print(f"\n⚠️  {len(puestos_sin_coordinador)} puestos sin coordinador")
        
        print()
        
        # 5. Testigos (1 por puesto)
        print("📋 5. Testigos (1 por puesto):")
        print("-" * 80)
        
        puestos_sin_testigo = []
        
        for puesto in puestos:
            testigos = User.query.filter_by(
                rol='testigo_electoral',
                ubicacion_id=puesto.id,
                activo=True
            ).all()
            
            if not testigos:
                puestos_sin_testigo.append(puesto.nombre_completo)
                continue
            
            # Marcar el primero como básico
            testigo_basico = next((t for t in testigos if t.es_usuario_basico), None)
            
            if testigo_basico:
                print(f"✅ {puesto.nombre_completo}: {testigo_basico.nombre}")
            else:
                testigos[0].es_usuario_basico = True
                usuarios_marcados += 1
                print(f"🔧 {puesto.nombre_completo}: Marcando {testigos[0].nombre}")
            
            # Advertir si hay múltiples testigos
            if len(testigos) > 1:
                print(f"   ⚠️  Hay {len(testigos)} testigos, solo el primero es básico")
        
        if puestos_sin_testigo:
            print(f"\n⚠️  {len(puestos_sin_testigo)} puestos sin testigo")
        
        print()
        
        # Guardar cambios
        if usuarios_marcados > 0:
            db.session.commit()
            print(f"✅ {usuarios_marcados} usuarios marcados como básicos")
        else:
            print("✅ Todos los usuarios definitivos ya estaban marcados como básicos")
        
        print()
        
        # Resumen final
        print("=" * 80)
        print("RESUMEN".center(80))
        print("=" * 80)
        
        total_basicos = User.query.filter_by(es_usuario_basico=True).count()
        print(f"📊 Total de usuarios básicos: {total_basicos}")
        print()
        print("   Desglose:")
        print(f"   - Super Admin: {User.query.filter_by(rol='super_admin', es_usuario_basico=True).count()}")
        print(f"   - Monitoreo: {User.query.filter_by(rol='monitoreo', es_usuario_basico=True).count()}")
        print(f"   - Coordinadores Departamentales: {User.query.filter_by(rol='coordinador_departamental', es_usuario_basico=True).count()}")
        print(f"   - Coordinadores Municipales: {User.query.filter_by(rol='coordinador_municipal', es_usuario_basico=True).count()}")
        print(f"   - Coordinadores de Puesto: {User.query.filter_by(rol='coordinador_puesto', es_usuario_basico=True).count()}")
        print(f"   - Testigos: {User.query.filter_by(rol='testigo_electoral', es_usuario_basico=True).count()}")
        print()
        print("=" * 80)
        print("✅ PROCESO COMPLETADO".center(80))
        print("=" * 80)

if __name__ == '__main__':
    try:
        marcar_usuarios_definitivos()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
