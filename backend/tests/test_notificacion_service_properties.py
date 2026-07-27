"""
Property-based tests para NotificacionService
"""
import pytest
from hypothesis import given, strategies as st, settings, assume
from unittest.mock import Mock, patch, MagicMock
from backend.services.notificacion_service import NotificacionService
from backend.models.notificacion import Notificacion
from backend.models.user import User
from datetime import datetime


# Estrategias personalizadas para generar datos del dominio

@st.composite
def incidente_strategy(draw):
    """Generar incidente de prueba con severidad aleatoria"""
    severidades = ['baja', 'media', 'alta', 'crítica', 'critica']
    
    incidente = Mock()
    incidente.id = draw(st.integers(min_value=1, max_value=10000))
    incidente.severidad = draw(st.sampled_from(severidades))
    incidente.tipo_incidente = draw(st.sampled_from([
        'retraso_apertura', 'falta_material', 'problemas_tecnicos',
        'irregularidades_proceso', 'ausencia_funcionarios'
    ]))
    incidente.descripcion = draw(st.text(min_size=10, max_size=200))
    incidente.reportado_por_id = draw(st.integers(min_value=1, max_value=1000))
    
    # Mock mesa y puesto
    mesa = Mock()
    mesa.id = draw(st.integers(min_value=1, max_value=5000))
    mesa.mesa_codigo = f"MESA-{mesa.id}"
    
    puesto = Mock()
    puesto.id = draw(st.integers(min_value=1, max_value=1000))
    puesto.nombre = f"Puesto {puesto.id}"
    puesto.municipio_id = draw(st.integers(min_value=1, max_value=100))
    puesto.departamento_id = draw(st.integers(min_value=1, max_value=32))
    
    mesa.puesto = puesto
    incidente.mesa = mesa
    
    return incidente


@st.composite
def delito_strategy(draw):
    """Generar delito de prueba con gravedad aleatoria"""
    gravedades = ['leve', 'grave', 'muy_grave']
    
    delito = Mock()
    delito.id = draw(st.integers(min_value=1, max_value=10000))
    delito.gravedad = draw(st.sampled_from(gravedades))
    delito.tipo_delito = draw(st.sampled_from([
        'compra_votos', 'coaccion', 'fraude_electoral',
        'violencia', 'suplantacion'
    ]))
    delito.descripcion = draw(st.text(min_size=10, max_size=200))
    delito.reportado_por_id = draw(st.integers(min_value=1, max_value=1000))
    
    # Mock mesa y puesto
    mesa = Mock()
    mesa.id = draw(st.integers(min_value=1, max_value=5000))
    mesa.mesa_codigo = f"MESA-{mesa.id}"
    
    puesto = Mock()
    puesto.id = draw(st.integers(min_value=1, max_value=1000))
    puesto.nombre = f"Puesto {puesto.id}"
    puesto.municipio_id = draw(st.integers(min_value=1, max_value=100))
    puesto.departamento_id = draw(st.integers(min_value=1, max_value=32))
    
    mesa.puesto = puesto
    delito.mesa = mesa
    
    return delito


@st.composite
def usuario_strategy(draw, rol=None):
    """Generar usuario de prueba"""
    roles = ['testigo', 'coordinador_puesto', 'coordinador_municipal', 
             'coordinador_departamental', 'auditor', 'super_admin']
    
    usuario = Mock()
    usuario.id = draw(st.integers(min_value=1, max_value=10000))
    usuario.rol = rol if rol else draw(st.sampled_from(roles))
    usuario.nombre_completo = draw(st.text(min_size=5, max_size=50))
    usuario.email = f"user{usuario.id}@test.com"
    
    return usuario


