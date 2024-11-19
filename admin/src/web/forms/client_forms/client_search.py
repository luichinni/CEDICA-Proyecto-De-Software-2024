from flask_wtf import FlaskForm
from wtforms.validators import Optional
from wtforms import StringField, SelectField, RadioField, SubmitField, IntegerField, BooleanField

class ClientSearchForm(FlaskForm):
    nombre = StringField("Nombre", validators=[Optional()])
    apellido = StringField("Apellido", validators=[Optional()])
    dni = IntegerField("DNI", validators=[Optional()])
    atendido_por = StringField("Profesionales que lo atienden", validators=[Optional()])
    order_by = SelectField("Ordenar por", choices=[
        ('nombre', 'Nombre'),
        ('apellido', 'Apellido'),
        ('dni', 'DNI')
    ],validators=[Optional()])
    ascending = RadioField('Orden',choices=[('1', 'Ascendente'), ('0', 'Descendente')], default='1', validators=[Optional()])
    deleted = BooleanField('Mostrar eliminados', default=False)
    submit = SubmitField('Buscar JyA')