"""
Script para listar usuarios testigos en la base de datos
Ejecutar: python scripts/listar_testigos.py
"""
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
except ImportError:
    print("❌ Error: SQLAlchemy no está instalado")
    print("   Instalar con: pip install sqlalchemy")
    sys.exit(1)

def get_database_url():
    """Obtener URL de la base de datos"""
    # Usar la ruta absoluta de la base de datos
    return 'sqlite:///C:/Users/Ivan/OneDrive - Fundación ProMITIERRA/Documentos/MVP/mvp/instance/electoral.db'

def listar_testigos():
    """Listar usuarios testigos"""
    print("=" * 80)
    print("USUARIOS TESTIGOS EN LA BASE DE DATOS")
    print("=" * 80)
    print()
    
    # Obtener URL de la BD
    database_url = get_database_url()
    print(f"📊 Conectando a la base de datos...")
    print()
    
    try:
        # Crear engine y sesión
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Verificar conexión
        session.execute(text("SELECT 1"))
        print("✅ Conexión exitosa")
        print()
        
        # Buscar usuarios testigos
        result = session.execute(
            text("""
                SELECT 
                    u.id,
                    u.nombre,
                    u.activo,
                    u.presencia_verificada,
                    l.departamento_nombre,
                    l.municipio_nombre,
                    l.puesto_nombre,
                    l.tipo
                FROM users u
                LEFT JOIN locations l ON u.ubicacion_id = l.id
                WHERE u.rol = 'testigo_electoral'
                ORDER BY u.nombre
            """)
        ).fetchall()
        
        if not result:
            print("⚠️ No se encontraron usuarios testigos")
            return
        
        print(f"✅ {len(result)} testigo(s) encontrado(s):")
        print()
        print("-" * 80)
        
        for row in result:
            user_id, nombre, activo, presencia, depto, muni, puesto, tipo = row
            
            estado = "✅ Activo" if activo else "❌ Inactivo"
            presencia_txt = "✅ Verificada" if presencia else "⚠️ No verificada"
            
            print(f"ID: {user_id}")
            print(f"Usuario: {nombre}")
            print(f"Estado: {estado}")
            print(f"Presencia: {presencia_txt}")
            
            if depto:
                print(f"Ubicación: {depto} - {muni}")
                if puesto:
                    print(f"Puesto: {puesto}")
                print(f"Tipo ubicación: {tipo}")
            else:
                print("Ubicación: No asignada")
            
            print("-" * 80)
        
        print()
        print("💡 Para iniciar sesión usa:")
        print("   Usuario: [nombre del testigo]")
        print("   Contraseña: test123")
        print()
        
        session.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    listar_testigos()
