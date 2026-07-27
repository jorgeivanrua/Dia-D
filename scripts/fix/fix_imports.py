"""
Script para actualizar las importaciones de Partido y Candidato
"""
import os
import re

def fix_imports_in_file(filepath):
    """Actualiza las importaciones en un archivo"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Patrón 1: from backend.models.configuracion_electoral import Partido, Candidato
        pattern1 = r'from backend\.models\.configuracion_electoral import Partido, Candidato'
        replacement1 = '''from backend.models.partido_politico import PartidoPolitico as Partido
from backend.models.candidato import Candidato'''
        content = re.sub(pattern1, replacement1, content)
        
        # Patrón 2: from backend.models.configuracion_electoral import ..., Partido, ...
        pattern2 = r'from backend\.models\.configuracion_electoral import ([^P]*)(Partido)([^C]*)(Candidato)'
        def replace2(match):
            before = match.group(1).strip().rstrip(',').strip()
            after = match.group(3).strip().rstrip(',').strip()
            
            parts = []
            if before:
                parts.append(f'from backend.models.configuracion_electoral import {before}')
            parts.append('from backend.models.partido_politico import PartidoPolitico as Partido')
            parts.append('from backend.models.candidato import Candidato')
            
            return '\n'.join(parts)
        
        content = re.sub(pattern2, replace2, content)
        
        # Patrón 3: Solo Partido
        pattern3 = r'from backend\.models\.configuracion_electoral import (.*,\s*)?Partido(\s*,.*)?$'
        def replace3(match):
            before = match.group(1) if match.group(1) else ''
            after = match.group(2) if match.group(2) else ''
            
            before = before.strip().rstrip(',').strip()
            after = after.strip().lstrip(',').strip()
            
            parts = []
            if before:
                parts.append(f'from backend.models.configuracion_electoral import {before}')
            parts.append('from backend.models.partido_politico import PartidoPolitico as Partido')
            if after:
                parts.append(f'from backend.models.configuracion_electoral import {after}')
            
            return '\n'.join(parts)
        
        content = re.sub(pattern3, replace3, content, flags=re.MULTILINE)
        
        # Patrón 4: Solo Candidato
        pattern4 = r'from backend\.models\.configuracion_electoral import (.*,\s*)?Candidato(\s*,.*)?$'
        def replace4(match):
            before = match.group(1) if match.group(1) else ''
            after = match.group(2) if match.group(2) else ''
            
            before = before.strip().rstrip(',').strip()
            after = after.strip().lstrip(',').strip()
            
            parts = []
            if before:
                parts.append(f'from backend.models.configuracion_electoral import {before}')
            parts.append('from backend.models.candidato import Candidato')
            if after:
                parts.append(f'from backend.models.configuracion_electoral import {after}')
            
            return '\n'.join(parts)
        
        content = re.sub(pattern4, replace4, content, flags=re.MULTILINE)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Actualizado: {filepath}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ Error en {filepath}: {e}")
        return False

def main():
    """Procesar todos los archivos Python"""
    count = 0
    for root, dirs, files in os.walk('backend'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                if fix_imports_in_file(filepath):
                    count += 1
    
    print(f"\n✨ Total de archivos actualizados: {count}")

if __name__ == '__main__':
    main()
