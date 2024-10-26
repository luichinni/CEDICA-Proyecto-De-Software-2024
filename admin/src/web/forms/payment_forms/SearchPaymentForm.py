from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField, DateField, FormField
from wtforms.validators import Optional
from src.core.enums.payment_enum.PaymentEnum import PaymentEnum
from web.forms.search_form import SearchForm

class RangoFechas(FlaskForm):
    fecha_desde = DateField('Fecha desde', format='%Y-%m-%d')
    fecha_hasta = DateField('Fecha hasta', format='%Y-%m-%d')

class SearchPaymentForm(SearchForm):
    """Form para buscar pagos por diferentes criterios"""
    rango_fechas = FormField(RangoFechas)
    tipo_pago = SelectField('Tipo de pago',
                            choices=[(tipo.name, tipo.name.capitalize().replace('_', ' ')) for tipo in PaymentEnum])

    submit = SubmitField('Aplicar')

