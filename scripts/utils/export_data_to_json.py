"""
Script para exportar datos de SQLite a JSON
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


def serialize_datetime(obj):
    """Serializar objetos datetime a string"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


def export_users():
    """Exportar usuarios"""
    users = User.query.all()
    return [{
        'id': u.id,
        'nombre': u.nombre,
        'rol': u.rol,
        'ubicacion_id': u.ubicacion_id,
        'activo': u.activo,
        'es_usuario_basico': u.es_usuario_basico,
        'presencia_verificada': u.presencia_verificada,
        'presencia_verificada_at': serialize_datetime(u.presencia_verificada_at),
        'ultimo_acceso': serialize_datetime(u.ultimo_acceso),
        'ultima_latitud': u.ultima_latitud,
        'ultima_longitud': u.ultima_longitud,
        'ultima_geolocalizacion_at': serialize_datetime(u.ultima_geolocalizacion_at),
        'precision_geolocalizacion': u.precision_geolocalizacion,
        'created_at': serialize_datetime(u.created_at),
        'updated_at': serialize_datetime(u.updated_at),
        # No exportamos password_hash por seguridad
    } for u in users]


def export_locations():
    """Exportar ubicaciones"""
    locations = Location.query.all()
    return [{
        'id': l.id,
        'tipo': l.tipo,
        'nombre': l.nombre,
        'codigo': l.codigo,
        'departamento_codigo': l.departamento_codigo,
        'municipio_codigo': l.municipio_codigo,
        'zona_codigo': l.zona_codigo,
        'puesto_codigo': l.puesto_codigo,
        'mesa_codigo': l.mesa_codigo,
        'nombre_completo': l.nombre_completo,
        'total_votantes_registrados': l.total_votantes_registrados,
        'mujeres': l.mujeres,
        'hombres': l.hombres,
        'latitud': l.latitud,
        'longitud': l.longitud,
        'activo': l.activo,
    } for l in locations]


def export_formularios():
    """Exportar formularios E-14"""
    formularios = FormularioE14.query.all()
    return [{
        'id': f.id,
        'mesa_id': f.mesa_id,
        'testigo_id': f.testigo_id,
        'tipo_eleccion_id': f.tipo_eleccion_id,
        'total_votantes_registrados': f.total_votantes_registrados,
        'total_votos': f.total_votos,
        'votos_validos': f.votos_validos,
        'votos_nulos': f.votos_nulos,
        'votos_blanco': f.votos_blanco,
        'tarjetas_no_marcadas': f.tarjetas_no_marcadas,
        'total_tarjetas': f.total_tarjetas,
        'estado': f.estado,
        'validado_por_id': f.validado_por_id,
        'validado_at': serialize_datetime(f.validado_at),
        'motivo_rechazo': f.motivo_rechazo,
        'imagen_url': f.imagen_url,
        'observaciones': f.observaciones,
        'created_at': serialize_datetime(f.created_at),
        'updated_at': serialize_datetime(f.updated_at),
    } for f in formularios]


def export_votos_partidos():
    """Exportar votos por partido"""
    votos = VotoPartido.query.all()
    return [{
        'id': v.id,
        'formulario_id': v.formulario_id,
        'partido_id': v.partido_id,
        'votos': v.votos,
        'created_at': serialize_datetime(v.created_at),
    } for v in votos]


def export_incidentes():
    """Exportar incidentes electorales"""
    incidentes = IncidenteElectoral.query.all()
    return [{
        'id': i.id,
        'titulo': i.titulo,
        'descripcion': i.descripcion,
        'tipo_incidente': i.tipo_incidente,
        'severidad': i.severidad,
        'estado': i.estado,
        'fecha_reporte': serialize_datetime(i.fecha_reporte),
        'ubicacion_gps': i.ubicacion_gps,
        'notas_resolucion': i.notas_resolucion,
        'mesa_id': i.mesa_id,
        'reportado_por_id': i.reportado_por_id,
        'created_at': serialize_datetime(i.created_at),
        'updated_at': serialize_datetime(i.updated_at),
    } for i in incidentes]


def export_delitos():
    """Exportar delitos electorales"""
    delitos = DelitoElectoral.query.all()
    return [{
        'id': d.id,
        'titulo': d.titulo,
        'descripcion': d.descripcion,
        'tipo_delito': d.tipo_delito,
        'gravedad': d.gravedad,
        'estado': d.estado,
        'fecha_reporte': serialize_datetime(d.fecha_reporte),
        'ubicacion_gps': d.ubicacion_gps,
        'testigos_adicionales': d.testigos_adicionales,
        'denunciado_formalmente': d.denunciado_formalmente,
        'numero_denuncia': d.numero_denuncia,
        'resultado_investigacion': d.resultado_investigacion,
        'mesa_id': d.mesa_id,
        'reportado_por_id': d.reportado_por_id,
        'created_at': serialize_datetime(d.created_at),
        'updated_at': serialize_datetime(d.updated_at),
    } for d in delitos]


def export_evidencias():
    """Exportar evidencias fotográficas"""
    evidencias = EvidenciaFotografica.query.all()
    return [{
        'id': e.id,
        'filename': e.filename,
        'url': e.url,
        'tipo': e.tipo,
        'descripcion': e.descripcion,
        'incidente_id': e.incidente_id,
        'delito_id': e.delito_id,
        'created_at': serialize_datetime(e.created_at),
    } for e in evidencias]


def main():
    """Exportar todos los datos a JSON"""
    print("=" * 80)
    print("EXPORTACIÓN DE DATOS DE SQLITE A JSON".center(80))
    print("=" * 80)
    
    # Crear app en modo desarrollo (SQLite)
    app = create_app('development')
    
    with app.app_context():
        print("\n📊 Exportando datos...")
        
        data = {
            'export_date': datetime.now().isoformat(),
            'database': 'SQLite (development)',
            'users': export_users(),
            'locations': export_locations(),
            'formularios': export_formularios(),
            'votos_partidos': export_votos_partidos(),
            'incidentes': export_incidentes(),
            'delitos': export_delitos(),
            'evidencias': export_evidencias(),
        }
        
        # Estadísticas
        print("\n📈 Estadísticas de exportación:")
        print(f"   - Usuarios: {len(data['users'])}")
        print(f"   - Ubicaciones: {len(data['locations'])}")
        print(f"   - Formularios E-14: {len(data['formularios'])}")
        print(f"   - Votos por partido: {len(data['votos_partidos'])}")
        print(f"   - Incidentes: {len(data['incidentes'])}")
        print(f"   - Delitos: {len(data['delitos'])}")
        print(f"   - Evidencias: {len(data['evidencias'])}")
        
        # Guardar a archivo
        output_file = 'data_export.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Datos exportados exitosamente a: {output_file}")
        print(f"   Tamaño del archivo: {os.path.getsize(output_file) / 1024:.2f} KB")
        
        print("\n" + "=" * 80)
        print("PRÓXIMOS PASOS:".center(80))
        print("=" * 80)
        print("\n1. Revisa el archivo 'data_export.json'")
        print("2. Ejecuta 'python scripts/utils/import_data_from_json.py' en Render")
        print("   (o configura DATABASE_URL local para probar)")
        print("\n⚠️  IMPORTANTE: Las contraseñas NO se exportan por seguridad")
        print("   Los usuarios deberán restablecer sus contraseñas")
        print("=" * 80)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error durante la exportación: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
