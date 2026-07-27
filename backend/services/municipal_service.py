"""
Servicio para operaciones del coordinador municipal
"""
from backend.database import db
from backend.models.location import Location
from backend.models.user import User
from backend.models.formulario_e14 import FormularioE14
from backend.services.consolidado_service import ConsolidadoService
from sqlalchemy import func, and_
from datetime import datetime, timedelta


class MunicipalService:
    """Servicio para operaciones del coordinador municipal"""
    
    @staticmethod
    def obtener_puestos_municipio(municipio_id, filtros=None):
        """
        Obtener lista de puestos del municipio con estadísticas
        
        Args:
            municipio_id: ID del municipio
            filtros: dict con filtros opcionales (estado, zona, etc.)
            
        Returns:
            dict con puestos y estadísticas generales
        """
        # Obtener el municipio
        municipio = Location.query.get(municipio_id)
        
        if not municipio or municipio.tipo != 'municipio':
            return None
        
        # Obtener todos los puestos del municipio
        query = Location.query.filter_by(
            municipio_codigo=municipio.municipio_codigo,
            tipo='puesto'
        )
        
        # Aplicar filtros si existen
        if filtros:
            if 'zona' in filtros:
                query = query.filter_by(zona_codigo=filtros['zona'])
        
        puestos = query.all()
        
        # Calcular estadísticas para cada puesto
        puestos_data = []
        total_puestos_completos = 0
        total_puestos_incompletos = 0
        total_puestos_con_discrepancias = 0
        
        for puesto in puestos:
            # Obtener estadísticas del puesto
            stats = ConsolidadoService.obtener_estadisticas_puesto(puesto.id)
            
            if not stats:
                continue
            
            # Obtener coordinador del puesto
            coordinador = User.query.filter_by(
                ubicacion_id=puesto.id,
                rol='coordinador_puesto'
            ).first()
            
            # Determinar estado del puesto
            porcentaje_avance = stats.get('porcentaje_avance', 0)
            if porcentaje_avance >= 100:
                estado = 'completo'
                total_puestos_completos += 1
            else:
                estado = 'incompleto'
                total_puestos_incompletos += 1
            
            # Detectar discrepancias básicas
            tiene_discrepancias = False
            if stats.get('formularios', {}).get('rechazados', 0) > stats.get('formularios', {}).get('validados', 0) * 0.15:
                tiene_discrepancias = True
                total_puestos_con_discrepancias += 1
            
            # Verificar última actividad del coordinador
            ultimo_acceso = None
            if coordinador and coordinador.last_login:
                ultimo_acceso = coordinador.last_login
            
            puesto_data = {
                'id': puesto.id,
                'codigo': puesto.puesto_codigo,
                'nombre': puesto.puesto_nombre or puesto.nombre_completo,
                'total_mesas': stats.get('total_mesas', 0),
                'mesas_reportadas': stats.get('mesas_reportadas', 0),
                'mesas_validadas': stats.get('formularios', {}).get('validados', 0),
                'porcentaje_avance': porcentaje_avance,
                'coordinador': {
                    'id': coordinador.id if coordinador else None,
                    'nombre': coordinador.nombre if coordinador else 'Sin asignar',
                    'ultimo_acceso': ultimo_acceso.isoformat() if ultimo_acceso else None
                },
                'estado': estado,
                'tiene_discrepancias': tiene_discrepancias,
                'ultima_actualizacion': datetime.utcnow().isoformat()
            }
            
            puestos_data.append(puesto_data)
        
        # Aplicar filtro de estado si existe
        if filtros and 'estado' in filtros:
            if filtros['estado'] == 'completo':
                puestos_data = [p for p in puestos_data if p['estado'] == 'completo']
            elif filtros['estado'] == 'incompleto':
                puestos_data = [p for p in puestos_data if p['estado'] == 'incompleto']
            elif filtros['estado'] == 'con_discrepancias':
                puestos_data = [p for p in puestos_data if p['tiene_discrepancias']]
        
        # Calcular cobertura
        total_puestos = len(puestos)
        cobertura_porcentaje = (total_puestos_completos / total_puestos * 100) if total_puestos > 0 else 0
        
        return {
            'puestos': puestos_data,
            'estadisticas': {
                'total_puestos': total_puestos,
                'puestos_completos': total_puestos_completos,
                'puestos_incompletos': total_puestos_incompletos,
                'puestos_con_discrepancias': total_puestos_con_discrepancias,
                'cobertura_porcentaje': round(cobertura_porcentaje, 2)
            }
        }
    
    @staticmethod
    def calcular_estadisticas_puesto(puesto_id):
        """
        Calcular estadísticas detalladas de un puesto
        Reutiliza ConsolidadoService.obtener_estadisticas_puesto()
        
        Args:
            puesto_id: ID del puesto
            
        Returns:
            dict con estadísticas del puesto
        """
        return ConsolidadoService.obtener_estadisticas_puesto(puesto_id)
    
    @staticmethod
    def obtener_puesto_detallado(puesto_id, coordinador_id):
        """
        Obtener información completa de un puesto
        
        Args:
            puesto_id: ID del puesto
            coordinador_id: ID del coordinador municipal (para validar permisos)
            
        Returns:
            dict con información completa del puesto
        """
        # Obtener el puesto
        puesto = Location.query.get(puesto_id)
        
        if not puesto or puesto.tipo != 'puesto':
            return None
        
        # Validar que el coordinador tenga acceso a este puesto
        coordinador = User.query.get(coordinador_id)
        if not coordinador or not coordinador.ubicacion_id:
            return None
        
        municipio_coordinador = Location.query.get(coordinador.ubicacion_id)
        if not municipio_coordinador or municipio_coordinador.municipio_codigo != puesto.municipio_codigo:
            return None
        
        # Obtener coordinador del puesto
        coordinador_puesto = User.query.filter_by(
            ubicacion_id=puesto.id,
            rol='coordinador_puesto'
        ).first()
        
        # Obtener mesas del puesto
        mesas = Location.query.filter_by(
            puesto_codigo=puesto.puesto_codigo,
            tipo='mesa',
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo
        ).all()
        
        # Obtener formularios del puesto
        mesa_ids = [mesa.id for mesa in mesas]
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).order_by(FormularioE14.created_at.desc()).limit(50).all()
        
        # Obtener consolidado del puesto
        consolidado = ConsolidadoService.calcular_consolidado_puesto(puesto.id)
        
        # Obtener estadísticas
        estadisticas = ConsolidadoService.obtener_estadisticas_puesto(puesto.id)
        
        return {
            'puesto': {
                'id': puesto.id,
                'codigo': puesto.puesto_codigo,
                'nombre': puesto.puesto_nombre or puesto.nombre_completo,
                'total_mesas': len(mesas)
            },
            'coordinador': {
                'id': coordinador_puesto.id if coordinador_puesto else None,
                'nombre': coordinador_puesto.nombre if coordinador_puesto else 'Sin asignar',
                'ultimo_acceso': coordinador_puesto.ultimo_acceso.isoformat() if coordinador_puesto and coordinador_puesto.ultimo_acceso else None
            },
            'mesas': [
                {
                    'id': mesa.id,
                    'codigo': mesa.mesa_codigo,
                    'nombre': mesa.nombre_completo,
                    'total_votantes_registrados': mesa.total_votantes_registrados
                }
                for mesa in mesas
            ],
            'formularios': [f.to_dict() for f in formularios],
            'consolidado': consolidado,
            'estadisticas': estadisticas
        }
    
    @staticmethod
    def comparar_puestos(puesto_ids):
        """
        Comparar estadísticas entre múltiples puestos
        
        Args:
            puesto_ids: Lista de IDs de puestos a comparar
            
        Returns:
            dict con datos comparativos
        """
        if not puesto_ids or len(puesto_ids) < 2:
            return None
        
        puestos_data = []
        participaciones = []
        
        for puesto_id in puesto_ids:
            # Obtener consolidado del puesto
            consolidado = ConsolidadoService.calcular_consolidado_puesto(puesto_id)
            
            if not consolidado:
                continue
            
            puesto_info = consolidado.get('puesto', {})
            resumen = consolidado.get('resumen', {})
            votos_por_partido = consolidado.get('votos_por_partido', [])
            
            participacion = resumen.get('participacion_porcentaje', 0)
            participaciones.append(participacion)
            
            puestos_data.append({
                'puesto_id': puesto_info.get('id'),
                'puesto_nombre': puesto_info.get('nombre'),
                'puesto_codigo': puesto_info.get('codigo'),
                'total_votos': resumen.get('total_votos', 0),
                'participacion_porcentaje': participacion,
                'votos_por_partido': votos_por_partido
            })
        
        # Calcular desviación estándar de participación
        if len(participaciones) > 1:
            media = sum(participaciones) / len(participaciones)
            varianza = sum((x - media) ** 2 for x in participaciones) / len(participaciones)
            desviacion_estandar = varianza ** 0.5
        else:
            desviacion_estandar = 0
        
        # Preparar datos de votos por partido para comparación
        # Obtener todos los partidos únicos
        partidos_set = set()
        for puesto in puestos_data:
            for vp in puesto['votos_por_partido']:
                partidos_set.add(vp['partido_id'])
        
        # Crear matriz de comparación
        votos_comparacion = []
        for partido_id in partidos_set:
            partido_nombre = None
            partido_color = None
            votos_por_puesto = []
            
            for puesto in puestos_data:
                voto_partido = next((vp for vp in puesto['votos_por_partido'] if vp['partido_id'] == partido_id), None)
                if voto_partido:
                    if not partido_nombre:
                        partido_nombre = voto_partido['partido_nombre_corto']
                        partido_color = voto_partido['partido_color']
                    votos_por_puesto.append(voto_partido['total_votos'])
                else:
                    votos_por_puesto.append(0)
            
            votos_comparacion.append({
                'partido_id': partido_id,
                'partido_nombre': partido_nombre,
                'partido_color': partido_color,
                'votos_por_puesto': votos_por_puesto
            })
        
        return {
            'puestos': puestos_data,
            'comparacion': {
                'participacion': participaciones,
                'votos_por_partido': votos_comparacion,
                'desviacion_estandar': round(desviacion_estandar, 2)
            }
        }
