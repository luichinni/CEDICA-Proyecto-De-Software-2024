from functools import wraps
from flask import session
from flask import abort
from src.core.services.user_service import user_has_permission

def get_current_user_id():
    current_user_id = 0 # TODO: cambiar el 0 por session.get('user_id') cuando se implemente session
    return current_user_id


def is_authenticated(session):
    return get_current_user_id() is not None

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated(session):
            return abort(401)
        return func(*args, **kwargs)
    return wrapper


def check_permissions(required_permission):
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):

            current_user_id = get_current_user_id()
            if not user_has_permission(required_permission, current_user_id):
                return abort(403) 

            return func(*args, **kwargs)
        return wrapper
    return decorator

'''
funcion de ejemplo:

@check_permissions("example")
def example_function():
    pass

'''