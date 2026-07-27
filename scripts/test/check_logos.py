"""
Script para verificar los logos de los partidos
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import create_app
from backend.models.configuracion_electoral import Partido

def verificar_logos():
    """Verificar estado de logos de partidos"""
    app = create_app()
    with app.app_context():
        partidos = Partido.query.order_by(Partido.nombre).all()
        
        print("=" * 80)
        print("VERIFICACIÓN DE LOGOS DE PARTIDOS")
        print("=" * 80)
        print(f"Total de partidos: {len(partidos)}\n")
        
        con_logo = 0
        sin_logo = 0
        activos_con_logo = 0
        activos_sin_logo = 0
        
        print("PARTIDOS CON LOGO:")
        print("-" * 80)
        for p in partidos:
            if p.logo_url:
                estado = "🟢 ACTIVO" if p.activo else "🔴 INACTIVO"
                print(f"✅ {p.nombre} ({p.codigo})")
                print(f"   Estado: {estado}")
                print(f"   Logo: {p.logo_url}")
                print(f"   Color: {p.color or 'Sin color'}")
                print()
                con_logo += 1
                if p.activo:
                    activos_con_logo += 1
        
        print("\n" + "=" * 80)
        print("PARTIDOS SIN LOGO:")
        print("-" * 80)
        for p in partidos:
            if not p.logo_url:
                estado = "🟢 ACTIVO" if p.activo else "🔴 INACTIVO"
                print(f"❌ {p.nombre} ({p.codigo})")
                print(f"   Estado: {estado}")
                print(f"   Color: {p.color or 'Sin color'}")
                print(f"   💡 Mostrará avatar con iniciales: {p.nombre_corto or p.nombre[:3]}")
                print()
                sin_logo += 1
                if p.activo:
                    activos_sin_logo += 1
        
        print("\n" + "=" * 80)
        print("RESUMEN:")
        print("-" * 80)
        print(f"  Total de partidos: {len(partidos)}")
        print(f"  Con logo: {con_logo} ({con_logo/len(partidos)*100:.1f}%)")
        print(f"  Sin logo: {sin_logo} ({sin_logo/len(partidos)*100:.1f}%)")
        print()
        print(f"  Partidos activos: {activos_con_logo + activos_sin_logo}")
        print(f"    • Con logo: {activos_con_logo}")
        print(f"    • Sin logo: {activos_sin_logo}")
        print("=" * 80)
        
        if sin_logo > 0:
            print("\n💡 RECOMENDACIÓN:")
            print("   Los partidos sin logo mostrarán un avatar con sus iniciales")
            print("   Para agregar logos, ejecuta: python backend/scripts/cargar_logos_reales.py")

if __name__ == '__main__':
    verificar_logos()
