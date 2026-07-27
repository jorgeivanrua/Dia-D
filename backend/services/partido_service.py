"""
Servicio para gestión de Partidos Políticos
"""
from backend.database import db
from backend.models.partido_politico import PartidoPolitico
from backend.models.candidato import Candidato
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_


class PartidoService:
    """Servicio para operaciones CRUD de partidos políticos"""
    
    @staticmethod
    def listar_partidos(filtros=None, pagina=1, por_pagina=50):
        """
        Listar partidos con filtros opcionales
        
        Args:
            filtros: dict con filtros opcionales (activo, busqueda)
            pagina: número de página
            por_pagina: registros por página
            
        Returns:
            dict con partidos y metadatos de paginación
        """
        query = PartidoPolitico.query
        
        # Aplicar filtros
        if filtros:
            if 'activo' in filtros and filtros['activo'] is not None:
                query = query.filter_by(activo=filtros['activo'])
            
            if 'busqueda' in filtros and filtros['busqueda']:
                busqueda = f"%{filtros['busqueda']}%"
                query = query.filter(
                    or_(
                        PartidoPolitico.nombre.ilike(busqueda),
                        PartidoPolitico.sigla.ilike(busqueda)
                    )
                )
        
        # Ordenar por nombre
        query = query.order_by(PartidoPolitico.nombre)
        
        # Paginar
        paginacion = query.paginate(page=pagina, per_page=por_pagina, error_out=False)
        
        return {
            'partidos': [p.to_dict() for p in paginacion.items],
            'total': paginacion.total,
            'pagina': pagina,
            'por_pagina': por_pagina,
            'total_paginas': paginacion.pages
        }
    
    @staticmethod
    def obtener_partido(partido_id):
        """
        Obtener un partido por ID
        
        Args:
            partido_id: ID del partido
            
        Returns:
            dict con datos del partido o None si no existe
        """
        partido = PartidoPolitico.query.get(partido_id)
        return partido.to_dict() if partido else None
    
    @staticmethod
    def crear_partido(data):
        """
        Crear un nuevo partido político
        
        Args:
            data: dict con datos del partido (nombre, sigla, color, logo_url, descripcion)
            
        Returns:
            tuple (partido_dict, error_message)
        """
        try:
            # Validar campos obligatorios
            if not data.get('nombre'):
                return None, 'El nombre es obligatorio'
            
            if not data.get('sigla'):
                return None, 'La sigla es obligatoria'
            
            if not data.get('color'):
                return None, 'El color es obligatorio'
            
            # Validar formato de color
            if not PartidoPolitico.validar_color(data['color']):
                return None, 'El color debe tener formato hexadecimal (#RRGGBB)'
            
            # Crear partido
            partido = PartidoPolitico(
                nombre=data['nombre'].strip(),
                sigla=data['sigla'].strip().upper(),
                color=data['color'],
                logo_url=data.get('logo_url'),
                descripcion=data.get('descripcion'),
                activo=data.get('activo', True)
            )
            
            db.session.add(partido)
            db.session.commit()
            
            return partido.to_dict(), None
            
        except IntegrityError as e:
            db.session.rollback()
            if 'nombre' in str(e.orig):
                return None, 'Ya existe un partido con ese nombre'
            elif 'sigla' in str(e.orig):
                return None, 'Ya existe un partido con esa sigla'
            else:
                return None, 'Error de integridad en la base de datos'
        except Exception as e:
            db.session.rollback()
            return None, f'Error al crear partido: {str(e)}'
    
    @staticmethod
    def actualizar_partido(partido_id, data):
        """
        Actualizar un partido existente
        
        Args:
            partido_id: ID del partido
            data: dict con datos a actualizar
            
        Returns:
            tuple (partido_dict, error_message)
        """
        try:
            partido = PartidoPolitico.query.get(partido_id)
            
            if not partido:
                return None, 'Partido no encontrado'
            
            # Actualizar campos si están presentes
            if 'nombre' in data and data['nombre']:
                partido.nombre = data['nombre'].strip()
            
            if 'sigla' in data and data['sigla']:
                partido.sigla = data['sigla'].strip().upper()
            
            if 'color' in data:
                if not PartidoPolitico.validar_color(data['color']):
                    return None, 'El color debe tener formato hexadecimal (#RRGGBB)'
                partido.color = data['color']
            
            if 'logo_url' in data:
                partido.logo_url = data['logo_url']
            
            if 'descripcion' in data:
                partido.descripcion = data['descripcion']
            
            if 'activo' in data:
                partido.activo = data['activo']
            
            db.session.commit()
            
            return partido.to_dict(), None
            
        except IntegrityError as e:
            db.session.rollback()
            if 'nombre' in str(e.orig):
                return None, 'Ya existe un partido con ese nombre'
            elif 'sigla' in str(e.orig):
                return None, 'Ya existe un partido con esa sigla'
            else:
                return None, 'Error de integridad en la base de datos'
        except Exception as e:
            db.session.rollback()
            return None, f'Error al actualizar partido: {str(e)}'
    
    @staticmethod
    def eliminar_partido(partido_id):
        """
        Eliminar un partido político
        Verifica que no tenga candidatos asociados antes de eliminar
        
        Args:
            partido_id: ID del partido
            
        Returns:
            tuple (success, error_message)
        """
        try:
            partido = PartidoPolitico.query.get(partido_id)
            
            if not partido:
                return False, 'Partido no encontrado'
            
            # Verificar que no tenga candidatos asociados
            total_candidatos = Candidato.query.filter_by(partido_id=partido_id).count()
            
            if total_candidatos > 0:
                return False, f'No se puede eliminar el partido porque tiene {total_candidatos} candidato(s) asociado(s)'
            
            db.session.delete(partido)
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f'Error al eliminar partido: {str(e)}'
    
    @staticmethod
    def validar_logo(archivo):
        """
        Validar archivo de logo
        
        Args:
            archivo: FileStorage object
            
        Returns:
            tuple (valid, error_message)
        """
        if not archivo:
            return False, 'No se proporcionó archivo'
        
        # Validar extensión
        extensiones_permitidas = {'png', 'jpg', 'jpeg', 'webp', 'svg'}
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
