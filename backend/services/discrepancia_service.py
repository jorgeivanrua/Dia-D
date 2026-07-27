"""
Servicio para detección de anomalías y discrepancias
"""
from backend.database import db
from backend.models.location import Location
from backend.models.user import User
from backend.models.formulario_e14 import FormularioE14
from backend.services.consolidado_service import ConsolidadoService
from datetime import datetime, timedelta
from sqlalchemy import func


class DiscrepanciaService:
    """Servicio para detección de anomalías y discrepancias"""
    
    # Umbrales para detección
    PARTICIPACION_ALTA = 95.0  # %
    PARTICIPACION_BAJA = 30.0  # %
    TASA_RECHAZO_ALTA = 15.0  # %
    TIEMPO_INACTIVIDAD = 2  # horas
    
    @staticmethod
    def detectar_discrepancias_puesto(puesto_id):
        """
        Detectar discrepancias en un puesto
        
        Tipos de discrepancias:
        - Participación anormal (>95% o <30%)
        - Suma de votos no coincide
        - Coordinador inactivo (>2 horas sin acceso)
        - Alta tasa de rechazo (>15%)
        
        Args:
            puesto_id: ID del puesto
            
        Returns:
            list de discrepancias con severidad
        """
        discrepancias = []
        
        # Obtener el puesto
        puesto = Location.query.get(puesto_id)
        if not puesto or puesto.tipo != 'puesto':
            return discrepancias
        
        # Obtener consolidado del puesto
        consolidado = ConsolidadoService.calcular_consolidado_puesto(puesto_id)
        if not consolidado:
            return discrepancias
        
        resumen = consolidado.get('resumen', {})
        participacion = resumen.get('participacion_porcentaje', 0)
        
        # 1. Detectar participación anormalmente alta
        if participacion > DiscrepanciaService.PARTICIPACION_ALTA:
            severidad = DiscrepanciaService.calcular_severidad(
                'participacion_alta',
                {'participacion': participacion}
            )
            discrepancias.append({
                'puesto_id': puesto_id,
                'puesto_nombre': puesto.puesto_nombre or puesto.nombre_completo,
                'tipo_discrepancia': 'participacion_alta',
                'severidad': severidad,
                'descripcion': f'Participación anormalmente alta: {participacion:.2f}%',
                'valor_esperado': f'< {DiscrepanciaService.PARTICIPACION_ALTA}%',
                'valor_actual': f'{participacion:.2f}%'
            })
        
        # 2. Detectar participación anormalmente baja
        if participacion < DiscrepanciaService.PARTICIPACION_BAJA and participacion > 0:
            severidad = DiscrepanciaService.calcular_severidad(
                'participacion_baja',
                {'participacion': participacion}
            )
            discrepancias.append({
                'puesto_id': puesto_id,
                'puesto_nombre': puesto.puesto_nombre or puesto.nombre_completo,
                'tipo_discrepancia': 'participacion_baja',
                'severidad': severidad,
                'descripcion': f'Participación anormalmente baja: {participacion:.2f}%',
                'valor_esperado': f'> {DiscrepanciaService.PARTICIPACION_BAJA}%',
                'valor_actual': f'{participacion:.2f}%'
            })
        
        # 3. Verificar coherencia de votos
        total_votos = resumen.get('total_votos', 0)
        votos_validos = resumen.get('votos_validos', 0)
        votos_nulos = resumen.get('votos_nulos', 0)
        votos_blanco = resumen.get('votos_blanco', 0)
        
        suma_votos = votos_validos + votos_nulos + votos_blanco
        if abs(suma_votos - total_votos) > 0:
            severidad = 'critica'
            discrepancias.append({
                'puesto_id': puesto_id,
                'puesto_nombre': puesto.puesto_nombre or puesto.nombre_completo,
                'tipo_discrepancia': 'suma_votos_incorrecta',
                'severidad': severidad,
                'descripcion': f'La suma de votos válidos + nulos + blanco ({suma_votos}) no coincide con el total de votos ({total_votos})',
                'valor_esperado': total_votos,
                'valor_actual': suma_votos
            })
        
        # 4. Verificar suma de votos por partido
        votos_por_partido = consolidado.get('votos_por_partido', [])
        suma_votos_partidos = sum(vp['total_votos'] for vp in votos_por_partido)
        if abs(suma_votos_partidos - votos_validos) > 0:
            severidad = 'alta'
            discrepancias.append({
                'puesto_id': puesto_id,
                'puesto_nombre': puesto.puesto_nombre or puesto.nombre_completo,
                'tipo_discrepancia': 'suma_partidos_incorrecta',
                'severidad': severidad,
                'descripcion': f'La suma de votos por partido ({suma_votos_partidos}) no coincide con votos válidos ({votos_validos})',
                'valor_esperado': votos_validos,
                'valor_actual': suma_votos_partidos
            })
        
        # 5. Verificar actividad del coordinador
        coordinador = User.query.filter_by(
            ubicacion_id=puesto_id,
            rol='coordinador_puesto'
        ).first()
        
        if coordinador:
            if coordinador.last_login:
                tiempo_inactivo = datetime.utcnow() - coordinador.last_login
                horas_inactivo = tiempo_inactivo.total_seconds() / 3600
                
                if horas_inactivo > DiscrepanciaService.TIEMPO_INACTIVIDAD:
                    severidad = DiscrepanciaService.calcular_severidad(
                        'coordinador_inactivo',
                        {'horas_inactivo': horas_inactivo}
                    )
                    discrepancias.append({
                        'puesto_id': puesto_id,
                        'puesto_nombre': puesto.puesto_nombre or puesto.nombre_completo,
                        'tipo_discrepancia': 'coordinador_inactivo',
                        'severidad': severidad,
                        'descripcion': f'Coordinador sin acceso por {horas_inactivo:.1f} horas',
                        'valor_esperado': f'< {DiscrepanciaService.TIEMPO_INACTIVIDAD} horas',
                        'valor_actual': f'{horas_inactivo:.1f} horas'
                    })
        else:
            # No hay coordinador asignado
            discrepancias.append({
                'puesto_id': puesto_id,
                'puesto_nombre': puesto.puesto_nombre or puesto.nombre_completo,
                'tipo_discrepancia': 'sin_coordinador',
                'severidad': 'critica',
                'descripcion': 'Puesto sin coordinador asignado',
                'valor_esperado': 'Coordinador asignado',
                'valor_actual': 'Sin coordinador'
            })
        
        # 6. Verificar tasa de rechazo
        estadisticas = ConsolidadoService.obtener_estadisticas_puesto(puesto_id)
        if estadisticas:
            formularios = estadisticas.get('formularios', {})
            total_formularios = formularios.get('total', 0)
            rechazados = formularios.get('rechazados', 0)
            
            if total_formularios > 0:
                tasa_rechazo = (rechazados / total_formularios) * 100
                
                if tasa_rechazo > DiscrepanciaService.TASA_RECHAZO_ALTA:
                    severidad = DiscrepanciaService.calcular_severidad(
                        'tasa_rechazo_alta',
                        {'tasa_rechazo': tasa_rechazo}
                    )
                    discrepancias.append({
                        'puesto_id': puesto_id,
                        'puesto_nombre': puesto.puesto_nombre or puesto.nombre_completo,
                        'tipo_discrepancia': 'tasa_rechazo_alta',
                        'severidad': severidad,
                        'descripcion': f'Alta tasa de rechazo de formularios: {tasa_rechazo:.1f}%',
                        'valor_esperado': f'< {DiscrepanciaService.TASA_RECHAZO_ALTA}%',
                        'valor_actual': f'{tasa_rechazo:.1f}%'
                    })
        
        return discrepancias
    
    @staticmethod
    def detectar_discrepancias_municipio(municipio_id):
        """
        Detectar discrepancias a nivel municipal
        Agrega discrepancias de todos los puestos
        
        Args:
            municipio_id: ID del municipio
            
        Returns:
            list de todas las discrepancias del municipio
        """
        # Obtener el municipio
        municipio = Location.query.get(municipio_id)
        if not municipio or municipio.tipo != 'municipio':
            return []
        
        # Obtener todos los puestos del municipio
        puestos = Location.query.filter_by(
            municipio_codigo=municipio.municipio_codigo,
            tipo='puesto'
        ).all()
        
        # Detectar discrepancias en cada puesto
        todas_discrepancias = []
        for puesto in puestos:
            discrepancias_puesto = DiscrepanciaService.detectar_discrepancias_puesto(puesto.id)
            todas_discrepancias.extend(discrepancias_puesto)
        
        # Ordenar por severidad (crítica > alta > media > baja)
        orden_severidad = {'critica': 0, 'alta': 1, 'media': 2, 'baja': 3}
        todas_discrepancias.sort(key=lambda x: orden_severidad.get(x['severidad'], 4))
        
        return todas_discrepancias
    
    @staticmethod
    def calcular_severidad(tipo_discrepancia, valores):
        """
        Calcular nivel de severidad de una discrepancia
        
        Args:
            tipo_discrepancia: Tipo de discrepancia
            valores: dict con valores relevantes
            
        Returns:
            str: 'baja', 'media', 'alta', 'critica'
        """
        if tipo_discrepancia == 'participacion_alta':
            participacion = valores.get('participacion', 0)
            if participacion > 98:
                return 'critica'
            elif participacion > 97:
                return 'alta'
            elif participacion > 96:
                return 'media'
            else:
                return 'baja'
        
        elif tipo_discrepancia == 'participacion_baja':
            participacion = valores.get('participacion', 0)
            if participacion < 10:
                return 'critica'
            elif participacion < 15:
                return 'alta'
            elif participacion < 20:
                return 'media'
            else:
                return 'baja'
        
        elif tipo_discrepancia == 'coordinador_inactivo':
            horas_inactivo = valores.get('horas_inactivo', 0)
            if horas_inactivo > 6:
                return 'critica'
            elif horas_inactivo > 4:
                return 'alta'
            elif horas_inactivo > 3:
                return 'media'
            else:
                return 'baja'
        
        elif tipo_discrepancia == 'tasa_rechazo_alta':
            tasa_rechazo = valores.get('tasa_rechazo', 0)
            if tasa_rechazo > 30:
                return 'critica'
            elif tasa_rechazo > 25:
                return 'alta'
            elif tasa_rechazo > 20:
                return 'media'
            else:
                return 'baja'
        
        elif tipo_discrepancia in ['suma_votos_incorrecta', 'sin_coordinador']:
            return 'critica'
        
        elif tipo_discrepancia == 'suma_partidos_incorrecta':
            return 'alta'
        
        else:
            return 'media'
