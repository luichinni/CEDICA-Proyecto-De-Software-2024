from src.core.models.employee import Employee
from src.core.database import db
from src.core.admin_data import AdminData

class EmployeeService:

    @staticmethod
    def create_employee(email):  # TODO: DESPUES CAMBIAR CUANDO SE IMPLEMENTE EL EMPLEADO
        """Crea un nuevo empleado."""
        new_employee = Employee(email=email)
        
        # TODO: CHEQUEAR QUE EL EMAIL SEA UNICO CUANDO SE IMPLEMENTE 

        db.session.add(new_employee)
        db.session.commit()
        
        return new_employee


    @staticmethod
    def get_employee_by_email(email):
        """Busca un empleado por email."""
        return Employee.query.filter_by(email=email).first()


    @staticmethod
    def create_admin_employee():
        """Crea un usuario admin con rol de 'System Admin' si no existe."""
        admin_email = AdminData.email
        EmployeeService.create_employee(admin_email)