"""
Servicio para cálculos consolidados de formularios E-14
"""
from backend.database import db
from backend.models.formulario_e14 import FormularioE14, VotoPartido, VotoCandidato
from backend.models.location import Location
from backend.models.partido_politico import PartidoPolitico as Partido
from backend.models.candidato import Candidato
from sqlalchemy import func, and_


class ConsolidadoService:
    """Servicio para cálculos agregados y consolidados"""
    
    @staticmethod
    def calcular_consolidado_puesto(puesto_id, tipo_eleccion_id=None):
        """
        Calcular consolidado de votos de un puesto
        
        Args:
            puesto_id: ID del puesto
            tipo_eleccion_id: ID del tipo de elección (opcional)
            
        Returns:
            dict: Diccionario con datos consolidados del puesto
        """
        from backend.utils.exceptions import NotFoundException
        
        # Obtener el puesto
        puesto = Location.query.get(puesto_id)
        
        if not puesto or puesto.tipo != 'puesto':
            raise NotFoundException('Puesto no encontrado')
        
        # Obtener todas las mesas del puesto
        mesas = Location.query.filter_by(
            puesto_codigo=puesto.puesto_codigo,
            tipo='mesa'
        ).all()
        
        mesa_ids = [mesa.id for mesa in mesas]
        
        # Construir query base para formularios validados
        query = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids),
            FormularioE14.estado == 'validado'
        )
        
        if tipo_eleccion_id:
            query = query.filter_by(tipo_eleccion_id=tipo_eleccion_id)
        
        formularios_validados = query.all()
        
        # Calcular totales
        total_votantes_registrados = sum(f.total_votantes_registrados for f in formularios_validados)
        total_votos = sum(f.total_votos for f in formularios_validados)
        votos_validos = sum(f.votos_validos for f in formularios_validados)
        votos_nulos = sum(f.votos_nulos for f in formularios_validados)
        votos_blanco = sum(f.votos_blanco for f in formularios_validados)
        tarjetas_no_marcadas = sum(f.tarjetas_no_marcadas for f in formularios_validados)
        
        # Calcular participación
        if total_votantes_registrados > 0:
            participacion_porcentaje = (total_votos / total_votantes_registrados) * 100
        else:
            participacion_porcentaje = 0
        
        # Consolidar votos por partido
        votos_por_partido = ConsolidadoService._consolidar_votos_partido(
            [f.id for f in formularios_validados]
        )
        
        # Consolidar votos por candidato
        votos_por_candidato = ConsolidadoService._consolidar_votos_candidato(
            [f.id for f in formularios_validados]
        )
        
        # Calcular mesas validadas
        mesas_validadas = len(formularios_validados)
        total_mesas = len(mesas)
        
        return {
            'puesto': {
                'id': puesto.id,
                'codigo': puesto.puesto_codigo,
                'nombre': puesto.puesto_nombre or puesto.nombre_completo,
                'total_mesas': total_mesas,
                'mesas_validadas': mesas_validadas
            },
            'resumen': {
                'total_votantes_registrados': total_votantes_registrados,
                'total_votos': total_votos,
                'votos_validos': votos_validos,
                'votos_nulos': votos_nulos,
                'votos_blanco': votos_blanco,
                'tarjetas_no_marcadas': tarjetas_no_marcadas,
                'participacion_porcentaje': round(participacion_porcentaje, 2)
            },
            'votos_por_partido': votos_por_partido,
            'votos_por_candidato': votos_por_candidato
        }
    
    @staticmethod
    def calcular_consolidado_municipal(municipio_id, tipo_eleccion_id=None):
        """
        Calcular consolidado de votos de un municipio
        
        Args:
            municipio_id: ID del municipio
            tipo_eleccion_id: ID del tipo de elección (opcional)
            
        Returns:
            dict: Diccionario con datos consolidados del municipio
        """
        # Obtener el municipio
        municipio = Location.query.get(municipio_id)
        
        if not municipio or municipio.tipo != 'municipio':
            return None
        
        # Obtener todos los puestos del municipio
        puestos = Location.query.filter_by(
            municipio_codigo=municipio.municipio_codigo,
            tipo='puesto'
        ).all()
        
        # Obtener todas las mesas de todos los puestos
        mesa_ids = []
        for puesto in puestos:
            mesas = Location.query.filter_by(
                puesto_codigo=puesto.puesto_codigo,
                tipo='mesa'
            ).all()
            mesa_ids.extend([mesa.id for mesa in mesas])
        
        # Construir query base para formularios validados
        query = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids),
            FormularioE14.estado == 'validado'
        )
        
        if tipo_eleccion_id:
            query = query.filter_by(tipo_eleccion_id=tipo_eleccion_id)
        
        formularios_validados = query.all()
        
        # Calcular totales
        total_votantes_registrados = sum(f.total_votantes_registrados for f in formularios_validados)
        total_votos = sum(f.total_votos for f in formularios_validados)
        votos_validos = sum(f.votos_validos for f in formularios_validados)
        votos_nulos = sum(f.votos_nulos for f in formularios_validados)
        votos_blanco = sum(f.votos_blanco for f in formularios_validados)
        
        # Calcular participación
        if total_votantes_registrados > 0:
            participacion_porcentaje = (total_votos / total_votantes_registrados) * 100
        else:
            participacion_porcentaje = 0
        
        # Consolidar votos por partido
        votos_por_partido = ConsolidadoService._consolidar_votos_partido(
            [f.id for f in formularios_validados]
        )
        
        # Consolidar votos por candidato
        votos_por_candidato = ConsolidadoService._consolidar_votos_candidato(
            [f.id for f in formularios_validados]
        )
        
        return {
            'municipio': {
                'id': municipio.id,
                'codigo': municipio.municipio_codigo,
                'nombre': municipio.municipio_nombre or municipio.nombre_completo,
                'total_puestos': len(puestos),
                'total_mesas': len(mesa_ids),
                'mesas_validadas': len(formularios_validados)
            },
            'resumen': {
                'total_votantes_registrados': total_votantes_registrados,
                'total_votos': total_votos,
                'votos_validos': votos_validos,
                'votos_nulos': votos_nulos,
                'votos_blanco': votos_blanco,
                'participacion_porcentaje': round(participacion_porcentaje, 2)
            },
            'votos_por_partido': votos_por_partido,
            'votos_por_candidato': votos_por_candidato
        }
    
    @staticmethod
    def obtener_estadisticas_puesto(puesto_id):
        """
        Obtener estadísticas generales de un puesto
        
        Args:
            puesto_id: ID del puesto
            
        Returns:
            dict: Diccionario con estadísticas del puesto
        """
        # Obtener el puesto
        puesto = Location.query.get(puesto_id)
        
        if not puesto or puesto.tipo != 'puesto':
            return None
        
        # Obtener todas las mesas del puesto
        mesas = Location.query.filter_by(
            puesto_codigo=puesto.puesto_codigo,
            tipo='mesa'
        ).all()
        
        mesa_ids = [mesa.id for mesa in mesas]
        
        # Contar formularios por estado
        total_formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).count()
        
        borradores = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids),
            FormularioE14.estado == 'borrador'
        ).count()
        
        pendientes = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids),
            FormularioE14.estado == 'pendiente'
        ).count()
        
        validados = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids),
            FormularioE14.estado == 'validado'
        ).count()
        
        rechazados = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids),
            FormularioE14.estado == 'rechazado'
        ).count()
        
        # Calcular mesas reportadas (con formulario pendiente o validado)
        mesas_reportadas = db.session.query(FormularioE14.mesa_id).filter(
            FormularioE14.mesa_id.in_(mesa_ids),
            FormularioE14.estado.in_(['pendiente', 'validado'])
        ).distinct().count()
        
        # Calcular porcentaje de avance
        total_mesas = len(mesas)
        if total_mesas > 0:
            porcentaje_avance = (mesas_reportadas / total_mesas) * 100
        else:
            porcentaje_avance = 0
        
        return {
            'total_mesas': total_mesas,
            'mesas_reportadas': mesas_reportadas,
            'porcentaje_avance': round(porcentaje_avance, 2),
            'formularios': {
                'total': total_formularios,
                'borradores': borradores,
                'pendientes': pendientes,
                'validados': validados,
                'rechazados': rechazados
            }
        }
    
    @staticmethod
    def _consolidar_votos_partido(formulario_ids):
        """Consolidar votos por partido de múltiples formularios"""
        if not formulario_ids:
            return []
        
        # Agrupar y sumar votos por partido
        votos_agrupados = db.session.query(
            VotoPartido.partido_id,
            func.sum(VotoPartido.votos).label('total_votos')
        ).filter(
            VotoPartido.formulario_id.in_(formulario_ids)
        ).group_by(
            VotoPartido.partido_id
        ).all()
        
        # Calcular total de votos para porcentajes
        total_votos = sum(voto.total_votos for voto in votos_agrupados)
        
        # Construir resultado con información del partido
        resultado = []
        for voto in votos_agrupados:
            partido = Partido.query.get(voto.partido_id)
            
            if partido:
                porcentaje = (voto.total_votos / total_votos * 100) if total_votos > 0 else 0
                
                resultado.append({
                    'partido_id': partido.id,
                    'partido_nombre': partido.nombre,
                    'partido_nombre_corto': partido.nombre_corto,
                    'partido_color': partido.color,
                    'total_votos': voto.total_votos,
                    'porcentaje': round(porcentaje, 2)
                })
        
        # Ordenar por total de votos descendente
        resultado.sort(key=lambda x: x['total_votos'], reverse=True)
        
        return resultado
    
    @staticmethod
    def _consolidar_votos_candidato(formulario_ids):
        """Consolidar votos por candidato de múltiples formularios"""
        if not formulario_ids:
            return []
        
        # Agrupar y sumar votos por candidato
        votos_agrupados = db.session.query(
            VotoCandidato.candidato_id,
            func.sum(VotoCandidato.votos).label('total_votos')
        ).filter(
            VotoCandidato.formulario_id.in_(formulario_ids)
        ).group_by(
            VotoCandidato.candidato_id
        ).all()
        
        # Calcular total de votos para porcentajes
        total_votos = sum(voto.total_votos for voto in votos_agrupados)
        
        # Construir resultado con información del candidato
        resultado = []
        for voto in votos_agrupados:
            candidato = Candidato.query.get(voto.candidato_id)
            
            if candidato:
                porcentaje = (voto.total_votos / total_votos * 100) if total_votos > 0 else 0
                
                resultado.append({
                    'candidato_id': candidato.id,
                    'candidato_nombre': candidato.nombre_completo,
                    'candidato_numero_lista': candidato.numero_lista,
                    'partido_id': candidato.partido_id,
                    'partido_nombre': candidato.partido.nombre if candidato.partido else None,
                    'total_votos': voto.total_votos,
                    'porcentaje': round(porcentaje, 2)
                })
        
        # Ordenar por total de votos descendente
        resultado.sort(key=lambda x: x['total_votos'], reverse=True)
        
        return resultado
