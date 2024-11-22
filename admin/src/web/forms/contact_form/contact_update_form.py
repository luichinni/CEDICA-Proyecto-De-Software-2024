from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, SubmitField, TextAreaField
from wtforms import Field
from wtforms.widgets import TextArea
from core.enums.message import StatuEnum
from wtforms.validators import Optional


class ContactUpdateForm(FlaskForm):    
    info = TextAreaField('Mensaje', default="No se pudo cargar el mensaje",render_kw = {'readonly': True}  )
    status = SelectField(choices=[(opcion.name, opcion.name.replace('_',' ').capitalize()) for opcion in StatuEnum ],
                         validators=[Optional()]) 
    coment= StringField("Ingrese un comentario",validators=[Optional()])
    submit = SubmitField('Aceptar')