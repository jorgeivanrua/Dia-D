"""
Ruta para inicializar la base de datos manualmente
SOLO PARA DESARROLLO/TESTING
"""
from flask import Blueprint, jsonify
import os
import sys

init_db_bp = Blueprint('init_db', __name__)


@init_db_bp.route('/init-db-manual', methods=['POST'])
def init_db_manual():
    """
    Endpoint para inicializar la BD manualmente
    ⚠️ SOLO USAR EN DESARROLLO O PRIMERA CONFIGURACIÓN
    """
    try:
        # Importar aquí para evitar problemas circulares
        from backend.database import db
        from backend.models.location import Location
        import csv
        
        # Verificar si ya hay datos
        existing_count = Location.query.count()
        if existing_count > 0:
            return jsonify({
                'success': False,
                'error': f'La base de datos ya tiene {existing_count} ubicaciones. Usa /clear-locations primero si quieres recargar.'
            }), 400
        
        # Buscar archivo CSV
        csv_paths = ['divipola.csv', 'todos los datos/divipola.csv', 'data/divipola.csv']
        csv_path = None
        for path in csv_paths:
            if os.path.exists(path):
                csv_path = path
                break
        
        if not csv_path:
            return jsonify({
                'success': False,
                'error': 'No se encontró el archivo divipola.csv'
            }), 404
        
        # Cargar datos
        locations_added = 0
        departamentos = {}
        municipios = {}
        zonas = {}
        puestos = {}
        
        # Departamentos a cargar (configurable vía env DIVIPOLA_DEPARTAMENTOS, default '44')
        deptos_a_cargar = set(
            d.strip().zfill(2) for d in
            os.getenv('DIVIPOLA_DEPARTAMENTOS', '44').replace(',', ' ').split()
            if d.strip()
        )
        if not deptos_a_cargar:
            deptos_a_cargar = {'44'}
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                dd = row['dd'].strip().zfill(2)
                
                # Solo cargar los departamentos configurados
                if dd not in deptos_a_cargar:
                    continue
                
                mm = row['mm'].strip().zfill(2)
                zz = row['zz'].strip().zfill(2)
                pp = row['pp'].strip().zfill(2)
                mesa = row['mesa'].strip().zfill(2)
                
                departamento_nombre = row['departamento'].strip()
                municipio_nombre = row['municipio'].strip()
                puesto_nombre = row['puesto'].strip()
                mesa_nombre = row['mesa_nombre'].strip()
                
                depto_codigo = dd
                muni_codigo = f"{dd}{mm}"
                zona_codigo = f"{dd}{mm}{zz}"
                puesto_codigo = f"{dd}{mm}{zz}{pp}"
                mesa_codigo = f"{dd}{mm}{zz}{pp}{mesa}"
                
                # Departamento
                if dd not in departamentos:
                    dept = Location(
                        departamento_codigo=depto_codigo,
                        departamento_nombre=departamento_nombre,
                        nombre_completo=departamento_nombre,
                        tipo='departamento',
                        activo=True
                    )
                    db.session.add(dept)
                    db.session.flush()
                    departamentos[dd] = dept.id
                    locations_added += 1
                
                # Municipio
                if muni_codigo not in municipios:
                    muni = Location(
                        departamento_codigo=depto_codigo,
                        municipio_codigo=muni_codigo,
                        departamento_nombre=departamento_nombre,
                        municipio_nombre=municipio_nombre,
                        nombre_completo=f"{departamento_nombre} - {municipio_nombre}",
                        tipo='municipio',
                        parent_id=departamentos[dd],
                        activo=True
                    )
                    db.session.add(muni)
                    db.session.flush()
                    municipios[muni_codigo] = muni.id
                    locations_added += 1
                
                # Zona
                if zona_codigo not in zonas:
                    zona = Location(
                        departamento_codigo=depto_codigo,
                        municipio_codigo=muni_codigo,
                        zona_codigo=zona_codigo,
                        departamento_nombre=departamento_nombre,
                        municipio_nombre=municipio_nombre,
                        nombre_completo=f"{departamento_nombre} - {municipio_nombre} - Zona {zz}",
                        tipo='zona',
                        parent_id=municipios[muni_codigo],
                        activo=True
                    )
                    db.session.add(zona)
                    db.session.flush()
                    zonas[zona_codigo] = zona.id
                    locations_added += 1
                
                # Puesto
                if puesto_codigo not in puestos:
                    puesto = Location(
                        departamento_codigo=depto_codigo,
                        municipio_codigo=muni_codigo,
                        zona_codigo=zona_codigo,
                        puesto_codigo=puesto_codigo,
                        departamento_nombre=departamento_nombre,
                        municipio_nombre=municipio_nombre,
                        puesto_nombre=puesto_nombre,
                        nombre_completo=f"{departamento_nombre} - {municipio_nombre} - Zona {zz} - {puesto_nombre}",
                        tipo='puesto',
                        direccion=row.get('direccion', '').strip() or None,
                        comuna=row.get('comuna', '').strip() or None,
                        latitud=float(row['LATITUD']) if row.get('LATITUD', '').strip() else None,
                        longitud=float(row['LONGITUD']) if row.get('LONGITUD', '').strip() else None,
                        parent_id=zonas[zona_codigo],
                        activo=True
                    )
                    db.session.add(puesto)
                    db.session.flush()
                    puestos[puesto_codigo] = puesto.id
                    locations_added += 1
                
                # Mesa
                mesa_location = Location(
                    departamento_codigo=depto_codigo,
                    municipio_codigo=muni_codigo,
                    zona_codigo=zona_codigo,
                    puesto_codigo=puesto_codigo,
                    mesa_codigo=mesa_codigo,
                    departamento_nombre=departamento_nombre,
                    municipio_nombre=municipio_nombre,
                    puesto_nombre=puesto_nombre,
                    mesa_nombre=mesa_nombre,
                    nombre_completo=f"{departamento_nombre} - {municipio_nombre} - Zona {zz} - {puesto_nombre} - Mesa {mesa}",
                    tipo='mesa',
                    total_votantes_registrados=int(row.get('total_mesa', 0) or 0),
                    mujeres=int(row.get('mujeres_mesa', 0) or 0),
                    hombres=int(row.get('hombres_mesa', 0) or 0),
                    direccion=row.get('direccion', '').strip() or None,
                    comuna=row.get('comuna', '').strip() or None,
                    latitud=float(row['LATITUD']) if row.get('LATITUD', '').strip() else None,
                    longitud=float(row['LONGITUD']) if row.get('LONGITUD', '').strip() else None,
                    parent_id=puestos[puesto_codigo],
                    activo=True
                )
                db.session.add(mesa_location)
                locations_added += 1
                
                if locations_added % 100 == 0:
                    db.session.commit()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Datos cargados exitosamente',
            'data': {
                'total_locations': locations_added,
                'departamentos': len(departamentos),
                'municipios': len(municipios),
                'zonas': len(zonas),
                'puestos': len(puestos),
                'mesas': locations_added - len(departamentos) - len(municipios) - len(zonas) - len(puestos)
            }
        }), 200
        
    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@init_db_bp.route('/clear-locations', methods=['POST'])
