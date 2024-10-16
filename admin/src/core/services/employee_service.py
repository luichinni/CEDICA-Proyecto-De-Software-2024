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
    def get_employees(filtro=None, order_by=None, ascending=True, include_deleted=False):
        """Obtiene todos los empleados"""
        employees_query = Employee.query.filter_by(deleted=include_deleted)
        if filtro:
            valid_filters = {key:value for key, value in filtro.items() if hasattr(Employee, key) and value is not None}
            employees_query = employees_query.filter_by(**valid_filters)

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
        """Busca un empleado por su email"""
        employee = Employee.query.filter_by(id=employee_id).first()
        if not employee:
            raise ValueError(f"No se encontro el empleado con id {employee_id}")
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
        """Crea un empleado admin con email del admin si no existe."""
        admin_email = AdminData.email
        EmployeeService.add_employee(nombre="admin", email=admin_email, apellido="a", dni="00000000",
        domicilio="a", localidad="a",telefono="1234",profesion=ProfesionEnum.MEDICO,puesto_laboral=PuestoLaboralEnum.DOMADOR,
        fecha_inicio=date(2023, 10, 8),
        fecha_cese =date(2023, 10, 8),
        contacto_emergencia_nombre ="a",
        contacto_emergencia_telefono = "123",
        obra_social="a",
        nro_afiliado ="0",
        condicion=CondicionEnum.VOLUNTARIO,
        activo=True)

    @staticmethod
    def create_example_employees():
        """Crea un empleados de ejemplo."""

        example_employees = [
            {"nombre" : "admin", "email" : "exa1@example.com", "apellido" : "a", "dni" : "00000004", "domicilio" : "a", "localidad" : "a", "telefono" : "1234", "profesion" : ProfesionEnum.MEDICO, "puesto_laboral" : PuestoLaboralEnum.DOMADOR, "fecha_inicio" : date(2023, 10, 8), "fecha_cese" : date(2023, 10, 8), "contacto_emergencia_nombre" : "a", "contacto_emergencia_telefono" : "1234", "obra_social" : "a", "nro_afiliado" : "0", "condicion" : CondicionEnum.VOLUNTARIO, "activo" : True},
            {"nombre" : "admin", "email" : "exa2@example.com", "apellido" : "a", "dni" : "00000001", "domicilio" : "a", "localidad" : "a", "telefono" : "1234", "profesion" : ProfesionEnum.MEDICO, "puesto_laboral" : PuestoLaboralEnum.DOMADOR, "fecha_inicio" : date(2023, 10, 8), "fecha_cese" : date(2023, 10, 8), "contacto_emergencia_nombre" : "a", "contacto_emergencia_telefono" : "1234", "obra_social" : "a", "nro_afiliado" : "0", "condicion" : CondicionEnum.VOLUNTARIO, "activo" : True},
            {"nombre" : "admin", "email" : "exa3@example.com", "apellido" : "a", "dni" : "00000002", "domicilio" : "a", "localidad" : "a", "telefono" : "1234", "profesion" : ProfesionEnum.MEDICO, "puesto_laboral" : PuestoLaboralEnum.DOMADOR, "fecha_inicio" : date(2023, 10, 8), "fecha_cese" : date(2023, 10, 8), "contacto_emergencia_nombre" : "a", "contacto_emergencia_telefono" : "1234", "obra_social" : "a", "nro_afiliado" : "0", "condicion" : CondicionEnum.VOLUNTARIO, "activo" : True}
        ]
        for employee_data in example_employees:
            EmployeeService.add_employee(**employee_data)


