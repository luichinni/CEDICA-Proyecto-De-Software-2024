from core.enums.client_enum import ExtensionesPermitidas, TipoDocs
from flask_wtf import FlaskForm
from wtforms.validators import Optional
from wtforms import BooleanField, StringField, SelectField, RadioField, SubmitField

def FileSearchForm(enum_tipo_docs):
    class FileSearchFormClass(FlaskForm):
        titulo = StringField("Titulo", validators=[Optional()]) 
        tipo = SelectField("Tipo de documentación", choices=[
            (tipo.name, tipo.name.replace('_',' ').capitalize()) for tipo in enum_tipo_docs
        ] + [
            ('TODOS', 'Todos')
        ],validators=[Optional()], default="TODOS")
        extension = SelectField("Tipo de archivo", choices=[
            (ext.name.upper(), ext.name.capitalize()) for ext in ExtensionesPermitidas
        ] + [
            ('LINK','Link'), ('TODOS','Todos') 
        ],validators=[Optional()], default="TODOS")
        order_by = SelectField("Ordenar por", choices=[
            ('titulo', 'Titulo'),
            ('tipo', 'Tipo de documentación'),
            ('created_at', 'Fecha de carga')
        ],validators=[Optional()])
        ascending = RadioField('Orden',choices=[('1', 'Ascendente'), ('0', 'Descendente')], default='1', validators=[Optional()])
        deleted = BooleanField('Mostrar eliminados', default=False)
        submit = SubmitField('Buscar archivo')

    return FileSearchFormClass