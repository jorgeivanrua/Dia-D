# Models package
from backend.models.user import User
from backend.models.location import Location
from backend.models.configuracion_electoral import TipoEleccion, Coalicion, PartidoCoalicion
from backend.models.partido_politico import PartidoPolitico as Partido
from backend.models.candidato import Candidato
from backend.models.formulario_e14 import FormularioE14, VotoPartido, VotoCandidato, HistorialFormulario
from backend.models.coordinador_municipal import (
    FormularioE24Puesto, VotoPartidoE24Puesto,
    FormularioE24Municipal, VotoPartidoE24Municipal, 
    NotificacionCoordinador, AuditLog
)
from backend.models.coordinador_departamental import ReporteDepartamental, VotoPartidoReporteDepartamental
from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral, NotificacionReporte
from backend.models.seguimiento import SeguimientoReporte
from backend.models.configuracion_sistema import ConfiguracionSistema, FondoLogin

__all__ = [
    'User',
    'Location',
    'TipoEleccion',
    'Partido',
    'Coalicion',
    'PartidoCoalicion',
    'Candidato',
    'FormularioE14',
    'VotoPartido',
    'VotoCandidato',
    'HistorialFormulario',
    'FormularioE24Puesto',
    'VotoPartidoE24Puesto',
    'FormularioE24Municipal',
    'VotoPartidoE24Municipal',
    'NotificacionCoordinador',
    'AuditLog',
    'ReporteDepartamental',
    'VotoPartidoReporteDepartamental',
    'IncidenteElectoral',
    'DelitoElectoral',
    'SeguimientoReporte',
    'NotificacionReporte',
    'ConfiguracionSistema',
    'FondoLogin'
]
