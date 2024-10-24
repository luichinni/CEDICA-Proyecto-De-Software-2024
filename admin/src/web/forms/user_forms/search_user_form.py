from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, SubmitField
from src.core.services.role_service import RoleService

class SearchUserForm(FlaskForm):
    email = StringField('Email')
    
    # SelectField para permitir "no filtrar", "filtrar por True", "filtrar por False"
    activo = SelectField('Activo', choices=[
        ('', 'No filtrar'),  # Opción para no filtrar
        ('1', 'Activo'),     # Filtrar por usuarios activos
        ('0', 'Inactivo')    # Filtrar por usuarios inactivos
    ])
    
    role_id = SelectField('Rol', coerce=int)  # Se espera un ID entero, pero se muestra el nombre del rol
    order_by = SelectField('Ordenar por', choices=[
        ('created_at', 'Fecha de creación'),
        ('email', 'Email')
    ])
    
    ascending = RadioField('Orden', choices=[('1', 'Ascendente'), ('0', 'Descendente')], default='1')
    submit = SubmitField('Aplicar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        role_choices = [(r.id, r.name) for r in RoleService.get_all_roles()]
        if not role_choices:
            raise ValueError("No hay roles disponibles.")

        self.role_id.choices = role_choices
