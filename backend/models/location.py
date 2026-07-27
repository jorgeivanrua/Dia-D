"""
Modelo de Ubicación (DIVIPOLA)
"""
from datetime import datetime
from backend.database import db


class Location(db.Model):
    """Modelo de ubicación jerárquica DIVIPOLA"""
    
    __tablename__ = 'locations'
    
    # Campos
    id = db.Column(db.Integer, primary_key=True)
    departamento_codigo = db.Column(db.String(10), nullable=False, index=True)
    municipio_codigo = db.Column(db.String(10), nullable=True, index=True)
    zona_codigo = db.Column(db.String(10), nullable=True, index=True)
    puesto_codigo = db.Column(db.String(10), nullable=True, index=True)
    mesa_codigo = db.Column(db.String(10), nullable=True, index=True)
    
    departamento_nombre = db.Column(db.String(100), nullable=False)
    municipio_nombre = db.Column(db.String(100), nullable=True)
    puesto_nombre = db.Column(db.String(200), nullable=True)
    mesa_nombre = db.Column(db.String(200), nullable=True)
    
    nombre_completo = db.Column(db.String(500), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # departamento, municipio, zona, puesto, mesa
    
    total_votantes_registrados = db.Column(db.Integer, default=0)
    mujeres = db.Column(db.Integer, default=0)
    hombres = db.Column(db.Integer, default=0)
    
    comuna = db.Column(db.String(100), nullable=True)
    direccion = db.Column(db.String(500), nullable=True)
    latitud = db.Column(db.Float, nullable=True)
    longitud = db.Column(db.Float, nullable=True)
    
    activo = db.Column(db.Boolean, default=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    children = db.relationship('Location', backref=db.backref('parent', remote_side=[id]), lazy=True)
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint(
            tipo.in_(['departamento', 'municipio', 'zona', 'puesto', 'mesa']),
            name='check_tipo_valido'
        ),
        db.Index('idx_location_hierarchy', 
                 departamento_codigo, municipio_codigo, zona_codigo, puesto_codigo, mesa_codigo),
    )
    
    @classmethod
    def find_by_hierarchy(cls, ubicacion_data):
        """
        Buscar ubicación por jerarquía
        
        Args:
            ubicacion_data: Dict con códigos de ubicación
            
        Returns:
            Location o None
        """
        query = cls.query
        
        if 'departamento_codigo' in ubicacion_data:
            query = query.filter_by(departamento_codigo=ubicacion_data['departamento_codigo'])
        
        if 'municipio_codigo' in ubicacion_data:
            query = query.filter_by(municipio_codigo=ubicacion_data['municipio_codigo'])
        
        if 'zona_codigo' in ubicacion_data:
            query = query.filter_by(zona_codigo=ubicacion_data['zona_codigo'])
        
        if 'puesto_codigo' in ubicacion_data:
            query = query.filter_by(puesto_codigo=ubicacion_data['puesto_codigo'])
        
        if 'mesa_codigo' in ubicacion_data:
            query = query.filter_by(mesa_codigo=ubicacion_data['mesa_codigo'])
        
        return query.first()
    
    def get_departamento(self):
        """Obtener el departamento de esta ubicación"""
        if self.tipo == 'departamento':
            return self
        return Location.query.filter_by(
            departamento_codigo=self.departamento_codigo,
            tipo='departamento'
        ).first()
    
    def get_municipio(self):
        """Obtener el municipio de esta ubicación"""
        if self.tipo == 'municipio':
            return self
        if self.municipio_codigo:
            return Location.query.filter_by(
                departamento_codigo=self.departamento_codigo,
                municipio_codigo=self.municipio_codigo,
                tipo='municipio'
            ).first()
        return None
    
    def get_puesto(self):
        """Obtener el puesto de esta ubicación"""
        if self.tipo == 'puesto':
            return self
        if self.puesto_codigo:
            return Location.query.filter_by(
                departamento_codigo=self.departamento_codigo,
                municipio_codigo=self.municipio_codigo,
                zona_codigo=self.zona_codigo,
                puesto_codigo=self.puesto_codigo,
                tipo='puesto'
            ).first()
        return None
    
    def to_dict(self):
        """
        Convertir a diccionario
        
        Returns:
            dict: Representación de la ubicación
        """
        return {
            'id': self.id,
            'departamento_codigo': self.departamento_codigo,
            'municipio_codigo': self.municipio_codigo,
            'zona_codigo': self.zona_codigo,
            'puesto_codigo': self.puesto_codigo,
            'mesa_codigo': self.mesa_codigo,
            'departamento_nombre': self.departamento_nombre,
            'municipio_nombre': self.municipio_nombre,
            'puesto_nombre': self.puesto_nombre,
            'mesa_nombre': self.mesa_nombre,
            'nombre_completo': self.nombre_completo,
            'tipo': self.tipo,
            'total_votantes_registrados': self.total_votantes_registrados,
            'mujeres': self.mujeres,
            'hombres': self.hombres,
            'comuna': self.comuna,
            'direccion': self.direccion,
            'latitud': self.latitud,
            'longitud': self.longitud,
            'activo': self.activo
        }
    
    def __repr__(self):
        return f'<Location {self.id}: {self.nombre_completo} ({self.tipo})>'
