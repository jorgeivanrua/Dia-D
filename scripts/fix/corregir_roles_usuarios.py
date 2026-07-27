"""
Script para corregir roles de usuarios y resolver errores 403
"""
import sqlite3
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def corregir_roles():
    """Corregir roles de usuarios en la base de datos"""
    db_path = 'instance/electoral.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=" * 80)
    print("CORRECCIÓN DE ROLES DE USUARIOS")
    print("=" * 80)
    print()
    
    # 1. Verificar estado actual
    print("1. ESTADO ACTUAL")
    print("-" * 80)
    
    cursor.execute("""
        SELECT nombre, rol, activo, password_hash
        FROM users
        WHERE nombre IN ('admin', 'testigo', 'coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental')
        ORDER BY nombre
    """)
    
    usuarios_antes = cursor.fetchall()
    
    if not usuarios_antes:
        print("⚠️ No se encontraron usuarios de prueba")
        print()
    else:
        for nombre, rol, activo, password in usuarios_antes:
            print(f"Usuario: {nombre}")
            print(f"  Rol actual: {rol}")
            print(f"  Activo: {activo}")
            print(f"  Contraseña: {password}")
            print()
    
    # 2. Aplicar correcciones
    print("2. APLICANDO CORRECCIONES")
    print("-" * 80)
    
    correcciones = [
        ('admin', 'super_admin', 'admin123'),
        ('testigo', 'testigo_electoral', 'test123'),
        ('coordinador_puesto', 'coordinador_puesto', 'test123'),
        ('coordinador_municipal', 'coordinador_municipal', 'test123'),
        ('coordinador_departamental', 'coordinador_departamental', 'test123')
    ]
    
    for nombre, rol_correcto, password_correcta in correcciones:
        # Verificar si el usuario existe
        cursor.execute("SELECT id, rol, password_hash FROM users WHERE nombre = ?", (nombre,))
        user = cursor.fetchone()
        
        if user:
            user_id, rol_actual, password_actual = user
            cambios = []
            
            # Verificar si necesita corrección de rol
            if rol_actual != rol_correcto:
                cursor.execute("UPDATE users SET rol = ? WHERE id = ?", (rol_correcto, user_id))
                cambios.append(f"rol: {rol_actual} → {rol_correcto}")
            
            # Verificar si necesita corrección de contraseña
            if password_actual != password_correcta:
                cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_correcta, user_id))
                cambios.append(f"contraseña: actualizada a {password_correcta}")
            
            # Activar usuario si está inactivo
            cursor.execute("SELECT activo FROM users WHERE id = ?", (user_id,))
            activo = cursor.fetchone()[0]
            if not activo:
                cursor.execute("UPDATE users SET activo = 1 WHERE id = ?", (user_id,))
                cambios.append("activado")
            
            if cambios:
                print(f"✅ Usuario '{nombre}' corregido:")
                for cambio in cambios:
                    print(f"   - {cambio}")
            else:
                print(f"✓ Usuario '{nombre}' ya está correcto")
        else:
            print(f"⚠️ Usuario '{nombre}' no encontrado (se debe crear)")
        
        print()
    
    # 3. Commit de cambios
    conn.commit()
    
    # 4. Verificar estado final
    print("3. ESTADO FINAL")
    print("-" * 80)
    
    cursor.execute("""
        SELECT nombre, rol, activo, password_hash
        FROM users
        WHERE nombre IN ('admin', 'testigo', 'coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental')
        ORDER BY nombre
    """)
    
    usuarios_despues = cursor.fetchall()
    
    for nombre, rol, activo, password in usuarios_despues:
        print(f"Usuario: {nombre}")
        print(f"  Rol: {rol}")
        print(f"  Activo: {activo}")
        print(f"  Contraseña: {password}")
        print()
    
    # 5. Resumen
    print("=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print()
    print("✅ Correcciones aplicadas exitosamente")
    print()
    print("IMPORTANTE:")
    print("  1. Todos los usuarios deben cerrar sesión")
    print("  2. Volver a iniciar sesión para obtener nuevos tokens JWT")
    print("  3. Los tokens antiguos tendrán roles incorrectos")
    print()
    
    conn.close()

if __name__ == '__main__':
    try:
        corregir_roles()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
