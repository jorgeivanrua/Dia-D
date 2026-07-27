"""
Script para verificar integridad de datos de mesas y testigos
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.database import db
from backend.models.location import Location
from backend.models.user import User
from backend.app import create_app


def verificar_mesas_puesto(puesto_codigo):
    """Verificar mesas de un puesto"""
    
    print(f"\n{'='*60}")
    print(f"VERIFICACIÓN DE MESAS - PUESTO: {puesto_codigo}")
    print(f"{'='*60}\n")
    
    # Buscar puesto
    puesto = Location.query.filter_by(
        puesto_codigo=puesto_codigo,
        tipo='puesto'
    ).first()
    
    if not puesto:
        print(f"❌ ERROR: Puesto '{puesto_codigo}' no encontrado en la base de datos")
        print(f"\nVerifique que el código sea correcto.")
        return
    
    print(f"✅ PUESTO ENCONTRADO")
    print(f"   Nombre: {puesto.nombre_completo}")
    print(f"   ID: {puesto.id}")
    print(f"   Código: {puesto.puesto_codigo}")
    print(f"   Activo: {'Sí' if puesto.activo else 'No'}")
    print(f"   Dirección: {puesto.direccion or 'N/A'}")
    
    # Buscar coordinador del puesto
    coordinador = User.query.filter_by(
        ubicacion_id=puesto.id,
        rol='coordinador_puesto'
    ).first()
    
    if coordinador:
        print(f"   Coordinador: {coordinador.nombre}")
    else:
        print(f"   ⚠️  Sin coordinador asignado")
    
    # Buscar mesas (todas, incluyendo inactivas)
    mesas_todas = Location.query.filter_by(
        puesto_codigo=puesto_codigo,
        tipo='mesa'
    ).all()
    
    mesas_activas = [m for m in mesas_todas if m.activo]
    mesas_inactivas = [m for m in mesas_todas if not m.activo]
    
    print(f"\n{'='*60}")
    print(f"RESUMEN DE MESAS")
    print(f"{'='*60}")
    print(f"   Total de mesas: {len(mesas_todas)}")
    print(f"   Mesas activas: {len(mesas_activas)}")
    print(f"   Mesas inactivas: {len(mesas_inactivas)}")
    
    if len(mesas_todas) == 0:
        print(f"\n❌ ERROR: No hay mesas registradas para este puesto")
        print(f"   Debe crear las mesas en la base de datos primero.")
        return
    
    # Estadísticas de testigos
    testigos_asignados = 0
    testigos_presentes = 0
    mesas_sin_testigo = []
    
    print(f"\n{'='*60}")
    print(f"DETALLE DE MESAS")
    print(f"{'='*60}\n")
    
    for i, mesa in enumerate(mesas_activas, 1):
        print(f"{i}. Mesa {mesa.mesa_codigo}")
        print(f"   ID: {mesa.id}")
        print(f"   Nombre: {mesa.nombre_completo}")
        print(f"   Votantes registrados: {mesa.total_votantes_registrados}")
        print(f"   Activa: {'Sí' if mesa.activo else 'No'}")
        
        # Buscar testigo asignado
        testigo = User.query.filter_by(
            ubicacion_id=mesa.id,
            rol='testigo_electoral'
        ).first()
        
        if testigo:
            testigos_asignados += 1
            print(f"   Testigo: {testigo.nombre} (ID: {testigo.id})")
            
            if testigo.presencia_verificada:
                testigos_presentes += 1
                print(f"   ✅ Presencia VERIFICADA")
                if testigo.presencia_verificada_at:
                    print(f"      Verificada el: {testigo.presencia_verificada_at.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"   ❌ Presencia NO VERIFICADA")
        else:
            mesas_sin_testigo.append(mesa.mesa_codigo)
            print(f"   ⚠️  SIN TESTIGO ASIGNADO")
        
        print()
    
    # Mostrar mesas inactivas si existen
    if mesas_inactivas:
        print(f"\n{'='*60}")
        print(f"MESAS INACTIVAS ({len(mesas_inactivas)})")
        print(f"{'='*60}\n")
        for mesa in mesas_inactivas:
            print(f"   - Mesa {mesa.mesa_codigo}: {mesa.nombre_completo}")
    
    # Resumen final
    print(f"\n{'='*60}")
    print(f"RESUMEN FINAL")
    print(f"{'='*60}")
    print(f"   Total mesas activas: {len(mesas_activas)}")
    print(f"   Testigos asignados: {testigos_asignados}/{len(mesas_activas)}")
    print(f"   Testigos presentes: {testigos_presentes}/{testigos_asignados if testigos_asignados > 0 else 0}")
    
    if mesas_sin_testigo:
        print(f"\n   ⚠️  MESAS SIN TESTIGO ({len(mesas_sin_testigo)}):")
        for codigo in mesas_sin_testigo:
            print(f"      - Mesa {codigo}")
    
    # Recomendaciones
    print(f"\n{'='*60}")
    print(f"RECOMENDACIONES")
    print(f"{'='*60}")
    
    if len(mesas_sin_testigo) > 0:
        print(f"   ⚠️  Asignar testigos a las {len(mesas_sin_testigo)} mesa(s) sin testigo")
    
    if testigos_asignados > 0 and testigos_presentes < testigos_asignados:
        faltantes = testigos_asignados - testigos_presentes
        print(f"   ⚠️  {faltantes} testigo(s) no han verificado su presencia")
        print(f"      Los testigos deben hacer clic en 'Verificar Mi Presencia' en su dashboard")
    
    if len(mesas_inactivas) > 0:
        print(f"   ⚠️  Hay {len(mesas_inactivas)} mesa(s) inactiva(s)")
        print(f"      Considere activarlas si deben estar operativas")
    
    if testigos_presentes == testigos_asignados and len(mesas_sin_testigo) == 0:
        print(f"   ✅ Todo está correcto!")
    
    print()


def listar_todos_los_puestos():
    """Listar todos los puestos disponibles"""
    puestos = Location.query.filter_by(tipo='puesto', activo=True).all()
    
    print(f"\n{'='*60}")
    print(f"PUESTOS DISPONIBLES ({len(puestos)})")
    print(f"{'='*60}\n")
    
    if len(puestos) == 0:
        print("   No hay puestos registrados en la base de datos")
        return
    
    for puesto in puestos:
        print(f"   - {puesto.puesto_codigo}: {puesto.nombre_completo}")
    
    print()


if __name__ == '__main__':
    # Crear app context
    app = create_app()
    
    with app.app_context():
        if len(sys.argv) < 2:
            print("\n" + "="*60)
            print("SCRIPT DE VERIFICACIÓN DE MESAS")
            print("="*60)
            print("\nUso:")
            print("   python backend/scripts/verificar_mesas.py <puesto_codigo>")
            print("   python backend/scripts/verificar_mesas.py --list")
            print("\nEjemplos:")
            print("   python backend/scripts/verificar_mesas.py PUESTO001")
            print("   python backend/scripts/verificar_mesas.py --list")
            print()
            sys.exit(1)
        
        comando = sys.argv[1]
        
        if comando == '--list':
            listar_todos_los_puestos()
        else:
            puesto_codigo = comando
            verificar_mesas_puesto(puesto_codigo)
