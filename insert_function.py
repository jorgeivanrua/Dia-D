#!/usr/bin/env python3
"""Script to insert search_formularios_e14 function into auth.py"""

FILE_PATH = r'D:\dev\Dia-D\backend\routes\auth.py'

def main():
    # Read the file
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # The function to insert - following exact same pattern as verificar_presencia
    # Lines 306-365 show the pattern we need to follow
    new_function_lines = [
        # Function decorators and definition (0 spaces like verificar_presencia)
        "@auth_bp.route('/e14/search', methods=['POST'])\n",
        "@jwt_required()\n",
        "def search_formularios_e14():\n",
        # Function docstring (4 spaces)
        '    """Buscar formularios E-14 por criterios"""\n',
        # Try block (4 spaces)
        "    try:\n",
        # Function body (8+ spaces for inner logic)
        "        user_id = get_jwt_identity()\n",
        "        user = User.query.get(int(user_id))\n",
        "        \n",
        "        if not user or user.rol != 'testigo_electoral':\n",
        "            return jsonify({\n",
        "                'success': False,\n",
        "                'error': 'Solo los testigos pueden buscar formularios'\n",
        "            }), 403\n",
        "        \n",
        "        data = request.get_json()\n",
        "        \n",
        "        testigo_id = data.get('testigo_id')\n",
        "        estado = data.get('estado')\n",
        "        mesa_id = data.get('mesa_id')\n",
        "        tipo_eleccion_id = data.get('tipo_eleccion_id')\n",
        "        \n",
        "        query = FormularioE14.query\n",
        "        \n",
        "        if testigo_id:\n",
        "            query = query.filter_by(testigo_id=testigo_id)\n",
        "        if estado:\n",
        "            query = query.filter_by(estado=estado)\n",
        "        if mesa_id:\n",
        "            query = query.filter_by(mesa_id=mesa_id)\n",
        "        if tipo_eleccion_id:\n",
        "            query = query.filter_by(tipo_eleccion_id=tipo_eleccion_id)\n",
        "        \n",
        "        formularios = query.order_by(FormularioE14.created_at.desc()).all()\n",
        "        \n",
        "        formularios_data = []\n",
        "        for f in formularios:\n",
        "            mesa = Location.query.get(f.mesa_id)\n",
        "            testigo = User.query.get(f.testigo_id)\n",
        "            \n",
        "            formularios_data.append({\n",
        "                'id': f.id,\n",
        "                'mesa_id': f.mesa_id,\n",
        "                'mesa_nombre': mesa.nombre_completo if mesa else None,\n",
        "                'testigo_id': f.testigo_id,\n",
        "                'testigo_nombre': testigo.nombre if testigo else None,\n",
        "                'estado': f.estado,\n",
        "                'total_votos': f.total_votos,\n",
        "                'votos_validos': f.votos_validos,\n",
        "                'created_at': f.created_at.isoformat() if f.created_at else None\n",
        "            })\n",
        "        \n",
        "        return jsonify({\n",
        "            'success': True,\n",
        "            'data': {\n",
        "                'formularios': formularios_data,\n",
        "                'total': len(formularios_data)\n",
        "            }\n",
        "        }), 200\n",
        # Except block (4 spaces)
        "    except Exception as e:\n",
        # Except body (8+ spaces)
        "        return jsonify({\n",
        "            'success': False,\n",
        "            'error': str(e)\n",
        "        }), 500\n"
    ]
    
    # Insert after line 365 (index 364), which is the last line of verificar_presencia except block
    # Currently lines 366-368 are blank lines (indices 365-367)
    # We want to insert the new function, then keep the blank lines
    new_lines = lines[:365] + new_function_lines + ['\n', '\n']  # Keep 2 blank lines at end
    
    # Write the file
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"Successfully inserted search_formularios_e14 function")
    print(f"Original lines: {len(lines)}, New lines: {len(new_lines)}")

if __name__ == '__main__':
    main()