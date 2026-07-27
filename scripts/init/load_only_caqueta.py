#!/usr/bin/env python3
"""
Script para cargar solo datos de Caquetá
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.location import Location
import csv

def load_caqueta_only():
    """Cargar solo datos de Caquetá con estructura completa"""
    app = create_app('development')
    
    with app.app_context():
        print("Limpiando datos de ubicaciones...")
        Location.query.delete()
        db.session.commit()
        
        print("Cargando datos de Caqueta...")
        
        # Leer archivo DIVIPOLA
        divipola_file = os.path.join('data', 'divipola.csv')
        
        if not os.path.exists(divipola_file):
            print(f"Error: No se encuentra {divipola_file}")
            return
        
        departamentos_creados = {}
        municipios_creados = {}
        zonas_creadas = {}
        puestos_creados = {}
        mesas_creadas = 0
        
        with open(divipola_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                dept_codigo = row['dd']
                dept_nombre = row['departamento']
                muni_codigo = row['mm']
                muni_nombre = row['municipio']
                zona_codigo = row['zz']
                puesto_codigo = row['pp']
                puesto_nombre = row['puesto']
                mesa_codigo = row['mesa']
                mesa_nombre = row['mesa_nombre']
                
                # Solo procesar Caquetá (código 44)
                if dept_codigo != '44':
                    continue
                
                # Crear departamento si no existe
                if dept_codigo not in departamentos_creados:
                    dept = Location(
                        departamento_codigo=dept_codigo,
                        departamento_nombre=dept_nombre,
                        nombre_completo=dept_nombre,
                        tipo='departamento',
                        activo=True
                    )
                    db.session.add(dept)
                    db.session.flush()
                    departamentos_creados[dept_codigo] = dept
                    print(f"  Departamento: {dept_nombre}")
                
                # Crear municipio si no existe
                muni_key = f"{dept_codigo}-{muni_codigo}"
                if muni_key not in municipios_creados:
                    dept = departamentos_creados[dept_codigo]
                    municipio = Location(
                        departamento_codigo=dept_codigo,
                        municipio_codigo=muni_codigo,
                        departamento_nombre=dept_nombre,
                        municipio_nombre=muni_nombre,
                        nombre_completo=f"{dept_nombre} - {muni_nombre}",
                        tipo='municipio',
                        parent_id=dept.id,
                        activo=True
                    )
                    db.session.add(municipio)
                    db.session.flush()
                    municipios_creados[muni_key] = municipio
                
                # Crear zona si no existe
                zona_key = f"{dept_codigo}-{muni_codigo}-{zona_codigo}"
                if zona_key not in zonas_creadas:
                    municipio = municipios_creados[muni_key]
                    zona = Location(
                        departamento_codigo=dept_codigo,
                        municipio_codigo=muni_codigo,
                        zona_codigo=zona_codigo,
                        departamento_nombre=dept_nombre,
                        municipio_nombre=muni_nombre,
                        nombre_completo=f"{dept_nombre} - {muni_nombre} - Zona {zona_codigo}",
                        tipo='zona',
                        parent_id=municipio.id,
                        activo=True
                    )
                    db.session.add(zona)
                    db.session.flush()
                    zonas_creadas[zona_key] = zona
                
                # Crear puesto si no existe
                puesto_key = f"{dept_codigo}-{muni_codigo}-{zona_codigo}-{puesto_codigo}"
                if puesto_key not in puestos_creados:
                    zona = zonas_creadas[zona_key]
                    puesto = Location(
                        departamento_codigo=dept_codigo,
                        municipio_codigo=muni_codigo,
                        zona_codigo=zona_codigo,
                        puesto_codigo=puesto_codigo,
                        departamento_nombre=dept_nombre,
                        municipio_nombre=muni_nombre,
                        puesto_nombre=puesto_nombre,
                        nombre_completo=f"{dept_nombre} - {muni_nombre} - {puesto_nombre}",
                        tipo='puesto',
                        parent_id=zona.id,
                        activo=True
                    )
                    db.session.add(puesto)
                    db.session.flush()
                    puestos_creados[puesto_key] = puesto
                
                # Crear mesa
                puesto = puestos_creados[puesto_key]
                try:
                    mujeres = int(row.get('mujeres_mesa', 0) or 0)
                    hombres = int(row.get('hombres_mesa', 0) or 0)
                    total = int(row.get('total_mesa', 0) or 0)
                    latitud = float(row.get('LATITUD', 0) or 0)
                    longitud = float(row.get('LONGITUD', 0) or 0)
                except:
                    mujeres = hombres = total = 0
                    latitud = longitud = 0
                
                mesa = Location(
                    departamento_codigo=dept_codigo,
                    municipio_codigo=muni_codigo,
                    zona_codigo=zona_codigo,
                    puesto_codigo=puesto_codigo,
                    mesa_codigo=mesa_codigo,
                    departamento_nombre=dept_nombre,
                    municipio_nombre=muni_nombre,
                    puesto_nombre=puesto_nombre,
                    mesa_nombre=mesa_nombre,
                    nombre_completo=f"{dept_nombre} - {muni_nombre} - {puesto_nombre} - {mesa_nombre}",
                    tipo='mesa',
                    parent_id=puesto.id,
                    mujeres=mujeres,
                    hombres=hombres,
                    total_votantes_registrados=total,
                    comuna=row.get('comuna', ''),
                    direccion=row.get('direccion', ''),
                    latitud=latitud,
                    longitud=longitud,
                    activo=True
                )
                db.session.add(mesa)
                mesas_creadas += 1
                
                # Commit cada 100 mesas para evitar problemas de memoria
                if mesas_creadas % 100 == 0:
                    db.session.commit()
                    print(f"  Procesadas {mesas_creadas} mesas...")
        
        db.session.commit()
        
        # Mostrar resumen
        total_dept = Location.query.filter_by(tipo='departamento').count()
        total_muni = Location.query.filter_by(tipo='municipio').count()
        total_zonas = Location.query.filter_by(tipo='zona').count()
        total_puestos = Location.query.filter_by(tipo='puesto').count()
        total_mesas = Location.query.filter_by(tipo='mesa').count()
        
        print(f"\nResumen final:")
        print(f"   - Departamentos: {total_dept}")
        print(f"   - Municipios: {total_muni}")
        print(f"   - Zonas: {total_zonas}")
        print(f"   - Puestos: {total_puestos}")
        print(f"   - Mesas: {total_mesas}")
        print(f"\nBase de datos lista con Caqueta completo")

if __name__ == '__main__':
    load_caqueta_only()
