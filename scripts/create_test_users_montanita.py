"""
Script para crear usuarios de prueba (admin/coordinadores/testigos)
para el municipio llamado "Montañita".

Ejecutar desde la raíz del repo:
  e:\Dia-D\mvp\.venv\Scripts\python.exe mvp\scripts\create_test_users_montanita.py

El script busca el municipio por nombre (case-insensitive) y crea:
- admin_municipal (si no existe)
- coordinador_municipal (si no existe)
- para cada puesto del municipio: coordinador_puesto (si no existe)
  y testigos hasta completar el número de mesas del puesto.
"""
from backend.app import create_app
from backend.database import db
from backend.models.location import Location
from backend.models.user import User
import secrets
import string


DEFAULT_INIT_PASSWORD = 'test123'


def generar_password_seguro(longitud=12):
    """Por compatibilidad, devuelve la contraseña inicial por defecto.
    Antes se generaban contraseñas aleatorias; ahora la política de pruebas
    usa `test123` como contraseña inicial para todos los usuarios creados
    por los scripts de prueba (excepto `super_admin`).
    """
    return DEFAULT_INIT_PASSWORD


def crear_usuarios_para_municipio(nombre_municipio):
    app = create_app('default')

    with app.app_context():
        # Buscar municipio por nombre (case-insensitive)
        municipio = Location.query.filter(
            Location.tipo == 'municipio',
            Location.municipio_nombre.ilike(f"%{nombre_municipio}%")
        ).first()

        if not municipio:
            print(f"Municipio '{nombre_municipio}' no encontrado.")
            # Mostrar coincidencias cercanas
            posibles = Location.query.filter(Location.tipo == 'municipio').limit(10).all()
            print('Algunos municipios disponibles:')
            for p in posibles:
                print(f" - {p.municipio_nombre} (id={p.id})")
            return 1

        print(f"Municipio encontrado: {municipio.municipio_nombre} (id={municipio.id})")

        creados = []

        # Crear admin_municipal
        admin_existente = User.query.filter_by(rol='admin_municipal', ubicacion_id=municipio.id).first()
        if not admin_existente:
            username = f"admin.mun.{municipio.municipio_codigo}"
            password = generar_password_seguro()
            admin = User(nombre=username, rol='admin_municipal', ubicacion_id=municipio.id, activo=True)
            admin.set_password(password)
            db.session.add(admin)
            creados.append({'rol': 'admin_municipal', 'username': username, 'password': password})
            print(f"Creando admin municipal: {username}")
        else:
            print(f"Admin municipal ya existe: {admin_existente.nombre}")

        # Crear coordinador_municipal
        coord_existente = User.query.filter_by(rol='coordinador_municipal', ubicacion_id=municipio.id).first()
        if not coord_existente:
            username = f"coord.mun.{municipio.municipio_codigo}"
            password = generar_password_seguro()
            coord = User(nombre=username, rol='coordinador_municipal', ubicacion_id=municipio.id, activo=True)
            coord.set_password(password)
            db.session.add(coord)
            creados.append({'rol': 'coordinador_municipal', 'username': username, 'password': password})
            print(f"Creando coordinador municipal: {username}")
        else:
            print(f"Coordinador municipal ya existe: {coord_existente.nombre}")

        # Para cada puesto del municipio: crear coordinador_puesto y testigos
        puestos = Location.query.filter_by(tipo='puesto', departamento_codigo=municipio.departamento_codigo, municipio_codigo=municipio.municipio_codigo).all()

        if not puestos:
            print('No se encontraron puestos en el municipio seleccionado.')
        else:
            for puesto in puestos:
                print(f"Procesando puesto: {puesto.puesto_nombre} (codigo={puesto.puesto_codigo}, id={puesto.id})")

                # coordinador_puesto
                coord_puesto = User.query.filter_by(rol='coordinador_puesto', ubicacion_id=puesto.id).first()
                if not coord_puesto:
                    username = f"coord.puesto.{puesto.puesto_codigo}"
                    password = generar_password_seguro()
                    cp = User(nombre=username, rol='coordinador_puesto', ubicacion_id=puesto.id, activo=True)
                    cp.set_password(password)
                    db.session.add(cp)
                    creados.append({'rol': 'coordinador_puesto', 'username': username, 'password': password, 'puesto_id': puesto.id})
                    print(f"  Creando coordinador de puesto: {username}")
                else:
                    print(f"  Coordinador de puesto ya existe: {coord_puesto.nombre}")

                # contar mesas del puesto
                total_mesas = Location.query.filter_by(tipo='mesa', departamento_codigo=puesto.departamento_codigo, municipio_codigo=puesto.municipio_codigo, zona_codigo=puesto.zona_codigo, puesto_codigo=puesto.puesto_codigo).count()
                # contar testigos existentes con ubicacion_id = puesto.id
                testigos_existentes = User.query.filter_by(rol='testigo_electoral', ubicacion_id=puesto.id).all()
                testigos_existentes_count = len(testigos_existentes)

                cantidad_a_crear = total_mesas - testigos_existentes_count
                if cantidad_a_crear <= 0:
                    print(f"  Ya existen {testigos_existentes_count} testigos (mesas={total_mesas}). Ninguno creado.")
                    continue

                # crear testigos
                for i in range(cantidad_a_crear):
                    numero_testigo = testigos_existentes_count + i + 1
                    username = f"testigo.{puesto.puesto_codigo}.{numero_testigo:02d}"
                    # asegurar unicidad
                    while User.query.filter_by(nombre=username).first():
                        numero_testigo += 1
                        username = f"testigo.{puesto.puesto_codigo}.{numero_testigo:02d}"

                    password = generar_password_seguro()
                    testigo = User(nombre=username, rol='testigo_electoral', ubicacion_id=puesto.id, activo=True)
                    testigo.set_password(password)
                    db.session.add(testigo)
                    creados.append({'rol': 'testigo_electoral', 'username': username, 'password': password, 'puesto_id': puesto.id})
                    print(f"  Creado testigo: {username}")

        # Commit de cambios
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error al guardar en la base de datos: {e}")
            return 2

        print('\nUsuarios creados:')
        for c in creados:
            print(c)

        return 0


if __name__ == '__main__':
    import sys

    nombre = 'montañita'
    if len(sys.argv) > 1:
        nombre = sys.argv[1]

    exit_code = crear_usuarios_para_municipio(nombre)
    sys.exit(exit_code)
