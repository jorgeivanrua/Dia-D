"""
Endpoint para cargar logos de partidos
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from backend.utils.decorators import role_required
from backend.database import db
from backend.models.partido_politico import PartidoPolitico as Partido

cargar_logos_bp = Blueprint('cargar_logos', __name__, url_prefix='/api/admin')

# URLs de logos de partidos políticos colombianos
LOGOS_PARTIDOS = {
    'PARTIDO LIBERAL': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Colombian_Liberal_Party_logo.svg/200px-Colombian_Liberal_Party_logo.svg.png',
    'PARTIDO CONSERVADOR': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Colombian_Conservative_Party_logo.svg/200px-Colombian_Conservative_Party_logo.svg.png',
    'CENTRO DEMOCRÁTICO': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Democratic_Center_%28Colombia%29_logo.svg/200px-Democratic_Center_%28Colombia%29_logo.svg.png',
    'PACTO HISTÓRICO': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Logo_Pacto_Hist%C3%B3rico.svg/200px-Logo_Pacto_Hist%C3%B3rico.svg.png',
    'CAMBIO RADICAL': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Radical_Change_logo.svg/200px-Radical_Change_logo.svg.png',
    'PARTIDO DE LA U': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Social_Party_of_National_Unity_logo.svg/200px-Social_Party_of_National_Unity_logo.svg.png',
    'ALIANZA VERDE': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Green_Alliance_%28Colombia%29_logo.svg/200px-Green_Alliance_%28Colombia%29_logo.svg.png',
    'POLO DEMOCRÁTICO': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Alternative_Democratic_Pole_logo.svg/200px-Alternative_Democratic_Pole_logo.svg.png',
    'MIRA': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/MIRA_logo.svg/200px-MIRA_logo.svg.png',
    'COMUNES': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Comunes_logo.svg/200px-Comunes_logo.svg.png',
    'LIBERAL': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Colombian_Liberal_Party_logo.svg/200px-Colombian_Liberal_Party_logo.svg.png',
    'CONSERVADOR': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Colombian_Conservative_Party_logo.svg/200px-Colombian_Conservative_Party_logo.svg.png',
    'CD': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Democratic_Center_%28Colombia%29_logo.svg/200px-Democratic_Center_%28Colombia%29_logo.svg.png',
    'CR': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Radical_Change_logo.svg/200px-Radical_Change_logo.svg.png',
    'LA U': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Social_Party_of_National_Unity_logo.svg/200px-Social_Party_of_National_Unity_logo.svg.png',
    'VERDE': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Green_Alliance_%28Colombia%29_logo.svg/200px-Green_Alliance_%28Colombia%29_logo.svg.png',
    'POLO': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Alternative_Democratic_Pole_logo.svg/200px-Alternative_Democratic_Pole_logo.svg.png',
}


@cargar_logos_bp.route('/cargar-logos-partidos', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def cargar_logos_partidos():
    """
    Cargar logos de partidos políticos colombianos
    Solo accesible por super_admin
    """
    try:
        partidos = Partido.query.all()
        
        if not partidos:
            return jsonify({
                'success': False,
                'error': 'No hay partidos en la base de datos'
            }), 404
        
        actualizados = []
        sin_cambios = []
        sin_logo = []
        
        for partido in partidos:
            # Buscar logo
            logo_url = None
            nombre_upper = partido.nombre.upper() if partido.nombre else ''
            nombre_corto_upper = partido.nombre_corto.upper() if partido.nombre_corto else ''
            
            # Intentar con nombre exacto
            if nombre_upper in LOGOS_PARTIDOS:
                logo_url = LOGOS_PARTIDOS[nombre_upper]
            
            # Intentar con nombre_corto exacto
            if not logo_url and nombre_corto_upper in LOGOS_PARTIDOS:
                logo_url = LOGOS_PARTIDOS[nombre_corto_upper]
            
            # Intentar búsqueda parcial
            if not logo_url:
                for key, url in LOGOS_PARTIDOS.items():
                    if key in nombre_upper or (len(key) > 3 and nombre_upper in key):
                        logo_url = url
                        break
            
            # Actualizar si encontramos logo y es diferente al actual
            if logo_url:
                if logo_url != partido.logo_url:
                    partido.logo_url = logo_url
                    actualizados.append({
                        'id': partido.id,
                        'nombre': partido.nombre,
                        'logo_url': logo_url
                    })
                else:
                    sin_cambios.append({
                        'id': partido.id,
                        'nombre': partido.nombre
                    })
            else:
                sin_logo.append({
                    'id': partido.id,
                    'nombre': partido.nombre
                })
        
        # Guardar cambios
        if actualizados:
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(actualizados)} logos actualizados exitosamente',
            'data': {
                'actualizados': actualizados,
                'sin_cambios': sin_cambios,
                'sin_logo': sin_logo,
                'total_partidos': len(partidos),
                'total_actualizados': len(actualizados),
                'total_sin_cambios': len(sin_cambios),
                'total_sin_logo': len(sin_logo)
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
