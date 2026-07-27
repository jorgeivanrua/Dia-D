"""
Servicio para gestión de formularios E-14
"""
from backend.database import db
from backend.models.formulario_e14 import FormularioE14, VotoPartido, VotoCandidato, HistorialFormulario
from backend.models.location import Location
from backend.models.user import User
from backend.models.configuracion_electoral import TipoEleccion
from backend.utils.exceptions import ValidationException, NotFoundException
from datetime import datetime
from sqlalchemy import and_, or_


class FormularioService:
    """Servicio para operaciones CRUD de formularios E-14"""
    
    @staticmethod
    def crear_formulario(data, testigo_id):
        """
        Crear un nuevo formulario E-14
        
        Args:
            data: Diccionario con datos del formulario
            testigo_id: ID del testigo que crea el formulario
            
        Returns:
            FormularioE14: Formulario creado
        """
        # Validar datos requeridos
        required_fields = [
            'mesa_id', 'tipo_eleccion_id', 'total_votantes_registrados',
            'total_votos', 'votos_validos', 'votos_nulos', 'votos_blanco',
            'tarjetas_no_marcadas', 'total_tarjetas'
        ]
        
        for field in required_fields:
            if field not in data:
                raise ValidationException({field: [f'El campo {field} es requerido']})
        
        # Validar que la mesa existe
        mesa = Location.query.get(data['mesa_id'])
        if not mesa or mesa.tipo != 'mesa':
            raise ValidationException({'mesa_id': ['Mesa no encontrada']})
        
        # Validar que el testigo tiene acceso a esta mesa
        testigo = User.query.get(testigo_id)
        if not testigo:
            raise ValidationException({'testigo_id': ['Testigo no encontrado']})
        
        # Validar que no exista ya un formulario para esta mesa y tipo de elección
        formulario_existente = FormularioE14.query.filter_by(
            mesa_id=data['mesa_id'],
            tipo_eleccion_id=data['tipo_eleccion_id']
        ).first()
        
        if formulario_existente:
            tipo_eleccion = TipoEleccion.query.get(data['tipo_eleccion_id'])
            tipo_nombre = tipo_eleccion.nombre if tipo_eleccion else 'esta elección'
            raise ValidationException({
                'mesa_tipo_eleccion': [
                    f'Ya existe un formulario para esta mesa y {tipo_nombre}. '
                    f'Cada mesa solo puede tener un formulario por tipo de elección.'
                ]
            })
        
        # Validar coherencia de datos
        FormularioService._validar_coherencia_datos(data)
        
        # Crear formulario
        formulario = FormularioE14(
            mesa_id=data['mesa_id'],
            testigo_id=testigo_id,
            tipo_eleccion_id=data['tipo_eleccion_id'],
            total_votantes_registrados=data['total_votantes_registrados'],
            total_votos=data['total_votos'],
            votos_validos=data['votos_validos'],
            votos_nulos=data['votos_nulos'],
            votos_blanco=data['votos_blanco'],
            tarjetas_no_marcadas=data['tarjetas_no_marcadas'],
            total_tarjetas=data['total_tarjetas'],
            estado=data.get('estado', 'borrador'),
            imagen_url=data.get('imagen_url'),
            imagen_hash=data.get('imagen_hash'),
            observaciones=data.get('observaciones', '')
        )
        
        db.session.add(formulario)
        db.session.flush()  # Para obtener el ID
        
        # Crear votos por partido
        if 'votos_partidos' in data:
            for vp_data in data['votos_partidos']:
                voto_partido = VotoPartido(
                    formulario_id=formulario.id,
                    partido_id=vp_data['partido_id'],
                    votos=vp_data['votos']
                )
                db.session.add(voto_partido)
        
        # Crear votos por candidato
        if 'votos_candidatos' in data:
            for vc_data in data['votos_candidatos']:
                voto_candidato = VotoCandidato(
                    formulario_id=formulario.id,
                    candidato_id=vc_data['candidato_id'],
                    votos=vc_data['votos']
                )
                db.session.add(voto_candidato)
        
        # Registrar en historial
        historial = HistorialFormulario(
            formulario_id=formulario.id,
            usuario_id=testigo_id,
            accion='creado',
            estado_nuevo='borrador',
            comentario='Formulario creado'
        )
        db.session.add(historial)
        
        db.session.commit()
        
        return formulario
    
    @staticmethod
    def obtener_formularios_por_puesto(puesto_id, filtros=None, page=1, per_page=20):
        """
        Obtener formularios de un puesto con filtros y paginación
        
        Args:
            puesto_id: ID del puesto
            filtros: Diccionario con filtros opcionales (estado, fecha_desde, fecha_hasta)
            page: Número de página
            per_page: Resultados por página
            
        Returns:
            dict: Diccionario con formularios y metadatos de paginación
        """
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
        
        if not mesa_ids:
            # No hay mesas, retornar estructura vacía
            return {
                'formularios': [],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': 0,
                    'pages': 0
                },
                'estadisticas': {
                    'total': 0,
                    'pendientes': 0,
                    'validados': 0,
                    'rechazados': 0,
                    'mesas_reportadas': 0,
                    'total_mesas': 0
                }
            }
        
        # Construir query base
        query = FormularioE14.query.filter(FormularioE14.mesa_id.in_(mesa_ids))
        
        # Aplicar filtros
        if filtros:
            if 'estado' in filtros and filtros['estado']:
                query = query.filter_by(estado=filtros['estado'])
            
            if 'fecha_desde' in filtros and filtros['fecha_desde']:
                query = query.filter(FormularioE14.created_at >= filtros['fecha_desde'])
            
            if 'fecha_hasta' in filtros and filtros['fecha_hasta']:
                query = query.filter(FormularioE14.created_at <= filtros['fecha_hasta'])
        
        # Ordenar por fecha de creación descendente
        query = query.order_by(FormularioE14.created_at.desc())
        
        # Paginar
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Calcular estadísticas
        total_formularios = FormularioE14.query.filter(FormularioE14.mesa_id.in_(mesa_ids)).count()
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
        
        # Calcular mesas reportadas
        mesas_reportadas = db.session.query(FormularioE14.mesa_id).filter(
            FormularioE14.mesa_id.in_(mesa_ids),
            FormularioE14.estado.in_(['pendiente', 'validado'])
        ).distinct().count()
        
        return {
            'formularios': [f.to_dict() for f in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            },
            'estadisticas': {
                'total': total_formularios,
                'pendientes': pendientes,
                'validados': validados,
                'rechazados': rechazados,
                'mesas_reportadas': mesas_reportadas,
                'total_mesas': len(mesa_ids)
            }
        }
    
    @staticmethod
    def obtener_formulario_por_id(formulario_id, include_votos=True, include_historial=True):
        """
        Obtener un formulario por ID con todos sus detalles
        
        Args:
            formulario_id: ID del formulario
            include_votos: Incluir votos por partido y candidato
            include_historial: Incluir historial de cambios
            
        Returns:
            dict: Diccionario con datos completos del formulario
        """
        formulario = FormularioE14.query.get(formulario_id)
        
        if not formulario:
            raise NotFoundException('Formulario no encontrado')
        
        # Obtener datos del formulario
        data = formulario.to_dict(include_votos=include_votos, include_historial=include_historial)
        
        # Agregar información adicional de la mesa
        if formulario.mesa:
            data['mesa'] = {
                'id': formulario.mesa.id,
                'codigo': formulario.mesa.mesa_codigo,
                'nombre': formulario.mesa.nombre_completo,
                'total_votantes_registrados': formulario.mesa.total_votantes_registrados,
                'puesto_codigo': formulario.mesa.puesto_codigo,
                'puesto_nombre': formulario.mesa.puesto_nombre
            }
        
        # Agregar información del testigo
        if formulario.testigo:
            data['testigo'] = {
                'id': formulario.testigo.id,
                'nombre': formulario.testigo.nombre
            }
        
        # Agregar información del validador
        if formulario.validado_por:
            data['validado_por'] = {
                'id': formulario.validado_por.id,
                'nombre': formulario.validado_por.nombre
            }
        
        # Agregar información del tipo de elección
        if formulario.tipo_eleccion:
            data['tipo_eleccion'] = {
                'id': formulario.tipo_eleccion.id,
                'nombre': formulario.tipo_eleccion.nombre,
                'es_uninominal': formulario.tipo_eleccion.es_uninominal
            }
        
        # Calcular validaciones automáticas
        data['validaciones'] = FormularioService._calcular_validaciones(formulario)
        
        return data
    
    @staticmethod
    def actualizar_formulario(formulario_id, data, usuario_id):
        """
        Actualizar un formulario existente
        
        Args:
            formulario_id: ID del formulario
            data: Diccionario con datos a actualizar
            usuario_id: ID del usuario que actualiza
            
        Returns:
            FormularioE14: Formulario actualizado
        """
        formulario = FormularioE14.query.get(formulario_id)
        
        if not formulario:
            raise NotFoundException('Formulario no encontrado')
        
        # Solo se pueden editar formularios en estado borrador o pendiente
        if formulario.estado not in ['borrador', 'pendiente']:
            raise ValidationException({'estado': ['No se puede editar un formulario validado o rechazado']})
        
        # Guardar estado anterior para historial
        cambios = {}
        
        # Actualizar campos de votación
        campos_votacion = [
            'total_votantes_registrados', 'total_votos', 'votos_validos',
            'votos_nulos', 'votos_blanco', 'tarjetas_no_marcadas', 'total_tarjetas'
        ]
        
        for campo in campos_votacion:
            if campo in data:
                valor_anterior = getattr(formulario, campo)
                valor_nuevo = data[campo]
                if valor_anterior != valor_nuevo:
                    cambios[campo] = {'anterior': valor_anterior, 'nuevo': valor_nuevo}
                    setattr(formulario, campo, valor_nuevo)
        
        # Actualizar observaciones
        if 'observaciones' in data:
            if formulario.observaciones != data['observaciones']:
                cambios['observaciones'] = {
                    'anterior': formulario.observaciones,
                    'nuevo': data['observaciones']
                }
                formulario.observaciones = data['observaciones']
        
        # Actualizar estado si se proporciona
        if 'estado' in data and data['estado'] != formulario.estado:
            cambios['estado'] = {'anterior': formulario.estado, 'nuevo': data['estado']}
            formulario.estado = data['estado']
        
        # Validar coherencia de datos
        FormularioService._validar_coherencia_datos(formulario.__dict__)
        
        # Actualizar votos por partido si se proporcionan
        if 'votos_partidos' in data:
            # Eliminar votos existentes
            VotoPartido.query.filter_by(formulario_id=formulario_id).delete()
            
            # Crear nuevos votos
            for vp_data in data['votos_partidos']:
                voto_partido = VotoPartido(
                    formulario_id=formulario_id,
                    partido_id=vp_data['partido_id'],
                    votos=vp_data['votos']
                )
                db.session.add(voto_partido)
        
        # Actualizar votos por candidato si se proporcionan
        if 'votos_candidatos' in data:
            # Eliminar votos existentes
            VotoCandidato.query.filter_by(formulario_id=formulario_id).delete()
            
            # Crear nuevos votos
            for vc_data in data['votos_candidatos']:
                voto_candidato = VotoCandidato(
                    formulario_id=formulario_id,
                    candidato_id=vc_data['candidato_id'],
                    votos=vc_data['votos']
                )
                db.session.add(voto_candidato)
        
        # Registrar en historial si hubo cambios
        if cambios:
            historial = HistorialFormulario(
                formulario_id=formulario_id,
                usuario_id=usuario_id,
                accion='editado',
                cambios=cambios,
                comentario='Formulario actualizado'
            )
            db.session.add(historial)
        
        formulario.updated_at = datetime.utcnow()
        db.session.commit()
        
        return formulario
    
    @staticmethod
    def _validar_coherencia_datos(data):
        """Validar coherencia de datos del formulario"""
        errors = {}
        
        # Validar que votos válidos + nulos + blanco = total votos
        total_calculado = data['votos_validos'] + data['votos_nulos'] + data['votos_blanco']
        if total_calculado != data['total_votos']:
            errors['total_votos'] = [
                f'La suma de votos válidos ({data["votos_validos"]}) + nulos ({data["votos_nulos"]}) + '
                f'blanco ({data["votos_blanco"]}) debe ser igual al total de votos ({data["total_votos"]})'
            ]
        
        # Validar que total votos + tarjetas no marcadas = total tarjetas
        total_tarjetas_calculado = data['total_votos'] + data['tarjetas_no_marcadas']
        if total_tarjetas_calculado != data['total_tarjetas']:
            errors['total_tarjetas'] = [
                f'La suma de total votos ({data["total_votos"]}) + tarjetas no marcadas '
                f'({data["tarjetas_no_marcadas"]}) debe ser igual al total de tarjetas ({data["total_tarjetas"]})'
            ]
        
        # Validar que total votos no exceda votantes registrados
        if data['total_votos'] > data['total_votantes_registrados']:
            errors['total_votos'] = [
                f'El total de votos ({data["total_votos"]}) no puede exceder los votantes registrados '
                f'({data["total_votantes_registrados"]})'
            ]
        
        # Validar que todos los valores sean no negativos
        campos_numericos = [
            'total_votantes_registrados', 'total_votos', 'votos_validos',
            'votos_nulos', 'votos_blanco', 'tarjetas_no_marcadas', 'total_tarjetas'
        ]
        
        for campo in campos_numericos:
            if campo in data and data[campo] < 0:
                errors[campo] = [f'El valor de {campo} no puede ser negativo']
        
        if errors:
            raise ValidationException(errors)
    
    @staticmethod
    def _calcular_validaciones(formulario):
        """Calcular validaciones automáticas del formulario"""
        # Calcular suma de votos por partido
        suma_votos_partidos = sum(vp.votos for vp in formulario.votos_partidos)
        
        # Calcular suma de votos por candidato
        suma_votos_candidatos = sum(vc.votos for vc in formulario.votos_candidatos)
        
        # Total de votos (partidos + candidatos)
        total_votos_calculado = suma_votos_partidos + suma_votos_candidatos
        
        # Verificar coherencia
        coincide_votos_validos = total_votos_calculado == formulario.votos_validos
        coincide_total_votos = (formulario.votos_validos + formulario.votos_nulos + 
                               formulario.votos_blanco) == formulario.total_votos
        coincide_total_tarjetas = (formulario.total_votos + formulario.tarjetas_no_marcadas) == formulario.total_tarjetas
        
        # Calcular discrepancia porcentual
        if formulario.total_votantes_registrados > 0:
            discrepancia_porcentaje = abs(
                (formulario.total_votos - formulario.total_votantes_registrados) / 
                formulario.total_votantes_registrados * 100
            )
        else:
            discrepancia_porcentaje = 0
        
        return {
            'suma_votos_partidos': suma_votos_partidos,
            'suma_votos_candidatos': suma_votos_candidatos,
            'total_votos_calculado': total_votos_calculado,
            'coincide_votos_validos': coincide_votos_validos,
            'coincide_total_votos': coincide_total_votos,
            'coincide_total_tarjetas': coincide_total_tarjetas,
            'discrepancia_porcentaje': round(discrepancia_porcentaje, 2)
        }
