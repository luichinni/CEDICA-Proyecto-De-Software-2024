from src.core.database import db
from src.core.models.Payment import Payment

class PaymentService:

    @staticmethod
    def create_payment(data):
        new_payment = Payment(**data)
        db.session.add(new_payment)
        db.session.commit()
        return new_payment

    @staticmethod
    def update_payment(payment_id, data):
        payment = Payment.query.get(payment_id)
        if not payment:
            raise ValueError('El pago no existe')
        for key, value in data.items():
            setattr(payment, key, value)
        db.session.add(payment)
        db.session.commit()
        return payment

    @staticmethod
    def delete_payment(payment_id):
        payment = PaymentService.get_payment_by_id(payment_id)
        if not payment:
            raise ValueError('El pago no existe')
        payment.deleted = True
        db.session.commit()
        return payment

    @staticmethod
    def get_payments(filtro=None, order_by=None, ascending=False, include_deleted=False):
        """Toma pagos basado en los filtros y el orden"""
        payments_query = Payment.query.filter_by(deleted=include_deleted)
        if filtro:
            valid_filters = {key:value for key, value in filtro.items() if hasattr(Payment, key) and value is not None}
            payments_query = payments_query.filter_by(**valid_filters)

        if order_by:
            if ascending:
                payments_query = payments_query.order_by(getattr(Payment, order_by).asc())
            else:
                payments_query = payments_query.order_by(getattr(Payment, order_by).desc())
        return payments_query.all()

    @staticmethod
    def get_payment_by_id(payment_id, include_deleted=False):
        payment = Payment.query.get(payment_id)
        if not payment:
            raise ValueError('El pago no existe')
        return payment
