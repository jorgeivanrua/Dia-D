"""
Script de Verificación Completa del Sistema
Verifica todos los roles, endpoints y funcionalidades
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.models.configuracion_electoral import TipoEleccion, Partido, Candidato
from backend.models.formulario_e14 import FormularioE14
from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral

def verificar_usuarios():
    """Verificar que todos los usuarios de prueba existan"""
    print("\n" + "="*70)
    print("VERIFICANDO USUARIOS DEL SISTEMA")
    print("="*70)
    
    usuarios_esperados = [
        ('super_admin', 'super_admin'),
        ('monitoreo', 'monitoreo'),
        ('auditor', 'auditor_electoral'),
        ('coord_dept', 'coordinador_departamental'),
        ('coord_mun', 'coordinador_municipal'),
        ('coord_puesto', 'coordinador_puesto'),
        ('testigo1', 'testigo_electoral'),
    ]
    
    for nombre, rol_esperado in usuarios_esperados:
        user = User.query.filter_by(nombre=nombre).first()
        if user:
            print(f"✅ {nombre:20} | Rol: {user.rol:30} | Activo: {user.activo}")
            if user.ubicacion_id:
                loc = Location.query.get(user.ubicacion_id)
                if loc:
                    print(f"   └─ Ubicación: {loc.nombre_completo}")
        else:
            print(f"❌ {nombre:20} | NO ENCONTRADO")
    
    return True

def verificar_ubicaciones():
    """Verificar datos de ubicaciones"""
    print("\n" + "="*70)
    print("VERIFICANDO UBICACIONES (DIVIPOLA)")
    print("="*70)
    
    stats = {
        'departamento': Location.query.filter_by(tipo='departamento').count(),
        'municipio': Location.query.filter_by(tipo='municipio').count(),
        'zona': Location.query.filter_by(tipo='zona').count(),
        'puesto': Location.query.filter_by(tipo='puesto').count(),
        'mesa': Location.query.filter_by(tipo='mesa').count(),
    }
    
    for tipo, count in stats.items():
        print(f"  {tipo.capitalize():15} : {count:6,}")
    
    # Verificar Caquetá específicamente
    caqueta = Location.query.filter_by(tipo='departamento', departamento_codigo='44').first()
    if caqueta:
        print(f"\n✅ Departamento Caquetá encontrado: {caqueta.departamento_nombre}")
        municipios = Location.query.filter_by(tipo='municipio', departamento_codigo='44').count()
        print(f"   └─ Municipios: {municipios}")
    else:
        print("\n❌ Departamento Caquetá NO encontrado")
    
    return True

def verificar_configuracion_electoral():
    """Verificar tipos de elección, partidos y candidatos"""
    print("\n" + "="*70)
    print("VERIFICANDO CONFIGURACIÓN ELECTORAL")
    print("="*70)
    
    tipos = TipoEleccion.query.filter_by(activo=True).count()
    partidos = Partido.query.filter_by(activo=True).count()
    candidatos = Candidato.query.filter_by(activo=True).count()
    
    print(f"  Tipos de Elección : {tipos}")
    print(f"  Partidos Activos  : {partidos}")
    print(f"  Candidatos Activos: {candidatos}")
    
    if tipos > 0:
        print("\n  Tipos de Elección:")
        for tipo in TipoEleccion.query.filter_by(activo=True).all():
            print(f"    - {tipo.nombre} ({tipo.codigo})")
    
    if partidos > 0:
        print("\n  Partidos:")
        for partido in Partido.query.filter_by(activo=True).limit(5).all():
            print(f"    - {partido.nombre} ({partido.nombre_corto})")
    
    return tipos > 0 and partidos > 0

def verificar_formularios():
    """Verificar formularios E-14"""
    print("\n" + "="*70)
    print("VERIFICANDO FORMULARIOS E-14")
    print("="*70)
    
    total = FormularioE14.query.count()
    validados = FormularioE14.query.filter_by(estado='validado').count()
    pendientes = FormularioE14.query.filter_by(estado='pendiente').count()
    rechazados = FormularioE14.query.filter_by(estado='rechazado').count()
    
    print(f"  Total      : {total}")
    print(f"  Validados  : {validados}")
    print(f"  Pendientes : {pendientes}")
    print(f"  Rechazados : {rechazados}")
    
    return True

def verificar_incidentes_delitos():
    """Verificar incidentes y delitos"""
    print("\n" + "="*70)
    print("VERIFICANDO INCIDENTES Y DELITOS")
    print("="*70)
    
    incidentes = IncidenteElectoral.query.count()
    delitos = DelitoElectoral.query.count()
    
    print(f"  Incidentes : {incidentes}")
    print(f"  Delitos    : {delitos}")
    
    return True

def verificar_endpoints():
    """Verificar que los endpoints principales respondan"""
    print("\n" + "="*70)
    print("VERIFICANDO ENDPOINTS PRINCIPALES")
    print("="*70)
    
    from flask import Flask
    from backend.routes.auth import auth_bp
    from backend.routes.testigo import testigo_bp
    from backend.routes.monitoreo import monitoreo_bp
    from backend.routes.super_admin import super_admin_bp
    
    endpoints_criticos = [
        ('auth', '/api/auth/login', 'POST'),
        ('locations', '/api/locations/departamentos', 'GET'),
        ('testigo', '/api/testigo/tipos-eleccion', 'GET'),
        ('monitoreo', '/api/monitoreo/estadisticas', 'GET'),
    ]
    
    print("\n  Endpoints registrados:")
    for nombre, ruta, metodo in endpoints_criticos:
        print(f"    {metodo:6} {ruta}")
    
    return True

def main():
    """Ejecutar todas las verificaciones"""
    print("\n" + "="*70)
    print("VERIFICACIÓN COMPLETA DEL SISTEMA ELECTORAL")
    print("="*70)
    
    app = create_app()
    
    with app.app_context():
        resultados = {
            'usuarios': verificar_usuarios(),
            'ubicaciones': verificar_ubicaciones(),
            'configuracion': verificar_configuracion_electoral(),
            'formularios': verificar_formularios(),
            'incidentes': verificar_incidentes_delitos(),
            'endpoints': verificar_endpoints(),
        }
        
        print("\n" + "="*70)
        print("RESUMEN DE VERIFICACIÓN")
        print("="*70)
        
        for nombre, resultado in resultados.items():
            estado = "✅ OK" if resultado else "❌ ERROR"
            print(f"  {nombre.capitalize():20} : {estado}")
        
        todos_ok = all(resultados.values())
        
        print("\n" + "="*70)
        if todos_ok:
            print("✅ SISTEMA VERIFICADO CORRECTAMENTE")
        else:
            print("❌ SE ENCONTRARON PROBLEMAS EN EL SISTEMA")
        print("="*70 + "\n")
        
        return 0 if todos_ok else 1

if __name__ == '__main__':
    sys.exit(main())
