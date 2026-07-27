"""
Servicio para gestión de notificaciones
"""
from backend.database import db
from backend.models.notificacion import Notificacion, ConfiguracionNotificaciones
from backend.models.user import User
try:
    from backend.services.websocket_service import WebSocketService
except:
    from backend.services.websocket_service_stub import WebSocketService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class NotificacionService:
    """
    Servicio para crear y enviar notificaciones
    """
    
    @staticmethod
    def notificar_incidente(incidente):
        """
        Crear notificaciones para un nuevo incidente
        
        Lógica de notificación según severidad:
        - Baja/Media: Coordinador de puesto
        - Alta: Coordinador de puesto + Coordinador municipal
        - Crítica: Coordinador de puesto + Coordinador municipal + Coordinador departamental
        
        Args:
            incidente: Instancia de IncidenteElectoral
            
        Returns:
            list: Lista de notificaciones creadas
        """
        try:
            notificaciones = []
            destinatarios = []
            
            # Obtener información del puesto y mesa
            mesa = incidente.mesa
            if not mesa:
                logger.error(f'Incidente {incidente.id} sin mesa asociada')
                return []
            
            puesto = mesa.puesto
            if not puesto:
                logger.error(f'Mesa {mesa.id} sin puesto asociado')
                return []
            
            # Determinar destinatarios según severidad
            severidad = incidente.severidad.lower() if incidente.severidad else 'baja'
            
            # 1. Coordinador de puesto (siempre)
            coordinador_puesto = NotificacionService._get_coordinador_puesto(puesto.id)
            if coordinador_puesto:
                destinatarios.append(coordinador_puesto)
            
            # 2. Coordinador municipal (si severidad >= alta)
            if severidad in ['alta', 'crítica', 'critica']:
                coordinador_municipal = NotificacionService._get_coordinador_municipal(puesto.municipio_id)
                if coordinador_municipal:
                    destinatarios.append(coordinador_municipal)
            
            # 3. Coordinador departamental (si severidad == crítica)
            if severidad in ['crítica', 'critica']:
                coordinador_departamental = NotificacionService._get_coordinador_departamental(puesto.departamento_id)
                if coordinador_departamental:
                    destinatarios.append(coordinador_departamental)
            
            # Crear notificaciones
            titulo = f'Nuevo Incidente - Severidad {incidente.severidad}'
            mensaje = f'Se ha reportado un incidente de tipo "{incidente.tipo_incidente}" en {puesto.nombre}. '
            mensaje += f'Descripción: {incidente.descripcion[:100]}...' if len(incidente.descripcion) > 100 else incidente.descripcion
            
            for usuario in destinatarios:
                # Verificar configuración de notificaciones del usuario
                if not NotificacionService._debe_notificar_incidente(usuario.id, severidad):
                    continue
                
                notificacion = Notificacion(
                    usuario_id=usuario.id,
                    tipo='nuevo_incidente',
                    titulo=titulo,
                    mensaje=mensaje,
                    incidente_id=incidente.id,
                    severidad=incidente.severidad
                )
                db.session.add(notificacion)
                notificaciones.append(notificacion)
            
            db.session.commit()
            
            # Enviar notificaciones en tiempo real
            for notificacion in notificaciones:
                NotificacionService._enviar_realtime(notificacion)
            
            # Actualizar mapa globalmente
            WebSocketService.notify_mapa_update()
            
            logger.info(f'Creadas {len(notificaciones)} notificaciones para incidente {incidente.id}')
            return notificaciones
            
        except Exception as e:
            logger.error(f'Error creando notificaciones para incidente: {str(e)}')
            db.session.rollback()
            return []
    
    @staticmethod
    def notificar_delito(delito):
        """
        Crear notificaciones para un nuevo delito
        
        Lógica de notificación:
        - Siempre: Coordinador municipal + Coordinador departamental + Auditores
        
        Args:
            delito: Instancia de DelitoElectoral
            
        Returns:
            list: Lista de notificaciones creadas
        """
        try:
            notificaciones = []
            destinatarios = []
            
            # Obtener información del puesto y mesa
            mesa = delito.mesa
            if not mesa:
                logger.error(f'Delito {delito.id} sin mesa asociada')
                return []
            
            puesto = mesa.puesto
            if not puesto:
                logger.error(f'Mesa {mesa.id} sin puesto asociado')
                return []
            
            # 1. Coordinador municipal
            coordinador_municipal = NotificacionService._get_coordinador_municipal(puesto.municipio_id)
            if coordinador_municipal:
                destinatarios.append(coordinador_municipal)
            
            # 2. Coordinador departamental
            coordinador_departamental = NotificacionService._get_coordinador_departamental(puesto.departamento_id)
            if coordinador_departamental:
                destinatarios.append(coordinador_departamental)
            
            # 3. Auditores (todos)
            auditores = NotificacionService._get_auditores()
            destinatarios.extend(auditores)
            
            # Crear notificaciones
            titulo = f'Nuevo Delito Electoral - Gravedad {delito.gravedad}'
            mensaje = f'Se ha reportado un delito electoral de tipo "{delito.tipo_delito}" en {puesto.nombre}. '
            mensaje += f'Descripción: {delito.descripcion[:100]}...' if len(delito.descripcion) > 100 else delito.descripcion
            
            for usuario in destinatarios:
                # Verificar configuración de notificaciones del usuario
                if not NotificacionService._debe_notificar_delito(usuario.id):
                    continue
                
                notificacion = Notificacion(
                    usuario_id=usuario.id,
                    tipo='nuevo_delito',
                    titulo=titulo,
                    mensaje=mensaje,
                    delito_id=delito.id,
                    gravedad=delito.gravedad
                )
                db.session.add(notificacion)
                notificaciones.append(notificacion)
            
            db.session.commit()
            
            # Enviar notificaciones en tiempo real
            for notificacion in notificaciones:
                NotificacionService._enviar_realtime(notificacion)
            
            # Actualizar mapa globalmente
            WebSocketService.notify_mapa_update()
            
            logger.info(f'Creadas {len(notificaciones)} notificaciones para delito {delito.id}')
            return notificaciones
            
        except Exception as e:
            logger.error(f'Error creando notificaciones para delito: {str(e)}')
            db.session.rollback()
            return []
    
    @staticmethod
    def notificar_cambio_estado(reporte, tipo_reporte, estado_anterior, estado_nuevo, usuario_actualizador):
        """
        Notificar al reportante sobre cambio de estado
        
        Args:
            reporte: Instancia de IncidenteElectoral o DelitoElectoral
            tipo_reporte: 'incidente' o 'delito'
            estado_anterior: Estado anterior
            estado_nuevo: Estado nuevo
            usuario_actualizador: Usuario que realizó el cambio
            
        Returns:
            Notificacion: Notificación creada
        """
        try:
            # Obtener reportante
            reportante_id = reporte.reportado_por_id
            if not reportante_id:
                logger.warning(f'{tipo_reporte.capitalize()} {reporte.id} sin reportante')
                return None
            
            # No notificar si el reportante es quien actualizó
            if reportante_id == usuario_actualizador.id:
                return None
            
            # Verificar configuración de notificaciones
            if not NotificacionService._debe_notificar_cambio_estado(reportante_id):
                return None
            
            # Crear notificación
            titulo = f'Actualización de {tipo_reporte.capitalize()}'
            mensaje = f'El estado de tu {tipo_reporte} ha cambiado de "{estado_anterior}" a "{estado_nuevo}". '
            mensaje += f'Actualizado por: {usuario_actualizador.nombre_completo}'
            
            notificacion = Notificacion(
                usuario_id=reportante_id,
                tipo='cambio_estado',
                titulo=titulo,
                mensaje=mensaje,
                incidente_id=reporte.id if tipo_reporte == 'incidente' else None,
                delito_id=reporte.id if tipo_reporte == 'delito' else None
            )
            
            db.session.add(notificacion)
            db.session.commit()
            
            # Enviar en tiempo real
            NotificacionService._enviar_realtime(notificacion)
            
            logger.info(f'Notificación de cambio de estado enviada a usuario {reportante_id}')
            return notificacion
            
        except Exception as e:
            logger.error(f'Error creando notificación de cambio de estado: {str(e)}')
            db.session.rollback()
            return None
    
    @staticmethod
    def marcar_leida(notificacion_id, usuario_id):
        """
        Marcar notificación como leída
        
        Args:
            notificacion_id: ID de la notificación
            usuario_id: ID del usuario (para validar permisos)
            
        Returns:
            bool: True si se marcó correctamente
        """
        try:
            notificacion = Notificacion.query.get(notificacion_id)
            if not notificacion:
                return False
            
            # Validar que la notificación pertenece al usuario
            if notificacion.usuario_id != usuario_id:
                logger.warning(f'Usuario {usuario_id} intentó marcar notificación {notificacion_id} de otro usuario')
                return False
            
            notificacion.leida = True
            notificacion.fecha_leida = datetime.utcnow()
            db.session.commit()
            
            return True
            
        except Exception as e:
            logger.error(f'Error marcando notificación como leída: {str(e)}')
            db.session.rollback()
            return False
    
    @staticmethod
    def obtener_notificaciones(usuario_id, solo_no_leidas=False, limit=50, offset=0):
        """
        Obtener notificaciones de un usuario
        
        Args:
            usuario_id: ID del usuario
            solo_no_leidas: Si True, solo retorna no leídas
            limit: Número máximo de resultados
            offset: Offset para paginación
            
        Returns:
            list: Lista de notificaciones
        """
        try:
            query = Notificacion.query.filter_by(usuario_id=usuario_id)
            
            if solo_no_leidas:
                query = query.filter_by(leida=False)
            
            query = query.order_by(Notificacion.fecha_creacion.desc())
            query = query.limit(limit).offset(offset)
            
            return query.all()
            
        except Exception as e:
            logger.error(f'Error obteniendo notificaciones: {str(e)}')
            return []
    
    @staticmethod
    def contar_no_leidas(usuario_id):
        """
        Contar notificaciones no leídas de un usuario
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            int: Número de notificaciones no leídas
        """
        try:
            return Notificacion.query.filter_by(
                usuario_id=usuario_id,
                leida=False
            ).count()
        except Exception as e:
            logger.error(f'Error contando notificaciones no leídas: {str(e)}')
            return 0
    
    # Métodos privados auxiliares
    
    @staticmethod
    def _get_coordinador_puesto(puesto_id):
        """Obtener coordinador de un puesto"""
        from backend.models.puesto import Puesto
        puesto = Puesto.query.get(puesto_id)
        return puesto.coordinador if puesto and puesto.coordinador else None
    
    @staticmethod
    def _get_coordinador_municipal(municipio_id):
        """Obtener coordinador municipal"""
        coordinador = User.query.filter_by(
            rol='coordinador_municipal',
            municipio_id=municipio_id
        ).first()
        return coordinador
    
    @staticmethod
    def _get_coordinador_departamental(departamento_id):
        """Obtener coordinador departamental"""
        coordinador = User.query.filter_by(
            rol='coordinador_departamental',
            departamento_id=departamento_id
        ).first()
        return coordinador
    
    @staticmethod
    def _get_auditores():
        """Obtener todos los auditores"""
        return User.query.filter_by(rol='auditor').all()
    
    @staticmethod
    def _debe_notificar_incidente(usuario_id, severidad):
        """Verificar si se debe notificar un incidente según configuración"""
        config = ConfiguracionNotificaciones.query.filter_by(usuario_id=usuario_id).first()
        
        # Si no hay configuración, notificar por defecto
        if not config or not config.notificar_web:
            return True
        
        # Verificar según severidad
        severidad_lower = severidad.lower()
        if severidad_lower == 'baja':
            return config.notificar_incidentes_baja
        elif severidad_lower == 'media':
            return config.notificar_incidentes_media
        elif severidad_lower == 'alta':
            return config.notificar_incidentes_alta
        elif severidad_lower in ['crítica', 'critica']:
            return config.notificar_incidentes_critica
        
        return True
    
    @staticmethod
    def _debe_notificar_delito(usuario_id):
        """Verificar si se debe notificar un delito según configuración"""
        config = ConfiguracionNotificaciones.query.filter_by(usuario_id=usuario_id).first()
        
        # Si no hay configuración, notificar por defecto
        if not config or not config.notificar_web:
            return True
        
        return config.notificar_delitos
    
    @staticmethod
    def _debe_notificar_cambio_estado(usuario_id):
        """Verificar si se debe notificar cambios de estado según configuración"""
        config = ConfiguracionNotificaciones.query.filter_by(usuario_id=usuario_id).first()
        
        # Si no hay configuración, notificar por defecto
        if not config or not config.notificar_web:
            return True
        
        return config.notificar_cambios_estado
    
    @staticmethod
    def _enviar_realtime(notificacion):
        """
        Enviar notificación en tiempo real por WebSocket
        
        Args:
            notificacion: Instancia de Notificacion
        """
        try:
            # Preparar datos para enviar
            data = notificacion.to_dict()
            
            # Enviar por WebSocket
            success = WebSocketService.emit_to_user(
                notificacion.usuario_id,
                'nueva_notificacion',
                data
            )
            
            if success:
                notificacion.enviada_realtime = True
                notificacion.fecha_envio_realtime = datetime.utcnow()
                db.session.commit()
            
        except Exception as e:
            logger.error(f'Error enviando notificación en tiempo real: {str(e)}')
