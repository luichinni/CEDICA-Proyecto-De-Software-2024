from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, SubmitField, DateField
from wtforms.validators import DataRequired, Optional, ValidationError
from src.core.models.collection import PaymentMethod

class SearchCollectionForm(FlaskForm):
    employee_name = StringField('Nombre de empleado', validators=[Optional()]) 
    employee_last_name = StringField('Apellido de empleado', validators=[Optional()]) 
    employee_email = StringField('Email de empleado', validators=[Optional()]) 
    
    client_dni = StringField('DNI de J&A', validators=[Optional()]) 

    start_date = DateField('Fecha de inicio', format='%Y-%m-%d', validators=[Optional()]) 
    end_date = DateField('Fecha de fin', format='%Y-%m-%d', validators=[Optional()]) 

    payment_method = SelectField('Método de Pago', choices=[('', 'No filtrar')] + [(method.value, method.value) for method in PaymentMethod],
                                  validators=[Optional()])    
    
    ascending = RadioField('Orden', choices=[('1', 'Ascendente'), ('0', 'Descendente')], default='1')
    submit = SubmitField('Buscar cobros')

    def validate_end_date(self, field):
        """
        Valida que la fecha de fin sea mayor o igual a la fecha de inicio.
        """
        if self.start_date.data and field.data:
            if field.data < self.start_date.data:
                raise ValidationError('La fecha de fin debe ser mayor o igual a la fecha de inicio.')
