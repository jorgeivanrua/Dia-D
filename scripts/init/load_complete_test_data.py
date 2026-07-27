"""
Script para cargar datos de prueba COMPLETOS para auditoría
Incluye: usuarios, ubicaciones, partidos, candidatos, formularios, incidentes, notificaciones
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import db
from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location
from backend.models.configuracion_electoral import TipoEleccion
from backend.models.partido_politico import PartidoPolitico as Partido
from backend.models.candidato import Candidato
from backend.models.configuracion_electoral import Campana
from backend.models.formulario_e14 import FormularioE14, VotoPartido
from backend.models.coordinador_municipal import (
    FormularioE24Puesto, VotoPartidoE24Puesto,
    FormularioE24Municipal, VotoPartidoE24Municipal,
    Notificacion, AuditLog
)
from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
from datetime import datetime, date, timedelta
import random


def create_locations():
    """Crear estructura completa de ubicaciones"""
    print("\n📍 Creando ubicaciones DIVIPOLA...")
    
    # Departamento
    dept = Location(
        departamento_codigo='TEST01',
        departamento_nombre='Departamento Test',
        nombre_completo='Departamento Test',
        tipo='departamento'
    )
    db.session.add(dept)
    db.session.flush()
    
    # Municipio
    mun = Location(
        departamento_codigo='TEST01',
        municipio_codigo='TEST0101',
        departamento_nombre='Departamento Test',
        municipio_nombre='Municipio Test',
        nombre_completo='Municipio Test - Departamento Test',
        tipo='municipio'
    )
    db.session.add(mun)
    db.session.flush()
    
    # Puestos y mesas
    puestos = []
    mesas = []
    
    for i in range(1, 4):  # 3 puestos
        puesto = Location(
            departamento_codigo='TEST01',
            municipio_codigo='TEST0101',
            zona_codigo=f'TEST01Z{i}',
            puesto_codigo=f'TEST010100{i}',
            departamento_nombre='Departamento Test',
            municipio_nombre='Municipio Test',
            puesto_nombre=f'Puesto de Votación {i}',
            nombre_completo=f'Puesto de Votación {i} - Municipio Test',
            tipo='puesto'
        )
        db.session.add(puesto)
        db.session.flush()
        puestos.append(puesto)
        
        # 5 mesas por puesto
        for j in range(1, 6):
            mesa = Location(
                departamento_codigo='TEST01',
                municipio_codigo='TEST0101',
                zona_codigo=f'TEST01Z{i}',
                puesto_codigo=f'TEST010100{i}',
                mesa_codigo=f'TEST010100{i}00{j}',
                departamento_nombre='Departamento Test',
                municipio_nombre='Municipio Test',
                puesto_nombre=f'Puesto de Votación {i}',
                mesa_nombre=f'Mesa {j}',
                nombre_completo=f'Mesa {j} - Puesto de Votación {i}',
                tipo='mesa',
                total_votantes_registrados=random.randint(250, 350)
            )
            db.session.add(mesa)
            db.session.flush()
            mesas.append(mesa)
    
    db.session.commit()
    print(f"✅ Creadas: 1 departamento, 1 municipio, {len(puestos)} puestos, {len(mesas)} mesas")
    
    return dept, mun, puestos, mesas


def create_users(dept, mun, puestos, mesas):
    """Crear usuarios para todos los roles"""
    print("\n👥 Creando usuarios de prueba...")
    
    usuarios = []
    
    # Super Admin
    admin = User(
        nombre='admin_test',
        rol='super_admin',
        ubicacion_id=None,
        activo=True
    )
    admin.set_password('test123')
    usuarios.append(admin)
    
    # Auditor
    auditor = User(
        nombre='auditor_test',
        rol='auditor_electoral',
        ubicacion_id=None,
        activo=True
    )
    auditor.set_password('test123')
    usuarios.append(auditor)
    
    # Coordinador Departamental
    coord_dept = User(
        nombre='coord_dept_test',
        rol='coordinador_departamental',
        ubicacion_id=dept.id,
        activo=True
    )
    coord_dept.set_password('test123')
    usuarios.append(coord_dept)
    
    # Coordinador Municipal
    coord_mun = User(
        nombre='coord_mun_test',
        rol='coordinador_municipal',
        ubicacion_id=mun.id,
        activo=True
    )
    coord_mun.set_password('test123')
    usuarios.append(coord_mun)
    
    # Coordinadores de Puesto (uno por puesto)
    for idx, puesto in enumerate(puestos):
        coord_puesto = User(
            nombre=f'coord_puesto_test_{idx+1}',
            rol='coordinador_puesto',
            ubicacion_id=puesto.id,
            activo=True
        )
        coord_puesto.set_password('test123')
        usuarios.append(coord_puesto)
    
    # Testigos (uno por mesa)
    for idx, mesa in enumerate(mesas):
        testigo = User(
            nombre=f'testigo_test_{idx+1}',
            rol='testigo_electoral',
            ubicacion_id=mesa.id,
            activo=True,
            presencia_verificada=True,
            presencia_verificada_at=datetime.utcnow()
        )
        testigo.set_password('test123')
        usuarios.append(testigo)
    
    for user in usuarios:
        db.session.add(user)
    
    db.session.commit()
    print(f"✅ Creados {len(usuarios)} usuarios")
    
    return usuarios


def create_electoral_config():
    """Crear configuración electoral completa"""
    print("\n🗳️  Creando configuración electoral...")
    
    # Campaña
    campana = Campana(
        codigo='TEST_2024',
        nombre='Campaña Electoral Test 2024',
        descripcion='Campaña completa para testing y auditoría del sistema',
        fecha_inicio=date.today() - timedelta(days=30),
        fecha_fin=date.today() + timedelta(days=30),
        color_primario='#FF5722',
        color_secundario='#FFC107',
        es_partido_completo=True,
        activa=True
    )
    db.session.add(campana)
    db.session.flush()
    
    # Tipos de elección
    tipos = []
    tipos_data = [
        {
            'codigo': 'PRESIDENTE',
            'nombre': 'Presidente de la República',
            'es_uninominal': True,
            'permite_coaliciones': True
        },
        {
            'codigo': 'SENADO',
            'nombre': 'Senado de la República',
            'es_uninominal': False,
            'permite_lista_cerrada': True,
            'permite_lista_abierta': True,
            'permite_coaliciones': True
        },
        {
            'codigo': 'CAMARA',
            'nombre': 'Cámara de Representantes',
            'es_uninominal': False,
            'permite_lista_cerrada': True,
            'permite_lista_abierta': False,
            'permite_coaliciones': False
        },
        {
            'codigo': 'GOBERNADOR',
            'nombre': 'Gobernador',
            'es_uninominal': True,
            'permite_coaliciones': True
        }
    ]
    
    for tipo_data in tipos_data:
        tipo = TipoEleccion(**tipo_data, activo=True)
        db.session.add(tipo)
        db.session.flush()
        tipos.append(tipo)
    
    # Partidos
    partidos = []
    partidos_data = [
        {'codigo': 'PL', 'nombre': 'Partido Liberal', 'nombre_corto': 'PL', 'color': '#FF0000'},
        {'codigo': 'PC', 'nombre': 'Partido Conservador', 'nombre_corto': 'PC', 'color': '#0000FF'},
        {'codigo': 'PV', 'nombre': 'Partido Verde', 'nombre_corto': 'PV', 'color': '#00FF00'},
        {'codigo': 'PU', 'nombre': 'Partido de la U', 'nombre_corto': 'PU', 'color': '#FFFF00'},
        {'codigo': 'CD', 'nombre': 'Centro Democrático', 'nombre_corto': 'CD', 'color': '#FF8800'},
        {'codigo': 'PP', 'nombre': 'Polo Democrático', 'nombre_corto': 'PP', 'color': '#FF00FF'},
    ]
    
    for partido_data in partidos_data:
        partido = Partido(**partido_data, activo=True)
        db.session.add(partido)
        db.session.flush()
        partidos.append(partido)
    
    # Candidatos
    candidatos_count = 0
    
    # Presidente (uno por partido)
    for idx, partido in enumerate(partidos):
        candidato = Candidato(
            codigo=f'PRES_{partido.codigo}',
            nombre_completo=f'Candidato Presidencial {partido.nombre_corto}',
            partido_id=partido.id,
            tipo_eleccion_id=tipos[0].id,
            es_independiente=False,
            activo=True
        )
        db.session.add(candidato)
        candidatos_count += 1
    
    # Senado (listas de 5 por partido)
    for partido in partidos:
        for i in range(1, 6):
            candidato = Candidato(
                codigo=f'SEN_{partido.codigo}_{i}',
                nombre_completo=f'Senador {partido.nombre_corto} #{i}',
                numero_lista=i,
                partido_id=partido.id,
                tipo_eleccion_id=tipos[1].id,
                es_cabeza_lista=(i == 1),
                activo=True
            )
            db.session.add(candidato)
            candidatos_count += 1
    
    # Cámara (listas de 3 por partido)
    for partido in partidos:
        for i in range(1, 4):
            candidato = Candidato(
                codigo=f'CAM_{partido.codigo}_{i}',
                nombre_completo=f'Representante {partido.nombre_corto} #{i}',
                numero_lista=i,
                partido_id=partido.id,
                tipo_eleccion_id=tipos[2].id,
                es_cabeza_lista=(i == 1),
                activo=True
            )
            db.session.add(candidato)
            candidatos_count += 1
    
    db.session.commit()
    print(f"✅ Creados: 1 campaña, {len(tipos)} tipos de elección, {len(partidos)} partidos, {candidatos_count} candidatos")
    
    return campana, tipos, partidos


def create_formularios_e14(mesas, partidos, testigos):
    """Crear formularios E-14 de prueba"""
    print("\n📝 Creando formularios E-14...")
    
    formularios = []
    
    # Crear formularios para las primeras 10 mesas
    for idx, mesa in enumerate(mesas[:10]):
        testigo = testigos[idx] if idx < len(testigos) else testigos[0]
        
        # Generar votos aleatorios pero realistas
        total_votantes = random.randint(250, 350)
        votos_depositados = int(total_votantes * random.uniform(0.85, 0.95))
        votos_nulos = random.randint(3, 10)
        votos_blancos = random.randint(5, 15)
        votos_no_marcados = random.randint(0, 3)
        tarjetas_no_usadas = total_votantes - votos_depositados
        
        formulario = FormularioE14(
            mesa_id=mesa.id,
            testigo_id=testigo.id,
            total_votantes=total_votantes,
            votos_depositados=votos_depositados,
            votos_nulos=votos_nulos,
            votos_blancos=votos_blancos,
            votos_no_marcados=votos_no_marcados,
            tarjetas_no_usadas=tarjetas_no_usadas,
            estado='enviado' if idx < 8 else 'borrador',
            enviado_at=datetime.utcnow() if idx < 8 else None
        )
        db.session.add(formulario)
        db.session.flush()
        
        # Distribuir votos entre partidos
        votos_validos = votos_depositados - votos_nulos - votos_blancos - votos_no_marcados
        votos_restantes = votos_validos
        
        for i, partido in enumerate(partidos):
            if i == len(partidos) - 1:
                # Último partido recibe los votos restantes
                votos = max(0, votos_restantes)
            else:
                # Distribución aleatoria
                votos = random.randint(int(votos_validos * 0.05), int(votos_validos * 0.30))
                votos = min(votos, votos_restantes)
            
            voto_partido = VotoPartido(
                formulario_id=formulario.id,
                partido_id=partido.id,
                votos=votos
            )
            db.session.add(voto_partido)
            votos_restantes -= votos
        
        formularios.append(formulario)
    
    db.session.commit()
    print(f"✅ Creados {len(formularios)} formularios E-14")
    
    return formularios


def create_incidentes(mesas, testigos):
    """Crear incidentes y delitos de prueba"""
    print("\n⚠️  Creando incidentes y delitos...")
    
    incidentes_tipos = [
        'irregularidad_votacion',
        'problema_tecnico',
        'alteracion_orden',
        'ausencia_funcionario',
        'material_faltante'
    ]
    
    delitos_tipos = [
        'compra_votos',
        'suplantacion',
        'coaccion',
        'fraude_electoral',
        'violencia'
    ]
    
    gravedades = ['baja', 'media', 'alta', 'critica']
    
    incidentes = []
    delitos = []
    
    # Crear 5 incidentes
    for i in range(5):
        mesa = random.choice(mesas)
        testigo = next((t for t in testigos if t.ubicacion_id == mesa.id), testigos[0])
        
        incidente = IncidenteElectoral(
            tipo_incidente=random.choice(incidentes_tipos),
            descripcion=f'Incidente de prueba #{i+1}: {random.choice(incidentes_tipos)}',
            gravedad=random.choice(gravedades),
            ubicacion_id=mesa.id,
            reportado_por=testigo.id,
            estado='reportado' if i < 3 else 'en_revision',
            fecha_hora=datetime.utcnow() - timedelta(hours=random.randint(1, 24))
        )
        db.session.add(incidente)
        incidentes.append(incidente)
    
    # Crear 3 delitos
    for i in range(3):
        mesa = random.choice(mesas)
        testigo = next((t for t in testigos if t.ubicacion_id == mesa.id), testigos[0])
        
        delito = DelitoElectoral(
            tipo_delito=random.choice(delitos_tipos),
            descripcion=f'Delito de prueba #{i+1}: {random.choice(delitos_tipos)}',
            gravedad=random.choice(['alta', 'critica']),
            ubicacion_id=mesa.id,
            reportado_por=testigo.id,
            estado='reportado',
            fecha_hora=datetime.utcnow() - timedelta(hours=random.randint(1, 12))
        )
        db.session.add(delito)
        delitos.append(delito)
    
    db.session.commit()
    print(f"✅ Creados {len(incidentes)} incidentes y {len(delitos)} delitos")
    
    return incidentes, delitos


def create_audit_logs(usuarios):
    """Crear logs de auditoría"""
    print("\n📋 Creando logs de auditoría...")
    
    acciones = [
        'login',
        'logout',
        'crear_formulario',
        'enviar_formulario',
        'aprobar_formulario',
        'rechazar_formulario',
        'crear_usuario',
        'actualizar_usuario',
        'reportar_incidente',
        'consolidar_e24'
    ]
    
    logs = []
    
    for i in range(20):
        usuario = random.choice(usuarios)
        accion = random.choice(acciones)
        
        log = AuditLog(
            usuario_id=usuario.id,
            accion=accion,
            detalles=f'Acción de prueba: {accion}',
            ip_address=f'192.168.1.{random.randint(1, 255)}',
            user_agent='Mozilla/5.0 (Test Browser)',
            timestamp=datetime.utcnow() - timedelta(hours=random.randint(1, 48))
        )
        db.session.add(log)
        logs.append(log)
    
    db.session.commit()
    print(f"✅ Creados {len(logs)} logs de auditoría")
    
    return logs


def create_notificaciones(usuarios):
    """Crear notificaciones de prueba"""
    print("\n📬 Creando notificaciones...")
    
    coordinadores = [u for u in usuarios if 'coordinador' in u.rol]
    
    notificaciones = []
    
    mensajes = [
        'Formulario E-14 pendiente de revisión',
        'Incidente reportado en su zona',
        'Consolidación de E-24 completada',
        'Actualización de datos requerida',
        'Reporte departamental disponible'
    ]
    
    for i in range(10):
        destinatario = random.choice(coordinadores)
        
        notif = Notificacion(
            destinatario_id=destinatario.id,
            tipo='sistema',
            titulo=f'Notificación #{i+1}',
            mensaje=random.choice(mensajes),
            prioridad=random.choice(['baja', 'normal', 'alta']),
            leida=(i < 5),
            fecha_lectura=datetime.utcnow() - timedelta(hours=random.randint(1, 12)) if i < 5 else None
        )
        db.session.add(notif)
        notificaciones.append(notif)
    
    db.session.commit()
    print(f"✅ Creadas {len(notificaciones)} notificaciones")
    
    return notificaciones


def load_complete_test_data(app_context=None):
    """Cargar datos de prueba completos"""
    if app_context is None:
        app = create_app()
        app_context = app.app_context()
        app_context.push()
    
    try:
        print("\n" + "="*60)
        print("  CARGA DE DATOS COMPLETOS PARA AUDITORÍA")
        print("="*60)
        
        # Limpiar datos existentes (opcional)
        print("\n⚠️  Limpiando datos existentes...")
        db.drop_all()
        db.create_all()
        print("✅ Base de datos limpia")
        
        # Crear datos
        dept, mun, puestos, mesas = create_locations()
        usuarios = create_users(dept, mun, puestos, mesas)
        campana, tipos, partidos = create_electoral_config()
        
        # Separar testigos
        testigos = [u for u in usuarios if u.rol == 'testigo_electoral']
        
        formularios = create_formularios_e14(mesas, partidos, testigos)
        incidentes, delitos = create_incidentes(mesas, testigos)
        logs = create_audit_logs(usuarios)
        notificaciones = create_notificaciones(usuarios)
        
        print("\n" + "="*60)
        print("  ✅ CARGA COMPLETA EXITOSA")
        print("="*60)
        print("\n📊 RESUMEN DE DATOS CARGADOS:")
        print(f"   • Ubicaciones: 1 dept, 1 mun, {len(puestos)} puestos, {len(mesas)} mesas")
        print(f"   • Usuarios: {len(usuarios)} (todos los roles)")
        print(f"   • Configuración: 1 campaña, {len(tipos)} tipos elección, {len(partidos)} partidos")
        print(f"   • Formularios E-14: {len(formularios)}")
        print(f"   • Incidentes: {len(incidentes)}")
        print(f"   • Delitos: {len(delitos)}")
        print(f"   • Logs de auditoría: {len(logs)}")
        print(f"   • Notificaciones: {len(notificaciones)}")
        
        print("\n🔑 CREDENCIALES DE ACCESO:")
        print("   • Super Admin: admin_test / test123")
        print("   • Auditor: auditor_test / test123")
        print("   • Coord. Departamental: coord_dept_test / test123")
        print("   • Coord. Municipal: coord_mun_test / test123")
        print("   • Coord. Puesto: coord_puesto_test_1 / test123")
        print("   • Testigo: testigo_test_1 / test123")
        
        print("\n🧪 SISTEMA LISTO PARA AUDITORÍA COMPLETA")
        print("   Ejecuta: python backend/tests/test_audit_system.py")
        print()
    except Exception as e:
        print(f"\n❌ Error durante la carga: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == '__main__':
    load_complete_test_data()
