from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, SubmitField

class SearchForm(FlaskForm):
    busqueda = StringField()
    tipo_filtro = SelectField(choices=[]) # campo que se quiere filtrar con la busqueda
    orden_filtro = SelectField(choices=[]) # campo por el que se quiere ordenar la busqueda, pueden ser iguales o diferentes
    orden = RadioField(choices=['Ascendente', 'Descendente'])
    submit = SubmitField('Aplicar')