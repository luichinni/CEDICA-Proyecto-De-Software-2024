from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField, FloatField, TextAreaField
from wtforms.validators import Optional, DataRequired
from src.core.models.Payment import PaymentEnum

class PaymentForm(FlaskForm):
    beneficiario = SelectField("Beneficiario", coerce=int, validators=[Optional()])
    monto = FloatField("Monto", validators=[DataRequired()])
    fecha_pago = DateField("Fecha del pago", format='%Y-%m-%d', validators=[DataRequired()])
    tipo_pago = SelectField("Tipo Pago", choices=[(payment.name) for payment in PaymentEnum], validators=[DataRequired()])
    descripcion = TextAreaField("Descripcion", validators=[DataRequired()])
    submit = SubmitField("Registrar pago")