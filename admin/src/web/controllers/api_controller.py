from flask import Blueprint, request, jsonify
from src.web.handlers import get_int_param, get_bool_param, get_str_param

bp = Blueprint('api',__name__,url_prefix='/api')

@bp.post('/contacto')
def contacto():
    contacto_data = request.json
    #TODO: Procesar contacto_data (Con get_int_param, get_bool_param, get_str_param por ejemplo? O manualmente o con otra cosa)
    
    datos_incorrectos = False #TODO: Implementar esto
    if datos_incorrectos:
        response = {
            "error": "Datos incorrectos.",
        }
        return jsonify(response), 400

    response = {
        "message": "Gracias por ponerte en contacto con nosotros.",
    }
    return jsonify(response), 201


@bp.get('/noticias')
def get_noticias():
    noticias_data = [
        {
            "fecha": "2024-11-01",
            "titulo": "Nueva investigación educativa",
            "copete": "Exploramos nuevas metodologías de enseñanza para mejorar la calidad educativa.",
            "link": "/noticia/1"
        },
        {
            "fecha": "2024-10-15",
            "titulo": "Evento cultural comunitario",
            "copete": "Únete a nosotros para celebrar la diversidad cultural.",
            "link": "/noticia/2"
        }
    ]

    #TODO: Obtener noticias_data de NoticiasService u otro lado

    return jsonify(noticias_data), 200