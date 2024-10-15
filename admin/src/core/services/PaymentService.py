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
        payment = Payment.query.get(payment_id)
        if not payment:
            raise ValueError('El pago no existe')
        db.session.delete(payment)
        db.session.commit()
        return payment

    @staticmethod
    def get_payments(filters):
        payments_query = Payment.query
        if 'fecha_inicio' in filters and 'fecha_fin' in filters:
            payments_query = payments_query.filter(Payment.fecha_pago.between(filters['fecha_inicio'], filters['fecha_fin']))
        if 'tipo_pago' in filters:
            payments_query = payments_query.filter_by(tipo_pago=filters['tipo_pago'])
        return payments_query.all()

    @staticmethod
    def get_payment_by_id(payment_id):
        payment = Payment.query.get(payment_id)
        if not payment:
            raise ValueError('El pago no existe')
        return payment
