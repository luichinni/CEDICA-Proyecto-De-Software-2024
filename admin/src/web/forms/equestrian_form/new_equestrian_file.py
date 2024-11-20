from core.enums.client_enum import ExtensionesPermitidas
from core.enums.equestrian_enum import TipoEnum
from flask_wtf import FlaskForm
from wtforms import FileField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired


class UploadFile(FlaskForm):
    titulo = StringField('Titulo (opcional)')
    tipo = SelectField('Tipo de Documentación', choices=[(tipo.value,tipo.name.capitalize()) for tipo in TipoEnum])
    archivo = FileField('Seleccionar Archivo (PDF, DOC, XLS o JPEG)', validators=[FileRequired(),FileAllowed([ext.name.lower() for ext in ExtensionesPermitidas],"Formato inválido")])
    submit = SubmitField('Cargar')

class UploadLink(FlaskForm):
    titulo = StringField('Nombre de referencia', validators=[DataRequired(), Length(max=100)])
    tipo = SelectField('Tipo de Documentación', choices=[(tipo.value,tipo.name.capitalize()) for tipo in TipoEnum], validators=[DataRequired()])
    archivo = StringField('URL o Link del Documento', validators=[DataRequired()])
    submit = SubmitField('Cargar')