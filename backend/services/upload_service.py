"""
Servicio para gestión de upload de evidencia fotográfica
"""
import os
import hashlib
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from backend.database import db
from backend.models.incidentes_delitos import EvidenciaFotografica


class UploadService:
    """Servicio para gestión de archivos de evidencia"""
    
    # Configuración
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'heic', 'heif'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads/evidencias')
    MAX_IMAGE_WIDTH = 1920
    MAX_IMAGE_HEIGHT = 1080
    COMPRESSION_QUALITY = 85
    
    @staticmethod
    def validate_file(file):
        """
        Validar archivo de evidencia
        
        Args:
            file: FileStorage object
            
        Returns:
            tuple: (is_valid, error_message)
        """
        # Verificar que hay archivo
        if not file or file.filename == '':
            return False, 'No se proporcionó ningún archivo'
        
        # Verificar extensión
        filename = file.filename.lower()
        extension = filename.rsplit('.', 1)[1] if '.' in filename else ''
        
        if extension not in UploadService.ALLOWED_EXTENSIONS:
            return False, f'Tipo de archivo no permitido. Permitidos: {", ".join(UploadService.ALLOWED_EXTENSIONS)}'
        
        # Verificar tamaño (si es posible)
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        
        if size > UploadService.MAX_FILE_SIZE:
            return False, f'Archivo demasiado grande. Máximo: {UploadService.MAX_FILE_SIZE / (1024*1024)}MB'
        
        return True, None
    
    @staticmethod
    def generate_unique_filename(original_filename):
        """
        Generar nombre único para archivo
        
        Args:
            original_filename: Nombre original del archivo
            
        Returns:
            str: Nombre único generado
        """
        # Obtener extensión
        extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
        
        # Generar timestamp
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        
        # Generar UUID corto
        unique_id = str(uuid.uuid4())[:8]
        
        # Generar hash del nombre original
        name_hash = hashlib.md5(original_filename.encode()).hexdigest()[:8]
        
        # Combinar: timestamp_uuid_hash.ext
        unique_filename = f"{timestamp}_{unique_id}_{name_hash}.{extension}"
        
        return secure_filename(unique_filename)
    
    @staticmethod
    def compress_image(image_path, max_width=None, max_height=None, quality=None):
        """
        Comprimir imagen manteniendo calidad aceptable
        
        Args:
            image_path: Ruta de la imagen
            max_width: Ancho máximo (opcional)
            max_height: Alto máximo (opcional)
            quality: Calidad de compresión (opcional)
            
        Returns:
            tuple: (width, height) de la imagen resultante
        """
        max_width = max_width or UploadService.MAX_IMAGE_WIDTH
        max_height = max_height or UploadService.MAX_IMAGE_HEIGHT
        quality = quality or UploadService.COMPRESSION_QUALITY
        
        try:
            with Image.open(image_path) as img:
                # Convertir HEIC/HEIF a JPEG si es necesario
                if img.format in ['HEIC', 'HEIF']:
                    img = img.convert('RGB')
                
                # Obtener dimensiones originales
                original_width, original_height = img.size
                
                # Calcular nuevas dimensiones manteniendo aspect ratio
                width, height = original_width, original_height
                
                if width > max_width:
                    height = int((height * max_width) / width)
                    width = max_width
                
                if height > max_height:
                    width = int((width * max_height) / height)
                    height = max_height
                
                # Redimensionar si es necesario
                if width < original_width or height < original_height:
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                
                # Guardar con compresión
                img.save(image_path, 'JPEG', quality=quality, optimize=True)
                
                return width, height
                
        except Exception as e:
            print(f"Error comprimiendo imagen: {e}")
            # Si falla la compresión, retornar dimensiones originales
            return None, None

    
    @staticmethod
    def extract_gps_metadata(image_path):
        """
        Extraer metadatos GPS de imagen
        
        Args:
            image_path: Ruta de la imagen
            
        Returns:
            dict: {'latitud': float, 'longitud': float, 'fecha_captura': datetime, 'dispositivo': str}
        """
        metadata = {
            'latitud': None,
            'longitud': None,
            'fecha_captura': None,
            'dispositivo': None
        }
        
        try:
            with Image.open(image_path) as img:
                exif_data = img._getexif()
                
                if not exif_data:
                    return metadata
                
                # Extraer información GPS
                gps_info = {}
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    
                    if tag_name == 'GPSInfo':
                        for gps_tag in value:
                            gps_tag_name = GPSTAGS.get(gps_tag, gps_tag)
                            gps_info[gps_tag_name] = value[gps_tag]
                    
                    elif tag_name == 'DateTime' or tag_name == 'DateTimeOriginal':
                        try:
                            metadata['fecha_captura'] = datetime.strptime(
                                str(value), '%Y:%m:%d %H:%M:%S'
                            )
                        except:
                            pass
                    
                    elif tag_name == 'Make' or tag_name == 'Model':
                        if metadata['dispositivo']:
                            metadata['dispositivo'] += f" {value}"
                        else:
                            metadata['dispositivo'] = str(value)
                
                # Convertir coordenadas GPS
                if 'GPSLatitude' in gps_info and 'GPSLongitude' in gps_info:
                    lat = UploadService._convert_gps_to_decimal(
                        gps_info['GPSLatitude'],
                        gps_info.get('GPSLatitudeRef', 'N')
                    )
                    lon = UploadService._convert_gps_to_decimal(
                        gps_info['GPSLongitude'],
                        gps_info.get('GPSLongitudeRef', 'E')
                    )
                    
                    metadata['latitud'] = lat
                    metadata['longitud'] = lon
                
        except Exception as e:
            print(f"Error extrayendo metadatos GPS: {e}")
        
        return metadata
    
    @staticmethod
    def _convert_gps_to_decimal(gps_coord, ref):
        """
        Convertir coordenadas GPS de formato DMS a decimal
        
        Args:
            gps_coord: Tupla (grados, minutos, segundos)
            ref: Referencia (N/S para latitud, E/W para longitud)
            
        Returns:
            float: Coordenada en formato decimal
        """
        try:
            degrees = float(gps_coord[0])
            minutes = float(gps_coord[1])
            seconds = float(gps_coord[2])
            
            decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
            
            if ref in ['S', 'W']:
                decimal = -decimal
            
            return decimal
        except:
            return None
    
    @staticmethod
    def upload_evidencia(file, tipo_reporte, reporte_id, user_id):
        """
        Subir archivo de evidencia
        
        Args:
            file: FileStorage object
            tipo_reporte: 'incidente' o 'delito'
            reporte_id: ID del reporte
            user_id: ID del usuario que sube
            
        Returns:
            dict: Información de la evidencia subida
            
        Raises:
            ValueError: Si hay error en validación
            Exception: Si hay error en el proceso
        """
        # Validar archivo
        is_valid, error = UploadService.validate_file(file)
        if not is_valid:
            raise ValueError(error)
        
        # Validar tipo de reporte
        if tipo_reporte not in ['incidente', 'delito']:
            raise ValueError('Tipo de reporte inválido')
        
        try:
            # Generar nombre único
            original_filename = file.filename
            unique_filename = UploadService.generate_unique_filename(original_filename)
            
            # Crear directorio si no existe
            upload_dir = UploadService.UPLOAD_FOLDER
            os.makedirs(upload_dir, exist_ok=True)
            
            # Guardar archivo temporalmente
            file_path = os.path.join(upload_dir, unique_filename)
            file.save(file_path)
            
            # Obtener tamaño original
            original_size = os.path.getsize(file_path)
            
            # Comprimir imagen
            width, height = UploadService.compress_image(file_path)
            
            # Obtener tamaño después de compresión
            compressed_size = os.path.getsize(file_path)
            
            # Extraer metadatos GPS
            gps_metadata = UploadService.extract_gps_metadata(file_path)
            
            # Generar URL de acceso
            url = f"/api/evidencia/{unique_filename}"
            
            # Crear registro en base de datos
            evidencia = EvidenciaFotografica(
                incidente_id=reporte_id if tipo_reporte == 'incidente' else None,
                delito_id=reporte_id if tipo_reporte == 'delito' else None,
                filename=unique_filename,
                filename_original=original_filename,
                url=url,
                mime_type=file.content_type or 'image/jpeg',
                size_bytes=compressed_size,
                width=width,
                height=height,
                latitud=gps_metadata['latitud'],
                longitud=gps_metadata['longitud'],
                fecha_captura=gps_metadata['fecha_captura'],
                dispositivo=gps_metadata['dispositivo'],
                subido_por_id=user_id
            )
            
            db.session.add(evidencia)
            db.session.commit()
            
            return {
                'id': evidencia.id,
                'filename': unique_filename,
                'url': url,
                'size_bytes': compressed_size,
                'original_size_bytes': original_size,
                'compression_ratio': round((1 - compressed_size / original_size) * 100, 2) if original_size > 0 else 0,
                'width': width,
                'height': height,
                'has_gps': gps_metadata['latitud'] is not None,
                'latitud': gps_metadata['latitud'],
                'longitud': gps_metadata['longitud'],
                'fecha_captura': gps_metadata['fecha_captura'].isoformat() if gps_metadata['fecha_captura'] else None,
                'dispositivo': gps_metadata['dispositivo']
            }
            
        except Exception as e:
            db.session.rollback()
            # Eliminar archivo si hubo error
            if os.path.exists(file_path):
                os.remove(file_path)
            raise e
    
    @staticmethod
    def get_evidencia_path(filename):
        """
        Obtener ruta completa de un archivo de evidencia
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            str: Ruta completa del archivo
        """
        return os.path.join(UploadService.UPLOAD_FOLDER, filename)
    
    @staticmethod
    def delete_evidencia(evidencia_id):
        """
        Eliminar evidencia fotográfica
        
        Args:
            evidencia_id: ID de la evidencia
            
        Returns:
            bool: True si se eliminó exitosamente
        """
        try:
            evidencia = EvidenciaFotografica.query.get(evidencia_id)
            
            if not evidencia:
                return False
            
            # Eliminar archivo físico
            file_path = UploadService.get_evidencia_path(evidencia.filename)
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Eliminar registro de base de datos
            db.session.delete(evidencia)
            db.session.commit()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error eliminando evidencia: {e}")
            return False
