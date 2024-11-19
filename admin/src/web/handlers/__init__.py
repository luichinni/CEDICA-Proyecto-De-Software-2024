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

def get_param(params, key, param_type, default=None, optional=False):
    """Obtiene y valida un parámetro del tipo especificado."""
    param = params.get(key)
    value = param.strip() if param else None

    if value:
        if param_type == int and value.isdigit():
            return int(value)
        elif param_type == str and isinstance(value, str) and value.strip() != '':
            return value
        elif param_type == bool:
            if isinstance(value, str) and value.strip() != '':
                if value.lower() in ('true', '1', 'yes', 'on', 'y'):
                    return True
                if value.lower() in ('false', '0', 'no', 'off', 'n'):
                    return False
        raise ValueError(f"El parámetro '{key}' debe ser del tipo {param_type.__name__}")
    
    if optional:
        return default
    raise ValueError(f"El parámetro '{key}' tiene que ser ingresado")


def get_int_param(params, key, default=None, optional=False):
    """Intenta obtener un parámetro como un entero."""
    return get_param(params, key, int, default, optional)


def get_str_param(params, key, default=None, optional=False):
    """Intenta obtener un parámetro como un string."""
    return get_param(params, key, str, default, optional)


def get_bool_param(params, key, default=None, optional=False):
    """Intenta obtener un parámetro como booleano."""
    return get_param(params, key, bool, default, optional)