from core.services.employee_service import EmployeeService
from flask import Blueprint
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from web.forms.auth_forms.login_form import LoginForm
from web.handlers.auth import login_required
from src.core.bcrypy_and_session import cipher


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
    
    try:
        return oauth.client.google.authorize_redirect(redirect_uri)

    except:
        flash("Parece que ocurrió un error, intenta nuevamente más tarde o ingresa utilizando tus credenciales.", "warning")
        return redirect(url_for("auths.index"))

@session_bp.route('/oauth')
def oauth_auth():
    token = oauth.client.google.authorize_access_token()
        
    user_info = token['userinfo']
    
    print(user_info.get('email'))
    
    user = UserService.search_users(email=user_info.get('email'), activo=True)[0]

    mode = session['login_mode']
    del session['login_mode']

    if mode == "login":        
        # Intento de login sin user
        if not user:
            flash('Parece que no estás registrado en el sistema!', 'warning')
            return redirect(url_for('auths.index'))
        
        # Validación si el user ya fue confirmado (en caso de ser necesario)
        try:
            UserService.validate_user_is_confirmed(user)
        except:
            flash('Se paciente, los administradores aun están verificando tu cuenta 📝', "warning")
            return redirect(url_for('auths.index'))

        # Generación de la sesión de usuario
        session["id"] = user[0].id
        
        flash('Iniciado Correctamente!','success')
        return redirect('/')
    
    elif mode == "registration":
        # Intento de registro con usuario existente, confirmado o no
        if user:
            try:
                UserService.validate_user_is_confirmed(user)
                flash('Parece que ya estás registrado, intenta iniciando sesión!', "info")
            except:
                flash('Se paciente, los administradores aun están verificando tu cuenta 📝', "warning")
            
            return redirect(url_for('auths.index'))

        # Intento de crear user para empleado registrado
        try:
            emp = EmployeeService.get_employee_by_email(user_info.get("email")) # lanza excepcion si no existe
            UserService.create_user(emp.id, user_info.get("name"), "1aA"+cipher.generate_word(8), employee_email=user_info.get("email"))
        
        except:
            # Si no se es empleado, se genera un user default
            UserService.create_user(-1, user_info.get("name"), "2aA"+cipher.generate_word(8), employee_email=user_info.get("email"))
        
        finally:
            # Por ultimo se comunica que debe quedar a la espera
            flash("Tu usuario ha quedado a la espera de que un administrador lo valide 📝", "info")
            return redirect(url_for('auths.index'))