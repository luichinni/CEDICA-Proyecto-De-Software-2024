from flask import render_template, Blueprint, redirect, url_for, flash

from core.enums.permission_enums import PermissionModel, PermissionCategory
from src.core.services.PaymentService import PaymentService
from src.web.forms.payment_forms.PaymentForm import PaymentForm
from src.web.forms.payment_forms.SearchPaymentForm import SearchPaymentForm
from src.web.handlers.auth import check_permissions
bp = Blueprint('payment_controller', __name__, url_prefix='/payments')

#TODO: ADD 'SHOW' FEATURE AND CHECK PERMISSIONS

@bp.route('/', methods=['GET'])
@check_permissions(f"{PermissionModel.PAYMENT.value}_{PermissionCategory.INDEX.value}")
def index():
    payments = PaymentService.get_payments()
    return render_template('payment/index.html', payments=payments)

@bp.route('/search', methods=['GET'])
@check_permissions(f"{PermissionModel.PAYMENT.value}_{PermissionCategory.INDEX.value}")
def search():
    form = SearchPaymentForm()
    payments = []
    if form.validate_on_submit():
        search_params = {
            'fecha_inferior': form.fecha_inferior.data,
            'fecha_superior': form.fecha_superior.data,
            'tipo_pago': form.tipo_pago.data,
            'order_by': form.order_by.data,
            'ascending': form.ascending.data
        }
        payments = PaymentService.get_payments(search_params)

    return render_template('payment/search.html', form=form, payments=payments)

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
        return redirect(url_for('payment_controller.index'))
    return render_template('payment/create.html', form=form)

@bp.route('/delete/<int:payment_id>', methods=['POST'])
@check_permissions(f"{PermissionModel.PAYMENT.value}_{PermissionCategory.DESTROY}")
def delete_payment(payment_id):
    payment = PaymentService.get_payment_by_id(payment_id)
    flash('Pago eliminado exitosamente', 'success')
    return redirect(url_for('payment_controller.index'))

@bp.route('/edit/<int:payment_id>', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.PAYMENT.value}_{PermissionCategory.UPDATE}")
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
        return redirect(url_for('payment_controller.index'))
    return render_template('payment/edit.html', form=form, payment=payment)

