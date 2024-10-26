from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional
from src.core.enums.employee_enum.CondicionEnum import CondicionEnum
from src.core.enums.employee_enum.ProfesionEnum import ProfesionEnum
from src.core.enums.employee_enum.PuestoLaboralEnum import PuestoLaboralEnum
from src.web.forms.employee_forms.EditEmployeeForm import EditEmployeeForm

class CreateEmployeeForm(EditEmployeeForm):
    """Form para crear o actualizar un Employee"""

    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])