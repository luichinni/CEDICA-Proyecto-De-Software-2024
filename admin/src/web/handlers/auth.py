from functools import wraps
from flask import session
from flask import abort
from src.core.services.user_service import UserService

def get_current_user_id():
    return session.get("id")

def is_authenticated():
    return get_current_user_id() is not None

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            return abort(401)
        return func(*args, **kwargs)
    return wrapper

def check_permissions(required_permission):
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):
            current_user_id = get_current_user_id()
            if not UserService.user_has_permission(required_permission, current_user_id):
                return abort(401) 
            return func(*args, **kwargs)
        return wrapper
    return decorator

def has_permission(required_permission):
    return UserService.user_has_permission(required_permission, get_current_user_id())

'''
funcion de ejemplo:

@check_permissions("example")
def example_function():
    pass

'''