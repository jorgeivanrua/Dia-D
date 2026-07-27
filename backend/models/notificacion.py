"""
Modelos para sistema de notificaciones
"""
from backend.database import db
from datetime import datetime


class Notificacion(db.Model):
    """Modelo para notificaciones del sistema"""
    __tablename__ = 'notificaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Destinatario
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Tipo de notificación
    tipo = db.Column(db.String(50), nullable=False)  # 'nuevo_incidente', 'nuevo_delito', 'cambio_estado'
    
    # Contenido
    titulo = db.Column(db.String(200), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    
    # Referencia al reporte
    incidente_id = db.Column(db.Integer, db.ForeignKey('incidentes_electorales.id'), nullable=True)
    delito_id = db.Column(db.Integer, db.ForeignKey('delitos_electorales.id'), nullable=True)
    
    # Estado
    leida = db.Column(db.Boolean, default=False)
    fecha_leida = db.Column(db.DateTime, nullable=True)
    
    # Metadatos
    severidad = db.Column(db.String(20), nullable=True)  # Para incidentes
    gravedad = db.Column(db.String(20), nullable=True)  # Para delitos
    
    # Auditoría
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    enviada_realtime = db.Column(db.Boolean, default=False)
    fecha_envio_realtime = db.Column(db.DateTime, nullable=True)
    
    # Relaciones
    usuario = db.relationship('User', backref='notificaciones')
    incidente = db.relationship('IncidenteElectoral', backref='notificaciones', foreign_keys=[incidente_id])
    delito = db.relationship('DelitoElectoral', backref='notificaciones', foreign_keys=[delito_id])
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'tipo': self.tipo,
            'titulo': self.titulo,
            'mensaje': self.mensaje,
            'incidente_id': self.incidente_id,
            'delito_id': self.delito_id,
            'leida': self.leida,
            'fecha_leida': self.fecha_leida.isoformat() if self.fecha_leida else None,
            'severidad': self.severidad,
            'gravedad': self.gravedad,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'enviada_realtime': self.enviada_realtime
        }


class ConfiguracionNotificaciones(db.Model):
    """Configuración de notificaciones por usuario"""
    __tablename__ = 'configuracion_notificaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Preferencias de notificación por severidad
    notificar_incidentes_baja = db.Column(db.Boolean, default=True)
    notificar_incidentes_media = db.Column(db.Boolean, default=True)
    notificar_incidentes_alta = db.Column(db.Boolean, default=True)
    notificar_incidentes_critica = db.Column(db.Boolean, default=True)
    notificar_delitos = db.Column(db.Boolean, default=True)
    notificar_cambios_estado = db.Column(db.Boolean, default=True)
    
    # Canales de notificación
    notificar_web = db.Column(db.Boolean, default=True)
    notificar_email = db.Column(db.Boolean, default=False)
    notificar_sms = db.Column(db.Boolean, default=False)
    
    # Auditoría
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    usuario = db.relationship('User', backref='config_notificaciones')
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'notificar_incidentes_baja': self.notificar_incidentes_baja,
            'notificar_incidentes_media': self.notificar_incidentes_media,
            'notificar_incidentes_alta': self.notificar_incidentes_alta,
            'notificar_incidentes_critica': self.notificar_incidentes_critica,
            'notificar_delitos': self.notificar_delitos,
            'notificar_cambios_estado': self.notificar_cambios_estado,
            'notificar_web': self.notificar_web,
            'notificar_email': self.notificar_email,
            'notificar_sms': self.notificar_sms
        }
