"""
Servicio para operaciones del coordinador departamental
Basado en MunicipalService pero operando a nivel departamental
"""
from backend.database import db
from backend.models.location import Location
from backend.models.user import User
from backend.models.coordinador_municipal import FormularioE24Municipal
from backend.services.consolidado_service import ConsolidadoService
from backend.services.municipal_service import MunicipalService
from sqlalchemy import func, and_
from datetime import datetime, timedelta


class DepartamentalService:
    """Servicio para operaciones del coordinador departamental"""
    
    @staticmethod
    def obtener_municipios_departamento(departamento_id, filtros=None):
        """
        Obtener lista de municipios del departamento con estadísticas
        Similar a MunicipalService.obtener_puestos_municipio() pero para municipios
        
        Args:
            departamento_id: ID del departamento
            filtros: dict con filtros opcionales (estado, etc.)
            
        Returns:
            dict con municipios y estadísticas generales
        """
        # Obtener el departamento
        departamento = Location.query.get(departamento_id)
        
        if not departamento or departamento.tipo != 'departamento':
            return None
        
        # Obtener todos los municipios del departamento
        municipios = Location.query.filter_by(
            departamento_codigo=departamento.departamento_codigo,
            tipo='municipio'
        ).all()
        
        # Calcular estadísticas para cada municipio
        municipios_data = []
        total_municipios_completos = 0
        total_municipios_incompletos = 0
        total_municipios_con_discrepancias = 0
        
        for municipio in municipios:
            # Obtener estadísticas del municipio usando MunicipalService
            stats_municipio = MunicipalService.obtener_puestos_municipio(municipio.id)
            
            if not stats_municipio:
                continue
            
            stats = stats_municipio.get('estadisticas', {})
            
            # Obtener coordinador del municipio
            coordinador = User.query.filter_by(
                ubicacion_id=municipio.id,
                rol='coordinador_municipal'
            ).first()
            
            # Determinar estado del municipio
            cobertura = stats.get('cobertura_porcentaje', 0)
            if cobertura >= 90:
                estado = 'completo'
                total_municipios_completos += 1
            else:
                estado = 'incompleto'
                total_municipios_incompletos += 1
            
            # Detectar discrepancias básicas
            tiene_discrepancias = stats.get('puestos_con_discrepancias', 0) > 0
            if tiene_discrepancias:
                total_municipios_con_discrepancias += 1
            
            # Verificar última actividad del coordinador
            ultimo_acceso = None
            if coordinador and coordinador.last_login:
                ultimo_acceso = coordinador.last_login
            
            municipio_data = {
                'id': municipio.id,
                'codigo': municipio.municipio_codigo,
                'nombre': municipio.municipio_nombre or municipio.nombre_completo,
                'total_puestos': stats.get('total_puestos', 0),
                'puestos_completos': stats.get('puestos_completos', 0),
                'puestos_incompletos': stats.get('puestos_incompletos', 0),
                'porcentaje_avance': cobertura,
                'coordinador': {
                    'id': coordinador.id if coordinador else None,
                    'nombre': coordinador.nombre if coordinador else 'Sin asignar',
                    'ultimo_acceso': ultimo_acceso.isoformat() if ultimo_acceso else None
                },
                'estado': estado,
                'tiene_discrepancias': tiene_discrepancias,
                'ultima_actualizacion': datetime.utcnow().isoformat()
            }
            
            municipios_data.append(municipio_data)
        
        # Aplicar filtro de estado si existe
        if filtros and 'estado' in filtros:
            if filtros['estado'] == 'completo':
                municipios_data = [m for m in municipios_data if m['estado'] == 'completo']
            elif filtros['estado'] == 'incompleto':
                municipios_data = [m for m in municipios_data if m['estado'] == 'incompleto']
            elif filtros['estado'] == 'con_discrepancias':
                municipios_data = [m for m in municipios_data if m['tiene_discrepancias']]
        
        # Calcular cobertura departamental
        total_municipios = len(municipios)
        cobertura_departamental = (total_municipios_completos / total_municipios * 100) if total_municipios > 0 else 0
        
        return {
            'municipios': municipios_data,
            'estadisticas': {
                'total_municipios': total_municipios,
                'municipios_completos': total_municipios_completos,
                'municipios_incompletos': total_municipios_incompletos,
                'municipios_con_discrepancias': total_municipios_con_discrepancias,
                'cobertura_porcentaje': round(cobertura_departamental, 2)
            }
        }
    
    @staticmethod
    def calcular_consolidado_departamental(departamento_id, tipo_eleccion_id=None):
        """
        Calcular consolidado departamental sumando todos los municipios
        
        Args:
            departamento_id: ID del departamento
            tipo_eleccion_id: ID del tipo de elección (opcional)
            
        Returns:
            dict con consolidado departamental
        """
        # Obtener el departamento
        departamento = Location.query.get(departamento_id)
        
        if not departamento or departamento.tipo != 'departamento':
            return None
        
        # Obtener todos los municipios del departamento
        municipios = Location.query.filter_by(
            departamento_codigo=departamento.departamento_codigo,
            tipo='municipio'
        ).all()
        
        # Inicializar totales
        total_votantes_registrados = 0
        total_votos = 0
        votos_validos = 0
        votos_nulos = 0
        votos_blanco = 0
        votos_por_partido_dept = {}
        total_puestos = 0
        total_mesas = 0
        
        for municipio in municipios:
            # Obtener consolidado del municipio
            consolidado_municipal = ConsolidadoService.calcular_consolidado_municipal(
                municipio.id, 
                tipo_eleccion_id
            )
            
            if consolidado_municipal:
                resumen = consolidado_municipal.get('resumen', {})
                municipio_info = consolidado_municipal.get('municipio', {})
                
                # Sumar totales
                total_votantes_registrados += resumen.get('total_votantes_registrados', 0)
                total_votos += resumen.get('total_votos', 0)
                votos_validos += resumen.get('votos_validos', 0)
                votos_nulos += resumen.get('votos_nulos', 0)
                votos_blanco += resumen.get('votos_blanco', 0)
                total_puestos += municipio_info.get('total_puestos', 0)
                total_mesas += municipio_info.get('total_mesas', 0)
                
                # Sumar votos por partido
                for vp in consolidado_municipal.get('votos_por_partido', []):
                    partido_id = vp['partido_id']
                    if partido_id not in votos_por_partido_dept:
                        votos_por_partido_dept[partido_id] = {
                            'partido_id': partido_id,
                            'partido_nombre': vp['partido_nombre'],
                            'partido_nombre_corto': vp['partido_nombre_corto'],
                            'partido_color': vp['partido_color'],
                            'total_votos': 0
                        }
                    votos_por_partido_dept[partido_id]['total_votos'] += vp['total_votos']
        
        # Calcular porcentajes
        votos_por_partido_lista = list(votos_por_partido_dept.values())
        for vp in votos_por_partido_lista:
            vp['porcentaje'] = (vp['total_votos'] / votos_validos * 100) if votos_validos > 0 else 0
        
        # Ordenar por votos
        votos_por_partido_lista.sort(key=lambda x: x['total_votos'], reverse=True)
        
        # Calcular participación
        participacion_porcentaje = (total_votos / total_votantes_registrados * 100) if total_votantes_registrados > 0 else 0
        
        return {
            'departamento': {
                'id': departamento.id,
                'codigo': departamento.departamento_codigo,
                'nombre': departamento.departamento_nombre or departamento.nombre_completo,
                'total_municipios': len(municipios),
                'total_puestos': total_puestos,
                'total_mesas': total_mesas
            },
            'resumen': {
                'total_votantes_registrados': total_votantes_registrados,
                'total_votos': total_votos,
                'votos_validos': votos_validos,
                'votos_nulos': votos_nulos,
                'votos_blanco': votos_blanco,
                'participacion_porcentaje': round(participacion_porcentaje, 2)
            },
            'votos_por_partido': votos_por_partido_lista
        }
    
    @staticmethod
    def obtener_municipio_detallado(municipio_id, coordinador_id):
        """
        Obtener información completa de un municipio
        
        Args:
            municipio_id: ID del municipio
            coordinador_id: ID del coordinador departamental (para validar permisos)
            
        Returns:
            dict con información completa del municipio
        """
        # Reutilizar la lógica del MunicipalService pero validando permisos departamentales
        coordinador = User.query.get(coordinador_id)
        if not coordinador or not coordinador.ubicacion_id:
            return None
        
        departamento_coordinador = Location.query.get(coordinador.ubicacion_id)
        municipio = Location.query.get(municipio_id)
        
        if not municipio or not departamento_coordinador:
            return None
        
        # Validar que el municipio pertenezca al departamento del coordinador
        if municipio.departamento_codigo != departamento_coordinador.departamento_codigo:
            return None
        
        # Obtener datos del municipio usando MunicipalService
        datos_municipio = MunicipalService.obtener_puestos_municipio(municipio_id)
        consolidado_municipal = ConsolidadoService.calcular_consolidado_municipal(municipio_id)
        
        # Obtener coordinador municipal
        coordinador_municipal = User.query.filter_by(
            ubicacion_id=municipio_id,
            rol='coordinador_municipal'
        ).first()
        
        return {
            'municipio': {
                'id': municipio.id,
                'codigo': municipio.municipio_codigo,
                'nombre': municipio.municipio_nombre or municipio.nombre_completo
            },
            'coordinador': {
                'id': coordinador_municipal.id if coordinador_municipal else None,
                'nombre': coordinador_municipal.nombre if coordinador_municipal else 'Sin asignar',
                'ultimo_acceso': coordinador_municipal.ultimo_acceso.isoformat() if coordinador_municipal and coordinador_municipal.ultimo_acceso else None
            },
            'puestos': datos_municipio.get('puestos', []) if datos_municipio else [],
            'estadisticas': datos_municipio.get('estadisticas', {}) if datos_municipio else {},
            'consolidado': consolidado_municipal
        }
    
    @staticmethod
    def comparar_municipios(municipio_ids):
        """
        Comparar estadísticas entre múltiples municipios
        Similar a MunicipalService.comparar_puestos() pero para municipios
        
        Args:
            municipio_ids: Lista de IDs de municipios a comparar
            
        Returns:
            dict con datos comparativos
        """
        if not municipio_ids or len(municipio_ids) < 2:
            return None
        
        municipios_data = []
        participaciones = []
        
        for municipio_id in municipio_ids:
            # Obtener consolidado del municipio
            consolidado = ConsolidadoService.calcular_consolidado_municipal(municipio_id)
            
            if not consolidado:
                continue
            
            municipio_info = consolidado.get('municipio', {})
            resumen = consolidado.get('resumen', {})
            votos_por_partido = consolidado.get('votos_por_partido', [])
            
            participacion = resumen.get('participacion_porcentaje', 0)
            participaciones.append(participacion)
            
            municipios_data.append({
                'municipio_id': municipio_info.get('id'),
                'municipio_nombre': municipio_info.get('nombre'),
                'municipio_codigo': municipio_info.get('codigo'),
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
        partidos_set = set()
        for municipio in municipios_data:
            for vp in municipio['votos_por_partido']:
                partidos_set.add(vp['partido_id'])
        
        # Crear matriz de comparación
        votos_comparacion = []
        for partido_id in partidos_set:
            partido_nombre = None
            partido_color = None
            votos_por_municipio = []
            
            for municipio in municipios_data:
                voto_partido = next((vp for vp in municipio['votos_por_partido'] if vp['partido_id'] == partido_id), None)
                if voto_partido:
                    if not partido_nombre:
                        partido_nombre = voto_partido['partido_nombre_corto']
                        partido_color = voto_partido['partido_color']
                    votos_por_municipio.append(voto_partido['total_votos'])
                else:
                    votos_por_municipio.append(0)
            
            votos_comparacion.append({
                'partido_id': partido_id,
                'partido_nombre': partido_nombre,
                'partido_color': partido_color,
                'votos_por_municipio': votos_por_municipio
            })
        
        return {
            'municipios': municipios_data,
            'comparacion': {
                'participacion': participaciones,
                'votos_por_partido': votos_comparacion,
                'desviacion_estandar': round(desviacion_estandar, 2)
            }
        }
