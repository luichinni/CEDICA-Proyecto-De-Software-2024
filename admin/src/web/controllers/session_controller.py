from flask import Blueprint
from flask import request
from flask import render_template
from flask import abort
from flask import redirect
from flask import url_for
from flask import flash
from web.forms.auth_forms.login_form import LoginForm

from src.core.services.user_service import UserService

from flask import session

session_bp = Blueprint('auths',__name__,url_prefix='/auths')

@session_bp.route("/",methods=['GET','POST'])
def index():
    form = LoginForm()
    
    if request.method == 'POST':
        form.validate_on_submit()
        
        id_user = UserService.check_user(form.email.data, form.password.data)
    
        if (not id_user):
            return redirect(url_for('auths.index'))

        session["id"] = id_user
        flash('Iniciado Correctamente','success')
        return redirect('/')
    
    return render_template('form.html',ruta_post=url_for('auths.login'),form=LoginForm())

@session_bp.get("/logout")
def logout():
    if session.get('id'):
        del session['id']
        session.clear()
    
    flash('Sesión cerrada correctamente!')
    return redirect(url_for('auths.index'))