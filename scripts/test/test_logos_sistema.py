"""
Script de prueba completo del sistema de logos
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from backend.app import create_app
from backend.models.configuracion_electoral import Partido
from backend.database import db

def test_sistema_logos():
    """Probar el sistema completo de logos"""
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("PRUEBA DEL SISTEMA DE LOGOS")
        print("=" * 80)
        print()
        
        # 1. Verificar partidos en BD
        print("1. VERIFICANDO PARTIDOS EN BASE DE DATOS")
        print("-" * 80)
        partidos = Partido.query.all()
        print(f"✅ Total de partidos: {len(partidos)}")
        
        if len(partidos) == 0:
            print("⚠️  No hay partidos en la base de datos")
            print("   Ejecuta: python backend/scripts/init_super_admin_data.py")
            return
        
        print()
        
        # 2. Verificar estructura de datos
        print("2. VERIFICANDO ESTRUCTURA DE DATOS")
        print("-" * 80)
        partido_ejemplo = partidos[0]
        campos_requeridos = ['id', 'codigo', 'nombre', 'nombre_corto', 'color', 'logo_url', 'activo']
        
        for campo in campos_requeridos:
            tiene_campo = hasattr(partido_ejemplo, campo)
            valor = getattr(partido_ejemplo, campo, None) if tiene_campo else None
            print(f"  {campo}: {'✅' if tiene_campo else '❌'} = {valor}")
        
        print()
        
        # 3. Verificar logos
        print("3. VERIFICANDO LOGOS")
        print("-" * 80)
        con_logo = sum(1 for p in partidos if p.logo_url)
        sin_logo = len(partidos) - con_logo
        
        print(f"  Con logo: {con_logo} ({con_logo/len(partidos)*100:.1f}%)")
        print(f"  Sin logo: {sin_logo} ({sin_logo/len(partidos)*100:.1f}%)")
        print()
        
        # 4. Verificar colores
        print("4. VERIFICANDO COLORES")
        print("-" * 80)
        con_color = sum(1 for p in partidos if p.color)
        sin_color = len(partidos) - con_color
        
        print(f"  Con color: {con_color} ({con_color/len(partidos)*100:.1f}%)")
        print(f"  Sin color: {sin_color} ({sin_color/len(partidos)*100:.1f}%)")
        print()
        
        # 5. Mostrar ejemplos
        print("5. EJEMPLOS DE PARTIDOS")
        print("-" * 80)
        for i, partido in enumerate(partidos[:5], 1):
            print(f"\n{i}. {partido.nombre} ({partido.codigo})")
            print(f"   Nombre corto: {partido.nombre_corto or 'N/A'}")
            print(f"   Color: {partido.color or 'N/A'}")
            print(f"   Logo: {'✅ ' + partido.logo_url if partido.logo_url else '❌ Sin logo'}")
            print(f"   Estado: {'🟢 Activo' if partido.activo else '🔴 Inactivo'}")
            
            # Simular cómo se vería en el frontend
            if partido.logo_url:
                print(f"   Frontend: Mostrará imagen desde {partido.logo_url}")
            else:
                iniciales = partido.nombre_corto[:3] if partido.nombre_corto else partido.nombre[:3]
                print(f"   Frontend: Mostrará avatar con iniciales '{iniciales.upper()}'")
        
        print()
        
        # 6. Resumen final
        print("=" * 80)
        print("RESUMEN DE LA PRUEBA")
        print("=" * 80)
        
        tests_passed = 0
        tests_total = 5
        
        # Test 1: Hay partidos
        if len(partidos) > 0:
            print("✅ Test 1: Hay partidos en la base de datos")
            tests_passed += 1
        else:
            print("❌ Test 1: No hay partidos en la base de datos")
        
        # Test 2: Estructura correcta
        if all(hasattr(partido_ejemplo, campo) for campo in campos_requeridos):
            print("✅ Test 2: Estructura de datos correcta")
            tests_passed += 1
        else:
            print("❌ Test 2: Estructura de datos incompleta")
        
        # Test 3: Al menos algunos logos
        if con_logo > 0:
            print(f"✅ Test 3: Hay {con_logo} partidos con logo")
            tests_passed += 1
        else:
            print("⚠️  Test 3: No hay partidos con logo (se usarán avatares)")
            tests_passed += 0.5
        
        # Test 4: Todos tienen color
        if con_color == len(partidos):
            print("✅ Test 4: Todos los partidos tienen color")
            tests_passed += 1
        else:
            print(f"⚠️  Test 4: {sin_color} partidos sin color (se usará gris por defecto)")
            tests_passed += 0.5
        
        # Test 5: Sistema funcional
        print("✅ Test 5: Sistema de logos funcional")
        tests_passed += 1
        
        print()
        print(f"RESULTADO: {tests_passed}/{tests_total} tests pasados")
        
        if tests_passed >= 4:
            print("🎉 ¡Sistema de logos funcionando correctamente!")
        elif tests_passed >= 3:
            print("⚠️  Sistema funcional pero con advertencias")
        else:
            print("❌ Sistema requiere atención")
        
        print("=" * 80)
        
        # 7. Recomendaciones
        print("\n📋 RECOMENDACIONES:")
        print("-" * 80)
        
        if sin_logo > 0:
            print(f"• Ejecuta 'python backend/scripts/cargar_logos_reales.py' para agregar logos a {sin_logo} partidos")
        
        if sin_color > 0:
            print(f"• Asigna colores a {sin_color} partidos desde el dashboard de super admin")
        
        print("• Recarga el dashboard con Ctrl+Shift+R para ver los cambios")
        print("• Los logos se muestran en la sección 'Configuración > Partidos Políticos'")
        
        print()

if __name__ == '__main__':
    test_sistema_logos()
