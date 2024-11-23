from core.enums.equestrian_enum import TipoClienteEnum
from flask_wtf import FlaskForm
from wtforms.validators import Optional
from wtforms import StringField, SelectField, RadioField, SubmitField,BooleanField

class EquestrianSearchForm(FlaskForm):
    nombre = StringField("Nombre", validators=[Optional()])
    tipo_de_jya_asignado = SelectField("Tipo de JyA asignado", choices=[("TODOS","Todos")]+[(tipo.name, tipo.name.replace("_"," ").capitalize()) for tipo in TipoClienteEnum],default="TODOS", validators=[Optional()]) 
    order_by = SelectField("Ordenar por", choices=[
        ('nombre', 'Nombre'),
        ('fecha_nacimiento', 'Fecha nacimiento'),
        ('fecha_ingreso', 'Fecha ingreso')
    ],validators=[Optional()])
    ascending = RadioField('Orden',choices=[('1', 'Ascendente'), ('0', 'Descendente')], default='1', validators=[Optional()])
    deleted = BooleanField('Mostrar eliminados', default=False)
    submit = SubmitField('Buscar JyA')