from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, FloatField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from src.core.models.collection import PaymentMethod

class CreateCollectionForm(FlaskForm):
    employee_id = SelectField('Empleado', coerce=int, validators=[DataRequired(message="El empleado es requerido.")])
    
    client_dni = StringField('Cliente', validators=[DataRequired(message="El cliente es requerido.")])   

    payment_date = DateField('Fecha de Pago', format='%Y-%m-%d', validators=[DataRequired(message="La fecha de pago es requerida.")])
    
    payment_method = SelectField('Método de Pago', choices=[(method.value, method.value) for method in PaymentMethod],
                                  validators=[DataRequired(message="El método de pago es requerido.")])
    
    amount = FloatField('Monto', validators=[DataRequired(message="El monto es requerido."), NumberRange(min=0.01, message="El monto debe ser mayor a 0.")])
    
    observations = StringField('Observaciones', validators=[Optional(), Length(max=255, message="Las observaciones no pueden exceder 255 caracteres.")])
    
    submit = SubmitField('Crear Colección')
