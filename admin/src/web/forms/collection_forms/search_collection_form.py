from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, SubmitField, DateField
from wtforms.validators import DataRequired, Optional, ValidationError
from datetime import datetime
from src.core.services.role_service import RoleService

class SearchCollectionForm(FlaskForm):
    nombre = StringField('Nombre', validators=[Optional()])  # Campo opcional
    apellido = StringField('Apellido', validators=[Optional()])  # Campo opcional

    start_date = DateField('Fecha de inicio', format='%Y-%m-%d', validators=[Optional()])  # Campo de fecha
    end_date = DateField('Fecha de fin', format='%Y-%m-%d', validators=[Optional()])  # Campo de fecha

    payment_method = StringField('Método de pago', validators=[Optional()])  # Campo opcional
    
    ascending = RadioField('Orden', choices=[('1', 'Ascendente'), ('0', 'Descendente')], default='1')
    submit = SubmitField('Aplicar')

    def validate_end_date(self, field):
        """
        Valida que la fecha de fin sea mayor o igual a la fecha de inicio.
        """
        if self.start_date.data and field.data:
            if field.data < self.start_date.data:
                raise ValidationError('La fecha de fin debe ser mayor o igual a la fecha de inicio.')
