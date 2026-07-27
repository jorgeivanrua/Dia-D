"""
Servicio para generación de reportes departamentales
Basado en E24Service pero para nivel departamental
"""
from backend.database import db
from backend.models.location import Location
from backend.models.user import User
from backend.models.coordinador_departamental import ReporteDepartamental, VotoPartidoReporteDepartamental
from backend.services.departamental_service import DepartamentalService
from datetime import datetime
import hashlib
import os


class ReporteDepartamentalService:
    """Servicio para generación de reportes departamentales"""
    
    REQUISITO_MINIMO_MUNICIPIOS = 0.90  # 90% de municipios con datos completos
    
    @staticmethod
    def validar_requisitos_reporte(departamento_id):
        """
        Validar que se cumplen requisitos para generar reporte departamental
        
        Args:
            departamento_id: ID del departamento
            
        Returns:
            tuple: (bool cumple_requisitos, list errores)
        """
        errores = []
        
        # Obtener el departamento
        departamento = Location.query.get(departamento_id)
        if not departamento or departamento.tipo != 'departamento':
            errores.append('Departamento no válido')
            return (False, errores)
        
        # Obtener estadísticas de municipios
        resultado = DepartamentalService.obtener_municipios_departamento(departamento_id)
        if not resultado:
            errores.append('No se pudieron obtener datos del departamento')
            return (False, errores)
        
        estadisticas = resultado.get('estadisticas', {})
        total_municipios = estadisticas.get('total_municipios', 0)
        municipios_completos = estadisticas.get('municipios_completos', 0)
        
        if total_municipios == 0:
            errores.append('El departamento no tiene municipios asignados')
            return (False, errores)
        
        # Verificar porcentaje de municipios completos
        porcentaje_completos = municipios_completos / total_municipios
        if porcentaje_completos < ReporteDepartamentalService.REQUISITO_MINIMO_MUNICIPIOS:
            errores.append(
                f'Se requiere al menos {ReporteDepartamentalService.REQUISITO_MINIMO_MUNICIPIOS * 100}% de municipios completos. '
                f'Actualmente: {porcentaje_completos * 100:.1f}% ({municipios_completos}/{total_municipios})'
            )
            return (False, errores)
        
        # Verificar que hay datos consolidados
        consolidado = DepartamentalService.calcular_consolidado_departamental(departamento_id)
        if not consolidado:
            errores.append('No se pudo calcular el consolidado departamental')
            return (False, errores)
        
        resumen = consolidado.get('resumen', {})
        if resumen.get('total_votos', 0) == 0:
            errores.append('No hay votos registrados en el departamento')
            return (False, errores)
        
        return (True, [])
    
    @staticmethod
    def generar_reporte_departamental(departamento_id, tipo_eleccion_id, coordinador_id):
        """
        Generar reporte departamental
        
        Args:
            departamento_id: ID del departamento
            tipo_eleccion_id: ID del tipo de elección
            coordinador_id: ID del coordinador que genera el reporte
            
        Returns:
            ReporteDepartamental: Reporte generado
        """
        # Validar requisitos
        cumple, errores = ReporteDepartamentalService.validar_requisitos_reporte(departamento_id)
        if not cumple:
            raise ValueError(f'No se cumplen los requisitos para generar reporte: {", ".join(errores)}')
        
        # Obtener consolidado departamental
        consolidado = DepartamentalService.calcular_consolidado_departamental(departamento_id, tipo_eleccion_id)
        if not consolidado:
            raise ValueError('No se pudo calcular el consolidado departamental')
        
        departamento_info = consolidado.get('departamento', {})
        resumen = consolidado.get('resumen', {})
        votos_por_partido = consolidado.get('votos_por_partido', [])
        
        # Generar PDF (simplificado por ahora)
        pdf_filename = f'reporte_departamental_{departamento_id}_{tipo_eleccion_id}_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.pdf'
        pdf_url = f'/pdfs/{pdf_filename}'
        pdf_hash = 'pending'  # Por ahora
        
        # Verificar si ya existe un reporte para este departamento y tipo de elección
        reporte_existente = ReporteDepartamental.query.filter_by(
            departamento_id=departamento_id,
            tipo_eleccion_id=tipo_eleccion_id
        ).order_by(ReporteDepartamental.version.desc()).first()
        
        version = 1
        if reporte_existente:
            version = reporte_existente.version + 1
        
        # Crear registro en base de datos
        reporte_departamental = ReporteDepartamental(
            departamento_id=departamento_id,
            coordinador_id=coordinador_id,
            tipo_eleccion_id=tipo_eleccion_id,
            total_municipios=departamento_info.get('total_municipios', 0),
            municipios_incluidos=departamento_info.get('total_municipios', 0),
            total_puestos=departamento_info.get('total_puestos', 0),
            total_mesas=departamento_info.get('total_mesas', 0),
            total_votantes_registrados=resumen.get('total_votantes_registrados', 0),
            total_votos=resumen.get('total_votos', 0),
            votos_validos=resumen.get('votos_validos', 0),
            votos_nulos=resumen.get('votos_nulos', 0),
            votos_blanco=resumen.get('votos_blanco', 0),
            pdf_url=pdf_url,
            pdf_hash=pdf_hash,
            version=version,
            created_at=datetime.utcnow()
        )
        
        db.session.add(reporte_departamental)
        db.session.flush()
        
        # Guardar votos por partido
        for vp in votos_por_partido:
            voto_partido = VotoPartidoReporteDepartamental(
                reporte_departamental_id=reporte_departamental.id,
                partido_id=vp['partido_id'],
                total_votos=vp['total_votos']
            )
            db.session.add(voto_partido)
        
        db.session.commit()
        
        return reporte_departamental
    
    @staticmethod
    def calcular_hash_archivo(filepath):
        """Calcular hash SHA256 de un archivo"""
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"Error calculando hash: {e}")
            return None
