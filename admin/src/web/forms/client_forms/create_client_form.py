from core.services.employee_service import EmployeeService
from core.services.equestrian_service import EquestrianService
from flask_wtf import FlaskForm
from wtforms import FieldList, Form, FormField, StringField, DateField, TelField, BooleanField, SelectField, SelectMultipleField, FileField
from wtforms.validators import DataRequired, Length, Regexp, Email
from flask_wtf. file import FileAllowed, FileRequired
from src.core.enums.client_enum import *
from src.web.forms.client_forms.client_form_validators import *
from wtforms.widgets import ListWidget, CheckboxInput

"""
# datos personales
    dni = db.Column(db.String(50), nullable=False) 
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    lugar_nacimiento = db.Column(db.String(255), nullable=False)
    domicilio = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    # Contacto de emergencia:			Tel:
    contacto_emergencia = db.Column(db.PickleType(mutable=True), nullable=False)
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
    # lugar de nacimiento -> (localidad y provincia)
    lugar_nacimiento = FormField(LugarNacimiento,label='Lugar de Nacimiento')
    # (calle, número, departamento, localidad, provincia)
    domicilio = FormField((Domicilio),label='Domicilio')
    telefono = TelField('Teléfono', validators=[DataRequired(),Regexp(r'^\+?1?\d{9,15}$')])
    # contacto_emergencia es un pickle que guardaré como un dict contacto_emergencia = {nombre: "", telefono: ""}
    contacto_emergencia = FormField((ContactoDeEmergencia), label="Contacto de Emergencia")

"""
# datos personales 2
    becado = db.Column(db.Boolean, nullable=True)
    obs_beca = db.Column(db.Text, nullable=False)
    cert_discapacidad = db.Column(db.String(255), nullable=True) # enum condicion va al front para esto.
    discapacidad = db.Column(Enum(Discapacidad), nullable=False)
    asignacion = db.Column(Enum(AsignacionFamiliar), nullable=True)
    pension = db.Column(Enum(Pension), nullable=True)
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
# situacion previsional
    
    Obra Social del Alumno:
    Nº afiliado:
    ¿Posee curatela? (si/no):
    Observaciones:
    
    obra_social = db.Column(db.String(255), nullable=False)
    nro_afiliado = db.Column(db.String(50), nullable=False)
    curatela = db.Column(db.Boolean, nullable=False)
    observaciones = db.Column(db.Text, nullable=False)
"""

class ClientThirdForm(FlaskForm):
    obra_social = StringField('Obra Social del Alumno', validators=[DataRequired(), Length(max=255)])
    nro_afiliado = StringField('Nº Afiliado', validators=[DataRequired(), Length(max=50)])
    curatela = BooleanField('Posee Curatela', validators=[])
    observaciones = StringField('Observaciones', validators=[DataRequired()])
    
"""
# inst escolar actual
    
    Nombre de la Institución:
    Dirección:
    Teléfono:
    Grado / año actual:
    Observaciones:
    
    institucion_escolar = db.Column(db.PickleType(mutable=True), nullable=True)
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
# profesionales q lo atienden (campo libre)
    atendido_por = db.Column(db.Text, nullable=False)
"""
class ClientFifthForm(FlaskForm):
    atendido_por = StringField('Profesionales que lo atienden')
    
"""
# tutores o responsables legales
    
    Parentesco:
    Nombre:
    Apellido
    DNI:
    Domicilio actual (calle, nº, piso, depto., localidad, provincia):
    Celular actual:
    e-mail:
    Nivel de escolaridad: (máximo nivel alcanzado): Primario – Secundario – Terciario - Universitario
    Actividad u ocupación:
    
    tutores_responsables = db.Column(db.PickleType(mutable=True), nullable=False)
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
# actividad q realiza
    
    Propuesta de trabajo institucional: Opciones desplegables: Hipoterapia – Monta Terapéutica – Deporte Ecuestre Adaptado – Actividades Recreativas - Equitación
    Condición: REGULAR – DE BAJA
    SEDE: CASJ  -  HLP   - OTRO
    DÍA: Lunes, Martes, Miércoles, Jueves, Viernes, Sábado, Domingo (puede seleccionarse más de un dia)
    Profesor/a o Terapeuta: miembro del equipo dado de alta en el sistema
    Conductor/a del Caballo: miembro del equipo dado de alta en el sistema
    Caballo:caballo cargado en el sistema
    Auxiliar de Pista:miembro del equipo dado de alta en el sistema
    
    propuesta_trabajo = db.Column(Enum(PropuestasInstitucionales), nullable=False)
    condicion = db.Column(db.Boolean, nullable=False)
    sede = db.Column(db.String(100), nullable=False)
    dias = db.Column(db.PickleType(mutable=True), nullable=False)
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
cargar múltiples archivos (formatos permitidos PDF, DOC, XLS, JPEG) o enlaces a archivos externos (por ej, a un Drive, Dropbox, etc). 
Los mismos aportan información complementaria. Junto con la subida del archivo o link deberá asociarse un tipo de documentación 
(entrevista, evaluación, planificaciones, evolución, crónicas, documental) como una forma de clasificarlos.

    título, fecha en la que se agregó el enlace, tipo

    titulo = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.Enum(TipoDocs), nullable=False)
    ubicacion = db.Column(db.Text, nullable=False)
    es_link = db.Column(db.Boolean, nullable=False)
    
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    cliente = db.relationship('Clients', back_populates='archivos')

"""

class UploadFile(FlaskForm):
    titulo = StringField('Titulo (opcional)')
    tipo = SelectField('Tipo de Documentación', choices=[(tipo.value,tipo.name.capitalize()) for tipo in TipoDocs])
    archivo = FileField('Seleccionar Archivo (PDF, DOC, XLS o JPEG)', validators=[FileRequired(),FileAllowed([ext.name.lower() for ext in ExtensionesPermitidas],"Formato inválido")])
    
class UploadLink(FlaskForm):
    titulo = StringField('Nombre de referencia', validators=[DataRequired(), Length(max=100)])
    tipo = SelectField('Tipo de Documentación', choices=[(tipo.value,tipo.name.capitalize()) for tipo in TipoDocs], validators=[DataRequired()])
    archivo = StringField('URL o Link del Documento', validators=[DataRequired()])