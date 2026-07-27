"""Script para verificar partidos en la base de datos"""
import sqlite3

conn = sqlite3.connect('instance/electoral.db')
cursor = conn.cursor()

# Contar partidos
cursor.execute('SELECT COUNT(*) FROM partidos_politicos')
total = cursor.fetchone()[0]
print(f'Total partidos en BD: {total}')

if total > 0:
    # Mostrar primeros 5
    cursor.execute('SELECT id, nombre, sigla, activo FROM partidos_politicos LIMIT 5')
    print('\nPrimeros 5 partidos:')
    for p in cursor.fetchall():
        print(f'  ID={p[0]}, Nombre={p[1]}, Sigla={p[2]}, Activo={p[3]}')
else:
    print('\n⚠️ No hay partidos en la base de datos')
    print('Esto explica por qué candidatos no se muestran correctamente')

conn.close()
