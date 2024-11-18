from src.core.database import db
from src.core.models.Payment import Payment
from sqlalchemy import and_

class PaymentService:

    @staticmethod
    def get_model_fields():
        return [column.name for column in Payment.__table__.columns]

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
    def get_payments(filtro=None, order_by=None, ascending=False, include_deleted=False, page=1, per_page=5):
        """Toma pagos basado en los filtros y el orden"""
        payments_query = Payment.query.filter_by(deleted=include_deleted)
        if filtro:
            if 'tipo_pago' in filtro and filtro['tipo_pago']:
                payments_query = payments_query.filter(Payment.tipo_pago == filtro['tipo_pago'])
            if 'start_date' in filtro and filtro['start_date']:
                payments_query = payments_query.filter(Payment.fecha_pago >= filtro['start_date'])
            if 'end_date' in filtro and filtro['end_date']:
                payments_query = payments_query.filter(Payment.fecha_pago <= filtro['end_date'])

        if order_by:
            column = Payment.fecha_pago
        else:
            column = Payment.created_at

        payments_query = payments_query.order_by(column.asc() if ascending else column.desc())

        pagination = payments_query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total, pagination.pages

    @staticmethod
    def get_payment_by_id(payment_id, include_deleted=False):
        payment = Payment.query.get(payment_id)
        if not payment:
            raise ValueError('El pago no existe')
        return payment
