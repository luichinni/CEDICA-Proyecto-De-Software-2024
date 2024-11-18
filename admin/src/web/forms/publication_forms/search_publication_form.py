from flask_wtf import FlaskForm
from wtforms import StringField, DateField, RadioField, SubmitField, SelectField, ValidationError
from wtforms.validators import Optional

class SearchPublicationForm(FlaskForm):
    title = StringField('Titulo', validators=[Optional()])
    start_published_date = DateField('Fecha de publicacion minima')
    end_published_date = DateField('Fecha de publicacion maxima')

    ascending = RadioField('Orden', choices=[('1', 'Ascendente'), ('0', 'Descendente')], default='1')
    order_by = SelectField('Ordenar por', chocies=[
        ('title', 'Titulo'),
        ('published_date', 'Fecha de publicacion'),
    ])

    submit = SubmitField('Buscar publicaciones')

    def validate_end_published_date(self, field):
        """
        Valida que la fecha de fin sea mayor o igual a la fecha de inicio.
        """
        if self.start_published_date.data and field.data:
            if field.data < self.start_published_date.data:
                raise ValidationError('La fecha de fin debe ser mayor o igual a la fecha de inicio.')