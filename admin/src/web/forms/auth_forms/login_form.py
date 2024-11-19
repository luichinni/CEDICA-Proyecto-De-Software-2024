from flask_wtf import FlaskForm
from web.forms.auth_forms.custom_widgets import CustomInput, CustomSubmit
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)], widget=CustomInput("email", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/At_%28CoreUI_Icons_v1.0.0%29.svg/320px-At_%28CoreUI_Icons_v1.0.0%29.svg.png?20200108023110", "Escribe tu email"))
    password = PasswordField('Contraseña', validators=[DataRequired()], widget=CustomInput("password", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Tabler-icons_lock.svg/320px-Tabler-icons_lock.svg.png?20230426212831", "Escribe tu contraseña"))
    submit = SubmitField("",widget=CustomSubmit('Iniciar sesion!'))
