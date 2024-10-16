from flask import Blueprint
from flask import request
from flask import render_template
from flask import abort
from flask import redirect
from flask import url_for
from flask import flash
from web.forms.auth_forms.login_form import LoginForm

from src.core.services.user_service import UserService

from src.core.bcrypt_y_session import bcrypt

from flask import session

session_bp = Blueprint('auth',__name__,url_prefix='/auth')

@session_bp.get("/")
def index():
    return render_template('form.html',ruta_post=url_for('auth.login'),form=LoginForm())
    
@session_bp.post("/")
def login():
    datos = LoginForm()
    
    id_user = UserService.check_user(datos.email.data, datos.password.data)
    
    if (not id_user):
        return redirect(url_for('auth.index'))

    session["id"] = id_user
    flash('Iniciado Correctamente','success')
    return redirect('/')

@session_bp.get("/logout")
def logout():
    if session.get('id'):
        del session['id']
        session.clear()
    
    flash('Sesión cerrada correctamente!')
    return redirect(url_for('auth.index'))