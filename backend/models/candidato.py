"""
Modelo para Candidatos
"""
from backend.database import db
from datetime import datetime


class Candidato(db.Model):
    """
    Modelo para gestionar candidatos de las elecciones
    """
    __tablename__ = 'candidatos'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50))  # Código único del candidato
    nombre_completo = db.Column(db.String(200), nullable=False)
    partido_id = db.Column(db.Integer, db.ForeignKey('partidos_politicos.id'), nullable=False)
    tipo_eleccion_id = db.Column(db.Integer, db.ForeignKey('tipos_eleccion.id'), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)  # Presidente, Alcalde, Diputado, etc.
    numero_lista = db.Column(db.Integer)  # Número en la lista electoral
    orden = db.Column(db.Integer, default=0)  # Orden de visualización
    foto_url = db.Column(db.String(500))
    biografia = db.Column(db.Text)
    es_independiente = db.Column(db.Boolean, default=False)  # Si es candidato independiente
    es_cabeza_lista = db.Column(db.Boolean, default=False)  # Si es cabeza de lista
    activo = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    # partido - definido en PartidoPolitico con backref
    tipo_eleccion = db.relationship('TipoEleccion', backref='candidatos')
    
    def __repr__(self):
        return f'<Candidato {self.nombre_completo} - {self.cargo}>'
    
    def to_dict(self, include_partido=True, include_tipo_eleccion=True):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'codigo': self.codigo,
            'nombre_completo': self.nombre_completo,
            'partido_id': self.partido_id,
            'tipo_eleccion_id': self.tipo_eleccion_id,
            'cargo': self.cargo,
            'numero_lista': self.numero_lista,
            'orden': self.orden,
            'foto_url': self.foto_url,
            'biografia': self.biografia,
            'es_independiente': self.es_independiente,
            'es_cabeza_lista': self.es_cabeza_lista,
            'activo': self.activo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_partido and self.partido:
            data['partido'] = {
                'id': self.partido.id,
                'nombre': self.partido.nombre,
                'sigla': self.partido.sigla,
                'color': self.partido.color,
                'logo_url': self.partido.logo_url
            }
        
        if include_tipo_eleccion and self.tipo_eleccion:
            data['tipo_eleccion'] = {
                'id': self.tipo_eleccion.id,
                'nombre': self.tipo_eleccion.nombre,
                'codigo': self.tipo_eleccion.codigo,
                'es_uninominal': self.tipo_eleccion.es_uninominal
            }
        
        return data
