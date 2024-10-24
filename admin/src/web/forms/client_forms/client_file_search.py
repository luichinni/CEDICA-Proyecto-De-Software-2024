from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, SubmitField

class ClientFileSearchForm(FlaskForm):
    busqueda = StringField()
    tipo_filtro = SelectField(choices=[(campo.replace(' ','_').lower(),campo) for campo in ['Titulo','Tipo','PDF', 'DOC', 'XLS', 'JPEG','Link']]) # campo que se quiere filtrar con la busqueda
    orden_filtro = SelectField(choices=[(campo.replace(' ','_').lower(),campo) for campo in ['Titulo','Tipo','Fecha de carga']]) # campo por el que se quiere ordenar la busqueda, pueden ser iguales o diferentes
    orden = RadioField(choices=['Ascendente', 'Descendente'])
    submit = SubmitField('Aplicar')