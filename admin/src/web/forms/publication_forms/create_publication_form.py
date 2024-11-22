from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Length
from src.core.models.publication import PublicationStatusEnum


class CreatePublicationForm(FlaskForm):
    title = StringField(
        'Titulo',
        validators=[
            DataRequired(),
            Length(max=100, message="El titulo no debe exceder los 100 caracteres.")
        ]
    )
    summary = StringField(
        'Copete',
        validators=[
            DataRequired(),
            Length(max=255, message="El copete no debe exceder los 255 caracteres")
        ]
    )

    body = TextAreaField('Contenido', validators=[DataRequired()],
            render_kw={"class": "form-control", "placeholder": "Escribe el contenido aquí..."})
    status = SelectField(
        'Estado',
        choices=[(estado.name, estado.name.replace('_',' ')) for estado in PublicationStatusEnum],
        validators=[DataRequired()]
    )
    published_at = DateField('Fecha de publicacion', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Guardar')