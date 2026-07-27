#!/usr/bin/env python3
"""
Script para aplicar índices de optimización a la base de datos
Ejecutar desde la raíz del proyecto: python scripts/aplicar_indices.py
"""

from backend.app import create_app
from backend.database import db
from sqlalchemy import text
import os

def main():
    print("="*70)
    print("APLICANDO ÍNDICES DE OPTIMIZACIÓN PARA MONITOREO")
    print("="*70)
    
    app = create_app()
    
    with app.app_context():
        # Leer el archivo SQL
        sql_file = os.path.join('scripts', 'crear_indices_monitoreo.sql')
        
        if not os.path.exists(sql_file):
            print(f"❌ Error: No se encontró el archivo {sql_file}")
            return
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Separar por comandos SQL individuales
        commands = []
        current_command = []
        
        for line in sql_content.split('\n'):
            # Ignorar comentarios y líneas vacías
            stripped = line.strip()
            if not stripped or stripped.startswith('--'):
                continue
            
            current_command.append(line)
            
            # Si la línea termina con ;, es el final del comando
            if stripped.endswith(';'):
                commands.append('\n'.join(current_command))
                current_command = []
        
        print(f"\n📋 Se encontraron {len(commands)} comandos SQL para ejecutar\n")
        
        success_count = 0
        error_count = 0
        
        for i, command in enumerate(commands, 1):
            # Extraer el nombre del índice o tabla del comando
            command_preview = command.strip()[:80].replace('\n', ' ')
            
            try:
                db.session.execute(text(command))
                db.session.commit()
                print(f"✅ [{i}/{len(commands)}] Ejecutado: {command_preview}...")
                success_count += 1
            except Exception as e:
                error_msg = str(e)
                # Si el error es porque el índice ya existe, no es crítico
                if 'already exists' in error_msg.lower() or 'duplicate' in error_msg.lower():
                    print(f"⚠️  [{i}/{len(commands)}] Ya existe: {command_preview}...")
                    success_count += 1
                else:
                    print(f"❌ [{i}/{len(commands)}] Error: {command_preview}...")
                    print(f"   Detalle: {error_msg}")
                    error_count += 1
                db.session.rollback()
        
        print("\n" + "="*70)
        print("RESUMEN DE APLICACIÓN DE ÍNDICES")
        print("="*70)
        print(f"\n✅ Comandos exitosos: {success_count}")
        print(f"❌ Comandos con error: {error_count}")
        print(f"📊 Total procesados: {len(commands)}")
        
        if error_count == 0:
            print("\n🎉 ¡Todos los índices se aplicaron correctamente!")
            print("\n📈 Mejoras esperadas:")
            print("   - Consultas simples: 50-80% más rápidas")
            print("   - Consultas con JOIN: 60-90% más rápidas")
            print("   - Dashboard completo: 50-75% más rápido")
        else:
            print(f"\n⚠️  Se encontraron {error_count} errores. Revisa los detalles arriba.")
        
        print("\n" + "="*70)

if __name__ == '__main__':
    main()
