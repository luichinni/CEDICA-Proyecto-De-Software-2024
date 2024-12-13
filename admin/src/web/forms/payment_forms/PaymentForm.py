from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField, FloatField, TextAreaField
from wtforms.validators import Optional, DataRequired, ValidationError

from src.core.models.Payment import PaymentEnum


class PaymentForm(FlaskForm):
    beneficiario = SelectField("Beneficiario", coerce=int, validators=[Optional()])
    monto = FloatField("Monto", validators=[DataRequired()])
    fecha_pago = DateField("Fecha del pago", format='%Y-%m-%d', validators=[DataRequired()])
    tipo_pago = SelectField("Tipo Pago", choices=[(payment.name) for payment in PaymentEnum],
                            validators=[DataRequired()])
    descripcion = TextAreaField("Descripcion", validators=[DataRequired()])
    submit = SubmitField("Registrar pago")

    def validate_beneficiario(self, field):
        if self.tipo_pago.data == "HONORARIOS" and (field.data is None or field.data == 0):
            raise ValidationError("El beneficiario es obligatorio para pagos de tipo HONORARIOS.")
