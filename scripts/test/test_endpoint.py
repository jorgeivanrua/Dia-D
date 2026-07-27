"""Script para probar el endpoint de puestos geolocalizados"""
import sqlite3

# Verificar usuarios
conn = sqlite3.connect('instance/electoral.db')
cursor = conn.cursor()

print("Buscando usuario super_admin...")
cursor.execute("SELECT id, nombre, rol FROM users WHERE rol = 'super_admin' LIMIT 1")
user = cursor.fetchone()

if user:
    print(f"Usuario encontrado: ID={user[0]}, Nombre={user[1]}, Rol={user[2]}")
else:
    print("No se encontró usuario super_admin")
    cursor.execute("SELECT id, nombre, rol FROM users LIMIT 5")
    users = cursor.fetchall()
    print("\nPrimeros 5 usuarios:")
    for u in users:
        print(f"  ID={u[0]}, Nombre={u[1]}, Rol={u[2]}")

# Verificar puestos con coordenadas
print("\n" + "="*60)
print("Verificando puestos con coordenadas...")
cursor.execute("""
    SELECT COUNT(*) 
    FROM locations 
    WHERE tipo = 'puesto' 
    AND activo = 1 
    AND latitud IS NOT NULL 
    AND longitud IS NOT NULL
""")
count = cursor.fetchone()[0]
print(f"Puestos con coordenadas: {count}")

if count > 0:
    cursor.execute("""
        SELECT id, puesto_codigo, puesto_nombre, latitud, longitud
        FROM locations 
        WHERE tipo = 'puesto' 
        AND activo = 1 
        AND latitud IS NOT NULL 
        AND longitud IS NOT NULL
        LIMIT 3
    """)
    puestos = cursor.fetchall()
    print("\nPrimeros 3 puestos:")
    for p in puestos:
        print(f"  ID={p[0]}, Código={p[1]}, Nombre={p[2]}, Lat={p[3]}, Lon={p[4]}")

conn.close()
