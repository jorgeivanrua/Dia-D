#!/usr/bin/env python3
"""Script to add search_formularios_e14 function to auth.py"""

import sys

FILE_PATH = r'D:\dev\Dia-D\backend\routes\auth.py'

def main():
    # Read the file
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the insertion point: after line 365 (index 364, the except block end)
    # and before line 366 (index 365, first blank line at 0 spaces)
    # The function to insert - using regular string with escaped newlines
    func_lines = [
        "    @auth_bp.route('/e14/search', methods=['POST'])",
        "    @jwt_required()",
        "    def search_formularios_e14():",
        '        """Buscar formularios E-14 por criterios"""',
        "        try:",
        "            user_id = get_jwt_identity()",
        "            user = User.query.get(int(user_id))",
        "            ",
        "            if not user or user.rol != 'testigo_electoral':",
        "                return jsonify({",
        "                    'success': False,",
        "                    'error': 'Solo los testigos pueden buscar formularios'",
        "                }), 403",
        "            ",
        "            data = request.get_json()",
        "            ",
        "            testigo_id = data.get('testigo_id')",
        "            estado = data.get('estado')",
        "            mesa_id = data.get('mesa_id')",
        "            tipo_eleccion_id = data.get('tipo_eleccion_id')",
        "            ",
        "            query = FormularioE14.query",
        "            ",
        "            if testigo_id:",
        "                query = query.filter_by(testigo_id=testigo_id)",
        "            if estado:",
        "                query = query.filter_by(estado=estado)",
        "            if mesa_id:",
        "                query = query.filter_by(mesa_id=mesa_id)",
        "            if tipo_eleccion_id:",
        "                query = query.filter_by(tipo_eleccion_id=tipo_eleccion_id)",
        "            ",
        "            formularios = query.order_by(FormularioE14.created_at.desc()).all()",
        "            ",
        "            formularios_data = []",
        "            for f in formularios:",
        "                mesa = Location.query.get(f.mesa_id)",
        "                testigo = User.query.get(f.testigo_id)",
        "                ",
        "                formularios_data.append({",
        "                    'id': f.id,",
        "                    'mesa_id': f.mesa_id,",
        "                    'mesa_nombre': mesa.nombre_completo if mesa else None,",
        "                    'testigo_id': f.testigo_id,",
        "                    'testigo_nombre': testigo.nombre if testigo else None,",
        "                    'estado': f.estado,",
        "                    'total_votos': f.total_votos,",
        "                    'votos_validos': f.votos_validos,",
        "                    'created_at': f.created_at.isoformat() if f.created_at else None",
        "                })",
        "            ",
        "            return jsonify({",
        "                'success': True,",
        "                'data': {",
        "                    'formularios': formularios_data,",
        "                    'total': len(formularios_data)",
        "                }",
        "            }), 200",
        "        except Exception e:",
        "        return jsonify({",
        "            'success': False,",
        "            'error': str(e)",
        "        }), 500",
    ]
    
    # Insert after line 365 (index 364), so the new function starts at index 365
    # Then add 2 blank lines at the end
    new_lines = lines[:365] + func_lines + ['\n', '\n']
    
    # Write the file
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"Successfully appended search_formularios_e14 function to {FILE_PATH}")
    print(f"Original lines: {len(lines)}, New lines: {len(new_lines)}")


if __name__ == '__main__':
    main()