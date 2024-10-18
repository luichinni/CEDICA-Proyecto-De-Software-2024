from flask import render_template, Blueprint, redirect, url_for, flash
from src.core.services.PaymentService import PaymentService
from src.web.forms.payment_forms.PaymentForms import PaymentForm
bp = Blueprint('payment_controller', __name__, url_prefix='/payments')

@bp.route('/', methods=['GET'])
def index():
    payments = PaymentService.get_payments()
    return render_template('payment/index.html', payments=payments)

@bp.route('/create', methods=['GET', 'POST'])
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
def delete_payment(payment_id):
    payment = PaymentService.get_payment_by_id(payment_id)
    flash('Pago eliminado exitosamente', 'success')
    return redirect(url_for('payment_controller.index'))

@bp.route('/edit/<int:payment_id>', methods=['GET', 'POST'])
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

