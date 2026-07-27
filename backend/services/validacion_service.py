"""
Servicio para validación de formularios E-14
"""
from backend.database import db
from backend.models.formulario_e14 import FormularioE14, VotoPartido, VotoCandidato, HistorialFormulario
from backend.utils.exceptions import ValidationException, NotFoundException, AuthorizationException
from datetime import datetime


class ValidacionService:
    """Servicio para validación y rechazo de formularios E-14"""
    
    @staticmethod
    def validar_formulario(formulario_id, coordinador_id, cambios=None, comentario=None):
        """
        Validar un formulario E-14
        
        Args:
            formulario_id: ID del formulario
            coordinador_id: ID del coordinador que valida
            cambios: Diccionario opcional con cambios a aplicar antes de validar
            comentario: Comentario opcional del coordinador
            
        Returns:
            FormularioE14: Formulario validado
        """
        formulario = FormularioE14.query.get(formulario_id)
        
        if not formulario:
            raise NotFoundException('Formulario no encontrado')
        
        # Verificar que el formulario esté en estado pendiente
        if formulario.estado != 'pendiente':
            raise ValidationException({
                'estado': [f'Solo se pueden validar formularios en estado pendiente. Estado actual: {formulario.estado}']
            })
        
        # Verificar que el coordinador tenga acceso a este puesto
        ValidacionService._verificar_acceso_coordinador(formulario, coordinador_id)
        
        # Verificar que no exista otro formulario validado para la misma mesa
        formulario_existente = FormularioE14.query.filter(
            FormularioE14.mesa_id == formulario.mesa_id,
            FormularioE14.estado == 'validado',
            FormularioE14.id != formulario_id
        ).first()
        
        if formulario_existente:
            raise ValidationException({
                'mesa_id': ['Ya existe un formulario validado para esta mesa']
            })
        
        # Aplicar cambios si se proporcionan
        cambios_realizados = {}
        if cambios:
            cambios_realizados = ValidacionService._aplicar_cambios(formulario, cambios)
        
        # Validar coherencia de datos
        validaciones = ValidacionService.validar_coherencia(formulario)
        
        # Alertar si hay discrepancias significativas (> 5%)
        if validaciones['discrepancia_porcentaje'] > 5:
            # Registrar alerta pero permitir validación
            cambios_realizados['alerta_discrepancia'] = {
                'porcentaje': validaciones['discrepancia_porcentaje'],
                'mensaje': 'Discrepancia significativa entre votantes registrados y votos emitidos'
            }
        
        # Cambiar estado a validado
        estado_anterior = formulario.estado
        formulario.estado = 'validado'
        formulario.validado_por_id = coordinador_id
        formulario.validado_at = datetime.utcnow()
        formulario.updated_at = datetime.utcnow()
        
        # Registrar en historial
        historial = HistorialFormulario(
            formulario_id=formulario_id,
            usuario_id=coordinador_id,
            accion='validado',
            estado_anterior=estado_anterior,
            estado_nuevo='validado',
            cambios=cambios_realizados if cambios_realizados else None,
            comentario=comentario or 'Formulario validado por coordinador'
        )
        db.session.add(historial)
        
        db.session.commit()
        
        return formulario
    
    @staticmethod
    def rechazar_formulario(formulario_id, coordinador_id, motivo):
        """
        Rechazar un formulario E-14
        
        Args:
            formulario_id: ID del formulario
            coordinador_id: ID del coordinador que rechaza
            motivo: Motivo del rechazo (obligatorio)
            
        Returns:
            FormularioE14: Formulario rechazado
        """
        if not motivo or not motivo.strip():
            raise ValidationException({'motivo': ['El motivo de rechazo es obligatorio']})
        
        formulario = FormularioE14.query.get(formulario_id)
        
        if not formulario:
            raise NotFoundException('Formulario no encontrado')
        
        # Verificar que el formulario esté en estado pendiente
        if formulario.estado != 'pendiente':
            raise ValidationException({
                'estado': [f'Solo se pueden rechazar formularios en estado pendiente. Estado actual: {formulario.estado}']
            })
        
        # Verificar que el coordinador tenga acceso a este puesto
        ValidacionService._verificar_acceso_coordinador(formulario, coordinador_id)
        
        # Cambiar estado a rechazado
        estado_anterior = formulario.estado
        formulario.estado = 'rechazado'
        formulario.motivo_rechazo = motivo.strip()
        formulario.updated_at = datetime.utcnow()
        
        # Registrar en historial
        historial = HistorialFormulario(
            formulario_id=formulario_id,
            usuario_id=coordinador_id,
            accion='rechazado',
            estado_anterior=estado_anterior,
            estado_nuevo='rechazado',
            comentario=f'Formulario rechazado. Motivo: {motivo}'
        )
        db.session.add(historial)
        
        db.session.commit()
        
        # TODO: Enviar notificación al testigo
        
        return formulario
    
    @staticmethod
    def validar_coherencia(formulario):
        """
        Validar coherencia de datos del formulario
        
        Args:
            formulario: Instancia de FormularioE14
            
        Returns:
            dict: Diccionario con resultados de validación
        """
        # Calcular suma de votos por partido
        suma_votos_partidos = sum(vp.votos for vp in formulario.votos_partidos)
        
        # Calcular suma de votos por candidato
        suma_votos_candidatos = sum(vc.votos for vc in formulario.votos_candidatos)
        
        # Total de votos (partidos + candidatos)
        total_votos_calculado = suma_votos_partidos + suma_votos_candidatos
        
        # Verificar coherencia
        coincide_votos_validos = total_votos_calculado == formulario.votos_validos
        
        total_votos_verificado = (formulario.votos_validos + formulario.votos_nulos + 
                                 formulario.votos_blanco)
        coincide_total_votos = total_votos_verificado == formulario.total_votos
        
        total_tarjetas_verificado = formulario.total_votos + formulario.tarjetas_no_marcadas
        coincide_total_tarjetas = total_tarjetas_verificado == formulario.total_tarjetas
        
        # Calcular discrepancia porcentual
        if formulario.total_votantes_registrados > 0:
            discrepancia_porcentaje = abs(
                (formulario.total_votos - formulario.total_votantes_registrados) / 
                formulario.total_votantes_registrados * 100
            )
        else:
            discrepancia_porcentaje = 0
        
        # Calcular participación
        if formulario.total_votantes_registrados > 0:
            participacion = (formulario.total_votos / formulario.total_votantes_registrados) * 100
        else:
            participacion = 0
        
        # Identificar errores
        errores = []
        if not coincide_votos_validos:
            errores.append(f'La suma de votos por partido/candidato ({total_votos_calculado}) no coincide con votos válidos ({formulario.votos_validos})')
        
        if not coincide_total_votos:
            errores.append(f'La suma de votos válidos + nulos + blanco ({total_votos_verificado}) no coincide con total de votos ({formulario.total_votos})')
        
        if not coincide_total_tarjetas:
            errores.append(f'La suma de total votos + tarjetas no marcadas ({total_tarjetas_verificado}) no coincide con total de tarjetas ({formulario.total_tarjetas})')
        
        # Identificar alertas
        alertas = []
        if participacion > 95:
            alertas.append(f'Participación muy alta: {participacion:.2f}%')
        elif participacion < 30:
            alertas.append(f'Participación muy baja: {participacion:.2f}%')
        
        if discrepancia_porcentaje > 5:
            alertas.append(f'Discrepancia significativa: {discrepancia_porcentaje:.2f}%')
        
        return {
            'suma_votos_partidos': suma_votos_partidos,
            'suma_votos_candidatos': suma_votos_candidatos,
            'total_votos_calculado': total_votos_calculado,
            'coincide_votos_validos': coincide_votos_validos,
            'coincide_total_votos': coincide_total_votos,
            'coincide_total_tarjetas': coincide_total_tarjetas,
            'discrepancia_porcentaje': round(discrepancia_porcentaje, 2),
            'participacion': round(participacion, 2),
            'errores': errores,
            'alertas': alertas,
            'es_valido': len(errores) == 0
        }
    
    @staticmethod
    def calcular_discrepancias(formulario):
        """
        Calcular discrepancias del formulario
        
        Args:
            formulario: Instancia de FormularioE14
            
        Returns:
            dict: Diccionario con discrepancias encontradas
        """
        validaciones = ValidacionService.validar_coherencia(formulario)
        
        discrepancias = {
            'tiene_discrepancias': len(validaciones['errores']) > 0 or len(validaciones['alertas']) > 0,
            'errores': validaciones['errores'],
            'alertas': validaciones['alertas'],
            'nivel_severidad': 'ninguno'
        }
        
        # Determinar nivel de severidad
        if len(validaciones['errores']) > 0:
            discrepancias['nivel_severidad'] = 'critico'
        elif validaciones['discrepancia_porcentaje'] > 10:
            discrepancias['nivel_severidad'] = 'alto'
        elif validaciones['discrepancia_porcentaje'] > 5 or len(validaciones['alertas']) > 0:
            discrepancias['nivel_severidad'] = 'medio'
        elif validaciones['discrepancia_porcentaje'] > 2:
            discrepancias['nivel_severidad'] = 'bajo'
        
        return discrepancias
    
    @staticmethod
    def _verificar_acceso_coordinador(formulario, coordinador_id):
        """Verificar que el coordinador tenga acceso al puesto del formulario"""
        from backend.models.user import User
        
        coordinador = User.query.get(coordinador_id)
        
        if not coordinador:
            raise NotFoundException('Coordinador no encontrado')
        
        if coordinador.rol != 'coordinador_puesto':
            raise AuthorizationException('Solo coordinadores de puesto pueden validar formularios')
        
        # Verificar que el coordinador esté asignado al puesto de la mesa
        if not coordinador.ubicacion_id:
            raise AuthorizationException('Coordinador sin ubicación asignada')
        
        # Obtener el puesto del coordinador
        from backend.models.location import Location
        ubicacion_coordinador = Location.query.get(coordinador.ubicacion_id)
        
        if not ubicacion_coordinador or ubicacion_coordinador.tipo != 'puesto':
            raise AuthorizationException('Coordinador no asignado a un puesto válido')
        
        # Verificar que la mesa pertenezca al puesto del coordinador
        if formulario.mesa.puesto_codigo != ubicacion_coordinador.puesto_codigo:
            raise AuthorizationException('No tiene permisos para validar formularios de este puesto')
    
    @staticmethod
    def _aplicar_cambios(formulario, cambios):
        """Aplicar cambios al formulario antes de validar"""
        cambios_realizados = {}
        
        # Campos que se pueden modificar
        campos_editables = [
            'votos_nulos', 'votos_blanco', 'tarjetas_no_marcadas',
            'total_votos', 'votos_validos', 'total_tarjetas'
        ]
        
        for campo in campos_editables:
            if campo in cambios:
                valor_anterior = getattr(formulario, campo)
                valor_nuevo = cambios[campo]
                
                if valor_anterior != valor_nuevo:
                    cambios_realizados[campo] = {
                        'anterior': valor_anterior,
                        'nuevo': valor_nuevo
                    }
                    setattr(formulario, campo, valor_nuevo)
        
        # Actualizar votos por partido si se proporcionan
        if 'votos_partidos' in cambios:
            # Eliminar votos existentes
            VotoPartido.query.filter_by(formulario_id=formulario.id).delete()
            
            # Crear nuevos votos
            votos_partidos_nuevos = []
            for vp_data in cambios['votos_partidos']:
                voto_partido = VotoPartido(
                    formulario_id=formulario.id,
                    partido_id=vp_data['partido_id'],
                    votos=vp_data['votos']
                )
                db.session.add(voto_partido)
                votos_partidos_nuevos.append({
                    'partido_id': vp_data['partido_id'],
                    'votos': vp_data['votos']
                })
            
            cambios_realizados['votos_partidos'] = {
                'anterior': [{'partido_id': vp.partido_id, 'votos': vp.votos} for vp in formulario.votos_partidos],
                'nuevo': votos_partidos_nuevos
            }
        
        # Actualizar votos por candidato si se proporcionan
        if 'votos_candidatos' in cambios:
            # Eliminar votos existentes
            VotoCandidato.query.filter_by(formulario_id=formulario.id).delete()
            
            # Crear nuevos votos
            votos_candidatos_nuevos = []
            for vc_data in cambios['votos_candidatos']:
                voto_candidato = VotoCandidato(
                    formulario_id=formulario.id,
                    candidato_id=vc_data['candidato_id'],
                    votos=vc_data['votos']
                )
                db.session.add(voto_candidato)
                votos_candidatos_nuevos.append({
                    'candidato_id': vc_data['candidato_id'],
                    'votos': vc_data['votos']
                })
            
            cambios_realizados['votos_candidatos'] = {
                'anterior': [{'candidato_id': vc.candidato_id, 'votos': vc.votos} for vc in formulario.votos_candidatos],
                'nuevo': votos_candidatos_nuevos
            }
        
        return cambios_realizados
