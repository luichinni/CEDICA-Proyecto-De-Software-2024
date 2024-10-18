from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField, DateField
from wtforms.validators import Optional
from src.core.enums.payment_enum.PaymentEnum import PaymentEnum

class SearchPaymentForm(FlaskForm):
    """Form para buscar pagos por diferentes criterios"""
    fecha_inferior = DateField('Fecha inferior',format='%Y-%m-%d', validators=[Optional()])
    fecha_superior = DateField('Fecha superior',format='%Y-%m-%d', validators=[Optional()])
    tipo_pago = SelectField('Tipo de pago', choices=[
        (tipo.name, tipo.value) for tipo in PaymentEnum
    ], validators=[Optional()])
    order_by = SelectField('Ordenar por', choices=[
        ('fecha_pago', 'Fecha del pago'),
    ], validators=[Optional()])

    ascending = SelectField('Orden', choices=[
        ('asc', 'Ascendente'),
        ('desc', 'Descendente')
    ], validators=[Optional()])

    submit = SubmitField('Buscar')
