"""
Sistema de Auditoría y Testing Completo
Prueba todas las funcionalidades de cada rol con datos precargados
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import json
from datetime import datetime, date
from typing import Dict, List, Tuple
from colorama import init, Fore, Style

# Inicializar colorama para colores en consola
init(autoreset=True)

# Configuración
BASE_URL = 'http://localhost:5000'
API_URL = f'{BASE_URL}/api'


class AuditLogger:
    """Logger para auditoría con colores"""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.warnings = 0
        self.results = []
    
    def success(self, message: str):
        """Log de éxito"""
        print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")
        self.tests_passed += 1
        self.results.append(('SUCCESS', message))
    
    def error(self, message: str):
        """Log de error"""
        print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")
        self.tests_failed += 1
        self.results.append(('ERROR', message))
    
    def warning(self, message: str):
        """Log de advertencia"""
        print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")
        self.warnings += 1
        self.results.append(('WARNING', message))
    
    def info(self, message: str):
        """Log informativo"""
        print(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")
    
    def section(self, title: str):
        """Separador de sección"""
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}{Style.RESET_ALL}\n")
    
    def summary(self):
        """Resumen final"""
        total = self.tests_passed + self.tests_failed
        success_rate = (self.tests_passed / total * 100) if total > 0 else 0
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"  RESUMEN DE AUDITORÍA")
        print(f"{'='*60}{Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}✅ Pruebas exitosas: {self.tests_passed}{Style.RESET_ALL}")
        print(f"{Fore.RED}❌ Pruebas fallidas: {self.tests_failed}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⚠️  Advertencias: {self.warnings}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}📊 Tasa de éxito: {success_rate:.1f}%{Style.RESET_ALL}\n")
        
        return success_rate >= 90


logger = AuditLogger()


class APIClient:
    """Cliente para interactuar con la API"""
    
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_info = None
    
    def login(self, username: str, password: str) -> bool:
        """Iniciar sesión"""
        try:
            response = self.session.post(
                f'{API_URL}/auth/login',
                json={'nombre': username, 'password': password}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('access_token')
                self.user_info = data.get('user')
                self.session.headers.update({
                    'Authorization': f'Bearer {self.token}'
                })
                return True
            else:
                logger.error(f"Login falló: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error en login: {str(e)}")
            return False
    
    def logout(self):
        """Cerrar sesión"""
        self.token = None
        self.user_info = None
        self.session.headers.pop('Authorization', None)
    
    def get(self, endpoint: str) -> Tuple[int, dict]:
        """GET request"""
        try:
            response = self.session.get(f'{API_URL}{endpoint}')
            return response.status_code, response.json() if response.text else {}
        except Exception as e:
            logger.error(f"Error en GET {endpoint}: {str(e)}")
            return 500, {'error': str(e)}
    
    def post(self, endpoint: str, data: dict) -> Tuple[int, dict]:
        """POST request"""
        try:
            response = self.session.post(f'{API_URL}{endpoint}', json=data)
            return response.status_code, response.json() if response.text else {}
        except Exception as e:
            logger.error(f"Error en POST {endpoint}: {str(e)}")
            return 500, {'error': str(e)}
    
    def put(self, endpoint: str, data: dict) -> Tuple[int, dict]:
        """PUT request"""
        try:
            response = self.session.put(f'{API_URL}{endpoint}', json=data)
            return response.status_code, response.json() if response.text else {}
        except Exception as e:
            logger.error(f"Error en PUT {endpoint}: {str(e)}")
            return 500, {'error': str(e)}
    
    def delete(self, endpoint: str) -> Tuple[int, dict]:
        """DELETE request"""
        try:
            response = self.session.delete(f'{API_URL}{endpoint}')
            return response.status_code, response.json() if response.text else {}
        except Exception as e:
            logger.error(f"Error en DELETE {endpoint}: {str(e)}")
            return 500, {'error': str(e)}


def test_super_admin_role(client: APIClient):
    """Pruebas para rol Super Admin"""
    logger.section("PRUEBAS: SUPER ADMIN")
    
    # Login
    if not client.login('admin_test', 'test123'):
        logger.error("No se pudo iniciar sesión como Super Admin")
        return
    
    logger.success(f"Login exitoso como: {client.user_info.get('nombre')}")
    
    # 1. Verificar acceso al dashboard
    status, data = client.get('/super-admin/dashboard')
    if status == 200:
        logger.success("Acceso al dashboard de Super Admin")
    else:
        logger.error(f"No se pudo acceder al dashboard: {status}")
    
    # 2. Listar usuarios
    status, data = client.get('/super-admin/usuarios')
    if status == 200 and data.get('success'):
        usuarios = data.get('usuarios', [])
        logger.success(f"Listado de usuarios: {len(usuarios)} usuarios encontrados")
    else:
        logger.error("No se pudo listar usuarios")
    
    # 3. Crear nuevo usuario
    nuevo_usuario = {
        'nombre': f'test_user_{datetime.now().timestamp()}',
        'password': 'test123',
        'rol': 'testigo',
        'ubicacion_id': 1
    }
    status, data = client.post('/super-admin/usuarios', nuevo_usuario)
    if status in [200, 201] and data.get('success'):
        logger.success(f"Usuario creado: {nuevo_usuario['nombre']}")
        user_id = data.get('usuario', {}).get('id')
        
        # 4. Actualizar usuario
        if user_id:
            status, data = client.put(f'/super-admin/usuarios/{user_id}', {'activo': False})
            if status == 200 and data.get('success'):
                logger.success(f"Usuario actualizado (desactivado)")
            else:
                logger.error("No se pudo actualizar usuario")
    else:
        logger.error("No se pudo crear usuario")
    
    # 5. Gestión de campañas
    status, data = client.get('/super-admin/campanas')
    if status == 200:
        logger.success("Acceso a gestión de campañas")
    else:
        logger.error("No se pudo acceder a campañas")
    
    # 6. Configuración electoral
    status, data = client.get('/configuracion/tipos-eleccion')
    if status == 200:
        logger.success("Acceso a configuración electoral")
    else:
        logger.error("No se pudo acceder a configuración")
    
    # 7. Estadísticas globales
    status, data = client.get('/super-admin/estadisticas')
    if status == 200:
        logger.success("Acceso a estadísticas globales")
    else:
        logger.warning("Endpoint de estadísticas no disponible")
    
    client.logout()


def test_testigo_role(client: APIClient):
    """Pruebas para rol Testigo Electoral"""
    logger.section("PRUEBAS: TESTIGO ELECTORAL")
    
    # Login
    if not client.login('testigo_test_1', 'test123'):
        logger.error("No se pudo iniciar sesión como Testigo")
        return
    
    logger.success(f"Login exitoso como: {client.user_info.get('nombre')}")
    
    # 1. Verificar presencia
    status, data = client.post('/api/testigo/verificar-presencia', {})
    if status == 200 and data.get('success'):
        logger.success("Presencia verificada correctamente")
    else:
        logger.warning("No se pudo verificar presencia (puede estar ya verificada)")
    
    # 2. Acceso al dashboard
    status, data = client.get('/api/testigo/dashboard')
    if status == 200:
        logger.success("Acceso al dashboard de testigo")
    else:
        logger.error(f"No se pudo acceder al dashboard: {status}")
    
    # 3. Crear formulario E-14
    formulario_e14 = {
        'mesa_id': client.user_info.get('ubicacion_id'),
        'total_votantes': 300,
        'votos_depositados': 285,
        'votos_nulos': 5,
        'votos_blancos': 10,
        'votos_no_marcados': 0,
        'tarjetas_no_usadas': 15,
        'votos_partidos': [
            {'partido_id': 1, 'votos': 100},
            {'partido_id': 2, 'votos': 85},
            {'partido_id': 3, 'votos': 75},
            {'partido_id': 4, 'votos': 10}
        ]
    }
    status, data = client.post('/api/formularios-e14', formulario_e14)
    if status in [200, 201] and data.get('success'):
        logger.success("Formulario E-14 creado correctamente")
        form_id = data.get('formulario', {}).get('id')
        
        # 4. Enviar formulario
        if form_id:
            status, data = client.post(f'/api/formularios-e14/{form_id}/enviar', {})
            if status == 200 and data.get('success'):
                logger.success("Formulario E-14 enviado correctamente")
            else:
                logger.error("No se pudo enviar el formulario")
    else:
        logger.error("No se pudo crear formulario E-14")
    
    # 5. Reportar incidente
    incidente = {
        'tipo_incidente': 'irregularidad_votacion',
        'descripcion': 'Prueba de reporte de incidente',
        'gravedad': 'media',
        'ubicacion_id': client.user_info.get('ubicacion_id')
    }
    status, data = client.post('/api/incidentes', incidente)
    if status in [200, 201] and data.get('success'):
        logger.success("Incidente reportado correctamente")
    else:
        logger.warning("No se pudo reportar incidente (endpoint puede no estar disponible)")
    
    # 6. Ver historial de formularios
    status, data = client.get('/api/formularios-e14/mis-formularios')
    if status == 200:
        logger.success("Acceso al historial de formularios")
    else:
        logger.error("No se pudo acceder al historial")
    
    client.logout()


def test_coordinador_puesto_role(client: APIClient):
    """Pruebas para rol Coordinador de Puesto"""
    logger.section("PRUEBAS: COORDINADOR DE PUESTO")
    
    # Login
    if not client.login('coord_puesto_test', 'test123'):
        logger.error("No se pudo iniciar sesión como Coordinador de Puesto")
        return
    
    logger.success(f"Login exitoso como: {client.user_info.get('nombre')}")
    
    # 1. Dashboard
    status, data = client.get('/api/coordinador-puesto/dashboard')
    if status == 200:
        logger.success("Acceso al dashboard de coordinador de puesto")
    else:
        logger.error(f"No se pudo acceder al dashboard: {status}")
    
    # 2. Ver formularios pendientes
    status, data = client.get('/api/coordinador-puesto/formularios-pendientes')
    if status == 200:
        logger.success("Acceso a formularios pendientes")
        formularios = data.get('formularios', [])
        logger.info(f"Formularios pendientes: {len(formularios)}")
    else:
        logger.error("No se pudo acceder a formularios pendientes")
    
    # 3. Consolidar E-24 Puesto
    e24_puesto = {
        'puesto_id': client.user_info.get('ubicacion_id'),
        'total_mesas': 5,
        'mesas_reportadas': 5,
        'total_votantes': 1500,
        'votos_depositados': 1425,
        'votos_nulos': 25,
        'votos_blancos': 50,
        'votos_partidos': [
            {'partido_id': 1, 'votos': 500},
            {'partido_id': 2, 'votos': 425},
            {'partido_id': 3, 'votos': 375},
            {'partido_id': 4, 'votos': 50}
        ]
    }
    status, data = client.post('/api/coordinador-puesto/e24-puesto', e24_puesto)
    if status in [200, 201] and data.get('success'):
        logger.success("Formulario E-24 Puesto consolidado")
    else:
        logger.warning("No se pudo consolidar E-24 Puesto (puede ya existir)")
    
    # 4. Ver incidentes del puesto
    status, data = client.get('/api/coordinador-puesto/incidentes')
    if status == 200:
        logger.success("Acceso a incidentes del puesto")
    else:
        logger.warning("No se pudo acceder a incidentes")
    
    # 5. Estadísticas del puesto
    status, data = client.get('/api/coordinador-puesto/estadisticas')
    if status == 200:
        logger.success("Acceso a estadísticas del puesto")
    else:
        logger.warning("Endpoint de estadísticas no disponible")
    
    client.logout()


def test_coordinador_municipal_role(client: APIClient):
    """Pruebas para rol Coordinador Municipal"""
    logger.section("PRUEBAS: COORDINADOR MUNICIPAL")
    
    # Login
    if not client.login('coord_mun_test', 'test123'):
        logger.error("No se pudo iniciar sesión como Coordinador Municipal")
        return
    
    logger.success(f"Login exitoso como: {client.user_info.get('nombre')}")
    
    # 1. Dashboard
    status, data = client.get('/api/coordinador-municipal/dashboard')
    if status == 200:
        logger.success("Acceso al dashboard de coordinador municipal")
    else:
        logger.error(f"No se pudo acceder al dashboard: {status}")
    
    # 2. Ver consolidados de puestos
    status, data = client.get('/api/coordinador-municipal/consolidados-puestos')
    if status == 200:
        logger.success("Acceso a consolidados de puestos")
    else:
        logger.error("No se pudo acceder a consolidados")
    
    # 3. Consolidar E-24 Municipal
    e24_municipal = {
        'municipio_id': client.user_info.get('ubicacion_id'),
        'total_puestos': 3,
        'puestos_reportados': 3,
        'total_mesas': 15,
        'mesas_reportadas': 15,
        'total_votantes': 4500,
        'votos_depositados': 4275,
        'votos_nulos': 75,
        'votos_blancos': 150,
        'votos_partidos': [
            {'partido_id': 1, 'votos': 1500},
            {'partido_id': 2, 'votos': 1275},
            {'partido_id': 3, 'votos': 1125},
            {'partido_id': 4, 'votos': 150}
        ]
    }
    status, data = client.post('/api/coordinador-municipal/e24-municipal', e24_municipal)
    if status in [200, 201] and data.get('success'):
        logger.success("Formulario E-24 Municipal consolidado")
    else:
        logger.warning("No se pudo consolidar E-24 Municipal (puede ya existir)")
    
    # 4. Ver incidentes municipales
    status, data = client.get('/api/coordinador-municipal/incidentes')
    if status == 200:
        logger.success("Acceso a incidentes municipales")
    else:
        logger.warning("No se pudo acceder a incidentes")
    
    # 5. Enviar notificaciones
    notificacion = {
        'destinatarios': ['coordinador_puesto'],
        'mensaje': 'Prueba de notificación desde auditoría',
        'prioridad': 'normal'
    }
    status, data = client.post('/api/coordinador-municipal/notificaciones', notificacion)
    if status in [200, 201]:
        logger.success("Notificación enviada correctamente")
    else:
        logger.warning("No se pudo enviar notificación")
    
    client.logout()


def test_coordinador_departamental_role(client: APIClient):
    """Pruebas para rol Coordinador Departamental"""
    logger.section("PRUEBAS: COORDINADOR DEPARTAMENTAL")
    
    # Login
    if not client.login('coord_dept_test', 'test123'):
        logger.error("No se pudo iniciar sesión como Coordinador Departamental")
        return
    
    logger.success(f"Login exitoso como: {client.user_info.get('nombre')}")
    
    # 1. Dashboard
    status, data = client.get('/api/coordinador-departamental/dashboard')
    if status == 200:
        logger.success("Acceso al dashboard de coordinador departamental")
    else:
        logger.error(f"No se pudo acceder al dashboard: {status}")
    
    # 2. Ver consolidados municipales
    status, data = client.get('/api/coordinador-departamental/consolidados-municipales')
    if status == 200:
        logger.success("Acceso a consolidados municipales")
    else:
        logger.error("No se pudo acceder a consolidados")
    
    # 3. Consolidar reporte departamental
    reporte_dept = {
        'departamento_id': client.user_info.get('ubicacion_id'),
        'total_municipios': 1,
        'municipios_reportados': 1,
        'total_puestos': 3,
        'total_mesas': 15,
        'total_votantes': 4500,
        'votos_depositados': 4275,
        'votos_nulos': 75,
        'votos_blancos': 150,
        'votos_partidos': [
            {'partido_id': 1, 'votos': 1500},
            {'partido_id': 2, 'votos': 1275},
            {'partido_id': 3, 'votos': 1125},
            {'partido_id': 4, 'votos': 150}
        ]
    }
    status, data = client.post('/api/coordinador-departamental/reporte', reporte_dept)
    if status in [200, 201] and data.get('success'):
        logger.success("Reporte departamental consolidado")
    else:
        logger.warning("No se pudo consolidar reporte departamental (puede ya existir)")
    
    # 4. Estadísticas departamentales
    status, data = client.get('/api/coordinador-departamental/estadisticas')
    if status == 200:
        logger.success("Acceso a estadísticas departamentales")
    else:
        logger.warning("Endpoint de estadísticas no disponible")
    
    client.logout()


def test_auditor_role(client: APIClient):
    """Pruebas para rol Auditor Electoral"""
    logger.section("PRUEBAS: AUDITOR ELECTORAL")
    
    # Login
    if not client.login('auditor_test', 'test123'):
        logger.error("No se pudo iniciar sesión como Auditor")
        return
    
    logger.success(f"Login exitoso como: {client.user_info.get('nombre')}")
    
    # 1. Dashboard de auditoría
    status, data = client.get('/api/auditor/dashboard')
    if status == 200:
        logger.success("Acceso al dashboard de auditor")
    else:
        logger.error(f"No se pudo acceder al dashboard: {status}")
    
    # 2. Ver logs de auditoría
    status, data = client.get('/api/auditor/audit-logs')
    if status == 200:
        logger.success("Acceso a logs de auditoría")
        logs = data.get('logs', [])
        logger.info(f"Logs encontrados: {len(logs)}")
    else:
        logger.error("No se pudo acceder a logs")
    
    # 3. Ver todos los formularios
    status, data = client.get('/api/auditor/formularios')
    if status == 200:
        logger.success("Acceso a todos los formularios")
    else:
        logger.error("No se pudo acceder a formularios")
    
    # 4. Ver incidentes y delitos
    status, data = client.get('/api/auditor/incidentes')
    if status == 200:
        logger.success("Acceso a incidentes y delitos")
    else:
        logger.warning("No se pudo acceder a incidentes")
    
    # 5. Generar reportes
    status, data = client.post('/api/auditor/reportes', {
        'tipo': 'consolidado',
        'fecha_inicio': date.today().isoformat(),
        'fecha_fin': date.today().isoformat()
    })
    if status in [200, 201]:
        logger.success("Reporte generado correctamente")
    else:
        logger.warning("No se pudo generar reporte")
    
    client.logout()


def test_security_and_permissions():
    """Pruebas de seguridad y permisos"""
    logger.section("PRUEBAS: SEGURIDAD Y PERMISOS")
    
    client = APIClient()
    
    # 1. Acceso sin autenticación
    status, data = client.get('/super-admin/usuarios')
    if status == 401:
        logger.success("Acceso denegado sin autenticación (correcto)")
    else:
        logger.error("Se permitió acceso sin autenticación (FALLO DE SEGURIDAD)")
    
    # 2. Testigo intentando acceder a funciones de admin
    if client.login('testigo_test_1', 'test123'):
        status, data = client.get('/super-admin/usuarios')
        if status in [401, 403]:
            logger.success("Testigo no puede acceder a funciones de admin (correcto)")
        else:
            logger.error("Testigo accedió a funciones de admin (FALLO DE SEGURIDAD)")
        client.logout()
    
    # 3. Login con credenciales incorrectas
    if not client.login('usuario_falso', 'password_falsa'):
        logger.success("Login rechazado con credenciales incorrectas (correcto)")
    else:
        logger.error("Login aceptado con credenciales incorrectas (FALLO DE SEGURIDAD)")
    
    # 4. Intentos de inyección SQL (básico)
    if not client.login("admin' OR '1'='1", "password"):
        logger.success("Protección contra inyección SQL básica (correcto)")
    else:
        logger.error("Vulnerable a inyección SQL (FALLO DE SEGURIDAD CRÍTICO)")


def run_full_audit():
    """Ejecutar auditoría completa del sistema"""
    logger.section("INICIO DE AUDITORÍA COMPLETA DEL SISTEMA")
    logger.info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"URL Base: {BASE_URL}")
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(BASE_URL, timeout=5)
        logger.success("Servidor accesible")
    except Exception as e:
        logger.error(f"No se puede conectar al servidor: {str(e)}")
        logger.error("Asegúrate de que el servidor esté corriendo en http://localhost:5000")
        return False
    
    client = APIClient()
    
    # Ejecutar pruebas por rol
    test_super_admin_role(client)
    test_testigo_role(client)
    test_coordinador_puesto_role(client)
    test_coordinador_municipal_role(client)
    test_coordinador_departamental_role(client)
    test_auditor_role(client)
    
    # Pruebas de seguridad
    test_security_and_permissions()
    
    # Resumen final
    return logger.summary()


if __name__ == '__main__':
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗")
    print(f"║  SISTEMA DE AUDITORÍA Y TESTING COMPLETO                 ║")
    print(f"║  Sistema Electoral - Pruebas Automatizadas               ║")
    print(f"╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    success = run_full_audit()
    
    if success:
        print(f"\n{Fore.GREEN}✅ AUDITORÍA COMPLETADA EXITOSAMENTE{Style.RESET_ALL}\n")
        sys.exit(0)
    else:
        print(f"\n{Fore.RED}❌ AUDITORÍA COMPLETADA CON ERRORES{Style.RESET_ALL}\n")
        sys.exit(1)
