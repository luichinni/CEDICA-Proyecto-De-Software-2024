from functools import wraps
from flask import flash, redirect

def handle_value_error(redirect_url_func):
    """Decorator para manejar ValueError y redirigir a una URL específica."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError as e:
                flash(str(e), "error")
                return redirect(redirect_url_func(*args, **kwargs))
        return wrapper
    return decorator
