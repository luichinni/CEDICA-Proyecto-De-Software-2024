from flask import render_template, Blueprint, redirect, url_for, flash, request

from core.enums.permission_enums import PermissionModel, PermissionCategory
from src.core.services.PaymentService import PaymentService
from src.core.services.employee_service import EmployeeService
from src.web.forms.payment_forms.PaymentForm import PaymentForm
from src.web.handlers.auth import check_permissions
from web.forms.payment_forms.SearchPaymentForm import SearchPaymentForm
from web.handlers import handle_error, get_int_param

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
    form = SearchPaymentForm()

    form.tipo_filtro.choices = [('rango_fechas','Rango de fechas'), ('tipo_pago','Tipo de pago')]
    form.orden_filtro.choices = [('fecha_pago', 'Fecha de pago')]

    params = request.args
    page = int(params.get('page', 1))
    per_page = int(params.get('per_page', 5))
    ascending = params.get('ascending', 'Ascendente') == 'Ascendente'

    order_by = 'fecha_pago'

    filtro = None
    for param, valor in params.items():
        if param in form._fields:
            form._fields[param].data = valor

    if params.get('tipo_pago'):
        filtro['tipo_pago'] = params.get('tipo_pago')
    elif params.get('rango_fechas-fecha_hasta') and params.get('rango_fechas-fecha_desde'):
        filtro['rango_fechas'] = {
            'desde': params.get('rango_fechas-fecha_desde'),
            'hasta': params.get('rango_fechas-fecha_hasta')
        }


    pagos, total, pages = PaymentService.get_payments(
        filtro=filtro,
        page=page,
        per_page=per_page,
        order_by=order_by,
        ascending=ascending
    )

    listado = [
        {
            'id': pago.id,
            'Fecha de Pago': pago.fecha_pago,
            'Monto': pago.monto,
            'Tipo de Pago': pago.tipo_pago.name,
            'Descripción': pago.descripcion,
        } for pago in pagos
    ] if pagos else [{
        'id': '0',
        'Fecha de Pago': '',
        'Monto': '',
        'Tipo de Pago': '',
        'Descripción': ''
    }]

    return render_template(
        'search_payment.html',
        form=form,
        entidad='payments',
        anterior=url_for('home'),
        lista_diccionarios=listado,
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
    form.beneficiario.choices = [(empleado.id, f"{empleado.nombre.capitalize()} {empleado.apellido.capitalize()}") for empleado in empleados]
    if form.validate_on_submit():
        new_payment = {
            'beneficiario_id': form.beneficiario.data,
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
@handle_error(lambda: url_for('payments.search'))
def delete(payment_id):
    payment = PaymentService.get_payment_by_id(payment_id)
    if not payment:
        flash("El pago seleccionado no existe", "danger")
    else:
        PaymentService.delete_payment(payment_id)
        flash('Pago eliminado exitosamente', 'success')
    return redirect(url_for('payments.search'))

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.PAYMENT.value}_{PermissionCategory.UPDATE.value}")
@handle_error(lambda: url_for('payments.search'))
def update(payment_id):
    payment = PaymentService.get_payment_by_id(payment_id)
    form = PaymentForm(obj=payment)
    if form.validate_on_submit():
        updated_payment = {
            'beneficiario_id': form.beneficiario.data,
            'monto': form.monto.data,
            'fecha_pago': form.fecha_pago.data,
            'tipo_pago': form.tipo_pago.data,
            'descripcion': form.descripcion.data
        }
        PaymentService.update_payment(payment_id, updated_payment)
        flash('Pago actualizado exitosamente', 'success')
        return redirect(url_for('payments.search'))
    context = {
        'form': form,
        'titulo': 'Editar un pago',
        'url_post': url_for('payments.update'),
        'url_volver': url_for('payments.search')
    }
    return render_template('form.html', **context)

@bp.route('<int:id>', methods=['GET'])
@check_permissions(f"{PermissionModel.PAYMENT.value}_{PermissionCategory.SHOW.value}")
@handle_error(lambda: url_for('payments.search'))
def detail(id):
    payment = PaymentService.get_payment_by_id(id)
    if not id:
        flash(f'Pago con ID {id} no encontrado', 'warning')
        return redirect(url_for('payments.search'))


    titulo = f'Detalle del pago {payment.nombre} {payment.apellido}',
    anterior = url_for('payments.search'),
    diccionario = payment.to_dict(),
    entidad = 'payments'

    return render_template('detail.html', titulo=titulo, anterior=anterior, diccionario= diccionario, entidad=entidad )

