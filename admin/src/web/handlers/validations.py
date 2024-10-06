from functools import wraps
import inspect

def validate_params(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Obtenemos la lista de nombres de los parámetros de la función original
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()  # Aplica valores por defecto si no fueron pasados

        # Recorremos cada argumento (nombre y valor)
        for param_name, value in bound_args.arguments.items():
            if value is None or (isinstance(value, str) and value.strip() == ''):
                raise ValueError(f"El parámetro '{param_name}' no puede ser nulo ni una cadena vacía.")
        
        return func(*args, **kwargs)
    return wrapper