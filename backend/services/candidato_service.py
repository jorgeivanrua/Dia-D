"""
Servicio para gestión de Candidatos
"""
from backend.database import db
from backend.models.candidato import Candidato
from backend.models.partido_politico import PartidoPolitico
from backend.models.tipo_eleccion import TipoEleccion
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_


class CandidatoService:
    """Servicio para operaciones CRUD de candidatos"""
    
    @staticmethod
    def listar_candidatos(filtros=None, pagina=1, por_pagina=50):
        """
        Listar candidatos con filtros opcionales
        
        Args:
            filtros: dict con filtros opcionales (partido_id, tipo_eleccion_id, activo, busqueda)
            pagina: número de página
            por_pagina: registros por página
            
        Returns:
            dict con candidatos y metadatos de paginación
        """
        query = Candidato.query
        
        # Aplicar filtros
        if filtros:
            if 'partido_id' in filtros and filtros['partido_id']:
                query = query.filter_by(partido_id=filtros['partido_id'])
            
            if 'tipo_eleccion_id' in filtros and filtros['tipo_eleccion_id']:
                query = query.filter_by(tipo_eleccion_id=filtros['tipo_eleccion_id'])
            
            if 'activo' in filtros and filtros['activo'] is not None:
                query = query.filter_by(activo=filtros['activo'])
            
            if 'busqueda' in filtros and filtros['busqueda']:
                busqueda = f"%{filtros['busqueda']}%"
                query = query.filter(
                    or_(
                        Candidato.nombre_completo.ilike(busqueda),
                        Candidato.cargo.ilike(busqueda)
                    )
                )
        
        # Ordenar por nombre
        query = query.order_by(Candidato.nombre_completo)
        
        # Paginar
        paginacion = query.paginate(page=pagina, per_page=por_pagina, error_out=False)
        
        return {
            'candidatos': [c.to_dict() for c in paginacion.items],
            'total': paginacion.total,
            'pagina': pagina,
            'por_pagina': por_pagina,
            'total_paginas': paginacion.pages
        }
    
    @staticmethod
    def obtener_candidato(candidato_id):
        """
        Obtener un candidato por ID
        
        Args:
            candidato_id: ID del candidato
            
        Returns:
            dict con datos del candidato o None si no existe
        """
        candidato = Candidato.query.get(candidato_id)
        return candidato.to_dict() if candidato else None
    
    @staticmethod
    def crear_candidato(data):
        """
        Crear un nuevo candidato
        
        Args:
            data: dict con datos del candidato
            
        Returns:
            tuple (candidato_dict, error_message)
        """
        try:
            # Validar campos obligatorios
            if not data.get('nombre_completo'):
                return None, 'El nombre completo es obligatorio'
            
            if not data.get('partido_id'):
                return None, 'El partido es obligatorio'
            
            if not data.get('tipo_eleccion_id'):
                return None, 'El tipo de elección es obligatorio'
            
            if not data.get('cargo'):
                return None, 'El cargo es obligatorio'
            
            # Validar que el partido existe
            partido = PartidoPolitico.query.get(data['partido_id'])
            if not partido:
                return None, 'El partido especificado no existe'
            
            if not partido.activo:
                return None, 'El partido especificado no está activo'
            
            # Validar que el tipo de elección existe
            tipo_eleccion = TipoEleccion.query.get(data['tipo_eleccion_id'])
            if not tipo_eleccion:
                return None, 'El tipo de elección especificado no existe'
            
            # Crear candidato
            candidato = Candidato(
                nombre_completo=data['nombre_completo'].strip(),
                partido_id=data['partido_id'],
                tipo_eleccion_id=data['tipo_eleccion_id'],
                cargo=data['cargo'].strip(),
                numero_lista=data.get('numero_lista'),
                foto_url=data.get('foto_url'),
                biografia=data.get('biografia'),
                activo=data.get('activo', True)
            )
            
            db.session.add(candidato)
            db.session.commit()
            
            return candidato.to_dict(), None
            
        except IntegrityError as e:
            db.session.rollback()
            return None, 'Error de integridad en la base de datos'
        except Exception as e:
            db.session.rollback()
            return None, f'Error al crear candidato: {str(e)}'
    
    @staticmethod
    def actualizar_candidato(candidato_id, data):
        """
        Actualizar un candidato existente
        
        Args:
            candidato_id: ID del candidato
            data: dict con datos a actualizar
            
        Returns:
            tuple (candidato_dict, error_message)
        """
        try:
            candidato = Candidato.query.get(candidato_id)
            
            if not candidato:
                return None, 'Candidato no encontrado'
            
            # Validar partido si se está actualizando
            if 'partido_id' in data:
                partido = PartidoPolitico.query.get(data['partido_id'])
                if not partido:
                    return None, 'El partido especificado no existe'
                if not partido.activo:
                    return None, 'El partido especificado no está activo'
                candidato.partido_id = data['partido_id']
            
            # Validar tipo de elección si se está actualizando
            if 'tipo_eleccion_id' in data:
                tipo_eleccion = TipoEleccion.query.get(data['tipo_eleccion_id'])
                if not tipo_eleccion:
                    return None, 'El tipo de elección especificado no existe'
                candidato.tipo_eleccion_id = data['tipo_eleccion_id']
            
            # Actualizar otros campos
            if 'nombre_completo' in data and data['nombre_completo']:
                candidato.nombre_completo = data['nombre_completo'].strip()
            
            if 'cargo' in data and data['cargo']:
                candidato.cargo = data['cargo'].strip()
            
            if 'numero_lista' in data:
                candidato.numero_lista = data['numero_lista']
            
            if 'foto_url' in data:
                candidato.foto_url = data['foto_url']
            
            if 'biografia' in data:
                candidato.biografia = data['biografia']
            
            if 'activo' in data:
                candidato.activo = data['activo']
            
            db.session.commit()
            
            return candidato.to_dict(), None
            
        except IntegrityError as e:
            db.session.rollback()
            return None, 'Error de integridad en la base de datos'
        except Exception as e:
            db.session.rollback()
            return None, f'Error al actualizar candidato: {str(e)}'
    
    @staticmethod
    def eliminar_candidato(candidato_id):
        """
        Eliminar un candidato
        Verifica que no tenga votos registrados antes de eliminar
        
        Args:
            candidato_id: ID del candidato
            
        Returns:
            tuple (success, error_message)
        """
        try:
            candidato = Candidato.query.get(candidato_id)
            
            if not candidato:
                return False, 'Candidato no encontrado'
            
            # TODO: Verificar que no tenga votos registrados
            # Esta verificación se implementará cuando exista el modelo de votos
            # Por ahora, permitimos la eliminación
            
            db.session.delete(candidato)
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f'Error al eliminar candidato: {str(e)}'
    
    @staticmethod
    def validar_foto(archivo):
        """
        Validar archivo de foto
        
        Args:
            archivo: FileStorage object
            
        Returns:
            tuple (valid, error_message)
        """
        if not archivo:
            return False, 'No se proporcionó archivo'
        
        # Validar extensión
        extensiones_permitidas = {'png', 'jpg', 'jpeg', 'webp'}
        extension = archivo.filename.rsplit('.', 1)[1].lower() if '.' in archivo.filename else ''
        
        if extension not in extensiones_permitidas:
            return False, f'Formato no permitido. Use: {", ".join(extensiones_permitidas)}'
        
        # Validar tamaño (max 5MB)
        archivo.seek(0, 2)  # Ir al final del archivo
        tamano = archivo.tell()
        archivo.seek(0)  # Volver al inicio
        
        max_tamano = 5 * 1024 * 1024  # 5MB
        if tamano > max_tamano:
            return False, f'El archivo es muy grande. Tamaño máximo: 5MB'
        
        return True, None
