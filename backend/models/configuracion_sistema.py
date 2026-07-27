"""
Modelo de Configuración del Sistema
Permite personalizar la apariencia del sistema
"""
from backend.database import db
from datetime import datetime


class ConfiguracionSistema(db.Model):
    """Configuración general del sistema"""
    __tablename__ = 'configuracion_sistema'
    
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.Text, nullable=True)
    tipo = db.Column(db.String(50), nullable=False)  # text, image, color, json
    descripcion = db.Column(db.String(255), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relación
    actualizado_por = db.relationship('User', foreign_keys=[updated_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'clave': self.clave,
            'valor': self.valor,
            'tipo': self.tipo,
            'descripcion': self.descripcion,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'updated_by': self.actualizado_por.nombre if self.actualizado_por else None
        }
    
    @staticmethod
    def get_valor(clave, default=None):
        """Obtener valor de configuración"""
        config = ConfiguracionSistema.query.filter_by(clave=clave).first()
        return config.valor if config else default
    
    @staticmethod
    def set_valor(clave, valor, tipo='text', descripcion=None, user_id=None):
        """Establecer valor de configuración"""
        config = ConfiguracionSistema.query.filter_by(clave=clave).first()
        
        if config:
            config.valor = valor
            config.updated_at = datetime.utcnow()
            config.updated_by = user_id
        else:
            config = ConfiguracionSistema(
                clave=clave,
                valor=valor,
                tipo=tipo,
                descripcion=descripcion,
                updated_by=user_id
            )
            db.session.add(config)
        
        db.session.commit()
        return config


class FondoLogin(db.Model):
    """Fondos disponibles para la página de login"""
    __tablename__ = 'fondos_login'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # gradient, image, solid
    
    # Para gradientes
    color1 = db.Column(db.String(7), nullable=True)  # #FCD116
    color2 = db.Column(db.String(7), nullable=True)  # #003893
    color3 = db.Column(db.String(7), nullable=True)  # #CE1126
    direccion = db.Column(db.String(20), default='180deg')  # 180deg, 135deg, etc
    
    # Para imágenes
    imagen_url = db.Column(db.String(500), nullable=True)
    imagen_posicion = db.Column(db.String(50), default='center')  # center, top, bottom
    imagen_tamano = db.Column(db.String(50), default='cover')  # cover, contain
    
    # Para colores sólidos
    color_solido = db.Column(db.String(7), nullable=True)
    
    # Overlay opcional
    overlay_color = db.Column(db.String(7), nullable=True)
    overlay_opacity = db.Column(db.Float, default=0.1)
    
    activo = db.Column(db.Boolean, default=False)
    predeterminado = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relación
    creado_por = db.relationship('User', foreign_keys=[created_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'color1': self.color1,
            'color2': self.color2,
            'color3': self.color3,
            'direccion': self.direccion,
            'imagen_url': self.imagen_url,
            'imagen_posicion': self.imagen_posicion,
            'imagen_tamano': self.imagen_tamano,
            'color_solido': self.color_solido,
            'overlay_color': self.overlay_color,
            'overlay_opacity': self.overlay_opacity,
            'activo': self.activo,
            'predeterminado': self.predeterminado,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'created_by': self.creado_por.nombre if self.creado_por else None
        }
    
    def get_css(self):
        """Generar CSS para el fondo"""
        if self.tipo == 'gradient':
            colors = []
            if self.color1:
                colors.append(f"{self.color1} 0%")
                colors.append(f"{self.color1} 50%")
            if self.color2:
                colors.append(f"{self.color2} 50%")
                colors.append(f"{self.color2} 75%")
            if self.color3:
                colors.append(f"{self.color3} 75%")
                colors.append(f"{self.color3} 100%")
            
            gradient = f"linear-gradient({self.direccion}, {', '.join(colors)})"
            
            css = {
                'background': gradient
            }
            
        elif self.tipo == 'image':
            css = {
                'background-image': f"url('{self.imagen_url}')",
                'background-position': self.imagen_posicion,
                'background-size': self.imagen_tamano,
                'background-repeat': 'no-repeat'
            }
            
        elif self.tipo == 'solid':
            css = {
                'background': self.color_solido
            }
        else:
            css = {}
        
        # Agregar overlay si existe
        if self.overlay_color and self.overlay_opacity:
            css['position'] = 'relative'
        
        return css
    
    @staticmethod
    def get_activo():
        """Obtener el fondo activo"""
        fondo = FondoLogin.query.filter_by(activo=True).first()
        if not fondo:
            # Si no hay activo, buscar el predeterminado
            fondo = FondoLogin.query.filter_by(predeterminado=True).first()
        return fondo
