"""
Script para importar datos de JSON a PostgreSQL
Para migrar de desarrollo (SQLite) a producción (PostgreSQL)
"""
import json
import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.models.formulario_e14 import FormularioE14, VotoPartido
from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral, EvidenciaFotografica


def parse_datetime(date_str):
    """Parsear string de fecha a datetime"""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str)
    except:
        return None


def import_users(users_data):
    """Importar usuarios"""
    print("\n👥 Importando usuarios...")
    count = 0
    
    for user_data in users_data:
        # Verificar si el usuario ya existe
        existing = User.query.filter_by(nombre=user_data['nombre'], rol=user_data['rol']).first()
        if existing:
            print(f"   ⚠️  Usuario '{user_data['nombre']}' ({user_data['rol']}) ya existe, omitiendo...")
            continue
        
        user = User(
            nombre=user_data['nombre'],
            rol=user_data['rol'],
            ubicacion_id=user_data.get('ubicacion_id'),
            activo=user_data.get('activo', True),
            es_usuario_basico=user_data.get('es_usuario_basico', False),
            presencia_verificada=user_data.get('presencia_verificada', False),
            presencia_verificada_at=parse_datetime(user_data.get('presencia_verificada_at')),
            ultimo_acceso=parse_datetime(user_data.get('ultimo_acceso')),
            ultima_latitud=user_data.get('ultima_latitud'),
            ultima_longitud=user_data.get('ultima_longitud'),
            ultima_geolocalizacion_at=parse_datetime(user_data.get('ultima_geolocalizacion_at')),
            precision_geolocalizacion=user_data.get('precision_geolocalizacion'),
            created_at=parse_datetime(user_data.get('created_at')) or datetime.now(),
            updated_at=parse_datetime(user_data.get('updated_at')) or datetime.now(),
        )
        
        # Establecer contraseña por defecto
        user.set_password('test123')  # Contraseña temporal
        
        db.session.add(user)
        count += 1
    
    db.session.commit()
    print(f"   ✅ {count} usuarios importados")
    print(f"   ⚠️  Contraseña temporal para todos: 'test123'")


def import_locations(locations_data):
    """Importar ubicaciones"""
    print("\n📍 Importando ubicaciones...")
    count = 0
    
    for loc_data in locations_data:
        # Verificar si la ubicación ya existe
        existing = Location.query.filter_by(codigo=loc_data['codigo']).first()
        if existing:
            continue
        
        location = Location(
            tipo=loc_data['tipo'],
            nombre=loc_data['nombre'],
            codigo=loc_data['codigo'],
            departamento_codigo=loc_data.get('departamento_codigo'),
            municipio_codigo=loc_data.get('municipio_codigo'),
            zona_codigo=loc_data.get('zona_codigo'),
            puesto_codigo=loc_data.get('puesto_codigo'),
            mesa_codigo=loc_data.get('mesa_codigo'),
            nombre_completo=loc_data.get('nombre_completo'),
            total_votantes_registrados=loc_data.get('total_votantes_registrados'),
            mujeres=loc_data.get('mujeres'),
            hombres=loc_data.get('hombres'),
            latitud=loc_data.get('latitud'),
            longitud=loc_data.get('longitud'),
            activo=loc_data.get('activo', True),
        )
        
        db.session.add(location)
        count += 1
    
    db.session.commit()
    print(f"   ✅ {count} ubicaciones importadas")


def import_formularios(formularios_data):
    """Importar formularios E-14"""
    print("\n📋 Importando formularios E-14...")
    count = 0
    
    for form_data in formularios_data:
        # Verificar si el formulario ya existe
        existing = FormularioE14.query.get(form_data['id'])
        if existing:
            continue
        
        formulario = FormularioE14(
            mesa_id=form_data['mesa_id'],
            testigo_id=form_data['testigo_id'],
            tipo_eleccion_id=form_data.get('tipo_eleccion_id'),
            total_votantes_registrados=form_data['total_votantes_registrados'],
            total_votos=form_data['total_votos'],
            votos_validos=form_data['votos_validos'],
            votos_nulos=form_data['votos_nulos'],
            votos_blanco=form_data['votos_blanco'],
            tarjetas_no_marcadas=form_data['tarjetas_no_marcadas'],
            total_tarjetas=form_data['total_tarjetas'],
            estado=form_data['estado'],
            validado_por_id=form_data.get('validado_por_id'),
            validado_at=parse_datetime(form_data.get('validado_at')),
            motivo_rechazo=form_data.get('motivo_rechazo'),
            imagen_url=form_data.get('imagen_url'),
            observaciones=form_data.get('observaciones'),
            created_at=parse_datetime(form_data.get('created_at')) or datetime.now(),
            updated_at=parse_datetime(form_data.get('updated_at')) or datetime.now(),
        )
        
        db.session.add(formulario)
        count += 1
    
    db.session.commit()
    print(f"   ✅ {count} formularios importados")


def import_votos_partidos(votos_data):
    """Importar votos por partido"""
    print("\n🗳️  Importando votos por partido...")
    count = 0
    
    for voto_data in votos_data:
        voto = VotoPartido(
            formulario_id=voto_data['formulario_id'],
            partido_id=voto_data['partido_id'],
            votos=voto_data['votos'],
            created_at=parse_datetime(voto_data.get('created_at')) or datetime.now(),
        )
        
        db.session.add(voto)
        count += 1
    
    db.session.commit()
    print(f"   ✅ {count} votos importados")


