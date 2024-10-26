from core.services.employee_service import EmployeeService
from core.services.equestrian_service import EquestrianService
from flask_wtf import FlaskForm
from web.forms.client_forms.file_widget import CustomFileInput
from wtforms import FieldList, Form, FormField, StringField, DateField, TelField, BooleanField, SelectField, SelectMultipleField, FileField
from wtforms.validators import DataRequired, Length, Regexp, Email
from flask_wtf. file import FileAllowed, FileRequired
from src.core.enums.client_enum import *
from src.web.forms.client_forms.client_form_validators import *
from wtforms.widgets import ListWidget, CheckboxInput

"""
# Datos personales - Formulario 1

    dni = numero de documento (obligatorio)
    nombre = nombre/s legales (obligatorio)
    apellido = apellido/s legales (obligatorio)
    fecha_nacimiento = fecha de nacimiento del JyA (obligatorio)
    lugar_nacimiento = lugar de nacimiento compuesto por localidad y provincia (obligatorio)
    domicilio = domicilio completo, calle, nro, dpto, localidad y provincia (obligatorio con dpto opcional)
    telefono = numero de telefono principal asociado al JyA (obligatorio)
    contacto_emergencia = nombre y telefono del contacto de emergencia del JyA (obligatorio)
"""
class LugarNacimiento(FlaskForm):
    localidad_nacimiento = StringField('Localidad', validators=[DataRequired(),Length(max=100)])
    provincia_nacimiento = StringField('Provincia', validators=[DataRequired(),Length(max=100)])

class Domicilio(FlaskForm):
    calle = StringField('Calle', validators=[DataRequired(), Length(max=50)])
    numero = StringField('Numero', validators=[DataRequired(), Length(max=50)])
    departamento = StringField('Dpto', validators=[Length(max=50)])
    localidad = StringField('Localidad', validators=[DataRequired(), Length(max=50)])
    provincia = StringField('Provincia', validators=[DataRequired(), Length(max=50)])

