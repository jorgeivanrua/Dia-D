"""
Migración: Agregar restricción única para mesa_id + tipo_eleccion_id
Fecha: 2025-11-25
Descripción: Asegura que cada mesa solo pueda tener un formulario por tipo de elección
"""

from backend.database import db
from backend.app import create_app
from sqlalchemy import text

def upgrade():
    """Agregar restricción única"""
    app = create_app()
    
    with app.app_context():
        try:
            # Primero, eliminar duplicados si existen
            print("🔍 Verificando duplicados...")
            
            # Encontrar duplicados
            query = text("""
                SELECT mesa_id, tipo_eleccion_id, COUNT(*) as count
                FROM formularios_e14
                GROUP BY mesa_id, tipo_eleccion_id
                HAVING COUNT(*) > 1
            """)
            
            result = db.session.execute(query)
            duplicados = result.fetchall()
            
            if duplicados:
                print(f"⚠️  Encontrados {len(duplicados)} grupos de duplicados")
                
                for dup in duplicados:
                    mesa_id, tipo_eleccion_id, count = dup
                    print(f"   Mesa {mesa_id}, Tipo Elección {tipo_eleccion_id}: {count} formularios")
                    
                    # Mantener solo el más reciente, eliminar los demás
                    query_delete = text("""
                        DELETE FROM formularios_e14
                        WHERE id NOT IN (
                            SELECT id FROM (
                                SELECT id
                                FROM formularios_e14
                                WHERE mesa_id = :mesa_id AND tipo_eleccion_id = :tipo_eleccion_id
                                ORDER BY created_at DESC
                                LIMIT 1
                            ) AS subquery
                        )
                        AND mesa_id = :mesa_id
                        AND tipo_eleccion_id = :tipo_eleccion_id
                    """)
                    
                    db.session.execute(query_delete, {
                        'mesa_id': mesa_id,
                        'tipo_eleccion_id': tipo_eleccion_id
                    })
                
                db.session.commit()
                print("✅ Duplicados eliminados")
            else:
                print("✅ No se encontraron duplicados")
            
            # Agregar la restricción única
            print("📝 Agregando restricción única...")
            
            # Verificar si la restricción ya existe
            query_check = text("""
                SELECT constraint_name
                FROM information_schema.table_constraints
                WHERE table_name = 'formularios_e14'
                AND constraint_name = 'uq_mesa_tipo_eleccion'
            """)
            
            result = db.session.execute(query_check)
            exists = result.fetchone()
            
            if exists:
                print("ℹ️  La restricción ya existe")
            else:
                # Crear la restricción
                query_constraint = text("""
                    ALTER TABLE formularios_e14
                    ADD CONSTRAINT uq_mesa_tipo_eleccion
                    UNIQUE (mesa_id, tipo_eleccion_id)
                """)
                
                db.session.execute(query_constraint)
                db.session.commit()
                print("✅ Restricción única agregada exitosamente")
            
            print("\n✅ Migración completada exitosamente")
            
        except Exception as e:
            print(f"\n❌ Error en migración: {str(e)}")
            db.session.rollback()
            raise

def downgrade():
    """Eliminar restricción única"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔄 Eliminando restricción única...")
            
            query = text("""
                ALTER TABLE formularios_e14
                DROP CONSTRAINT IF EXISTS uq_mesa_tipo_eleccion
            """)
            
            db.session.execute(query)
            db.session.commit()
            
            print("✅ Restricción eliminada exitosamente")
            
        except Exception as e:
            print(f"❌ Error al eliminar restricción: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'downgrade':
        downgrade()
    else:
        upgrade()
