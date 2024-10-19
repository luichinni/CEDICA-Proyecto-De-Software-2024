from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional
from src.core.enums.employee_enum.CondicionEnum import CondicionEnum
from src.core.enums.employee_enum.ProfesionEnum import ProfesionEnum
from src.core.enums.employee_enum.PuestoLaboralEnum import PuestoLaboralEnum

class EditEmployeeForm(FlaskForm):
    """Form para crear o actualizar un Employee"""

    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=50)])
    dni = StringField('DNI', validators=[DataRequired(), Length(max=8)])
    domicilio = StringField('Domicilio', validators=[DataRequired(), Length(max=100)])
    localidad = StringField('Localidad', validators=[DataRequired(), Length(max=50)])
    telefono = StringField('Telefono', validators=[DataRequired(), Length(max=50)])
    profesion = SelectField('Profesión', choices=[
        profesion.name.replace('_',' ').title() for profesion in ProfesionEnum], validators=[DataRequired()])
    puesto_laboral = SelectField('Puesto laboral', choices=[
        (puesto_laboral.name.replace('_',' ')
         .title()) for puesto_laboral in PuestoLaboralEnum], validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de inicio', format='%Y-%m-%d', validators=[DataRequired()])
    fecha_cese = DateField('Fecha de cese', format='%Y-%m-%d', validators=[Optional()])
    contacto_emergencia_nombre = StringField('Nombre contacto emergencia', validators=[DataRequired()])
    contacto_emergencia_telefono = StringField('Telefono contacto emergencia', validators=[DataRequired()])
    obra_social = StringField('Obra social', validators=[DataRequired()])
    nro_afiliado = StringField('Nro afiliado', validators=[DataRequired()])
    condicion = SelectField('Condicion', choices=[(condicion.name.replace('_',' ')
        .title()) for condicion in CondicionEnum], validators=[DataRequired()])
    activo = BooleanField('Activo', default=True)