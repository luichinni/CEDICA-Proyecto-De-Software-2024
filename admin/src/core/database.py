from flask_sqlalchemy import SQLAlchemy
#from src.core.services import user_service
#from src.core.services import role_service
#from src.core.services import empleado_service

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

    create_admin()

    print("Listo!")

def create_admin():
    pass
    '''print("Creando empleado admin")
    empleado_service.create_admin_user()

    print("Creando rol system admin")
    role_service.create_admin_user()

    print("Creando user admin del sistema")
    user_service.create_admin_user()'''
    