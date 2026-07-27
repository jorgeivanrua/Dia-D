"""Modelos para incidentes y delitos electorales"""

from backend.database import db
from datetime import datetime
from sqlalchemy import func


class IncidenteElectoral(db.Model):
    """Modelo para incidentes electorales"""
    __tablename__ = 'incidentes_electorales'
    
    id = db.Column(db.Integer, primary_key=True)
    reportado_por_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mesa_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    puesto_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    municipio_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    departamento_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    
    tipo_incidente = db.Column(db.String(50), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    severidad = db.Column(db.String(20), default='media')  # baja, media, alta, critica
    estado = db.Column(db.String(20), default='reportado')  # reportado, en_revision, resuelto, escalado
    
    evidencia_url = db.Column(db.String(500), nullable=True)
    ubicacion_gps = db.Column(db.String(100), nullable=True)
    
    fecha_incidente = db.Column(db.DateTime, nullable=True)
    fecha_reporte = db.Column(db.DateTime, default=datetime.utcnow)
    
    resuelto_por_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    fecha_resolucion = db.Column(db.DateTime, nullable=True)
    notas_resolucion = db.Column(db.Text, nullable=True)
    escalado_a = db.Column(db.String(50), nullable=True)  # coordinador_municipal, coordinador_departamental, auditor
    
    # Metadatos de geolocalización del reporte
    latitud_reporte = db.Column(db.Float, nullable=True)
    longitud_reporte = db.Column(db.Float, nullable=True)
    precision_gps = db.Column(db.Float, nullable=True)  # en metros
    
    # Sincronización offline
    sincronizado = db.Column(db.Boolean, default=True)
    fecha_sincronizacion = db.Column(db.DateTime, nullable=True)
    dispositivo_id = db.Column(db.String(100), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    reportado_por = db.relationship('User', foreign_keys=[reportado_por_id], backref='incidentes_reportados')
    resuelto_por = db.relationship('User', foreign_keys=[resuelto_por_id], backref='incidentes_resueltos')
    mesa = db.relationship('Location', foreign_keys=[mesa_id])
    puesto = db.relationship('Location', foreign_keys=[puesto_id])
    municipio = db.relationship('Location', foreign_keys=[municipio_id])
    departamento = db.relationship('Location', foreign_keys=[departamento_id])
    
    # Tipos de incidentes
    TIPOS_INCIDENTE = {
        'retraso_apertura': 'Retraso en apertura de mesa',
        'falta_material': 'Falta de material electoral',
        'problemas_tecnicos': 'Problemas técnicos',
        'irregularidades_proceso': 'Irregularidades en el proceso',
        'ausencia_funcionarios': 'Ausencia de funcionarios',
        'problemas_acceso': 'Problemas de acceso al puesto',
        'disturbios': 'Disturbios o alteración del orden',
        'otros': 'Otros incidentes'
    }
    
    # Niveles de severidad
    SEVERIDADES = {
        'baja': 'Baja',
        'media': 'Media',
        'alta': 'Alta',
        'critica': 'Crítica'
    }
    
    # Estados
    ESTADOS = {
        'reportado': 'Reportado',
        'en_revision': 'En revisión',
        'resuelto': 'Resuelto',
        'escalado': 'Escalado'
    }
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'reportado_por_id': self.reportado_por_id,
            'reportado_por_nombre': self.reportado_por.nombre if self.reportado_por else None,
            'mesa_id': self.mesa_id,
            'mesa_codigo': self.mesa.mesa_codigo if self.mesa else None,
            'puesto_id': self.puesto_id,
            'puesto_nombre': self.puesto.puesto_nombre if self.puesto else None,
            'municipio_id': self.municipio_id,
            'municipio_nombre': self.municipio.municipio_nombre if self.municipio else None,
            'departamento_id': self.departamento_id,
            'departamento_nombre': self.departamento.departamento_nombre if self.departamento else None,
            'tipo_incidente': self.tipo_incidente,
            'tipo_incidente_label': self.TIPOS_INCIDENTE.get(self.tipo_incidente, self.tipo_incidente),
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'severidad': self.severidad,
            'severidad_label': self.SEVERIDADES.get(self.severidad, self.severidad),
            'estado': self.estado,
            'estado_label': self.ESTADOS.get(self.estado, self.estado),
            'evidencia_url': self.evidencia_url,
            'ubicacion_gps': self.ubicacion_gps,
            'fecha_incidente': self.fecha_incidente.isoformat() if self.fecha_incidente else None,
            'fecha_reporte': self.fecha_reporte.isoformat() if self.fecha_reporte else None,
            'resuelto_por_id': self.resuelto_por_id,
            'resuelto_por_nombre': self.resuelto_por.nombre if self.resuelto_por else None,
            'fecha_resolucion': self.fecha_resolucion.isoformat() if self.fecha_resolucion else None,
            'notas_resolucion': self.notas_resolucion,
            'escalado_a': self.escalado_a,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class DelitoElectoral(db.Model):
    """Modelo para delitos electorales"""
    __tablename__ = 'delitos_electorales'
    
    id = db.Column(db.Integer, primary_key=True)
    reportado_por_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mesa_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    puesto_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    municipio_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    departamento_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    
    tipo_delito = db.Column(db.String(50), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    gravedad = db.Column(db.String(20), default='media')  # leve, media, grave, muy_grave
    estado = db.Column(db.String(30), default='reportado')  # reportado, en_investigacion, investigado, denunciado, archivado
    
    evidencia_url = db.Column(db.String(500), nullable=True)
    testigos_adicionales = db.Column(db.Text, nullable=True)
    ubicacion_gps = db.Column(db.String(100), nullable=True)
    
    fecha_delito = db.Column(db.DateTime, nullable=True)
    fecha_reporte = db.Column(db.DateTime, default=datetime.utcnow)
    
    investigado_por_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    fecha_investigacion = db.Column(db.DateTime, nullable=True)
    resultado_investigacion = db.Column(db.Text, nullable=True)
    
    denunciado_formalmente = db.Column(db.Boolean, default=False)
    numero_denuncia = db.Column(db.String(100), nullable=True)
    autoridad_competente = db.Column(db.String(200), nullable=True)
    fecha_denuncia = db.Column(db.DateTime, nullable=True)
    seguimiento = db.Column(db.Text, nullable=True)
    
    # Metadatos de geolocalización del reporte
    latitud_reporte = db.Column(db.Float, nullable=True)
    longitud_reporte = db.Column(db.Float, nullable=True)
    precision_gps = db.Column(db.Float, nullable=True)  # en metros
    
    # Sincronización offline
    sincronizado = db.Column(db.Boolean, default=True)
    fecha_sincronizacion = db.Column(db.DateTime, nullable=True)
    dispositivo_id = db.Column(db.String(100), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    reportado_por = db.relationship('User', foreign_keys=[reportado_por_id], backref='delitos_reportados')
    investigado_por = db.relationship('User', foreign_keys=[investigado_por_id], backref='delitos_investigados')
    mesa = db.relationship('Location', foreign_keys=[mesa_id])
    puesto = db.relationship('Location', foreign_keys=[puesto_id])
    municipio = db.relationship('Location', foreign_keys=[municipio_id])
    departamento = db.relationship('Location', foreign_keys=[departamento_id])
    
    # Tipos de delitos
    TIPOS_DELITO = {
        'compra_votos': 'Compra de votos',
        'coaccion_votante': 'Coacción al votante',
        'fraude_electoral': 'Fraude electoral',
        'suplantacion_identidad': 'Suplantación de identidad',
        'alteracion_resultados': 'Alteración de resultados',
        'violencia_electoral': 'Violencia electoral',
        'propaganda_ilegal': 'Propaganda ilegal',
        'financiacion_ilegal': 'Financiación ilegal de campaña',
        'otros_delitos': 'Otros delitos electorales'
    }
    
    # Niveles de gravedad
    GRAVEDADES = {
        'leve': 'Leve',
        'media': 'Media',
        'grave': 'Grave',
        'muy_grave': 'Muy grave'
    }
    
    # Estados
    ESTADOS = {
        'reportado': 'Reportado',
        'en_investigacion': 'En investigación',
        'investigado': 'Investigado',
        'denunciado': 'Denunciado formalmente',
        'archivado': 'Archivado'
    }
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'reportado_por_id': self.reportado_por_id,
            'reportado_por_nombre': self.reportado_por.nombre if self.reportado_por else None,
            'mesa_id': self.mesa_id,
            'mesa_codigo': self.mesa.mesa_codigo if self.mesa else None,
            'puesto_id': self.puesto_id,
            'puesto_nombre': self.puesto.puesto_nombre if self.puesto else None,
            'municipio_id': self.municipio_id,
            'municipio_nombre': self.municipio.municipio_nombre if self.municipio else None,
            'departamento_id': self.departamento_id,
            'departamento_nombre': self.departamento.departamento_nombre if self.departamento else None,
            'tipo_delito': self.tipo_delito,
            'tipo_delito_label': self.TIPOS_DELITO.get(self.tipo_delito, self.tipo_delito),
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'gravedad': self.gravedad,
            'gravedad_label': self.GRAVEDADES.get(self.gravedad, self.gravedad),
            'estado': self.estado,
            'estado_label': self.ESTADOS.get(self.estado, self.estado),
            'evidencia_url': self.evidencia_url,
            'testigos_adicionales': self.testigos_adicionales,
            'ubicacion_gps': self.ubicacion_gps,
            'fecha_delito': self.fecha_delito.isoformat() if self.fecha_delito else None,
            'fecha_reporte': self.fecha_reporte.isoformat() if self.fecha_reporte else None,
            'investigado_por_id': self.investigado_por_id,
            'investigado_por_nombre': self.investigado_por.nombre if self.investigado_por else None,
            'fecha_investigacion': self.fecha_investigacion.isoformat() if self.fecha_investigacion else None,
            'resultado_investigacion': self.resultado_investigacion,
            'denunciado_formalmente': self.denunciado_formalmente,
            'numero_denuncia': self.numero_denuncia,
            'autoridad_competente': self.autoridad_competente,
            'fecha_denuncia': self.fecha_denuncia.isoformat() if self.fecha_denuncia else None,
            'seguimiento': self.seguimiento,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# NOTA: SeguimientoReporte ahora está definido en backend/models/seguimiento.py
# Importar desde allí si se necesita
# from backend.models.seguimiento import SeguimientoReporte


class NotificacionReporte(db.Model):
    """Modelo para notificaciones de reportes"""
    __tablename__ = 'notificaciones_reportes'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tipo_reporte = db.Column(db.String(20), nullable=False)  # 'incidente' o 'delito'
    reporte_id = db.Column(db.Integer, nullable=False)
    tipo_notificacion = db.Column(db.String(50), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    leida = db.Column(db.Boolean, default=False)
    fecha_lectura = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuario = db.relationship('User', backref='notificaciones_reportes')
    
    def marcar_como_leida(self):
        """Marcar notificación como leída"""
        self.leida = True
        self.fecha_lectura = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'tipo_reporte': self.tipo_reporte,
            'reporte_id': self.reporte_id,
            'tipo_notificacion': self.tipo_notificacion,
            'titulo': self.titulo,
            'mensaje': self.mensaje,
            'leida': self.leida,
            'fecha_lectura': self.fecha_lectura.isoformat() if self.fecha_lectura else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }



class EvidenciaFotografica(db.Model):
    """Modelo para evidencia fotográfica de incidentes y delitos"""
    __tablename__ = 'evidencias_fotograficas'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relación con reporte (puede ser incidente o delito)
    incidente_id = db.Column(db.Integer, db.ForeignKey('incidentes_electorales.id'), nullable=True)
    delito_id = db.Column(db.Integer, db.ForeignKey('delitos_electorales.id'), nullable=True)
    
    # Información del archivo
    filename = db.Column(db.String(255), nullable=False, unique=True)
    filename_original = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    mime_type = db.Column(db.String(50), nullable=False)
    size_bytes = db.Column(db.Integer, nullable=False)
    
    # Metadatos de la foto
    width = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    latitud = db.Column(db.Float, nullable=True)
    longitud = db.Column(db.Float, nullable=True)
    fecha_captura = db.Column(db.DateTime, nullable=True)
    dispositivo = db.Column(db.String(200), nullable=True)
    
    # Auditoría
    subido_por_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    subido_por = db.relationship('User', backref='evidencias_subidas')
    incidente = db.relationship('IncidenteElectoral', backref='evidencias', foreign_keys=[incidente_id])
    delito = db.relationship('DelitoElectoral', backref='evidencias', foreign_keys=[delito_id])
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'incidente_id': self.incidente_id,
            'delito_id': self.delito_id,
            'filename': self.filename,
            'filename_original': self.filename_original,
            'url': self.url,
            'mime_type': self.mime_type,
            'size_bytes': self.size_bytes,
            'width': self.width,
            'height': self.height,
            'latitud': self.latitud,
            'longitud': self.longitud,
            'fecha_captura': self.fecha_captura.isoformat() if self.fecha_captura else None,
            'dispositivo': self.dispositivo,
            'subido_por_id': self.subido_por_id,
            'subido_por_nombre': self.subido_por.nombre if self.subido_por else None,
            'fecha_subida': self.fecha_subida.isoformat() if self.fecha_subida else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