class TestNotificacionServiceProperties:
    """Property tests para NotificacionService"""
    
    @given(incidente=incidente_strategy())
    @settings(max_examples=100)
    @patch('backend.services.notificacion_service.db')
    @patch('backend.services.notificacion_service.WebSocketService')
    def test_property_notificacion_coordinador_puesto(self, mock_ws, mock_db, incidente):
        """
        Property 2: Notificación a coordinador de puesto
        
        Para cualquier incidente creado, debe existir al menos una notificación
        para el coordinador de puesto correspondiente.
        
        Validates: Requirements 1.5
        """
        # Mock coordinador de puesto
        coordinador = Mock()
        coordinador.id = 999
        coordinador.rol = 'coordinador_puesto'
        
        with patch.object(NotificacionService, '_get_coordinador_puesto', return_value=coordinador):
            with patch.object(NotificacionService, '_get_coordinador_municipal', return_value=None):
                with patch.object(NotificacionService, '_get_coordinador_departamental', return_value=None):
                    with patch.object(NotificacionService, '_debe_notificar_incidente', return_value=True):
                        # Capturar notificaciones creadas
                        notificaciones_creadas = []
                        
                        def mock_add(notificacion):
                            notificaciones_creadas.append(notificacion)
                        
                        mock_db.session.add = mock_add
                        mock_db.session.commit = Mock()
                        
                        # Ejecutar
                        NotificacionService.notificar_incidente(incidente)
                        
                        # Verificar: debe haber al menos una notificación para el coordinador de puesto
                        notificaciones_coordinador = [
                            n for n in notificaciones_creadas 
                            if n.usuario_id == coordinador.id
                        ]
                        
                        assert len(notificaciones_coordinador) >= 1, \
                            f"Debe existir al menos una notificación para coordinador de puesto"
    
    @given(incidente=incidente_strategy())
    @settings(max_examples=100)
    @patch('backend.services.notificacion_service.db')
    @patch('backend.services.notificacion_service.WebSocketService')
    def test_property_notificacion_severidad_critica(self, mock_ws, mock_db, incidente):
        """
        Property 3: Notificación por severidad crítica
        
        Para cualquier incidente con severidad "crítica", deben existir notificaciones
        para coordinador de puesto, coordinador municipal y coordinador departamental.
        
        Validates: Requirements 1.6, 4.3
        """
        # Forzar severidad crítica
        incidente.severidad = 'crítica'
        
        # Mock coordinadores
        coord_puesto = Mock()
        coord_puesto.id = 100
        coord_puesto.rol = 'coordinador_puesto'
        
        coord_municipal = Mock()
        coord_municipal.id = 200
        coord_municipal.rol = 'coordinador_municipal'
        
        coord_departamental = Mock()
        coord_departamental.id = 300
        coord_departamental.rol = 'coordinador_departamental'
        
        with patch.object(NotificacionService, '_get_coordinador_puesto', return_value=coord_puesto):
            with patch.object(NotificacionService, '_get_coordinador_municipal', return_value=coord_municipal):
                with patch.object(NotificacionService, '_get_coordinador_departamental', return_value=coord_departamental):
                    with patch.object(NotificacionService, '_debe_notificar_incidente', return_value=True):
                        # Capturar notificaciones creadas
                        notificaciones_creadas = []
                        
                        def mock_add(notificacion):
                            notificaciones_creadas.append(notificacion)
                        
                        mock_db.session.add = mock_add
                        mock_db.session.commit = Mock()
                        
                        # Ejecutar
                        NotificacionService.notificar_incidente(incidente)
                        
                        # Verificar: deben existir notificaciones para los 3 niveles
                        usuarios_notificados = {n.usuario_id for n in notificaciones_creadas}
                        
                        assert coord_puesto.id in usuarios_notificados, \
                            "Debe notificar a coordinador de puesto en incidente crítico"
                        assert coord_municipal.id in usuarios_notificados, \
                            "Debe notificar a coordinador municipal en incidente crítico"
                        assert coord_departamental.id in usuarios_notificados, \
                            "Debe notificar a coordinador departamental en incidente crítico"
    
    @given(incidente=incidente_strategy())
    @settings(max_examples=50)
    @patch('backend.services.notificacion_service.db')
    @patch('backend.services.notificacion_service.WebSocketService')
    def test_property_notificacion_severidad_alta(self, mock_ws, mock_db, incidente):
        """
        Property: Notificación por severidad alta
        
        Para cualquier incidente con severidad "alta", deben existir notificaciones
        para coordinador de puesto y coordinador municipal (pero no departamental).
        
        Validates: Requirements 1.6, 4.3
        """
        # Forzar severidad alta
        incidente.severidad = 'alta'
        
        # Mock coordinadores
        coord_puesto = Mock()
        coord_puesto.id = 100
        
        coord_municipal = Mock()
        coord_municipal.id = 200
        
        coord_departamental = Mock()
        coord_departamental.id = 300
        
        with patch.object(NotificacionService, '_get_coordinador_puesto', return_value=coord_puesto):
            with patch.object(NotificacionService, '_get_coordinador_municipal', return_value=coord_municipal):
                with patch.object(NotificacionService, '_get_coordinador_departamental', return_value=coord_departamental):
                    with patch.object(NotificacionService, '_debe_notificar_incidente', return_value=True):
                        # Capturar notificaciones creadas
                        notificaciones_creadas = []
                        
                        def mock_add(notificacion):
                            notificaciones_creadas.append(notificacion)
                        
                        mock_db.session.add = mock_add
                        mock_db.session.commit = Mock()
                        
                        # Ejecutar
                        NotificacionService.notificar_incidente(incidente)
                        
                        # Verificar
                        usuarios_notificados = {n.usuario_id for n in notificaciones_creadas}
                        
                        assert coord_puesto.id in usuarios_notificados, \
                            "Debe notificar a coordinador de puesto en incidente alta"
                        assert coord_municipal.id in usuarios_notificados, \
                            "Debe notificar a coordinador municipal en incidente alta"
                        assert coord_departamental.id not in usuarios_notificados, \
                            "NO debe notificar a coordinador departamental en incidente alta"
    
    @given(incidente=incidente_strategy())
    @settings(max_examples=50)
    @patch('backend.services.notificacion_service.db')
    @patch('backend.services.notificacion_service.WebSocketService')
    def test_property_notificacion_severidad_baja_media(self, mock_ws, mock_db, incidente):
        """
        Property: Notificación por severidad baja/media
        
        Para cualquier incidente con severidad "baja" o "media", debe existir
        notificación solo para coordinador de puesto.
        
        Validates: Requirements 1.5, 4.1
        """
        # Forzar severidad baja o media
        incidente.severidad = 'baja' if incidente.id % 2 == 0 else 'media'
        
        # Mock coordinadores
        coord_puesto = Mock()
        coord_puesto.id = 100
        
        coord_municipal = Mock()
        coord_municipal.id = 200
        
        coord_departamental = Mock()
        coord_departamental.id = 300
        
        with patch.object(NotificacionService, '_get_coordinador_puesto', return_value=coord_puesto):
            with patch.object(NotificacionService, '_get_coordinador_municipal', return_value=coord_municipal):
                with patch.object(NotificacionService, '_get_coordinador_departamental', return_value=coord_departamental):
                    with patch.object(NotificacionService, '_debe_notificar_incidente', return_value=True):
                        # Capturar notificaciones creadas
                        notificaciones_creadas = []
                        
                        def mock_add(notificacion):
                            notificaciones_creadas.append(notificacion)
                        
                        mock_db.session.add = mock_add
                        mock_db.session.commit = Mock()
                        
                        # Ejecutar
                        NotificacionService.notificar_incidente(incidente)
                        
                        # Verificar
                        usuarios_notificados = {n.usuario_id for n in notificaciones_creadas}
                        
                        assert coord_puesto.id in usuarios_notificados, \
                            f"Debe notificar a coordinador de puesto en incidente {incidente.severidad}"
                        assert coord_municipal.id not in usuarios_notificados, \
                            f"NO debe notificar a coordinador municipal en incidente {incidente.severidad}"
                        assert coord_departamental.id not in usuarios_notificados, \
                            f"NO debe notificar a coordinador departamental en incidente {incidente.severidad}"


