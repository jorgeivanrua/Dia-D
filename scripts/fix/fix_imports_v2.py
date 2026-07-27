"""
Script mejorado para actualizar las importaciones
"""
import re

def fix_file(filepath):
    """Arregla las importaciones en un archivo"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Patrón: from backend.models.configuracion_electoral import ... Partido ...
        # Solo reemplazar si está en una línea completa de import
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            if 'from backend.models.configuracion_electoral import' in line:
                # Extraer la indentación
                indent = len(line) - len(line.lstrip())
                indent_str = ' ' * indent
                
                # Extraer los imports
                import_part = line.split('import')[1].strip()
                imports = [i.strip() for i in import_part.split(',')]
                
                # Separar los imports
                other_imports = []
                has_partido = False
                has_candidato = False
                
                for imp in imports:
                    if imp == 'Partido':
                        has_partido = True
                    elif imp == 'Candidato':
                        has_candidato = True
                    else:
                        other_imports.append(imp)
                
                # Reconstruir las líneas
                if other_imports:
                    new_lines.append(f"{indent_str}from backend.models.configuracion_electoral import {', '.join(other_imports)}")
                if has_partido:
                    new_lines.append(f"{indent_str}from backend.models.partido_politico import PartidoPolitico as Partido")
                if has_candidato:
                    new_lines.append(f"{indent_str}from backend.models.candidato import Candidato")
            else:
                new_lines.append(line)
        
        content = '\n'.join(new_lines)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filepath}")
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error en {filepath}: {e}")
        return False

# Archivos a arreglar
files = [
    'backend/routes/testigo.py',
    'backend/routes/super_admin.py'
]

for file in files:
    fix_file(file)

print("\n✨ Completado")
