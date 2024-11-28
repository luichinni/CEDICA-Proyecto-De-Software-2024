from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

from src.web.forms.employee_forms.EditEmployeeForm import EditEmployeeForm


class CreateEmployeeForm(EditEmployeeForm):
    """Form para crear o actualizar un Employee"""

    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    submit = SubmitField('Crear Empleado')