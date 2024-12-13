import csv
import json
from flask import Blueprint, request, Response
from io import StringIO

bp = Blueprint('download_csv', __name__, url_prefix='/download_csv')

def download_csv(lista_diccionarios):
    # Obtener todas las claves (keys) de los diccionarios, excepto 'id'
    keys = lista_diccionarios[0].keys()

    # Crear el CSV en una cadena
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=keys, delimiter=';')
    writer.writeheader()
    writer.writerows(lista_diccionarios)
    csv_content = output.getvalue()
    output.close()

    # Configurar la respuesta como archivo descargable
    response = Response(csv_content, mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=reporte.csv'
    return response

@bp.post('/list')
def from_list_of_dictionaries():
    # Obtener los datos enviados como JSON desde el formulario
    lista_diccionarios_json = request.form['data']
    lista_diccionarios_json_transformada = lista_diccionarios_json.replace("'", '"')
    lista_diccionarios = json.loads(lista_diccionarios_json_transformada)

    # Eliminar la columna con la clave "id" de cada diccionario
    for diccionario in lista_diccionarios:
        diccionario.pop('id', None)  # Eliminar la clave 'id' si existe

    return download_csv(lista_diccionarios)



@bp.post('/one')
def from_dictionary():
    # Obtener los datos enviados como JSON desde el formulario
    diccionario_json = request.form['data']
    diccionario_json_transformada = diccionario_json.replace("'", '"')
    diccionario = json.loads(diccionario_json_transformada)
    
    lista_diccionarios = [{"Nombre":nombre, "Cantidad":cantidad} for nombre, cantidad in diccionario.items()]
    lista_diccionarios.sort(key=lambda x: x['Cantidad'], reverse=True)

    return download_csv(lista_diccionarios)
