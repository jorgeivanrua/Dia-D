#!/usr/bin/env python3
"""
Script para verificar qué datos hay en la base de datos
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.configuracion_electoral import Partido, Candidato, TipoEleccion

def check_data():
    """Verificar datos en la BD"""
    app = create_app('development')
    
    with app.app_context():
        print("=" * 60)
        print("VERIFICACIÓN DE DATOS EN LA BASE DE DATOS")
        print("=" * 60)
        
        # Usuarios
        total_users = User.query.count()
        active_users = User.query.filter_by(activo=True).count()
        print(f"\n📊 USUARIOS:")
        print(f"   Total: {total_users}")
        print(f"   Activos: {active_users}")
        
        if total_users > 0:
            print(f"\n   Primeros 5 usuarios:")
            for user in User.query.limit(5).all():
                print(f"   - {user.nombre} ({user.rol})")
        
        # Partidos
        total_partidos = Partido.query.count()
        print(f"\n📊 PARTIDOS POLÍTICOS:")
        print(f"   Total: {total_partidos}")
        
        if total_partidos > 0:
            print(f"\n   Todos los partidos:")
            for partido in Partido.query.all():
                print(f"   - {partido.nombre} (Activo: {partido.activo})")
        else:
            print("   ⚠️ No hay partidos en la base de datos")
        
        # Candidatos
        total_candidatos = Candidato.query.count()
        print(f"\n📊 CANDIDATOS:")
        print(f"   Total: {total_candidatos}")
        
        if total_candidatos > 0:
            print(f"\n   Todos los candidatos:")
            for candidato in Candidato.query.all():
                print(f"   - {candidato.nombre} ({candidato.partido.nombre if candidato.partido else 'Sin partido'})")
        else:
            print("   ⚠️ No hay candidatos en la base de datos")
        
        # Tipos de Elección
        total_tipos = TipoEleccion.query.count()
        print(f"\n📊 TIPOS DE ELECCIÓN:")
        print(f"   Total: {total_tipos}")
        
        if total_tipos > 0:
            print(f"\n   Todos los tipos:")
            for tipo in TipoEleccion.query.all():
                print(f"   - {tipo.nombre} (Activo: {tipo.activo})")
        else:
            print("   ⚠️ No hay tipos de elección en la base de datos")
        
        print("\n" + "=" * 60)
        print("RESUMEN")
        print("=" * 60)
        print(f"✓ Usuarios: {total_users}")
        print(f"{'✓' if total_partidos > 0 else '✗'} Partidos: {total_partidos}")
        print(f"{'✓' if total_candidatos > 0 else '✗'} Candidatos: {total_candidatos}")
        print(f"{'✓' if total_tipos > 0 else '✗'} Tipos de Elección: {total_tipos}")
        
        if total_partidos == 0 or total_candidatos == 0 or total_tipos == 0:
            print("\n⚠️ ADVERTENCIA: Faltan datos básicos en la base de datos")
            print("   Ejecuta los scripts de inicialización para cargar los datos")

if __name__ == '__main__':
    check_data()
