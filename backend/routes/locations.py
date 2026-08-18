"""
Rutas de Ubicaciones (DIVIPOLA) - Accesible para todos
Endpoints públicos necesarios para el proceso de login
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, jwt_required, get_jwt_identity
from functools import wraps
from backend.database import db
from backend.models.location import Location

locations_bp = Blueprint('locations', __name__)


def _auto_load_divipola():
    """
    Cargar datos de DIVIPOLA automáticamente si la BD está vacía
    """
    import os
    import csv
    
    try:
        # Verificar si ya hay datos
        total_locations = Location.query.count()
        if total_locations > 0:
            print(f"[AUTO-LOAD] BD ya tiene {total_locations} ubicaciones, omitiendo carga")
            return True
        
        print("[AUTO-LOAD] BD vacía, cargando DIVIPOLA automáticamente...")
        
        # Buscar archivo CSV
        csv_paths = ['divipola.csv', 'todos los datos/divipola.csv', 'data/divipola.csv']
        csv_path = None
        for path in csv_paths:
            if os.path.exists(path):
                csv_path = path
                break
        
        if not csv_path:
            print("[AUTO-LOAD] ERROR: No se encontró divipola.csv")
            return False
        
        print(f"[AUTO-LOAD] Cargando desde: {csv_path}")
        
        # Departamentos a cargar (configurable vía env DIVIPOLA_DEPARTAMENTOS, default '44')
        deptos_a_cargar = set(
            d.strip().zfill(2) for d in
            os.getenv('DIVIPOLA_DEPARTAMENTOS', '44').replace(',', ' ').split()
            if d.strip()
        )
        if not deptos_a_cargar:
            deptos_a_cargar = {'44'}
        print(f"[AUTO-LOAD] Departamentos a cargar: {sorted(deptos_a_cargar)}")
        
        # Cargar datos
        locations_added = 0
        departamentos = {}
        municipios = {}
        zonas = {}
        puestos = {}
        
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
        
        print(f"[AUTO-LOAD] ✅ Carga completada: {locations_added} ubicaciones")
        print(f"[AUTO-LOAD]   - Departamentos: {len(departamentos)}")
        print(f"[AUTO-LOAD]   - Municipios: {len(municipios)}")
        print(f"[AUTO-LOAD]   - Zonas: {len(zonas)}")
        print(f"[AUTO-LOAD]   - Puestos: {len(puestos)}")
        
        return True
        
    except Exception as e:
        import traceback
        print(f"[AUTO-LOAD] ❌ Error: {str(e)}")
        print(f"[AUTO-LOAD] Traceback: {traceback.format_exc()}")
        db.session.rollback()
        return False


def _auto_create_users():
    """
    Crear usuarios automáticamente si no existen
    """
    from backend.models.user import User
    
    try:
        # Verificar si ya hay usuarios
        total_users = User.query.count()
        if total_users > 0:
            print(f"[AUTO-USERS] Ya existen {total_users} usuarios, omitiendo creación")
            return True
        
        print("[AUTO-USERS] No hay usuarios, creando usuarios de prueba...")
        
        # Obtener ubicaciones necesarias
        caqueta = Location.query.filter_by(
            tipo='departamento',
            departamento_codigo='44'
        ).first()
        
        florencia = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo='44',
            municipio_codigo='4401'
        ).first()
        
        # Obtener algunos puestos para testigos y coordinadores
        puestos = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo='44',
            municipio_codigo='4401'
        ).limit(3).all()
        
        if not caqueta or not florencia:
            print("[AUTO-USERS] ERROR: No se encontraron ubicaciones necesarias")
            return False
        
        # Crear usuarios de prueba
        usuarios = [
            # Super Admin - Contraseña fija admin123
            {
                'nombre': 'admin',
                'rol': 'super_admin',
                'ubicacion_id': None,
                'password': 'admin123'
            },
            # Administradores
            {
                'nombre': 'admin_caqueta',
                'rol': 'admin_departamental',
                'ubicacion_id': caqueta.id,
                'password': 'test123'
            },
            {
                'nombre': 'admin_florencia',
                'rol': 'admin_municipal',
                'ubicacion_id': florencia.id,
                'password': 'test123'
            },
            # Coordinadores
            {
                'nombre': 'coord_dpto',
                'rol': 'coordinador_departamental',
                'ubicacion_id': caqueta.id,
                'password': 'test123'
            },
            {
                'nombre': 'coord_muni',
                'rol': 'coordinador_municipal',
                'ubicacion_id': florencia.id,
                'password': 'test123'
            },
            # Auditor
            {
                'nombre': 'auditor',
                'rol': 'auditor_electoral',
                'ubicacion_id': caqueta.id,
                'password': 'test123'
            },
            # Monitoreo
            {
                'nombre': 'monitoreo',
                'rol': 'monitoreo',
                'ubicacion_id': None,
                'password': 'test123'
            }
        ]
        
        # Agregar coordinadores de puesto y testigos
        for i, puesto in enumerate(puestos, 1):
            # Coordinador de puesto
            usuarios.append({
                'nombre': f'coord_puesto_{i}',
                'rol': 'coordinador_puesto',
                'ubicacion_id': puesto.id,
                'password': 'test123'
            })
            # Testigos (2 por puesto)
            usuarios.append({
                'nombre': f'testigo_{i}_1',
                'rol': 'testigo_electoral',
                'ubicacion_id': puesto.id,
                'password': 'test123'
            })
            usuarios.append({
                'nombre': f'testigo_{i}_2',
                'rol': 'testigo_electoral',
                'ubicacion_id': puesto.id,
                'password': 'test123'
            })
        
        for user_data in usuarios:
            user = User(
                nombre=user_data['nombre'],
                rol=user_data['rol'],
                ubicacion_id=user_data['ubicacion_id'],
                activo=True
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            print(f"[AUTO-USERS] Creado: {user_data['nombre']} ({user_data['rol']})")
        
        db.session.commit()
        print(f"[AUTO-USERS] ✅ {len(usuarios)} usuarios creados")
        return True
        
    except Exception as e:
        import traceback
        print(f"[AUTO-USERS] ❌ Error: {str(e)}")
        print(f"[AUTO-USERS] Traceback: {traceback.format_exc()}")
        db.session.rollback()
        return False


def _auto_load_partidos_candidatos():
    """
    Cargar partidos y candidatos automáticamente si no existen
    """
    from backend.models.partido_politico import PartidoPolitico as Partido
    from backend.models.candidato import Candidato
    from backend.models.configuracion_electoral import TipoEleccion
    
    try:
        # Verificar si ya hay partidos
        total_partidos = Partido.query.count()
        if total_partidos > 0:
            print(f"[AUTO-PARTIDOS] Ya existen {total_partidos} partidos, omitiendo carga")
            return True
        
        print("[AUTO-PARTIDOS] No hay partidos, cargando datos electorales...")
        
        # Crear tipos de elección
        tipos_eleccion = [
            {'codigo': 'SENADO', 'nombre': 'Senado de la República', 'descripcion': 'Elección para Senadores', 'activo': True},
            {'codigo': 'CAMARA', 'nombre': 'Cámara de Representantes', 'descripcion': 'Elección para Representantes', 'activo': True}
        ]
        
        tipos_creados = {}
        for tipo_data in tipos_eleccion:
            tipo = TipoEleccion(**tipo_data)
            db.session.add(tipo)
            db.session.flush()
            tipos_creados[tipo_data['codigo']] = tipo
            print(f"[AUTO-PARTIDOS] Tipo: {tipo_data['nombre']}")
        
        # Crear partidos con logos
        partidos_data = [
            {'codigo': 'LIBERAL', 'nombre': 'Partido Liberal Colombiano', 'sigla': 'PLC', 'color': '#FF0000', 
             'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Partido_Liberal_Colombiano_logo.svg/200px-Partido_Liberal_Colombiano_logo.svg.png', 'activo': True},
            {'codigo': 'CONSERVADOR', 'nombre': 'Partido Conservador Colombiano', 'sigla': 'PCC', 'color': '#0000FF',
             'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Partido_Conservador_Colombiano_logo.svg/200px-Partido_Conservador_Colombiano_logo.svg.png', 'activo': True},
            {'codigo': 'PACTO', 'nombre': 'Pacto Histórico', 'sigla': 'PH', 'color': '#FF1493',
             'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Pacto_Hist%C3%B3rico_logo.svg/200px-Pacto_Hist%C3%B3rico_logo.svg.png', 'activo': True},
            {'codigo': 'CENTRO_DEM', 'nombre': 'Centro Democrático', 'sigla': 'CD', 'color': '#00BFFF',
             'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Centro_Democr%C3%A1tico_logo.svg/200px-Centro_Democr%C3%A1tico_logo.svg.png', 'activo': True},
            {'codigo': 'CAMBIO_RAD', 'nombre': 'Cambio Radical', 'sigla': 'CR', 'color': '#FFD700',
             'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Cambio_Radical_logo.svg/200px-Cambio_Radical_logo.svg.png', 'activo': True},
            {'codigo': 'VERDE', 'nombre': 'Alianza Verde', 'sigla': 'AV', 'color': '#00FF00',
             'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Alianza_Verde_logo.svg/200px-Alianza_Verde_logo.svg.png', 'activo': True},
            {'codigo': 'POLO', 'nombre': 'Polo Democrático Alternativo', 'sigla': 'PDA', 'color': '#FFD700',
             'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Polo_Democr%C3%A1tico_Alternativo_logo.svg/200px-Polo_Democr%C3%A1tico_Alternativo_logo.svg.png', 'activo': True},
            {'codigo': 'MIRA', 'nombre': 'MIRA', 'sigla': 'MIRA', 'color': '#800080',
             'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/MIRA_logo.svg/200px-MIRA_logo.svg.png', 'activo': True},
            {'codigo': 'U', 'nombre': 'Partido de la U', 'sigla': 'U', 'color': '#FFA500',
             'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Partido_de_la_U_logo.svg/200px-Partido_de_la_U_logo.svg.png', 'activo': True},
            {'codigo': 'COMUNES', 'nombre': 'Comunes', 'sigla': 'COMUNES', 'color': '#DC143C',
             'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Comunes_logo.svg/200px-Comunes_logo.svg.png', 'activo': True},
            {'codigo': 'VOTO_BLANCO', 'nombre': 'Voto en Blanco', 'sigla': 'BLANCO', 'color': '#CCCCCC', 'logo_url': None, 'activo': True}
        ]
        
        partidos_creados = {}
        for partido_data in partidos_data:
            partido = Partido(**partido_data)
            db.session.add(partido)
            db.session.flush()
            partidos_creados[partido_data['codigo']] = partido
            print(f"[AUTO-PARTIDOS] Partido: {partido_data['sigla']}")
        
        # Crear candidatos por listas (más realista)
        candidatos_data = [
            # ========== SENADO - LISTAS COMPLETAS ==========
            
            # PACTO HISTÓRICO - Lista Senado (5 candidatos)
            {'nombre': 'Gustavo Bolívar', 'partido': 'PACTO', 'tipo': 'SENADO', 'numero_lista': 1},
            {'nombre': 'María José Pizarro', 'partido': 'PACTO', 'tipo': 'SENADO', 'numero_lista': 2},
            {'nombre': 'Iván Cepeda', 'partido': 'PACTO', 'tipo': 'SENADO', 'numero_lista': 3},
            {'nombre': 'María Fernanda Cabal', 'partido': 'CENTRO_DEM', 'tipo': 'SENADO', 'numero_lista': 3},
            {'nombre': 'Angélica Lozano', 'partido': 'VERDE', 'tipo': 'SENADO', 'numero_lista': 1},
            {'nombre': 'Ariel Ávila', 'partido': 'VERDE', 'tipo': 'SENADO', 'numero_lista': 2},
            {'nombre': 'Efraín Cepeda', 'partido': 'CONSERVADOR', 'tipo': 'SENADO', 'numero_lista': 1},
            {'nombre': 'David Barguil', 'partido': 'CONSERVADOR', 'tipo': 'SENADO', 'numero_lista': 2},
            {'nombre': 'Juan Fernando Cristo', 'partido': 'LIBERAL', 'tipo': 'SENADO', 'numero_lista': 1},
            {'nombre': 'Alejandro Gaviria', 'partido': 'LIBERAL', 'tipo': 'SENADO', 'numero_lista': 2},
            {'nombre': 'Germán Varón', 'partido': 'CAMBIO_RAD', 'tipo': 'SENADO', 'numero_lista': 1},
            {'nombre': 'Carlos Fernando Motoa', 'partido': 'CAMBIO_RAD', 'tipo': 'SENADO', 'numero_lista': 2},
            
            # CÁMARA - CAQUETÁ
            {'nombre': 'Hernán Banguero', 'partido': 'LIBERAL', 'tipo': 'CAMARA', 'numero_lista': 1, 'depto': '44'},
            {'nombre': 'Deisy Gómez', 'partido': 'LIBERAL', 'tipo': 'CAMARA', 'numero_lista': 2, 'depto': '44'},
            {'nombre': 'Carlos Ramírez', 'partido': 'CONSERVADOR', 'tipo': 'CAMARA', 'numero_lista': 1, 'depto': '44'},
            {'nombre': 'Martha Villalba', 'partido': 'CONSERVADOR', 'tipo': 'CAMARA', 'numero_lista': 2, 'depto': '44'},
            {'nombre': 'Ana María Torres', 'partido': 'PACTO', 'tipo': 'CAMARA', 'numero_lista': 1, 'depto': '44'},
            {'nombre': 'Luis Eduardo Díaz', 'partido': 'PACTO', 'tipo': 'CAMARA', 'numero_lista': 2, 'depto': '44'},
            {'nombre': 'Jorge Enrique Rojas', 'partido': 'CENTRO_DEM', 'tipo': 'CAMARA', 'numero_lista': 1, 'depto': '44'},
            {'nombre': 'Sandra Milena Gutiérrez', 'partido': 'VERDE', 'tipo': 'CAMARA', 'numero_lista': 1, 'depto': '44'},
            {'nombre': 'Pedro Nel Jiménez', 'partido': 'CAMBIO_RAD', 'tipo': 'CAMARA', 'numero_lista': 1, 'depto': '44'},
            {'nombre': 'Gloria Stella Díaz', 'partido': 'U', 'tipo': 'CAMARA', 'numero_lista': 1, 'depto': '44'}
        ]
        
        for cand_data in candidatos_data:
            candidato = Candidato(
                nombre=cand_data['nombre'],
                partido_id=partidos_creados[cand_data['partido']].id,
                tipo_eleccion_id=tipos_creados[cand_data['tipo']].id,
                numero_lista=cand_data['numero_lista'],
                departamento_codigo=cand_data.get('depto'),
                activo=True
            )
            db.session.add(candidato)
        
        db.session.commit()
        print(f"[AUTO-PARTIDOS] ✅ {len(partidos_creados)} partidos y {len(candidatos_data)} candidatos creados")
        return True
        
    except Exception as e:
        import traceback
        print(f"[AUTO-PARTIDOS] ❌ Error: {str(e)}")
        print(f"[AUTO-PARTIDOS] Traceback: {traceback.format_exc()}")
        db.session.rollback()
        return False


@locations_bp.route('/departamentos', methods=['GET'])
def get_departamentos():
    """
    Obtener departamentos cargados en la base de datos
    Endpoint público (necesario para login)

    Returns:
        JSON con lista de departamentos cargados
    """
    try:
        # Verificar si hay datos, si no, cargar automáticamente
        total_locations = Location.query.count()
        if total_locations == 0:
            print("[DEPARTAMENTOS] BD vacía, intentando carga automática...")
            _auto_load_divipola()
            # Crear usuarios después de cargar ubicaciones
            _auto_create_users()
            # Cargar partidos y candidatos
            _auto_load_partidos_candidatos()
        
        # Todos los departamentos cargados en la BD
        departamentos = Location.query.filter_by(
            tipo='departamento',
            activo=True
        ).all()
        
        if departamentos:
            data = [{
                'departamento_codigo': dept.departamento_codigo,
                'departamento_nombre': dept.departamento_nombre
            } for dept in departamentos]
            
            return jsonify({
                'success': True,
                'data': data
            }), 200
        else:
            # Si aún no hay datos después de intentar cargar
            total_deptos = Location.query.filter_by(tipo='departamento').count()
            
            return jsonify({
                'success': False,
                'error': 'No se encontraron departamentos. La base de datos puede estar vacía o el archivo divipola.csv no está disponible.',
                'data': [],
                'debug': {
                    'total_departamentos': total_deptos,
                    'total_locations': Location.query.count()
                }
            }), 404
            
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"[ERROR] Error en get_departamentos: {str(e)}")
        print(f"[ERROR] Traceback: {error_trace}")
        return jsonify({
            'success': False,
            'error': f'Error al obtener departamentos: {str(e)}'
        }), 500


@locations_bp.route('/municipios/<departamento_codigo>', methods=['GET'])
def get_municipios(departamento_codigo):
    """
    Obtener municipios de un departamento
    Endpoint público (necesario para login)
    
    Args:
        departamento_codigo: Código del departamento
        
    Returns:
        JSON con lista de municipios
    """
    try:
        print(f"[MUNICIPIOS] Solicitando municipios para departamento: {departamento_codigo}")
        
        # Obtener municipios activos del departamento
        municipios = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo=departamento_codigo,
            activo=True
        ).order_by(Location.municipio_nombre).all()
        
        print(f"[MUNICIPIOS] Encontrados {len(municipios)} municipios")
        
        if not municipios:
            # Verificar si el departamento existe
            departamento = Location.query.filter_by(
                tipo='departamento',
                departamento_codigo=departamento_codigo
            ).first()
            
            if not departamento:
                return jsonify({
                    'success': False,
                    'error': f'Departamento con código {departamento_codigo} no encontrado',
                    'data': []
                }), 404
            
            return jsonify({
                'success': False,
                'error': f'No se encontraron municipios para {departamento.departamento_nombre}',
                'data': []
            }), 404
        
        return jsonify({
            'success': True,
            'data': [{
                'municipio_codigo': muni.municipio_codigo,
                'municipio_nombre': muni.municipio_nombre
            } for muni in municipios]
        }), 200
        
    except Exception as e:
        import traceback
        print(f"[ERROR] Error en get_municipios: {str(e)}")
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': f'Error al obtener municipios: {str(e)}'
        }), 500


@locations_bp.route('/zonas/<municipio_codigo>', methods=['GET'])
def get_zonas(municipio_codigo):
    """
    Obtener zonas de un municipio
    Endpoint público (necesario para login)
    
    Args:
        municipio_codigo: Código del municipio (ej: '01' para Florencia)
        
    Returns:
        JSON con lista de zonas
    """
    try:
        print(f"[ZONAS] Solicitando zonas para municipio: {municipio_codigo}")
        
        # Obtener zonas activas del municipio
        # Nota: municipio_codigo es solo el código del municipio (ej: '01'), 
        # no incluye el departamento
        zonas = Location.query.filter_by(
            tipo='zona',
            municipio_codigo=municipio_codigo,
            activo=True
        ).order_by(Location.zona_codigo).all()
        
        print(f"[ZONAS] Encontradas {len(zonas)} zonas")
        
        if not zonas:
            # Verificar si el municipio existe
            municipio = Location.query.filter_by(
                tipo='municipio',
                municipio_codigo=municipio_codigo
            ).first()
            
            if not municipio:
                return jsonify({
                    'success': False,
                    'error': f'Municipio con código {municipio_codigo} no encontrado',
                    'data': []
                }), 404
            
            return jsonify({
                'success': False,
                'error': f'No se encontraron zonas para {municipio.municipio_nombre}',
                'data': []
            }), 404
        
        return jsonify({
            'success': True,
            'data': [{
                'zona_codigo': zona.zona_codigo,
                'zona_nombre': f"Zona {zona.zona_codigo}"
            } for zona in zonas]
        }), 200
        
    except Exception as e:
        import traceback
        print(f"[ERROR] Error en get_zonas: {str(e)}")
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': f'Error al obtener zonas: {str(e)}'
        }), 500


@locations_bp.route('/puestos/<zona_codigo>', methods=['GET'])
def get_puestos(zona_codigo):
    """
    Obtener puestos de una zona
    Endpoint público (necesario para login)
    
    Args:
        zona_codigo: Código de la zona (ej: '01')
        
    Returns:
        JSON con lista de puestos
    """
    try:
        print(f"[PUESTOS] Solicitando puestos para zona: {zona_codigo}")
        
        # Obtener puestos activos de la zona
        # Nota: zona_codigo es solo el código de la zona (ej: '01')
        puestos = Location.query.filter_by(
            tipo='puesto',
            zona_codigo=zona_codigo,
            activo=True
        ).order_by(Location.puesto_nombre).all()
        
        print(f"[PUESTOS] Encontrados {len(puestos)} puestos")
        
        if not puestos:
            # Verificar si la zona existe
            zona = Location.query.filter_by(
                tipo='zona',
                zona_codigo=zona_codigo
            ).first()
            
            if not zona:
                return jsonify({
                    'success': False,
                    'error': f'Zona con código {zona_codigo} no encontrada',
                    'data': []
                }), 404
            
            return jsonify({
                'success': False,
                'error': f'No se encontraron puestos para la zona {zona_codigo}',
                'data': []
            }), 404
        
        return jsonify({
            'success': True,
            'data': [{
                'puesto_codigo': puesto.puesto_codigo,
                'puesto_nombre': puesto.puesto_nombre
            } for puesto in puestos]
        }), 200
        
    except Exception as e:
        import traceback
        print(f"[ERROR] Error en get_puestos: {str(e)}")
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': f'Error al obtener puestos: {str(e)}'
        }), 500


@locations_bp.route('/mesas', methods=['GET'])
def get_mesas_query():
    """
    Obtener mesas de un puesto usando query params
    Endpoint público (necesario para testigos)
    
    Query params:
        puesto_codigo: Código del puesto
        zona_codigo: Código de la zona (opcional)
        municipio_codigo: Código del municipio (opcional)
        departamento_codigo: Código del departamento (opcional)
        
    Returns:
        JSON con lista de mesas
    """
    try:
        puesto_codigo = request.args.get('puesto_codigo')
        
        if not puesto_codigo:
            return jsonify({
                'success': False,
                'error': 'puesto_codigo es requerido',
                'data': []
            }), 400
        
        # Construir query
        query = Location.query.filter_by(
            tipo='mesa',
            puesto_codigo=puesto_codigo,
            activo=True
        )
        
        # Filtros opcionales
        zona_codigo = request.args.get('zona_codigo')
        if zona_codigo:
            query = query.filter_by(zona_codigo=zona_codigo)
            
        municipio_codigo = request.args.get('municipio_codigo')
        if municipio_codigo:
            query = query.filter_by(municipio_codigo=municipio_codigo)
            
        departamento_codigo = request.args.get('departamento_codigo')
        if departamento_codigo:
            query = query.filter_by(departamento_codigo=departamento_codigo)
        
        # Obtener mesas
        mesas = query.order_by(Location.mesa_codigo).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'id': mesa.id,
                'mesa_codigo': mesa.mesa_codigo,
                'mesa_nombre': mesa.mesa_nombre,
                'puesto_codigo': mesa.puesto_codigo,
                'puesto_nombre': mesa.puesto_nombre,
                'zona_codigo': mesa.zona_codigo,
                'municipio_codigo': mesa.municipio_codigo,
                'departamento_codigo': mesa.departamento_codigo,
                'total_votantes_registrados': mesa.total_votantes_registrados,
                'mujeres': mesa.mujeres,
                'hombres': mesa.hombres
            } for mesa in mesas]
        }), 200
        
    except Exception as e:
        print(f"Error en get_mesas_query: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error al obtener mesas: {str(e)}',
            'data': []
        }), 500


@locations_bp.route('/mesas/<puesto_codigo>', methods=['GET'])
def get_mesas(puesto_codigo):
    """
    Obtener mesas de un puesto usando path param
    Endpoint público (necesario para login)
    
    Args:
        puesto_codigo: Código del puesto
        
    Returns:
        JSON con lista de mesas
    """
    try:
        # Obtener mesas activas
        mesas = Location.query.filter_by(
            tipo='mesa',
            puesto_codigo=puesto_codigo,
            activo=True
        ).order_by(Location.mesa_codigo).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'id': mesa.id,
                'mesa_codigo': mesa.mesa_codigo,
                'mesa_nombre': mesa.mesa_nombre,
                'puesto_codigo': mesa.puesto_codigo,
                'puesto_nombre': mesa.puesto_nombre
            } for mesa in mesas]
        }), 200
        
    except Exception as e:
        print(f"Error en get_mesas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener mesas',
            'data': []
        }), 500


@locations_bp.route('/partidos', methods=['GET'])
@jwt_required()
def get_partidos():
    """
    Obtener todos los partidos activos
    Accesible para todos los roles autenticados
    """
    try:
        from backend.models.partido_politico import PartidoPolitico as Partido
        
        partidos = Partido.query.filter_by(activo=True).order_by(Partido.nombre).all()
        
        return jsonify({
            'success': True,
            'data': [partido.to_dict() for partido in partidos]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@locations_bp.route('/tipos-eleccion', methods=['GET'])
@jwt_required()
def get_tipos_eleccion():
    """
    Obtener todos los tipos de elección activos
    Accesible para todos los roles autenticados
    """
    try:
        from backend.models.configuracion_electoral import TipoEleccion
        
        tipos = TipoEleccion.query.filter_by(activo=True).order_by(TipoEleccion.nombre).all()
        
        return jsonify({
            'success': True,
            'data': [tipo.to_dict() for tipo in tipos]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@locations_bp.route('/puestos-todos', methods=['GET'])
@jwt_required()
def get_todos_puestos():
    """
    Obtener todos los puestos electorales con sus coordenadas
    Para mostrar en el mapa de monitoreo
    """
    try:
        puestos = Location.query.filter(
            Location.tipo == 'puesto',
            Location.latitud.isnot(None),
            Location.longitud.isnot(None)
        ).all()
        
        from backend.models.user import User
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
        
        puestos_data = []
        for puesto in puestos:
            # Contar mesas del puesto
            total_mesas = Location.query.filter(
                Location.tipo == 'mesa',
                Location.departamento_codigo == puesto.departamento_codigo,
                Location.municipio_codigo == puesto.municipio_codigo,
                Location.zona_codigo == puesto.zona_codigo,
                Location.puesto_codigo == puesto.puesto_codigo
            ).count()
            
            # Contar testigos del puesto
            testigos_verificados = User.query.filter(
                User.rol == 'testigo_electoral',
                User.ubicacion_id == puesto.id,
                User.presencia_verificada == True
            ).count()
            
            testigos_pendientes = User.query.filter(
                User.rol == 'testigo_electoral',
                User.ubicacion_id == puesto.id,
                User.presencia_verificada == False
            ).count()
            
            # Obtener IDs de mesas del puesto
            mesas_ids = [m.id for m in Location.query.filter(
                Location.tipo == 'mesa',
                Location.departamento_codigo == puesto.departamento_codigo,
                Location.municipio_codigo == puesto.municipio_codigo,
                Location.zona_codigo == puesto.zona_codigo,
                Location.puesto_codigo == puesto.puesto_codigo
            ).all()]
            
            # Contar formularios E-14
            formularios_validados = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesas_ids),
                FormularioE14.estado == 'validado'
            ).count() if mesas_ids else 0
            
            formularios_pendientes = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesas_ids),
                FormularioE14.estado == 'pendiente'
            ).count() if mesas_ids else 0
            
            formularios_rechazados = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesas_ids),
                FormularioE14.estado == 'rechazado'
            ).count() if mesas_ids else 0
            
            # Contar incidentes y delitos
            total_incidentes = IncidenteElectoral.query.filter(
                IncidenteElectoral.mesa_id.in_(mesas_ids)
            ).count() if mesas_ids else 0
            
            total_delitos = DelitoElectoral.query.filter(
                DelitoElectoral.mesa_id.in_(mesas_ids)
            ).count() if mesas_ids else 0
            
            puestos_data.append({
                'id': puesto.id,
                'puesto_codigo': puesto.puesto_codigo,
                'nombre': puesto.puesto_nombre or puesto.nombre_completo,
                'latitud': puesto.latitud,
                'longitud': puesto.longitud,
                'departamento_codigo': puesto.departamento_codigo,
                'departamento_nombre': puesto.departamento_nombre,
                'municipio_codigo': puesto.municipio_codigo,
                'municipio_nombre': puesto.municipio_nombre,
                'zona_codigo': puesto.zona_codigo,
                'direccion': puesto.direccion,
                'total_mesas': total_mesas,
                'testigos_verificados': testigos_verificados,
                'testigos_pendientes': testigos_pendientes,
                'formularios_validados': formularios_validados,
                'formularios_pendientes': formularios_pendientes,
                'formularios_rechazados': formularios_rechazados,
                'total_incidentes': total_incidentes,
                'total_delitos': total_delitos
            })
        
        return jsonify({
            'success': True,
            'data': puestos_data,
            'total': len(puestos_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