def clear_locations():
    """
    Limpiar todas las ubicaciones
    ⚠️ USAR CON CUIDADO
    """
    try:
        from backend.database import db
        from backend.models.location import Location
        
        count = Location.query.count()
        Location.query.delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{count} ubicaciones eliminadas'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@init_db_bp.route('/check-locations', methods=['GET'])
def check_locations():
    """
    Verificar cuántas ubicaciones hay en la BD
    """
    try:
        from backend.database import db
        from backend.models.location import Location
        
        total = Location.query.count()
        departamentos = Location.query.filter_by(tipo='departamento').count()
        municipios = Location.query.filter_by(tipo='municipio').count()
        zonas = Location.query.filter_by(tipo='zona').count()
        puestos = Location.query.filter_by(tipo='puesto').count()
        mesas = Location.query.filter_by(tipo='mesa').count()
        
        # Obtener el departamento de Caquetá
        caqueta = Location.query.filter_by(
            tipo='departamento',
            departamento_codigo='44'
        ).first()
        
        return jsonify({
            'success': True,
            'data': {
                'total': total,
                'departamentos': departamentos,
                'municipios': municipios,
                'zonas': zonas,
                'puestos': puestos,
                'mesas': mesas,
                'caqueta_exists': caqueta is not None,
                'caqueta_data': {
                    'codigo': caqueta.departamento_codigo,
                    'nombre': caqueta.departamento_nombre
                } if caqueta else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
