from flask import render_template, Blueprint, redirect, request, url_for, flash

from app import app
from src.core.services.employee_service import EmployeeService
from web.forms.employee_forms.EmployeeForm import EmployeeForm
from web.forms.employee_forms.SearchEmployeeForm import SearchEmployeeForm
from web.handlers.auth import check_permissions
from web.handlers import handle_error
from src.core.enums.permission_enums import PermissionCategory, PermissionModel

bp = Blueprint('employee_controller', __name__, url_prefix='/employee')

def collect_employee_data_from_form(form):
    """Retorna los datos del form en formato de diccionario"""
    return {
            'nombre': form.nombre.data,
            'apellido': form.apellido.data,
            'dni': form.dni.data,
            'domicilio': form.domicilio.data,
            'email': form.email.data,
            'localidad': form.localidad.data,
            'telefono': form.telefono.data,
            'profesion': form.profesion.data,
            'puesto_laboral': form.puesto_laboral.data,
            'fecha_inicio': form.fecha_inicio.data,
            'fecha_cese': form.fecha_cese.data,
            'contacto_emergencia_nombre': form.contacto_emergencia_nombre.data,
            'contacto_emergencia_telefono': form.contacto_emergencia_telefono.data,
            'obra_social': form.obra_social.data,
            'nro_afiliado': form.nro_afiliado.data,
            'condicion': form.condicion.data,
            'activo': form.activo.data,
        }

@bp.route('/create', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.EMPLOYEE.name}_{PermissionCategory.NEW}")
def create_employee():
    """Crear un empleado"""
    form = EmployeeForm()
    if form.validate_on_submit():
        new_employee_data = collect_employee_data_from_form(form)
        EmployeeService.add_employee(**new_employee_data)
        flash("Se registro el empleado exitosamente", "success")
        return redirect(url_for('employee_controller.list_employees'))
    return render_template('employee/create.html', form=form)

@bp.route('/list', methods=['GET'])
@check_permissions(f"{PermissionModel.EMPLOYEE.name}_{PermissionCategory.INDEX}")
def index():
    """Listar los empleados"""
    employees = EmployeeService.get_employees()
    return render_template('employee/list.html', employees=employees)

@bp.route('/search', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.EMPLOYEE.name}_{PermissionCategory.INDEX}")
def search_employees():
    form = SearchEmployeeForm()
    employees = []

    if form.validate_on_submit():
        search_params = {}

        if form.nombre.data:
            search_params['nombre'] = form.nombre.data
        if form.apellido.data:
            search_params['apellido'] = form.apellido.data
        if form.dni.data:
            search_params['dni'] = form.dni.data
        if form.email.data:
            search_params['email'] = form.email.data
        if form.puesto_laboral.data:
            search_params['puesto_laboral'] = form.puesto_laboral.data

        employees = EmployeeService.get_employees(filtro=search_params, order_by=form.order_by.data, ascending=form.ascending.data)

    return render_template('employee/search.html', form=form, employees=employees)

@bp.route('/edit/<int:id_employee>', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.EMPLOYEE.name}_{PermissionCategory.UPDATE}")
@handle_error(lambda: url_for('employee_controller.index'))
def edit_employee(employee_id):
    """Editar un empleado existente"""
    employee = EmployeeService.get_employee_by_id(employee_id)
    if not employee:
        flash("El empleado seleccionado no existe", "danger")
        return redirect(url_for('employee_controller.list_employees'))
    form = EmployeeForm(obj=employee)
    if form.validate_on_submit():
        employee_data = collect_employee_data_from_form(form)
        EmployeeService.update_employee(employee, **employee_data)
        flash(f"Empleado {employee.nombre} {employee.apellido} actualizado con éxito", "success")
        return redirect(url_for('employee_controller.list_employees'))
    return render_template('employee/edit.html', form=form, employee=employee)

@bp.route('/delete/<int:id_employee>', methods=['POST'])
@check_permissions(f"{PermissionModel.EMPLOYEE.name}_{PermissionCategory.DESTROY}")
@handle_error(lambda: url_for('employee_controller.index'))
def delete_employee(employee_id):
    """Eliminar un empleado de manera logica"""
    employee = EmployeeService.get_employee_by_id(employee_id)
    if not employee:
        flash("El empleado seleccionado no existe", "danger")
        return redirect(url_for('employee_controller.list_employees'))

    EmployeeService.delete_employee(employee_id)
    flash("Se elimino el empleado exitosamente", "success")
    return redirect(url_for('employee_controller.list_employees'))