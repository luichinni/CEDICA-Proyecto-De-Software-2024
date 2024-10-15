from src.core.models.employee import Employee
from src.core.database import db
from src.core.admin_data import AdminData
from src.core.models.employee import ProfesionEnum
from src.core.models.employee import CondicionEnum
from src.core.models.employee import PuestoLaboralEnum
from datetime import date

class EmployeeService:

    @staticmethod
    def add_employee(**kwargs):
        """Crea un empleado"""
        employee = Employee(**kwargs)
        db.session.add(employee)
        db.session.commit()
        return employee
    @staticmethod
    def delete_employee(employee_id):
        """Elimina un empleado de manera logica"""
        employee = EmployeeService.get_employee_by_id(employee_id)
        if not employee:
            raise ValueError(f"No existe el empleado con id {employee_id} empleado")
        employee.deleted = True
        return employee

    @staticmethod
    def get_employees(filtro=None, order_by=None, ascending=True):
        """Obtiene todos los empleados"""
        employees_query = Employee.query
        if filtro:
            employees_query = employees_query.filter_by(**filtro)

        if order_by:
            if ascending:
                employees_query = employees_query.order_by(getattr(Employee, order_by).asc())
            else:
                employees_query = employees_query.order_by(getattr(Employee, order_by).desc())
        return employees_query.all()

    @staticmethod
    def update_employee(employee, **kwargs):
        """Actualiza los datos de un empleado"""

        for key, value in kwargs.items():
            if value is not None and getattr(employee, key) != value:
                setattr(employee, key, value)
        db.session.commit()
        return employee

    @staticmethod
    def get_employee_by_id(employee_id):
        employee = Employee.query.filter_by(id=employee_id).first()
        return employee

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
        EmployeeService.add_employee(nombre="admin", email=admin_email, apellido="a", dni="00000000",
        domicilio="a", localidad="a",telefono="1234",profesion=ProfesionEnum.MEDICO,puesto_laboral=PuestoLaboralEnum.DOMADOR,
        fecha_inicio=date(2023, 10, 8),
        fecha_cese =date(2023, 10, 8),
        contacto_emergencia ="a",
        obra_social="a",
        nro_afiliado ="0",
        condicion=CondicionEnum.VOLUNTARIO,
        activo=True)

    @staticmethod
    def create_exaple_employees():
        """Crea un empleados de ejemplo."""
        EmployeeService.add_employee(nombre="admin", email="a", apellido="a", dni="00000004",
        domicilio="a", localidad="a",telefono="1234",profesion=ProfesionEnum.MEDICO,puesto_laboral=PuestoLaboralEnum.DOMADOR,
        fecha_inicio=date(2023, 10, 8),
        fecha_cese =date(2023, 10, 8),
        contacto_emergencia ="a",
        obra_social="a",
        nro_afiliado ="0",
        condicion=CondicionEnum.VOLUNTARIO,
        activo=True)
        EmployeeService.add_employee(nombre="admin", email="aaa", apellido="a", dni="00000001",
        domicilio="a", localidad="a",telefono="1234",profesion=ProfesionEnum.MEDICO,puesto_laboral=PuestoLaboralEnum.DOMADOR,
        fecha_inicio=date(2023, 10, 8),
        fecha_cese =date(2023, 10, 8),
        contacto_emergencia ="a",
        obra_social="a",
        nro_afiliado ="0",
        condicion=CondicionEnum.VOLUNTARIO,
        activo=True)
        EmployeeService.add_employee(nombre="admin", email="bbb", apellido="a", dni="00000002",
        domicilio="a", localidad="a",telefono="1234",profesion=ProfesionEnum.MEDICO,puesto_laboral=PuestoLaboralEnum.DOMADOR,
        fecha_inicio=date(2023, 10, 8),
        fecha_cese =date(2023, 10, 8),
        contacto_emergencia ="a",
        obra_social="a",
        nro_afiliado ="0",
        condicion=CondicionEnum.VOLUNTARIO,
        activo=True)


