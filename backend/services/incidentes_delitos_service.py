"""Servicio para manejo de incidentes y delitos electorales"""

from backend.database import db
from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral, NotificacionReporte
from backend.models.seguimiento import SeguimientoReporte
from backend.models.user import User
from backend.models.location import Location
from datetime import datetime
from sqlalchemy import and_, or_, desc


class IncidentesDelitosService:
    """Servicio para gestión de incidentes y delitos electorales"""
    
    @staticmethod
    def crear_incidente(data, usuario_id):
        """
        Crear un nuevo incidente electoral
        
        Args:
            data: dict con datos del incidente
            usuario_id: ID del usuario que reporta
            
        Returns:
            IncidenteElectoral: Incidente creado
        """
        try:
            # Obtener información del usuario para determinar ubicaciones
            usuario = User.query.get(usuario_id)
            if not usuario:
                raise ValueError('Usuario no encontrado')
            
            # Determinar ubicaciones basadas en el rol y ubicación del usuario
            mesa_id = data.get('mesa_id')
            puesto_id = None
            municipio_id = None
            departamento_id = None
            
            if mesa_id:
                mesa = Location.query.get(mesa_id)
                if mesa:
                    # Buscar puesto, municipio y departamento de la mesa
                    puesto = Location.query.filter_by(
                        puesto_codigo=mesa.puesto_codigo,
                        zona_codigo=mesa.zona_codigo,
                        municipio_codigo=mesa.municipio_codigo,
                        departamento_codigo=mesa.departamento_codigo,
                        tipo='puesto'
                    ).first()
                    
                    municipio = Location.query.filter_by(
                        municipio_codigo=mesa.municipio_codigo,
                        departamento_codigo=mesa.departamento_codigo,
                        tipo='municipio'
                    ).first()
                    
                    departamento = Location.query.filter_by(
                        departamento_codigo=mesa.departamento_codigo,
                        tipo='departamento'
                    ).first()
                    
                    puesto_id = puesto.id if puesto else None
                    municipio_id = municipio.id if municipio else None
                    departamento_id = departamento.id if departamento else None
            
            # Crear el incidente
            incidente = IncidenteElectoral(
                reportado_por_id=usuario_id,
                mesa_id=mesa_id,
                puesto_id=puesto_id,
                municipio_id=municipio_id,
                departamento_id=departamento_id,
                tipo_incidente=data.get('tipo_incidente'),
                titulo=data.get('titulo'),
                descripcion=data.get('descripcion'),
                severidad=data.get('severidad', 'media'),
                evidencia_url=data.get('evidencia_url'),
                ubicacion_gps=data.get('ubicacion_gps'),
                fecha_incidente=datetime.fromisoformat(data['fecha_incidente']) if data.get('fecha_incidente') else datetime.utcnow()
            )
            
            db.session.add(incidente)
            db.session.flush()
            
            # Registrar seguimiento
            IncidentesDelitosService._registrar_seguimiento(
                'incidente', incidente.id, usuario_id, 'crear', 
                f'Incidente reportado: {incidente.titulo}'
            )
            
            # Crear notificaciones
            IncidentesDelitosService._crear_notificaciones_incidente(incidente)
            
            db.session.commit()
            return incidente
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def crear_delito(data, usuario_id):
        """
        Crear un nuevo delito electoral
        
        Args:
            data: dict con datos del delito
            usuario_id: ID del usuario que reporta
            
        Returns:
            DelitoElectoral: Delito creado
        """
        try:
            # Obtener información del usuario
            usuario = User.query.get(usuario_id)
            if not usuario:
                raise ValueError('Usuario no encontrado')
            
            # Determinar ubicaciones
            mesa_id = data.get('mesa_id')
            puesto_id = None
            municipio_id = None
            departamento_id = None
            
            if mesa_id:
                mesa = Location.query.get(mesa_id)
                if mesa:
                    # Buscar ubicaciones relacionadas
                    puesto = Location.query.filter_by(
                        puesto_codigo=mesa.puesto_codigo,
                        zona_codigo=mesa.zona_codigo,
                        municipio_codigo=mesa.municipio_codigo,
                        departamento_codigo=mesa.departamento_codigo,
                        tipo='puesto'
                    ).first()
                    
                    municipio = Location.query.filter_by(
                        municipio_codigo=mesa.municipio_codigo,
                        departamento_codigo=mesa.departamento_codigo,
                        tipo='municipio'
                    ).first()
                    
                    departamento = Location.query.filter_by(
                        departamento_codigo=mesa.departamento_codigo,
                        tipo='departamento'
                    ).first()
                    
                    puesto_id = puesto.id if puesto else None
                    municipio_id = municipio.id if municipio else None
                    departamento_id = departamento.id if departamento else None
            
            # Crear el delito
            delito = DelitoElectoral(
                reportado_por_id=usuario_id,
                mesa_id=mesa_id,
                puesto_id=puesto_id,
                municipio_id=municipio_id,
                departamento_id=departamento_id,
                tipo_delito=data.get('tipo_delito'),
                titulo=data.get('titulo'),
                descripcion=data.get('descripcion'),
                gravedad=data.get('gravedad', 'media'),
                evidencia_url=data.get('evidencia_url'),
                testigos_adicionales=data.get('testigos_adicionales'),
                ubicacion_gps=data.get('ubicacion_gps'),
                fecha_delito=datetime.fromisoformat(data['fecha_delito']) if data.get('fecha_delito') else datetime.utcnow()
            )
            
            db.session.add(delito)
            db.session.flush()
            
            # Registrar seguimiento
            IncidentesDelitosService._registrar_seguimiento(
                'delito', delito.id, usuario_id, 'crear', 
                f'Delito reportado: {delito.titulo}'
            )
            
            # Crear notificaciones (más urgentes para delitos)
            IncidentesDelitosService._crear_notificaciones_delito(delito)
            
            db.session.commit()
            return delito
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def obtener_incidentes(filtros=None, usuario_id=None, rol_usuario=None):
        """
        Obtener incidentes según filtros y permisos del usuario
        
        Args:
            filtros: dict con filtros opcionales
            usuario_id: ID del usuario que consulta
            rol_usuario: Rol del usuario
            
        Returns:
            list: Lista de incidentes
        """
        query = IncidenteElectoral.query
        
        # Aplicar filtros de permisos según el rol
        if rol_usuario == 'testigo_electoral':
            # Testigos solo ven sus propios reportes
            query = query.filter(IncidenteElectoral.reportado_por_id == usuario_id)
        elif rol_usuario == 'coordinador_puesto':
            # Coordinadores de puesto ven incidentes de su puesto
            usuario = User.query.get(usuario_id)
            if usuario and usuario.ubicacion_id:
                query = query.filter(IncidenteElectoral.puesto_id == usuario.ubicacion_id)
        elif rol_usuario == 'coordinador_municipal':
            # Coordinadores municipales ven incidentes de su municipio
            usuario = User.query.get(usuario_id)
            if usuario and usuario.ubicacion_id:
                query = query.filter(IncidenteElectoral.municipio_id == usuario.ubicacion_id)
        elif rol_usuario == 'coordinador_departamental':
            # Coordinadores departamentales ven incidentes de su departamento
            usuario = User.query.get(usuario_id)
            if usuario and usuario.ubicacion_id:
                query = query.filter(IncidenteElectoral.departamento_id == usuario.ubicacion_id)
        # super_admin y auditor_electoral ven todos
        
        # Aplicar filtros adicionales
        if filtros:
            if filtros.get('estado'):
                query = query.filter(IncidenteElectoral.estado == filtros['estado'])
            if filtros.get('severidad'):
                query = query.filter(IncidenteElectoral.severidad == filtros['severidad'])
            if filtros.get('tipo_incidente'):
                query = query.filter(IncidenteElectoral.tipo_incidente == filtros['tipo_incidente'])
            if filtros.get('fecha_desde'):
                query = query.filter(IncidenteElectoral.fecha_reporte >= datetime.fromisoformat(filtros['fecha_desde']))
            if filtros.get('fecha_hasta'):
                query = query.filter(IncidenteElectoral.fecha_reporte <= datetime.fromisoformat(filtros['fecha_hasta']))
        
        # Ordenar por fecha de reporte descendente
        incidentes = query.order_by(desc(IncidenteElectoral.fecha_reporte)).all()
        
        return [incidente.to_dict() for incidente in incidentes]
    
    @staticmethod
    def obtener_delitos(filtros=None, usuario_id=None, rol_usuario=None):
        """
        Obtener delitos según filtros y permisos del usuario
        
        Args:
            filtros: dict con filtros opcionales
            usuario_id: ID del usuario que consulta
            rol_usuario: Rol del usuario
            
        Returns:
            list: Lista de delitos
        """
        query = DelitoElectoral.query
        
        # Aplicar filtros de permisos según el rol
        if rol_usuario == 'testigo_electoral':
            # Testigos solo ven sus propios reportes
            query = query.filter(DelitoElectoral.reportado_por_id == usuario_id)
        elif rol_usuario == 'coordinador_puesto':
            # Coordinadores de puesto ven delitos de su puesto
            usuario = User.query.get(usuario_id)
            if usuario and usuario.ubicacion_id:
                query = query.filter(DelitoElectoral.puesto_id == usuario.ubicacion_id)
        elif rol_usuario == 'coordinador_municipal':
            # Coordinadores municipales ven delitos de su municipio
            usuario = User.query.get(usuario_id)
            if usuario and usuario.ubicacion_id:
                query = query.filter(DelitoElectoral.municipio_id == usuario.ubicacion_id)
        elif rol_usuario == 'coordinador_departamental':
            # Coordinadores departamentales ven delitos de su departamento
            usuario = User.query.get(usuario_id)
            if usuario and usuario.ubicacion_id:
                query = query.filter(DelitoElectoral.departamento_id == usuario.ubicacion_id)
        # super_admin y auditor_electoral ven todos
        
        # Aplicar filtros adicionales
        if filtros:
            if filtros.get('estado'):
                query = query.filter(DelitoElectoral.estado == filtros['estado'])
            if filtros.get('gravedad'):
                query = query.filter(DelitoElectoral.gravedad == filtros['gravedad'])
            if filtros.get('tipo_delito'):
                query = query.filter(DelitoElectoral.tipo_delito == filtros['tipo_delito'])
            if filtros.get('fecha_desde'):
                query = query.filter(DelitoElectoral.fecha_reporte >= datetime.fromisoformat(filtros['fecha_desde']))
            if filtros.get('fecha_hasta'):
                query = query.filter(DelitoElectoral.fecha_reporte <= datetime.fromisoformat(filtros['fecha_hasta']))
        
        # Ordenar por fecha de reporte descendente
        delitos = query.order_by(desc(DelitoElectoral.fecha_reporte)).all()
        
        return [delito.to_dict() for delito in delitos]
    
    @staticmethod
    def actualizar_estado_incidente(incidente_id, nuevo_estado, usuario_id, comentario=None):
        """
        Actualizar estado de un incidente
        
        Args:
            incidente_id: ID del incidente
            nuevo_estado: Nuevo estado
            usuario_id: ID del usuario que actualiza
            comentario: Comentario opcional
            
        Returns:
            IncidenteElectoral: Incidente actualizado
        """
        try:
            incidente = IncidenteElectoral.query.get(incidente_id)
            if not incidente:
                raise ValueError('Incidente no encontrado')
            
            estado_anterior = incidente.estado
            incidente.estado = nuevo_estado
            incidente.updated_at = datetime.utcnow()
            
            if nuevo_estado == 'resuelto':
                incidente.resuelto_por_id = usuario_id
                incidente.fecha_resolucion = datetime.utcnow()
                if comentario:
                    incidente.notas_resolucion = comentario
            
            # Registrar seguimiento
            IncidentesDelitosService._registrar_seguimiento(
                'incidente', incidente_id, usuario_id, 'cambiar_estado',
                comentario or f'Estado cambiado de {estado_anterior} a {nuevo_estado}',
                estado_anterior, nuevo_estado
            )
            
            db.session.commit()
            return incidente
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def actualizar_estado_delito(delito_id, nuevo_estado, usuario_id, comentario=None):
        """
        Actualizar estado de un delito
        
        Args:
            delito_id: ID del delito
            nuevo_estado: Nuevo estado
            usuario_id: ID del usuario que actualiza
            comentario: Comentario opcional
            
        Returns:
            DelitoElectoral: Delito actualizado
        """
        try:
            delito = DelitoElectoral.query.get(delito_id)
            if not delito:
                raise ValueError('Delito no encontrado')
            
            estado_anterior = delito.estado
            delito.estado = nuevo_estado
            delito.updated_at = datetime.utcnow()
            
            if nuevo_estado == 'en_investigacion':
                delito.investigado_por_id = usuario_id
                delito.fecha_investigacion = datetime.utcnow()
            elif nuevo_estado == 'investigado' and comentario:
                delito.resultado_investigacion = comentario
            
            # Registrar seguimiento
            IncidentesDelitosService._registrar_seguimiento(
                'delito', delito_id, usuario_id, 'cambiar_estado',
                comentario or f'Estado cambiado de {estado_anterior} a {nuevo_estado}',
                estado_anterior, nuevo_estado
            )
            
            db.session.commit()
            return delito
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def denunciar_formalmente(delito_id, usuario_id, numero_denuncia, autoridad_competente):
        """
        Marcar un delito como denunciado formalmente
        
        Args:
            delito_id: ID del delito
            usuario_id: ID del usuario que denuncia
            numero_denuncia: Número de la denuncia
            autoridad_competente: Autoridad que recibe la denuncia
            
        Returns:
            DelitoElectoral: Delito actualizado
        """
        try:
            delito = DelitoElectoral.query.get(delito_id)
            if not delito:
                raise ValueError('Delito no encontrado')
            
            delito.denunciado_formalmente = True
            delito.numero_denuncia = numero_denuncia
            delito.autoridad_competente = autoridad_competente
            delito.fecha_denuncia = datetime.utcnow()
            delito.estado = 'denunciado'
            delito.updated_at = datetime.utcnow()
            
            # Registrar seguimiento
            IncidentesDelitosService._registrar_seguimiento(
                'delito', delito_id, usuario_id, 'denunciar',
                f'Delito denunciado formalmente. Número: {numero_denuncia}, Autoridad: {autoridad_competente}'
            )
            
            db.session.commit()
            return delito
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def obtener_estadisticas(usuario_id=None, rol_usuario=None):
        """
        Obtener estadísticas de incidentes y delitos
        
        Args:
            usuario_id: ID del usuario
            rol_usuario: Rol del usuario
            
        Returns:
            dict: Estadísticas
        """
        # Aplicar filtros según el rol
        incidentes_query = IncidenteElectoral.query
        delitos_query = DelitoElectoral.query
        
        if rol_usuario == 'testigo_electoral':
            incidentes_query = incidentes_query.filter(IncidenteElectoral.reportado_por_id == usuario_id)
            delitos_query = delitos_query.filter(DelitoElectoral.reportado_por_id == usuario_id)
        elif rol_usuario == 'coordinador_puesto':
            usuario = User.query.get(usuario_id)
            if usuario and usuario.ubicacion_id:
                incidentes_query = incidentes_query.filter(IncidenteElectoral.puesto_id == usuario.ubicacion_id)
                delitos_query = delitos_query.filter(DelitoElectoral.puesto_id == usuario.ubicacion_id)
        elif rol_usuario == 'coordinador_municipal':
            usuario = User.query.get(usuario_id)
            if usuario and usuario.ubicacion_id:
                incidentes_query = incidentes_query.filter(IncidenteElectoral.municipio_id == usuario.ubicacion_id)
                delitos_query = delitos_query.filter(DelitoElectoral.municipio_id == usuario.ubicacion_id)
        elif rol_usuario == 'coordinador_departamental':
            usuario = User.query.get(usuario_id)
            if usuario and usuario.ubicacion_id:
                incidentes_query = incidentes_query.filter(IncidenteElectoral.departamento_id == usuario.ubicacion_id)
                delitos_query = delitos_query.filter(DelitoElectoral.departamento_id == usuario.ubicacion_id)
        
        # Estadísticas de incidentes
        total_incidentes = incidentes_query.count()
        incidentes_por_estado = {}
        for estado in ['reportado', 'en_revision', 'resuelto', 'escalado']:
            incidentes_por_estado[estado] = incidentes_query.filter(IncidenteElectoral.estado == estado).count()
        
        incidentes_por_severidad = {}
        for severidad in ['baja', 'media', 'alta', 'critica']:
            incidentes_por_severidad[severidad] = incidentes_query.filter(IncidenteElectoral.severidad == severidad).count()
        
        # Estadísticas de delitos
        total_delitos = delitos_query.count()
        delitos_por_estado = {}
        for estado in ['reportado', 'en_investigacion', 'investigado', 'denunciado', 'archivado']:
            delitos_por_estado[estado] = delitos_query.filter(DelitoElectoral.estado == estado).count()
        
        delitos_por_gravedad = {}
        for gravedad in ['leve', 'media', 'grave', 'muy_grave']:
            delitos_por_gravedad[gravedad] = delitos_query.filter(DelitoElectoral.gravedad == gravedad).count()
        
        delitos_denunciados = delitos_query.filter(DelitoElectoral.denunciado_formalmente == True).count()
        
        return {
            'incidentes': {
                'total': total_incidentes,
                'por_estado': incidentes_por_estado,
                'por_severidad': incidentes_por_severidad
            },
            'delitos': {
                'total': total_delitos,
                'por_estado': delitos_por_estado,
                'por_gravedad': delitos_por_gravedad,
                'denunciados': delitos_denunciados
            }
        }
    
    @staticmethod
    def _registrar_seguimiento(tipo_reporte, reporte_id, usuario_id, accion, comentario=None, estado_anterior=None, estado_nuevo=None):
        """
        Registrar seguimiento de un reporte
        
        Args:
            tipo_reporte: 'incidente' o 'delito'
            reporte_id: ID del reporte
            usuario_id: ID del usuario
            accion: Acción realizada
            comentario: Comentario opcional
            estado_anterior: Estado anterior
            estado_nuevo: Estado nuevo
        """
        seguimiento = SeguimientoReporte(
            incidente_id=reporte_id if tipo_reporte == 'incidente' else None,
            delito_id=reporte_id if tipo_reporte == 'delito' else None,
            usuario_id=usuario_id,
            accion=accion,
            comentario=comentario,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_nuevo
        )
        db.session.add(seguimiento)
    
    @staticmethod
    def _crear_notificaciones_incidente(incidente):
        """
        Crear notificaciones para un nuevo incidente
        
        Args:
            incidente: IncidenteElectoral
        """
        # Notificar al coordinador de puesto
        if incidente.puesto_id:
            coordinadores_puesto = User.query.filter_by(
                rol='coordinador_puesto',
                ubicacion_id=incidente.puesto_id
            ).all()
            
            for coordinador in coordinadores_puesto:
                notificacion = NotificacionReporte(
                    usuario_id=coordinador.id,
                    tipo_reporte='incidente',
                    reporte_id=incidente.id,
                    tipo_notificacion='nuevo_incidente',
                    titulo=f'Nuevo incidente: {incidente.titulo}',
                    mensaje=f'Se ha reportado un incidente de tipo {incidente.tipo_incidente} con severidad {incidente.severidad}'
                )
                db.session.add(notificacion)
        
        # Si es crítico, notificar también al coordinador municipal
        if incidente.severidad == 'critica' and incidente.municipio_id:
            coordinadores_municipales = User.query.filter_by(
                rol='coordinador_municipal',
                ubicacion_id=incidente.municipio_id
            ).all()
            
            for coordinador in coordinadores_municipales:
                notificacion = NotificacionReporte(
                    usuario_id=coordinador.id,
                    tipo_reporte='incidente',
                    reporte_id=incidente.id,
                    tipo_notificacion='incidente_critico',
                    titulo=f'⚠️ Incidente CRÍTICO: {incidente.titulo}',
                    mensaje=f'Se ha reportado un incidente crítico que requiere atención inmediata'
                )
                db.session.add(notificacion)
    
    @staticmethod
    def _crear_notificaciones_delito(delito):
        """
        Crear notificaciones para un nuevo delito
        
        Args:
            delito: DelitoElectoral
        """
        # Notificar al coordinador municipal (los delitos son más graves)
        if delito.municipio_id:
            coordinadores_municipales = User.query.filter_by(
                rol='coordinador_municipal',
                ubicacion_id=delito.municipio_id
            ).all()
            
            for coordinador in coordinadores_municipales:
                notificacion = NotificacionReporte(
                    usuario_id=coordinador.id,
                    tipo_reporte='delito',
                    reporte_id=delito.id,
                    tipo_notificacion='nuevo_delito',
                    titulo=f'🚨 Nuevo delito electoral: {delito.titulo}',
                    mensaje=f'Se ha reportado un delito de tipo {delito.tipo_delito} con gravedad {delito.gravedad}'
                )
                db.session.add(notificacion)
        
        # Notificar también al coordinador departamental
        if delito.departamento_id:
            coordinadores_departamentales = User.query.filter_by(
                rol='coordinador_departamental',
                ubicacion_id=delito.departamento_id
            ).all()
            
            for coordinador in coordinadores_departamentales:
                notificacion = NotificacionReporte(
                    usuario_id=coordinador.id,
                    tipo_reporte='delito',
                    reporte_id=delito.id,
                    tipo_notificacion='nuevo_delito',
                    titulo=f'🚨 Nuevo delito electoral: {delito.titulo}',
                    mensaje=f'Se ha reportado un delito electoral en su departamento'
                )
                db.session.add(notificacion)
        
        # Notificar a auditores
        auditores = User.query.filter_by(rol='auditor_electoral').all()
        for auditor in auditores:
            notificacion = NotificacionReporte(
                usuario_id=auditor.id,
                tipo_reporte='delito',
                reporte_id=delito.id,
                tipo_notificacion='nuevo_delito',
                titulo=f'🚨 Nuevo delito electoral: {delito.titulo}',
                mensaje=f'Se ha reportado un delito electoral que requiere investigación'
            )
            db.session.add(notificacion)
    
    @staticmethod
    def obtener_seguimiento(tipo_reporte, reporte_id):
        """
        Obtener historial de seguimiento de un reporte
        
        Args:
            tipo_reporte: 'incidente' o 'delito'
            reporte_id: ID del reporte
            
        Returns:
            list: Lista de seguimientos
        """
        if tipo_reporte == 'incidente':
            seguimientos = SeguimientoReporte.query.filter_by(
                incidente_id=reporte_id
            ).order_by(desc(SeguimientoReporte.fecha_accion)).all()
        else:
            seguimientos = SeguimientoReporte.query.filter_by(
                delito_id=reporte_id
            ).order_by(desc(SeguimientoReporte.fecha_accion)).all()
        
        return [seg.to_dict() for seg in seguimientos]
    
    @staticmethod
    def obtener_notificaciones(usuario_id, solo_no_leidas=False):
        """
        Obtener notificaciones de un usuario
        
        Args:
            usuario_id: ID del usuario
            solo_no_leidas: Si True, solo devuelve notificaciones no leídas
            
        Returns:
            list: Lista de notificaciones
        """
        query = NotificacionReporte.query.filter_by(usuario_id=usuario_id)
        
        if solo_no_leidas:
            query = query.filter_by(leida=False)
        
        notificaciones = query.order_by(desc(NotificacionReporte.created_at)).all()
        
        return [notif.to_dict() for notif in notificaciones]
    
    @staticmethod
    def marcar_notificacion_leida(notificacion_id):
        """
        Marcar una notificación como leída
        
        Args:
            notificacion_id: ID de la notificación
        """
        notificacion = NotificacionReporte.query.get(notificacion_id)
        if notificacion:
            notificacion.marcar_como_leida()
    
