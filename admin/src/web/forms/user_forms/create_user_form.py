from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp
from src.core.models.employee import Employee
from src.core.models.user.role import Role

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