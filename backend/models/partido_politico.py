"""
Modelo para Partidos Políticos
"""
from backend.database import db
from datetime import datetime


class PartidoPolitico(db.Model):
    """
    Modelo para gestionar partidos políticos participantes en las elecciones
    """
    __tablename__ = 'partidos_politicos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False, unique=True)
    sigla = db.Column(db.String(20), nullable=False, unique=True)
    color = db.Column(db.String(7), nullable=False, default='#000000')  # Formato hex: #RRGGBB
    logo_url = db.Column(db.String(500))
    descripcion = db.Column(db.Text)
    orden = db.Column(db.Integer, default=0)  # Orden de visualización
    activo = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    candidatos = db.relationship('Candidato', backref='partido', lazy='dynamic')
    
    def __repr__(self):
        return f'<PartidoPolitico {self.sigla}: {self.nombre}>'
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'sigla': self.sigla,
            'color': self.color,
            'logo_url': self.logo_url,
            'descripcion': self.descripcion,
            'orden': self.orden,
            'activo': self.activo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'total_candidatos': self.candidatos.count()
        }
    
    @staticmethod
    def validar_color(color):
        """Validar formato de color hexadecimal"""
        import re
        pattern = r'^#[0-9A-Fa-f]{6}$'
        return bool(re.match(pattern, color))
