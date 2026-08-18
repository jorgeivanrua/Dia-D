"""
Servicio de autenticación
"""
from datetime import datetime, timedelta
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.utils.exceptions import (
    AuthenticationException,
    AccountBlockedException,
    ValidationException
)
from backend.utils.jwt_utils import generate_tokens
from backend.utils.logging_config import get_logger

logger = get_logger(__name__)


class AuthService:
    """Servicio para gestión de autenticación"""
    
    @staticmethod
    def authenticate_location_based(rol, ubicacion_data, password):
        """
        Autenticar usuario basado en rol, ubicación y contraseña
        
        Args:
            rol: Rol del usuario
            ubicacion_data: Dict con datos de ubicación jerárquica
            password: Contraseña
            
        Returns:
            tuple: (user, access_token, refresh_token)
        """
        logger.info(f"Autenticando: rol={rol}, ubicacion_data={ubicacion_data}")
        
        # Super admin, monitoreo y auditor no necesitan ubicación
        if rol in ['super_admin', 'monitoreo', 'auditor_electoral']:
            user = User.query.filter_by(
                rol=rol,
                activo=True
            ).first()
            logger.info(f"Usuario sin ubicación encontrado: {user.id if user else None}")
        else:
            # Buscar ubicación según jerarquía
            location = AuthService._find_location_by_hierarchy(rol, ubicacion_data)
            logger.info(f"Ubicación encontrada: {location.id if location else None}")
            
            if not location:
                raise AuthenticationException("Ubicación no encontrada")
            
            # Buscar usuario por rol y ubicación
            user = User.query.filter_by(
                rol=rol,
                ubicacion_id=location.id,
                activo=True
            ).first()

            # Si no hay usuario en el puesto, algunos testigos pueden estar registrados
            # a nivel de mesa dentro del mismo puesto.
            if not user and rol == 'testigo_electoral' and location.tipo == 'puesto':
                logger.info(
                    f"No se encontró usuario testigo en el puesto {location.puesto_codigo}; verificando mesas asociadas"
                )

                mesa_ids = [
                    mesa.id for mesa in Location.query.filter_by(
                        tipo='mesa',
                        departamento_codigo=location.departamento_codigo,
                        municipio_codigo=location.municipio_codigo,
                        zona_codigo=location.zona_codigo,
                        puesto_codigo=location.puesto_codigo
                    ).all()
                ]

                if mesa_ids:
                    user = User.query.filter(
                        User.rol == rol,
                        User.ubicacion_id.in_(mesa_ids),
                        User.activo == True
                    ).first()
                    logger.info(f"Usuario encontrado en mesa del puesto: {user.id if user else None}")

        if not user:
            raise AuthenticationException("Credenciales inválidas")
        
        # Verificar si está bloqueado
        if user.bloqueado_hasta and user.bloqueado_hasta > datetime.now():
            tiempo_restante = (user.bloqueado_hasta - datetime.now()).seconds // 60
            raise AccountBlockedException(
                f"Cuenta bloqueada. Intente en {tiempo_restante} minutos",
                user.bloqueado_hasta
            )
        
        # Verificar contraseña
        if not user.check_password(password):
            user.intentos_fallidos += 1
            
            if user.intentos_fallidos >= 5:
                user.bloqueado_hasta = datetime.now() + timedelta(minutes=1)
                db.session.commit()
                raise AccountBlockedException(
                    "Cuenta bloqueada por múltiples intentos fallidos. Intente en 1 minuto",
                    user.bloqueado_hasta
                )
            
            db.session.commit()
            raise AuthenticationException("Credenciales inválidas")
        
        # Reset intentos fallidos y actualizar último acceso
        user.intentos_fallidos = 0
        user.bloqueado_hasta = None
        user.ultimo_acceso = datetime.now()
        db.session.commit()
        
        # Generar tokens
        access_token, refresh_token = generate_tokens(user)
        
        return user, access_token, refresh_token
    
    @staticmethod
    def _find_location_by_hierarchy(rol, ubicacion_data):
        """
        Encontrar ubicación según jerarquía y rol
        
        Args:
            rol: Rol del usuario
            ubicacion_data: Dict con datos de ubicación
            
        Returns:
            Location o None
        """
        # Super admin, monitoreo y auditor no necesitan ubicación
        if rol in ['super_admin', 'monitoreo', 'auditor_electoral']:
            return None
        
        query = Location.query
        logger.debug(f"Buscando ubicación - rol={rol}, ubicacion_data={ubicacion_data}")
        
        # Filtrar por departamento
        if 'departamento_codigo' in ubicacion_data:
            query = query.filter_by(departamento_codigo=ubicacion_data['departamento_codigo'])
            logger.debug(f"Filtrado por departamento: {ubicacion_data['departamento_codigo']}")
        
        # Según el rol, determinar el tipo de ubicación
        if rol in ['admin_departamental', 'coordinador_departamental', 'auditor_electoral']:
            query = query.filter_by(tipo='departamento')
            result = query.first()
            logger.debug("Filtrando por tipo=departamento")

        elif rol in ['admin_municipal', 'coordinador_municipal']:
            if 'municipio_codigo' in ubicacion_data:
                query = query.filter_by(
                    tipo='municipio',
                    municipio_codigo=ubicacion_data['municipio_codigo']
                )
                logger.debug(f"Filtrando por tipo=municipio, municipio_codigo={ubicacion_data['municipio_codigo']}")
            result = query.first()

        elif rol == 'coordinador_puesto':
            if 'puesto_codigo' in ubicacion_data:
                # Construir el código completo si es necesario
                zona_cod = ubicacion_data.get('zona_codigo', '')
                puesto_cod = ubicacion_data.get('puesto_codigo', '')

                # Si puesto_codigo tiene menos de 8 caracteres, construir el completo
                if len(puesto_cod) < 8 and zona_cod:
                    # zona_codigo (6) + últimos 2 dígitos de puesto_codigo = código completo (8)
                    puesto_codigo_completo = zona_cod + puesto_cod[-2:]
                    logger.debug(
                        f"Puesto código completo construido: {puesto_cod} -> {puesto_codigo_completo}"
                    )
                else:
                    puesto_codigo_completo = puesto_cod

                filters = {
                    'tipo': 'puesto',
                    'puesto_codigo': puesto_codigo_completo
                }
                query = query.filter_by(**filters)
                logger.debug(f"Filtrando por tipo=puesto, puesto_codigo={puesto_codigo_completo}")
            result = query.first()
        
        elif rol == 'testigo_electoral':
            # Testigos se autentican a nivel de puesto
            # La mesa específica se selecciona en el dashboard
            if 'puesto_codigo' in ubicacion_data:
                # Construir el código completo si es necesario
                zona_cod = ubicacion_data.get('zona_codigo', '')
                puesto_cod = ubicacion_data.get('puesto_codigo', '')
                
                # Si puesto_codigo tiene menos de 8 caracteres, construir el completo
                if len(puesto_cod) < 8 and zona_cod:
                    # zona_codigo (6) + últimos 2 dígitos de puesto_codigo = código completo (8)
                    puesto_codigo_completo = zona_cod + puesto_cod[-2:]
                    logger.debug(
                        f"Puesto código completo construido: {puesto_cod} -> {puesto_codigo_completo}"
                    )
                else:
                    puesto_codigo_completo = puesto_cod
                
                filters = {
                    'tipo': 'puesto',
                    'puesto_codigo': puesto_codigo_completo
                }
                query = query.filter_by(**filters)
                logger.debug(f"Filtrando por tipo=puesto, puesto_codigo={puesto_codigo_completo}")
                result = query.first()
                
                # Si no encontramos el puesto directamente, intentar contra mesas dentro de ese puesto
                if not result:
                    logger.debug(
                        f"No se encontró puesto para testigo, intentando buscar mesas bajo el puesto {puesto_codigo_completo}"
                    )
                    query = Location.query.filter_by(
                        tipo='mesa',
                        departamento_codigo=ubicacion_data.get('departamento_codigo'),
                        municipio_codigo=ubicacion_data.get('municipio_codigo'),
                        zona_codigo=ubicacion_data.get('zona_codigo'),
                        puesto_codigo=puesto_codigo_completo
                    )
                    result = query.first()
                    if result:
                        logger.debug(f"Se encontró ubicación de mesa para testigo: {result.id}")
                        return result
            else:
                result = None
        else:
            result = query.first()
        logger.debug(f"Resultado de ubicación: {result.id if result else None}")
        if result:
            logger.debug(
                f"Detalles de ubicación: id={result.id}, nombre={result.nombre_completo}, tipo={result.tipo}, puesto_codigo={result.puesto_codigo}"
            )
        
        return result
    
    @staticmethod
    def change_password(user_id, current_password, new_password):
        """
        Cambiar contraseña de usuario
        
        Args:
            user_id: ID del usuario
            current_password: Contraseña actual
            new_password: Nueva contraseña
        """
        user = User.query.get(user_id)
        
        if not user:
            raise ValidationException({'user': ['Usuario no encontrado']})
        
        # ⚠️ PROTECCIÓN: Super Admin no puede cambiar su contraseña desde el código
        if user.rol == 'super_admin':
            raise ValidationException({
                'user': ['La contraseña del Super Administrador no puede ser modificada desde el sistema. Contacte al administrador del sistema.']
            })
        
        # Verificar contraseña actual
        if not user.check_password(current_password):
            raise ValidationException({'current_password': ['Contraseña actual incorrecta']})
        
        # Validar nueva contraseña
        if len(new_password) < 8:
            raise ValidationException({'new_password': ['La contraseña debe tener al menos 8 caracteres']})
        
        if not any(c.isupper() for c in new_password):
            raise ValidationException({'new_password': ['La contraseña debe contener al menos una mayúscula']})
        
        if not any(c.islower() for c in new_password):
            raise ValidationException({'new_password': ['La contraseña debe contener al menos una minúscula']})
        
        if not any(c.isdigit() for c in new_password):
            raise ValidationException({'new_password': ['La contraseña debe contener al menos un número']})
        
        # Cambiar contraseña
        user.set_password(new_password)
        db.session.commit()
