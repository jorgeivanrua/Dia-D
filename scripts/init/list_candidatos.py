#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app import create_app
from backend.database import db
from backend.models.candidato import Candidato
from backend.models.partido_politico import PartidoPolitico as Partido
from backend.models.configuracion_electoral import TipoEleccion

def main():
    app = create_app()
    out_path = os.path.join(os.path.dirname(__file__), 'candidatos_list.txt')
    with app.app_context():
        candidatos = Candidato.query.order_by(Candidato.id).limit(100).all()
        lines = []
        for i, c in enumerate(candidatos, start=1):
            partido = Partido.query.get(c.partido_id)
            tipo = TipoEleccion.query.get(c.tipo_eleccion_id)
            partido_sigla = partido.sigla if partido else 'N/A'
            tipo_codigo = tipo.codigo if tipo else 'N/A'
            lines.append(f"{i}. {c.nombre_completo} — Partido: {partido_sigla} — Tipo: {tipo_codigo} \n")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"WROTE {out_path}")

if __name__ == '__main__':
    main()
