"""
Actualizar contraseñas iniciales a `test123` para todos los usuarios
excepto los que tengan rol `super_admin`.

Ejecutar desde la raíz del repo con el venv activado:
  $env:PYTHONPATH = (Get-Location).Path; .venv\Scripts\python.exe scripts\set_initial_passwords.py
"""
from backend.app import create_app
from backend.database import db
from backend.models.user import User


def set_passwords(default_password='test123'):
    app = create_app('default')

    with app.app_context():
        usuarios = User.query.filter(User.rol != 'super_admin').all()
        if not usuarios:
            print('No se encontraron usuarios para actualizar.')
            return 0

        updated = []
        for u in usuarios:
            try:
                u.set_password(default_password)
                updated.append(u.nombre)
            except Exception as e:
                print(f'Error actualizando {u.nombre}: {e}')

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f'Error guardando cambios en DB: {e}')
            return 2

        print(f'Contraseñas actualizadas para {len(updated)} usuarios (excepto super_admin).')
        for n in updated:
            print(' -', n)

        return 0


if __name__ == '__main__':
    import sys
    pwd = 'test123'
    if len(sys.argv) > 1:
        pwd = sys.argv[1]
    exit(set_passwords(pwd))
