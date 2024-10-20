from datetime import datetime, timezone
from src.core.database import db
from src.core.enums.client_enum import * # solo hay enums
from .client_docs import *

class Clients(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # datos personales
    dni = db.Column(db.String(50), nullable=False) 
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    lugar_nacimiento = db.Column(db.String(255), nullable=False)
    domicilio = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    # Contacto de emergencia:			Tel:
    contacto_emergencia = db.Column(db.PickleType, nullable=False)

    # datos personales 2
    becado = db.Column(db.Boolean, nullable=True)
    obs_beca = db.Column(db.Text, nullable=False)
    cert_discapacidad = db.Column(db.String(255), nullable=True) # enum condicion va al front para esto.
    discapacidad = db.Column(db.Enum(Discapacidad), nullable=False)
    asignacion = db.Column(db.Enum(AsignacionFamiliar), nullable=True)
    pension = db.Column(db.Enum(Pension), nullable=True)

    # situacion previsional
    """
    Obra Social del Alumno:
    Nº afiliado:
    ¿Posee curatela? (si/no):
    Observaciones:
    """
    obra_social = db.Column(db.String(255), nullable=False)
    nro_afiliado = db.Column(db.String(50), nullable=False)
    curatela = db.Column(db.Boolean, nullable=False)
    observaciones = db.Column(db.Text, nullable=False)

    # inst escolar actual
    """
    Nombre de la Institución:
    Dirección:
    Teléfono:
    Grado / año actual:
    Observaciones:
    """
    institucion_escolar = db.Column(db.PickleType, nullable=True)

    # profesionales q lo atienden (campo libre)
    atendido_por = db.Column(db.Text, nullable=False)

    # tutores o responsables legales
    """
    Parentesco:
    Nombre:
    Apellido
    DNI:
    Domicilio actual (calle, nº, piso, depto., localidad, provincia):
    Celular actual:
    e-mail:
    Nivel de escolaridad: (máximo nivel alcanzado): Primario – Secundario – Terciario - Universitario
    Actividad u ocupación:
    """
    tutores_responsables = db.Column(db.PickleType, nullable=False)

    # actividad q realiza
    """
    Propuesta de trabajo institucional: Opciones desplegables: Hipoterapia – Monta Terapéutica – Deporte Ecuestre Adaptado – Actividades Recreativas - Equitación
    Condición: REGULAR – DE BAJA
    SEDE: CASJ  -  HLP   - OTRO
    DÍA: Lunes, Martes, Miércoles, Jueves, Viernes, Sábado, Domingo (puede seleccionarse más de un dia)
    Profesor/a o Terapeuta: miembro del equipo dado de alta en el sistema
    Conductor/a del Caballo: miembro del equipo dado de alta en el sistema
    Caballo:caballo cargado en el sistema
    Auxiliar de Pista:miembro del equipo dado de alta en el sistema
    """
    propuesta_trabajo = db.Column(db.Enum(PropuestasInstitucionales), nullable=False)
    condicion = db.Column(db.Boolean, nullable=False)
    sede = db.Column(db.String(100), nullable=False)
    dias = db.Column(db.PickleType, nullable=False)
    
    profesor_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    profesor = db.relationship('Employee', backref="terapea", foreign_keys=[profesor_id]) # TODO agregarlo a employee

    conductor_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    conductor = db.relationship('Employee', backref="conduce_para", foreign_keys=[conductor_id]) # TODO agregarlo a employee

    caballo_id = db.Column(db.Integer, db.ForeignKey('equestrians.id'), nullable=False)
    caballo = db.relationship('Equestrian', backref="clientes")

    auxiliar_pista_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    auxiliar = db.relationship('Employee', backref="auxilia", foreign_keys=[auxiliar_pista_id]) # TODO agregarlo a employee

    archivos = db.relationship('ClientDocuments', back_populates="cliente")

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))  
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)) 
    deleted = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"<Client id={self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            'dni': self.dni,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
