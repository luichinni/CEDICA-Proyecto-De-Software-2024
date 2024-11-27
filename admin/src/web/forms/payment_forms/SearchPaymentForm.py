from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, DateField, RadioField, ValidationError
from wtforms.validators import Optional

from src.core.models.Payment import PaymentEnum


class SearchPaymentForm(FlaskForm):
    """Form para buscar pagos por diferentes criterios"""
    start_date = DateField('Fecha de inicio', format='%Y-%m-%d', validators=[Optional()])
    end_date = DateField('Fecha de fin', format='%Y-%m-%d', validators=[Optional()])
    payment_type = SelectField('Tipo de pago',
                               choices=[('', 'No filtrar')] + [(tipo.name, tipo.name.capitalize().replace('_', ' ')) for
                                                               tipo in PaymentEnum])

    ascending = RadioField('Orden', choices=[('1', 'Ascendente'), ('0', 'Descendente')], default='1')

    submit = SubmitField('Buscar pagos')

    def validate_end_date(self, field):
        """
        Valida que la fecha de fin sea mayor o igual a la fecha de inicio.
        """
        if self.start_date.data and field.data:
            if field.data < self.start_date.data:
                raise ValidationError('La fecha de fin debe ser mayor o igual a la fecha de inicio.')
