from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, SubmitField

class ClientSearchForm(FlaskForm):
    busqueda = StringField()
    tipo_filtro = SelectField(choices=[(campo.replace(' ','_').lower(),campo) for campo in ['Nombre','Apellido','DNI','Atendido por']]) # campo que se quiere filtrar con la busqueda
    orden_filtro = SelectField(choices=[(campo.replace(' ','_').lower(),campo) for campo in ['Nombre','Apellido','DNI','Atendido por']]) # campo por el que se quiere ordenar la busqueda, pueden ser iguales o diferentes
    orden = RadioField(choices=['Ascendente', 'Descendente'])
    submit = SubmitField('Aplicar')