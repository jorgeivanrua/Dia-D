"""
Servicio para gestión de Configuración del Sistema
"""
from backend.database import db
from backend.models.configuracion_sistema import ConfiguracionSistema
from backend.models.partido_politico import PartidoPolitico
from backend.models.candidato import Candidato
from backend.models.configuracion_electoral import TipoEleccion
import json
from datetime import datetime


class ConfiguracionService:
    """Servicio para operaciones de configuración del sistema"""
    
    # Cache simple en memoria
    _cache = {}
    _cache_time = {}
    _cache_ttl = 300  # 5 minutos
    
    @staticmethod
    def obtener_configuracion(clave, default=None):
        """
        Obtener valor de configuración con cache
        
        Args:
            clave: Clave de configuración
            default: Valor por defecto si no existe
            
        Returns:
            Valor de configuración o default
        """
        # Verificar cache
        if clave in ConfiguracionService._cache:
            cache_time = ConfiguracionService._cache_time.get(clave, 0)
            if (datetime.now().timestamp() - cache_time) < ConfiguracionService._cache_ttl:
                return ConfiguracionService._cache[clave]
        
        # Obtener de base de datos
        config = ConfiguracionSistema.query.filter_by(clave=clave).first()
        valor = config.valor if config else default
        
        # Guardar en cache
        ConfiguracionService._cache[clave] = valor
        ConfiguracionService._cache_time[clave] = datetime.now().timestamp()
        
        return valor
    
    @staticmethod
    def actualizar_configuracion(clave, valor, tipo='text', descripcion=None, user_id=None):
        """
        Actualizar o crear configuración
        
        Args:
            clave: Clave de configuración
            valor: Nuevo valor
            tipo: Tipo de dato (text, integer, boolean, json)
            descripcion: Descripción de la configuración
            user_id: ID del usuario que actualiza
            
        Returns:
            tuple (config_dict, error_message)
        """
        try:
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
            
            # Invalidar cache
            if clave in ConfiguracionService._cache:
                del ConfiguracionService._cache[clave]
                del ConfiguracionService._cache_time[clave]
            
            return config.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f'Error al actualizar configuración: {str(e)}'
    
    @staticmethod
    def obtener_todas_configuraciones():
        """
        Obtener todas las configuraciones
        
        Returns:
            list: Lista de configuraciones
        """
        configs = ConfiguracionSistema.query.order_by(ConfiguracionSistema.clave).all()
        return [c.to_dict() for c in configs]
    
    @staticmethod
    def exportar_partidos():
        """
        Exportar todos los partidos políticos
        
        Returns:
            dict: Datos de partidos en formato JSON
        """
        partidos = PartidoPolitico.query.order_by(PartidoPolitico.nombre).all()
        
        return {
            'tipo': 'partidos_politicos',
            'version': '1.0',
            'fecha_exportacion': datetime.utcnow().isoformat(),
            'total': len(partidos),
            'datos': [
                {
                    'nombre': p.nombre,
                    'sigla': p.sigla,
                    'color': p.color,
                    'descripcion': p.descripcion,
                    'activo': p.activo
                }
                for p in partidos
            ]
        }
    
    @staticmethod
    def exportar_candidatos():
        """
        Exportar todos los candidatos
        
        Returns:
            dict: Datos de candidatos en formato JSON
        """
        candidatos = Candidato.query.order_by(Candidato.nombre_completo).all()
        
        return {
            'tipo': 'candidatos',
            'version': '1.0',
            'fecha_exportacion': datetime.utcnow().isoformat(),
            'total': len(candidatos),
            'datos': [
                {
                    'nombre_completo': c.nombre_completo,
                    'partido_sigla': c.partido.sigla if c.partido else None,
                    'tipo_eleccion_nombre': c.tipo_eleccion.nombre if c.tipo_eleccion else None,
                    'cargo': c.cargo,
                    'numero_lista': c.numero_lista,
                    'biografia': c.biografia,
                    'activo': c.activo
                }
                for c in candidatos
            ]
        }
    
    @staticmethod
    def exportar_tipos_eleccion():
        """
        Exportar todos los tipos de elección
        
        Returns:
            dict: Datos de tipos de elección en formato JSON
        """
        tipos = TipoEleccion.query.order_by(TipoEleccion.nombre).all()
        
        return {
            'tipo': 'tipos_eleccion',
            'version': '1.0',
            'fecha_exportacion': datetime.utcnow().isoformat(),
            'total': len(tipos),
            'datos': [
                {
                    'nombre': t.nombre,
                    'nivel': t.nivel,
                    'descripcion': t.descripcion,
                    'activo': getattr(t, 'activo', True)
                }
                for t in tipos
            ]
        }
    
    @staticmethod
    def exportar_configuracion_completa():
        """
        Exportar configuración completa del sistema
        
        Returns:
            dict: Configuración completa en formato JSON
        """
        return {
            'tipo': 'configuracion_completa',
            'version': '1.0',
            'fecha_exportacion': datetime.utcnow().isoformat(),
            'partidos': ConfiguracionService.exportar_partidos(),
            'candidatos': ConfiguracionService.exportar_candidatos(),
            'tipos_eleccion': ConfiguracionService.exportar_tipos_eleccion(),
            'configuraciones': ConfiguracionService.obtener_todas_configuraciones()
        }
    
    @staticmethod
    def importar_configuracion(data):
        """
        Importar configuración desde JSON
        
        Args:
            data: dict con datos a importar
            
        Returns:
            tuple (resumen_dict, error_message)
        """
        try:
            # Validar formato
            if not isinstance(data, dict):
                return None, 'Formato inválido: se esperaba un objeto JSON'
            
            if 'tipo' not in data:
                return None, 'Formato inválido: falta campo "tipo"'
            
            resumen = {
                'partidos_importados': 0,
                'candidatos_importados': 0,
                'tipos_importados': 0,
                'configuraciones_importadas': 0,
                'errores': []
            }
            
            tipo = data['tipo']
            
            # Importar según tipo
            if tipo == 'partidos_politicos':
                resumen['partidos_importados'] = ConfiguracionService._importar_partidos(data.get('datos', []))
            
            elif tipo == 'candidatos':
                resumen['candidatos_importados'] = ConfiguracionService._importar_candidatos(data.get('datos', []))
            
            elif tipo == 'tipos_eleccion':
                resumen['tipos_importados'] = ConfiguracionService._importar_tipos_eleccion(data.get('datos', []))
            
            elif tipo == 'configuracion_completa':
                if 'partidos' in data and 'datos' in data['partidos']:
                    resumen['partidos_importados'] = ConfiguracionService._importar_partidos(data['partidos']['datos'])
                
                if 'candidatos' in data and 'datos' in data['candidatos']:
                    resumen['candidatos_importados'] = ConfiguracionService._importar_candidatos(data['candidatos']['datos'])
                
                if 'tipos_eleccion' in data and 'datos' in data['tipos_eleccion']:
                    resumen['tipos_importados'] = ConfiguracionService._importar_tipos_eleccion(data['tipos_eleccion']['datos'])
            
            else:
                return None, f'Tipo de importación no soportado: {tipo}'
            
            return resumen, None
            
        except Exception as e:
            db.session.rollback()
            return None, f'Error al importar configuración: {str(e)}'
    
    @staticmethod
    def _importar_partidos(datos):
        """Importar partidos desde lista de datos"""
        count = 0
        for item in datos:
            # Verificar si ya existe
            existe = PartidoPolitico.query.filter_by(sigla=item['sigla']).first()
            if not existe:
                partido = PartidoPolitico(
                    nombre=item['nombre'],
                    sigla=item['sigla'],
                    color=item.get('color', '#000000'),
                    descripcion=item.get('descripcion'),
                    activo=item.get('activo', True)
                )
                db.session.add(partido)
                count += 1
        
        db.session.commit()
        return count
    
    @staticmethod
    def _importar_candidatos(datos):
        """Importar candidatos desde lista de datos"""
        count = 0
        for item in datos:
            # Buscar partido y tipo de elección
            partido = PartidoPolitico.query.filter_by(sigla=item['partido_sigla']).first()
            tipo_eleccion = TipoEleccion.query.filter_by(nombre=item['tipo_eleccion_nombre']).first()
            
            if partido and tipo_eleccion:
                candidato = Candidato(
                    nombre_completo=item['nombre_completo'],
                    partido_id=partido.id,
                    tipo_eleccion_id=tipo_eleccion.id,
                    cargo=item['cargo'],
                    numero_lista=item.get('numero_lista'),
                    biografia=item.get('biografia'),
                    activo=item.get('activo', True)
                )
                db.session.add(candidato)
                count += 1
        
        db.session.commit()
        return count
    
    @staticmethod
    def _importar_tipos_eleccion(datos):
        """Importar tipos de elección desde lista de datos"""
        count = 0
        for item in datos:
            # Verificar si ya existe
            existe = TipoEleccion.query.filter_by(nombre=item['nombre']).first()
            if not existe:
                tipo = TipoEleccion(
                    nombre=item['nombre'],
                    nivel=item.get('nivel', 'nacional'),
                    descripcion=item.get('descripcion')
                )
                db.session.add(tipo)
                count += 1
        
        db.session.commit()
        return count
