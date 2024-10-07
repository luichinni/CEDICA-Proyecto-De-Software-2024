from functools import wraps
from flask import flash, redirect
import inspect

def handle_error(redirect_url_func):
    """Decorator para manejar ValueError y redirigir a una URL específica."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError as e:
                flash(str(e), "error")
                return redirect(redirect_url_func(*args, **kwargs))
            except Exception as e:  
                flash(f"Ocurrió un error inesperado: {str(e)}", "error") 
                return redirect(redirect_url_func(*args, **kwargs))
        return wrapper
    return decorator

def validate_params(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Obtenemos la lista de nombres de los parámetros de la función original
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()  # Aplica valores por defecto si no fueron pasados

        # Recorremos cada argumento (nombre y valor)
        for param_name, value in bound_args.arguments.items():
            if value is None:
                raise ValueError(f"El parámetro '{param_name}' no puede ser nulo.")
            if (isinstance(value, str) and value.strip() == ''):
                raise ValueError(f"El parámetro '{param_name}' no puede una cadena vacía.")
        
        return func(*args, **kwargs)
    return wrapper