class TestNotificacionDelitosProperties:
    """Property tests para notificaciones de delitos"""
    
    @given(delito=delito_strategy())
    @settings(max_examples=100)
    @patch('backend.services.notificacion_service.db')
    @patch('backend.services.notificacion_service.WebSocketService')
    @patch('backend.services.notificacion_service.User')
    def test_property_notificacion_delitos(self, mock_user_class, mock_ws, mock_db, delito):
        """
        Property 4: Notificación de delitos
        
        Para cualquier delito creado, deben existir notificaciones para
        coordinador municipal, coordinador departamental y todos los auditores.
        
        Validates: Requirements 2.3, 4.4
        """
        # Mock coordinadores
        coord_municipal = Mock()
        coord_municipal.id = 200
        coord_municipal.rol = 'coordinador_municipal'
        
        coord_departamental = Mock()
        coord_departamental.id = 300
        coord_departamental.rol = 'coordinador_departamental'
        
        # Mock auditores
        auditor1 = Mock()
        auditor1.id = 400
        auditor1.rol = 'auditor'
        
        auditor2 = Mock()
        auditor2.id = 500
        auditor2.rol = 'auditor'
        
        auditores = [auditor1, auditor2]
        
        with patch.object(NotificacionService, '_get_coordinador_municipal', return_value=coord_municipal):
            with patch.object(NotificacionService, '_get_coordinador_departamental', return_value=coord_departamental):
                with patch.object(NotificacionService, '_get_auditores', return_value=auditores):
                    with patch.object(NotificacionService, '_debe_notificar_delito', return_value=True):
                        # Capturar notificaciones creadas
                        notificaciones_creadas = []
                        
                        def mock_add(notificacion):
                            notificaciones_creadas.append(notificacion)
                        
                        mock_db.session.add = mock_add
                        mock_db.session.commit = Mock()
                        
                        # Ejecutar
                        NotificacionService.notificar_delito(delito)
                        
                        # Verificar: deben existir notificaciones para coordinadores y auditores
                        usuarios_notificados = {n.usuario_id for n in notificaciones_creadas}
                        
                        assert coord_municipal.id in usuarios_notificados, \
                            "Debe notificar a coordinador municipal en delito"
                        assert coord_departamental.id in usuarios_notificados, \
                            "Debe notificar a coordinador departamental en delito"
                        assert auditor1.id in usuarios_notificados, \
                            "Debe notificar a auditor 1 en delito"
                        assert auditor2.id in usuarios_notificados, \
                            "Debe notificar a auditor 2 en delito"
                        
                        # Verificar que se notificó a todos (2 coordinadores + 2 auditores = 4)
                        assert len(usuarios_notificados) >= 4, \
                            f"Debe notificar a al menos 4 usuarios en delito, notificó a {len(usuarios_notificados)}"
    
    @given(delito=delito_strategy())
    @settings(max_examples=50)
    @patch('backend.services.notificacion_service.db')
    @patch('backend.services.notificacion_service.WebSocketService')
    def test_property_delito_tipo_notificacion(self, mock_ws, mock_db, delito):
        """
        Property: Tipo de notificación para delitos
        
        Para cualquier delito, todas las notificaciones creadas deben tener
        tipo='nuevo_delito' y delito_id correcto.
        
        Validates: Requirements 2.3, 4.4
        """
        # Mock coordinadores y auditores
        coord_municipal = Mock()
        coord_municipal.id = 200
        
        coord_departamental = Mock()
        coord_departamental.id = 300
        
        auditor = Mock()
        auditor.id = 400
        
        with patch.object(NotificacionService, '_get_coordinador_municipal', return_value=coord_municipal):
            with patch.object(NotificacionService, '_get_coordinador_departamental', return_value=coord_departamental):
                with patch.object(NotificacionService, '_get_auditores', return_value=[auditor]):
                    with patch.object(NotificacionService, '_debe_notificar_delito', return_value=True):
                        # Capturar notificaciones creadas
                        notificaciones_creadas = []
                        
                        def mock_add(notificacion):
                            notificaciones_creadas.append(notificacion)
                        
                        mock_db.session.add = mock_add
                        mock_db.session.commit = Mock()
                        
                        # Ejecutar
                        NotificacionService.notificar_delito(delito)
                        
                        # Verificar: todas las notificaciones deben ser de tipo 'nuevo_delito'
                        for notificacion in notificaciones_creadas:
                            assert notificacion.tipo == 'nuevo_delito', \
                                f"Notificación debe ser tipo 'nuevo_delito', es '{notificacion.tipo}'"
                            assert notificacion.delito_id == delito.id, \
                                f"Notificación debe tener delito_id={delito.id}, tiene {notificacion.delito_id}"
                            assert notificacion.incidente_id is None, \
                                "Notificación de delito no debe tener incidente_id"
