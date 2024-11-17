from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, RadioField
from wtforms.validators import Optional
from src.core.enums.employee_enum.PuestoLaboralEnum import PuestoLaboralEnum

class SearchEmployeeForm(FlaskForm):
    """Form para busqueda de empleados"""

    nombre = StringField('Nombre', validators=[Optional()])
    apellido = StringField('Apellido', validators=[Optional()])
    dni = StringField('DNI', validators=[Optional()])
    email = StringField('Email', validators=[Optional()])
    puesto_laboral = SelectField('Puesto Laboral',
        choices=[('', 'No filtrar')] + [
        (puesto_laboral.name, puesto_laboral.name.replace('_',' ').upper()) for puesto_laboral in PuestoLaboralEnum])

    order_by = SelectField('Ordenar por', choices=[
        ('nombre', 'Nombre'),
        ('apellido', 'Apellido'),
        ('created_at', 'Fecha de creación')
    ], validators=[Optional()])

    ascending = RadioField('Orden ascendente',choices=[('1', 'Ascendente'), ('0', 'Descendente')], default='1')
    submit = SubmitField('Buscar empleados')