class ContactoDeEmergencia(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    telefono = TelField('Teléfono', validators=[DataRequired(),Regexp(r'^\+?1?\d{9,15}$')])

class ClientFirstForm(FlaskForm):
    dni = StringField('Dni', validators=[DataRequired(), Length(max=50)])
    nombre = StringField('Nombre/s', validators=[DataRequired(), Length(max=50)])
    apellido = StringField('Apellido/s', validators=[DataRequired(),Length(max=50)])
    fecha_nacimiento = DateField('Fecha de Nacimiento', format='%Y-%m-%d', validators=[DataRequired(), validate_not_in_future])
    lugar_nacimiento = FormField(LugarNacimiento,label='Lugar de Nacimiento')
    domicilio = FormField((Domicilio),label='Domicilio')
    telefono = TelField('Teléfono', validators=[DataRequired(),Regexp(r'^\+?1?\d{9,15}$')])
    contacto_emergencia = FormField((ContactoDeEmergencia), label="Contacto de Emergencia")

"""
# Detalles - Formulario 2

    becado = campo booleano que indica si es becado o no (obligatorio)
    obs_beca = campo de texto obligatorio de la observacion de la beca (obligatorio)
    cert_discapacidad = certificado de discapacidad que posee (obligatorio)
    discapacidad = enumerativo de discapacidad que tiene (obligatorio)
    asignacion = asignacion que percibe (obligatorio)
    pension = pension que percibe (obligatorio)
"""
class ClientSecondForm(FlaskForm):
    becado = BooleanField('Está becado', validators=[])
    obs_beca = StringField('Observaciones de beca')
    cert_discapacidad = SelectField('Certificado de discapacidad que dispone', choices=[ (opcion.value, opcion.name.replace('_',' ').capitalize()) for opcion in Condicion], validators=[DataRequired()])
    otro_cert = StringField('Otro', validators=[OtroCertificadoRequired])
    discapacidad = SelectField('Tipo de Discapacidad', choices=[ (disc.value,disc.name.replace('_',' ').capitalize()) for disc in Discapacidad], validators=[DataRequired()])
    asignacion = SelectField('Asignación Familiar', choices=[(asig.value,asig.name.replace('_',' ').capitalize()) for asig in AsignacionFamiliar], validators=[DataRequired()])
    pension = SelectField('Beneficiario de Pensión', choices=[(pen.value,pen.name.replace('_',' ').capitalize()) for pen in Pension], validators=[DataRequired()])
    
"""
# Situacion previsional - Formulario 3

    obra_social = nombre de la obra social del alumno (obligatorio)
    nro_afiliado = numero de afiliado a dicha obra social (obligatorio)
    curatela = indicativo de si posee o no curatela (obligatorio)
    observaciones = observaciones grales (obligatorio)
"""

class ClientThirdForm(FlaskForm):
    obra_social = StringField('Obra Social del Alumno', validators=[DataRequired(), Length(max=255)])
    nro_afiliado = StringField('Nº Afiliado', validators=[DataRequired(), Length(max=50)])
    curatela = BooleanField('Posee Curatela', validators=[])
    observaciones = StringField('Observaciones', validators=[DataRequired()])
    
"""
# Institucion escolar actual - Formulario 4

    institucion_escolar = informacion completa de la institucion escolar (obligatorio):
        Nombre de la Institución
        Dirección completa 
        Teléfono
        Grado / año actual
        Observaciones
"""
class InstitucionEscolar(FlaskForm):
    nombre = StringField('Nombre de la Institución', validators=[DataRequired(), Length(max=255)])
    direccion = FormField(Domicilio,label="Dirección")
    telefono = TelField('Teléfono', validators=[DataRequired(),Regexp(r'^\+?1?\d{9,15}$')])
    grado = StringField('Grado / año actual', validators=[DataRequired(), Length(max=50)])
    observaciones = StringField('Observaciones')

class ClientFourthForm(FlaskForm):
    institucion_escolar = FormField(InstitucionEscolar)
    
"""
# Profesionales que lo atienden (campo libre) (Opcional) - Formulario 5
"""
class ClientFifthForm(FlaskForm):
    atendido_por = StringField('Profesionales que lo atienden')
    
"""
# Tutores o responsables legales - Formulario 6
    
    tutores_responsables = campo que representa la informacion correspondiente a 1 o varios tutores con:
        Parentesco
        Nombre
        Apellido
        DNI
        Domicilio actual completo
        Celular actual
        e-mail
        Nivel de escolaridad: (máximo nivel alcanzado): Primario – Secundario – Terciario - Universitario
        Actividad u ocupación
"""
class TutoresLegales(FlaskForm):
    parentesco = StringField('Parentesco', validators=[DataRequired()])
    nombre = StringField('Nombre/s', validators=[DataRequired(), Length(max=50)])
    apellido = StringField('Apellido/s', validators=[DataRequired(),Length(max=50)])
    dni = StringField('Dni', validators=[DataRequired(), Length(max=50)])
    domicilio = FormField(Domicilio,label="Dirección")
    telefono = TelField('Teléfono', validators=[DataRequired(),Regexp(r'^\+?1?\d{9,15}$')])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    escolaridad = SelectField('Nivel de escolaridad (máximo alcanzado)', choices=[(nivel.value,nivel.name) for nivel in Escolaridad], validators=[DataRequired()])
    ocupacion = StringField('Actividad u Ocupación', validators=[DataRequired()])

class ClientSixthForm(FlaskForm):
    tutores_responsables = FieldList(FormField(TutoresLegales), label='Tutores o Responsables Legales' ,min_entries=1, max_entries=3)

"""
# Propuesta de trabajo institucional - Formulario 7

    propuesta_trabajo = Tipo de actividad que realiza (enumerativo) (obligatorio)
    condicion = condicion de regular o baja (obligatorio)
    sede = sede en la que realiza actividad (obligatorio)
    dias = dias a la semana en que realiza dicha actividad (obligatorio)
    Profesor/a o Terapeuta: miembro del equipo dado de alta en el sistema (obligatorio)
    Conductor/a del Caballo: miembro del equipo dado de alta en el sistema (obligatorio)
    Caballo:caballo cargado en el sistema (obligatorio)
    Auxiliar de Pista:miembro del equipo dado de alta en el sistema (obligatorio)
"""
class PropuestaDeTrabajo(FlaskForm):
    propuesta_trabajo = SelectField('Propuesta de trabajo institucional',choices=[(prop.value,prop.name.capitalize()) for prop in PropuestasInstitucionales], validators=[DataRequired()])
    condicion = BooleanField('Condicion: Marcar para regular, desmarcar para dado de baja', validators=[])
    sede = StringField('Sede',validators=[DataRequired()])
    dias = SelectMultipleField('Dia/s',
                               choices=[(dia.value, dia.name) for dia in Dias],
                               widget=ListWidget(prefix_label=False),
                               option_widget=CheckboxInput(),
                               validators=[validar_dias])
    profesor_id = SelectField('Profesor/a', choices=[], validators=[DataRequired()])
    conductor_id = SelectField('Conductor/a', choices=[], validators=[DataRequired()])
    caballo_id = SelectField('Caballo', choices=[], validators=[DataRequired()])
    auxiliar_pista_id = SelectField('Auxiliar de pista', choices=[], validators=[DataRequired()])

class ClientSeventhForm(FlaskForm):
    propuesta_trabajo = FormField(PropuestaDeTrabajo,label="Propuesta de Trabajo Institucional")
    
"""
# Formulario de carga de archivos

    titulo = titulo o nombre del archivo
    tipo = tipo segun enumerativo, entrevista, etc
    ubicacion = ubicacion del archivo (ref interna o link)
    es_link = flag que indica si es un archivo externo o interno al servidor
"""

class UploadFile(FlaskForm):
    titulo = StringField('Titulo (opcional)')
    tipo = SelectField('Tipo de Documentación', choices=[(tipo.value,tipo.name.capitalize()) for tipo in TipoDocs])
    archivo = FileField('Seleccionar Archivo (PDF, DOC, XLS o JPEG)', validators=[FileRequired(),FileAllowed([ext.name.lower() for ext in ExtensionesPermitidas],"Formato inválido")], widget=CustomFileInput(False))
    
class UploadLink(FlaskForm):
    titulo = StringField('Nombre de referencia', validators=[DataRequired(), Length(max=100)])
    tipo = SelectField('Tipo de Documentación', choices=[(tipo.value,tipo.name.capitalize()) for tipo in TipoDocs], validators=[DataRequired()])
    archivo = StringField('URL o Link del Documento', validators=[DataRequired()])
    
