"""
Script para cargar datos de prueba completos en el sistema
Incluye: usuarios, ubicaciones, partidos, candidatos, formularios, incidentes
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
from datetime import datetime, date, timedelta
import random


def load_test_data():
    """Cargar datos de prueba completos"""
    app = create_app()
    
    with app.app_context():
        print("🧪 Iniciando carga de datos de prueba...")
        
        # 1. Crear campaña de prueba
        print("\n📅 Creando campaña de prueba...")
        campana = Campana(
            codigo='TEST_2024',
            nombre='Campaña de Prueba 2024',
            descripcion='Campaña para testing y auditoría del sistema',
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=30),
            color_primario='#FF5722',
            color_secundario='#FFC107',
            es_partido_completo=True,
            activa=True
        )
        db.session.add(campana)
        db.session.commit()
        print(f"✅ Campaña creada: {campana.nombre}")
        
        # 2. Crear ubicaciones (DIVIPOLA simplificada)
        print("\n📍 Creando ubicaciones...")
        
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
        
        # Puestos
        puestos = []
        for i in range(1, 4):
            puesto = Location(
                departamento_codigo='TEST01',
                municipio_codigo='TEST0101',
                zona_codigo=f'TEST01Z{i}',
                puesto_codigo=f'TEST010100{i}',
                departamento_nombre='Departamento Test',
                municipio_nombre='Municipio Test',
                puesto_nombre=f'Puesto Test {i}',
                nombre_completo=f'Puesto Test {i} - Municipio Test',
                tipo='puesto'
            )
            db.session.add(puesto)
            db.session.flush()
            puestos.append(puesto)
            
            # Mesas por puesto
            for j in range(1, 6):
                mesa = Location(
                    departamento_codigo='TEST01',
                    municipio_codigo='TEST0101',
                    zona_codigo=f'TEST01Z{i}',
                    puesto_codigo=f'TEST010100{i}',
                    mesa_codigo=f'TEST010100{i}00{j}',
                    departamento_nombre='Departamento Test',
                    municipio_nombre='Municipio Test',
                    puesto_nombre=f'Puesto Test {i}',
                    mesa_nombre=f'Mesa {j}',
                    nombre_completo=f'Mesa {j} - Puesto Test {i}',
                    tipo='mesa',
                    total_votantes_registrados=300
                )
                db.session.add(mesa)
        
        db.session.commit()
        print(f"✅ Creadas: 1 departamento, 1 municipio, 3 puestos, 15 mesas")
        
        # 3. Crear usuarios de prueba para cada rol
        print("\n👥 Creando usuarios de prueba...")
        
        usuarios_test = [
            {
                'nombre': 'admin_test',
                'password': 'test123',
                'rol': 'super_admin',
                'ubicacion_id': None
            },
            {
                'nombre': 'auditor_test',
                'password': 'test123',
                'rol': 'auditor_electoral',
                'ubicacion_id': None
            },
            {
                'nombre': 'coord_dept_test',
                'password': 'test123',
                'rol': 'coordinador_departamental',
                'ubicacion_id': dept.id
            },
            {
                'nombre': 'coord_mun_test',
                'password': 'test123',
                'rol': 'coordinador_municipal',
                'ubicacion_id': mun.id
            },
            {
                'nombre': 'coord_puesto_test',
                'password': 'test123',
                'rol': 'coordinador_puesto',
                'ubicacion_id': puestos[0].id
            },
            {
                'nombre': 'coord_puesto_test_2',
                'password': 'test123',
                'rol': 'coordinador_puesto',
                'ubicacion_id': puestos[1].id
            },
            {
                'nombre': 'coord_puesto_test_3',
                'password': 'test123',
                'rol': 'coordinador_puesto',
                'ubicacion_id': puestos[2].id
            }
        ]
        
        # Crear testigos para cada mesa
        mesas = Location.query.filter_by(tipo='mesa').all()
        for idx, mesa in enumerate(mesas):  # Todas las mesas
            usuarios_test.append({
                'nombre': f'testigo_test_{idx+1}',
                'password': 'test123',
                'rol': 'testigo_electoral',
                'ubicacion_id': mesa.id
            })
        
        for user_data in usuarios_test:
            user = User(
                nombre=user_data['nombre'],
                rol=user_data['rol'],
                ubicacion_id=user_data['ubicacion_id'],
                activo=True
            )
            user.set_password(user_data['password'])
            db.session.add(user)
        
        db.session.commit()
        print(f"✅ Creados {len(usuarios_test)} usuarios de prueba")
        print("   Credenciales: usuario_test / test123")
        
        # 4. Crear tipos de elección
        print("\n🗳️  Creando tipos de elección...")
        
        tipos = [
            {
                'codigo': 'PRESIDENTE_TEST',
                'nombre': 'Presidente Test',
                'es_uninominal': True,
                'permite_coaliciones': True
            },
            {
                'codigo': 'SENADO_TEST',
                'nombre': 'Senado Test',
                'es_uninominal': False,
                'permite_lista_cerrada': True,
                'permite_lista_abierta': True,
                'permite_coaliciones': True
            },
            {
                'codigo': 'CAMARA_TEST',
                'nombre': 'Cámara Test',
                'es_uninominal': False,
                'permite_lista_cerrada': True,
                'permite_lista_abierta': False,
                'permite_coaliciones': False
            }
        ]
        
        tipos_eleccion = []
        for tipo_data in tipos:
            tipo = TipoEleccion(**tipo_data, activo=True)
            db.session.add(tipo)
            db.session.flush()
            tipos_eleccion.append(tipo)
        
        db.session.commit()
        print(f"✅ Creados {len(tipos)} tipos de elección")
        
        # 5. Crear partidos
        print("\n🏛️  Creando partidos políticos...")
        
        partidos_data = [
            {'codigo': 'PL_TEST', 'nombre': 'Partido Liberal Test', 'nombre_corto': 'PL', 'color': '#FF0000'},
            {'codigo': 'PC_TEST', 'nombre': 'Partido Conservador Test', 'nombre_corto': 'PC', 'color': '#0000FF'},
            {'codigo': 'PV_TEST', 'nombre': 'Partido Verde Test', 'nombre_corto': 'PV', 'color': '#00FF00'},
            {'codigo': 'PU_TEST', 'nombre': 'Partido de la U Test', 'nombre_corto': 'PU', 'color': '#FFFF00'},
        ]
        
        partidos = []
        for partido_data in partidos_data:
            partido = Partido(**partido_data, activo=True)
            db.session.add(partido)
            db.session.flush()
            partidos.append(partido)
        
        db.session.commit()
        print(f"✅ Creados {len(partidos)} partidos")
        
        # 6. Crear candidatos
        print("\n👤 Creando candidatos...")
        
        candidatos_count = 0
        
        # Candidatos presidenciales (uno por partido)
        for idx, partido in enumerate(partidos):
            candidato = Candidato(
                codigo=f'PRES_{partido.codigo}',
                nombre_completo=f'Candidato Presidencial {idx+1}',
                partido_id=partido.id,
                tipo_eleccion_id=tipos_eleccion[0].id,  # Presidente
                es_independiente=False,
                activo=True
            )
            db.session.add(candidato)
            candidatos_count += 1
        
        # Candidatos de Senado (listas de 5 por partido)
        for partido in partidos:
            for i in range(1, 6):
                candidato = Candidato(
                    codigo=f'SEN_{partido.codigo}_{i}',
                    nombre_completo=f'Senador {partido.nombre_corto} #{i}',
                    numero_lista=i,
                    partido_id=partido.id,
                    tipo_eleccion_id=tipos_eleccion[1].id,  # Senado
                    es_cabeza_lista=(i == 1),
                    activo=True
                )
                db.session.add(candidato)
                candidatos_count += 1
        
        # Candidatos de Cámara (listas de 3 por partido)
        for partido in partidos:
            for i in range(1, 4):
                candidato = Candidato(
                    codigo=f'CAM_{partido.codigo}_{i}',
                    nombre_completo=f'Representante {partido.nombre_corto} #{i}',
                    numero_lista=i,
                    partido_id=partido.id,
                    tipo_eleccion_id=tipos_eleccion[2].id,  # Cámara
                    es_cabeza_lista=(i == 1),
                    activo=True
                )
                db.session.add(candidato)
                candidatos_count += 1
        
        db.session.commit()
        print(f"✅ Creados {candidatos_count} candidatos")
        
        print("\n✅ ¡Datos de prueba cargados exitosamente!")
        print("\n📋 Resumen:")
        print(f"   - 1 Campaña activa")
        print(f"   - 1 Departamento, 1 Municipio, 3 Puestos, 15 Mesas")
        print(f"   - {len(usuarios_test)} Usuarios (todos los roles)")
        print(f"   - {len(tipos)} Tipos de elección")
        print(f"   - {len(partidos)} Partidos políticos")
        print(f"   - {candidatos_count} Candidatos")
        print("\n🔑 Credenciales de acceso:")
        print("   Usuario: admin_test | Contraseña: test123 (Super Admin)")
        print("   Usuario: testigo_test_1 | Contraseña: test123 (Testigo)")
        print("   Usuario: coord_puesto_test | Contraseña: test123 (Coordinador Puesto)")
        print("\n🧪 Sistema listo para testing!")


if __name__ == '__main__':
    load_test_data()
