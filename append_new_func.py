#!/usr/bin/env python3
import sys

FILE_PATH = r'D:\dev\Dia-D\backend\routes\auth.py'

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Keep first 365 lines (indices 0-364), which ends at the except block of verificar_presencia
# Then add the new function, then 2 blank lines
new_func = [
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
    "        except Exception as e:",
    "        return jsonify({",
    "            'success': False,",
    "            'error': str(e)",
    "        }), 500",
]

new_lines = lines[:365] + new_func + ['\n', '\n']

with open(FILE_PATH, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Function appended successfully')