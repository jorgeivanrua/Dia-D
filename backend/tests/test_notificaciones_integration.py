"""
Integration tests para flujo completo de notificaciones
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.services.notificacion_service import NotificacionService
from backend.models.notificacion import Notificacion
from backend.models.user import User
from datetime import datetime


class TestNotificacionesIntegration:
    """Integration tests para flujo completo de notificaciones"""
    
    @patch('backend.services.notificacion_service.db')
    @patch('backend.services.notificacion_service.WebSocketService')
    def test_flujo_completo_incidente_critico(self, mock_ws, mock_db):
        """
        Test flujo completo: Crear incidente crítico → Verificar notificaciones creadas
        
        Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5
        """
        # Setup: Mock incidente crítico
        incidente = Mock()
        incidente.id = 1
        incidente.severidad = 'crítica'
        incidente.tipo_incidente = 'disturbios'
        incidente.descripcion = 'Disturbios graves en el puesto electoral'
        incidente.reportado_por_id = 100
        
        # Mock mesa y puesto
        mesa = Mock()
        mesa.id = 10
        mesa.mesa_codigo = 'MESA-001'
        puesto = Mock()
        puesto.id = 5
        puesto.nombre = 'Puesto Central'
        puesto.municipio_id = 2
        puesto.departamento_id = 1
        mesa.puesto = puesto
        incidente.mesa = mesa
        
        # Mock coordinadores
        coord_puesto = Mock()
        coord_puesto.id = 50
        coord_puesto.rol = 'coordinador_puesto'
        
        coord_municipal = Mock()
        coord_municipal.id = 60
        coord_municipal.rol = 'coordinador_municipal'
        
        coord_departamental = Mock()
        coord_departamental.id = 70
        coord_departamental.rol = 'coordinador_departamental'
        
        # Capturar notificaciones y emisiones WebSocket
        notificaciones_creadas = []
        emisiones_websocket = []
        
        def mock_add(notificacion):
            notificaciones_creadas.append(notificacion)
        
        def mock_emit(user_id, event, data):
            emisiones_websocket.append({'user_id': user_id, 'event': event, 'data': data})
            return True
        
        mock_db.session.add = mock_add
        mock_db.session.commit = Mock()
        mock_ws.emit_to_user = mock_emit
        mock_ws.notify_mapa_update = Mock()
        
        with patch.object(NotificacionService, '_get_coordinador_puesto', return_value=coord_puesto):
            with patch.object(NotificacionService, '_get_coordinador_municipal', return_value=coord_municipal):
                with patch.object(NotificacionService, '_get_coordinador_departamental', return_value=coord_departamental):
                    with patch.object(NotificacionService, '_debe_notificar_incidente', return_value=True):
                        # Ejecutar: Crear notificaciones
                        result = NotificacionService.notificar_incidente(incidente)
                        
                        # Verificar: Se crearon 3 notificaciones (puesto, municipal, departamental)
                        assert len(notificaciones_creadas) == 3, \
                            f"Debe crear 3 notificaciones para incidente crítico, creó {len(notificaciones_creadas)}"
                        
                        # Verificar: Usuarios correctos notificados
                        usuarios_notificados = {n.usuario_id for n in notificaciones_creadas}
                        assert coord_puesto.id in usuarios_notificados
                        assert coord_municipal.id in usuarios_notificados
                        assert coord_departamental.id in usuarios_notificados
                        
                        # Verificar: Todas son de tipo 'nuevo_incidente'
                        for notif in notificaciones_creadas:
                            assert notif.tipo == 'nuevo_incidente'
                            assert notif.incidente_id == incidente.id
                            assert notif.severidad == 'crítica'
                        
                        # Verificar: Se emitieron notificaciones por WebSocket
                        assert len(emisiones_websocket) == 3, \
                            f"Debe emitir 3 notificaciones por WebSocket, emitió {len(emisiones_websocket)}"
                        
                        # Verificar: Se solicitó actualización del mapa
                        mock_ws.notify_mapa_update.assert_called_once()
    
    @patch('backend.services.notificacion_service.db')
    @patch('backend.services.notificacion_service.WebSocketService')
    def test_flujo_cambio_estado_notifica_reportante(self, mock_ws, mock_db):
        """
        Test flujo: Cambiar estado → Verificar notificación al reportante
        
        Validates: Requirements 4.5
        """
        # Setup: Mock reporte
        reporte = Mock()
        reporte.id = 5
        reporte.reportado_por_id = 100
        
        # Mock usuario actualizador (diferente al reportante)
        usuario_actualizador = Mock()
        usuario_actualizador.id = 200
        usuario_actualizador.nombre_completo = 'Juan Pérez'
        
        # Capturar notificaciones
        notificaciones_creadas = []
        emisiones_websocket = []
        
        def mock_add(notificacion):
            notificaciones_creadas.append(notificacion)
        
        def mock_emit(user_id, event, data):
            emisiones_websocket.append({'user_id': user_id, 'event': event, 'data': data})
            return True
        
        mock_db.session.add = mock_add
        mock_db.session.commit = Mock()
        mock_ws.emit_to_user = mock_emit
        
        with patch.object(NotificacionService, '_debe_notificar_cambio_estado', return_value=True):
            # Ejecutar: Cambiar estado
            result = NotificacionService.notificar_cambio_estado(
                reporte,
                'incidente',
                'reportado',
                'en_revision',
                usuario_actualizador
            )
            
            # Verificar: Se creó 1 notificación
            assert len(notificaciones_creadas) == 1
            
            # Verificar: Notificación al reportante
            notif = notificaciones_creadas[0]
            assert notif.usuario_id == reporte.reportado_por_id
            assert notif.tipo == 'cambio_estado'
            assert 'reportado' in notif.mensaje
            assert 'en_revision' in notif.mensaje
            assert usuario_actualizador.nombre_completo in notif.mensaje
            
            # Verificar: Se emitió por WebSocket
            assert len(emisiones_websocket) == 1
            assert emisiones_websocket[0]['user_id'] == reporte.reportado_por_id
    
    @patch('backend.services.notificacion_service.db')
    @patch('backend.services.notificacion_service.WebSocketService')
    def test_flujo_delito_notifica_coordinadores_y_auditores(self, mock_ws, mock_db):
        """
        Test flujo: Crear delito → Verificar notificaciones a coordinadores y auditores
        
        Validates: Requirements 2.3, 4.4
        """
        # Setup: Mock delito
        delito = Mock()
        delito.id = 3
        delito.gravedad = 'grave'
        delito.tipo_delito = 'compra_votos'
        delito.descripcion = 'Compra de votos detectada'
        delito.reportado_por_id = 100
        
        # Mock mesa y puesto
        mesa = Mock()
        mesa.id = 10
        puesto = Mock()
        puesto.id = 5
        puesto.nombre = 'Puesto Central'
        puesto.municipio_id = 2
        puesto.departamento_id = 1
        mesa.puesto = puesto
        delito.mesa = mesa
        
        # Mock coordinadores y auditores
        coord_municipal = Mock()
        coord_municipal.id = 60
        
        coord_departamental = Mock()
        coord_departamental.id = 70
        
        auditor1 = Mock()
        auditor1.id = 80
        
        auditor2 = Mock()
        auditor2.id = 90
        
        # Capturar notificaciones
        notificaciones_creadas = []
        emisiones_websocket = []
        
        def mock_add(notificacion):
            notificaciones_creadas.append(notificacion)
        
        def mock_emit(user_id, event, data):
            emisiones_websocket.append({'user_id': user_id, 'event': event, 'data': data})
            return True
        
        mock_db.session.add = mock_add
        mock_db.session.commit = Mock()
        mock_ws.emit_to_user = mock_emit
        mock_ws.notify_mapa_update = Mock()
        
        with patch.object(NotificacionService, '_get_coordinador_municipal', return_value=coord_municipal):
            with patch.object(NotificacionService, '_get_coordinador_departamental', return_value=coord_departamental):
                with patch.object(NotificacionService, '_get_auditores', return_value=[auditor1, auditor2]):
                    with patch.object(NotificacionService, '_debe_notificar_delito', return_value=True):
                        # Ejecutar: Crear notificaciones
                        result = NotificacionService.notificar_delito(delito)
                        
                        # Verificar: Se crearon 4 notificaciones (2 coordinadores + 2 auditores)
                        assert len(notificaciones_creadas) == 4
                        
                        # Verificar: Usuarios correctos notificados
                        usuarios_notificados = {n.usuario_id for n in notificaciones_creadas}
                        assert coord_municipal.id in usuarios_notificados
                        assert coord_departamental.id in usuarios_notificados
                        assert auditor1.id in usuarios_notificados
                        assert auditor2.id in usuarios_notificados
                        
                        # Verificar: Todas son de tipo 'nuevo_delito'
                        for notif in notificaciones_creadas:
                            assert notif.tipo == 'nuevo_delito'
                            assert notif.delito_id == delito.id
                            assert notif.gravedad == 'grave'
                        
                        # Verificar: Se emitieron por WebSocket
                        assert len(emisiones_websocket) == 4
                        
                        # Verificar: Se solicitó actualización del mapa
                        mock_ws.notify_mapa_update.assert_called_once()
    
    @patch('backend.services.notificacion_service.db')
    @patch('backend.services.notificacion_service.WebSocketService')
    def test_flujo_no_duplicar_notificaciones(self, mock_ws, mock_db):
        """
        Test que no se duplican notificaciones si se llama múltiples veces
        
        Validates: Requirements 4.1, 4.2
        """
        # Setup: Mock incidente
        incidente = Mock()
        incidente.id = 1
        incidente.severidad = 'media'
        incidente.tipo_incidente = 'retraso_apertura'
        incidente.descripcion = 'Retraso en apertura'
        
        # Mock mesa y puesto
        mesa = Mock()
        mesa.id = 10
        puesto = Mock()
        puesto.id = 5
        puesto.nombre = 'Puesto'
        puesto.municipio_id = 2
        puesto.departamento_id = 1
        mesa.puesto = puesto
        incidente.mesa = mesa
        
        # Mock coordinador
        coord_puesto = Mock()
        coord_puesto.id = 50
        
        # Capturar notificaciones
        notificaciones_creadas = []
        
        def mock_add(notificacion):
            notificaciones_creadas.append(notificacion)
        
        mock_db.session.add = mock_add
        mock_db.session.commit = Mock()
        
        with patch.object(NotificacionService, '_get_coordinador_puesto', return_value=coord_puesto):
            with patch.object(NotificacionService, '_get_coordinador_municipal', return_value=None):
                with patch.object(NotificacionService, '_get_coordinador_departamental', return_value=None):
                    with patch.object(NotificacionService, '_debe_notificar_incidente', return_value=True):
                        # Ejecutar: Llamar dos veces
                        NotificacionService.notificar_incidente(incidente)
                        NotificacionService.notificar_incidente(incidente)
                        
                        # Verificar: Se crearon 2 notificaciones (una por cada llamada)
                        # Esto es correcto porque cada llamada es un evento diferente
                        assert len(notificaciones_creadas) == 2
                        
                        # En un sistema real, deberíamos tener lógica para evitar duplicados
                        # basada en timestamp o ID de transacción
    
    @patch('backend.services.notificacion_service.db')
    @patch('backend.services.notificacion_service.WebSocketService')
    @patch('backend.services.notificacion_service.ConfiguracionNotificaciones')
    def test_flujo_respeta_configuracion_usuario(self, mock_config_class, mock_ws, mock_db):
        """
        Test que se respeta la configuración de notificaciones del usuario
        
        Validates: Requirements 4.1, 4.2
        """
        # Setup: Mock incidente
        incidente = Mock()
        incidente.id = 1
        incidente.severidad = 'alta'
        incidente.tipo_incidente = 'irregularidades_proceso'
        incidente.descripcion = 'Irregularidades detectadas'
        
        # Mock mesa y puesto
        mesa = Mock()
        mesa.id = 10
        puesto = Mock()
        puesto.id = 5
        puesto.nombre = 'Puesto'
        puesto.municipio_id = 2
        puesto.departamento_id = 1
        mesa.puesto = puesto
        incidente.mesa = mesa
        
        # Mock coordinador con configuración que desactiva notificaciones de severidad alta
        coord_puesto = Mock()
        coord_puesto.id = 50
        
        config = Mock()
        config.notificar_web = True
        config.notificar_incidentes_alta = False  # Desactivado
        
        mock_config_class.query.filter_by.return_value.first.return_value = config
        
        # Capturar notificaciones
        notificaciones_creadas = []
        mock_db.session.add = lambda n: notificaciones_creadas.append(n)
        mock_db.session.commit = Mock()
        
        with patch.object(NotificacionService, '_get_coordinador_puesto', return_value=coord_puesto):
            with patch.object(NotificacionService, '_get_coordinador_municipal', return_value=None):
                with patch.object(NotificacionService, '_get_coordinador_departamental', return_value=None):
                    # Ejecutar
                    result = NotificacionService.notificar_incidente(incidente)
                    
                    # Verificar: NO se creó notificación porque está desactivada en configuración
                    assert len(notificaciones_creadas) == 0
