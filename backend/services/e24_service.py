"""
Servicio para generación de formularios E-24 Municipal
"""
from backend.database import db
from backend.models.location import Location
from backend.models.user import User
from backend.models.coordinador_municipal import FormularioE24Municipal, VotoPartidoE24Municipal
from backend.services.consolidado_service import ConsolidadoService
from backend.services.municipal_service import MunicipalService
from datetime import datetime
import hashlib
import os


class E24Service:
    """Servicio para generación de formularios E-24 Municipal"""
    
    REQUISITO_MINIMO_PUESTOS = 0.80  # 80% de puestos con datos completos
    
    @staticmethod
    def validar_requisitos_e24(municipio_id):
        """
        Validar que se cumplen requisitos para generar E-24
        
        Args:
            municipio_id: ID del municipio
            
        Returns:
            tuple: (bool cumple_requisitos, list errores)
        """
        errores = []
        
        # Obtener el municipio
        municipio = Location.query.get(municipio_id)
        if not municipio or municipio.tipo != 'municipio':
            errores.append('Municipio no válido')
            return (False, errores)
        
        # Obtener estadísticas de puestos
        resultado = MunicipalService.obtener_puestos_municipio(municipio_id)
        if not resultado:
            errores.append('No se pudieron obtener datos del municipio')
            return (False, errores)
        
        estadisticas = resultado.get('estadisticas', {})
        total_puestos = estadisticas.get('total_puestos', 0)
        puestos_completos = estadisticas.get('puestos_completos', 0)
        
        if total_puestos == 0:
            errores.append('El municipio no tiene puestos asignados')
            return (False, errores)
        
        # Verificar porcentaje de puestos completos
        porcentaje_completos = puestos_completos / total_puestos
        if porcentaje_completos < E24Service.REQUISITO_MINIMO_PUESTOS:
            errores.append(
                f'Se requiere al menos {E24Service.REQUISITO_MINIMO_PUESTOS * 100}% de puestos completos. '
                f'Actualmente: {porcentaje_completos * 100:.1f}% ({puestos_completos}/{total_puestos})'
            )
            return (False, errores)
        
        # Verificar que hay datos consolidados
        consolidado = ConsolidadoService.calcular_consolidado_municipal(municipio_id)
        if not consolidado:
            errores.append('No se pudo calcular el consolidado municipal')
            return (False, errores)
        
        resumen = consolidado.get('resumen', {})
        if resumen.get('total_votos', 0) == 0:
            errores.append('No hay votos registrados en el municipio')
            return (False, errores)
        
        return (True, [])
    
    @staticmethod
    def generar_e24_municipal(municipio_id, tipo_eleccion_id, coordinador_id):
        """
        Generar formulario E-24 Municipal
        
        Args:
            municipio_id: ID del municipio
            tipo_eleccion_id: ID del tipo de elección
            coordinador_id: ID del coordinador que genera el E-24
            
        Returns:
            FormularioE24Municipal: Formulario generado
        """
        # Validar requisitos
        cumple, errores = E24Service.validar_requisitos_e24(municipio_id)
        if not cumple:
            raise ValueError(f'No se cumplen los requisitos para generar E-24: {", ".join(errores)}')
        
        # Obtener consolidado municipal
        consolidado = ConsolidadoService.calcular_consolidado_municipal(municipio_id, tipo_eleccion_id)
        if not consolidado:
            raise ValueError('No se pudo calcular el consolidado municipal')
        
        municipio_info = consolidado.get('municipio', {})
        resumen = consolidado.get('resumen', {})
        votos_por_partido = consolidado.get('votos_por_partido', [])
        
        # Generar PDF
        pdf_filename = f'e24_municipal_{municipio_id}_{tipo_eleccion_id}_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.pdf'
        pdf_path = os.path.join('pdfs', pdf_filename)
        
        # Asegurar que el directorio existe
        os.makedirs('pdfs', exist_ok=True)
        
        # Generar PDF (por ahora solo creamos un archivo placeholder)
        pdf_url = E24Service.generar_pdf_e24(consolidado, municipio_id, coordinador_id, pdf_path)
        
        # Calcular hash del PDF
        pdf_hash = E24Service.calcular_hash_archivo(pdf_path)
        
        # Verificar si ya existe un E-24 para este municipio y tipo de elección
        e24_existente = FormularioE24Municipal.query.filter_by(
            municipio_id=municipio_id,
            tipo_eleccion_id=tipo_eleccion_id
        ).order_by(FormularioE24Municipal.version.desc()).first()
        
        version = 1
        if e24_existente:
            version = e24_existente.version + 1
        
        # Crear registro en base de datos
        e24_municipal = FormularioE24Municipal(
            municipio_id=municipio_id,
            coordinador_id=coordinador_id,
            tipo_eleccion_id=tipo_eleccion_id,
            total_puestos=municipio_info.get('total_puestos', 0),
            puestos_incluidos=municipio_info.get('total_puestos', 0),
            total_mesas=municipio_info.get('total_mesas', 0),
            total_votantes_registrados=resumen.get('total_votantes_registrados', 0),
            total_votos=resumen.get('total_votos', 0),
            votos_validos=resumen.get('votos_validos', 0),
            votos_nulos=resumen.get('votos_nulos', 0),
            votos_blanco=resumen.get('votos_blanco', 0),
            pdf_url=pdf_url,
            pdf_hash=pdf_hash,
            version=version
        )
        
        db.session.add(e24_municipal)
        db.session.flush()  # Para obtener el ID
        
        # Guardar votos por partido
        for vp in votos_por_partido:
            voto_partido_e24 = VotoPartidoE24Municipal(
                e24_municipal_id=e24_municipal.id,
                partido_id=vp['partido_id'],
                votos=vp['total_votos'],
                porcentaje=vp['porcentaje']
            )
            db.session.add(voto_partido_e24)
        
        db.session.commit()
        
        return e24_municipal
    
    @staticmethod
    def generar_pdf_e24(consolidado, municipio_id, coordinador_id, pdf_path):
        """
        Generar PDF del formulario E-24 Municipal
        
        Args:
            consolidado: dict con datos consolidados
            municipio_id: ID del municipio
            coordinador_id: ID del coordinador
            pdf_path: Ruta donde guardar el PDF
            
        Returns:
            str: URL del PDF generado
        """
        # Por ahora, crear un archivo de texto simple como placeholder
        # En producción, usar ReportLab o WeasyPrint para generar PDF real
        
        municipio = Location.query.get(municipio_id)
        coordinador = User.query.get(coordinador_id)
        
        municipio_info = consolidado.get('municipio', {})
        resumen = consolidado.get('resumen', {})
        votos_por_partido = consolidado.get('votos_por_partido', [])
        
        contenido = f"""
FORMULARIO E-24 MUNICIPAL
=========================

Municipio: {municipio_info.get('nombre', 'N/A')}
Código: {municipio_info.get('codigo', 'N/A')}
Total Puestos: {municipio_info.get('total_puestos', 0)}
Total Mesas: {municipio_info.get('total_mesas', 0)}

RESUMEN DE VOTACIÓN
-------------------
Total Votantes Registrados: {resumen.get('total_votantes_registrados', 0)}
Total Votos: {resumen.get('total_votos', 0)}
Votos Válidos: {resumen.get('votos_validos', 0)}
Votos Nulos: {resumen.get('votos_nulos', 0)}
Votos en Blanco: {resumen.get('votos_blanco', 0)}
Participación: {resumen.get('participacion_porcentaje', 0):.2f}%

VOTOS POR PARTIDO
-----------------
"""
        
        for vp in votos_por_partido:
            contenido += f"{vp['partido_nombre']}: {vp['total_votos']} votos ({vp['porcentaje']:.2f}%)\n"
        
        contenido += f"""

FIRMA DIGITAL
-------------
Coordinador: {coordinador.nombre if coordinador else 'N/A'}
Fecha: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
"""
        
        # Guardar archivo
        with open(pdf_path, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        # Retornar URL relativa
        return f'/{pdf_path}'
    
    @staticmethod
    def calcular_hash_archivo(filepath):
        """
        Calcular hash SHA-256 de un archivo
        
        Args:
            filepath: Ruta del archivo
            
        Returns:
            str: Hash SHA-256 en hexadecimal
        """
        sha256_hash = hashlib.sha256()
        
        with open(filepath, 'rb') as f:
            # Leer en bloques para archivos grandes
            for byte_block in iter(lambda: f.read(4096), b''):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
