from flask import render_template, Blueprint, redirect, request, url_for, flash
from src.core.services import employee_service
from web.forms.employee_forms.EmployeeForm import EmployeeForm

bp = Blueprint('employee_controller', __name__, url_prefix='/employee')

@bp.route('/create', methods=['GET', 'POST'])
def create_employee():
    """Crear un empleado"""
    form = EmployeeForm()
    if form.validate_on_submit():
        new_employee_data = {
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
            'contacto_emergencia': form.contacto_emergencia.data,
            'obra_social': form.obra_social.data,
            'nro_afiliado': form.nro_afiliado.data,
            'condicion': form.condicion.data,
            'activo': form.activo.data,
        }
        employee_service.add_employee(**new_employee_data)
        flash("Se registro el empleado exitosamente", "success")
        return redirect(url_for('employee_controller.list_employees'))
    return render_template('employee/create.html', form=form)

@bp.route('/list', methods=['GET'])
def list_employees():
    """Listar los empleados"""
    employees = employee_service.get_employees()
    return render_template('employee/list.html', employees=employees)

@bp.route('/edit/<int:id_employee>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    """Editar un empleado existente"""
    employee = employee_service.get_employee_by_id(employee_id)
    if not employee:
        flash("El empleado seleccionado no existe", "danger")
        return redirect(url_for('employee_controller.list_employees'))
    form = EmployeeForm(obj=employee)
    if form.validate_on_submit():
        employee_data = {
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
            'contacto_emergencia': form.contacto_emergencia.data,
            'obra_social': form.obra_social.data,
            'nro_afiliado': form.nro_afiliado.data,
            'condicion': form.condicion.data,
            'activo': form.activo.data,
        }
        employee_service.update_employee(employee, **employee_data)
        flash(f"Empleado {employee.nombre} {employee.apellido} actualizado con éxito", "success")
        return redirect(url_for('employee_controller.list_employees'))
    return render_template('employee/edit.html', form=form, employee=employee)

@bp.route('/delete/<int:id_employee>', methods=['POST'])
def delete_employee(employee_id):
    """Eliminar un empleado de manera logica"""
    employee = employee_service.get_employee_by_id(employee_id)
    if not employee:
        flash("El empleado seleccionado no existe", "danger")
        return redirect(url_for('employee_controller.list_employees'))

    employee_service.delete_employee(employee_id)
    flash("Se elimino el empleado exitosamente", "success")
    return redirect(url_for('employee_controller.list_employees'))