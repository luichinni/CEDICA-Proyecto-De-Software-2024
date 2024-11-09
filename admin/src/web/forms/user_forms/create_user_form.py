from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp
from src.core.services.role_service import RoleService
from src.core.services.employee_service import EmployeeService

class CreateUserForm(FlaskForm):
    employee_id = SelectField('Empleado', coerce=int, validators=[DataRequired(message="El empleado es requerido.")])
    
    alias = StringField('Alias', validators=[
        DataRequired(message="El alias es requerido."),
        Length(min=4, max=50, message="El alias debe tener entre 4 y 50 caracteres.")
    ])
    
    password = PasswordField('Contraseña', validators=[
        DataRequired(message="La contraseña es requerida."),
        Length(min=8, max=20, message="La contraseña debe tener entre 8 y 20 caracteres."),
        EqualTo('confirm_password', message="Las contraseñas deben coincidir."),
        Regexp(
            regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,20}$',
            message="La contraseña debe tener al menos una letra mayúscula, una letra minúscula y un número."
        )
    ])
    
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message="La confirmación de contraseña es requerida.")
    ])

    role_id = SelectField('Rol', coerce=int, validators=[DataRequired(message="El rol es requerido.")])
    
    activo = BooleanField('Activo')
    
    submit = SubmitField('Crear Usuario')

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        employee_choices = [(e.id, e.email) for e in EmployeeService.get_employees_without_user()]
        if not employee_choices:
            raise ValueError("No hay empleados sin usuario disponibles.")
        
        role_choices = [(r.id, r.name) for r in RoleService.get_all_roles()]
        if not role_choices:
            raise ValueError("No hay roles disponibles.")
        
        
        self.employee_id.choices = employee_choices
        self.role_id.choices = role_choices