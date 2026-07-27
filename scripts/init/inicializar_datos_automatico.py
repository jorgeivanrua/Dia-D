#!/usr/bin/env python3
"""
Script para inicializar automáticamente todos los datos necesarios
Ejecutar: python scripts/inicializar_datos_automatico.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.models.partido_politico import PartidoPolitico as Partido
from backend.models.candidato import Candidato
from backend.models.configuracion_electoral import TipoEleccion
from datetime import datetime

def cargar_divipola_basico():
    """Cargar datos DIVIPOLA básicos"""
    print("\n📍 Cargando datos DIVIPOLA...")
    
    # Verificar si ya existen
    if Location.query.count() > 0:
        print("   ✅ DIVIPOLA ya cargado")
        return True
    
    # Cargar departamentos básicos
    departamentos = [
        {'codigo': '05', 'nombre': 'Antioquia'},
        {'codigo': '08', 'nombre': 'Atlántico'},
        {'codigo': '11', 'nombre': 'Bogotá D.C.'},
        {'codigo': '13', 'nombre': 'Bolívar'},
        {'codigo': '15', 'nombre': 'Boyacá'},
        {'codigo': '17', 'nombre': 'Caldas'},
        {'codigo': '19', 'nombre': 'Cauca'},
        {'codigo': '23', 'nombre': 'Córdoba'},
        {'codigo': '25', 'nombre': 'Cundinamarca'},
        {'codigo': '27', 'nombre': 'Chocó'},
        {'codigo': '41', 'nombre': 'Huila'},
        {'codigo': '44', 'nombre': 'La Guajira'},
        {'codigo': '47', 'nombre': 'Magdalena'},
        {'codigo': '50', 'nombre': 'Meta'},
        {'codigo': '52', 'nombre': 'Nariño'},
        {'codigo': '54', 'nombre': 'Norte de Santander'},
        {'codigo': '63', 'nombre': 'Quindío'},
        {'codigo': '66', 'nombre': 'Risaralda'},
        {'codigo': '68', 'nombre': 'Santander'},
        {'codigo': '70', 'nombre': 'Sucre'},
        {'codigo': '73', 'nombre': 'Tolima'},
        {'codigo': '76', 'nombre': 'Valle del Cauca'},
    ]
    
    for dept in departamentos:
        location = Location(
            departamento_codigo=dept['codigo'],
            departamento_nombre=dept['nombre'],
            nombre_completo=dept['nombre'],
            tipo='departamento',
            activo=True
        )
        db.session.add(location)
    
    db.session.commit()
    print(f"   ✅ Cargados {len(departamentos)} departamentos")
    return True

def cargar_partidos_basicos():
    """Cargar partidos políticos básicos"""
    print("\n🎨 Cargando partidos políticos...")
    
    # Verificar si ya existen
    if Partido.query.count() > 0:
        print("   ✅ Partidos ya cargados")
        return True
    
    partidos = [
        {'codigo': 'PACTO', 'nombre': 'Pacto Histórico', 'nombre_corto': 'PACTO', 'color': '#FF0000', 'orden': 1},
        {'codigo': 'LIBERAL', 'nombre': 'Partido Liberal', 'nombre_corto': 'LIBERAL', 'color': '#FF0000', 'orden': 2},
        {'codigo': 'CONSERVADOR', 'nombre': 'Partido Conservador', 'nombre_corto': 'CONSERVADOR', 'color': '#0000FF', 'orden': 3},
        {'codigo': 'VERDE', 'nombre': 'Alianza Verde', 'nombre_corto': 'VERDE', 'color': '#00FF00', 'orden': 4},
        {'codigo': 'CENTRO_DEM', 'nombre': 'Centro Democrático', 'nombre_corto': 'CENTRO DEM', 'color': '#0080FF', 'orden': 5},
        {'codigo': 'CAMBIO_RADICAL', 'nombre': 'Cambio Radical', 'nombre_corto': 'C. RADICAL', 'color': '#FFA500', 'orden': 6},
        {'codigo': 'U', 'nombre': 'Partido de la U', 'nombre_corto': 'LA U', 'color': '#FFFF00', 'orden': 7},
        {'codigo': 'MIRA', 'nombre': 'MIRA', 'nombre_corto': 'MIRA', 'color': '#800080', 'orden': 8},
        {'codigo': 'OTROS', 'nombre': 'Otros Partidos', 'nombre_corto': 'OTROS', 'color': '#808080', 'orden': 99},
    ]
    
    for p in partidos:
        # PartidoPolitico model uses 'sigla' instead of 'codigo' and has no 'nombre_corto'
        partido = Partido(
            sigla=p['codigo'],
            nombre=p['nombre'],
            color=p['color'],
            activo=True,
            orden=p['orden']
        )
        db.session.add(partido)
    
    db.session.commit()
    print(f"   ✅ Cargados {len(partidos)} partidos")
    return True

def cargar_tipos_eleccion():
    """Cargar tipos de elección"""
    print("\n🗳️  Cargando tipos de elección...")
    
    # Verificar si ya existen
    if TipoEleccion.query.count() > 0:
        print("   ✅ Tipos de elección ya cargados")
        return True
    
    # Ajustado para RN testing y diagnóstico: solo tipos locales/territoriales
    tipos = [
        {'codigo': 'GOBERNACION', 'nombre': 'Gobernación', 'orden': 1},
        {'codigo': 'ASAMBLEA', 'nombre': 'Asamblea Departamental', 'orden': 2},
        {'codigo': 'ALCALDIA', 'nombre': 'Alcaldía', 'orden': 3},
        {'codigo': 'CONCEJO', 'nombre': 'Concejo Municipal', 'orden': 4},
        {'codigo': 'EDIL', 'nombre': 'Ediles / Juntas Locales', 'orden': 5},
    ]
    
    for t in tipos:
        tipo = TipoEleccion(
            codigo=t['codigo'],
            nombre=t['nombre'],
            activo=True,
            orden=t['orden']
        )
        db.session.add(tipo)
    
    db.session.commit()
    print(f"   ✅ Cargados {len(tipos)} tipos de elección")
    return True

def cargar_candidatos_basicos():
    """Cargar candidatos básicos"""
    print("\n👤 Cargando candidatos...")
    
    # Conteo actual de candidatos (se usará para actualizaciones/creaciones)
    existing = Candidato.query.count()
    
    # Obtener todos los partidos registrados
    partidos = Partido.query.order_by(Partido.orden).all()
    tipos = {
        'GOBERNACION': TipoEleccion.query.filter_by(codigo='GOBERNACION').first(),
        'ASAMBLEA': TipoEleccion.query.filter_by(codigo='ASAMBLEA').first(),
        'ALCALDIA': TipoEleccion.query.filter_by(codigo='ALCALDIA').first(),
        'CONCEJO': TipoEleccion.query.filter_by(codigo='CONCEJO').first(),
        'EDIL': TipoEleccion.query.filter_by(codigo='EDIL').first(),
    }

    if not partidos or not all(tipos.values()):
        print("   ⚠️  Faltan partidos o tipos de elección (asegúrate de cargar partidos y tipos primero)")
        return False

    # Mapear cargo por tipo
    cargo_map = {
        'GOBERNACION': 'Gobernador',
        'ASAMBLEA': 'Asambleísta',
        'ALCALDIA': 'Alcalde',
        'CONCEJO': 'Concejal',
        'EDIL': 'Edil',
    }

    # Definir 20 nombres únicos para testing/diagnóstico
    unique_names = [
        'Alejandro Rojas', 'Beatriz Morales', 'Camilo Torres', 'Daniela Vásquez',
        'Eduardo Peña', 'Fabiana Gómez', 'Gabriel Suárez', 'Helena Ortiz',
        'Ignacio Castro', 'Juliana Ramírez', 'Kevin Duarte', 'Laura Medina',
        'Mario Paredes', 'Natalia Serrano', 'Óscar Molina', 'Patricia León',
        'Quintín Herrera', 'Rocío Fernández', 'Samuel Bravo', 'Tamara Aguilar'
    ]

    total_candidates = len(unique_names)
    tipo_keys = list(tipos.keys())
    num_types = len(tipo_keys)
    partido_count = len(partidos)

    # Obtener candidatos existentes ordenados
    existing_candidates = Candidato.query.order_by(Candidato.id).all()
    updated = 0
    created = 0

    # Actualizar los primeros N candidatos para que tengan nombres únicos y datos consistentes
    for i in range(total_candidates):
        name = unique_names[i]
        tipo_key = tipo_keys[i % num_types]
        tipo = tipos[tipo_key]
        partido = partidos[i % partido_count]
        cargo = cargo_map[tipo_key]
        numero_lista = i + 1
        codigo = f"{tipo_key[:3]}-{i+1}-{partido.sigla}"

        if i < len(existing_candidates):
            c = existing_candidates[i]
            c.codigo = codigo
            c.nombre_completo = name
            c.partido_id = partido.id
            c.tipo_eleccion_id = tipo.id
            c.cargo = cargo
            c.numero_lista = numero_lista
            c.activo = True
            updated += 1
        else:
            c = Candidato(
                codigo=codigo,
                nombre_completo=name,
                partido_id=partido.id,
                tipo_eleccion_id=tipo.id,
                cargo=cargo,
                numero_lista=numero_lista,
                activo=True
            )
            db.session.add(c)
            created += 1

    if updated > 0 or created > 0:
        db.session.commit()

    print(f"   ✅ Actualizados {updated} y creados {created} candidatos (total ahora {Candidato.query.count()})")
    return True

def cargar_usuarios_basicos():
    """Cargar usuarios básicos del sistema"""
    print("\n👥 Cargando usuarios del sistema...")
    
    # Verificar si ya existen
    if User.query.count() > 0:
        print("   ✅ Usuarios ya cargados")
        return True
    
    usuarios = [
        {'nombre': 'monitoreo', 'rol': 'monitoreo', 'password': 'Monitoreo2025!'},
        {'nombre': 'auditor', 'rol': 'auditor_electoral', 'password': 'test123'},
        {'nombre': 'coord_dept', 'rol': 'coordinador_departamental', 'password': 'test123'},
        {'nombre': 'coord_mun', 'rol': 'coordinador_municipal', 'password': 'test123'},
        {'nombre': 'coord_puesto', 'rol': 'coordinador_puesto', 'password': 'test123'},
        {'nombre': 'testigo1', 'rol': 'testigo_electoral', 'password': 'test123'},
    ]
    
    for u in usuarios:
        user = User(
            nombre=u['nombre'],
            rol=u['rol'],
            activo=True
        )
        user.set_password(u['password'])
        db.session.add(user)
    
    db.session.commit()
    print(f"   ✅ Cargados {len(usuarios)} usuarios")
    return True

def main():
    print("\n" + "="*70)
    print("INICIALIZACIÓN AUTOMÁTICA DE DATOS")
    print("="*70)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Cargar datos en orden
            resultados = {
                'divipola': cargar_divipola_basico(),
                'tipos_eleccion': cargar_tipos_eleccion(),
                'partidos': cargar_partidos_basicos(),
                'candidatos': cargar_candidatos_basicos(),
                'usuarios': cargar_usuarios_basicos(),
            }
            
            print("\n" + "="*70)
            print("RESUMEN DE INICIALIZACIÓN")
            print("="*70)
            
            print("\n📊 Estado:")
            for nombre, estado in resultados.items():
                icono = "✅" if estado else "❌"
                print(f"  {icono} {nombre.capitalize()}: {'OK' if estado else 'ERROR'}")
            
            todos_ok = all(resultados.values())
            
            if todos_ok:
                print("\n🎉 ¡TODOS LOS DATOS INICIALIZADOS CORRECTAMENTE!")
                print("\n📝 Credenciales de acceso:")
                print("   Monitoreo: monitoreo / Monitoreo2025!")
                print("   Otros: [usuario] / test123")
            else:
                print("\n⚠️  ALGUNOS DATOS NO SE PUDIERON CARGAR")
            
            print("\n" + "="*70)
            
        except Exception as e:
            print(f"\n❌ Error durante la inicialización: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main()
