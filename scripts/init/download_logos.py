"""
Script para descargar logos de partidos y guardarlos localmente
"""
import os
import sys
# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import requests
from backend.app import create_app
from backend.models.partido_politico import PartidoPolitico as Partido
from backend.database import db

def download_logos():
    """Descargar logos de Wikipedia y guardarlos localmente"""
    app = create_app()
    
    with app.app_context():
        # Crear directorio para logos si no existe
        logos_dir = os.path.join('frontend', 'static', 'uploads', 'logos')
        os.makedirs(logos_dir, exist_ok=True)
        
        partidos = Partido.query.filter(Partido.logo_url.isnot(None)).all()
        
        print("=" * 80)
        print("DESCARGANDO LOGOS DE PARTIDOS")
        print("=" * 80)
        
        downloaded = 0
        errors = 0
        
        for partido in partidos:
            try:
                print(f"\n📥 Descargando: {partido.nombre}")
                print(f"   URL: {partido.logo_url}")
                
                # Descargar imagen con User-Agent para evitar 403
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(partido.logo_url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # Generar nombre de archivo
                filename = f"{partido.codigo}.png"
                filepath = os.path.join(logos_dir, filename)
                
                # Guardar imagen
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                # Actualizar URL en BD a ruta local
                partido.logo_url = f"/static/uploads/logos/{filename}"
                
                print(f"   ✅ Guardado: {filepath}")
                downloaded += 1
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                errors += 1
        
        # Guardar cambios en BD
        if downloaded > 0:
            db.session.commit()
            print(f"\n✅ Base de datos actualizada")
        
        print("\n" + "=" * 80)
        print(f"RESUMEN: {downloaded} logos descargados, {errors} errores")
        print("=" * 80)

if __name__ == '__main__':
    download_logos()
