from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    """Inicializar la base de datos."""
    db.init_app(app)
    config(app)

    return app

def config(app):
    """Cerrar la session de la base de datos al finalizar el contexto de la app"""
    @app.teardown_appcontext
    def close_session(exception=None):
        db.session.close()
    return app

def reset():
    """Resetea la base de datos"""
    print("Eliminando la base de datos")
    db.drop_all()
    print("Creando la base de datos")
    db.create_all()
    print("Finalizacion del reset de la base de datos!")

def init(UserService, RoleService, EmployeeService):
    """Inicializa la base de datos"""
    print("Creando empleado admin")
    EmployeeService.create_admin_employee()

    print("Creando rol system admin")
    RoleService.create_admin_role()

    print("Creando user admin del sistema")
    UserService.create_admin_user()
    print("Finalizacion de la inicializacion de la base de datos!")

    