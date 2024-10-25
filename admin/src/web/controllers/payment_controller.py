from flask import render_template, Blueprint, redirect, url_for, flash, request

from core.enums.permission_enums import PermissionModel, PermissionCategory
from src.core.services.PaymentService import PaymentService
from src.web.forms.payment_forms.PaymentForm import PaymentForm
from src.web.forms.search_form import SearchForm
from src.web.handlers.auth import check_permissions
from web.handlers import handle_error, get_int_param

bp = Blueprint('payments', __name__, url_prefix='/payments')

#TODO: ADD 'SHOW' FEATURE AND CHECK PERMISSIONS

@bp.route('/', methods=['GET'])
@check_permissions(f"{PermissionModel.PAYMENT.value}_{PermissionCategory.INDEX.value}")
def index():
    params = request.args
    page = get_int_param(params, 'page', 1, optional= True)
    per_page = get_int_param(params, 'per_page', 25, optional=True)

    payments, total, pages = PaymentService.get_payments(page=page, per_page=per_page)

    lista_diccionarios = [payment.to_dict() for payment in payments]

    return render_template('list.html', lista_diccionarios=lista_diccionarios, entidad="payment")


@bp.route('/search', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.PAYMENT.value}_{PermissionCategory.INDEX.value}")
def search():
    form = SearchForm()

    payment_fields = PaymentService.get_model_fields()
    form.tipo_filtro.choices = [(campo, campo.replace('_',' ').capitalize()) for campo in payment_fields]
    form.orden_filtro.choices = [(campo, campo.replace('_', ' ').capitalize()) for campo in payment_fields]

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
    payments, total, pages = PaymentService.get_payments(filtro=filtro, page=page, per_page=per_page,
                                                            order_by=order_by, ascending=ascending)
    listado = [
      {
          'id': payment.id,
          'Beneficiario': payment.beneficiario_id, #TODO: DEBERIA APARECER EL NOMBRE DEL BENEFICIARIO MEJOR
          'Monto': payment.monto,
          'Fecha de Pago': payment.fecha_pago,
          'Tipo de Pago': payment.tipo_pago,
          'Descripcion': payment.descripcion,
          'Empleado' : payment.empleado #TODO: DEBERIA APARECER EL NOMBRE DEL EMPLEADO MEJOR
      } for payment in payments] if payments else [{
        'id': '0',
        'Beneficiario': '0',
        'Monto': '0',
        'Fecha de Pago': '',
        'Tipo de Pago': '',
        'Descripcion': '',
        'Empleado': '0'
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

@bp.route('/create', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.PAYMENT.name}_{PermissionCategory.NEW.value}")
def create_payment():
    form = PaymentForm()
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
        return redirect(url_for('payment.index'))
    return render_template('payment/create.html', form=form)

@bp.route('/delete/<int:payment_id>', methods=['POST'])
@check_permissions(f"{PermissionModel.PAYMENT.value}_{PermissionCategory.DESTROY}")
@handle_error(lambda: url_for('payment.index'))
def delete_payment(payment_id):
    payment = PaymentService.get_payment_by_id(payment_id)
    flash('Pago eliminado exitosamente', 'success')
    return redirect(url_for('payment.index'))

@bp.route('/edit/<int:payment_id>', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.PAYMENT.value}_{PermissionCategory.UPDATE}")
@handle_error(lambda: url_for('payment.index'))
def update_payment(payment_id):
    payment = PaymentService.get_payment_by_id(payment_id)
    form = PaymentForm()
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
        return redirect(url_for('payment.index'))
    return render_template('payment/edit.html', form=form, payment=payment)

