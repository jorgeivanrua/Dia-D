#!/usr/bin/env python3
"""
Actualizar `tipos_eleccion` para entornos de testing/diagnóstico:
- Eliminar códigos nacionales no deseados (SENADO, CAMARA, PRESIDENCIAL)
- Asegurar que existan GOBERNACION, ASAMBLEA, ALCALDIA, CONCEJO, EDIL
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

        to_remove = ['SENADO', 'CAMARA', 'PRESIDENCIAL']
        # Asegurar destino para reasignaciones
        destino = TipoEleccion.query.filter_by(codigo='GOBERNACION').first()
        if not destino:
            destino = TipoEleccion(codigo='GOBERNACION', nombre='Gobernación', activo=True, orden=1)
            db.session.add(destino)
            db.session.commit()

        from sqlalchemy import text
        for code in to_remove:
            t = TipoEleccion.query.filter_by(codigo=code).first()
            if t:
                print(f"Reasignando registros de {code} a GOBERNACION y eliminando {code}")
                # Reasignar candidatos
                db.session.execute(
                    text("UPDATE candidatos SET tipo_eleccion_id = :dest WHERE tipo_eleccion_id = :src"),
                    {'dest': destino.id, 'src': t.id}
                )
                # Reasignar formularios_e14
                db.session.execute(
                    text("UPDATE formularios_e14 SET tipo_eleccion_id = :dest WHERE tipo_eleccion_id = :src"),
                    {'dest': destino.id, 'src': t.id}
                )
                db.session.commit()
                db.session.delete(t)
                db.session.commit()

        desired = [
            {'codigo': 'GOBERNACION', 'nombre': 'Gobernación', 'orden': 1},
            {'codigo': 'ASAMBLEA', 'nombre': 'Asamblea Departamental', 'orden': 2},
            {'codigo': 'ALCALDIA', 'nombre': 'Alcaldía', 'orden': 3},
            {'codigo': 'CONCEJO', 'nombre': 'Concejo Municipal', 'orden': 4},
            {'codigo': 'EDIL', 'nombre': 'Ediles / Juntas Locales', 'orden': 5},
        ]

        for d in desired:
            existing = TipoEleccion.query.filter_by(codigo=d['codigo']).first()
            if existing:
                existing.nombre = d['nombre']
                existing.orden = d['orden']
                existing.activo = True
                print(f"Actualizado: {d['codigo']}")
            else:
                tipo = TipoEleccion(codigo=d['codigo'], nombre=d['nombre'], activo=True, orden=d['orden'])
                db.session.add(tipo)
                print(f"Creado: {d['codigo']}")

        db.session.commit()
        print("Sincronización de tipos de elección completada.")


if __name__ == '__main__':
    main()
