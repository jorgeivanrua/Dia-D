"""
Script de diagnóstico del sistema electoral
Verifica la configuración de usuarios, roles y permisos
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.models.configuracion_electoral import TipoEleccion, Partido, Candidato

def diagnosticar_sistema():
    """Ejecutar diagnóstico completo del sistema"""
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("DIAGNÓSTICO DEL SISTEMA ELECTORAL")
        print("=" * 80)
        print()
        
        # 1. Verificar usuarios
        print("1. USUARIOS DEL SISTEMA")
        print("-" * 80)
        usuarios = User.query.all()
        print(f"Total de usuarios: {len(usuarios)}")
        print()
        
        roles_count = {}
        for user in usuarios:
            roles_count[user.rol] = roles_count.get(user.rol, 0) + 1
        
        print("Usuarios por rol:")
        for rol, count in sorted(roles_count.items()):
            print(f"  - {rol}: {count}")
        print()
        
        # 2. Verificar usuarios de prueba
        print("2. USUARIOS DE PRUEBA")
        print("-" * 80)
        usuarios_prueba = [
            ('admin', 'super_admin'),
            ('testigo', 'testigo_electoral'),
            ('coordinador_puesto', 'coordinador_puesto'),
            ('coordinador_municipal', 'coordinador_municipal'),
            ('coordinador_departamental', 'coordinador_departamental')
        ]
        
        for nombre, rol_esperado in usuarios_prueba:
            user = User.query.filter_by(nombre=nombre).first()
            if user:
                print(f"✅ Usuario '{nombre}' encontrado")
                print(f"   - Rol: {user.rol}")
                print(f"   - Activo: {user.activo}")
                print(f"   - Ubicación ID: {user.ubicacion_id}")
                print(f"   - Presencia verificada: {user.presencia_verificada}")
                
                # Verificar contraseña
                if user.check_password('test123'):
                    print(f"   - Contraseña: test123 ✅")
                elif user.check_password('admin123'):
                    print(f"   - Contraseña: admin123 ✅")
                else:
                    print(f"   - Contraseña: ⚠️ No es test123 ni admin123")
                
                # Verificar ubicación
                if user.ubicacion_id:
                    ubicacion = Location.query.get(user.ubicacion_id)
                    if ubicacion:
                        print(f"   - Ubicación: {ubicacion.nombre_completo} ({ubicacion.tipo})")
                print()
            else:
                print(f"❌ Usuario '{nombre}' NO encontrado")
                print()
        
        # 3. Verificar ubicaciones
        print("3. UBICACIONES")
        print("-" * 80)
        ubicaciones = Location.query.all()
        print(f"Total de ubicaciones: {len(ubicaciones)}")
        print()
        
        tipos_count = {}
        for loc in ubicaciones:
            tipos_count[loc.tipo] = tipos_count.get(loc.tipo, 0) + 1
        
        print("Ubicaciones por tipo:")
        for tipo, count in sorted(tipos_count.items()):
            print(f"  - {tipo}: {count}")
        print()
        
        # 4. Verificar configuración electoral
        print("4. CONFIGURACIÓN ELECTORAL")
        print("-" * 80)
        
        tipos_eleccion = TipoEleccion.query.all()
        print(f"Tipos de elección: {len(tipos_eleccion)}")
        for tipo in tipos_eleccion:
            print(f"  - {tipo.nombre} (activo: {tipo.activo})")
        print()
        
        partidos = Partido.query.all()
        print(f"Partidos políticos: {len(partidos)}")
        for partido in partidos:
            print(f"  - {partido.nombre} (activo: {partido.activo})")
        print()
        
        candidatos = Candidato.query.all()
        print(f"Candidatos: {len(candidatos)}")
        print()
        
        # 5. Verificar testigos con problemas
        print("5. TESTIGOS CON POSIBLES PROBLEMAS")
        print("-" * 80)
        
        testigos = User.query.filter_by(rol='testigo_electoral').all()
        print(f"Total de testigos: {len(testigos)}")
        print()
        
        testigos_sin_ubicacion = [t for t in testigos if not t.ubicacion_id]
        if testigos_sin_ubicacion:
            print(f"⚠️ Testigos sin ubicación: {len(testigos_sin_ubicacion)}")
            for t in testigos_sin_ubicacion[:5]:  # Mostrar solo los primeros 5
                print(f"   - {t.nombre} (ID: {t.id})")
            print()
        
        testigos_inactivos = [t for t in testigos if not t.activo]
        if testigos_inactivos:
            print(f"⚠️ Testigos inactivos: {len(testigos_inactivos)}")
            print()
        
        testigos_con_presencia = [t for t in testigos if t.presencia_verificada]
        print(f"✅ Testigos con presencia verificada: {len(testigos_con_presencia)}")
        print()
        
        # 6. Verificar contraseñas
        print("6. VERIFICACIÓN DE CONTRASEÑAS")
        print("-" * 80)
        
        usuarios_test123 = 0
        usuarios_admin123 = 0
        usuarios_otra = 0
        
        for user in usuarios:
            if user.check_password('test123'):
                usuarios_test123 += 1
            elif user.check_password('admin123'):
                usuarios_admin123 += 1
            else:
                usuarios_otra += 1
        
        print(f"Usuarios con contraseña 'test123': {usuarios_test123}")
        print(f"Usuarios con contraseña 'admin123': {usuarios_admin123}")
        print(f"Usuarios con otra contraseña: {usuarios_otra}")
        print()
        
        if usuarios_otra > 0:
            print("⚠️ ADVERTENCIA: Hay usuarios con contraseñas diferentes a test123/admin123")
            print("   Esto puede causar problemas de autenticación.")
            print()
        
        # 7. Resumen
        print("=" * 80)
        print("RESUMEN DEL DIAGNÓSTICO")
        print("=" * 80)
        
        problemas = []
        
        if usuarios_otra > 0:
            problemas.append(f"⚠️ {usuarios_otra} usuarios con contraseñas no estándar")
        
        if testigos_sin_ubicacion:
            problemas.append(f"⚠️ {len(testigos_sin_ubicacion)} testigos sin ubicación")
        
        if testigos_inactivos:
            problemas.append(f"⚠️ {len(testigos_inactivos)} testigos inactivos")
        
        if not problemas:
            print("✅ No se detectaron problemas críticos")
        else:
            print("Problemas detectados:")
            for problema in problemas:
                print(f"  {problema}")
        
        print()
        print("=" * 80)

if __name__ == '__main__':
    diagnosticar_sistema()
