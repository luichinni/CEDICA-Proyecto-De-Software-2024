from datetime import datetime, timezone
from src.core.database import db
from src.core.enums.client_enum import * # solo hay enums
from .client_docs import *

class Clients(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dni = db.Column(db.String(50), nullable=False) 
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    lugar_nacimiento = db.Column(db.PickleType, nullable=False)
    """
    {
        'calle':,
        'numero':,
        'departamento':,
        'localidad':,
        'provincia':
    }
    """
    domicilio = db.Column(db.PickleType, nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    contacto_emergencia = db.Column(db.PickleType, nullable=False)
    """
    {
        nombre:,
        telefono:
    }
    """
    becado = db.Column(db.Boolean, nullable=True)
    obs_beca = db.Column(db.Text, nullable=False)
    cert_discapacidad = db.Column(db.String(255), nullable=True) # enum condicion va al front para esto.
    discapacidad = db.Column(db.Enum(Discapacidad), nullable=False)
    asignacion = db.Column(db.Enum(AsignacionFamiliar), nullable=True)
    pension = db.Column(db.Enum(Pension), nullable=True)
    obra_social = db.Column(db.String(255), nullable=False)
    nro_afiliado = db.Column(db.String(50), nullable=False)
    curatela = db.Column(db.Boolean, nullable=False)
    observaciones = db.Column(db.Text, nullable=False)
    
    institucion_escolar = db.Column(db.PickleType, nullable=True)
    """
    {
        'nombre':,
        'direccion':{
            'calle':,
            'numero':,
            'departamento':,
            'localidad':,
            'provincia':
        }, 
        'telefono':,
        'grado':,
        'observaciones':
    }
    """
    atendido_por = db.Column(db.Text, nullable=False)
    tutores_responsables = db.Column(db.PickleType, nullable=False)
    """
    [{
            'parentesco':,
            'nombre':,
            'apellido':,
            'dni':,
            'domicilio': {
                'calle':,
                'numero':,
                'departamento':,
                'localidad':,
                'provincia':
            }, 
            'telefono':,
            'email':,
            'escolaridad':,
            'ocupacion':
        },...]
    """
    propuesta_trabajo = db.Column(db.Enum(PropuestasInstitucionales), nullable=False)
    condicion = db.Column(db.Boolean, nullable=False)
    sede = db.Column(db.String(100), nullable=False)
    dias = db.Column(db.PickleType, nullable=False)
    
    profesor_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    profesor = db.relationship('Employee', backref="terapea", foreign_keys=[profesor_id])

    conductor_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    conductor = db.relationship('Employee', backref="conduce_para", foreign_keys=[conductor_id])

    caballo_id = db.Column(db.Integer, db.ForeignKey('equestrians.id'), nullable=False)
    caballo = db.relationship('Equestrian', backref="clientes")

    auxiliar_pista_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    auxiliar = db.relationship('Employee', backref="auxilia", foreign_keys=[auxiliar_pista_id])

    archivos = db.relationship('ClientDocuments', back_populates="cliente")

    deudor = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))  
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)) 
    deleted = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"<Client id={self.id}>"

    def to_dict(self, include_id=True):
        jya_dict = {
            "id": self.id,
            "dni": self.dni,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_nacimiento": self.fecha_nacimiento,
            "lugar_nacimiento": self.lugar_nacimiento,
            "domicilio": self.domicilio,
            "telefono": self.telefono,
            "contacto_emergencia": self.contacto_emergencia,
            "becado": self.becado,
            "obs_beca": self.obs_beca,
            "deudor": self.deudor,
            "cert_discapacidad": self.cert_discapacidad,
            "discapacidad": self.discapacidad.value,
            "asignacion": self.asignacion.value,
            "pension": self.pension.value,
            "obra_social": self.obra_social,
            "nro_afiliado": self.nro_afiliado,
            "curatela": self.curatela,
            "observaciones": self.observaciones,
            "institucion_escolar": self.institucion_escolar,
            "atendido_por": self.atendido_por,
            "tutores_responsables": list(self.tutores_responsables.values()),
            "propuesta_trabajo": self.propuesta_trabajo,
            "condicion": self.condicion,
            "sede": self.sede,
            "dias": self.dias,
            "profesor_id": self.profesor_id,
            "conductor_id": self.conductor_id,
            "auxiliar_pista_id": self.auxiliar_pista_id,
            "caballo_id": self.caballo_id
        }

        if not include_id:
            del jya_dict['id']
        
        return jya_dict