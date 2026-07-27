"""
Script para arreglar las importaciones en super_admin.py
"""

with open('backend/routes/super_admin.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Caso 1: Solo Partido
    if 'from backend.models.configuracion_electoral import Partido' in line and 'Candidato' not in line and 'TipoEleccion' not in line:
        indent = len(line) - len(line.lstrip())
        new_lines.append(' ' * indent + 'from backend.models.partido_politico import PartidoPolitico as Partido\n')
    
    # Caso 2: Candidato, Partido, TipoEleccion
    elif 'from backend.models.configuracion_electoral import Candidato, Partido, TipoEleccion' in line:
        indent = len(line) - len(line.lstrip())
        new_lines.append(' ' * indent + 'from backend.models.configuracion_electoral import TipoEleccion\n')
        new_lines.append(' ' * indent + 'from backend.models.partido_politico import PartidoPolitico as Partido\n')
        new_lines.append(' ' * indent + 'from backend.models.candidato import Candidato\n')
    
    # Caso 3: TipoEleccion, Partido, Candidato
    elif 'from backend.models.configuracion_electoral import TipoEleccion, Partido, Candidato' in line:
        indent = len(line) - len(line.lstrip())
        new_lines.append(' ' * indent + 'from backend.models.configuracion_electoral import TipoEleccion\n')
        new_lines.append(' ' * indent + 'from backend.models.partido_politico import PartidoPolitico as Partido\n')
        new_lines.append(' ' * indent + 'from backend.models.candidato import Candidato\n')
    
    # Caso 4: Partido, Candidato, TipoEleccion
    elif 'from backend.models.configuracion_electoral import Partido, Candidato, TipoEleccion' in line:
        indent = len(line) - len(line.lstrip())
        new_lines.append(' ' * indent + 'from backend.models.configuracion_electoral import TipoEleccion\n')
        new_lines.append(' ' * indent + 'from backend.models.partido_politico import PartidoPolitico as Partido\n')
        new_lines.append(' ' * indent + 'from backend.models.candidato import Candidato\n')
    
    else:
        new_lines.append(line)
    
    i += 1

with open('backend/routes/super_admin.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ Archivo super_admin.py actualizado")
