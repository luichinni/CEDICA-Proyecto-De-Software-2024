from src import operations

def calculate(a, b, operator):
    match operator:
        case '-':
            return operations.subtract(a,b)
        case '/':
            return operations.divide(a, b)
        case _:
            raise ValueError(f"Operador invalido {operator}")




