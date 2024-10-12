from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional
from src.core.enums.employee_enum.CondicionEnum import CondicionEnum
from src.core.enums.employee_enum.ProfesionEnum import ProfesionEnum
from src.core.enums.employee_enum.PuestoLaboralEnum import PuestoLaboralEnum
class EmployeeForm(FlaskForm):
    """Form para crear o actualizar un Employee"""

    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=50)])
    dni = StringField('DNI', validators=[DataRequired(), Length(max=8)])
    domicilio = StringField('Domicilio', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    localidad = StringField('Localidad', validators=[DataRequired(), Length(max=50)])
    telefono = StringField('Telefono', validators=[DataRequired(), Length(max=50)])
    profesion = SelectField('Profesión', choices=[
        (profesion.name.replace('_',' ').upper()) for profesion in ProfesionEnum], validators=[DataRequired()])
    puesto_laboral = SelectField('Puesto laboral', choices=[
        (puesto_laboral.name.replace('_',' ')
         .upper()) for puesto_laboral in PuestoLaboralEnum], validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de Inicio', format='%Y-%m-%d', validators=[DataRequired()])
    fecha_cese = DateField('Fecha de Cese', format='%Y-%m-%d', validators=[Optional()])
    contacto_emergencia = StringField('Contacto Emergencia', validators=[DataRequired()])
    obra_social = StringField('Obra Social', validators=[DataRequired()])
    nro_afiliado = StringField('Nro Afiliado', validators=[DataRequired()])
    condicion = SelectField('Condicion', choices=[(condicion.name.replace('_',' ')
        .upper()) for condicion in CondicionEnum], validators=[DataRequired()])
    activo = BooleanField('Activo', default=True)