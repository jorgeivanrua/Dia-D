"""
Modelos para funcionalidades del coordinador municipal
"""
from backend.database import db
from datetime import datetime


class FormularioE24Puesto(db.Model):
    """Formulario E-24 consolidado de puesto"""
    __tablename__ = 'formularios_e24_puesto'
    
    id = db.Column(db.Integer, primary_key=True)
    puesto_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    coordinador_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tipo_eleccion_id = db.Column(db.Integer, db.ForeignKey('tipos_eleccion.id'), nullable=False)
    
    # Datos consolidados del puesto
    total_mesas = db.Column(db.Integer, nullable=False)
    mesas_incluidas = db.Column(db.Integer, nullable=False)
    total_votantes_registrados = db.Column(db.Integer, nullable=False)
    total_votos = db.Column(db.Integer, nullable=False)
    votos_validos = db.Column(db.Integer, nullable=False)
    votos_nulos = db.Column(db.Integer, nullable=False)
    votos_blanco = db.Column(db.Integer, nullable=False)
    
    # Archivo PDF
    pdf_url = db.Column(db.String(500), nullable=False)
    pdf_hash = db.Column(db.String(64))  # SHA-256
    
    # Metadatos
    version = db.Column(db.Integer, default=1)
    observaciones = db.Column(db.Text)
    
    # Auditoría
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    puesto = db.relationship('Location', foreign_keys=[puesto_id])
    coordinador = db.relationship('User', foreign_keys=[coordinador_id])
    tipo_eleccion = db.relationship('TipoEleccion')
    votos_partidos = db.relationship('VotoPartidoE24Puesto', back_populates='e24_puesto', cascade='all, delete-orphan')
    
    def to_dict(self, include_votos=False):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'puesto_id': self.puesto_id,
            'coordinador_id': self.coordinador_id,
            'tipo_eleccion_id': self.tipo_eleccion_id,
            'total_mesas': self.total_mesas,
            'mesas_incluidas': self.mesas_incluidas,
            'total_votantes_registrados': self.total_votantes_registrados,
            'total_votos': self.total_votos,
            'votos_validos': self.votos_validos,
            'votos_nulos': self.votos_nulos,
            'votos_blanco': self.votos_blanco,
            'pdf_url': self.pdf_url,
            'pdf_hash': self.pdf_hash,
            'version': self.version,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if self.puesto:
            data['puesto_nombre'] = self.puesto.puesto_nombre or self.puesto.nombre_completo
            data['puesto_codigo'] = self.puesto.puesto_codigo
        
        if self.coordinador:
            data['coordinador_nombre'] = self.coordinador.nombre
        
        if self.tipo_eleccion:
            data['tipo_eleccion_nombre'] = self.tipo_eleccion.nombre
        
        if include_votos:
            data['votos_partidos'] = [vp.to_dict() for vp in self.votos_partidos]
        
        return data


class VotoPartidoE24Puesto(db.Model):
    """Votos por partido en E-24 Puesto"""
    __tablename__ = 'votos_partidos_e24_puesto'
    
    id = db.Column(db.Integer, primary_key=True)
    e24_puesto_id = db.Column(db.Integer, db.ForeignKey('formularios_e24_puesto.id'), nullable=False)
    partido_id = db.Column(db.Integer, db.ForeignKey('partidos_politicos.id'), nullable=False)
    votos = db.Column(db.Integer, nullable=False)
    porcentaje = db.Column(db.Float, nullable=False)
    
    # Relaciones
    e24_puesto = db.relationship('FormularioE24Puesto', back_populates='votos_partidos')
    partido = db.relationship('PartidoPolitico', backref='votos_e24_puesto')
    
    def to_dict(self):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'e24_puesto_id': self.e24_puesto_id,
            'partido_id': self.partido_id,
            'votos': self.votos,
            'porcentaje': self.porcentaje
        }
        
        if self.partido:
            data['partido_nombre'] = self.partido.nombre
            data['partido_nombre_corto'] = self.partido.nombre_corto
            data['partido_color'] = self.partido.color
        
        return data


