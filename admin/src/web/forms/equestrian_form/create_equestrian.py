from core.models.equestrian import SexoEnum, TipoClienteEnum
from flask_wtf import FlaskForm
from wtforms import  DateField, StringField, SelectField, RadioField
from wtforms.validators import DataRequired
class EquestrianCreateForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    sexo = SelectField('Sexo', choices=[[(opcion.value, opcion.name.replace('_',' ').capitalize()) for opcion in SexoEnum ]], validators=[DataRequired()])
    raza = StringField('Raza', validators=[DataRequired()])
    pelaje = StringField('Pelaje', validators=[DataRequired()])

    compra = RadioField(choices=['Comprado', 'Donado'])
 
    fecha_nacimiento = DateField('Fecha de Nacimiento', format='%Y-%m-%d', validators=[DataRequired()])

    fecha_ingreso = DateField('Fecha de Ingreso', format='%Y-%m-%d', validators=[DataRequired()])
    sede_asignada = StringField('Sede Asignada', validators=[DataRequired()])
    tipo_de_jya_asignado = SelectField('Tipo de Cliente', 
                    choices=[(opcion.value, opcion.name.replace('_',' ').capitalize()) for opcion in TipoClienteEnum ], validators=[DataRequired()])
