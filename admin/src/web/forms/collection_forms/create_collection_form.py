from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, FloatField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from src.core.models.collection import PaymentMethod
from src.core.services.employee_service import EmployeeService
from src.core.services.client_service import ClientService
from src.core.admin_data import AdminData

class CreateCollectionForm(FlaskForm):
    employee_id = SelectField('Empleado', coerce=int, validators=[DataRequired(message="El empleado es requerido.")])
    client_id = SelectField('J&A', coerce=int, validators=[DataRequired(message="El J&A es requerido.")])
    
    payment_date = DateField('Fecha de Pago', format='%Y-%m-%d', validators=[DataRequired(message="La fecha de pago es requerida.")])
    
    payment_method = SelectField('Método de Pago', choices=[(method.value, method.value) for method in PaymentMethod],
                                  validators=[DataRequired(message="El método de pago es requerido.")])
    
    amount = FloatField('Monto', validators=[DataRequired(message="El monto es requerido."), NumberRange(min=0.01, message="El monto debe ser mayor a 0.")])
    
    observations = StringField('Observaciones', validators=[Optional(), Length(max=255, message="Las observaciones no pueden exceder 255 caracteres.")])
    
    submit = SubmitField('Crear Colección')

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        admin_email = AdminData.email
        employee_choices = [(e.id, e.email) for e in EmployeeService.get_employees()[0] if e.email != admin_email]
        if not employee_choices:
            raise ValueError("No hay empleados registrados.")
        self.employee_id.choices = employee_choices

        client_choices = [(e.id, e.dni) for e in ClientService.get_clients()[0]]
        if not client_choices:
            raise ValueError("No hay clientes registrados.")
        self.client_id.choices = client_choices