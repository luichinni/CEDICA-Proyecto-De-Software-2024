from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField, SubmitField
from core.enums.message import StatuEnum
from wtforms.validators import Optional

class SearchContactForm(FlaskForm):
    status = SelectField("Estado: ",default="TODOS" ,choices=[(opcion.name, opcion.name.replace('_',' ').capitalize()) for opcion in StatuEnum ]+[('TODOS','Todos')]) 
    order_by = SelectField("Ordenar por: ", choices=[
        ('created_at', 'Fecha de creacion'),
        ('closed_at', 'Fecha de cierre')
    ],validators=[Optional()])
    ascending = RadioField('Orden: ',choices=[('1', 'Ascendente'), ('0', 'Descendente')], default='1', validators=[Optional()])
  
    submit = SubmitField('Aceptar')