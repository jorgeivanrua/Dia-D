"""
Migración de datos: agregar tipos de elección por defecto.
Este script puede ejecutarse desde el contexto de la aplicación para poblar la tabla si está vacía.
"""
from datetime import datetime

def run(db, TipoEleccion):
    if TipoEleccion.query.count() > 0:
        print('Tipos de elección ya existentes, omitiendo migración')
        return 0

    # Ajustado para entornos de testing/diagnóstico: eliminar presidenciales/senado/cámara
    tipos = [
        {'codigo': 'GOBERNACION', 'nombre': 'Gobernación', 'orden': 1},
        {'codigo': 'ASAMBLEA', 'nombre': 'Asamblea Departamental', 'orden': 2},
        {'codigo': 'ALCALDIA', 'nombre': 'Alcaldía', 'orden': 3},
        {'codigo': 'CONCEJO', 'nombre': 'Concejo Municipal', 'orden': 4},
        {'codigo': 'EDIL', 'nombre': 'Ediles / Juntas Locales', 'orden': 5},
    ]

    for t in tipos:
        tipo = TipoEleccion(
            codigo=t['codigo'],
            nombre=t['nombre'],
            activo=True,
            orden=t['orden']
        )
        db.session.add(tipo)

    db.session.commit()
    print(f"Migración: se agregaron {len(tipos)} tipos de elección")
    return len(tipos)
