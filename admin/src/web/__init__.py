from flask import Flask
from flask import render_template
from web.handlers import error
from src.core import database
from src.core.config import config

from src.core.models.user import User
from src.core.models.employee import Employee
from src.core.models.user.permission import Permission
from src.core.models.user.role_permission import RolePermission
from src.core.models.user.role import Role

from src.core.services.user_service import UserService 
from src.core.services.role_service import RoleService 
from core.services.employee_service import EmployeeService 

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(config[env])
    database.init_app(app)

    @app.route("/")
    def home():
        return render_template("home.html")


    app.register_error_handler(404, error.not_found_error)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()
        database.init(UserService, RoleService, EmployeeService)

    return app