"""
Vuelca cuentas relacionadas con el municipio Montañita y prueba logins.

Genera `mvp/tmp/montanita_users.json` y `mvp/tmp/montanita_users.csv`,
y realiza POST a `/api/auth/login` para una cuenta admin y una cuenta testigo.

Ejecutar desde la raíz del repo con venv activado.
"""
import os
import csv
import json
import urllib.request
import urllib.error
import json as _json

from backend.app import create_app
from backend.database import db
from backend.models.location import Location
from backend.models.user import User


OUTPUT_DIR = os.path.join('mvp', 'tmp')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def find_municipio_by_name(substr='mont'):
    app = create_app('default')
    with app.app_context():
        m = Location.query.filter(Location.tipo == 'municipio', Location.municipio_nombre.ilike(f'%{substr}%')).first()
        return m


def collect_users_for_municipio(municipio):
    app = create_app('default')
    with app.app_context():
        puestos = Location.query.filter_by(tipo='puesto', departamento_codigo=municipio.departamento_codigo, municipio_codigo=municipio.municipio_codigo).all()
        puesto_ids = [p.id for p in puestos]

        usuarios = User.query.filter((User.ubicacion_id == municipio.id) | (User.ubicacion_id.in_(puesto_ids))).all()

        rows = []
        for u in usuarios:
            rows.append({
                'id': u.id,
                'nombre': u.nombre,
                'rol': u.rol,
                'ubicacion_id': u.ubicacion_id,
                'activo': u.activo
            })

        return rows


def save_outputs(rows, municipio):
    json_path = os.path.join(OUTPUT_DIR, f"montanita_users_{municipio.municipio_codigo}.json")
    csv_path = os.path.join(OUTPUT_DIR, f"montanita_users_{municipio.municipio_codigo}.csv")

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'nombre', 'rol', 'ubicacion_id', 'activo'])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    return json_path, csv_path


def test_logins(rows):
    base = 'http://127.0.0.1:5000'
    login_url = base + '/api/auth/login'
    results = []

    # pick admin and a testigo if present
    admin = next((r for r in rows if r['rol'] == 'admin_municipal'), None)
    testigo = next((r for r in rows if r['rol'] == 'testigo_electoral'), None)

    for user in (admin, testigo):
        if not user:
            continue
        payload = {'rol': user['rol'], 'password': 'test123'}

        # add location fields when needed
        if user['rol'] in ('admin_municipal', 'coordinador_municipal'):
            # need municipio_codigo
            loc = Location.query.get(user['ubicacion_id'])
            payload['municipio_codigo'] = loc.municipio_codigo
        elif user['rol'] in ('coordinador_puesto', 'testigo_electoral'):
            # need puesto_codigo and optionally zona_codigo
            loc = Location.query.get(user['ubicacion_id'])
            payload['puesto_codigo'] = loc.puesto_codigo
            payload['zona_codigo'] = loc.zona_codigo

        try:
            data = _json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(login_url, data=data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                body = resp.read().decode('utf-8')
                try:
                    body_json = _json.loads(body)
                except Exception:
                    body_json = body
                results.append({'user': user['nombre'], 'status_code': resp.getcode(), 'body': body_json})
        except urllib.error.HTTPError as e:
            try:
                err_body = e.read().decode('utf-8')
                err_json = _json.loads(err_body)
            except Exception:
                err_json = e.reason
            results.append({'user': user['nombre'], 'status_code': e.code, 'body': err_json})
        except Exception as e:
            results.append({'user': user['nombre'], 'error': str(e)})

    return results


def main():
    municipio = find_municipio_by_name('mont')
    if not municipio:
        print('Municipio Montañita no encontrado. Abortando.')
        return 1

    rows = collect_users_for_municipio(municipio)
    json_path, csv_path = save_outputs(rows, municipio)
    print(f'Guardado JSON: {json_path}\nGuardado CSV: {csv_path}')

    # Cargar app context for Location query in test_logins
    from backend.app import create_app as _create
    app = _create('default')
    with app.app_context():
        results = test_logins(rows)

    print('\nResultados de login:')
    for r in results:
        print(r)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
