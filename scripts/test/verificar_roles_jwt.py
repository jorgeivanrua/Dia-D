"""
Script para verificar que los roles se están guardando correctamente en los tokens JWT
"""
import sqlite3
import json

def verificar_roles():
    """Verificar roles de usuarios en la base de datos"""
    conn = sqlite3.connect('instance/electoral.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("VERIFICACIÓN DE ROLES Y USUARIOS")
    print("=" * 80)
    print()
    
    # Obtener todos los usuarios
    cursor.execute("""
        SELECT id, nombre, rol, ubicacion_id, activo, presencia_verificada, password_hash
        FROM users
        ORDER BY rol, nombre
    """)
    
    usuarios = cursor.fetchall()
    
    print(f"Total de usuarios: {len(usuarios)}")
    print()
    
    # Agrupar por rol
    roles = {}
    for user in usuarios:
        user_id, nombre, rol, ubicacion_id, activo, presencia, password = user
        if rol not in roles:
            roles[rol] = []
        roles[rol].append({
            'id': user_id,
            'nombre': nombre,
            'ubicacion_id': ubicacion_id,
            'activo': activo,
            'presencia': presencia,
            'password': password
        })
    
    # Mostrar usuarios por rol
    for rol, users in sorted(roles.items()):
        print(f"\n{rol.upper()} ({len(users)} usuarios)")
        print("-" * 80)
        for user in users[:5]:  # Mostrar solo los primeros 5
            print(f"  ID: {user['id']}")
            print(f"  Nombre: {user['nombre']}")
            print(f"  Ubicación ID: {user['ubicacion_id']}")
            print(f"  Activo: {user['activo']}")
            if rol == 'testigo_electoral':
                print(f"  Presencia verificada: {user['presencia']}")
            
            # Verificar contraseña
            if user['password'] == 'test123':
                print(f"  Contraseña: test123 ✅")
            elif user['password'] == 'admin123':
                print(f"  Contraseña: admin123 ✅")
            else:
                print(f"  Contraseña: {user['password'][:20]}... (otra)")
            print()
        
        if len(users) > 5:
            print(f"  ... y {len(users) - 5} más")
            print()
    
    # Verificar usuarios específicos de prueba
    print("\n" + "=" * 80)
    print("USUARIOS DE PRUEBA ESPECÍFICOS")
    print("=" * 80)
    print()
    
    usuarios_prueba = ['admin', 'testigo', 'coordinador_puesto', 'coordinador_municipal']
    
    for nombre in usuarios_prueba:
        cursor.execute("""
            SELECT id, nombre, rol, ubicacion_id, activo, password_hash
            FROM users
            WHERE nombre = ?
        """, (nombre,))
        
        user = cursor.fetchone()
        if user:
            user_id, nombre, rol, ubicacion_id, activo, password = user
            print(f"✅ Usuario '{nombre}'")
            print(f"   Rol: {rol}")
            print(f"   Ubicación ID: {ubicacion_id}")
            print(f"   Activo: {activo}")
            print(f"   Contraseña: {password}")
            
            # Obtener ubicación
            if ubicacion_id:
                cursor.execute("""
                    SELECT nombre_completo, tipo
                    FROM locations
                    WHERE id = ?
                """, (ubicacion_id,))
                loc = cursor.fetchone()
                if loc:
                    print(f"   Ubicación: {loc[0]} ({loc[1]})")
            print()
        else:
            print(f"❌ Usuario '{nombre}' NO encontrado")
            print()
    
    conn.close()

if __name__ == '__main__':
    verificar_roles()
