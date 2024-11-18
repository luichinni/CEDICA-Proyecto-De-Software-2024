from argon2 import PasswordHasher
from flask import Blueprint
from flask import request
from flask import render_template
from flask import abort
from flask import redirect
from flask import url_for
from flask import flash
from web.forms.auth_forms.login_form import LoginForm
from web.handlers.auth import login_required

from src.core.services.user_service import UserService

from src.core.oauth import oauth

from flask import session

session_bp = Blueprint('auths',__name__,url_prefix='/auths')

@session_bp.route("/",methods=['GET','POST'])
def index():
    form = LoginForm()
    
    if request.method == 'POST':
        form.validate_on_submit()
        
        id_user = UserService.check_user(form.email.data, form.password.data)
    
        if (not id_user):
            return redirect(url_for('auths.index', titulo='Inicio de Sesión!'))

        session["id"] = id_user
        flash('Iniciado Correctamente!','success')
        return redirect('/')
    
    return render_template('auth/login.html',ruta_post=url_for('auths.index'),form=LoginForm(), titulo='Inicio de Sesión!')

@session_bp.get("/logout")
@login_required
def logout():
    del session['id']
    session.clear()
    
    flash('Sesión cerrada correctamente!', 'info')
        
    return redirect(url_for('auths.index'))

@session_bp.route('/login/<string:mode>')
def oauth_login(mode):
    session['login_mode'] = mode # guardo el estado para más tarde

    redirect_uri = url_for('auths.oauth_auth', _external = True)
    
    return oauth.client.google.authorize_redirect(redirect_uri)

@session_bp.route('/oauth')
def oauth_auth():
    token = oauth.client.google.authorize_access_token()
        
    user_info = token['userinfo']
    
    print(user_info.get('email'))
    
    user = UserService.search_users(email=user_info.get('email'), activo=True)[0]

    if session['login_mode'] == "login":        
        if not user:
            flash('Parece que no estás registrado en el sistema!', 'warning')
            return redirect(url_for('auths.index'))
        
        session["id"] = user[0].id
        
        flash('Iniciado Correctamente!','success')
        return redirect('/')
    
    elif session['login_mode'] == "registration":
        if user:
            flash('Parece que ya estás registrado, intenta iniciando sesión!')
            return redirect(url_for('auths.index'))

        del session['login_mode']

        # === Registro sin rol ===
        