def import_incidentes(incidentes_data):
    """Importar incidentes electorales"""
    print("\n⚠️  Importando incidentes...")
    count = 0
    
    for inc_data in incidentes_data:
        incidente = IncidenteElectoral(
            titulo=inc_data['titulo'],
            descripcion=inc_data['descripcion'],
            tipo_incidente=inc_data['tipo_incidente'],
            severidad=inc_data['severidad'],
            estado=inc_data['estado'],
            fecha_reporte=parse_datetime(inc_data.get('fecha_reporte')) or datetime.now(),
            ubicacion_gps=inc_data.get('ubicacion_gps'),
            notas_resolucion=inc_data.get('notas_resolucion'),
            mesa_id=inc_data.get('mesa_id'),
            reportado_por_id=inc_data.get('reportado_por_id'),
            created_at=parse_datetime(inc_data.get('created_at')) or datetime.now(),
            updated_at=parse_datetime(inc_data.get('updated_at')) or datetime.now(),
        )
        
        db.session.add(incidente)
        count += 1
    
    db.session.commit()
    print(f"   ✅ {count} incidentes importados")


def import_delitos(delitos_data):
    """Importar delitos electorales"""
    print("\n🚨 Importando delitos...")
    count = 0
    
    for del_data in delitos_data:
        delito = DelitoElectoral(
            titulo=del_data['titulo'],
            descripcion=del_data['descripcion'],
            tipo_delito=del_data['tipo_delito'],
            gravedad=del_data['gravedad'],
            estado=del_data['estado'],
            fecha_reporte=parse_datetime(del_data.get('fecha_reporte')) or datetime.now(),
            ubicacion_gps=del_data.get('ubicacion_gps'),
            testigos_adicionales=del_data.get('testigos_adicionales'),
            denunciado_formalmente=del_data.get('denunciado_formalmente', False),
            numero_denuncia=del_data.get('numero_denuncia'),
            resultado_investigacion=del_data.get('resultado_investigacion'),
            mesa_id=del_data.get('mesa_id'),
            reportado_por_id=del_data.get('reportado_por_id'),
            created_at=parse_datetime(del_data.get('created_at')) or datetime.now(),
            updated_at=parse_datetime(del_data.get('updated_at')) or datetime.now(),
        )
        
        db.session.add(delito)
        count += 1
    
    db.session.commit()
    print(f"   ✅ {count} delitos importados")


def import_evidencias(evidencias_data):
    """Importar evidencias fotográficas"""
    print("\n📸 Importando evidencias...")
    count = 0
    
    for ev_data in evidencias_data:
        evidencia = EvidenciaFotografica(
            filename=ev_data['filename'],
            url=ev_data['url'],
            tipo=ev_data['tipo'],
            descripcion=ev_data.get('descripcion'),
            incidente_id=ev_data.get('incidente_id'),
            delito_id=ev_data.get('delito_id'),
            created_at=parse_datetime(ev_data.get('created_at')) or datetime.now(),
        )
        
        db.session.add(evidencia)
        count += 1
    
    db.session.commit()
    print(f"   ✅ {count} evidencias importadas")


def main():
    """Importar todos los datos desde JSON"""
    print("=" * 80)
    print("IMPORTACIÓN DE DATOS DE JSON A POSTGRESQL".center(80))
    print("=" * 80)
    
    # Obtener archivo de entrada (argumento o por defecto)
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'data_export.json'
    
    # Verificar que existe el archivo
    if not os.path.exists(input_file):
        print(f"\n❌ Error: No se encontró el archivo '{input_file}'")
        print("   Ejecuta primero: python scripts/utils/export_data_to_json.py")
        sys.exit(1)
    
    # Leer datos
    print(f"\n📂 Leyendo datos de: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"   Fecha de exportación: {data['export_date']}")
    print(f"   Base de datos origen: {data['database']}")
    
    # Crear app (usará DATABASE_URL si está configurada)
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print(f"\n🔗 Conectado a: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
        
        # Confirmar antes de importar (solo si es interactivo)
        is_render = os.getenv('RENDER') == 'true'
        if not is_render and sys.stdin.isatty():
            response = input("\n⚠️  ¿Deseas continuar con la importación? (s/n): ")
            if response.lower() != 's':
                print("❌ Importación cancelada")
                sys.exit(0)
        else:
            print("\n✅ Modo automático detectado, continuando con importación...")
        
        # Importar en orden (respetando relaciones)
        try:
            import_locations(data['locations'])
            import_users(data['users'])
            import_formularios(data['formularios'])
            import_votos_partidos(data['votos_partidos'])
            import_incidentes(data['incidentes'])
            import_delitos(data['delitos'])
            import_evidencias(data['evidencias'])
            
            print("\n" + "=" * 80)
            print("✅ IMPORTACIÓN COMPLETADA EXITOSAMENTE".center(80))
            print("=" * 80)
            print("\n⚠️  IMPORTANTE:")
            print("   - Todos los usuarios tienen contraseña temporal: 'test123'")
            print("   - Los usuarios deben cambiar su contraseña al primer acceso")
            print("   - Las imágenes/archivos deben migrarse manualmente si es necesario")
            print("=" * 80)
            
        except Exception as e:
            print(f"\n❌ Error durante la importación: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
