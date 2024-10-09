from flask import Flask, render_template
from web.handlers import error
from src.core import database
from src.core.config import config

from src.core.models.user import User
from src.core.models import Employee
from src.core.models.user.permission import Permission
from src.core.models.user.role_permission import RolePermission
from src.core.models.user.role import Role

from src.core.services.user_service import UserService, RoleService
from src.core.services import employee_service
from src.core.services.permission_service import PermissionService 

from src.web.controllers.user_controller import bp as users_bp
from src.web.controllers.employee.employee_controller import bp as employee_bp

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(config[env])
    database.init_app(app)

    @app.route("/")
    def home():
        return render_template("home.html")


    app.register_error_handler(404, error.not_found_error)

    app.register_blueprint(users_bp) 
    app.register_blueprint(employee_bp)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()
        database.init(UserService, RoleService, employee_service, PermissionService)

    return app