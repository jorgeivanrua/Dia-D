"""
Actualizar coordenadas de puestos desde DIVIPOLA
"""
import csv
from backend.app import create_app
from backend.models.location import Location
from backend.database import db

app = create_app()

with app.app_context():
    print("Actualizando coordenadas de puestos desde DIVIPOLA...")
    
    # Leer CSV
    puestos_actualizados = 0
    puestos_sin_coordenadas = 0
    
    with open('data/divipola.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # Agrupar por puesto (dd, mm, zz, pp)
        puestos_coords = {}
        
        for row in reader:
            dd = row['dd']
            mm = row['mm']
            zz = row['zz']
            pp = row['pp']
            
            # Solo Caquetá (código 44)
            if dd != '44':
                continue
            
            puesto_key = f"{dd}{mm}{zz}{pp}"
            
            # Obtener coordenadas
            try:
                lat = float(row['LATITUD'])
                lon = float(row['LONGITUD'])
                
                if lat != 0 and lon != 0:
                    puestos_coords[puesto_key] = {
                        'latitud': lat,
                        'longitud': lon,
                        'direccion': row.get('direccion', ''),
                        'comuna': row.get('comuna', '')
                    }
            except (ValueError, KeyError):
                continue
    
    print(f"Puestos con coordenadas en CSV: {len(puestos_coords)}")
    
    # Actualizar en la base de datos
    for puesto_codigo, coords in puestos_coords.items():
        # Buscar puesto en la BD
        puesto = Location.query.filter_by(
            tipo='puesto',
            puesto_codigo=puesto_codigo[-2:]  # Últimos 2 dígitos
        ).filter(
            Location.departamento_codigo == '44'
        ).first()
        
        if puesto:
            puesto.latitud = coords['latitud']
            puesto.longitud = coords['longitud']
            if coords['direccion'] and not puesto.direccion:
                puesto.direccion = coords['direccion']
            if coords['comuna'] and not puesto.comuna:
                puesto.comuna = coords['comuna']
            
            puestos_actualizados += 1
        else:
            puestos_sin_coordenadas += 1
    
    db.session.commit()
    
    print(f"✓ Puestos actualizados: {puestos_actualizados}")
    print(f"✗ Puestos no encontrados en BD: {puestos_sin_coordenadas}")
    
    # Verificar
    puestos_con_coords = Location.query.filter(
        Location.tipo == 'puesto',
        Location.latitud.isnot(None)
    ).count()
    
    print(f"\nTotal puestos con coordenadas en BD: {puestos_con_coords}")
