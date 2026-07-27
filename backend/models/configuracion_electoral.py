"""
Modelos para configuración electoral
"""
from backend.database import db
from datetime import datetime


class TipoEleccion(db.Model):
    """Tipos de elección configurables"""
    __tablename__ = 'tipos_eleccion'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    es_uninominal = db.Column(db.Boolean, default=False)  # True para presidencia, gobernación, alcaldía
    permite_lista_cerrada = db.Column(db.Boolean, default=True)  # Para corporaciones
    permite_lista_abierta = db.Column(db.Boolean, default=False)  # Voto preferente
    permite_coaliciones = db.Column(db.Boolean, default=False)  # Coaliciones de partidos
    activo = db.Column(db.Boolean, default=True)
    orden = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'es_uninominal': self.es_uninominal,
            'permite_lista_cerrada': self.permite_lista_cerrada,
            'permite_lista_abierta': self.permite_lista_abierta,
            'permite_coaliciones': self.permite_coaliciones,
            'activo': self.activo,
            'orden': self.orden
        }


# NOTA: Modelo Partido movido a backend/models/partido_politico.py
# Importar desde allí si se necesita
# class Partido(db.Model):
#     """Partidos políticos"""
#     __tablename__ = 'partidos'
#     ...


class Coalicion(db.Model):
    """Coaliciones de partidos"""
    __tablename__ = 'coaliciones'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    partidos_coalicion = db.relationship('PartidoCoalicion', back_populates='coalicion', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'activo': self.activo,
            'partidos': [pc.partido.to_dict() for pc in self.partidos_coalicion]
        }


class PartidoCoalicion(db.Model):
    """Relación entre partidos y coaliciones"""
    __tablename__ = 'partidos_coaliciones'
    
    id = db.Column(db.Integer, primary_key=True)
    partido_id = db.Column(db.Integer, db.ForeignKey('partidos_politicos.id'), nullable=False)
    coalicion_id = db.Column(db.Integer, db.ForeignKey('coaliciones.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    partido = db.relationship('PartidoPolitico', backref='coaliciones')
    coalicion = db.relationship('Coalicion', back_populates='partidos_coalicion')


# NOTA: Modelo Candidato movido a backend/models/candidato.py
# Importar desde allí si se necesita
# class Candidato(db.Model):
#     """Candidatos"""
#     __tablename__ = 'candidatos'
#     ...



class Campana(db.Model):
    """Campañas electorales - permite múltiples campañas independientes"""
    __tablename__ = 'campanas'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    
    # Configuración visual
    color_primario = db.Column(db.String(7), default='#1e3c72')  # Color principal
    color_secundario = db.Column(db.String(7), default='#2a5298')  # Color secundario
    logo_url = db.Column(db.String(500))
    
    # Tipos de campaña
    es_candidato_unico = db.Column(db.Boolean, default=False)  # TRUE si es campaña de un candidato
    es_partido_completo = db.Column(db.Boolean, default=False)  # TRUE si es campaña de partido
    
    # Estado
    activa = db.Column(db.Boolean, default=False)  # Solo una campaña activa a la vez
    completada = db.Column(db.Boolean, default=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'color_primario': self.color_primario,
            'color_secundario': self.color_secundario,
            'logo_url': self.logo_url,
            'es_candidato_unico': self.es_candidato_unico,
            'es_partido_completo': self.es_partido_completo,
            'activa': self.activa,
            'completada': self.completada
        }


class ConfiguracionTema(db.Model):
    """Configuración de temas visuales por rol o tipo de elección"""
    __tablename__ = 'configuracion_temas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    
    # Aplicación del tema
    aplica_a_rol = db.Column(db.String(50))  # testigo, coordinador_puesto, etc.
    aplica_a_tipo_eleccion_id = db.Column(db.Integer, db.ForeignKey('tipos_eleccion.id'))
    campana_id = db.Column(db.Integer, db.ForeignKey('campanas.id'))
    
    # Colores
    color_primario = db.Column(db.String(7), default='#1e3c72')
    color_secundario = db.Column(db.String(7), default='#2a5298')
    color_acento = db.Column(db.String(7), default='#28a745')
    color_fondo = db.Column(db.String(7), default='#f8f9fa')
    color_texto = db.Column(db.String(7), default='#212529')
    
    # Configuración adicional
    logo_url = db.Column(db.String(500))
    favicon_url = db.Column(db.String(500))
    
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'aplica_a_rol': self.aplica_a_rol,
            'aplica_a_tipo_eleccion_id': self.aplica_a_tipo_eleccion_id,
            'campana_id': self.campana_id,
            'color_primario': self.color_primario,
            'color_secundario': self.color_secundario,
            'color_acento': self.color_acento,
            'color_fondo': self.color_fondo,
            'color_texto': self.color_texto,
            'logo_url': self.logo_url,
            'favicon_url': self.favicon_url,
            'activo': self.activo
        }
