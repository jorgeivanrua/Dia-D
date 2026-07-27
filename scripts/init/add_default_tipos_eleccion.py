#!/usr/bin/env python3
"""
Script pequeño para agregar tipos de elección por defecto si la tabla está vacía.
Ejecutar: python scripts/init/add_default_tipos_eleccion.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.app import create_app


def main():
    app = create_app()
    with app.app_context():
        from backend.database import db
        from backend.models.configuracion_electoral import TipoEleccion

        if TipoEleccion.query.count() > 0:
            print('Tipos de elección ya existentes, no se hizo nada')
            return

        # Ajustado: cargar solo tipos relevantes para RN testing y diagnóstico
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
        print(f"Se agregaron {len(tipos)} tipos de elección por defecto")


if __name__ == '__main__':
    main()
