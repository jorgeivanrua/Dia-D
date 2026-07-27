"""
Modelo de Usuario
"""
from datetime import datetime, timedelta
from backend.database import db
import bcrypt


class User(db.Model):
    """Modelo de usuario del sistema"""
    
    __tablename__ = 'users'
    
    # Campos
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    ubicacion_id = db.Column(db.Integer, nullable=True)  # FK se agregará cuando Location exista
    activo = db.Column(db.Boolean, default=True, nullable=False)
    ultimo_acceso = db.Column(db.DateTime, nullable=True)
    intentos_fallidos = db.Column(db.Integer, default=0, nullable=False)
    bloqueado_hasta = db.Column(db.DateTime, nullable=True)
    
    # Usuario básico fijo (no se puede eliminar, solo super admin puede modificar)
    es_usuario_basico = db.Column(db.Boolean, default=False, nullable=False)
    
    # Verificación de presencia (para testigos)
    presencia_verificada = db.Column(db.Boolean, default=False, nullable=False)
    presencia_verificada_at = db.Column(db.DateTime, nullable=True)
    
    # Geolocalización
    ultima_latitud = db.Column(db.Float, nullable=True)
    ultima_longitud = db.Column(db.Float, nullable=True)
    ultima_geolocalizacion_at = db.Column(db.DateTime, nullable=True)
    precision_geolocalizacion = db.Column(db.Float, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones (se configurarán cuando los modelos existan)
    # ubicacion = db.relationship('Location', backref='usuarios', lazy=True)
    # formularios_e14 = db.relationship('FormE14', foreign_keys='FormE14.testigo_id', backref='testigo', lazy=True)
    # formularios_aprobados = db.relationship('FormE14', foreign_keys='FormE14.aprobado_por', backref='aprobador', lazy=True)
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint(
            rol.in_([
                'super_admin',
                'admin_departamental',
                'admin_municipal',
                'coordinador_departamental',
                'coordinador_municipal',
                'coordinador_puesto',
                'testigo_electoral',
                'auditor_electoral',
                'monitoreo'  # Rol para monitoreo en tiempo real
            ]),
            name='check_rol_valido'
        ),
    )
    
    def set_password(self, password):
        """
        Establecer contraseña con hash seguro
        
        Args:
            password: Contraseña en texto plano
        """
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verificar contraseña
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            bool: True si la contraseña es correcta
        """
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    
    def is_blocked(self):
        """
        Verificar si el usuario está bloqueado
        
        Returns:
            bool: True si está bloqueado
        """
        if self.bloqueado_hasta is None:
            return False
        return datetime.utcnow() < self.bloqueado_hasta
    
    def increment_failed_attempts(self):
        """
        Incrementar intentos fallidos de login
        Bloquea la cuenta después de 5 intentos
        """
        self.intentos_fallidos += 1
        
        if self.intentos_fallidos >= 5:
            self.bloqueado_hasta = datetime.utcnow() + timedelta(minutes=1)
    
    def reset_failed_attempts(self):
        """Resetear intentos fallidos después de login exitoso"""
        self.intentos_fallidos = 0
        self.bloqueado_hasta = None
        self.ultimo_acceso = datetime.utcnow()
    
    def verificar_presencia(self):
        """Marcar presencia del testigo en la mesa"""
        self.presencia_verificada = True
        self.presencia_verificada_at = datetime.utcnow()
    
    def to_dict(self, include_sensitive=False):
        """
        Convertir a diccionario
        
        Args:
            include_sensitive: Incluir datos sensibles
            
        Returns:
            dict: Representación del usuario
        """
        data = {
            'id': self.id,
            'nombre': self.nombre,
            'rol': self.rol,
            'ubicacion_id': self.ubicacion_id,
            'activo': self.activo,
            'ultimo_acceso': self.ultimo_acceso.isoformat() if self.ultimo_acceso else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_sensitive:
            data['intentos_fallidos'] = self.intentos_fallidos
            data['bloqueado_hasta'] = self.bloqueado_hasta.isoformat() if self.bloqueado_hasta else None
        
        return data
    
    def __repr__(self):
        return f'<User {self.id}: {self.nombre} ({self.rol})>'
