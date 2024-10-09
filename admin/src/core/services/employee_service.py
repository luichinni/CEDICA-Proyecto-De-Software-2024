from src.core.models.Employee import Employee
from src.core.database import db
from src.core.admin_data import AdminData
from src.core.models.Employee import ProfesionEnum
from src.core.models.Employee import CondicionEnum
from src.core.models.Employee import PuestoLaboralEnum
from datetime import date

def add_employee(**kwargs):
    """Crea un empleado"""
    employee = Employee(**kwargs)
    db.session.add(employee)
    db.session.commit()
    return employee

def delete_employee(employee_id):
    """Elimina un empleado de manera logica"""
    employee = get_employee_by_id(employee_id)
    if not employee:
        raise ValueError(f"No existe el empleado con id {employee_id} empleado")
    employee.deleted = True
    return employee

def get_employees():
    """Obtiene todos los empleados"""
    employees = Employee.query.all()
    return employees

def update_employee(employee, **kwargs):
    """Actualiza los datos de un empleado"""

    for key, value in kwargs.items():
        if value is not None and getattr(employee, key) != value:
            setattr(employee, key, value)
    db.session.commit()
    return employee

def get_employee_by_id(employee_id):
    employee = Employee.query.filter_by(id=employee_id).first()
    return employee

def get_employee_by_email(email):
    """Busca un empleado por email y lanza un error si no existe."""
    existing_employee = Employee.query.filter_by(email=email).first()
    if existing_employee is None:
        raise ValueError(f"No existe empleado con el email ingresado: '{email}'")
    return existing_employee

def create_admin_employee():
    """Crea un empleado admin con emal del admin si no existe."""
    admin_email = AdminData.email
    add_employee(nombre="admin", email=admin_email, apellido="a", dni="00000000",
    domicilio="a", localidad="a",telefono="1234",profesion=ProfesionEnum.MEDICO,puesto_laboral=PuestoLaboralEnum.DOMADOR,
    fecha_inicio=date(2023, 10, 8),
    fecha_cese =date(2023, 10, 8),
    contacto_emergencia ="a",
    obra_social="a",
    nro_afiliado ="0",
    condicion=CondicionEnum.VOLUNTARIO,
    activo=True)

def create_exaple_employees():
    """Crea un empleados de ejemplo."""
    add_employee(nombre="admin", email="a", apellido="a", dni="00000004",
    domicilio="a", localidad="a",telefono="1234",profesion=ProfesionEnum.MEDICO,puesto_laboral=PuestoLaboralEnum.DOMADOR,
    fecha_inicio=date(2023, 10, 8),
    fecha_cese =date(2023, 10, 8),
    contacto_emergencia ="a",
    obra_social="a",
    nro_afiliado ="0",
    condicion=CondicionEnum.VOLUNTARIO,
    activo=True)
    add_employee(nombre="admin", email="aaa", apellido="a", dni="00000001",
    domicilio="a", localidad="a",telefono="1234",profesion=ProfesionEnum.MEDICO,puesto_laboral=PuestoLaboralEnum.DOMADOR,
    fecha_inicio=date(2023, 10, 8),
    fecha_cese =date(2023, 10, 8),
    contacto_emergencia ="a",
    obra_social="a",
    nro_afiliado ="0",
    condicion=CondicionEnum.VOLUNTARIO,
    activo=True)
    add_employee(nombre="admin", email="bbb", apellido="a", dni="00000002",
    domicilio="a", localidad="a",telefono="1234",profesion=ProfesionEnum.MEDICO,puesto_laboral=PuestoLaboralEnum.DOMADOR,
    fecha_inicio=date(2023, 10, 8),
    fecha_cese =date(2023, 10, 8),
    contacto_emergencia ="a",
    obra_social="a",
    nro_afiliado ="0",
    condicion=CondicionEnum.VOLUNTARIO,
    activo=True)


