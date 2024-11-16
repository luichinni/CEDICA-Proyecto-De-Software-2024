import os
from flask import Flask, flash
from flask import render_template
from flask_cors import CORS
from web.handlers import error
from src.web.handlers.auth import has_permission, is_authenticated
from src.web.handlers.auth import check_permissions
from src.core import database
from src.core.config import config

from src.core.services.user_service import UserService
from src.core.services.user_service import RoleService
from src.core.services.employee_service import EmployeeService
from src.core.services.permission_service import PermissionService 
from src.core.services.client_service import ClientService
from src.core.services.equestrian_service import EquestrianService

from src.web.controllers.collection_controller import bp as collection_bp
from src.web.controllers.user_controller import bp as users_bp
from src.web.controllers.client_controller import clients_bp
from src.web.controllers.client_controller import clients_files_bp
from src.web.controllers.payment_controller import bp as payment_bp
from web.controllers.employee_controller import bp as employee_bp
from src.web.controllers.session_controller import session_bp
from src.web.controllers.equestrian_controller import  bp as equestrians_bp
from src.web.controllers.equestrian_controller import bp_file as equestrian_file_bp
from src.web.controllers.reports_controller import bp as reports_bp
from src.web.controllers.api_controller import bp as api_bp

from src.core.storage import storage
from src.core.bcrypy_and_session import bcrypt, session

from src.core.oauth import oauth

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(config[env])
    database.init_app(app)

    bcrypt.init_app(app)
    session.init_app(app)
    storage.init_app(app)
    oauth.init_app(app)
    CORS(app)

    @app.route("/")
    def home():
        return render_template("home.html")

    app.register_error_handler(404, error.not_found_error)
    app.register_error_handler(401, error.unauthorized)

    app.register_blueprint(session_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(collection_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(clients_files_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(equestrians_bp) 
    app.register_blueprint(equestrian_file_bp)
    app.register_blueprint(reports_bp) 
    app.register_blueprint(api_bp) 

    #Registrar funcion en jinja
    app.jinja_env.globals.update(is_authenticated = is_authenticated)
    app.jinja_env.globals.update(check_permission = has_permission)
    app.jinja_env.globals.update(enumerate = enumerate)
    app.jinja_env.globals.update(google_client_id = lambda: app.config['GOOGLE_CLIENT_ID'])

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()
        database.init(UserService, RoleService, EmployeeService, PermissionService, ClientService, EquestrianService)

    return app