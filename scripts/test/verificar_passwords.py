"""Script para verificar las contraseñas en la BD"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.app import create_app
from backend.models.user import User

app = create_app('development')
with app.app_context():
    users = User.query.all()
    print(f"\nTotal usuarios: {len(users)}\n")
    for user in users:
        print(f"Usuario: {user.nombre}")
        print(f"Rol: {user.rol}")
        print(f"Password: {user.password_hash}")
        print("-" * 50)
