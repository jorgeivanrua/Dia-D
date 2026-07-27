#!/usr/bin/env python3
"""
Script para probar el sistema de incidentes y delitos electorales
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.services.incidentes_delitos_service import IncidentesDelitosService
from datetime import datetime


def test_incidentes_delitos():
    """Probar creación de incidentes y delitos"""
    app = create_app()
    
    with app.app_context():
        print("\n=== PRUEBA DEL SISTEMA DE INCIDENTES Y DELITOS ===\n")
        
        # Buscar un testigo electoral
        testigo = User.query.filter_by(rol='testigo_electoral').first()
        if not testigo:
            print("❌ No se encontró ningún testigo electoral")
            return
        
        print(f"✓ Testigo encontrado: {testigo.nombre} (ID: {testigo.id})")
        
        # Buscar una mesa
        mesa = Location.query.filter_by(tipo='mesa').first()
        if not mesa:
            print("❌ No se encontró ninguna mesa")
            return
        
        print(f"✓ Mesa encontrada: {mesa.mesa_codigo}")
        
        # Crear un incidente
        print("\n--- Creando incidente ---")
        data_incidente = {
            'mesa_id': mesa.id,
            'tipo_incidente': 'falta_material',
            'titulo': 'Falta de boletas electorales',
            'descripcion': 'La mesa no cuenta con suficientes boletas para todos los votantes registrados',
            'severidad': 'alta',
            'ubicacion_gps': '-1.234567,-78.123456'
        }
        
        try:
            incidente = IncidentesDelitosService.crear_incidente(data_incidente, testigo.id)
            print(f"✓ Incidente creado exitosamente (ID: {incidente.id})")
            print(f"  - Tipo: {incidente.tipo_incidente}")
            print(f"  - Severidad: {incidente.severidad}")
            print(f"  - Estado: {incidente.estado}")
        except Exception as e:
            print(f"❌ Error al crear incidente: {e}")
            return
        
        # Crear un delito
        print("\n--- Creando delito electoral ---")
        data_delito = {
            'mesa_id': mesa.id,
            'tipo_delito': 'compra_votos',
            'titulo': 'Intento de compra de votos',
            'descripcion': 'Se observó a una persona ofreciendo dinero a cambio de votos',
            'gravedad': 'grave',
            'testigos_adicionales': 'Juan Pérez, María González',
            'ubicacion_gps': '-1.234567,-78.123456'
        }
        
        try:
            delito = IncidentesDelitosService.crear_delito(data_delito, testigo.id)
            print(f"✓ Delito creado exitosamente (ID: {delito.id})")
            print(f"  - Tipo: {delito.tipo_delito}")
            print(f"  - Gravedad: {delito.gravedad}")
            print(f"  - Estado: {delito.estado}")
        except Exception as e:
            print(f"❌ Error al crear delito: {e}")
            return
        
        # Obtener incidentes
        print("\n--- Obteniendo incidentes ---")
        incidentes = IncidentesDelitosService.obtener_incidentes(
            usuario_id=testigo.id,
            rol_usuario=testigo.rol
        )
        print(f"✓ Se encontraron {len(incidentes)} incidente(s)")
        
        # Obtener delitos
        print("\n--- Obteniendo delitos ---")
        delitos = IncidentesDelitosService.obtener_delitos(
            usuario_id=testigo.id,
            rol_usuario=testigo.rol
        )
        print(f"✓ Se encontraron {len(delitos)} delito(s)")
        
        # Obtener estadísticas
        print("\n--- Estadísticas ---")
        estadisticas = IncidentesDelitosService.obtener_estadisticas(
            usuario_id=testigo.id,
            rol_usuario=testigo.rol
        )
        print(f"✓ Total de incidentes: {estadisticas['incidentes']['total']}")
        print(f"✓ Total de delitos: {estadisticas['delitos']['total']}")
        
        # Actualizar estado del incidente
        print("\n--- Actualizando estado de incidente ---")
        coordinador = User.query.filter_by(rol='coordinador_puesto').first()
        if coordinador:
            try:
                incidente_actualizado = IncidentesDelitosService.actualizar_estado_incidente(
                    incidente.id, 'en_revision', coordinador.id, 
                    'Incidente en revisión por coordinador de puesto'
                )
                print(f"✓ Estado actualizado a: {incidente_actualizado.estado}")
            except Exception as e:
                print(f"❌ Error al actualizar estado: {e}")
        
        # Obtener seguimiento
        print("\n--- Obteniendo seguimiento ---")
        seguimiento = IncidentesDelitosService.obtener_seguimiento('incidente', incidente.id)
        print(f"✓ Se encontraron {len(seguimiento)} registro(s) de seguimiento")
        for seg in seguimiento:
            print(f"  - {seg['accion']}: {seg['comentario']}")
        
        # Obtener notificaciones
        print("\n--- Obteniendo notificaciones ---")
        if coordinador:
            notificaciones = IncidentesDelitosService.obtener_notificaciones(coordinador.id)
            print(f"✓ Se encontraron {len(notificaciones)} notificación(es)")
            for notif in notificaciones[:3]:  # Mostrar solo las primeras 3
                print(f"  - {notif['titulo']}")
        
        print("\n=== PRUEBA COMPLETADA EXITOSAMENTE ===\n")


if __name__ == '__main__':
    test_incidentes_delitos()
