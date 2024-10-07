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
    def get_employee_by_id(employee_id):
        """Busca un empleado por id y lanza un error si no existe."""
        existing_employee = Employee.query.get(employee_id)
        if existing_employee is None:
            raise ValueError(f"No existe empleado con el id ingresado: '{employee_id}'")
        return existing_employee
    
    @staticmethod
    def get_employee_by_email(email):
        """Busca un empleado por email y lanza un error si no existe."""
        existing_employee = Employee.query.filter_by(email=email).first()
        if existing_employee is None:
            raise ValueError(f"No existe empleado con el email ingresado: '{email}'")
        return existing_employee


    @staticmethod
    def create_admin_employee():
        """Crea un empleado admin con emal del admin si no existe."""
        admin_email = AdminData.email
        EmployeeService.create_employee(admin_email)

    @staticmethod
    def create_exaple_employees():
        """Crea un empleados de ejemplo."""
        EmployeeService.create_employee("exa1@example.com")
        EmployeeService.create_employee("exa2@example.com")
        EmployeeService.create_employee("exa3@example.com")