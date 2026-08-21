# Script para agregar search_formularios_e14 a auth.py

with open('backend/routes/auth.py', 'r', encoding='utf-8') as f:
    content = f.read()

# New function to add, following exact pattern of verificar_presencia
new_function = '''

    @auth_bp.route('/e14/search', methods=['POST'])
    @jwt_required()
    def search_formularios_e14():
        """Buscar formularios E-14 por criterios"""
        try:
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id))
            
            if not user or user.rol != 'testigo_electoral':
                return jsonify({
                    'success': False,
                    'error': 'Solo los testigos pueden buscar formularios'
                }), 403
            
            data = request.get_json()
            
            # Criterios de búsqueda
            testigo_id = data.get('testigo_id')
            estado = data.get('estado')
            mesa_id = data.get('mesa_id')
            tipo_eleccion_id = data.get('tipo_eleccion_id')
            
            # Construir query base
            query = FormularioE14.query
            
            # Aplicar filtros
            if testigo_id:
                query = query.filter_by(testigo_id=testigo_id)
            if estado:
                query = query.filter_by(estado=estado)
            if mesa_id:
                query = query.filter_by(mesa_id=mesa_id)
            if tipo_eleccion_id:
                query = query.filter_by(tipo_eleccion_id=tipo_eleccion_id)
            
            # Ejecutar búsqueda
            formularios = query.order_by(FormularioE14.created_at.desc()).all()
            
            formularios_data = []
            for f in formularios:
                mesa = Location.query.get(f.mesa_id)
                testigo = User.query.get(f.testigo_id)
                
                formularios_data.append({
                    'id': f.id,
                    'mesa_id': f.mesa_id,
                    'mesa_nombre': mesa.nombre_completo if mesa else None,
                    'testigo_id': f.testigo_id,
                    'testigo_nombre': testigo.nombre if testigo else None,
                    'estado': f.estado,
                    'total_votos': f.total_votos,
                    'votos_validos': f.votos_validos,
                    'created_at': f.created_at.isoformat() if f.created_at else None
                })
            
            return jsonify({
                'success': True,
                'data': {
                    'formularios': formularios_data,
                    'total': len(formularios_data)
                }
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

"""

# Append the new function
new_content = content + new_function

with open('backend/routes/auth.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Function appended successfully')