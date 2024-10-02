from src.core.models.empleado import Empleado
from src.core.database import db

class RoleService:

    @staticmethod
    def get_empleado_by_email(email):
        return Empleado.query.filter_by(email=email).first()
