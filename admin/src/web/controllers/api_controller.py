import random
import string
from flask import Blueprint, Response, request, jsonify
from src.web.handlers import get_int_param, get_bool_param, get_str_param

import base64
import requests
from src.core.bcrypy_and_session import cipher

bp = Blueprint('api',__name__,url_prefix='/api')

@bp.post('/contacto')
def contacto():
    contacto_data = request.json
    #TODO: Procesar contacto_data (Con get_int_param, get_bool_param, get_str_param por ejemplo? O manualmente o con otra cosa)
    print(contacto_data)
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


def generate_word(length = 6):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

@bp.route('/captcha', methods=['GET','POST'])
def generate_captcha():
    """
    GET
    -----

    Envia como respuesta:
    ```
    {
        captcha: str_base64_captcha_img,
        token: str_encrypted_word
    }
    ```
    El token debe volver junto a la palabra ingresada para comprobar si es una rta válida

    POST
    -----

    Recibe en el cuerpo:
    ```
    {
        token: str_encrypted_word,
        word: str_for_comparison
    }
    ```
    Compara el token desencriptado con la palabra en word.
    Retorna:
    ```
    {
        result: True | False
    }
    ```
    Segun si:
    - Es correcta --> True
    - No es correcta --> False
    """
    captcha_res = {}
    status = 400

    if request.method == 'GET':
        word = generate_word()

        api_res = requests.post(
            "https://api.opencaptcha.io/captcha",
            json={
                "text": word,
                "difficulty": 1,
                "height": 192,
                "width": 512
            },
            headers={
                "Content-Type": "application/json"
            }
        )

        captcha_str = base64.b64encode(api_res.content).decode('utf-8') # base 64 de la foto
        content_type = api_res.headers.get('Content-Type') # tipo de la foto
        img_src = f"data:{content_type};base64,{captcha_str}" # str necesario para src de un <img>

        token_str = cipher.encrypt(word.encode('utf-8')).decode('utf-8')

        captcha_res = {
            "captcha": img_src,
            "token": token_str
        }
        status = 200
    else:
        rta = request.json
        captcha_res['result'] = cipher.compare(rta['word'], rta['token'].encode('utf-8'))
        status = 200
    
    return captcha_res, status