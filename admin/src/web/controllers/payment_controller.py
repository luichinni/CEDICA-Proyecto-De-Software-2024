from datetime import datetime

from flask import render_template, Blueprint, redirect, url_for, flash, request

from core.enums.permission_enums import PermissionModel, PermissionCategory
from src.core.services.PaymentService import PaymentService
from src.core.services.employee_service import EmployeeService
from src.web.forms.payment_forms.PaymentForm import PaymentForm
from src.web.handlers.auth import check_permissions
from web.forms.payment_forms.SearchPaymentForm import SearchPaymentForm
from web.handlers import handle_error, get_int_param, get_str_param, get_bool_param

bp = Blueprint('payments', __name__, url_prefix='/payments')


@bp.route('/', methods=['GET'])
@check_permissions(f"{PermissionModel.PAYMENT.value}_{PermissionCategory.INDEX.value}")
def index():
    params = request.args
    page = get_int_param(params, 'page', 1, optional= True)
    per_page = get_int_param(params, 'per_page', 5, optional=True)

    payments, total, pages = PaymentService.get_payments(page=page, per_page=per_page)

    lista_diccionarios = [payment.to_dict() for payment in payments]

    return render_template('list.html', lista_diccionarios=lista_diccionarios, entidad="payment")


@bp.route('/search', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.PAYMENT.value}_{PermissionCategory.INDEX.value}")
def search():
    """Buscar pagos con filtros"""

    params = request.args

    start_date_str = get_str_param(params, 'start_date', optional=True)
    end_date_str = get_str_param(params, 'end_date', optional=True)

    filtros = {'start_date' : datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None,
                'end_date' : datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None,
               'tipo_pago': get_str_param(params, 'tipo_pago', optional=True)}

    page = get_int_param(params, 'page', 1, optional=True)
    per_page = get_int_param(params, 'per_page', 5, optional=True)
    order_by_date = get_bool_param(params, 'order_by_date', default=True, optional=True)
    ascending = params.get('ascending', 'Ascendente') == 'Ascendente'

    payments, total, pages = PaymentService.get_payments(
        filtro=filtros,
        order_by=order_by_date,
        ascending=ascending,
        page=page,
        per_page=per_page
    )

    payments_list = [payment.to_dict() for payment in payments]

    params_dict = params.to_dict()
    # Manejar start_date y end_date para que no de error al pasar **params_dict

    if 'start_date' in params_dict:
        if not params_dict['start_date']:
            del params_dict['start_date']
        else:
            params_dict['start_date'] = datetime.strptime(params_dict['start_date'], '%Y-%m-%d').date()

    if 'end_date' in params_dict:
        if not params_dict['end_date']:
            del params_dict['end_date']
        else:
            params_dict['end_date'] = datetime.strptime(params_dict['end_date'], '%Y-%m-%d').date()

    form = SearchPaymentForm(**params_dict)

    return render_template(
        'search_payment.html',
        form=form,
        entidad='payments',
        anterior=url_for('home'),
        lista_diccionarios=payments_list,
        total=total,
        current_page=page,
        per_page=per_page,
        pages=pages,
        titulo='Listado de Pagos'
    )

@bp.route('/create', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.PAYMENT.value}_{PermissionCategory.NEW.value}")
def new():
    form = PaymentForm()
    empleados = EmployeeService.get_all_employees()
    form.beneficiario.choices = [(0, "No aplica")] + [(empleado.id, f"{empleado.nombre.capitalize()} {empleado.apellido.capitalize()}") for empleado in empleados]
    if form.validate_on_submit():
        new_beneficiario_id = form.beneficiario.data

        if new_beneficiario_id == 0:
            new_beneficiario_id = None

        new_payment = {
            'beneficiario_id': new_beneficiario_id,
            'monto': form.monto.data,
            'fecha_pago': form.fecha_pago.data,
            'tipo_pago': form.tipo_pago.data,
            'descripcion': form.descripcion.data
        }
        PaymentService.create_payment(new_payment)
        flash('Pago registrado exitosamente', 'success')
        return redirect(url_for('payments.search'))
    context = {
        'form': form,
        'titulo': 'Cargar un pago',
        'url_post': url_for('payments.new'),
        'url_volver': url_for('payments.search')
    }
    return render_template('form.html', **context)

@bp.route('/delete/<int:id>', methods=['POST'])
@check_permissions(f"{PermissionModel.PAYMENT.value}_{PermissionCategory.DESTROY.value}")
@handle_error(lambda id: url_for('payments.search'))
def delete(id):
    payment = PaymentService.get_payment_by_id(id)
    if not payment:
        flash("El pago seleccionado no existe", "danger")
    else:
        PaymentService.delete_payment(id)
        flash('Pago eliminado exitosamente', 'success')
    return redirect(url_for('payments.search'))

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.PAYMENT.value}_{PermissionCategory.UPDATE.value}")
@handle_error(lambda id: url_for('payments.search'))
def update(id):
    payment = PaymentService.get_payment_by_id(id)
    form = PaymentForm(obj=payment)
    empleados = EmployeeService.get_all_employees()
    form.beneficiario.choices = [(0, "No aplica")] + [(empleado.id, f"{empleado.nombre.capitalize()} {empleado.apellido.capitalize()}") for empleado in empleados]
    if form.validate_on_submit():
        updated_payment = {
            'beneficiario_id': form.beneficiario.data,
            'monto': form.monto.data,
            'fecha_pago': form.fecha_pago.data,
            'tipo_pago': form.tipo_pago.data,
            'descripcion': form.descripcion.data
        }
        PaymentService.update_payment(id, updated_payment)
        flash('Pago actualizado exitosamente', 'success')
        return redirect(url_for('payments.search'))
    context = {
        'form': form,
        'titulo': 'Editar un pago',
        'url_post': url_for('payments.update', id=id),
        'url_volver': url_for('payments.search')
    }
    return render_template('form.html', **context)

@bp.route('<int:id>', methods=['GET'])
@check_permissions(f"{PermissionModel.PAYMENT.value}_{PermissionCategory.SHOW.value}")
@handle_error(lambda : url_for('payments.search'))
def detail(id):
    payment = PaymentService.get_payment_by_id(id)
    if not id:
        flash(f'Pago con ID {id} no encontrado', 'warning')
        return redirect(url_for('payments.search'))


    titulo = f'Detalle del pago'
    anterior = url_for('payments.search')
    diccionario = payment.to_dict()
    diccionario['beneficiario'] = EmployeeService.get_employee_by_id(diccionario['beneficiario'])
    entidad = 'payments'

    return render_template('detail.html', titulo=titulo, anterior=anterior, diccionario= diccionario, entidad=entidad )