class FormularioE24Municipal(db.Model):
    """Formulario E-24 consolidado municipal"""
    __tablename__ = 'formularios_e24_municipal'
    
    id = db.Column(db.Integer, primary_key=True)
    municipio_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    coordinador_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tipo_eleccion_id = db.Column(db.Integer, db.ForeignKey('tipos_eleccion.id'), nullable=False)
    
    # Datos consolidados
    total_puestos = db.Column(db.Integer, nullable=False)
    puestos_incluidos = db.Column(db.Integer, nullable=False)
    total_mesas = db.Column(db.Integer, nullable=False)
    total_votantes_registrados = db.Column(db.Integer, nullable=False)
    total_votos = db.Column(db.Integer, nullable=False)
    votos_validos = db.Column(db.Integer, nullable=False)
    votos_nulos = db.Column(db.Integer, nullable=False)
    votos_blanco = db.Column(db.Integer, nullable=False)
    
    # Archivo PDF
    pdf_url = db.Column(db.String(500), nullable=False)
    pdf_hash = db.Column(db.String(64))  # SHA-256
    
    # Metadatos
    version = db.Column(db.Integer, default=1)  # Para regeneraciones
    observaciones = db.Column(db.Text)
    
    # Auditoría
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    municipio = db.relationship('Location', foreign_keys=[municipio_id])
    coordinador = db.relationship('User', foreign_keys=[coordinador_id])
    tipo_eleccion = db.relationship('TipoEleccion')
    votos_partidos = db.relationship('VotoPartidoE24Municipal', back_populates='e24_municipal', cascade='all, delete-orphan')
    
    def to_dict(self, include_votos=False):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'municipio_id': self.municipio_id,
            'coordinador_id': self.coordinador_id,
            'tipo_eleccion_id': self.tipo_eleccion_id,
            'total_puestos': self.total_puestos,
            'puestos_incluidos': self.puestos_incluidos,
            'total_mesas': self.total_mesas,
            'total_votantes_registrados': self.total_votantes_registrados,
            'total_votos': self.total_votos,
            'votos_validos': self.votos_validos,
            'votos_nulos': self.votos_nulos,
            'votos_blanco': self.votos_blanco,
            'pdf_url': self.pdf_url,
            'pdf_hash': self.pdf_hash,
            'version': self.version,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        # Incluir información de relaciones
        if self.municipio:
            data['municipio_nombre'] = self.municipio.municipio_nombre or self.municipio.nombre_completo
            data['municipio_codigo'] = self.municipio.municipio_codigo
        
        if self.coordinador:
            data['coordinador_nombre'] = self.coordinador.nombre
        
        if self.tipo_eleccion:
            data['tipo_eleccion_nombre'] = self.tipo_eleccion.nombre
        
        # Incluir votos si se solicita
        if include_votos:
            data['votos_partidos'] = [vp.to_dict() for vp in self.votos_partidos]
        
        return data


class VotoPartidoE24Municipal(db.Model):
    """Votos por partido en E-24 Municipal"""
    __tablename__ = 'votos_partidos_e24_municipal'
    
    id = db.Column(db.Integer, primary_key=True)
    e24_municipal_id = db.Column(db.Integer, db.ForeignKey('formularios_e24_municipal.id'), nullable=False)
    partido_id = db.Column(db.Integer, db.ForeignKey('partidos_politicos.id'), nullable=False)
    votos = db.Column(db.Integer, nullable=False)
    porcentaje = db.Column(db.Float, nullable=False)
    
    # Relaciones
    e24_municipal = db.relationship('FormularioE24Municipal', back_populates='votos_partidos')
    partido = db.relationship('PartidoPolitico', backref='votos_e24_municipal')
    
    def to_dict(self):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'e24_municipal_id': self.e24_municipal_id,
            'partido_id': self.partido_id,
            'votos': self.votos,
            'porcentaje': self.porcentaje
        }
        
        if self.partido:
            data['partido_nombre'] = self.partido.nombre
            data['partido_nombre_corto'] = self.partido.nombre_corto
            data['partido_color'] = self.partido.color
        
        return data


class NotificacionCoordinador(db.Model):
    """Notificaciones enviadas a coordinadores"""
    __tablename__ = 'notificaciones_coordinadores'
    
    id = db.Column(db.Integer, primary_key=True)
    remitente_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    destinatario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    prioridad = db.Column(db.String(20), default='normal')  # baja, normal, alta, urgente
    leida = db.Column(db.Boolean, default=False)
    leida_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    remitente = db.relationship('User', foreign_keys=[remitente_id], backref='notificaciones_enviadas')
    destinatario = db.relationship('User', foreign_keys=[destinatario_id], backref='notificaciones_recibidas')
    
    def to_dict(self):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'remitente_id': self.remitente_id,
            'destinatario_id': self.destinatario_id,
            'mensaje': self.mensaje,
            'prioridad': self.prioridad,
            'leida': self.leida,
            'leida_at': self.leida_at.isoformat() if self.leida_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if self.remitente:
            data['remitente_nombre'] = self.remitente.nombre
        
        if self.destinatario:
            data['destinatario_nombre'] = self.destinatario.nombre
        
        return data


class AuditLog(db.Model):
    """Log de auditoría de acciones"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    accion = db.Column(db.String(100), nullable=False)
    recurso = db.Column(db.String(100))  # ej: 'puesto', 'e24_municipal'
    recurso_id = db.Column(db.Integer)
    detalles = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    user = db.relationship('User', backref='audit_logs')
    
    def to_dict(self):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'accion': self.accion,
            'recurso': self.recurso,
            'recurso_id': self.recurso_id,
            'detalles': self.detalles,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if self.user:
            data['user_nombre'] = self.user.nombre
            data['user_rol'] = self.user.rol
        
        return data
