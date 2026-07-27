"""
Modelos para formularios E-14 y votos
"""
from backend.database import db
from datetime import datetime


class FormularioE14(db.Model):
    """Formulario E-14 de mesa electoral"""
    __tablename__ = 'formularios_e14'
    
    # Restricción única: una mesa solo puede tener un formulario por tipo de elección
    __table_args__ = (
        db.UniqueConstraint('mesa_id', 'tipo_eleccion_id', name='uq_mesa_tipo_eleccion'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    mesa_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    testigo_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tipo_eleccion_id = db.Column(db.Integer, db.ForeignKey('tipos_eleccion.id'), nullable=False)
    
    # Datos de votación
    total_votantes_registrados = db.Column(db.Integer, nullable=False)
    total_votos = db.Column(db.Integer, nullable=False)
    votos_validos = db.Column(db.Integer, nullable=False)
    votos_nulos = db.Column(db.Integer, nullable=False, default=0)
    votos_blanco = db.Column(db.Integer, nullable=False, default=0)
    tarjetas_no_marcadas = db.Column(db.Integer, nullable=False, default=0)
    total_tarjetas = db.Column(db.Integer, nullable=False)
    
    # Estado y validación
    estado = db.Column(db.String(20), nullable=False, default='borrador')
    # Estados: borrador, pendiente, validado, rechazado
    
    validado_por_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    validado_at = db.Column(db.DateTime)
    motivo_rechazo = db.Column(db.Text)
    
    # Imagen del formulario
    imagen_url = db.Column(db.String(500))
    imagen_hash = db.Column(db.String(64))  # SHA-256 para integridad
    
    # Observaciones
    observaciones = db.Column(db.Text)
    
    # Auditoría
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    mesa = db.relationship('Location', foreign_keys=[mesa_id], backref='formularios_e14')
    testigo = db.relationship('User', foreign_keys=[testigo_id], backref='formularios_creados')
    validado_por = db.relationship('User', foreign_keys=[validado_por_id], backref='formularios_validados')
    tipo_eleccion = db.relationship('TipoEleccion', backref='formularios')
    votos_partidos = db.relationship('VotoPartido', back_populates='formulario', cascade='all, delete-orphan')
    votos_candidatos = db.relationship('VotoCandidato', back_populates='formulario', cascade='all, delete-orphan')
    historial = db.relationship('HistorialFormulario', back_populates='formulario', cascade='all, delete-orphan', order_by='HistorialFormulario.created_at.desc()')
    
    def to_dict(self, include_votos=False, include_historial=False):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'mesa_id': self.mesa_id,
            'testigo_id': self.testigo_id,
            'tipo_eleccion_id': self.tipo_eleccion_id,
            'total_votantes_registrados': self.total_votantes_registrados,
            'total_votos': self.total_votos,
            'votos_validos': self.votos_validos,
            'votos_nulos': self.votos_nulos,
            'votos_blanco': self.votos_blanco,
            'tarjetas_no_marcadas': self.tarjetas_no_marcadas,
            'total_tarjetas': self.total_tarjetas,
            'estado': self.estado,
            'validado_por_id': self.validado_por_id,
            'validado_at': self.validado_at.isoformat() if self.validado_at else None,
            'motivo_rechazo': self.motivo_rechazo,
            'imagen_url': self.imagen_url,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        # Incluir información de relaciones
        if self.mesa:
            data['mesa_codigo'] = self.mesa.mesa_codigo
            data['mesa_nombre'] = self.mesa.nombre_completo
        
        if self.testigo:
            data['testigo_nombre'] = self.testigo.nombre
        
        if self.validado_por:
            data['validado_por_nombre'] = self.validado_por.nombre
        
        if self.tipo_eleccion:
            data['tipo_eleccion_nombre'] = self.tipo_eleccion.nombre
            data['es_uninominal'] = self.tipo_eleccion.es_uninominal
        
        # Incluir votos si se solicita
        if include_votos:
            data['votos_partidos'] = [vp.to_dict() for vp in self.votos_partidos]
            data['votos_candidatos'] = [vc.to_dict() for vc in self.votos_candidatos]
        
        # Incluir historial si se solicita
        if include_historial:
            data['historial'] = [h.to_dict() for h in self.historial]
        
        return data


class VotoPartido(db.Model):
    """Votos por partido en un formulario E-14"""
    __tablename__ = 'votos_partidos'
    
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios_e14.id'), nullable=False)
    partido_id = db.Column(db.Integer, db.ForeignKey('partidos_politicos.id'), nullable=False)
    votos = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    formulario = db.relationship('FormularioE14', back_populates='votos_partidos')
    partido = db.relationship('PartidoPolitico', backref='votos_e14')
    
    def to_dict(self):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'formulario_id': self.formulario_id,
            'partido_id': self.partido_id,
            'votos': self.votos,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if self.partido:
            data['partido_nombre'] = self.partido.nombre
            data['partido_nombre_corto'] = self.partido.nombre_corto
            data['partido_color'] = self.partido.color
        
        return data


class VotoCandidato(db.Model):
    """Votos por candidato en un formulario E-14"""
    __tablename__ = 'votos_candidatos'
    
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios_e14.id'), nullable=False)
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidatos.id'), nullable=False)
    votos = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    formulario = db.relationship('FormularioE14', back_populates='votos_candidatos')
    candidato = db.relationship('Candidato', backref='votos_e14')
    
    def to_dict(self):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'formulario_id': self.formulario_id,
            'candidato_id': self.candidato_id,
            'votos': self.votos,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if self.candidato:
            data['candidato_nombre'] = self.candidato.nombre_completo
            data['candidato_numero_lista'] = self.candidato.numero_lista
            data['partido_id'] = self.candidato.partido_id
        
        return data


class HistorialFormulario(db.Model):
    """Historial de cambios de formularios E-14"""
    __tablename__ = 'historial_formularios'
    
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios_e14.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    accion = db.Column(db.String(50), nullable=False)
    # Acciones: creado, enviado, validado, rechazado, editado
    
    estado_anterior = db.Column(db.String(20))
    estado_nuevo = db.Column(db.String(20))
    cambios = db.Column(db.JSON)  # Detalles de cambios realizados
    comentario = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    formulario = db.relationship('FormularioE14', back_populates='historial')
    usuario = db.relationship('User', backref='acciones_formularios')
    
    def to_dict(self):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'formulario_id': self.formulario_id,
            'usuario_id': self.usuario_id,
            'accion': self.accion,
            'estado_anterior': self.estado_anterior,
            'estado_nuevo': self.estado_nuevo,
            'cambios': self.cambios,
            'comentario': self.comentario,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if self.usuario:
            data['usuario_nombre'] = self.usuario.nombre
        
        return data
