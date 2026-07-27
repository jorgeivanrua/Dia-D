"""
Actualizar coordenadas de TODOS los puestos desde DIVIPOLA
Versión mejorada que usa la clave completa
"""
import csv
from backend.app import create_app
from backend.models.location import Location
from backend.database import db

app = create_app()

with app.app_context():
    print("Actualizando coordenadas de puestos desde DIVIPOLA (v2)...")
    
    # Leer CSV y agrupar por puesto
    puestos_coords = {}
    
    with open('data/divipola.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            dd = row['dd']
            mm = row['mm']
            zz = row['zz']
            pp = row['pp']
            
            # Solo Caquetá (código 44)
            if dd != '44':
                continue
            
            # Clave única por puesto
            puesto_key = f"{dd}{mm}{zz}{pp}"
            
            # Solo guardar el primer registro de cada puesto (todos tienen las mismas coordenadas)
            if puesto_key not in puestos_coords:
                try:
                    lat = float(row['LATITUD'])
                    lon = float(row['LONGITUD'])
                    
                    if lat != 0 and lon != 0:
                        puestos_coords[puesto_key] = {
                            'departamento_codigo': dd,
                            'municipio_codigo': mm,
                            'zona_codigo': zz,
                            'puesto_codigo': pp,
                            'latitud': lat,
                            'longitud': lon,
                            'direccion': row.get('direccion', ''),
                            'comuna': row.get('comuna', '')
                        }
                except (ValueError, KeyError) as e:
                    print(f"Error procesando {puesto_key}: {e}")
                    continue
    
    print(f"Puestos con coordenadas en CSV: {len(puestos_coords)}")
    
    # Actualizar en la base de datos usando la clave completa
    puestos_actualizados = 0
    puestos_no_encontrados = 0
    
    for puesto_key, coords in puestos_coords.items():
        # Buscar puesto en la BD usando todos los códigos
        puesto = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo=coords['departamento_codigo'],
            municipio_codigo=coords['municipio_codigo'],
            zona_codigo=coords['zona_codigo'],
            puesto_codigo=coords['puesto_codigo']
        ).first()
        
        if puesto:
            puesto.latitud = coords['latitud']
            puesto.longitud = coords['longitud']
            
            # Actualizar dirección y comuna si no existen
            if coords['direccion'] and not puesto.direccion:
                puesto.direccion = coords['direccion']
            if coords['comuna'] and not puesto.comuna:
                puesto.comuna = coords['comuna']
            
            puestos_actualizados += 1
            
            if puestos_actualizados % 10 == 0:
                print(f"  Actualizados: {puestos_actualizados}...")
        else:
            puestos_no_encontrados += 1
            print(f"  No encontrado: {puesto_key} ({coords['departamento_codigo']}-{coords['municipio_codigo']}-{coords['zona_codigo']}-{coords['puesto_codigo']})")
    
    db.session.commit()
    
    print(f"\n✓ Puestos actualizados: {puestos_actualizados}")
    print(f"✗ Puestos no encontrados en BD: {puestos_no_encontrados}")
    
    # Verificar resultado final
    puestos_con_coords = Location.query.filter(
        Location.tipo == 'puesto',
        Location.departamento_codigo == '44',
        Location.latitud.isnot(None)
    ).count()
    
    puestos_total = Location.query.filter_by(
        tipo='puesto',
        departamento_codigo='44'
    ).count()
    
    print(f"\nTotal puestos en BD: {puestos_total}")
    print(f"Puestos con coordenadas: {puestos_con_coords}")
    print(f"Porcentaje: {round(puestos_con_coords/puestos_total*100, 1)}%")
