"""
Modelo para seguimiento de reportes (incidentes y delitos)
"""
from backend.database import db
from datetime import datetime


class SeguimientoReporte(db.Model):
    """Modelo para registro de seguimiento de reportes"""
    __tablename__ = 'seguimiento_reportes'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relación con reporte
    incidente_id = db.Column(db.Integer, db.ForeignKey('incidentes_electorales.id'), nullable=True)
    delito_id = db.Column(db.Integer, db.ForeignKey('delitos_electorales.id'), nullable=True)
    
    # Tipo de acción
    accion = db.Column(db.String(50), nullable=False)
    # Valores: 'crear', 'cambiar_estado', 'agregar_comentario', 'denunciar', 'resolver', 'escalar', 'exportar'
    
    # Detalles de la acción
    estado_anterior = db.Column(db.String(50), nullable=True)
    estado_nuevo = db.Column(db.String(50), nullable=True)
    comentario = db.Column(db.Text, nullable=True)
    
    # Usuario que realizó la acción
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Metadatos adicionales (JSON)
    metadatos = db.Column(db.JSON, nullable=True)
    
    # Auditoría
    fecha_accion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    
    # Relaciones
    usuario = db.relationship('User', backref='acciones_seguimiento')
    incidente = db.relationship('IncidenteElectoral', backref='seguimiento_detallado', foreign_keys=[incidente_id])
    delito = db.relationship('DelitoElectoral', backref='seguimiento_detallado', foreign_keys=[delito_id])
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'incidente_id': self.incidente_id,
            'delito_id': self.delito_id,
            'accion': self.accion,
            'estado_anterior': self.estado_anterior,
            'estado_nuevo': self.estado_nuevo,
            'comentario': self.comentario,
            'usuario_id': self.usuario_id,
            'usuario_nombre': self.usuario.nombre_completo if self.usuario else None,
            'usuario_rol': self.usuario.rol if self.usuario else None,
            'metadatos': self.metadatos,
            'fecha_accion': self.fecha_accion.isoformat(),
            'ip_address': self.ip_address
        }
    
    @staticmethod
    def registrar_accion(tipo_reporte, reporte_id, accion, usuario_id, **kwargs):
        """
        Registrar una acción de seguimiento
        
        Args:
            tipo_reporte: 'incidente' o 'delito'
            reporte_id: ID del reporte
            accion: Tipo de acción
            usuario_id: ID del usuario
            **kwargs: Campos adicionales (estado_anterior, estado_nuevo, comentario, etc.)
        
        Returns:
            SeguimientoReporte: Registro creado
        """
        seguimiento = SeguimientoReporte(
            incidente_id=reporte_id if tipo_reporte == 'incidente' else None,
            delito_id=reporte_id if tipo_reporte == 'delito' else None,
            accion=accion,
            usuario_id=usuario_id,
            estado_anterior=kwargs.get('estado_anterior'),
            estado_nuevo=kwargs.get('estado_nuevo'),
            comentario=kwargs.get('comentario'),
            metadatos=kwargs.get('metadatos'),
            ip_address=kwargs.get('ip_address'),
            user_agent=kwargs.get('user_agent')
        )
        
        db.session.add(seguimiento)
        db.session.commit()
        
        return seguimiento
    
    @staticmethod
    def obtener_seguimiento(tipo_reporte, reporte_id):
        """
        Obtener seguimiento de un reporte
        
        Args:
            tipo_reporte: 'incidente' o 'delito'
            reporte_id: ID del reporte
            
        Returns:
            list: Lista de registros de seguimiento
        """
        if tipo_reporte == 'incidente':
            return SeguimientoReporte.query.filter_by(
                incidente_id=reporte_id
            ).order_by(SeguimientoReporte.fecha_accion.desc()).all()
        else:
            return SeguimientoReporte.query.filter_by(
                delito_id=reporte_id
            ).order_by(SeguimientoReporte.fecha_accion.desc()).all()
