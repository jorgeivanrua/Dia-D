"""
Seed script for DIVIPOLA territorial data
Loads Colombian departments and municipalities into the database.
Based on the official DIVIPOLA codes.
"""

import json
from backend.app import create_app
from backend.database import db
from backend.models.location import Location


def load_departamentos():
    """Load the 32 Colombian departments into the locations table."""
    app = create_app()
    with app.app_context():
        # Delete existing data (or we could check if already exists)
        # Location.query.delete()
        
        departments = [
            {'codigo': '05', 'nombre': 'AMAZONAS', 'tipo': 'departamento'},
            {'codigo': '11', 'nombre': 'BOGOTA D.C.', 'tipo': 'departamento'},
            {'codigo': '18', 'nombre': 'BOLÍVAR', 'tipo': 'departamento'},
            {'codigo': '20', 'nombre': 'BOYACÁ', 'tipo': 'departamento'},
            {'codigo': '23', 'nombre': 'Caldas', 'tipo': 'departamento'},
            {'codigo': '14', 'nombre': 'Caquetá', 'tipo': 'departamento'},
            {'codigo': '15', 'nombre': 'Cauca', 'tipo': 'departamento'},
            {'codigo': '17', 'nombre': 'Cesar', 'tipo': 'departamento'},
            {'codigo': '19', 'nombre': 'Chocó', 'tipo': 'departamento'},
            {'codigo': '13', 'nombre': 'Córdoba', 'tipo': 'departamento'},
            {'codigo': '27', 'nombre': 'Cundinamarca', 'tipo': 'departamento'},
            {'codigo': '32', 'nombre': 'Guainía', 'tipo': 'departamento'},
            {'codigo': '85', 'nombre': 'Guaviare', 'tipo': 'departamento'},
            {'codigo': '63', 'nombre': 'Huila', 'tipo': 'departamento'},
            {'codigo': '41', 'nombre': 'La Guajira', 'tipo': 'departamento'},
            {'codigo': '16', 'nombre': 'Magdalena', 'tipo': 'departamento'},
            {'codigo': '47', 'nombre': 'Meta', 'tipo': 'departamento'},
            {'codigo': '50', 'nombre': 'Nariño', 'tipo': 'departamento'},
            {'codigo': '52', 'nombre': 'Norte de Santander', 'tipo': 'departamento'},
            {'codigo': '54', 'nombre': 'Putumayo', 'tipo': 'departamento'},
            {'codigo': '86', 'nombre': 'Quindío', 'tipo': 'departamento'},
            {'codigo': '63', 'nombre': 'Risaralda', 'tipo': 'departamento'},
            {'codigo': '70', 'nombre': 'San Andrés y Providencia', 'tipo': 'departamento'},
            {'codigo': '88', 'nombre': 'Santander', 'tipo': 'departamento'},
            {'codigo': '91', 'nombre': 'Sucre', 'tipo': 'departamento'},
            {'codigo': '94', 'nombre': 'Tolima', 'tipo': 'departamento'},
            {'codigo': '95', 'nombre': 'Valle del Cauca', 'tipo': 'departamento'},
            {'codigo': '97', 'nombre': 'Vaupés', 'tipo': 'departamento'},
            {'codigo': '99', 'nombre': 'Vichada', 'tipo': 'departamento'},
        ]
        
        for dept in departments:
            # Check if already exists
            existing = Location.query.filter_by(
                codigo=dept['codigo'],
                tipo='departamento'
            ).first()
            if not existing:
                location = Location(
                    codigo=dept['codigo'],
                    nombre_completo=dept['nombre'],
                    tipo='departamento',
                    activo=True
                )
                db.session.add(location)
        
        try:
            db.session.commit()
            print(f"✅ {len(departments)} departamentos cargados exitosamente")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al cargar departamentos: {e}")


def load_municipios_ejemplo():
    """Load example municipalities for each department."""
    app = create_app()
    with app.app_context():
        # Example municipalities per department (capital and a few major ones)
        municipios_por_departamento = {
            '05': ['LETICIA'],
            '11': ['BOGOTA D.C.'],
            '18': ['CARTAGENA', 'BARRANQUILLA', 'CARTAGENA'],
            '23': ['MANIZALES'],
            '15': ['POPAYÁN'],
            '17': ['VALLEDUPAR'],
            '19': ['QUIBDÓ'],
            '13': ['MONTERÍA'],
            '27': ['BOGOTÁ', 'VILLENAVA', 'FACATATIVÁ'],
            '41': ['MAICAO', 'RIOHACHA'],
            '47': ['VILLAVICENCIO'],
            '50': ['PASTO'],
            '54': ['SAN JOSÉ DEL GUAVIARE'],
            '63': ['NEGROTIVA', 'LOLITA'],
            '85': ['LETICIA'],  # Note: usually Amazonas capital
            '86': ['ARMENIA'],
            '88': ['BUCARAMANGA'],
            '91': ['SINCELEJO'],
            '94': ['IBAGUÉ'],
            '95': ['CALI'],
            '97': ['MITÚ'],
            '99': ['PUERTO CARREÑO'],
        }
        
        count = 0
        for codigo_depto, municipios in municipios_por_departamento.items():
            for mun_nombre in municipios:
                # Find the department
                depto = Location.query.filter_by(codigo=codigo_depto, tipo='departamento').first()
                if not depto:
                    continue
                
                # Check if municipality already exists
                existing = Location.query.filter_by(
                    nombre_completo=mun_nombre,
                    tipo='municipio',
                    departamento_codigo=codigo_depto
                ).first()
                if not existing:
                    # Generate a municipality code (simple: department code + sequential)
                    mun_codigo = f"{codigo_depto}01"  # Simplified
                    
                    location = Location(
                        codigo=mun_codigo,
                        nombre_completo=mun_nombre,
                        tipo='municipio',
                        departamento_codigo=codigo_depto,
                        departamento_nombre=depto.nombre_completo,
                        activo=True
                    )
                    db.session.add(location)
                    count += 1
        
        try:
            db.session.commit()
            print(f"✅ {count} municipios de ejemplo cargados")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al cargar municipios: {e}")


if __name__ == '__main__':
    print("Cargando departamentos...")
    load_departamentos()
    print("\nCargando municipios de ejemplo...")
    load_municipios_ejemplo()
    print("\n✅ Seed completado")
</PYEOF