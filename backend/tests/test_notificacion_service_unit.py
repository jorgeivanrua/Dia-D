"""
Unit tests para NotificacionService
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.services.notificacion_service import NotificacionService
from backend.models.notificacion import Notificacion, ConfiguracionNotificaciones
from datetime import datetime


class TestNotificacionServiceUnit:
    """Unit tests para NotificacionService"""
    
    @patch('backend.services.notificacion_service.db')
    @patch('backend.services.notificacion_service.WebSocketService')
    def test_notificar_incidente_severidad_baja(self, mock_ws, mock_db):
        """Test notificaciones para incidente de severidad baja"""
        # Mock incidente
        incidente = Mock()
        incidente.id = 1
        incidente.severidad = 'baja'
        incidente.tipo_incidente = 'retraso_apertura'
        incidente.descripcion = 'Retraso de 30 minutos'
        
        # Mock mesa y puesto
        mesa = Mock()
        mesa.id = 100
        puesto = Mock()
        puesto.id = 10
        puesto.nombre = 'Puesto Central'
        puesto.municipio_id = 5
        puesto.departamento_id = 1
        mesa.puesto = puesto
        incidente.mesa = mesa
        
        # Mock coordinador de puesto
        coord_puesto = Mock()
        coord_puesto.id = 50
        
        with patch.object(NotificacionService, '_get_coordinador_puesto', return_value=coord_puesto):
            with patch.object(NotificacionService, '_get_coordinador_municipal', return_value=None):
                with patch.object(NotificacionService, '_get_coordinador_departamental', return_value=None):
                    with patch.object(NotificacionService, '_debe_notificar_incidente', return_value=True):
                        notificaciones_creadas = []
                        mock_db.session.add = lambda n: notificaciones_creadas.append(n)
                        mock_db.session.commit = Mock()
                        
                        # Ejecutar
                        result = NotificacionService.notificar_incidente(incidente)
                        
                        # Verificar
                        assert len(notificaciones_creadas) == 1
                        assert notificaciones_creadas[0].usuario_id == coord_puesto.id
                        assert notificaciones_creadas[0].tipo == 'nuevo_incidente'
                        assert notificaciones_creadas[0].severidad == 'baja'
    
    @patch('backend.services.notificacion_service.db')
    @patch('backend.services.notificacion_service.WebSocketService')
    def test_notificar_incidente_severidad_critica(self, mock_ws, mock_db):
        """Test notificaciones para incidente de severidad crítica"""
        # Mock incidente
        incidente = Mock()
        incidente.id = 2
        incidente.severidad = 'crítica'
        incidente.tipo_incidente = 'disturbios'
        incidente.descripcion = 'Disturbios graves en el puesto'
        
        # Mock mesa y puesto
        mesa = Mock()
        mesa.id = 100
        puesto = Mock()
        puesto.id = 10
        puesto.nombre = 'Puesto Central'
        puesto.municipio_id = 5
        puesto.departamento_id = 1
        mesa.puesto = puesto
        incidente.mesa = mesa
        
        # Mock coordinadores
        coord_puesto = Mock()
        coord_puesto.id = 50
        coord_municipal = Mock()
        coord_municipal.id = 60
        coord_departamental = Mock()
        coord_departamental.id = 70
        
        with patch.object(NotificacionService, '_get_coordinador_puesto', return_value=coord_puesto):
            with patch.object(NotificacionService, '_get_coordinador_municipal', return_value=coord_municipal):
                with patch.object(NotificacionService, '_get_coordinador_departamental', return_value=coord_departamental):
                    with patch.object(NotificacionService, '_debe_notificar_incidente', return_value=True):
                        notificaciones_creadas = []
                        mock_db.session.add = lambda n: notificaciones_creadas.append(n)
                        mock_db.session.commit = Mock()
                        
                        # Ejecutar
                        result = NotificacionService.notificar_incidente(incidente)
                        
                        # Verificar: debe notificar a los 3 niveles
                        assert len(notificaciones_creadas) == 3
                        usuarios_notificados = {n.usuario_id for n in notificaciones_creadas}
                        assert coord_puesto.id in usuarios_notificados
                        assert coord_municipal.id in usuarios_notificados
                        assert coord_departamental.id in usuarios_notificados
    
    @patch('backend.services.notificacion_service.db')
    @patch('backend.services.notificacion_service.WebSocketService')
    def test_notificar_delito(self, mock_ws, mock_db):
        """Test notificaciones para delito"""
        # Mock delito
        delito = Mock()
        delito.id = 3
        delito.gravedad = 'grave'
        delito.tipo_delito = 'compra_votos'
        delito.descripcion = 'Compra de votos detectada'
        
        # Mock mesa y puesto
        mesa = Mock()
        mesa.id = 100
        puesto = Mock()
        puesto.id = 10
        puesto.nombre = 'Puesto Central'
        puesto.municipio_id = 5
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
        
        with patch.object(NotificacionService, '_get_coordinador_municipal', return_value=coord_municipal):
            with patch.object(NotificacionService, '_get_coordinador_departamental', return_value=coord_departamental):
                with patch.object(NotificacionService, '_get_auditores', return_value=[auditor1, auditor2]):
                    with patch.object(NotificacionService, '_debe_notificar_delito', return_value=True):
                        notificaciones_creadas = []
                        mock_db.session.add = lambda n: notificaciones_creadas.append(n)
                        mock_db.session.commit = Mock()
                        
                        # Ejecutar
                        result = NotificacionService.notificar_delito(delito)
                        
                        # Verificar: debe notificar a coordinadores y auditores
                        assert len(notificaciones_creadas) == 4
                        usuarios_notificados = {n.usuario_id for n in notificaciones_creadas}
                        assert coord_municipal.id in usuarios_notificados
                        assert coord_departamental.id in usuarios_notificados
                        assert auditor1.id in usuarios_notificados
                        assert auditor2.id in usuarios_notificados
                        
                        # Verificar tipo de notificación
                        for notif in notificaciones_creadas:
                            assert notif.tipo == 'nuevo_delito'
                            assert notif.delito_id == delito.id
    
    @patch('backend.services.notificacion_service.db')
    @patch('backend.services.notificacion_service.WebSocketService')
    def test_notificar_cambio_estado(self, mock_ws, mock_db):
        """Test notificación de cambio de estado"""
        # Mock reporte
        reporte = Mock()
        reporte.id = 5
        reporte.reportado_por_id = 100
        
        # Mock usuario actualizador
        usuario_actualizador = Mock()
        usuario_actualizador.id = 200
        usuario_actualizador.nombre_completo = 'Juan Pérez'
        
        with patch.object(NotificacionService, '_debe_notificar_cambio_estado', return_value=True):
            notificaciones_creadas = []
            mock_db.session.add = lambda n: notificaciones_creadas.append(n)
            mock_db.session.commit = Mock()
            
            # Ejecutar
            result = NotificacionService.notificar_cambio_estado(
                reporte, 'incidente', 'reportado', 'en_revision', usuario_actualizador
            )
            
            # Verificar
            assert len(notificaciones_creadas) == 1
            notif = notificaciones_creadas[0]
            assert notif.usuario_id == reporte.reportado_por_id
            assert notif.tipo == 'cambio_estado'
            assert 'reportado' in notif.mensaje
            assert 'en_revision' in notif.mensaje
    
    @patch('backend.services.notificacion_service.db')
    @patch('backend.services.notificacion_service.WebSocketService')
    def test_notificar_cambio_estado_mismo_usuario(self, mock_ws, mock_db):
        """Test que no se notifica si el reportante es quien actualiza"""
        # Mock reporte
        reporte = Mock()
        reporte.id = 5
        reporte.reportado_por_id = 100
        
        # Mock usuario actualizador (mismo que reportante)
        usuario_actualizador = Mock()
        usuario_actualizador.id = 100
        usuario_actualizador.nombre_completo = 'Juan Pérez'
        
        notificaciones_creadas = []
        mock_db.session.add = lambda n: notificaciones_creadas.append(n)
        mock_db.session.commit = Mock()
        
        # Ejecutar
        result = NotificacionService.notificar_cambio_estado(
            reporte, 'incidente', 'reportado', 'en_revision', usuario_actualizador
        )
        
        # Verificar: no debe crear notificación
        assert result is None
        assert len(notificaciones_creadas) == 0
    
    @patch('backend.services.notificacion_service.Notificacion')
    @patch('backend.services.notificacion_service.db')
    def test_marcar_leida_success(self, mock_db, mock_notif_class):
        """Test marcar notificación como leída"""
        # Mock notificación
        notificacion = Mock()
        notificacion.id = 1
        notificacion.usuario_id = 100
        notificacion.leida = False
        notificacion.fecha_leida = None
        
        mock_notif_class.query.get.return_value = notificacion
        mock_db.session.commit = Mock()
        
        # Ejecutar
        result = NotificacionService.marcar_leida(1, 100)
        
        # Verificar
        assert result is True
        assert notificacion.leida is True
        assert notificacion.fecha_leida is not None
        mock_db.session.commit.assert_called_once()
    
    @patch('backend.services.notificacion_service.Notificacion')
    def test_marcar_leida_usuario_incorrecto(self, mock_notif_class):
        """Test que no se puede marcar notificación de otro usuario"""
        # Mock notificación
        notificacion = Mock()
        notificacion.id = 1
        notificacion.usuario_id = 100
        
        mock_notif_class.query.get.return_value = notificacion
        
        # Ejecutar con usuario diferente
        result = NotificacionService.marcar_leida(1, 200)
        
        # Verificar: debe fallar
        assert result is False
    
    @patch('backend.services.notificacion_service.Notificacion')
    def test_marcar_leida_no_existe(self, mock_notif_class):
        """Test marcar notificación que no existe"""
        mock_notif_class.query.get.return_value = None
        
        # Ejecutar
        result = NotificacionService.marcar_leida(999, 100)
        
        # Verificar
        assert result is False
    
    @patch('backend.services.notificacion_service.Notificacion')
    def test_obtener_notificaciones(self, mock_notif_class):
        """Test obtener notificaciones de un usuario"""
        # Mock query
        mock_query = Mock()
        mock_notif_class.query.filter_by.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.offset.return_value = mock_query
        
        notif1 = Mock()
        notif1.id = 1
        notif2 = Mock()
        notif2.id = 2
        mock_query.all.return_value = [notif1, notif2]
        
        # Ejecutar
        result = NotificacionService.obtener_notificaciones(100, solo_no_leidas=False)
        
        # Verificar
        assert len(result) == 2
        mock_notif_class.query.filter_by.assert_called_with(usuario_id=100)
    
    @patch('backend.services.notificacion_service.Notificacion')
    def test_obtener_notificaciones_solo_no_leidas(self, mock_notif_class):
        """Test obtener solo notificaciones no leídas"""
        # Mock query
        mock_query = Mock()
        mock_notif_class.query.filter_by.return_value = mock_query
        mock_query.filter_by.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.all.return_value = []
        
        # Ejecutar
        result = NotificacionService.obtener_notificaciones(100, solo_no_leidas=True)
        
        # Verificar que se filtró por leida=False
        assert mock_query.filter_by.call_count >= 1
    
    @patch('backend.services.notificacion_service.Notificacion')
    def test_contar_no_leidas(self, mock_notif_class):
        """Test contar notificaciones no leídas"""
        # Mock query
        mock_query = Mock()
        mock_notif_class.query.filter_by.return_value = mock_query
        mock_query.count.return_value = 5
        
        # Ejecutar
        result = NotificacionService.contar_no_leidas(100)
        
        # Verificar
        assert result == 5
        mock_notif_class.query.filter_by.assert_called_with(usuario_id=100, leida=False)
    
    @patch('backend.services.notificacion_service.ConfiguracionNotificaciones')
    def test_debe_notificar_incidente_sin_config(self, mock_config_class):
        """Test que notifica por defecto si no hay configuración"""
        mock_config_class.query.filter_by.return_value.first.return_value = None
        
        # Ejecutar
        result = NotificacionService._debe_notificar_incidente(100, 'alta')
        
        # Verificar: debe notificar por defecto
        assert result is True
    
    @patch('backend.services.notificacion_service.ConfiguracionNotificaciones')
    def test_debe_notificar_incidente_con_config(self, mock_config_class):
        """Test que respeta configuración de usuario"""
        # Mock configuración
        config = Mock()
        config.notificar_web = True
        config.notificar_incidentes_alta = False
        mock_config_class.query.filter_by.return_value.first.return_value = config
        
        # Ejecutar
        result = NotificacionService._debe_notificar_incidente(100, 'alta')
        
        # Verificar: no debe notificar según configuración
        assert result is False
    
    @patch('backend.services.notificacion_service.db')
    @patch('backend.services.notificacion_service.WebSocketService')
    def test_no_duplicar_notificaciones(self, mock_ws, mock_db):
        """Test que no se duplican notificaciones al mismo usuario"""
        # Mock incidente
        incidente = Mock()
        incidente.id = 1
        incidente.severidad = 'alta'
        incidente.tipo_incidente = 'retraso_apertura'
        incidente.descripcion = 'Test'
        
        # Mock mesa y puesto
        mesa = Mock()
        mesa.id = 100
        puesto = Mock()
        puesto.id = 10
        puesto.nombre = 'Puesto'
        puesto.municipio_id = 5
        puesto.departamento_id = 1
        mesa.puesto = puesto
        incidente.mesa = mesa
        
        # Mock coordinadores (mismo usuario en dos roles - caso edge)
        coord_puesto = Mock()
        coord_puesto.id = 50
        coord_municipal = Mock()
        coord_municipal.id = 50  # Mismo ID
        
        with patch.object(NotificacionService, '_get_coordinador_puesto', return_value=coord_puesto):
            with patch.object(NotificacionService, '_get_coordinador_municipal', return_value=coord_municipal):
                with patch.object(NotificacionService, '_get_coordinador_departamental', return_value=None):
                    with patch.object(NotificacionService, '_debe_notificar_incidente', return_value=True):
                        notificaciones_creadas = []
                        mock_db.session.add = lambda n: notificaciones_creadas.append(n)
                        mock_db.session.commit = Mock()
                        
                        # Ejecutar
                        result = NotificacionService.notificar_incidente(incidente)
                        
                        # Verificar: debe crear 2 notificaciones (una por cada rol)
                        # aunque sea el mismo usuario
                        assert len(notificaciones_creadas) == 2
