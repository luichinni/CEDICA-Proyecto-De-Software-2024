from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, FloatField, StringField, SubmitField, HiddenField
from wtforms.validators import Length, Optional, NumberRange
from src.core.models.collection import PaymentMethod

class UpdateCollectionForm(FlaskForm):
    payment_date = DateField('Fecha de Pago', format='%Y-%m-%d', validators=[Optional()])
    
    payment_method = SelectField('Método de Pago', choices=[(method.value, method.value) for method in PaymentMethod], 
                                  validators=[Optional()])
    
    amount = FloatField('Monto', validators=[Optional(), NumberRange(min=0.01, message="El monto debe ser mayor a 0.")])
    
    observations = StringField('Observaciones', validators=[Optional(), Length(max=255, message="Las observaciones no pueden exceder 255 caracteres.")])
    
    submit = SubmitField('Actualizar Colección')

    def __init__(self, collection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        """Llena el formulario con los datos del objeto Collection."""
        self.payment_date.data = collection.payment_date.date() if collection.payment_date else None 
        self.payment_method.data = collection.payment_method.value
        self.amount.data = collection.amount
        self.observations.data = collection.observations