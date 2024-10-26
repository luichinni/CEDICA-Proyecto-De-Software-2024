from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField
from wtforms.validators import Optional
from src.core.enums.employee_enum.PuestoLaboralEnum import PuestoLaboralEnum

class SearchEmployeeForm(FlaskForm):
    """Form para busqueda de empleados"""

    nombre = StringField('Nombre', validators=[Optional()])
    apellido = StringField('Apellido', validators=[Optional()])
    dni = StringField('DNI', validators=[Optional()])
    email = StringField('Email', validators=[Optional()])
    puesto_laboral = SelectField('Puesto Laboral', choices=[
        (puesto_laboral.name, puesto_laboral.name.replace('_',' ').upper()) for puesto_laboral in PuestoLaboralEnum], validators=[Optional()])
    order_by = SelectField('Ordenar por', choices=[
        ('nombre', 'Nombre'),
        ('apellido', 'Apellido'),
        ('created_at', 'Fecha de creación')
    ], validators=[Optional()])

    ascending = BooleanField('Orden ascendente', default=True)
    submit = SubmitField('Buscar')