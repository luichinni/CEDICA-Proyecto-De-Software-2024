from flask import Blueprint
from flask import request
from flask import render_template
from flask import abort
from flask import redirect
from flask import url_for
from flask import flash

from src.core.services.user_service import UserService

session_bp = Blueprint('auth',__name__,url_prefix='/auth')

@session_bp.get("/")
def index():
    return render_template('auth/login.html')
    
@session_bp.post("/")
def login():
    datos = request.form
    
    user = UserService.search_users(email=datos['email'],activo=True)[0]
    
    print(user[0].password)
    
    if (user != []):
        flash('Iniciado Correctamente','success')
        return redirect('/')
    
    flash('Comprueba tus datos de sesión!')
    return index()