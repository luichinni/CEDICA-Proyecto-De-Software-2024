from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import Optional, Length, EqualTo, Regexp, ValidationError
from src.core.services.role_service import RoleService

class UpdateUserForm(FlaskForm):
    alias = StringField('Alias', validators=[
        Optional(),
        Length(min=4, max=50, message="El alias debe tener entre 4 y 50 caracteres.")
    ])

    password = PasswordField('Contraseña', validators=[
        Optional(),
        Length(min=8, max=20, message="La contraseña debe tener entre 8 y 20 caracteres."),
        Regexp(
            regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,20}$',
            message="La contraseña debe tener al menos una letra mayúscula, una letra minúscula y un número."
        )
    ])

    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        Optional(),
        EqualTo('password', message="Las contraseñas deben coincidir.")
    ])

    role_id = SelectField('Rol', coerce=int, validators=[Optional()])

    activo = BooleanField('Activo')

    submit = SubmitField('Actualizar Usuario')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        role_choices = [(r.id, r.name) for r in RoleService.get_all_roles()]
        if not role_choices:
            raise ValueError("No hay roles disponibles.")
        
        self.role_id.choices = role_choices