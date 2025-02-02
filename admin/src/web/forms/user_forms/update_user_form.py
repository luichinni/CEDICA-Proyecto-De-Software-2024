from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import Optional, Length, EqualTo, Regexp, ValidationError
from src.core.models.user.role import Role

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

    def populate_obj(self, user):
        """Rellena el formulario con los datos del usuario existente."""
        self.alias.data = user.alias
        self.role_id.data = user.role_id  # Asumiendo que role_id es un entero
        self.activo.data = user.activo
