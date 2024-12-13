from core.services.message_service import MessageService
from datetime import datetime
from flask import Blueprint, request, jsonify
from src.web.schemas.publication_schema import publications_schema
from core.services.publication_service import PublicationService
from src.web.handlers import get_int_param, get_bool_param, get_str_param
import base64
import requests
from src.core.bcrypy_and_session import cipher

bp = Blueprint('api',__name__,url_prefix='/api')


@bp.post('/contacto')
def contacto():
    contacto_data = request.json
    #TODO: Procesar contacto_data (Con get_int_param, get_bool_param, get_str_param por ejemplo? O manualmente o con otra cosa)
    try: 
       print("llega al add")
       MessageService.add_message(**contacto_data)
    except Exception as e:
        response = {
            "error": "Datos incorrectos.",
            "message": f"{e}"
        } 
        return jsonify(response),400
       
    else:
        response = {
                "message": "Gracias por ponerte en contacto con nosotros.",
            } 
        return jsonify(response),200

@bp.get('/noticias')
def get_noticias():
    params = request.args

    page = get_int_param(params, 'page', 1, optional=True)
    per_page = get_int_param(params, 'per_page', 10, optional=True)
    start_published_date = get_str_param(params, 'published_from', optional=True)
    end_published_date = get_str_param(params, 'published_to', optional=True)

    filtro = {'status': 'PUBLICADO',
              'author': get_str_param(params, 'author', optional=True),
              'start_published_date': datetime.strptime(start_published_date, '%Y-%m-%d').date() if start_published_date else None,
              'end_published_date': datetime.strptime(end_published_date, '%Y-%m-%d').date() if end_published_date else None,}
    order_by = get_str_param(params, 'order_by', None, optional=True)
    ascending = get_bool_param(params, 'ascending', True, optional=True)

    publications, total, pages = PublicationService.list_publications(filtro=filtro, order_by=order_by, ascending=ascending, page=page, per_page=per_page)


    return jsonify({
        'total': total,
        'pages': pages,
        'current_page': page,
        'per_page': per_page,
        'publications': publications_schema.dump(publications)
    })


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
        word = cipher.generate_word()

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