import os
from flask import Flask, flash
from flask import render_template
from web.handlers import error
from src.web.handlers.auth import is_authenticated
from src.web.handlers.auth import check_permissions
from src.core import database
from src.core.config import config

from flask_bcrypt import Bcrypt
from flask_session import Session

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField
from wtforms.validators import DataRequired

from src.core.models.user import User
from src.core.models import employee
from src.core.models.user.permission import Permission
from src.core.models.user.role_permission import RolePermission
from src.core.models.user.role import Role
from src.core.models.collection import Collection
from src.core.models.client import Client

from src.core.services.user_service import UserService
from src.core.services.user_service import RoleService
from src.core.services.employee_service import EmployeeService
from src.core.services.permission_service import PermissionService 
from src.core.services.client_service import ClientService

from src.web.controllers.collection_controller import bp as collection_bp
from src.web.controllers.user_controller import bp as users_bp
from src.web.controllers.payment_controller import bp as payment_bp
from web.controllers.employee_controller import bp as employee_bp
from src.web.controllers.session_controller import session_bp

session = Session()
bcrypt = Bcrypt()

from src.web.forms.user_forms.create_user_form import CreateUserForm


class MyForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    submit = SubmitField('Enviar')
    opciones = SelectField('Selecciona una opción', choices=[
            ('opcion1', 'Opción 1'),
            ('opcion2', 'Opción 2'),
            ('opcion3', 'Opción 3')
        ])
def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(config[env])
    database.init_app(app)

    bcrypt.init_app(app)
    session.init_app(app)

    @app.route("/")
    def home():
        print(os.environ.keys())
        return render_template("home.html")

    @app.route("/prueba")
    def prueba():
        return render_template('form.html', form=MyForm() )

    @app.route("/pruebados")
    def pruebados():
        opciones= [
            {"value":"opcion 1",
             "text":"opcion 1"},
             {"value":"opcion 2",
             "text":"opcion 2"},
        ]
        return render_template('search_box.html', opciones_tipo = opciones, opciones = opciones)

    app.register_error_handler(404, error.not_found_error)
    app.register_error_handler(401, error.unauthorized)

    app.register_blueprint(session_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(collection_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(payment_bp)

    #Registrar funcion en jinja
    app.jinja_env.globals.update(is_authenticated = is_authenticated)
    app.jinja_env.globals.update(check_permissions = check_permissions)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()
        database.init(UserService, RoleService, EmployeeService, PermissionService, ClientService)

    return app