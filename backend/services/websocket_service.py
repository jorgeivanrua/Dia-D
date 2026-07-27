"""
WebSocket Service Stub - Temporal mientras se instala flask-socketio
"""
import logging

logger = logging.getLogger(__name__)


class WebSocketService:
    """Stub temporal para WebSocketService"""
    
    @staticmethod
    def emit_to_user(user_id, event, data):
        """Stub - no hace nada sin socketio"""
        logger.debug(f"WebSocket deshabilitado - evento {event} para usuario {user_id}")
        pass
    
    @staticmethod
    def emit_to_all(event, data):
        """Stub - no hace nada sin socketio"""
        logger.debug(f"WebSocket deshabilitado - evento {event} para todos")
        pass
    
    @staticmethod
    def emit_to_room(room, event, data):
        """Stub - no hace nada sin socketio"""
        logger.debug(f"WebSocket deshabilitado - evento {event} para room {room}")
        pass
