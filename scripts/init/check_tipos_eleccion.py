#!/usr/bin/env python3
"""
Comprobar la existencia de tipos de elección en la base de datos y llamar al endpoint '/testigo/tipos-eleccion' vía test_client.
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

        tipos = TipoEleccion.query.order_by(TipoEleccion.orden).all()
        print(f"Tipos en DB: {len(tipos)}")
        for t in tipos:
            print(f" - {t.id}: {t.nombre} ({t.codigo})")

        # Intentar llamar al endpoint via test_client (sin JWT no permitirá, pero mostramos el resultado)
        client = app.test_client()
        resp = client.get('/testigo/tipos-eleccion')
        print('\nGET /testigo/tipos-eleccion status:', resp.status_code)
        try:
            print('Body:', resp.get_json())
        except Exception:
            print('No JSON body')


if __name__ == '__main__':
    main()
