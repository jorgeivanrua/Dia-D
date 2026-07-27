"""
Script para verificar todos los usuarios y roles del sistema
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location
from backend.database import db
from collections import Counter

def test_usuarios_roles():
    """Verificar todos los usuarios y roles del sistema"""
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("ANÁLISIS COMPLETO DE USUARIOS Y ROLES")
        print("=" * 80)
        print()
        
        # 1. Obtener todos los usuarios
        print("1. USUARIOS EN EL SISTEMA")
        print("-" * 80)
        usuarios = User.query.order_by(User.rol, User.nombre).all()
        
        print(f"Total de usuarios: {len(usuarios)}")
        print()
        
        # 2. Agrupar por rol
        print("2. DISTRIBUCIÓN POR ROL")
        print("-" * 80)
        roles_count = Counter([u.rol for u in usuarios])
        
        for rol, count in sorted(roles_count.items()):
            print(f"  {rol}: {count} usuario(s)")
        
        print()
        
        # 3. Roles definidos en el modelo
        print("3. ROLES DEFINIDOS EN EL SISTEMA")
        print("-" * 80)
        roles_definidos = [
            'super_admin',
            'admin_departamental',
            'admin_municipal',
            'coordinador_departamental',
            'coordinador_municipal',
            'coordinador_puesto',
            'testigo_electoral',
            'auditor_electoral',
            'monitoreo'
        ]
        
        for rol in roles_definidos:
            count = roles_count.get(rol, 0)
            estado = "✅" if count > 0 else "⚠️ "
            print(f"  {estado} {rol}: {count} usuario(s)")
        
        print()
        
        # 4. Detalles de cada usuario
        print("4. DETALLE DE USUARIOS")
        print("-" * 80)
        
        for usuario in usuarios:
            ubicacion = None
            if usuario.ubicacion_id:
                ubicacion = Location.query.get(usuario.ubicacion_id)
            
            print(f"\n{usuario.id}. {usuario.nombre}")
            print(f"   Rol: {usuario.rol}")
            print(f"   Estado: {'🟢 Activo' if usuario.activo else '🔴 Inactivo'}")
            print(f"   Usuario básico: {'Sí' if usuario.es_usuario_basico else 'No'}")
            
            if ubicacion:
                print(f"   Ubicación: {ubicacion.nombre_completo}")
            else:
                print(f"   Ubicación: Sin asignar")
            
            if usuario.ultima_latitud and usuario.ultima_longitud:
                print(f"   Geolocalización: ✅ ({usuario.ultima_latitud}, {usuario.ultima_longitud})")
                if usuario.ultima_geolocalizacion_at:
                    print(f"   Última actualización GPS: {usuario.ultima_geolocalizacion_at}")
            else:
                print(f"   Geolocalización: ❌ No disponible")
            
            if usuario.rol == 'testigo_electoral':
                print(f"   Presencia verificada: {'✅ Sí' if usuario.presencia_verificada else '❌ No'}")
                if usuario.presencia_verificada_at:
                    print(f"   Verificada el: {usuario.presencia_verificada_at}")
            
            if usuario.ultimo_acceso:
                print(f"   Último acceso: {usuario.ultimo_acceso}")
            else:
                print(f"   Último acceso: Nunca")
            
            print(f"   Creado: {usuario.created_at}")
        
        print()
        
        # 5. Usuarios básicos del sistema
        print("5. USUARIOS BÁSICOS DEL SISTEMA")
        print("-" * 80)
        usuarios_basicos = User.query.filter_by(es_usuario_basico=True).all()
        
        if len(usuarios_basicos) > 0:
            print(f"Total: {len(usuarios_basicos)} usuarios básicos")
            print()
            for usuario in usuarios_basicos:
                print(f"  ✅ {usuario.nombre} ({usuario.rol})")
        else:
            print("  ⚠️  No hay usuarios básicos marcados")
            print("  💡 Ejecuta: python scripts/init_system.py")
        
        print()
        
        # 6. Usuarios con geolocalización
        print("6. USUARIOS CON GEOLOCALIZACIÓN")
        print("-" * 80)
        usuarios_geo = User.query.filter(
            User.ultima_latitud.isnot(None),
            User.ultima_longitud.isnot(None)
        ).all()
        
        print(f"Total: {len(usuarios_geo)} usuarios con GPS")
        
        if len(usuarios_geo) > 0:
            print()
            roles_geo = Counter([u.rol for u in usuarios_geo])
            for rol, count in sorted(roles_geo.items()):
                print(f"  {rol}: {count} usuario(s)")
        else:
            print("  ⚠️  Ningún usuario ha compartido su ubicación aún")
        
        print()
        
        # 7. Usuarios por ubicación
        print("7. USUARIOS POR UBICACIÓN")
        print("-" * 80)
        usuarios_con_ubicacion = User.query.filter(
            User.ubicacion_id.isnot(None)
        ).all()
        
        print(f"Total: {len(usuarios_con_ubicacion)} usuarios con ubicación asignada")
        
        if len(usuarios_con_ubicacion) > 0:
            print()
            ubicaciones_count = Counter([u.ubicacion_id for u in usuarios_con_ubicacion])
            for ubicacion_id, count in sorted(ubicaciones_count.items(), key=lambda x: x[1], reverse=True)[:10]:
                ubicacion = Location.query.get(ubicacion_id)
                if ubicacion:
                    print(f"  {ubicacion.nombre_completo}: {count} usuario(s)")
        
        print()
        
        # 8. Estadísticas de seguridad
        print("8. ESTADÍSTICAS DE SEGURIDAD")
        print("-" * 80)
        
        usuarios_bloqueados = User.query.filter(
            User.bloqueado_hasta.isnot(None)
        ).count()
        
        usuarios_con_intentos = User.query.filter(
            User.intentos_fallidos > 0
        ).count()
        
        print(f"  Usuarios bloqueados: {usuarios_bloqueados}")
        print(f"  Usuarios con intentos fallidos: {usuarios_con_intentos}")
        
        print()
        
        # 9. Resumen de capacidades por rol
        print("9. CAPACIDADES POR ROL")
        print("-" * 80)
        
        capacidades = {
            'super_admin': {
                'descripcion': 'Administrador principal del sistema',
                'geolocalización': 'Opcional',
                'dashboard': '/admin/super-admin-dashboard',
                'permisos': 'Todos (crear, editar, eliminar, configurar)'
            },
            'monitoreo': {
                'descripcion': 'Supervisión en tiempo real',
                'geolocalización': 'Solo lectura (ve todos)',
                'dashboard': '/monitoreo/dashboard',
                'permisos': 'Solo lectura (supervisión)'
            },
            'auditor_electoral': {
                'descripcion': 'Auditoría del proceso electoral',
                'geolocalización': 'Activa (envía su ubicación)',
                'dashboard': '/auditor/dashboard',
                'permisos': 'Solo lectura (auditoría)'
            },
            'coordinador_departamental': {
                'descripcion': 'Coordinación a nivel departamental',
                'geolocalización': 'Activa (envía su ubicación)',
                'dashboard': '/coordinador/departamental',
                'permisos': 'Supervisión de su departamento'
            },
            'coordinador_municipal': {
                'descripcion': 'Coordinación a nivel municipal',
                'geolocalización': 'Activa (envía su ubicación)',
                'dashboard': '/coordinador/municipal',
                'permisos': 'Supervisión de su municipio'
            },
            'coordinador_puesto': {
                'descripcion': 'Coordinación de puesto de votación',
                'geolocalización': 'Activa (envía su ubicación)',
                'dashboard': '/coordinador/puesto',
                'permisos': 'Supervisión de su puesto'
            },
            'testigo_electoral': {
                'descripcion': 'Testigo en mesa de votación',
                'geolocalización': 'Activa (envía su ubicación)',
                'dashboard': '/testigo/dashboard',
                'permisos': 'Registro de votos e incidentes'
            },
            'admin_departamental': {
                'descripcion': 'Administrador departamental',
                'geolocalización': 'Opcional',
                'dashboard': '/admin/departamental',
                'permisos': 'Administración de su departamento'
            },
            'admin_municipal': {
                'descripcion': 'Administrador municipal',
                'geolocalización': 'Opcional',
                'dashboard': '/admin/municipal',
                'permisos': 'Administración de su municipio'
            }
        }
        
        for rol in roles_definidos:
            if rol in capacidades:
                info = capacidades[rol]
                count = roles_count.get(rol, 0)
                print(f"\n{rol.upper()} ({count} usuario(s))")
                print(f"  Descripción: {info['descripcion']}")
                print(f"  Geolocalización: {info['geolocalización']}")
                print(f"  Dashboard: {info['dashboard']}")
                print(f"  Permisos: {info['permisos']}")
        
        print()
        
        # 10. Resumen final
        print("=" * 80)
        print("RESUMEN FINAL")
        print("=" * 80)
        
        print(f"\n📊 ESTADÍSTICAS GENERALES:")
        print(f"  • Total de usuarios: {len(usuarios)}")
        print(f"  • Usuarios activos: {sum(1 for u in usuarios if u.activo)}")
        print(f"  • Usuarios inactivos: {sum(1 for u in usuarios if not u.activo)}")
        print(f"  • Usuarios básicos: {len(usuarios_basicos)}")
        print(f"  • Usuarios con ubicación: {len(usuarios_con_ubicacion)}")
        print(f"  • Usuarios con GPS: {len(usuarios_geo)}")
        
        print(f"\n🎭 ROLES:")
        print(f"  • Roles definidos: {len(roles_definidos)}")
        print(f"  • Roles en uso: {len(roles_count)}")
        print(f"  • Roles sin usuarios: {len([r for r in roles_definidos if r not in roles_count])}")
        
        print(f"\n🗺️  GEOLOCALIZACIÓN:")
        print(f"  • Roles con geolocalización activa: 5")
        print(f"    - testigo_electoral")
        print(f"    - coordinador_puesto")
        print(f"    - coordinador_municipal")
        print(f"    - coordinador_departamental")
        print(f"    - auditor_electoral")
        print(f"  • Roles con geolocalización pasiva: 2")
        print(f"    - monitoreo (solo lectura)")
        print(f"    - super_admin (opcional)")
        
        print()
        print("=" * 80)
        
        # 11. Recomendaciones
        print("\n📋 RECOMENDACIONES:")
        print("-" * 80)
        
        if len(usuarios_basicos) < 6:
            print("• Ejecuta 'python scripts/init_system.py' para crear usuarios básicos")
        
        if len(usuarios_geo) == 0:
            print("• Los usuarios deben iniciar sesión y permitir geolocalización")
        
        roles_sin_usuarios = [r for r in roles_definidos if r not in roles_count]
        if roles_sin_usuarios:
            print(f"• Roles sin usuarios: {', '.join(roles_sin_usuarios)}")
        
        print()

if __name__ == '__main__':
    test_usuarios_roles()
