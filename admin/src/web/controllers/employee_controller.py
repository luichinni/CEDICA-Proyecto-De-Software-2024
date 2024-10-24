from flask import render_template, Blueprint, redirect, request, url_for, flash

from src.core.services.employee_service import EmployeeService
from web.forms.employee_forms.CreateEmployeeForm import CreateEmployeeForm
from web.forms.employee_forms.EditEmployeeForm import EditEmployeeForm
from web.forms.search_form import SearchForm
from web.handlers.auth import check_permissions
from web.handlers import handle_error, get_int_param
from src.core.enums.permission_enums import PermissionCategory, PermissionModel

bp = Blueprint('employees', __name__, url_prefix='/employee')

def collect_employee_data_from_form(form):
    """Retorna los datos del form en formato de diccionario"""
    return {
            'nombre': form.nombre.data,
            'apellido': form.apellido.data,
            'dni': form.dni.data,
            'domicilio': form.domicilio.data,
            'localidad': form.localidad.data,
            'telefono': form.telefono.data,
            'profesion': form.profesion.data.upper(),
            'puesto_laboral': form.puesto_laboral.data.upper(),
            'fecha_inicio': form.fecha_inicio.data,
            'fecha_cese': form.fecha_cese.data,
            'contacto_emergencia_nombre': form.contacto_emergencia_nombre.data,
            'contacto_emergencia_telefono': form.contacto_emergencia_telefono.data,
            'obra_social': form.obra_social.data,
            'nro_afiliado': form.nro_afiliado.data,
            'condicion': form.condicion.data.replace(' ','_').upper(),
            'activo': form.activo.data,
        }

@bp.route('/create', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.NEW.value}")
def new():
    """Crear un empleado"""
    form = CreateEmployeeForm()
    if form.validate_on_submit():
        new_employee_data = collect_employee_data_from_form(form)
        new_employee_data['email'] : form.email.data
        EmployeeService.add_employee(**new_employee_data)
        flash("Se registro el empleado exitosamente", "success")
        return redirect(url_for('employee.search'))
    context = {
        'form': form,
        'titulo': 'Crear un empleado',
        'url_post': url_for('employee.new'),
        'url_volver': url_for('employee.search')
    }
    return render_template('form.html', **context)

@bp.route('/', methods=['GET'])
@check_permissions(f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.INDEX.value}")
def index():
    """Listar los empleados"""
    params = request.args
    page = get_int_param(params, 'page', 1, True)
    per_page = get_int_param(params, 'per_page', 25, True)

    employees, total, pages = EmployeeService.get_employees(page=page, per_page=per_page)

    lista_diccionarios = [employee.to_dict() for employee in employees]
    return render_template('list.html', lista_diccionarios=lista_diccionarios, entidad="employee")

@bp.route('/search', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.INDEX.value}")
def search():
    form = SearchForm()

    employee_fields = EmployeeService.get_model_fields()
    form.tipo_filtro.choices = [(campo, campo.replace('_',' ').capitalize()) for campo in employee_fields]
    form.orden_filtro.choices = [(campo, campo.replace('_', ' ').capitalize()) for campo in employee_fields]

    params = request.args
    page = int(params.get('page', 1))
    per_page = int(params.get('per_page', 25))
    order_by = params.get('order_by', None)
    ascending = params.get('ascending', 'Ascendente') == 'Ascendente'

    filtro = None
    for param, valor in params.items():
        if param in form._fields:
            form._fields[param].data = valor

    if params.get('tipo_filtro', None) and params.get('busqueda', '') != '':
        filtro = {
            params['tipo_filtro']: params.get('busqueda')
        }
    employees, total, pages = EmployeeService.get_employees(filtro=filtro, page=page, per_page=per_page,
                                                            order_by=order_by, ascending=ascending)
    listado = [
      {
          'id': employee.id,
          'Nombre': employee.nombre,
          'Apellido': employee.apellido,
          'DNI': employee.dni,
          'Email': employee.email,
          'Puesto Laboral': employee.puesto_laboral
      } for employee in employees] if employees else [{
        'id': '0',
        'Nombre': '',
        'Apellido': '',
        'DNI': '',
        'Email': '',
        'Puesto Laboral': ''
    }]

    return render_template('search_box.html',
                                              form=form,
                                              entidad='employees',
                                              anterior=url_for('home'),
                                              lista_diccionarios=listado,
                                              total=total,
                                              current_page=page,
                                              per_page =per_page,
                                              pages=pages,
                                              titulo='Listado de empleados')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.UPDATE.value}")
@handle_error(lambda: url_for('employee.search'))
def update(employee_id):
    """Editar un empleado existente"""
    employee = EmployeeService.get_employee_by_id(employee_id)
    if not employee:
        flash("El empleado seleccionado no existe", "danger")
        return redirect(url_for('employee.list_employees'))
    form = EditEmployeeForm(obj=employee)
    if form.validate_on_submit():
        employee_data = collect_employee_data_from_form(form)
        EmployeeService.update_employee(employee, **employee_data)
        flash(f"Empleado {employee.nombre} {employee.apellido} actualizado con éxito", "success")
        return redirect(url_for('employee.list_employees'))
    context = {
        'form': form,
        'titulo': 'Crear un empleado',
        'url_post': url_for('employee.update'),
        'url_volver': url_for('employee.seach')
    }
    return render_template('form.html', **context)

@bp.route('/delete/<int:id>', methods=['POST'])
@check_permissions(f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.DESTROY.value}")
@handle_error(lambda: url_for('employee.search'))
def delete(employee_id):
    """Eliminar un empleado de manera logica"""
    employee = EmployeeService.get_employee_by_id(employee_id)
    if not employee:
        flash("El empleado seleccionado no existe", "danger")
    else:
        EmployeeService.delete_employee(employee_id)
        flash("Se elimino el empleado exitosamente", "success")
    return redirect(url_for('employee.search'))

@bp.route('<int:id>', methods=['GET'])
@check_permissions(f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.SHOW.value}")
@handle_error(lambda: url_for('employee.search'))
def detail(employee_id):
    employee = EmployeeService.get_employee_by_id(employee_id)
    if not employee:
        flash(f'Empleado con ID {employee_id} no encontrado', 'warning')
        return redirect(url_for('employees.search_employees'))


    titulo = f'Detalle del empleado {employee.nombre} {employee.apellido}',
    anterior = url_for('employee.search'),
    diccionario = employee.to_dict(),
    entidad = 'employee'

    return render_template('detail.html', titulo=titulo, anterior=anterior, diccionario= diccionario, entidad=entidad )