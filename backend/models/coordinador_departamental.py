"""
Modelos para funcionalidades del coordinador departamental
"""
from backend.database import db
from datetime import datetime


class ReporteDepartamental(db.Model):
    """Reporte consolidado departamental"""
    __tablename__ = 'reportes_departamentales'
    
    id = db.Column(db.Integer, primary_key=True)
    departamento_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    coordinador_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tipo_eleccion_id = db.Column(db.Integer, db.ForeignKey('tipos_eleccion.id'), nullable=False)
    
    # Datos consolidados
    total_municipios = db.Column(db.Integer, nullable=False)
    municipios_incluidos = db.Column(db.Integer, nullable=False)
    total_puestos = db.Column(db.Integer, nullable=False)
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
    departamento = db.relationship('Location', foreign_keys=[departamento_id])
    coordinador = db.relationship('User', foreign_keys=[coordinador_id])
    tipo_eleccion = db.relationship('TipoEleccion')
    votos_partidos = db.relationship('VotoPartidoReporteDepartamental', back_populates='reporte_departamental', cascade='all, delete-orphan')
    
    def to_dict(self, include_votos=False):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'departamento_id': self.departamento_id,
            'coordinador_id': self.coordinador_id,
            'tipo_eleccion_id': self.tipo_eleccion_id,
            'total_municipios': self.total_municipios,
            'municipios_incluidos': self.municipios_incluidos,
            'total_puestos': self.total_puestos,
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
        if self.departamento:
            data['departamento_nombre'] = self.departamento.departamento_nombre or self.departamento.nombre_completo
            data['departamento_codigo'] = self.departamento.departamento_codigo
        
        if self.coordinador:
            data['coordinador_nombre'] = self.coordinador.nombre
        
        if self.tipo_eleccion:
            data['tipo_eleccion_nombre'] = self.tipo_eleccion.nombre
        
        # Incluir votos si se solicita
        if include_votos:
            data['votos_partidos'] = [vp.to_dict() for vp in self.votos_partidos]
        
        return data


class VotoPartidoReporteDepartamental(db.Model):
    """Votos por partido en Reporte Departamental"""
    __tablename__ = 'votos_partidos_reporte_departamental'
    
    id = db.Column(db.Integer, primary_key=True)
    reporte_departamental_id = db.Column(db.Integer, db.ForeignKey('reportes_departamentales.id'), nullable=False)
    partido_id = db.Column(db.Integer, db.ForeignKey('partidos_politicos.id'), nullable=False)
    votos = db.Column(db.Integer, nullable=False)
    porcentaje = db.Column(db.Float, nullable=False)
    
    # Relaciones
    reporte_departamental = db.relationship('ReporteDepartamental', back_populates='votos_partidos')
    partido = db.relationship('PartidoPolitico')
    
    def to_dict(self):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'reporte_departamental_id': self.reporte_departamental_id,
            'partido_id': self.partido_id,
            'votos': self.votos,
            'porcentaje': self.porcentaje
        }
        
        if self.partido:
            data['partido_nombre'] = self.partido.nombre
            data['partido_nombre_corto'] = self.partido.nombre_corto
            data['partido_color'] = self.partido.color
        
        return data
