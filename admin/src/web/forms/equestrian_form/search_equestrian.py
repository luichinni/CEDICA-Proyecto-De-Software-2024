from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, SubmitField

class EquestriantSearchForm(FlaskForm):
    busqueda = StringField()
    tipo_filtro = SelectField(choices=[(campo.replace(' ','_').lower(),campo) for campo in ['Nombre','Tipo de JyA asignado']]) # campo que se quiere filtrar con la busqueda
    orden_filtro = SelectField(choices=[(campo.replace(' ','_').lower(),campo) for campo in ['Nombre','Fecha nacimiento','Fecha ingreso']]) # campo por el que se quiere ordenar la busqueda, pueden ser iguales o diferentes
    orden = RadioField(choices=['Ascendente', 'Descendente'])
    submit = SubmitField('Aplicar')