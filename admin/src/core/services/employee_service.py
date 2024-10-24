from src.core.models.employee import Employee
from src.core.models.user import User
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
    def get_all_employees(include_admin=False, include_deleted=False):
        """Obtiene todos los roles."""
        query = Employee.query
        if not include_admin:
            query = query.filter(Employee.email != AdminData.email)
        if not include_deleted:
            query = query.filter(Employee.deleted == False)
        return query.all()

    @staticmethod
    def get_employees(filtro=None, order_by=None, ascending=True, include_deleted=False, page=1, per_page=25):
        """Obtiene todos los empleados"""
        employees_query = Employee.query.filter_by(Employee.deleted == include_deleted)
        if filtro:
            valid_filters = {key:value for key, value in filtro.items() if hasattr(Employee, key) and value is not None}
            employees_query = employees_query.filter_by(**valid_filters)

        if order_by:
            if ascending:
                employees_query = employees_query.order_by(getattr(Employee, order_by).asc())
            else:
                employees_query = employees_query.order_by(getattr(Employee, order_by).desc())

        pagination = employees_query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total, pagination.pages
    
    @staticmethod
    def get_employees_without_user():
        """Obtiene todos los empleados que no tienen un usuario asociado o cuyos usuarios están eliminados,
        siempre y cuando no tengan ningún usuario activo."""
        
        # Subconsulta: obtener empleados que tienen usuarios no eliminados
        subquery = Employee.query.join(User).filter(User.deleted == False).with_entities(Employee.id)
        
        # Consulta principal: empleados que no tienen usuario o cuyos usuarios están eliminados
        query = Employee.query.outerjoin(User).filter(
            (Employee.user == None) | (User.deleted == True)
        ).filter(
            Employee.id.notin_(subquery)  # Excluir empleados con usuarios activos
        )
        
        return query.all()

    @staticmethod
    def update_employee(employee, **kwargs):
        """Actualiza los datos de un empleado"""

        for key, value in kwargs.items():
            if value is not None and getattr(employee, key) != value:
                setattr(employee, key, value)
        db.session.commit()
        return employee

    @staticmethod
    def get_employee_by_id(employee_id, include_deleted=False):
        """Busca un empleado por su email"""
        query = Employee.query.filter_by(Employee.id == employee_id)
        if not include_deleted:
            query = query.filter_by(Employee.deleted == include_deleted)
        if not query:
            raise ValueError(f"No se encontro el empleado con id {employee_id}")
        return query.first()

    @staticmethod
    def get_employee_by_email(email, include_deleted=False):
        """Busca un empleado por email y lanza un error si no existe."""
        existing_employee = Employee.query.filter_by(Employee.email == email)
        if not include_deleted:
            existing_employee = existing_employee.filter_by(deleted=False)
        if existing_employee is None:
            raise ValueError(f"No existe empleado con el email ingresado: '{email}'")
        return existing_employee.first()

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


