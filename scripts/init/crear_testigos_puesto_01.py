#!/usr/bin/env python3
"""
Script para crear testigos de prueba para el Puesto 01 de La Salle
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

def crear_testigos_puesto_01():
    """Crear testigos para el puesto 01"""
    app = create_app()
    
    with app.app_context():
        print("\n=== CREANDO TESTIGOS PARA PUESTO 01 ===\n")
        
        # Buscar el puesto 01 de La Salle (ubicacion_id = 4)
        puesto = Location.query.get(4)
        
        if not puesto:
            print("❌ No se encontró el puesto con ID 4")
            return
        
        print(f"✓ Puesto encontrado: {puesto.puesto_nombre}")
        print(f"  Ubicación ID: {puesto.id}")
        print(f"  Códigos: Dept={puesto.departamento_codigo}, Mun={puesto.municipio_codigo}, Zona={puesto.zona_codigo}, Puesto={puesto.puesto_codigo}")
        
        # Buscar mesas del puesto
        mesas = Location.query.filter_by(
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo,
            puesto_codigo=puesto.puesto_codigo,
            tipo='mesa'
        ).all()
        
        print(f"✓ Mesas encontradas: {len(mesas)}")
        
        # Crear un testigo por cada mesa
        testigos_creados = 0
        for mesa in mesas:
            # Verificar si ya existe un testigo para esta mesa
            testigo_existente = User.query.filter_by(
                nombre=f"Testigo Mesa {mesa.mesa_codigo}",
                rol='testigo_electoral'
            ).first()
            
            if testigo_existente:
                print(f"  - Testigo para mesa {mesa.mesa_codigo} ya existe")
                continue
            
            # Crear testigo
            testigo = User(
                nombre=f"Testigo Mesa {mesa.mesa_codigo}",
                rol='testigo_electoral',
                ubicacion_id=mesa.id,
                activo=True
            )
            testigo.set_password('testigo123')  # Contraseña por defecto
            
            db.session.add(testigo)
            testigos_creados += 1
            print(f"  ✓ Creado: Testigo Mesa {mesa.mesa_codigo}")
        
        db.session.commit()
        
        print(f"\n✓ Se crearon {testigos_creados} testigos nuevos")
        print(f"✓ Total de testigos en el puesto: {len(mesas)}")
        print("\nCredenciales:")
        print("  Usuario: Testigo Mesa 01, Testigo Mesa 02, Testigo Mesa 03")
        print("  Contraseña: testigo123")

if __name__ == '__main__':
    crear_testigos_puesto_01()
